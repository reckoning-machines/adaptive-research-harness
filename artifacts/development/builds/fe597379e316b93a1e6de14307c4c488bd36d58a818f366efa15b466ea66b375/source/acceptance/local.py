"""Disposable cooperative integration fixture; same core/actors/tools, no OS isolation claim.

Core, each actor invocation and A/B workers are separate actual processes.
Tokens bind cooperative test actors to ingress; same-UID attackers are outside
this fixture's claims. Linux peer credentials and UID isolation remain separate.
"""
from pathlib import Path
import argparse
import json
import os
import secrets
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from adaptive_research_harness.encoding import canonical,decode,digest,Refusal,require
from adaptive_research_harness.clock import durable_write,SyntheticClock
from adaptive_research_harness.transport import receive,send,request,LifetimeLock,DropReply
from adaptive_research_harness.client import Client
from adaptive_research_harness.profile import Profile
from .runtime import Runtime

ROOT=Path(__file__).resolve().parents[1]
BUNDLE=ROOT/'docs/builds/first_cycle_20261029/run_bundle'


def local_serve(path,handler,allowed):
    """Private fixture sockets; assumed same-user identity, never OS-isolation evidence."""
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():path.unlink()
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as server:
        server.bind(str(path));os.chmod(path,0o600);server.listen(64)
        def connection(conn):
            with conn:
                try:send(conn,handler({'uid':20000,'pid':0},receive(conn)))
                except DropReply:pass
                except (Refusal,OSError,EOFError,ValueError,KeyError,TypeError) as exc:
                    try:send(conn,{'status':'ERROR','reason':getattr(exc,'code','OPERATIONAL_ERROR'),'detail':str(exc)})
                    except OSError:pass
        while True:
            conn,_=server.accept();threading.Thread(target=connection,args=(conn,),daemon=True).start()


class LocalClient(Client):
    def __init__(self,config,actor):
        super().__init__(Path(config['state'])/'core.sock',actor);self.token=config['tokens'][actor]
    def call(self,op,payload=None,key=None):
        return request(self.path,{'actor':self.actor,'op':op,'payload':payload or {},'request_id':key or str(uuid.uuid4()),'token':self.token,'pid':os.getpid()})


def process_generation(config,pid=None):return {'pid':pid or os.getpid(),'run':config['run_id']}


def local_quiescence(path,inventory,core,worker):
    require(Path(path).is_file(),'WORKER_NOT_QUIESCENT');proof=decode(Path(path).read_bytes())
    require(proof['inventory_sha256']==inventory and proof.get('channels_discarded') is True,'WORKER_NOT_QUIESCENT')
    for old in (core,worker):
        if old is None:continue
        require(old in proof['terminated_generations'],'WORKER_NOT_QUIESCENT')
        try:os.kill(old['pid'],0)
        except ProcessLookupError:continue
        raise Refusal('WORKER_NOT_QUIESCENT')
    return proof


def worker(mode,config_path,label=None):
    global BUNDLE
    config=decode(Path(config_path).read_bytes());BUNDLE=Path(config['bundle']);state=Path(config['state']);profile=Profile(BUNDLE)
    if mode=='core':
        from adaptive_research_harness.storage import Store
        from adaptive_research_harness.engine import Engine
        from adaptive_research_harness.dispatch import Dispatcher
        from adaptive_research_harness.service import core_handler,Faults
        permission=profile.development_permission(ROOT,state)
        class Clock:
            def read(self):
                require(not (state/'clock-off').exists(),'CLOCK_UNAVAILABLE')
                return SyntheticClock(state/'clock.json',profile.setup['clock']).read()
        with LifetimeLock(state/'writer.lock'):
            store=Store(state/'harness.sqlite');engine=Engine(store,profile,Clock(),permission)
            faults=Faults(engine,state/'faults',lambda:process_generation(config));engine.fault_hook=faults.hit
            dispatcher=Dispatcher(engine,{t:str(state/(l+'.sock')) for t,l in [('SYN-A-1','tool-a'),('SYN-B-1','tool-b')]},state/'supervisor',generation_value=process_generation(config),quiescence_verifier=local_quiescence)
            engine.dispatcher=dispatcher
            handler=core_handler(engine,dispatcher,faults,lambda pid:process_generation(config,pid))
            uids={v:k for k,v in profile.roles.items()}
            def ingress(who,b):
                token=b.pop('token',None);pid=b.pop('pid',None)
                require(token is not None and secrets.compare_digest(token,config['tokens'].get(b.get('actor'),'')),'ACTOR_MISMATCH')
                return handler({'uid':uids[b['actor']],'pid':pid},b)
            local_serve(state/'core.sock',ingress,set())
    elif mode=='tool':
        from adaptive_research_harness.tool_worker import run_worker
        run_worker({'tool-a':'SYN-A-1','tool-b':'SYN-B-1'}[label],state/(label+'.sock'),state/label,profile,serve_function=local_serve,generation_provider=lambda:process_generation(config))
    else:
        from adaptive_research_harness import actors
        data=decode(sys.stdin.buffer.read());client=LocalClient(config,label);op=data['op'];p=data.get('payload',{})
        def hook(point):
            fault=state/('actor-'+label+'.fault')
            if not fault.exists() or decode(fault.read_bytes())['point']!=point:return
            fault.unlink();paused=state/(digest([label,point,os.getpid()])+'.paused')
            durable_write(paused,{'point':point,'generation':process_generation(config)})
            while not paused.with_suffix('.release').exists():time.sleep(.01)
        try:
            if op=='independent-read':
                from .reader import read
                result=read(client)
            elif op=='check':result=actors.check(client,p['transition_id'],hook)
            elif op=='research':result=actors.research(client,p.get('tool','SYN-A-1'),p.get('stop_after'))
            elif op=='complete-research':result=actors.complete_research(client,p['attempt'])
            elif op=='propose-mutated':result=actors.propose_mutated(client,**p)
            elif op=='propose-hypothesis':result=actors.propose_hypothesis(client,p['research_ref'],p.get('previous'))
            elif op=='propose-successor':result=actors.propose_successor(client,p['case'],p['ordinal'])
            elif op=='observe':result=actors.observe(client,p.get('date','2026-10-28'),p.get('form','DOCUMENT'))
            elif op=='settle-pending':result=actors.recover_settlement(client,p['attempt'])
            elif op=='retry-research':result=actors.retry_research(client,p['attempt'])
            elif op=='inspect-request':result=client.query(op,p)
            elif op=='close-reservation':result=client.call('close',p)
            elif op=='reserve':result=client.call(op,p,data.get('request_id'))
            elif op=='adversarial-command':
                require(p['command'] not in ('propose','research-commit'),'INVALID_CASE')
                result=client.call(p['command'],p['payload'],p.get('request_id'))
            elif op=='peer-impersonation':
                result=request(client.path,{'actor':p['actor'],'op':'fence','payload':{'grant':'AU-RP-1','reason':'negative'},'request_id':str(uuid.uuid4()),'token':client.token,'pid':os.getpid()})
            else:raise Refusal('CAPABILITY_UNSUPPORTED',op)
        except (Refusal,OSError,EOFError,ValueError,KeyError,TypeError) as exc:result={'status':'ERROR','reason':getattr(exc,'code','OPERATIONAL_ERROR'),'detail':str(exc)}
        print(canonical(result).decode())


class LocalRuntime(Runtime):
    def __init__(self,case,output):
        from concurrent.futures import ThreadPoolExecutor
        self.case=case;self.pool=ThreadPoolExecutor(8);self.ordinal=0;self.trace=[]
        self.state=Path(tempfile.mkdtemp(prefix='arh-',dir='/private/tmp' if sys.platform=='darwin' else '/tmp'))
        self.output=Path(output);self.processes=[];self.dead=[];self.logfiles=[];self.mutex=threading.Lock()
        profile=Profile(BUNDLE);self.config={'bundle':str(BUNDLE),'state':str(self.state),'run_id':uuid.uuid4().hex,'tokens':{actor:secrets.token_hex(24) for actor in profile.roles.values()}}
        durable_write(self.state/'DISPOSABLE.json',{'disposable':True,'run_id':self.config['run_id']})
        self.config_path=self.state/'fixture.json';durable_write(self.config_path,self.config)
        self.client=LocalClient(self.config,'Principal')
    def launch(self,mode,label=None):
        args=[sys.executable,'-m','acceptance.local','--worker',mode,'--config',str(self.config_path)]
        if label:args+=['--label',label]
        if mode=='actor':
            proc=subprocess.Popen(args,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        else:
            log=open(self.state/(mode+'-'+str(label)+'.log'),'ab');self.logfiles.append(log)
            proc=subprocess.Popen(args,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=log,stderr=log)
        with self.mutex:self.processes.append((mode,label,proc))
        return proc
    def ready(self):
        deadline=time.monotonic()+15
        while time.monotonic()<deadline:
            try:
                self.read('profile')
                if all((self.state/(x+'.sock')).exists() for x in ('tool-a','tool-b')):return
            except (OSError,EOFError,Refusal):pass
            time.sleep(.02)
        raise AssertionError('Local core failed: '+str([p.read_text() for p in self.state.glob('*.log')]))
    def adversarial(self,actor,command,payload,request_id=None):
        return self.agent(actor,'adversarial-command',{'case':{'X02':'R01','X03':'R14','X04':'R12'}.get(self.case,self.case.split('.')[0]),'command':command,'payload':payload,'request_id':request_id})
    def agent(self,actor,op,payload=None,request_id=None):
        identity={'ck1':'AD-CK-1.0','ck2':'AD-CK-2.0','observe':'Observation function'}.get(actor, f'AD-R{int(actor[1:])}.0' if actor.startswith('r') else actor)
        proc=self.launch('actor',identity)
        out,err=proc.communicate(canonical({'op':op,'payload':payload or {},'request_id':request_id}),timeout=45)
        r=decode(out) if out.strip() else {'status':'ERROR','reason':'PROCESS_INTERRUPTED','detail':err.decode()}
        self.trace.append({'agent':actor,'op':op,'pid':proc.pid,'result':r});return r
    def tick(self,value):return {'time_ms':SyntheticClock(self.state/'clock.json',Profile(BUNDLE).setup['clock']).advance(value)}
    def startup(self):
        self.host('new-case',case=self.case);self.ready()
        # Reuse the actual startup recipe without its Linux-only clock/socket preamble.
        return self.startup_records()
    def stop(self,only=None):
        with self.mutex:processes=list(self.processes)
        for mode,label,p in processes:
            if only and mode!=only:continue
            if p.poll() is None:p.kill()
            p.wait(timeout=5)
            g=process_generation(self.config,p.pid)
            if g not in self.dead:self.dead.append(g)
        return processes
    def host(self,op,**p):
        if op=='new-case':
            clock=SyntheticClock(self.state/'clock.json',Profile(BUNDLE).setup['clock']);clock.initialize()
            for label in ('tool-a','tool-b'):self.launch('tool',label)
            self.launch('core');return {'status':'NEW_EMPTY_CASE'}
        if op in ('restart','quiesce'):
            old=list(self.dead);processes=self.stop();proof={'inventory_sha256':Profile(BUNDLE).inventory_hash,'terminated_generations':self.dead,'channels_discarded':True,'old_channels_closed':True}
            cores=[process_generation(self.config,proc.pid) for mode,label,proc in processes if mode=='core']
            for g in cores:durable_write(self.state/'supervisor'/(digest(g)+'.json'),proof)
            if op=='restart':
                for label in ('tool-a','tool-b'):self.launch('tool',label)
                self.launch('core')
            return {'proof':proof}
        if op in ('kill','stop','start'):
            unit=p['unit'];mode='core' if unit=='harness-core.service' else 'tool'
            if unit=='harness-clock.service':
                off=self.state/'clock-off'
                if op=='start':off.unlink(missing_ok=True)
                else:off.touch()
            elif op=='start':self.launch(mode)
            else:self.stop(mode)
            return {'status':'DONE'}
        if op=='barriers':return {'barriers':[{'path':str(x),'content':decode(x.read_bytes())} for x in self.state.rglob('*.paused')]}
        if op=='release-barrier':durable_write(Path(p['path']).with_suffix('.release'),{});return {'status':'RELEASED'}
        if op=='pause-actor':
            label={'ck1':'AD-CK-1.0','ck2':'AD-CK-2.0'}[p['actor']];durable_write(self.state/('actor-'+label+'.fault'),{'point':p['point']});return {'status':'ARMED'}
        if op in ('rollback-clock','restore-clock'):
            clock=self.state/'clock.json';receipts=[decode(x) for x in clock.with_suffix('.receipts').read_bytes().splitlines()]
            durable_write(clock,receipts[0] if op=='rollback-clock' else receipts[-1]);return {'status':'DONE'}
        if op=='competing-core':
            proc=self.launch('core');proc.wait(timeout=10)
            return {'returncode':0 if proc.returncode else 1,'stdout':(self.state/'core-None.log').read_text(),'stderr':''}
        if op=='artifact-probe':
            import shutil
            profile=Profile(BUNDLE)
            with tempfile.TemporaryDirectory(prefix='arh-candidate-') as d:
                root=Path(d)
                for item in profile.inventory['files']:
                    q=root/item['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/item['path'],q)
                target=root/'adaptive_research_harness/checkers/a.py';target.write_bytes(target.read_bytes()+b'\n# deliberate candidate mutation\n')
                try:profile.verify_files(root)
                except Refusal as exc:return {'status':'CANDIDATE_REFUSED','reason':exc.code,'actual_candidate_bytes_changed':True}
                raise AssertionError('Changed source accepted')
        raise Refusal('ISOLATION_UNVERIFIED',op)
    def verify_artifacts(self):Profile(BUNDLE).verify_files(ROOT)
    def finish(self):
        result=self.agent('Principal','independent-read');require(result.get('status')=='RECONSTRUCTED','READER_FAILED');self.trace.append({'independent_reader':result})
        return {'case':self.case,'status':'PASS','os_isolation':'UNVERIFIED','records':result}
    def close(self,report):
        self.stop();self.pool.shutdown(wait=True,cancel_futures=True)
        for log in self.logfiles:log.close()
        self.output.mkdir(parents=True,exist_ok=True)
        profile=Profile(BUNDLE)
        coverage={'B10':{'status':'SUBSTITUTED','tested':'Whole-core outage and exact reconstruction','unexecuted':'Transition-ledger-only outage; shared SQLite carrier has no independent ledger service'},'R14':{'status':'PARTIAL','tested':'Known scientific failures','unreachable':'Constitutional NOT DETERMINABLE/STOP branch in this bounded language'}}.get(self.case,{'status':'COOPERATIVE'})
        report.update(coverage=coverage,state_directory=str(self.state),inventory_sha256=profile.inventory_hash,source_snapshot=str(ROOT/'artifacts/development/builds'/profile.inventory_hash),tested_files=profile.inventory['files'],trace=self.trace)
        try:profile.verify_files(ROOT)
        except Refusal as exc:report.update(status='FAIL',error='SOURCE_CHANGED_DURING_RUN: '+str(exc))
        durable_write(self.output/(self.case+'.json'),report)
        # Keep the database, failures and useful logs; remove capability tokens.
        self.config_path.unlink(missing_ok=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',choices=['core','actor','tool']);parser.add_argument('--config');parser.add_argument('--label');parser.add_argument('--case',action='append');parser.add_argument('--example',action='store_true');parser.add_argument('--output',default='artifacts/development/latest');parser.add_argument('--jobs',type=int,default=1)
    args=parser.parse_args()
    if args.worker:return worker(args.worker,args.config,args.label)
    global BUNDLE
    run_id=uuid.uuid4().hex
    args.output=str(Path(args.output)/run_id)
    BUNDLE=ROOT/'artifacts/development/run-bundles'/run_id/'bundle'
    from build_support.freeze import freeze
    freeze(BUNDLE)
    print('Run evidence:',args.output,flush=True)
    from .catalog import CASES,DEATH_POINTS
    from . import cases,death
    selected=args.case or (['E01'] if args.example else [x for x in CASES if x!='T06']+['D-'+x for x in DEATH_POINTS]+['D-terminal-apply','D-terminal-invalidate','X01','X02','X03','X04','X05'])
    def execute(case):
        r=LocalRuntime(case,args.output);report={'case':case,'status':'FAIL'}
        try:
            r.startup()
            if case in CASES or case in ('X01','X02','X03','X04','X05'):getattr(cases,case)(r)
            elif case.startswith('D-terminal-'):death.terminal_order(r,case.removeprefix('D-terminal-'))
            else:death.run(r,case.removeprefix('D-'))
            report=r.finish()
        except Exception as exc:
            import traceback
            report.update(error=str(exc),traceback=traceback.format_exc())
        finally:r.close(report)
        print(case,report['status'],report.get('error',''),flush=True)
        if args.example and report['status']=='PASS':
            example=next(x['worked_example'] for x in r.trace if 'worked_example' in x)
            print(example['question'])
            print('Counts:',canonical(example['counts']).decode())
            print('Cost:',example['research_cost']+'; Checker '+example['checker_cost'])
            print('Registered through independent Check and P-1/Apply at N='+str(report['records']['N']))
            print('Evidence:',canonical(example['evidence']).decode())
            print(example['classification'])
            print('Next:',example['next_permitted_action'])
        return {'case':case,'status':report['status'],'state_directory':str(r.state)}
    from concurrent.futures import ThreadPoolExecutor
    require(1<=args.jobs<=8,'INVALID_JOBS')
    with ThreadPoolExecutor(args.jobs) as pool:results=list(pool.map(execute,selected))
    durable_write(Path(args.output)/'summary.json',{'inventory_sha256':Profile(BUNDLE).inventory_hash,'results':results,'os_isolation':'UNVERIFIED','excluded_linux_case':'T06','coverage_notes':{'B10':'SUBSTITUTED: whole-core outage, not a Transition-ledger-only failure','R14_STOP':'UNREACHABLE: no supported input with missing constitutional meaning','peer_identity_cases':'Cooperative attribution only; R01/R12/R13/T07 OS enforcement unverified'},'source_snapshot':str(ROOT/'artifacts/development/builds'/Profile(BUNDLE).inventory_hash)})
    return 1 if any(r['status']!='PASS' for r in results) else 0

if __name__=='__main__':raise SystemExit(main())
