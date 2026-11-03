"""The Principal's own documents through the workbench session: provenance, expectation, analysis, check, selection, revision, rejection, stop and resume."""
from pathlib import Path
import json
import os
import shutil
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'client'))
from workbench.local_session import LocalRun, open_local, RUNS, derive
from workbench.session import list_runs
from workbench import records

MEMOS = {'memo-a.md': 'Q3 review. Revenue beat guidance and margins expanded. Management raised the outlook and discussed a buyback.',
         'memo-b.md': 'Q3 review. Revenue missed guidance on weak demand. Management cut the outlook. No buyback discussed.',
         'memo-c.md': 'Q3 review. Revenue in line. Management reiterated the outlook and announced a dividend increase and a buyback.'}
TABLE = 'ticker,day,return_bp,guidance\nAAA,1,120,raised\nBBB,1,-90,cut\nCCC,1,40,reiterated\nAAA,2,30,raised\nBBB,2,-20,cut\n'
TERMS = {'comparator': '>=', 'value': {'numerator': 2, 'denominator': 3}, 'minimum_n': 3, 'statement': 'at least two in three memos contain raised, beat, buyback or increase'}


class LocalDocuments(unittest.TestCase):
    created = []
    @classmethod
    def tearDownClass(cls):
        for name in cls.created: shutil.rmtree(RUNS / name, ignore_errors=True)

    def test_one_usable_workflow_with_stop_and_resume(self):
        name = 'test-local-' + os.urandom(3).hex(); self.created.append(name)
        s = LocalRun.create('# Charter\nDo management tone words in Q3 memos line up with next-day returns?\n', name)
        try:
            v = s.view(); self.assertEqual(v['state']['N'], 5); self.assertEqual(v['charter']['class'], 'historical'); self.assertEqual(v['charter']['name'], 'charter.md')
            for n, text in MEMOS.items():
                o = s.import_document(n, text.encode(), 'local folder', note='Q3 memos', date='2026-10-30'); self.assertTrue(o.ok, o)
            v = s.view(); self.assertEqual([d['name'] for d in v['documents']], list(MEMOS)); self.assertTrue(all(d['class'] == 'historical' and d['file_sha256'] and d['origin'] == 'local folder' for d in v['documents']))
            # expectation recorded before the analysis, as a design record with no attempt
            d1 = s.design('Do most Q3 memos use positive tone words?', TERMS, {'kind': 'term-count', 'terms': ['raised', 'beat', 'buyback', 'increase']}, [d['seq'] for d in v['documents']])
            self.assertTrue(d1.ok, d1); v = s.view(); self.assertEqual(v['next'][0]['op'], 'run'); self.assertIsNone(v['investigations'][0].get('result'))
            r1 = s.run(d1.sequence); self.assertEqual(r1['status'], 'recorded', r1); self.assertEqual(r1['conclusion']['state'], 'MET'); self.assertEqual(r1['conclusion']['metric'], {'numerator': 3, 'denominator': 3})
            self.assertEqual(r1['execution'], 'registered'); self.assertTrue(r1['settlement'].ok)
            v = s.view(); inv = v['investigations'][0]; self.assertEqual(inv['result']['conclusion']['state'], 'MET'); self.assertTrue(inv['result']['settled']); self.assertEqual(v['next'][0]['op'], 'select')
            self.assertEqual([c['id'] for c in s.candidates(inv['result']['seq'])], ['extend', 'sharpen', 'alternative'])
            with self.assertRaises(AssertionError): s.select(inv['result']['seq'], 'reject', 'not a candidate for a met expectation', 'x')
            sel = s.select(inv['result']['seq'], 'extend', 'three memos is a small set', 'Do memos with positive tone match raised guidance in the trade table?'); self.assertTrue(sel.ok, sel)
            v = s.view(); self.assertEqual(v['next'][0]['op'], 'propose'); self.assertEqual(v['investigations'][0]['selection']['rejections'][0]['id'], 'sharpen')
            pr = s.propose(sel.sequence); self.assertTrue(pr.ok, pr); self.assertTrue(pr.raw['funded'])
            v = s.view(); self.assertEqual(v['next'][0]['op'], 'check')
            # the researcher cannot admit its own direction
            self.assertEqual(s.researcher.c.call('decide', {'transition_id': pr.transition_id, 'check': 1, 'decision': 'ADMITTED', 'reason': 'self'}).reason, 'UNAUTHORIZED')
            c1 = s.check(pr.transition_id); self.assertEqual(c1.result, 'PASS', c1.criteria)
            v = s.view(); self.assertEqual(v['next'][0]['op'], 'decide')
            d = s.decide(pr.transition_id, 'ADMITTED', 'next investigation admitted'); self.assertTrue(d.ok, d)
            v = s.view(); self.assertEqual(v['next'][0]['op'], 'apply'); a = s.apply(pr.transition_id); self.assertTrue(a.ok, a)
            v = s.view(); self.assertEqual(v['state']['N'], 6); self.assertIn('TH-L1', v['state']['themes']); self.assertEqual(v['next'], [])
            self.assertEqual(v['budgets']['AU-RL-1']['committed'], '0.30')
            # a revision that fails its expectation is kept beside the first, and its direction can be rejected by the Principal
            t = s.import_document('trades.csv', TABLE.encode(), 'local folder', note='trade table', date='2026-10-30'); self.assertTrue(t.ok)
            v = s.view(); table = next(x for x in v['documents'] if x['name'] == 'trades.csv'); self.assertEqual(table['rows'], 5)
            d2 = s.design('Do raised-guidance days return at least 100bp?', {'comparator': '>=', 'value': {'numerator': 1, 'denominator': 1}, 'minimum_n': 2, 'statement': 'every raised-guidance row returns at least 100bp'},
                          {'kind': 'table-stat', 'stat': 'ratio', 'filter': [{'field': 'guidance', 'equals': 'raised'}], 'numerator': [{'field': 'return_bp', 'at_least': 100}]}, [table['seq']], revises=d1.sequence, theme='TH-L1')
            self.assertTrue(d2.ok, d2); r2 = s.run(d2.sequence); self.assertEqual(r2['conclusion']['state'], 'NOT_MET'); self.assertEqual(r2['conclusion']['metric'], {'numerator': 1, 'denominator': 2})
            v = s.view(); i2 = v['investigations'][1]; self.assertEqual(i2['revises'], d1.sequence); self.assertEqual(i2['theme'], 'TH-L1')
            sel2 = s.select(i2['result']['seq'], 'reject', 'half the raised days fell short', 'Is a weaker claim, a positive return on raised days, supported?'); pr2 = s.propose(sel2.sequence)
            c2 = s.check(pr2.transition_id); self.assertEqual(c2.result, 'PASS', c2.criteria)
            dd = s.decide(pr2.transition_id, 'REJECTED', 'not now'); self.assertTrue(dd.ok, dd)
            v = s.view(); self.assertEqual(v['investigations'][1]['proposal']['decision']['decision'], 'REJECTED'); self.assertEqual(v['state']['N'], 6); self.assertEqual(v['next'], [])
            self.assertEqual(v['investigations'][0]['result']['conclusion']['state'], 'MET'); self.assertEqual(v['investigations'][1]['result']['conclusion']['state'], 'NOT_MET')
            self.assertEqual(s.reader()['status'], 'NOT_AVAILABLE')
            # a tampered conclusion: an analysis record claiming MET where the arithmetic says NOT_MET fails the independent check
            from arh_client import event_ref
            lr = s.researcher; an = lr.c.get({'ledger': 'E', 'sequence': i2['result']['seq'], 'sha256': i2['result']['sha256']})
            forged = {k: v for k, v in an['body'].items() if k != 'witness'}; forged['conclusion'] = dict(forged['conclusion'], state='MET'); forged['closure'] = dict(forged['closure'], E=lr.c.clock()['E'])
            fr = lr.r.research_commit(forged, None); self.assertTrue(fr.ok, fr)
            fs = lr.select(fr.ref, 'extend', 'forged', 'forged next'); fp = lr.propose(fs.ref, 'TH-L9')
            fc = s.check(fp.transition_id); self.assertEqual(fc.result, 'FAIL'); self.assertEqual(fc.criteria['motivation'], 'NOT MET')
            self.assertEqual(s.decide(fp.transition_id, 'ADMITTED', 'try').reason, 'CHECK_NOT_PASS'); self.assertEqual(s.view()['state']['N'], 6)
            es_before, ts_before = s.records()
        finally: s.close()
        self.assertFalse((RUNS / name / 'state' / 'connection.json').exists())
        # resume: same records, nothing re-executed, the same next actions
        r = open_local(RUNS / name); self.assertEqual(r.mode, 'live')
        try:
            v = r.view(); self.assertEqual(v['state']['N'], 6); self.assertEqual(len(v['investigations']), 3); self.assertEqual(v['pending_attempts'], [])
            es, ts = r.records(); self.assertEqual(es, es_before); self.assertEqual(ts, ts_before)
            self.assertEqual(len([e for e in es if e['kind'] == 'ATTEMPT' and e['actor'] == 'AD-L1.0']), 2)
            listed = {x['run']: x for x in list_runs()}; self.assertEqual(listed[name]['kind'], 'local'); self.assertTrue(listed[name]['live_eligible'])
        finally: r.close()
        # a retained run under a differing build opens read-only with the same derivation
        old = RUNS / (name + '-old'); self.created.append(old.name); shutil.copytree(RUNS / name, old, ignore=shutil.ignore_patterns('*.sock', 'fixture.json', 'connection.json'))
        from workbench.demo import differing_build
        differing_build(old / 'bundle')
        ro = open_local(old); self.assertEqual(ro.mode, 'read-only'); self.assertEqual(len(ro.view()['investigations']), 3); self.assertEqual(ro.view()['state']['N'], 6)

    def test_derive_on_empty_ledgers(self):
        d = derive([], []); self.assertEqual(d['investigations'], []); self.assertEqual(d['next'], []); self.assertIsNone(d['charter'])


class LocalApi(unittest.TestCase):
    """The page's routes: start with a charter, import, design, run, select, propose, check, decide, apply, close and reopen."""
    created = []
    @classmethod
    def setUpClass(cls):
        import threading
        from workbench.api import serve
        cls.bench, cls.server = serve(0); cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True); cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.bench.close_all(); cls.server.shutdown()
        for name in cls.created: shutil.rmtree(RUNS / name, ignore_errors=True)
    def req(self, method, path, body=None):
        from http.client import HTTPConnection
        c = HTTPConnection('127.0.0.1', self.port, timeout=180); c.request(method, path, json.dumps(body) if body is not None else None, {'Content-Type': 'application/json'})
        r = c.getresponse(); data = r.read(); c.close()
        return r.status, (json.loads(data) if r.getheader('Content-Type', '').startswith('application/json') else data)
    def test_local_page_and_routes(self):
        import time
        status, html = self.req('GET', '/local'); self.assertEqual(status, 200); self.assertIn(b'Research on your documents', html)
        status, r = self.req('POST', '/api/local/runs', {'charter': '', 'name': None}); self.assertEqual(r.get('error'), 'CHARTER_REQUIRED')
        name = 'test-localapi-' + os.urandom(3).hex(); self.created.append(name)
        status, r = self.req('POST', '/api/local/runs', {'charter': 'Which memos mention a buyback?', 'name': name}); self.assertEqual(status, 202)
        deadline = time.monotonic() + 120
        while time.monotonic() < deadline:
            status, v = self.req('GET', f'/api/runs/{name}')
            if v.get('mode') or v.get('status') == 'failed': break
            time.sleep(.5)
        self.assertEqual(v.get('mode'), 'live', v); self.assertEqual(v['state']['N'], 5)
        for n, text in MEMOS.items():
            status, o = self.req('POST', f'/api/runs/{name}/documents', {'name': n, 'text': text, 'origin': 'folder', 'note': 'memo', 'date': '2026-10-30'}); self.assertEqual(o['status'], 'COMMITTED', o)
        status, v = self.req('GET', f'/api/runs/{name}'); docs = [d['seq'] for d in v['documents']]; self.assertEqual(len(docs), 3)
        status, d = self.req('POST', f'/api/runs/{name}/design', {'question': 'Do most memos mention a buyback?', 'expectation': {'statement': 'at least two in three', 'comparator': '>=', 'value': {'numerator': 2, 'denominator': 3}, 'minimum_n': 3},
                                                                   'analysis': {'kind': 'term-count', 'terms': ['buyback'], 'case_sensitive': False}, 'documents': docs}); self.assertEqual(d['status'], 'COMMITTED', d)
        status, run = self.req('POST', f'/api/runs/{name}/run', {'design': d['ref']['sequence']}); self.assertEqual(run['status'], 'recorded', run); self.assertEqual(run['conclusion']['state'], 'MET')
        status, v = self.req('GET', f'/api/runs/{name}'); inv = v['investigations'][0]; self.assertEqual(v['next'][0]['op'], 'select')
        status, cands = self.req('POST', f'/api/runs/{name}/candidates', {'analysis': inv['result']['seq']}); self.assertEqual([c['id'] for c in cands['candidates']], ['extend', 'sharpen', 'alternative'])
        status, sel = self.req('POST', f'/api/runs/{name}/select', {'analysis': inv['result']['seq'], 'chosen': 'sharpen', 'reason': 'two of three is loose', 'next_question': 'Do all memos mention a buyback?'}); self.assertEqual(sel['status'], 'COMMITTED')
        status, pr = self.req('POST', f'/api/runs/{name}/propose', {'selection': sel['ref']['sequence']}); self.assertEqual(pr['status'], 'COMMITTED', pr); tr = pr['transition_id']
        status, bad = self.req('POST', f'/api/runs/{name}/decide', {'transition': tr, 'decision': 'ADMITTED', 'reason': 'too early'}); self.assertEqual(status, 409); self.assertEqual(bad['error'], 'NO_CHECK')
        status, c = self.req('POST', f'/api/runs/{name}/check', {'transition': tr}); self.assertEqual(c['result'], 'PASS', c)
        status, dec = self.req('POST', f'/api/runs/{name}/decide', {'transition': tr, 'decision': 'ADMITTED', 'reason': 'go'}); self.assertEqual(dec['status'], 'COMMITTED', dec)
        status, ap = self.req('POST', f'/api/runs/{name}/apply', {'transition': tr}); self.assertEqual(ap['status'], 'COMMITTED', ap)
        status, v = self.req('GET', f'/api/runs/{name}'); self.assertEqual(v['state']['N'], 6); self.assertEqual(v['next'], [])
        status, st = self.req('POST', f'/api/runs/{name}/step', {'op': 'research'}); self.assertNotEqual(status, 200)
        status, closed = self.req('POST', f'/api/runs/{name}/close'); self.assertEqual(closed['status'], 'closed')
        status, v = self.req('POST', f'/api/runs/{name}/open'); self.assertEqual(status, 200); self.assertEqual(v['mode'], 'live'); self.assertEqual(v['state']['N'], 6); self.assertEqual(len(v['investigations']), 1)
        status, runs = self.req('GET', '/api/runs'); self.assertTrue(any(x['run'] == name and x['kind'] == 'local' and x['progress'] == 'complete' for x in runs['runs']))
