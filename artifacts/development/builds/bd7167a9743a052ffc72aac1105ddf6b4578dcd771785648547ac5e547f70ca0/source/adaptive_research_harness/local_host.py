"""Cooperative local host: token ingress, core and tool workers as processes, a control socket.

One host process generates every actor token and writes them to a connection
file. A caller's identity is that shared secret plus a self-reported pid.
This is the arrangement the acceptance fixture and the workbench use; it
makes no OS isolation claim. Linux peer-credential isolation is the separate
arrangement under isolation/.
"""
from pathlib import Path
import argparse
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
from .encoding import canonical,decode,digest,Refusal,require
from .clock import durable_write,SyntheticClock
from .transport import receive,send,request,LifetimeLock,DropReply
from .client import Client
from .profile import Profile

ROOT=Path(__file__).resolve().parents[1]
CONTROL_OPS=('tick','quiesce','status','stop')


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
        super().__init__(Path(config.get('sockets',config['state']))/'core.sock',actor);self.token=config['tokens'][actor]
    def call(self,op,payload=None,key=None):
        return request(self.path,{'actor':self.actor,'op':op,'payload':payload or {},'request_id':key or str(uuid.uuid4()),'token':self.token,'pid':os.getpid()})


def process_generation(config,pid=None):return {'pid':pid or os.getpid(),'run':config['run_id']}


def local_quiescence(path,inventory,core,worker):
    """Fixture evidence: a proof file naming each generation, and the pid no longer running. core is None for a caller-executed tool."""
    require(Path(path).is_file(),'WORKER_NOT_QUIESCENT');proof=decode(Path(path).read_bytes())
    require(proof['inventory_sha256']==inventory and proof.get('channels_discarded') is True,'WORKER_NOT_QUIESCENT')
    for old in (core,worker):
        if old is None:continue
        require(old in proof['terminated_generations'],'WORKER_NOT_QUIESCENT')
        try:os.kill(old['pid'],0)
        except ProcessLookupError:continue
        raise Refusal('WORKER_NOT_QUIESCENT')
    return proof


def serve_core(config,root=None):
    """The core as one process: real Engine, Store, Dispatcher and command handler behind the token ingress."""
    from .storage import Store
    from .engine import Engine
    from .dispatch import Dispatcher
    from .service import core_handler,Faults
    bundle=Path(config['bundle']);state=Path(config['state']);sockets=Path(config.get('sockets',config['state']));profile=Profile(bundle)
    permission=profile.development_permission(root or config.get('root') or ROOT,state)
    class Clock:
        def read(self):
            require(not (state/'clock-off').exists(),'CLOCK_UNAVAILABLE')
            return SyntheticClock(state/'clock.json',profile.setup['clock']).read()
    with LifetimeLock(state/'writer.lock'):
        store=Store(state/'harness.sqlite');engine=Engine(store,profile,Clock(),permission)
        faults=Faults(engine,state/'faults',lambda:process_generation(config));engine.fault_hook=faults.hit
        tool_sockets={t:str(sockets/(s['label']+'.sock')) for t,s in profile.experiment.core_tools().items()}
        dispatcher=Dispatcher(engine,tool_sockets,state/'supervisor',generation_value=process_generation(config),quiescence_verifier=local_quiescence)
        engine.dispatcher=dispatcher
        handler=core_handler(engine,dispatcher,faults,lambda pid:process_generation(config,pid))
        uids={v:k for k,v in profile.roles.items()}
        def ingress(who,b):
            token=b.pop('token',None);pid=b.pop('pid',None)
            require(token is not None and secrets.compare_digest(token,config['tokens'].get(b.get('actor'),'')),'ACTOR_MISMATCH')
            return handler({'uid':uids[b['actor']],'pid':pid},b)
        local_serve(sockets/'core.sock',ingress,set())


def serve_tool(config,label):
    """One core-dispatched tool worker. It imports the tool module; the core process never does."""
    from .tool_worker import run_worker
    bundle=Path(config['bundle']);state=Path(config['state']);sockets=Path(config.get('sockets',config['state']));profile=Profile(bundle)
    tool=profile.experiment.tool_by_label(label)
    run_worker(tool,sockets/(label+'.sock'),state/label,profile,serve_function=local_serve,generation_provider=lambda:process_generation(config))


class LocalHost:
    """Start a core and its tool workers against a frozen bundle; hand out a connection file; serve a control socket.

    Every actor token lives in this process and in the connection file. The
    Principal token is also the control token. Nothing here is OS isolation.
    """
    def __init__(self,bundle,state,sockets=None,root=ROOT):
        self.bundle=Path(bundle).resolve();self.state=Path(state).resolve();self.root=Path(root)
        self.sockets=Path(sockets) if sockets else Path(tempfile.mkdtemp(prefix='arh-host-',dir='/private/tmp' if sys.platform=='darwin' else '/tmp'))
        self.profile=Profile(self.bundle);self.processes=[];self.dead=[];self.logfiles=[];self.mutex=threading.Lock();self.stopping=threading.Event()
        self.state.mkdir(parents=True,exist_ok=True)
        self.config={'bundle':str(self.bundle),'state':str(self.state),'sockets':str(self.sockets),'root':str(self.root),'run_id':uuid.uuid4().hex,
                     'tokens':{actor:secrets.token_hex(24) for actor in self.profile.roles.values()}}
        self.config_path=self.state/'fixture.json';self.connection_path=self.state/'connection.json'
    # ----- processes -----
    def launch(self,mode,label=None):
        args=[sys.executable,'-m','adaptive_research_harness.local_host','--worker',mode,'--config',str(self.config_path)]
        if label:args+=['--label',label]
        log=open(self.state/(mode+'-'+str(label)+'.log'),'ab');self.logfiles.append(log)
        proc=subprocess.Popen(args,cwd=self.root,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=log,stderr=log)
        with self.mutex:self.processes.append((mode,label,proc))
        return proc
    def start(self):
        marker=self.state/'DISPOSABLE.json'
        if not marker.exists():durable_write(marker,{'disposable':True,'run_id':self.config['run_id']})
        clock=SyntheticClock(self.state/'clock.json',self.profile.setup['clock'])
        if not (self.state/'clock.json').exists():clock.initialize()
        durable_write(self.config_path,self.config)
        for label in self.profile.experiment.core_labels():self.launch('tool',label)
        self.launch('core');self.ready()
        durable_write(self.connection_path,{'socket':str(self.sockets/'core.sock'),'control':str(self.sockets/'control.sock'),'tokens':self.config['tokens'],
            'bundle':str(self.bundle),'state':str(self.state),'run_id':self.config['run_id'],'inventory_sha256':self.profile.inventory_hash,
            'roles':sorted(self.profile.roles.values()),'trust':'Cooperative tokens held by one host process; no OS isolation; caller-executed tools report their own receipts.'})
        return self.connection_path
    def ready(self):
        deadline=time.monotonic()+20
        while time.monotonic()<deadline:
            try:
                self.client('Principal').query('profile')
                if all((self.sockets/(x+'.sock')).exists() for x in self.profile.experiment.core_labels()):return
            except (OSError,EOFError,Refusal):pass
            time.sleep(.02)
        raise AssertionError('Local core failed: '+str([p.read_text() for p in self.state.glob('*.log')]))
    def client(self,actor):return LocalClient(self.config,actor)
    def stop(self,only=None):
        with self.mutex:processes=list(self.processes)
        for mode,label,p in processes:
            if only and mode!=only:continue
            if p.poll() is None:p.kill()
            p.wait(timeout=5)
            g=process_generation(self.config,p.pid)
            if g not in self.dead:self.dead.append(g)
        with self.mutex:self.processes=[x for x in self.processes if only and x[0]!=only]
        return processes
    def proof(self,generations,provider_dispositions=None):
        """Write a fixture quiescence proof for generations verified gone. Dispositions are recorded per attempt."""
        for g in generations:
            try:os.kill(g['pid'],0)
            except ProcessLookupError:pass
            else:raise Refusal('WORKER_NOT_QUIESCENT','process %d still running'%g['pid'])
        base={'inventory_sha256':self.profile.inventory_hash,'terminated_generations':[],'channels_discarded':True,'old_channels_closed':True,'provider_dispositions':{}}
        out=[]
        for g in generations:
            path=self.state/'supervisor'/(digest(g)+'.json')
            proof=decode(path.read_bytes()) if path.exists() else dict(base)
            if g not in proof['terminated_generations']:proof['terminated_generations']=proof['terminated_generations']+[g]
            proof['provider_dispositions']={**proof.get('provider_dispositions',{}),**(provider_dispositions or {})}
            durable_write(path,proof);out.append(str(path))
        return out
    def restart(self):
        self.stop();self.proof(list(self.dead))
        for label in self.profile.experiment.core_labels():self.launch('tool',label)
        self.launch('core');self.ready()
    def tick(self,value):return SyntheticClock(self.state/'clock.json',self.profile.setup['clock']).advance(value)
    def close(self):
        self.stop()
        for log in self.logfiles:log.close()
        self.config_path.unlink(missing_ok=True);self.connection_path.unlink(missing_ok=True)
    # ----- control socket -----
    def control_handler(self,who,b):
        require(secrets.compare_digest(b.get('token',''),self.config['tokens']['Principal']),'UNAUTHORIZED')
        op=b.get('op');require(op in CONTROL_OPS,'CAPABILITY_UNSUPPORTED',str(op))
        if op=='tick':return {'time_ms':self.tick(b['tick'])}
        if op=='quiesce':
            g=b['generation'];require(isinstance(g,dict) and type(g.get('pid')) is int and g.get('run')==self.config['run_id'],'INVALID_GENERATION')
            return {'proofs':self.proof([g],b.get('provider_dispositions'))}
        if op=='status':
            with self.mutex:procs=[{'mode':m,'label':l,'pid':p.pid,'alive':p.poll() is None} for m,l,p in self.processes]
            return {'run_id':self.config['run_id'],'inventory_sha256':self.profile.inventory_hash,'processes':procs,'state':str(self.state)}
        self.stopping.set();return {'status':'STOPPING'}
    def serve_control(self):
        t=threading.Thread(target=local_serve,args=(self.sockets/'control.sock',self.control_handler,set()),daemon=True);t.start()
        deadline=time.monotonic()+5
        while not (self.sockets/'control.sock').exists() and time.monotonic()<deadline:time.sleep(.01)
        return t


def main():
    p=argparse.ArgumentParser(prog='adaptive_research_harness.local_host')
    p.add_argument('--worker',choices=['core','tool']);p.add_argument('--config');p.add_argument('--label')
    p.add_argument('--setup',help='setup directory, or omitted for the synthetic packet');p.add_argument('--run',help='run directory for bundle and state')
    args=p.parse_args()
    if args.worker:
        config=decode(Path(args.config).read_bytes())
        return serve_core(config) if args.worker=='core' else serve_tool(config,args.label)
    require(bool(args.run),'RUN_DIRECTORY_REQUIRED')
    from build_support.freeze import freeze
    run=Path(args.run).resolve();run.mkdir(parents=True,exist_ok=True)
    bundle=run/'bundle'
    if not (bundle/'inventory.json').exists():freeze(bundle,args.setup)
    host=LocalHost(bundle,run/'state');host.start();host.serve_control()
    print('connection',host.connection_path,flush=True)
    def stop(*_):host.stopping.set()
    signal.signal(signal.SIGINT,stop);signal.signal(signal.SIGTERM,stop)
    try:
        while not host.stopping.is_set():time.sleep(.1)
    finally:host.close()
    return 0

if __name__=='__main__':raise SystemExit(main())
