"""The everyday interface: a two-source analysis through LangGraph with the awkward interruption points, plus the client pieces under it."""
from pathlib import Path
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'client'))
from arh_client.operations import OperationStore, resolve_stage
from arh_client.results import Outcome
from arh_client.langgraph_nodes import merge_operations
from arh_client.analysis import check_records, conclude, Inputs
from arh_client.project import Project
from arh_client.refusals import explain


class FakeConnection:
    def __init__(self, known): self.known = known; self.sent = []
    def outcome(self, key): return self.known.get(key, {'status': 'UNKNOWN'})


class Journal(unittest.TestCase):
    def test_keys_persist_before_use_and_a_lost_reply_is_resolved_from_the_core(self):
        with tempfile.TemporaryDirectory() as d:
            store = OperationStore(d); e = store.begin('join', 'analysis', work={'tool': 'T'}); again = store.begin('join', 'analysis', work={'tool': 'T'})
            self.assertEqual(e['keys'], again['keys']); self.assertEqual(sorted(e['keys']), ['attempt', 'close', 'design', 'record', 'reserve', 'settle'])
            committed = {'status': 'COMMITTED', 'refs': [{'ledger': 'E', 'sequence': 9, 'sha256': 'x'}]}
            c = FakeConnection({e['keys']['reserve']: committed})
            sent = []
            r = resolve_stage(c, e, 'reserve', lambda key: sent.append(key) or Outcome.from_reply({'status': 'COMMITTED', 'refs': []}), store)
            self.assertEqual(sent, []); self.assertEqual(r.sequence, 9)   # the core already had it: nothing is re-sent
            r2 = resolve_stage(c, store.get('join'), 'attempt', lambda key: sent.append(key) or Outcome.from_reply({'status': 'REFUSED', 'reason': 'X', 'refs': []}), store)
            self.assertEqual(sent, [e['keys']['attempt']]); self.assertFalse(r2.ok)
            r3 = resolve_stage(c, store.get('join'), 'attempt', lambda key: sent.append(key), store); self.assertEqual(len(sent), 1); self.assertEqual(r3.reason, 'X')   # journaled: final
            with self.assertRaises(Exception): store.begin('join', 'call')
    def test_state_namespaces_merge_by_operation(self):
        a = {'join': {'status': 'recorded', 'evidence': 1}}; b = {'placebo': {'status': 'recorded'}, 'join': {'review': 'applied'}}
        self.assertEqual(merge_operations(a, b), {'join': {'status': 'recorded', 'evidence': 1, 'review': 'applied'}, 'placebo': {'status': 'recorded'}})


class Conclusions(unittest.TestCase):
    def test_results_broader_than_metric_and_n(self):
        self.assertEqual(conclude({'table': [1, 2]}, None, 'Q?')['state'], 'RECORDED')
        self.assertEqual(conclude({'table': [1, 2]}, {'comparator': '>=', 'value': 1, 'statement': 's'}, 'Q?')['state'], 'INCONCLUSIVE')
        self.assertEqual(conclude({'metric': {'numerator': 2, 'denominator': 3}, 'n': 3}, {'comparator': '>=', 'value': {'numerator': 1, 'denominator': 2}, 'minimum_n': 3, 'statement': 's'}, 'Q?')['state'], 'MET')
    def test_a_selection_without_a_rule_names_its_own_question(self):
        self.assertTrue(check_records({'documents': [{'seq': 1}], 'records': [], 'evidence': {}, 'proposer': 'Principal'}, lambda i, s, r: True))
        doc = {'seq': 1, 'sha256': 'd', 'kind': 'OBSERVATION', 'body': {'form': 'DOCUMENT', 'document': {'rows': [{'a': 1}]}}}
        design = {'seq': 2, 'sha256': 'g', 'kind': 'RESEARCH_RECORD', 'actor': 'R', 'body': {'kind': 'EXPERIMENT DESIGN', 'question': 'Q?', 'analysis': {'kind': 'k'}, 'expectation': None}}
        res = {'x': 1, 'design': {'seq': 2, 'sha256': 'g'}, 'inputs': [{'seq': 1, 'sha256': 'd'}]}
        from arh_client.protocol import digest
        attempt = {'seq': 3, 'kind': 'ATTEMPT', 'actor': 'R', 'body': {'input': {'input_refs': [{'sequence': 1, 'sha256': 'd'}, {'sequence': 2, 'sha256': 'g'}]}}}
        analysis = {'seq': 4, 'sha256': 'a', 'kind': 'RESEARCH_RECORD', 'actor': 'R', 'body': {'kind': 'plain', 'attempt': 3, 'design': {'sequence': 2, 'sha256': 'g'}, 'result': res, 'reproducibility': {'result_hash': digest(res)}, 'conclusion': {'state': 'RECORDED'}}}
        settlement = {'seq': 5, 'kind': 'SETTLEMENT', 'body': {'attempt': 3}}
        selection = {'seq': 6, 'sha256': 's', 'kind': 'RESEARCH_RECORD', 'actor': 'R', 'body': {'kind': 'SELECTION', 'result': {'analysis': {'seq': 4, 'sha256': 'a'}, 'chosen': 'own', 'candidates': [], 'rejections': []}}}
        ev = {e['seq']: e for e in (doc, design, attempt, analysis, settlement, selection)}
        ctx = {'documents': [doc], 'records': [design, analysis, selection], 'evidence': ev, 'proposer': 'R'}
        self.assertTrue(check_records(ctx, lambda inputs, spec, result: isinstance(inputs, Inputs) and inputs.rows == [{'a': 1}] and result['x'] == 1))
        self.assertFalse(check_records(ctx, lambda inputs, spec, result: False))
        selection['body']['result']['chosen'] = 'something-else'; self.assertFalse(check_records(ctx, lambda i, s, r: True))
    def test_refusals_explain_themselves(self):
        meaning, action = explain('WORKER_NOT_QUIESCENT'); self.assertIn('quiescence', action.lower()); self.assertEqual(len(explain('NO_SUCH_CODE')), 2)


class ProjectFile(unittest.TestCase):
    def test_setup_files_regenerate_byte_identical_from_project_json(self):
        for example in ('examples/signal_groups', 'examples/memo_returns'):
            src = ROOT / example
            with tempfile.TemporaryDirectory() as d:
                data = json.loads((src / 'project.json').read_bytes()); (Path(d) / 'project.json').write_text(json.dumps(data))
                Project.load(d).write_setup()
                for f in ('setup.json', 'designs_and_methods.json', 'experiment.json'):
                    with self.subTest(example=example, file=f): self.assertEqual((Path(d) / f).read_bytes(), (src / f).read_bytes())
    def test_project_resolves_analyses_and_budgets(self):
        p = Project.load(ROOT / 'examples/memo_returns')
        self.assertEqual(p.tool_id('tone-return-join'), 'TONE-JOIN-1'); self.assertEqual(p.budget('memo-tests')['purpose'], {'kind': 'Theme', 'id': 'TH-M0'}); self.assertEqual(p.actor('checker'), 'AD-CK-M1.0')
        with self.assertRaises(Exception): p.budget('no-such-budget')


class TwoSourceExample(unittest.TestCase):
    name = 'test-memo-' + os.urandom(3).hex()
    @classmethod
    def tearDownClass(cls): shutil.rmtree(ROOT / 'artifacts' / 'development' / 'memo_returns' / cls.name, ignore_errors=True)
    def test_every_demonstration_holds(self):
        venv = ROOT / '.venv' / 'bin' / 'python'
        if not venv.exists(): self.skipTest('needs .venv with the langgraph extra')
        import subprocess
        proc = subprocess.run([str(venv), '-m', 'examples.memo_returns', '--name', self.name, '--quiet'], cwd=ROOT, capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        report = json.loads((ROOT / 'artifacts' / 'development' / 'memo_returns' / self.name / 'report.json').read_text())
        self.assertEqual(proc.returncode, 0, proc.stderr[-2000:]); self.assertEqual(report['status'], 'PASS', report['lines'][-15:])
        for name, ok in report['checks'].items():
            with self.subTest(name): self.assertTrue(ok, name)
        self.assertEqual(report['results']['join']['state'], 'MET'); self.assertEqual(report['results']['placebo']['state'], 'MET'); self.assertEqual(report['state'], 6)
        self.assertLess(report['line_groups']['configuration'] + report['line_groups']['process'], report['line_groups']['research'])
