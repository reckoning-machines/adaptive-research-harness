import ast
from copy import deepcopy
from pathlib import Path
import random
import sqlite3
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from adaptive_research_harness.encoding import canonical,decode,digest,units,instant,Refusal
from adaptive_research_harness.clock import SyntheticClock,durable_write
from adaptive_research_harness.storage import Store
from adaptive_research_harness.engine import Engine
from adaptive_research_harness.rules import Rules,funding
from adaptive_research_harness.model import View
from adaptive_research_harness.checkers import a,b
from adaptive_research_harness.tools_a import calculate as calc_a
from adaptive_research_harness.tools_b import calculate as calc_b
from adaptive_research_harness.contracts import COMMON,CLASS_CRITERIA
from .fabricated import Input,profile,ROOT


class Encoding(unittest.TestCase):
    def test_canonical(self):self.assertEqual(canonical({'z':'é','a':[True,None,3]}),b'{"a":[true,null,3],"z":"\xc3\xa9"}')
    def test_duplicate_key(self):
        with self.assertRaises(Refusal):decode(b'{"a":1,"a":2}')
    def test_float(self):
        for v in [1.1,float('nan'),float('inf')]:
            with self.subTest(v=v),self.assertRaises(Refusal):canonical(v)
    def test_bad_units(self):
        for v in ['1','1.000','-1.00','NaN','1e2',True,1.0]:
            with self.subTest(v=v),self.assertRaises(Refusal):units(v)
    def test_exact_units(self):self.assertEqual(units('12.34'),1234)
    def test_clock_time(self):self.assertEqual(instant('1970-01-01T00:00:00.001Z'),1)


class Tools(unittest.TestCase):
    def test_formation(self):
        p=profile();doc=p.artifacts['formation_cohort']['content']
        for fn in (calc_a,calc_b):self.assertEqual({k:fn(doc)[k] for k in ['n','k','n_large','k_large']},{'n':12,'k':8,'n_large':2,'k_large':2})
    def test_independent_algorithms_random_inputs(self):
        rng=random.Random(49);doc=deepcopy(profile().artifacts['formation_cohort']['content'])
        for n in [0,1,12,1024,4096]:
            doc['rows']=[dict(event_id=str(i),spike=bool(rng.randrange(2)),selling=bool(rng.randrange(2)),size_units=rng.randrange(11)) for i in range(n)]
            self.assertEqual(calc_a(doc),calc_b(doc))
    def test_invalid_rows(self):
        original=profile().artifacts['formation_cohort']['content']
        for bad in ('duplicate','bool_as_size','nonbool','too_many'):
            doc=deepcopy(original)
            if bad=='duplicate':doc['rows'].append(doc['rows'][0])
            if bad=='bool_as_size':doc['rows'][0]['size_units']=True
            if bad=='nonbool':doc['rows'][0]['selling']=1
            if bad=='too_many':doc['rows']*=400
            for fn in (calc_a,calc_b):
                with self.subTest(bad=bad,fn=fn),self.assertRaises(Refusal):fn(doc)


class Accounting(unittest.TestCase):
    def setUp(self):self.x=Input();self.rules=Rules(self.x.profile)
    def run_rule(self,op,p,actor='AD-R1.0',now=None):return self.rules.execute(self.x.view(),actor,op,p,self.x.now if now is None else now)
    def reject(self,code,op,p,actor='AD-R1.0'):
        with self.assertRaises(Refusal) as caught:self.run_rule(op,p,actor)
        self.assertEqual(caught.exception.code,code)
    def test_pending_close_retains_maximum(self):
        r=self.x.reservation();a=self.x.attempt(r);self.x.add('E','CLOSED',{'reservation':r['seq']})
        self.assertEqual(self.x.view().totals('AU-RP-1',self.x.now),(100,100))
    def test_settle_without_clock_after_fence_and_revocation(self):
        a=self.x.attempt();self.x.add('E','FENCE',{'grant':'AU-RP-1'})
        v=self.x.view();v.active.remove('AU-RP-1');v.revoked.add('AU-RP-1')
        result=self.rules.execute(v,'AD-R1.0','settle',{'attempt':a['seq'],'actual':'1.00','unit':'simulated_research_units','provenance':{'kind':'UNKNOWN'}},None)
        self.assertEqual(result[0]['kind'],'SETTLEMENT');self.assertIsNone(result[0]['time_ms'])
    def test_duplicate_settlement(self):
        a=self.x.attempt();p={'attempt':a['seq'],'actual':'1.00','unit':'simulated_research_units','provenance':{'kind':'UNKNOWN'}}
        self.x.add('E','SETTLEMENT',dict(p,reservation=a['body']['reservation'],grant='AU-RP-1'))
        self.reject('ALREADY_SETTLED','settle',p)
    def test_invalid_settlement(self):
        a=self.x.attempt();p={'attempt':a['seq'],'actual':'0.00','unit':'simulated_research_units','provenance':{'kind':'UNKNOWN'}}
        self.reject('INVALID_SETTLEMENT','settle',p)
    def test_reservation_expiry(self):
        p={'grant':'AU-RP-1','amount':'1.00','purpose':{'kind':'Theme','id':'TH-G1'}}
        r=self.run_rule('reserve',p)[0]['body'];self.assertEqual(r['expiry_ms'],self.x.now+604800000)
        self.reject('INVALID_EXPIRY','reserve',dict(p,expiry_ms=self.x.now+604800001))
    def test_pool_competition_pure_order(self):
        # Each actor remains below its lineage cap; two orders model both winners.
        for i in range(1,7):self.x.reservation('90.00',f'AD-R{i}.0',purpose={'kind':'Theme','id':'TH-G1'} if i<=5 else {'kind':'SearchFamily','id':'SF-G1'})
        actor='AD-R7.0';p={'grant':'AU-RP-1','amount':'40.00','purpose':{'kind':'SearchFamily','id':'SF-G1'}}
        action=self.run_rule('reserve',p,actor)[0];self.x.add('E',action['kind'],action['body'],actor)
        self.reject('BUDGET_EXCEEDED','reserve',p,'AD-R8.0')
    def test_cross_grant_lineage(self):
        self.x.reservation('90.00');self.x.reservation('11.00',grant='FABRICATED-SUCCESSOR')
        self.assertEqual(self.x.view().totals('AU-RP-1',self.x.now,'AD-R1'),(0,10100))
    def test_fence_releases_allowance_but_not_liability(self):
        r=self.x.reservation();self.x.attempt(r);self.x.add('E','FENCE',{'grant':'AU-RP-1'})
        self.assertEqual(self.x.view().totals('AU-RP-1',self.x.now),(100,100))
        self.reject('FENCED','reserve',{'grant':'AU-RP-1','amount':'1.00','purpose':{'kind':'Theme','id':'TH-G1'}})
    def test_overrun(self):
        a=self.x.attempt();self.x.add('E','SETTLEMENT',{'attempt':a['seq'],'actual':'601.00','reservation':a['body']['reservation']})
        self.assertEqual(self.x.view().totals('AU-RP-1',self.x.now),(60100,60100))
        self.reject('OVERSPENT','reserve',{'grant':'AU-RP-1','amount':'0.00','purpose':{'kind':'Theme','id':'TH-G1'}})
    def test_exact_prospective_reference(self):
        p,r=self.x.hypothesis();funding(self.x.view(),p,self.x.now)
        p['body']['funding_ref']+=1
        with self.assertRaises(Refusal):funding(self.x.view(),p,self.x.now)
    def test_conditional_append_collision(self):
        p,r=self.x.hypothesis()
        self.reject('FUNDING_REFERENCE_TAKEN','reserve',{'grant':'AU-RP-1','amount':'2.00','purpose':{'kind':'Transition','id':p['transition_id']},'expected_sequence':r['seq']})
    def test_frozen_expiry_and_invalidation(self):
        p,r=self.x.hypothesis();bind=self.x.add('E','BIND',{'reservation':r['seq'],'transition_id':p['transition_id'],'decision':9,'interval_ms':300000,'time_ms':self.x.now})
        self.x.now+=604800001
        self.assertTrue(self.x.view().reservation(r['seq'],self.x.now)['frozen'])
        self.assertFalse(self.x.view().reservation(r['seq'],self.x.now)['closed'])
        self.reject('RESERVATION_BOUND','close',{'reservation':r['seq']})
        inv=self.run_rule('invalidate-request',{'bind':bind['seq']},'@Apply')[0]
        self.x.add('T',inv['kind'],inv['body'],inv['actor'],p['transition_id'])
        self.assertTrue(self.x.view().reservation(r['seq'],self.x.now)['frozen'])
        self.x.add('E','RELEASE',{'bind':bind['seq'],'invalidation':len(self.x.t)})
        self.assertTrue(self.x.view().reservation(r['seq'],self.x.now)['closed'])
    def test_strict_elapsed_equality(self):
        p,r=self.x.hypothesis();bind=self.x.add('E','BIND',{'reservation':r['seq'],'transition_id':p['transition_id'],'interval_ms':300000,'time_ms':self.x.now})
        self.x.now+=300000;self.reject('INTERVAL_NOT_ELAPSED','invalidate-request',{'bind':bind['seq']},'@Apply')
        self.x.now+=1;self.assertEqual(self.run_rule('invalidate-request',{'bind':bind['seq']},'@Apply')[0]['kind'],'BINDING_INVALIDATED')
    def test_unauthorized_fence(self):self.reject('UNAUTHORIZED','fence',{'grant':'AU-RP-1','reason':'test'})


class CheckerCoverage(unittest.TestCase):
    def evaluate(self,x,p,checker='AD-CK-1.0'):
        grant='AU-CK-A' if checker=='AD-CK-1.0' else 'AU-CK-B'
        return [m.evaluate(x.snapshot(),p['transition_id'],checker,grant,999,x.profile_dict()) for m in (a,b)]
    def test_startup_16_computed_cases(self):
        x=Input(full=False)
        for n,cls,subject,c in x.startup():
            p=x.propose(cls,subject,c)
            for result in self.evaluate(x,p):
                self.assertEqual(set(result['criteria']),set(COMMON+CLASS_CRITERIA[cls]))
                self.assertEqual(result['result'],'PASS',(n,result['criteria']))
            x.n+=1;x.add('T','APPLIED',{'n':x.n,'bind':None},'Principal',p['transition_id'])
    def test_ordinary_both_algorithms(self):
        x=Input();p,_=x.hypothesis()
        for r in self.evaluate(x,p):self.assertEqual(r['result'],'PASS',r['criteria'])
    def test_missing_setup_fields(self):
        for ident,path in [('AU-RP-1',('binding_interval_ms',)),('AU-RP-1',('tools',0,'tier')),('AU-OBS-1',('source_declarations',1,'content','resolution_grace_ms')),('AU-OBS-1',('source_declarations',1,'content','enumeration_contract'))]:
            x=Input();g=deepcopy(x.profile.grants[ident]);target=g
            for key in path[:-1]:target=target[key]
            target[path[-1]]=None
            p=x.propose('AUTHORIZATION','bad',{'action':'GRANT','predecessor':None,'grant':g})
            for r in self.evaluate(x,p):self.assertEqual(r['result'],'FAIL',(ident,path,r))
    def test_bad_designs(self):
        for mutation in ['method','identity','inherited','provider','hash']:
            x=Input();c=deepcopy(x.profile.designs['AD-R1.0'])
            if mutation=='method':c['initial_method']=None
            if mutation=='inherited':c['authorization_request']='AU-RP-1'
            if mutation=='provider':c['provenance']['provider']='fictional-diversity'
            if mutation=='hash':c['executable_closure_sha256']='0'*64
            p=x.propose('AGENT_DESIGN',c['AgentDesignVersionId'],c)
            for r in self.evaluate(x,p):self.assertEqual(r['result'],'FAIL')
    def test_bad_hypothesis(self):
        for mutation in ['count','overlap','time','origin','method','hash','falsifier','member']:
            x=Input();p,_=x.hypothesis();c=p['body']['content']
            if mutation=='count':x.e[1]['body']['result']['n']=999;x.e[1]['sha256']=digest(x.e[1]['body'])
            if mutation=='overlap':c['resolution_period']['start']='2026-10-28T00:00:00.000Z'
            if mutation in ('time','origin'):c['selection_basis'].pop('time_estimate_ms' if mutation=='time' else 'origin')
            if mutation=='method':c['initial_method']['sha256']='0'*64
            if mutation=='hash':c['motivation_closure']['refs'][0]['sha256']='0'*64
            if mutation=='falsifier':c['falsifier']='Always approve'
            if mutation=='member':c['resolution_set'][0]['print']='LATER'
            for r in self.evaluate(x,p):self.assertEqual(r['result'],'FAIL',(mutation,r))
    def test_own_subject_and_second_checker(self):
        x=Input();g=deepcopy(x.profile.grants['AU-CK-A']);g['AuthorizationId']='AU-CK-A-S06-1'
        x.add('E','FENCE',{'grant':'AU-CK-A'})
        p=x.propose('AUTHORIZATION',g['AuthorizationId'],{'action':'SUPERSEDE','predecessor':'AU-CK-A','grant':g})
        for r in self.evaluate(x,p):self.assertEqual(r['criteria']['independence']['status'],'NOT MET')
        for r in self.evaluate(x,p,'AD-CK-2.0'):self.assertEqual(r['result'],'PASS',r['criteria'])
    def test_unsupported_science(self):
        x=Input();p,_=x.hypothesis();p['body']['content']['template_id']='unknown'
        with self.assertRaises(Refusal):self.evaluate(x,p)
    def test_import_independence(self):
        for path in (ROOT/'adaptive_research_harness/checkers').glob('[ab].py'):
            tree=ast.parse(path.read_text())
            imports=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
            self.assertEqual(set(imports),{'encoding','contracts'})
            self.assertFalse(any(isinstance(n,ast.Import) for n in ast.walk(tree)))


class EmptyStorageAndClock(unittest.TestCase):
    def test_storage_request_transaction_and_concurrency_without_genesis(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'empty.sqlite';s=Store(path);s.close()
            barrier=threading.Barrier(2)
            def work():
                db=Store(path);barrier.wait()
                with db.transaction():
                    old=db.lookup('BUILD-ONLY','receipt','fixed')
                    if old is None:db.remember('BUILD-ONLY','receipt','fixed',{'status':'COMPONENT_PROBE','refs':[]})
                db.close()
            with ThreadPoolExecutor(2) as pool:list(pool.map(lambda _:work(),range(2)))
            s=Store(path);self.assertEqual(s.db.execute('SELECT count(*) FROM requests').fetchone()[0],1)
            self.assertEqual(s.events('E'),[]);self.assertEqual(s.events('T'),[])
            with self.assertRaises(Refusal):s.lookup('BUILD-ONLY','receipt','changed')
            try:
                with s.transaction():s.remember('BUILD-ONLY','rollback','x',{});raise RuntimeError('abort')
            except RuntimeError:pass
            self.assertIsNone(s.lookup('BUILD-ONLY','rollback'));s.close()
    def test_clock_persistence_and_rollback(self):
        with tempfile.TemporaryDirectory() as d:
            config=profile().setup['clock'];path=Path(d)/'clock.json';c=SyntheticClock(path,config)
            with self.assertRaises(Refusal):c.read()
            c.initialize();c.advance(1001);self.assertEqual(SyntheticClock(path,config).read(),instant(config['epoch'])+1001)
            with self.assertRaises(Refusal):c.advance(1000)
            with self.assertRaises(Refusal):c.initialize()
    def test_engine_gate_without_constructing_store(self):
        with self.assertRaises(Refusal):Engine(None,profile(),None,None)
    def test_disposable_development_has_no_manual_permit_gate(self):
        from unittest.mock import patch
        p=profile()
        with patch.object(p,'verify_files') as verify:
            permission=p.approve_run('/no-manual-permit',ROOT,require_linux=False)
        verify.assert_called_once_with(ROOT)
        self.assertTrue(permission['allow_apply_zero'])

if __name__=='__main__':unittest.main()
