"""Protected Linux service and role-specific worker entrypoints."""
from pathlib import Path
import os
import threading
import time
from .encoding import fields, canonical, decode, digest, require, Refusal
from .transport import LifetimeLock, serve, request, DropReply
from .storage import Store
from .engine import Engine
from .dispatch import Dispatcher
from .host import generation
from .clock import SyntheticClock, durable_write
from .profile import Profile
from .contracts import READS


class ClockClient:
    def __init__(self,path):self.path=path
    def read(self):
        try:
            response=request(self.path,{'op':'read'})
            if response.get('status')=='ERROR':raise Refusal(response.get('reason','CLOCK_UNAVAILABLE'))
            require('time_ms' in response,'CLOCK_UNAVAILABLE');return response['time_ms']
        except Refusal:raise
        except (OSError,EOFError,ValueError) as exc:raise Refusal('CLOCK_UNAVAILABLE') from exc


class Faults:
    def __init__(self,engine,directory,generation_provider=generation):
        self.engine=engine;self.directory=Path(directory);self.local=threading.local();self.generation_provider=generation_provider
    def take(self,key,op):
        self.local.fault=None
        with self.engine.lock,self.engine.store.transaction():
            row=self.engine.store.db.execute('SELECT body,target FROM faults WHERE target IN (?,?) AND consumed=0 ORDER BY target LIMIT 1',(key,'@op:'+op)).fetchone()
            if row:
                self.local.fault=decode(row['body']);self.engine.store.db.execute('UPDATE faults SET consumed=1 WHERE target=?',(row['target'],))
    def hit(self,point):
        f=getattr(self.local,'fault',None)
        if not f or f.get('point')!=point:return
        if f['kind']=='DROP_COMMAND_REPLY':raise DropReply()
        if f['kind']=='PAUSE_AT_BOUNDARY':
            self.directory.mkdir(parents=True,exist_ok=True)
            key=digest(f);durable_write(self.directory/(key+'.paused'),{'point':point,'generation':self.generation_provider(),'fault':f})
            while not (self.directory/(key+'.release')).exists():time.sleep(.05)


def core_handler(engine, dispatcher, faults, peer_generation=generation):
    profile=engine.profile;store=engine.store
    def handler(who,b):
        fields(b,{'op','payload','request_id','actor'})
        actor=profile.roles.get(who['uid']);require(actor is not None and actor==b['actor'],'ACTOR_MISMATCH')
        op,payload,key=b['op'],b['payload'],b['request_id']
        require(isinstance(payload,dict),'INVALID_OBJECT')
        if op in READS:return engine.query(actor,op,payload)
        if op=='tool-run':
            faults.take(key,op)
            fields(payload,{'attempt'});return dispatcher.run(actor,payload['attempt'],peer_generation(who['pid']))
        if op=='check-finish':
            fields(payload,{'attempt','receipt'});return dispatcher.finish_check(actor,payload['attempt'],payload['receipt'])
        if op=='tool-receipt':
            fields(payload,{'attempt'})
            return dispatcher.receipt(actor,payload['attempt'])
        if op=='fixture-fault':
            require(actor=='Principal','UNAUTHORIZED')
            fields(payload,{'target','kind','case'}, {'point'})
            if payload['kind']=='DROP_COMMAND_REPLY':require(payload.get('point','').startswith('after_'),'INVALID_FAULT')
            require(payload['kind'] in ('AFTER_START_FAILURE','DROP_TOOL_RESPONSE','DROP_COMMAND_REPLY','OVERRUN_601','PAUSE_AT_BOUNDARY','FOREIGN_AUTHORITY_OUTPUT'),'INVALID_FAULT')
            if payload['kind']=='OVERRUN_601':require(payload['case']=='R09','INVALID_FAULT')
            if payload['kind']=='FOREIGN_AUTHORITY_OUTPUT':require(payload['case']=='T03','INVALID_FAULT')
            with engine.lock,store.transaction():
                store.db.execute('INSERT INTO faults VALUES(?,?,0)',(str(payload['target']),canonical(payload)))
            return {'status':'ARMED','fault_hash':digest(payload)}
        if op=='recover':
            fields(payload,set(),{'transition_id','continue'})
            if not payload.get('continue'):return engine.query(actor,'obligations',{})
            if actor!='Principal':return engine._commit(actor,key,op,payload,failure='UNAUTHORIZED')
            with engine.lock:
                v=engine.view();tr=payload['transition_id']
                if tr in v.applies:return {'status':'ALREADY_APPLIED','ref':{'ledger':'T','sequence':v.applies[tr]['seq'],'sha256':v.applies[tr]['sha256']}}
                binds=[(k,e) for k,e in v.binds.items() if e['body']['transition_id']==tr]
                for k,e in binds:
                    if v.binding_state(k)=='PENDING_RELEASE':return engine.command(actor,key,'release',{'bind':k})
                decisions=[(k,e) for k,e in v.decisions.items() if e['transition_id']==tr and e['body']['decision']=='ADMITTED']
                require(bool(decisions),'RECHECK_OR_DECISION_REQUIRED');d=max(decisions)[0]
                current=[k for k,e in binds if v.binding_state(k)=='FROZEN']
                p={'transition_id':tr,'decision':d}
                if current:p['bind']=current[-1]
            return engine.command(actor,key,'apply',p)
        faults.take(key,op)
        response=engine.command(actor,key,op,payload)
        faults.hit('after_'+op+'_commit')
        return response
    return handler


def run_core(args):
    require(os.getuid()==20000,'WRONG_SERVICE_UID')
    profile=Profile(args.bundle);permit=profile.approve_run(args.run_approval,args.root)
    state=Path(args.state);state.mkdir(parents=True,exist_ok=True,mode=0o700)
    with LifetimeLock(Path(args.socket).parent/'writer.lock'):
        store=Store(state/'harness.sqlite');clock=ClockClient(args.clock_socket)
        engine=Engine(store,profile,clock,permit)
        faults=Faults(engine,state/'faults');engine.fault_hook=faults.hit
        dispatcher=Dispatcher(engine,{'SYN-A-1':args.tool_a_socket,'SYN-B-1':args.tool_b_socket},args.supervisor_receipts)
        engine.dispatcher=dispatcher
        handler=core_handler(engine,dispatcher,faults)
        try:serve(args.socket,handler,set(profile.roles))
        finally:store.close()


def run_clock(args):
    require(os.getuid()==20003,'WRONG_SERVICE_UID')
    profile=Profile(args.bundle);profile.approve_run(args.run_approval,args.root)
    clock=SyntheticClock(Path(args.state)/'clock.json',profile.setup['clock'])
    def handler(who,b):
        op=b.get('op')
        if op=='read':require(who['uid']==20000,'UNAUTHORIZED');return {'time_ms':clock.read()}
        require(who['uid']==20001,'UNAUTHORIZED')
        if op=='initialize':clock.initialize();return {'time_ms':clock.read()}
        if op=='advance':return {'time_ms':clock.advance(b['tick'])}
        raise Refusal('CAPABILITY_UNSUPPORTED')
    with LifetimeLock(Path(args.state)/'clock.lock'):serve(args.socket,handler,{20000,20001})


def run_agent(args):
    from .client import Client
    from . import actors
    profile=Profile(args.bundle);profile.approve_run(args.run_approval,args.root)
    actor=profile.roles.get(os.getuid());require(actor is not None and actor==args.actor,'WRONG_ACTOR_UID')
    client=Client(args.core_socket,actor)
    def actor_hook(point):
        state=Path(args.state);fault=state/'next-fault.json'
        if not fault.exists() or decode(fault.read_bytes()).get('point')!=point:return
        fault.unlink();key=digest([point,generation()]);paused=state/(key+'.paused')
        durable_write(paused,{'point':point,'generation':generation()})
        while not paused.with_suffix('.release').exists():time.sleep(.05)
    def handler(who,b):
        require(who['uid']==20001,'UNAUTHORIZED')
        op=b['op'];payload=b.get('payload',{})
        if op=='peer-impersonation':
            require(actor.startswith('AD-R'),'INVALID_CASE')
            return Client(args.core_socket,payload['actor']).call('fence',{'grant':'AU-RP-1','reason':'T07 negative identity assertion'})
        if op=='check':return actors.check(client,payload['transition_id'],actor_hook)
        if op=='choose-next-experiment':return actors.choose_next_experiment(client,payload['research_ref'])
        if op=='run-next-experiment':return actors.run_next_experiment(client,payload['selection_ref'])
        if op=='research':return actors.research(client,payload.get('tool','SYN-A-1'),payload.get('stop_after'))
        if op=='complete-research':return actors.complete_research(client,payload['attempt'])
        if op=='propose-successor':return actors.propose_successor(client,payload['case'],payload['ordinal'])
        if op=='propose-mutated':return actors.propose_mutated(client,**payload)
        if op=='propose-hypothesis':return actors.propose_hypothesis(client,payload['research_ref'],payload.get('previous'))
        if op=='observe':return actors.observe(client,payload.get('date','2026-10-28'),payload.get('form','DOCUMENT'))
        if op=='settle-pending':return actors.recover_settlement(client,payload['attempt'])
        if op=='inspect-request':return client.query('inspect-request',payload)
        if op=='close-reservation':return client.call('close',payload)
        if op=='reserve':return client.call('reserve',payload,b.get('request_id'))
        if op=='retry-research':return actors.retry_research(client,payload['attempt'])
        # Negative tests are distinguished from the program's genuine research outputs.
        if op=='adversarial-command':
            require(payload['command'] not in ('propose','research-commit'),'INVALID_CASE')
            require(payload['command'] in {'reserve','attempt','settle','close','fence','propose','check-commit','decide','policy-decide','apply','bind','observation-commit','standing','research-commit','release','invalidate-request','genesis','recover'},'INVALID_CASE')
            require(payload.get('case') in {f'{prefix}{i:02d}' for prefix,n in [('R',16),('B',12),('C',7),('S',8),('T',7)] for i in range(1,n+1)},'INVALID_CASE')
            return client.call(payload['command'],payload['payload'],payload.get('request_id'))
        raise Refusal('CAPABILITY_UNSUPPORTED')
    with LifetimeLock(Path(args.socket).parent/'actor.lock'):serve(args.socket,handler,{20001})
