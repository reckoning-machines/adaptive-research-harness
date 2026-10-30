"""Focused workbench tests. These start real core, tool and actor processes."""
from http.client import HTTPConnection
from pathlib import Path
import glob
import json
import os
import shutil
import threading
import time
import unittest
from adaptive_research_harness.encoding import Refusal
from workbench import records
from workbench.session import Session, open_run, list_runs, RUNS
from workbench.api import serve

ROOT=Path(__file__).resolve().parents[2]
PREFIX='test-'+time.strftime('%Y%m%d%H%M%S')+'-'


def complete(run):
    n=0
    while run.view()['next'] is not None:
        r=run.step();n+=1
        st=r['result'].get('status') if isinstance(r['result'],dict) else None
        assert st not in ('ERROR','REFUSED'),r
    return n


class Records(unittest.TestCase):
    def test_retained_e01_history_derives_as_complete(self):
        dbs=glob.glob(str(ROOT/'artifacts/development/*/*/state/E01/harness.sqlite'))
        if not dbs:self.skipTest('no retained E01 history')
        es,ts,claims=records.load_readonly(sorted(dbs)[-1]);d=records.derive(es,ts)
        self.assertIsNone(records.next_step(d,'original',claims))
        self.assertTrue(all(s['done'] for s in records.stages(d,es,ts)))
        c=records.controls(es,ts);self.assertEqual(c['pending_attempts'],[]);self.assertEqual(c['settled_hundredths_by_grant']['AU-RP-1'],200)
    def test_empty_history_asks_for_research_first(self):
        step=records.next_step(records.derive([],[]),'independent-shocks',[])
        self.assertEqual(step['op'],'research');self.assertEqual(step['payload']['cohort'],'independent-shocks')
        self.assertIsNone(records.next_step(records.derive([],[]),'original',[])['payload']['cohort'])


class Cohorts(unittest.TestCase):
    created=[]
    @classmethod
    def tearDownClass(cls):
        for name in cls.created:shutil.rmtree(RUNS/name,ignore_errors=True)
    def run_cohort(self,cohort):
        name=PREFIX+cohort;self.created.append(name);s=Session.create(cohort,name=name)
        try:
            steps=complete(s);v=s.view();reader=s.reader()
        finally:s.close()
        return steps,v,reader
    def test_original_matches_e01(self):
        steps,v,reader=self.run_cohort('original')
        self.assertEqual(steps,8);self.assertEqual(v['status'],'complete');self.assertEqual(v['state']['N'],17);self.assertEqual(v['counts'],{'E':86,'T':71})
        c=next(x for x in v['stages'] if x['key']=='control');self.assertEqual(c['analysis'],'complement-control');self.assertFalse(c['passes']);self.assertIn('6 of 10',c['text']);self.assertTrue(c['research_failure'])
        self.assertEqual(v['controls']['budgets']['AU-RP-1']['committed'],'2.00');self.assertEqual(v['controls']['budgets']['AU-CK-A']['committed'],'4.25')
        self.assertEqual(reader['status'],'RECONSTRUCTED');self.assertEqual(reader['pending_attempts'],[])
    def test_independent_shocks_reproduces_rather_than_controls(self):
        steps,v,reader=self.run_cohort('independent-shocks')
        self.assertEqual(v['status'],'complete');self.assertEqual(v['state']['N'],17);self.assertEqual(v['counts']['E'],89)
        c=next(x for x in v['stages'] if x['key']=='control');self.assertEqual(c['analysis'],'independent-reproduction');self.assertTrue(c['passes']);self.assertIsNone(c['research_failure'])
        self.assertIn('not independent evidence',c['nature']);self.assertIn('new independent cohort',c['next_action'])
        d=next(x for x in v['stages'] if x['key']=='diagnostic');self.assertIn('span 2 shocks',d['text']);self.assertIsNone(d['initial_failure'])
        self.assertEqual(reader['status'],'RECONSTRUCTED')
    def test_control_survives_passes_its_diagnostic(self):
        steps,v,reader=self.run_cohort('control-survives')
        self.assertEqual(v['status'],'complete');self.assertEqual(v['state']['N'],17)
        c=next(x for x in v['stages'] if x['key']=='control');self.assertEqual(c['analysis'],'complement-control');self.assertTrue(c['passes']);self.assertIn('7 of 10',c['text']);self.assertIsNone(c['research_failure'])
        self.assertIn('not a statistical test',c['nature']);self.assertEqual(reader['status'],'RECONSTRUCTED')


class Reopen(unittest.TestCase):
    created=[]
    @classmethod
    def tearDownClass(cls):
        for name in cls.created:shutil.rmtree(RUNS/name,ignore_errors=True)
    def test_interrupted_run_resumes_without_duplicate_work(self):
        name=PREFIX+'interrupted';self.created.append(name);s=Session.create('control-survives',name=name)
        try:
            s.step();s.step();v=s.view();self.assertEqual(v['next']['op'],'run-next-experiment')
            with self.assertRaises(Refusal) as ctx:s.step('apply')
            self.assertEqual(ctx.exception.code,'STEP_NOT_PERMITTED')
        finally:s.close()
        self.assertFalse((RUNS/name/'state'/'fixture.json').exists())
        es1,ts1,_=records.load_readonly(RUNS/name/'state'/'harness.sqlite')
        r=open_run(RUNS/name);self.assertEqual(r.mode,'live')
        try:
            self.assertEqual(r.view()['next']['op'],'run-next-experiment');steps=complete(r);v=r.view();reader=r.reader()
        finally:r.close()
        self.assertEqual(steps,6);self.assertEqual(v['status'],'complete');self.assertEqual(v['state']['N'],17)
        es2,ts2,_=records.load_readonly(RUNS/name/'state'/'harness.sqlite')
        self.assertEqual(es2[:len(es1)],es1);self.assertEqual(ts2[:len(ts1)],ts1)
        attempts=[e for e in es2 if e['kind']=='ATTEMPT' and e['actor']=='AD-R1.0'];self.assertEqual(len(attempts),2)
        self.assertEqual(v['controls']['budgets']['AU-RP-1']['committed'],'2.00');self.assertEqual(v['controls']['pending_attempts'],[])
        self.assertEqual(reader['status'],'RECONSTRUCTED');self.assertEqual(reader['pending_attempts'],[])
        self.assertEqual(sum(1 for e in ts2 if e['kind']=='APPLIED'),18)
    def test_completed_run_reopens_with_nothing_permitted_and_core_still_refuses(self):
        name=PREFIX+'completed';self.created.append(name);s=Session.create('original',name=name)
        try:complete(s)
        finally:s.close()
        r=open_run(RUNS/name)
        try:
            self.assertEqual(r.mode,'live');self.assertIsNone(r.view()['next'])
            with self.assertRaises(Refusal):r.step()
            # The core, not the page, is the authority: a Principal command outside the plan is refused by the core.
            result=r.call('apply',{'transition_id':'TR-NOT-REAL','decision':1})
            self.assertEqual(result['status'],'REFUSED');self.assertEqual(result['reason'],'NO_PROPOSAL')
            result=r.agent('r01','adversarial-command',{'case':'R01','command':'fence','payload':{'grant':'AU-RP-1','reason':'page cannot fence'}})
            self.assertEqual(result['status'],'REFUSED')
            es,ts=r.records();self.assertTrue(any(e['kind']=='REFUSAL' for e in es+ts))
        finally:r.close()
    def test_differing_build_opens_read_only(self):
        src=RUNS/(PREFIX+'completed')
        if not src.exists():self.skipTest('completed run not available')
        name=PREFIX+'old-build';self.created.append(name);dst=RUNS/name
        shutil.copytree(src,dst,ignore=shutil.ignore_patterns('*.sock','fixture.json'))
        inv=json.loads((dst/'bundle/inventory.json').read_bytes());inv['files'][0]['sha256']='0'*64
        (dst/'bundle/inventory.json').write_bytes(json.dumps(inv,sort_keys=True,separators=(',',':')).encode()+b'\n')
        r=open_run(dst);self.assertEqual(r.mode,'read-only');self.assertIn('ARTIFACT_CHANGED',r.reason)
        v=r.view();self.assertEqual(v['mode'],'read-only');self.assertTrue(all(s['done'] for s in v['stages']))
        self.assertEqual(r.reader()['status'],'RECONSTRUCTED')
        with self.assertRaises(Refusal) as ctx:r.step()
        self.assertEqual(ctx.exception.code,'READ_ONLY')
        listed={x['run']:x for x in list_runs()};self.assertFalse(listed[name]['live_eligible'])


class Api(unittest.TestCase):
    created=[]
    @classmethod
    def setUpClass(cls):
        cls.bench,cls.server=serve(0);cls.port=cls.server.server_address[1]
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.bench.close_all();cls.server.shutdown()
        for name in cls.created:shutil.rmtree(RUNS/name,ignore_errors=True)
    def req(self,method,path,body=None):
        c=HTTPConnection('127.0.0.1',self.port,timeout=120);c.request(method,path,json.dumps(body) if body is not None else None,{'Content-Type':'application/json'})
        r=c.getresponse();data=r.read();c.close()
        return r.status,(json.loads(data) if r.getheader('Content-Type','').startswith('application/json') else data)
    def test_page_cohorts_runs_and_one_live_cycle(self):
        status,html=self.req('GET','/');self.assertEqual(status,200);self.assertIn(b'synthetic data',html);self.assertIn(b'deterministic researcher',html)
        status,c=self.req('GET','/api/cohorts');self.assertEqual(status,200);self.assertEqual({x['name'] for x in c['cohorts']},{'original','independent-shocks','control-survives'})
        self.assertEqual(next(x for x in c['cohorts'] if x['name']=='independent-shocks')['large_shocks'],['s01','s07'])
        status,r=self.req('POST','/api/runs',{'cohort':'independent-shocks'});self.assertEqual(status,202);name=r['run'];self.created.append(name)
        deadline=time.monotonic()+90
        while time.monotonic()<deadline:
            status,v=self.req('GET',f'/api/runs/{name}')
            if v.get('status')!='starting':break
            time.sleep(.5)
        self.assertEqual(v['mode'],'live',v);self.assertEqual(v['next']['op'],'research')
        status,st=self.req('POST',f'/api/runs/{name}/step',{'op':'apply'});self.assertEqual(status,409);self.assertEqual(st['error'],'STEP_NOT_PERMITTED')
        status,st=self.req('POST',f'/api/runs/{name}/step',{'op':'research'});self.assertEqual(status,200);self.assertEqual(st['performed']['op'],'research')
        status,v=self.req('GET',f'/api/runs/{name}');self.assertTrue(v['stages'][0]['done']);ref=v['stages'][2]['ref']
        status,rec=self.req('GET',f"/api/runs/{name}/record/{ref['ledger']}/{ref['sequence']}");self.assertEqual(rec['kind'],'RESEARCH_RECORD');self.assertEqual(rec['body']['result']['n'],12)
        status,runs=self.req('GET','/api/runs');self.assertTrue(any(x['run']==name and x['open'] and x['mode']=='live' for x in runs['runs']))
        status,closed=self.req('POST',f'/api/runs/{name}/close');self.assertEqual(closed['status'],'closed')
        status,v=self.req('POST',f'/api/runs/{name}/open');self.assertEqual(status,200);self.assertEqual(v['mode'],'live');self.assertEqual(v['next']['op'],'choose-next-experiment')
        status,missing=self.req('GET','/api/runs/no-such-run');self.assertEqual(status,404)


class BuildIdentity(unittest.TestCase):
    def test_identity_ignores_working_tree_status_and_variants_declare_themselves(self):
        import uuid
        from build_support.freeze import freeze
        from adaptive_research_harness.encoding import digest,decode
        marker=ROOT/'artifacts/development'/('scratch-'+uuid.uuid4().hex+'.txt');bundles=[]
        try:
            a=ROOT/'artifacts/development/run-bundles'/('test-'+uuid.uuid4().hex)/'bundle';bundles.append(a.parent);first=freeze(a)
            marker.write_text('untracked working-tree change')
            b=ROOT/'artifacts/development/run-bundles'/('test-'+uuid.uuid4().hex)/'bundle';bundles.append(b.parent);second=freeze(b)
            self.assertEqual(first,second)
            ma=decode((a/'build_metadata.json').read_bytes());mb=decode((b/'build_metadata.json').read_bytes())
            self.assertNotEqual(ma['source_status'],mb['source_status']);self.assertNotIn('source_status',decode((a/'inventory.json').read_bytes()))
            arts=decode((a/'designs_and_methods.json').read_bytes());formation=arts['formation_cohort']['content']
            for name,v in arts['variant_cohorts'].items():
                doc=v['content'];self.assertEqual(v['content_sha256'],digest(doc))
                if name=='original':self.assertNotIn('variant',doc);self.assertEqual(digest(doc),digest(formation))
                else:
                    self.assertEqual(doc['variant']['name'],name);self.assertEqual(doc['variant']['of_content_sha256'],digest(formation));self.assertIn('not independent corroboration',doc['variant']['standing'])
                    self.assertEqual(doc['item_id'],formation['item_id'])
        finally:
            marker.unlink(missing_ok=True)
            for d in bundles:shutil.rmtree(d,ignore_errors=True)
