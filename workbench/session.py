"""Live and read-only runs for the workbench.

A live run is the acceptance fixture kept alive: real core, tool workers and
actor programs as separate processes, state retained in place under
artifacts/development/workbench/<run>/. Every mutation goes through an
existing actor operation or Principal command; the core enforces permission
and current state on each one. A read-only run is a retained ledger read
from SQLite without a core, used when the current build differs from the
run's inventory.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import os
import secrets
import shutil
import sys
import tempfile
import threading
import time
import uuid
from adaptive_research_harness.encoding import decode, digest, require, Refusal
from adaptive_research_harness.clock import durable_write, SyntheticClock
from adaptive_research_harness.profile import Profile
from acceptance import local
from acceptance.local import LocalRuntime, LocalClient, process_generation
from acceptance.runtime import expect
from acceptance.reader import audit
from . import records

ROOT=Path(__file__).resolve().parents[1]
RUNS=ROOT/'artifacts/development/workbench'
LABELS={'researcher':'deterministic policy (AD-R1.0)','data':'synthetic cohorts, SRC-SYN','store':'disposable SQLite','isolation':'OS isolation unverified','charges':'simulated research units; nothing billed'}
ACTOR_OPS={'research':'r01','choose-next-experiment':'r01','run-next-experiment':'r01','propose-hypothesis':'r01','complete-research':'r01','settle-pending':'r01','close-reservation':'r01','check':'ck1'}
PRINCIPAL_OPS={'policy-decide','apply'}


def now_ms():return int(time.time()*1000)


def run_dirs():
    if not RUNS.exists():return []
    return sorted((p for p in RUNS.iterdir() if (p/'workbench.json').is_file()),key=lambda p:p.stat().st_mtime)


def manifest(run_dir):return decode((Path(run_dir)/'workbench.json').read_bytes())


def inventory_matches(bundle):
    """True when every file that takes part in this run's execution or recovery equals the current tree and the environment matches."""
    try:Profile(bundle).verify_execution(ROOT);return True,None
    except Refusal as exc:return False,exc.code+(' '+exc.detail if exc.detail else '')
    except OSError as exc:return False,'BUNDLE_UNREADABLE '+str(exc)


class Session(LocalRuntime):
    """One live run. Constructed by Session.create or Session.resume, never directly."""
    def __init__(self,run_dir,cohort):
        self.run_dir=Path(run_dir);self.cohort=cohort;self.case='W-'+cohort
        self.bundle=self.run_dir/'bundle';self.profile_obj=Profile(self.bundle)
        self.pool=ThreadPoolExecutor(8);self.ordinal=0;self.trace=[]
        self.state=self.run_dir/'state';self.state.mkdir(parents=True,exist_ok=True)
        self.sockets=Path(tempfile.mkdtemp(prefix='arh-wb-',dir='/private/tmp' if sys.platform=='darwin' else '/tmp'))
        self.output=self.run_dir;self.processes=[];self.dead=[];self.logfiles=[];self.mutex=threading.Lock();self.lock=threading.RLock()
        self.config={'bundle':str(self.bundle),'state':str(self.state),'sockets':str(self.sockets),'run_id':uuid.uuid4().hex,
                     'tokens':{actor:secrets.token_hex(24) for actor in self.profile_obj.roles.values()}}
        self.config_path=self.state/'fixture.json';durable_write(self.config_path,self.config)
        self.client=LocalClient(self.config,'Principal');self.mode='live';self.closed=False

    # ----- construction -----
    @classmethod
    def create(cls,cohort,name=None):
        from build_support.freeze import freeze
        catalog=decode((ROOT/'workbench/cohorts.json').read_bytes())['cohorts']
        require(cohort in catalog,'UNKNOWN_COHORT',cohort)
        name=name or time.strftime('%Y%m%d-%H%M%S')+'-'+cohort+'-'+uuid.uuid4().hex[:6]
        run_dir=RUNS/name;require(not run_dir.exists(),'RUN_EXISTS',name)
        (run_dir/'state').mkdir(parents=True)
        inventory=freeze(run_dir/'bundle')
        durable_write(run_dir/'state'/'DISPOSABLE.json',{'disposable':True,'run_id':name})
        content_sha=Profile(run_dir/'bundle').artifacts['variant_cohorts'][cohort]['content_sha256']
        durable_write(run_dir/'workbench.json',{'run':name,'cohort':cohort,'cohort_content_sha256':content_sha,'created_ms':now_ms(),'inventory_sha256':inventory,'bundle':str((run_dir/'bundle').relative_to(ROOT)),'status':'starting','labels':LABELS})
        s=cls(run_dir,cohort)
        try:
            s.host('new-case');s.ready();s.startup_records()
            if cohort!='original':expect(s.agent('observe','observe',{'cohort':cohort}))
            s.note(status='live',started_ms=now_ms())
        except BaseException:
            s.close(status='failed');raise
        return s

    @classmethod
    def resume(cls,run_dir):
        run_dir=Path(run_dir);m=manifest(run_dir)
        ok,reason=inventory_matches(run_dir/'bundle');require(ok,'INVENTORY_MISMATCH',reason or '')
        s=cls(run_dir,m['cohort'])
        try:
            s.prove_quiescence();s.host('resume');s.ready();s.note(status='live',resumed_ms=now_ms())
        except BaseException:
            s.close(status='closed');raise
        return s

    def prove_quiescence(self):
        """Write fixture quiescence proofs for generations recorded in unresolved dispatch claims.

        A proof is written only when the recorded core and worker processes are gone.
        A still-running recorded process refuses the resume.
        """
        es,ts,claims=records.load_readonly(self.state/'harness.sqlite')
        settled={e['body']['attempt'] for e in es if e['kind']=='SETTLEMENT'}
        proof={'inventory_sha256':self.profile_obj.inventory_hash,'terminated_generations':[],'channels_discarded':True,'old_channels_closed':True}
        for c in claims:
            if c['attempt'] in settled:continue
            for g in (c['claim'].get('core'),c['claim'].get('worker')):
                if not g or g in proof['terminated_generations']:continue
                try:os.kill(g['pid'],0)
                except ProcessLookupError:proof['terminated_generations'].append(g);continue
                except PermissionError:raise Refusal('PREVIOUS_SESSION_ALIVE',str(g))
                raise Refusal('PREVIOUS_SESSION_ALIVE',str(g))
        for g in proof['terminated_generations']:
            if 'run' in g:durable_write(self.state/'supervisor'/(digest(g)+'.json'),proof)

    # ----- fixture overrides that avoid the module-global bundle -----
    def ready(self):
        deadline=time.monotonic()+20
        while time.monotonic()<deadline:
            try:
                self.read('profile')
                if all((self.sockets/(x+'.sock')).exists() for x in self.profile_obj.experiment.core_labels()):return
            except (OSError,EOFError,Refusal):pass
            time.sleep(.02)
        raise AssertionError('Workbench core failed: '+str([p.read_text() for p in self.state.glob('*.log')]))
    def tick(self,value):return {'time_ms':SyntheticClock(self.state/'clock.json',self.profile_obj.setup['clock']).advance(value)}
    def host(self,op,**p):
        if op=='new-case':
            SyntheticClock(self.state/'clock.json',self.profile_obj.setup['clock']).initialize()
        elif op!='resume':raise Refusal('CAPABILITY_UNSUPPORTED',op)
        for label in self.profile_obj.experiment.core_labels():self.launch('tool',label)
        self.launch('core');return {'status':op.upper()}
    def note(self,**fields):
        m=manifest(self.run_dir);m.update(fields);durable_write(self.run_dir/'workbench.json',m)
    def close(self,status='closed'):
        with self.lock:
            if self.closed:return
            self.closed=True;self.stop();self.pool.shutdown(wait=True,cancel_futures=True)
            for log in self.logfiles:log.close()
            self.config_path.unlink(missing_ok=True)
            shutil.rmtree(self.sockets,ignore_errors=True)
            try:self.note(status=status,closed_ms=now_ms())
            except OSError:pass

    # ----- reading -----
    def records(self):
        return self.history('E'),self.history('T')
    def claims(self):
        try:return self.read('dispatch-status')['claims']
        except Refusal:return []
    def budgets(self):
        state=self.read('state');out={}
        for g in state['active']:
            try:out[g]=self.read('budget',{'grant':g})
            except Refusal as exc:out[g]={'error':exc.code}
        return out
    def view(self):
        es,ts=self.records();d=records.derive(es,ts);claims=self.claims()
        step=records.next_step(d,self.cohort,claims)
        return {'run':self.run_dir.name,'cohort':self.cohort,'mode':'live','status':'complete' if step is None else 'in_progress',
                'inventory_sha256':self.profile_obj.inventory_hash,'labels':LABELS,'cohort_info':self.cohort_info(),
                'state':{k:v for k,v in self.read('state').items() if k in ('N','active','hypotheses')},'clock':self.read('clock'),
                'stages':records.stages(d,es,ts),'next':step,'controls':records.controls(es,ts,self.budgets()),
                'observations':records.observations(es,d),'counts':{'E':len(es),'T':len(ts)}}
    def cohort_info(self):
        v=self.profile_obj.artifacts['variant_cohorts'][self.cohort]
        return {k:v[k] for k in ('description','differs_from_formation','expected_path','content_sha256')}
    def record(self,ledger,seq):
        es,ts=self.records();rows=es if ledger=='E' else ts
        e=next((x for x in rows if x['seq']==seq),None);require(e is not None,'NO_RECORD');return e
    def reader(self):
        result=self.agent('Principal','independent-read');return result

    # ----- acting -----
    def step(self,op=None):
        """Perform the next permitted operation, or the named one if it is that operation."""
        with self.lock:
            es,ts=self.records();d=records.derive(es,ts);planned=records.next_step(d,self.cohort,self.claims())
            require(planned is not None,'RUN_COMPLETE','No further operation is permitted for this run')
            require(op is None or op==planned['op'],'STEP_NOT_PERMITTED',f"next permitted operation is {planned['op']}")
            op=planned['op'];payload=planned['payload']
            if op in PRINCIPAL_OPS:result=self.call(op,payload)
            elif op=='check':result=self.agent('ck1','check',payload)
            else:result=self.agent('r01',op,payload)
            return {'performed':planned,'result':result}


class ReadOnlyRun:
    """A retained run inspected without a core. Nothing can be performed."""
    def __init__(self,run_dir,reason):
        self.run_dir=Path(run_dir);self.m=manifest(run_dir);self.cohort=self.m['cohort'];self.reason=reason;self.mode='read-only'
        self.es,self.ts,self.claims=records.load_readonly(self.run_dir/'state'/'harness.sqlite')
        # Read the retained artifacts directly: an older bundle may predate the experiment profile and cannot form a Profile.
        self.artifacts=decode((self.run_dir/'bundle'/'designs_and_methods.json').read_bytes())
    def view(self):
        d=records.derive(self.es,self.ts);step=records.next_step(d,self.cohort,self.claims)
        v=self.artifacts['variant_cohorts'][self.cohort]
        return {'run':self.run_dir.name,'cohort':self.cohort,'mode':'read-only','read_only_reason':self.reason,'status':'complete' if step is None else 'in_progress',
                'inventory_sha256':self.m.get('inventory_sha256'),'labels':LABELS,'cohort_info':{k:v[k] for k in ('description','differs_from_formation','expected_path','content_sha256')},
                'state':{'N':max((e['body']['n'] for e in self.ts if e['kind']=='APPLIED'),default=None)},'clock':None,
                'stages':records.stages(d,self.es,self.ts),'next':step,'controls':records.controls(self.es,self.ts,None),
                'observations':records.observations(self.es,d),'counts':{'E':len(self.es),'T':len(self.ts)}}
    def record(self,ledger,seq):
        rows=self.es if ledger=='E' else self.ts
        e=next((x for x in rows if x['seq']==seq),None);require(e is not None,'NO_RECORD');return e
    def records(self):return self.es,self.ts
    def reader(self):
        try:return audit(self.es,self.ts)
        except AssertionError as exc:return {'status':'NOT_RECONSTRUCTED','reason':str(exc)}
    def step(self,op=None):raise Refusal('READ_ONLY','This run was retained under a different build; it can be inspected, not continued')
    def close(self,status=None):pass


def open_run(run_dir):
    """Live when the inventory matches the current tree, otherwise read-only. Local-document runs open through their own session."""
    if manifest(run_dir).get('kind')=='local':
        from .local_session import open_local
        return open_local(run_dir)
    ok,reason=inventory_matches(Path(run_dir)/'bundle')
    if ok:return Session.resume(run_dir)
    return ReadOnlyRun(run_dir,reason)


def list_runs(live=None):
    live=live or {}
    out=[]
    for p in run_dirs():
        m=manifest(p);name=p.name
        entry={'run':name,'kind':m.get('kind','synthetic'),'cohort':m.get('cohort'),'status':m.get('status'),'created_ms':m.get('created_ms'),'inventory_sha256':m.get('inventory_sha256'),'open':name in live,'mode':getattr(live.get(name),'mode',None)}
        try:
            es,ts,claims=records.load_readonly(p/'state'/'harness.sqlite')
            if entry['kind']=='local':
                from .local_session import derive as derive_local, identities
                ids=identities(p/'bundle');entry['progress']='in_progress' if derive_local(es,ts,ids['researcher'],ids['source'],ids['checker'])['next'] else 'complete'
            else:
                d=records.derive(es,ts);entry['progress']='complete' if records.next_step(d,m.get('cohort'),claims) is None else 'in_progress'
            entry['counts']={'E':len(es),'T':len(ts)}
        except (OSError,Refusal,KeyError) as exc:entry['progress']='unreadable';entry['error']=str(exc)
        ok,reason=inventory_matches(p/'bundle');entry['live_eligible']=ok;entry['live_reason']=reason
        out.append(entry)
    return out
