"""The experiment profile boundary: what a profile may declare, what the core computes from it, and what it cannot change."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from adaptive_research_harness.encoding import Refusal, digest
from adaptive_research_harness.experiment import Experiment, row_ratio
from adaptive_research_harness.rules import Rules
from adaptive_research_harness.actors import invocation, event_ref
from .fabricated import Input, profile, ROOT

SYNTHETIC = json.loads((ROOT / 'experiments/synthetic_flow/experiment.json').read_bytes())
HEADLINES = json.loads((ROOT / 'examples/langgraph_headlines/experiment.json').read_bytes())


class ProfileLoading(unittest.TestCase):
    def test_both_profiles_load_and_declare_their_shape(self):
        s = Experiment(SYNTHETIC); h = Experiment(HEADLINES)
        self.assertEqual(s.steps_of('research'), ['research-counts', 'replacement-counts', 'verification-candidate']); self.assertEqual(s.steps_of('check'), ['check-transition'])
        self.assertEqual(s.core_labels(), ['tool-a', 'tool-b']); self.assertTrue(s.caller_executed('CHECK-A-1')); self.assertFalse(s.caller_executed('SYN-A-1'))
        self.assertEqual(h.core_labels(), []); self.assertTrue(h.caller_executed('FAKE-LLM-1')); self.assertTrue(h.may_outlive_caller('FAKE-LLM-1')); self.assertFalse(h.may_outlive_caller('CHECK-H-1'))
        self.assertEqual(h.file_module('FAKE-LLM-1'), 'tools/provider.py'); self.assertIsNone(s.file_module('SYN-A-1'))
    def test_malformed_profiles_are_refused(self):
        def mutant(change):
            d = deepcopy(SYNTHETIC); change(d); return d
        cases = {
            'unknown validator': lambda d: d['sources']['SRC-SYN']['extraction'].update(validator='python-code'),
            'non-synthetic source': lambda d: d['sources']['SRC-SYN']['document'].update(synthetic=False),
            'module outside the experiment': lambda d: d['tools']['SYN-A-1'].update(module='../../etc/evil.py'),
            'absolute module': lambda d: d['tools']['SYN-A-1'].update(module='/tmp/evil.py'),
            'unknown execution': lambda d: d['tools']['SYN-A-1'].update(execution='anywhere'),
            'missing provider_work': lambda d: d['tools']['SYN-A-1'].pop('provider_work'),
            'band ends before limit': lambda d: d['steps'][0]['tariff']['bands'].pop(),
            'two inputs': lambda d: d['steps'][0]['inputs'].update(count=2),
            'unknown step tool': lambda d: d['steps'][0]['tools'].append('NOT-A-TOOL'),
            'extra field': lambda d: d.update(rules='override'),
            'check without maximum': lambda d: d['steps'][3].pop('maximum'),
        }
        for name, change in cases.items():
            with self.subTest(name), self.assertRaises(Refusal) as ctx: Experiment(mutant(change))
            self.assertIn(ctx.exception.code, ('INVALID_PROFILE', 'MISSING_FIELD', 'UNKNOWN_FIELD'), name)

    def test_tariffs(self):
        s = Experiment(SYNTHETIC); h = Experiment(HEADLINES)
        self.assertEqual(s.expected_maximum(s.step('research-counts'), 0), 100); self.assertEqual(s.expected_maximum(s.step('research-counts'), 1024), 100)
        self.assertEqual(s.expected_maximum(s.step('research-counts'), 1025), 200); self.assertEqual(s.expected_maximum(s.step('research-counts'), 4096), 200)
        with self.assertRaises(Refusal): s.expected_maximum(s.step('research-counts'), 4097)
        self.assertEqual(h.expected_maximum(h.step('classify-headlines'), 24), 48); self.assertEqual(h.expected_maximum(h.step('classify-headlines'), 500), 1000)
        with self.assertRaises(Refusal): h.expected_maximum(h.step('classify-headlines'), 501)


class RowRatio(unittest.TestCase):
    def test_reproduces_the_src_syn_extraction(self):
        doc = profile().artifacts['formation_cohort']['content']; spec = SYNTHETIC['sources']['SRC-SYN']['extraction']
        self.assertEqual(row_ratio(spec, doc), (True, {'numerator': 2, 'denominator': 2}))
        small = deepcopy(doc)
        for r in small['rows']: r['size_units'] = 1
        self.assertEqual(row_ratio(spec, small), (False, None))
        dup = deepcopy(doc); dup['rows'][1]['event_id'] = dup['rows'][0]['event_id']; self.assertEqual(row_ratio(spec, dup)[0], False)
        typed = deepcopy(doc); typed['rows'][0]['spike'] = 1; self.assertEqual(row_ratio(spec, typed)[0], False)
    def test_headline_returns_extraction(self):
        rows = [{'row_id': 'a', 'next_day_return_bp': 5}, {'row_id': 'b', 'next_day_return_bp': -5}, {'row_id': 'c', 'next_day_return_bp': 0}]
        self.assertEqual(row_ratio(HEADLINES['sources']['SRC-RET-SYN']['extraction'], {'rows': rows}), (True, {'numerator': 1, 'denominator': 3}))


class RulesReadTheProfile(unittest.TestCase):
    def attempt_payload(self, x, step='research-counts', tool='SYN-A-1', parameters=None, maximum='1.00'):
        r = x.reservation(); inp = invocation(x.profile_dict(), tool, step, [event_ref(x.e[0])], {'threshold': 2} if parameters is None else parameters)
        return {'reservation': r['seq'], 'step': step, 'input': inp, 'dispatch_index': 0, 'maximum': maximum, 'tier': 1}
    def test_attempt_admission_follows_the_declared_steps_and_tariff(self):
        x = Input(); rules = Rules(x.profile)
        good = self.attempt_payload(x); self.assertEqual(rules.execute(x.view(), 'AD-R1.0', 'attempt', good, x.now)[0]['kind'], 'ATTEMPT')
        for name, payload, code in [
            ('tool not permitted for the step', self.attempt_payload(x, step='replacement-counts', tool='SYN-A-1'), 'INVALID_STEP'),
            ('step with no tools', self.attempt_payload(x, step='verification-candidate'), 'INVALID_STEP'),
            ('unknown step', dict(self.attempt_payload(x), step='anything'), 'INVALID_STEP'),
            ('parameters not the declared ones', self.attempt_payload(x, parameters={'threshold': 3}), 'CAPABILITY_UNSUPPORTED'),
            ('estimate off the tariff', self.attempt_payload(x, maximum='0.99'), 'INVALID_ESTIMATE'),
        ]:
            with self.subTest(name), self.assertRaises(Refusal) as ctx: rules.execute(x.view(), 'AD-R1.0', 'attempt', payload, x.now)
            self.assertEqual(ctx.exception.code, code, name)
    def test_observation_route_follows_the_declared_source_rules(self):
        x = Input(); rules = Rules(x.profile); g = x.profile.grants['AU-OBS-1']
        src = next(s for s in g['source_declarations'] if s['content']['SourceId'] == 'SRC-SYN'); doc = x.profile.artifacts['formation_cohort']['content']
        base = {'grant': 'AU-OBS-1', 'source': 'SRC-SYN', 'revision': src['SourceRevision'], 'form': 'DOCUMENT', 'period': {'start': doc['period_start'], 'end': doc['period_end']}, 'item_id': doc['item_id'], 'document': doc, 'slot': x.now}
        self.assertEqual(rules.execute(x.view(), 'Observation function', 'observation-commit', base, x.now)[0]['kind'], 'OBSERVATION')
        other = next(s for s in g['source_declarations'] if s['content']['SourceId'] == 'SRC-E')
        with self.assertRaises(Refusal) as ctx: rules.execute(x.view(), 'Observation function', 'observation-commit', dict(base, source='SRC-E', revision=other['SourceRevision']), x.now)
        self.assertEqual(ctx.exception.code, 'CAPABILITY_UNSUPPORTED')
        with self.assertRaises(Refusal) as ctx: rules.execute(x.view(), 'Observation function', 'observation-commit', dict(base, item_id='other-2026-10-28'), x.now)
        self.assertEqual(ctx.exception.code, 'INVALID_ITEM')
        unsynthetic = dict(base, document=dict(doc, synthetic=False))
        with self.assertRaises(Refusal) as ctx: rules.execute(x.view(), 'Observation function', 'observation-commit', unsynthetic, x.now)
        self.assertEqual(ctx.exception.code, 'INVALID_DOCUMENT')


class CallerExecutedTools(unittest.TestCase):
    """Dispatcher rules for tools the caller executes, with a fabricated engine that holds only what the rules read."""
    def dispatcher(self, x, claims, settlements):
        from adaptive_research_harness.dispatch import Dispatcher
        from adaptive_research_harness.encoding import canonical
        import sqlite3
        db = sqlite3.connect(':memory:'); db.row_factory = sqlite3.Row
        db.execute('CREATE TABLE dispatch_claims(attempt_seq INTEGER PRIMARY KEY, body BLOB NOT NULL, receipt BLOB)')
        for seq, body, receipt in claims: db.execute('INSERT INTO dispatch_claims VALUES(?,?,?)', (seq, canonical(body), canonical(receipt) if receipt else None))
        class Store: pass
        class Engine: pass
        e = Engine(); e.profile = x.profile; e.store = Store(); e.store.db = db; e.lock = __import__('threading').RLock()
        proofs = {}
        def verifier(path, inventory, core, worker):
            key = Path(path).name
            if key not in proofs: raise Refusal('WORKER_NOT_QUIESCENT')
            return proofs[key]
        d = Dispatcher(e, {}, '/nonexistent', generation_value={'pid': 1, 'run': 'x'}, quiescence_verifier=verifier)
        return d, proofs
    def test_replacement_rules_for_caller_tools(self):
        from adaptive_research_harness.encoding import digest
        x = Input(); r = x.reservation(actor='AD-CK-1.0', grant='AU-CK-A', purpose={'kind': 'Check', 'id': 'FABRICATED-2'})
        inp = invocation(x.profile_dict(), 'CHECK-A-1', 'check-transition', [event_ref(x.t[1], 'T')], {'transition_id': 'FABRICATED-2'})
        a = x.add('E', 'ATTEMPT', {'reservation': r['seq'], 'actor': 'AD-CK-1.0', 'grant': 'AU-CK-A', 'lineage': 'AD-CK-1', 'maximum': '0.25', 'input': inp, 'input_hash': digest(inp), 'step': 'check-transition', 'dispatch_index': 0, 'tier': 1, 'admission_generation': {'pid': 1, 'run': 'x'}}, 'AD-CK-1.0')
        worker = {'pid': 424242, 'run': 'x'}; claim = {'attempt': a['seq'], 'input_hash': digest(inp), 'core': {'pid': 1, 'run': 'x'}, 'worker': worker, 'tool_id': 'CHECK-A-1', 'inventory_sha256': x.profile.inventory_hash}
        candidate = dict(a['body'], dispatch_index=1)
        # Unsettled predecessor with a claim: never replaced.
        d, proofs = self.dispatcher(x, [(a['seq'], claim, None)], {})
        with self.assertRaises(Refusal) as ctx: d.ensure_retry(x.view(), 'AD-CK-1.0', candidate)
        self.assertEqual(ctx.exception.code, 'PENDING_PREDECESSOR')
        # Settled at UNKNOWN but the caller generation is not shown gone: refused; the core generation is irrelevant.
        x.add('E', 'SETTLEMENT', {'attempt': a['seq'], 'actual': '0.25', 'unit': 'simulated_research_units', 'provenance': {'kind': 'UNKNOWN'}, 'reservation': r['seq'], 'grant': 'AU-CK-A'}, 'AD-CK-1.0')
        d, proofs = self.dispatcher(x, [(a['seq'], claim, None)], {})
        with self.assertRaises(Refusal) as ctx: d.ensure_retry(x.view(), 'AD-CK-1.0', candidate)
        self.assertEqual(ctx.exception.code, 'WORKER_NOT_QUIESCENT')
        proofs[digest(worker) + '.json'] = {'terminated_generations': [worker]}
        d.ensure_retry(x.view(), 'AD-CK-1.0', candidate)   # ends_with_caller: the dead caller suffices
        # Settled without any claim: nothing was ever permitted to run.
        d2, _ = self.dispatcher(x, [], {}); d2.ensure_retry(x.view(), 'AD-CK-1.0', candidate)
    def test_provider_that_may_outlive_its_caller_needs_a_disposition(self):
        from adaptive_research_harness.encoding import digest
        x = Input(); x.profile.experiment = Experiment(HEADLINES)
        r = x.reservation(); step = 'classify-headlines'
        inp = {'schema_version': 1, 'tool_id': 'FAKE-LLM-1', 'tool_spec_hash': 'x', 'executable_hash': 'y', 'step': step, 'parameters': {}, 'input_refs': [event_ref(x.e[0])]}
        a = x.add('E', 'ATTEMPT', {'reservation': r['seq'], 'actor': 'AD-R1.0', 'grant': 'AU-RP-1', 'lineage': 'AD-R1', 'maximum': '0.48', 'input': inp, 'input_hash': digest(inp), 'step': step, 'dispatch_index': 0, 'tier': 1, 'admission_generation': {'pid': 1, 'run': 'x'}}, 'AD-R1.0')
        x.add('E', 'SETTLEMENT', {'attempt': a['seq'], 'actual': '0.48', 'unit': 'simulated_research_units', 'provenance': {'kind': 'UNKNOWN'}, 'reservation': r['seq'], 'grant': 'AU-RP-1'}, 'AD-R1.0')
        worker = {'pid': 424243, 'run': 'x'}; claim = {'attempt': a['seq'], 'input_hash': digest(inp), 'core': {'pid': 1, 'run': 'x'}, 'worker': worker, 'tool_id': 'FAKE-LLM-1', 'inventory_sha256': x.profile.inventory_hash}
        candidate = dict(a['body'], dispatch_index=1); d, proofs = self.dispatcher(x, [(a['seq'], claim, None)], {})
        proofs[digest(worker) + '.json'] = {'terminated_generations': [worker]}
        with self.assertRaises(Refusal) as ctx: d.ensure_retry(x.view(), 'AD-R1.0', candidate)
        self.assertEqual(ctx.exception.code, 'WORKER_NOT_QUIESCENT')
        for state in ('DEDUPLICATED', 'PENDING'):
            proofs[digest(worker) + '.json'] = {'terminated_generations': [worker], 'provider_dispositions': {str(a['seq']): {'state': state, 'claim_input_hash': digest(inp)}}}
            with self.subTest(state), self.assertRaises(Refusal): d.ensure_retry(x.view(), 'AD-R1.0', candidate)
        proofs[digest(worker) + '.json'] = {'terminated_generations': [worker], 'provider_dispositions': {str(a['seq']): {'state': 'CANCELLED', 'claim_input_hash': 'other'}}}
        with self.assertRaises(Refusal): d.ensure_retry(x.view(), 'AD-R1.0', candidate)
        proofs[digest(worker) + '.json'] = {'terminated_generations': [worker], 'provider_dispositions': {str(a['seq']): {'state': 'CANCELLED', 'claim_input_hash': digest(inp)}}}
        d.ensure_retry(x.view(), 'AD-R1.0', candidate)


class ReceiptBinding(unittest.TestCase):
    def test_finish_refuses_a_different_receipt_for_the_same_claim(self):
        """Through a real engine and store on a disposable bundle: the caller's first receipt binds; a second differing one is refused."""
        import tempfile, uuid
        from adaptive_research_harness.storage import Store
        from adaptive_research_harness.engine import Engine
        from adaptive_research_harness.dispatch import Dispatcher
        from adaptive_research_harness.clock import SyntheticClock
        from adaptive_research_harness.encoding import digest
        p = profile()
        with tempfile.TemporaryDirectory(prefix='arh-disposable-') as d:
            store = Store(Path(d) / 't.sqlite'); clock = SyntheticClock(Path(d) / 'clock.json', p.setup['clock']); clock.initialize()
            e = Engine(store, p, clock, {'inventory_sha256': p.inventory_hash, 'allow_apply_zero': True})
            disp = Dispatcher(e, {}, Path(d) / 'sup', generation_value={'pid': 1, 'run': 'x'}, quiescence_verifier=lambda *a: {}); e.dispatcher = disp
            good = {'constitution_sha256': p.setup['constitution']['sha256'], 'design': p.designs['AD-CK-1.0'], 'grant': p.grants['AU-CK-A']}
            self.assertEqual(e.command('Principal', str(uuid.uuid4()), 'genesis', good)['status'], 'COMMITTED')
            tr = 'TR-X'; content = {'action': 'GRANT', 'predecessor': None, 'grant': p.grants['AU-OBS-1']}
            e.command('Principal', str(uuid.uuid4()), 'propose', {'transition_id': tr, 'base': 0, 'class': 'AUTHORIZATION', 'subject': 'AU-OBS-1', 'content': content, 'grant': None, 'budget': '0.00', 'funding_ref': None, 'delta': {'O': 0, 'S': 0, 'A': 0}})
            r = e.command('AD-CK-1.0', str(uuid.uuid4()), 'reserve', {'grant': 'AU-CK-A', 'amount': '0.25', 'purpose': {'kind': 'Check', 'id': tr}}); self.assertEqual(r['status'], 'COMMITTED', r)
            pe = e.view().proposals[tr]; inp = invocation({'artifacts': p.artifacts, 'inventory': p.inventory}, 'CHECK-A-1', 'check-transition', [event_ref(pe, 'T')], {'transition_id': tr})
            a = e.command('AD-CK-1.0', str(uuid.uuid4()), 'attempt', {'reservation': r['refs'][0]['sequence'], 'step': 'check-transition', 'input': inp, 'dispatch_index': 0, 'maximum': '0.25', 'tier': 1}); self.assertEqual(a['status'], 'COMMITTED', a)
            seq = a['refs'][0]['sequence']; peer = {'pid': 77, 'run': 'x'}
            self.assertEqual(disp.run('AD-CK-1.0', seq, peer)['status'], 'PERMISSION_CONSUMED')
            self.assertEqual(disp.run('AD-CK-1.0', seq, peer)['status'], 'IN_PROGRESS_OR_UNCERTAIN')
            receipt = {'attempt': seq, 'input_hash': digest(inp), 'tool_id': 'CHECK-A-1', 'actual': '0.25', 'synthetic': True, 'result': None, 'error': 'x'}
            self.assertEqual(disp.finish('AD-CK-1.0', seq, receipt)['status'], 'RECEIPT')
            with self.assertRaises(Refusal) as ctx: disp.finish('AD-CK-1.0', seq, dict(receipt, error='y'))
            self.assertEqual(ctx.exception.code, 'RECEIPT_CONFLICT')
            with self.assertRaises(Refusal) as ctx: disp.finish('AD-CK-1.0', seq, dict(receipt, actual='0.50'))
            self.assertIn(ctx.exception.code, ('INVALID_TOOL_RECEIPT', 'RECEIPT_CONFLICT'))
            self.assertEqual(disp.run('AD-CK-1.0', seq, peer)['status'], 'RECEIPT')
            with self.assertRaises(Refusal) as ctx: disp.run('AD-R1.0', seq, peer)
            self.assertEqual(ctx.exception.code, 'UNAUTHORIZED')
            store.close()


LOCAL = json.loads((ROOT / 'experiments/local_documents/experiment.json').read_bytes())


class HistoricalDocuments(unittest.TestCase):
    """The document class and the shapes the local-documents workflow needs, through Rules with fabricated views."""
    def local_input(self):
        x = Input(); x.profile.experiment = Experiment(LOCAL); return x
    def doc(self, text='alpha beta', name='a.md', date='2026-10-30'):
        import hashlib
        raw = text.encode(); sha = hashlib.sha256(raw).hexdigest()
        return {'class': 'historical', 'synthetic': False, 'file': {'name': name, 'sha256': sha, 'bytes': len(raw), 'media_type': 'text/markdown'},
                'provenance': {'origin': 'test', 'received_at': '2026-10-31T00:00:00.000Z', 'note': ''}, 'text': text,
                'item_id': 'doc-' + date + '-' + sha[:16], 'period_start': date + 'T00:00:00.000Z', 'period_end': '2026-10-31T00:00:00.000Z', 'claimed_publication_time': '2026-10-31T00:00:00.000Z'}
    def observation(self, x, d, **over):
        g = x.profile.grants['AU-OBS-1']; src = next(s for s in g['source_declarations'] if s['content']['SourceId'] == 'SRC-SYN')
        p = {'grant': 'AU-OBS-1', 'source': 'SRC-SYN', 'revision': src['SourceRevision'], 'form': 'DOCUMENT', 'period': {'start': d['period_start'], 'end': d['period_end']}, 'item_id': d['item_id'], 'document': d, 'slot': x.now}
        p.update(over); return p
    def test_profile_loads_with_the_new_shapes(self):
        e = Experiment(LOCAL)
        self.assertEqual(e.document_class('SRC-LOCAL-DOC'), 'historical'); self.assertEqual(e.steps['analyze-documents']['tariff']['measure'], 'documents')
        self.assertEqual(e.expected_maximum(e.step('analyze-documents'), 3), 30); self.assertEqual(e.tool('LOCAL-CALC-1')['interface'], 'inputs')
        with self.assertRaises(Refusal): e.extract('SRC-LOCAL-DOC', {})
        bad = deepcopy(LOCAL); bad['sources']['SRC-LOCAL-DOC']['document']['class'] = 'prospective'
        with self.assertRaises(Refusal): Experiment(bad)
        bad = deepcopy(LOCAL); bad['steps'][0]['inputs'] = [{'kind': 'RESEARCH_RECORD', 'min': 0, 'max': 1, 'record_kind': 'EXPERIMENT DESIGN'}]
        with self.assertRaises(Refusal): Experiment(bad)
    def test_historical_document_rules(self):
        """A source declared historical refuses synthetic labels and incomplete provenance, and stamps the class it admits."""
        x = Input(); rules = Rules(x.profile)
        local = deepcopy(SYNTHETIC); local['sources']['SRC-SYN']['document'] = {'class': 'historical', 'synthetic': False, 'max_bytes': 4194304}
        local['sources']['SRC-SYN']['item_id'] = {'prefix': 'cohort-', 'per_period': 'many'}; local['sources']['SRC-SYN']['extraction'] = {'validator': 'none'}
        x.profile.experiment = Experiment(local); now = x.now + 3 * 86400000
        d = self.doc(); d['item_id'] = 'cohort-2026-10-30-' + d['file']['sha256'][:16]
        out = rules.execute(x.view(), 'Observation function', 'observation-commit', self.observation(x, d, slot=now), now)[0]
        self.assertEqual(out['body']['class'], 'historical'); self.assertFalse(out['body']['synthetic'])
        for name, change, code in [
            ('synthetic label on a historical source', lambda q: q['document'].update({'class': 'synthetic', 'synthetic': True}), 'INVALID_DOCUMENT'),
            ('missing provenance', lambda q: q['document'].pop('provenance'), 'INVALID_DOCUMENT'),
            ('file hash not in the item id', lambda q: q.update(item_id='cohort-2026-10-30-0000000000000000') or q['document'].update(item_id='cohort-2026-10-30-0000000000000000'), 'INVALID_ITEM'),
            ('listing for a many-per-period source', lambda q: q.update(form='COMPLETE', document=None, items=[q['item_id']], window=q['period']), 'CAPABILITY_UNSUPPORTED'),
        ]:
            q = self.observation(x, deepcopy(d), slot=now); change(q)
            with self.subTest(name), self.assertRaises(Refusal) as ctx: rules.execute(x.view(), 'Observation function', 'observation-commit', q, now)
            self.assertEqual(ctx.exception.code, code, name)
        committed = x.add('E', 'OBSERVATION', dict(self.observation(x, d, slot=now), **{'class': 'historical', 'synthetic': False}), 'Observation function')
        q = dict(self.observation(x, d, slot=now), form='VALUE', document=None, document_ref={'ledger': 'E', 'sequence': committed['seq'], 'sha256': committed['sha256']}, value={'numerator': 1, 'denominator': 1})
        with self.assertRaises(Refusal) as ctx: rules.execute(x.view(), 'Observation function', 'observation-commit', q, now)
        self.assertEqual(ctx.exception.code, 'CAPABILITY_UNSUPPORTED')
        # The synthetic source still refuses a historical document.
        y = Input(); q = self.observation(y, dict(y.profile.artifacts['formation_cohort']['content'], **{'class': 'historical', 'synthetic': False}))
        with self.assertRaises(Refusal) as ctx: Rules(y.profile).execute(y.view(), 'Observation function', 'observation-commit', q, y.now)
        self.assertEqual(ctx.exception.code, 'INVALID_DOCUMENT')
    def test_design_records_without_an_attempt_and_class_inheritance(self):
        x = Input(); rules = Rules(x.profile)
        body = {'grant': 'AU-RP-1', 'attempt': None, 'question': 'q', 'result': {'expectation': {}}, 'failure': None, 'closure': {'E': len(x.e), 'N': x.n, 'refs': [event_ref(x.e[0])]},
                'claims': [{'kind': 'QUESTION', 'text': 'q'}], 'kind': 'EXPERIMENT DESIGN', 'snapshot': {'identity': 'x', 'sha256': x.e[0]['sha256']}, 'source_cutoff': '2026-10-29T00:00:00.000Z',
                'parameters': {}, 'tool': {'id': 'SYN-A-1', 'planned': True}, 'reproducibility': {'input_refs': [], 'invocation_hash': None, 'result_hash': digest({'expectation': {}})}, 'synthetic': True, 'class': 'synthetic'}
        self.assertEqual(rules.execute(x.view(), 'AD-R1.0', 'research-commit', body, x.now)[0]['kind'], 'RESEARCH_RECORD')
        with self.assertRaises(Refusal) as ctx: rules.execute(x.view(), 'AD-R1.0', 'research-commit', dict(body, kind='plain'), x.now)
        self.assertEqual(ctx.exception.code, 'UNAUTHORIZED')
        with self.assertRaises(Refusal) as ctx: rules.execute(x.view(), 'AD-R1.0', 'research-commit', dict(body, synthetic=False), x.now)
        self.assertEqual(ctx.exception.code, 'INVALID_CLASS')
        # A record citing a historical document cannot call itself synthetic.
        hist = x.add('E', 'OBSERVATION', {'form': 'DOCUMENT', 'source': 'SRC-SYN', 'document': self.doc(), 'class': 'historical', 'synthetic': False}, 'Observation function')
        cites = dict(body, closure={'E': len(x.e), 'N': x.n, 'refs': [event_ref(hist)]})
        with self.assertRaises(Refusal) as ctx: rules.execute(x.view(), 'AD-R1.0', 'research-commit', cites, x.now)
        self.assertEqual(ctx.exception.code, 'INVALID_CLASS')
        self.assertEqual(rules.execute(x.view(), 'AD-R1.0', 'research-commit', dict(cites, synthetic=False, **{'class': 'historical'}), x.now)[0]['body']['class'], 'historical')
        # A revision must name an earlier record of the same actor.
        prior = x.add('E', 'RESEARCH_RECORD', {'kind': 'EXPERIMENT DESIGN'}, 'AD-R1.0'); other = x.add('E', 'RESEARCH_RECORD', {'kind': 'EXPERIMENT DESIGN'}, 'AD-R2.0')
        self.assertEqual(rules.execute(x.view(), 'AD-R1.0', 'research-commit', dict(body, closure={'E': len(x.e), 'N': x.n, 'refs': [event_ref(x.e[0])]}, revises=event_ref(prior)), x.now)[0]['kind'], 'RESEARCH_RECORD')
        with self.assertRaises(Refusal) as ctx: rules.execute(x.view(), 'AD-R1.0', 'research-commit', dict(body, closure={'E': len(x.e), 'N': x.n, 'refs': [event_ref(x.e[0])]}, revises=event_ref(other)), x.now)
        self.assertEqual(ctx.exception.code, 'INVALID_REVISION')
    def test_attempts_match_declared_input_shapes_and_measures(self):
        x = Input(); rules = Rules(x.profile)
        local = deepcopy(SYNTHETIC)
        local['steps'][0]['inputs'] = [{'kind': 'OBSERVATION', 'form': 'DOCUMENT', 'min': 1, 'max': 3}, {'kind': 'RESEARCH_RECORD', 'record_kind': 'EXPERIMENT DESIGN', 'min': 1, 'max': 1}]
        local['steps'][0]['tariff'] = {'measure': 'documents', 'limit': 3, 'per_unit': '0.10'}
        x.profile.experiment = Experiment(local)
        design = x.add('E', 'RESEARCH_RECORD', {'kind': 'EXPERIMENT DESIGN', 'analysis': {}}, 'AD-R1.0'); other = x.add('E', 'RESEARCH_RECORD', {'kind': 'EXPERIMENT DESIGN'}, 'AD-R2.0')
        doc2 = x.add('E', 'OBSERVATION', {'form': 'DOCUMENT', 'document': x.profile.artifacts['formation_cohort']['content']}, 'Observation function')
        r = x.reservation()
        def payload(refs, maximum):
            inp = invocation(x.profile_dict(), 'SYN-A-1', 'research-counts', refs, {'threshold': 2})
            return {'reservation': r['seq'], 'step': 'research-counts', 'input': inp, 'dispatch_index': 0, 'maximum': maximum, 'tier': 1}
        self.assertEqual(rules.execute(x.view(), 'AD-R1.0', 'attempt', payload([event_ref(x.e[0]), event_ref(doc2), event_ref(design)], '0.20'), x.now)[0]['kind'], 'ATTEMPT')
        for name, refs, maximum, code in [
            ('no design record', [event_ref(x.e[0])], '0.10', 'INVALID_INPUT'),
            ("another actor's design", [event_ref(x.e[0]), event_ref(other)], '0.10', 'INVALID_INPUT'),
            ('two designs', [event_ref(x.e[0]), event_ref(design), event_ref(design)], '0.10', 'INVALID_INPUT'),
            ('estimate off the per-document tariff', [event_ref(x.e[0]), event_ref(design)], '0.20', 'INVALID_ESTIMATE'),
        ]:
            with self.subTest(name), self.assertRaises(Refusal) as ctx: rules.execute(x.view(), 'AD-R1.0', 'attempt', payload(refs, maximum), x.now)
            self.assertEqual(ctx.exception.code, code, name)
