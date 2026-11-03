"""The signal-groups example: the script verified on its own, the candidate rule through the client, the demonstration, and a user's own CSV through the command line."""
from pathlib import Path
import ast
import os
import shutil
import statistics
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'client'))
from examples.signal_groups.signal_groups import analyze, read_csv
from examples.signal_groups.candidates import RULE
from workbench.local_session import RUNS, open_local

# Typed by hand for this test. Twelve rows, a signal that rises with the outcome in nine of them.
OWN_CSV = ('date,ticker,sig,out_bp\n2026-10-01,A,-30,-40\n2026-10-01,B,-20,-10\n2026-10-01,C,-10,15\n2026-10-01,D,0,-5\n2026-10-01,E,10,20\n2026-10-01,F,20,35\n'
           '2026-10-02,A,-25,-30\n2026-10-02,B,-15,5\n2026-10-02,C,-5,-10\n2026-10-02,D,5,10\n2026-10-02,E,15,30\n2026-10-02,F,25,45\n')


class Script(unittest.TestCase):
    def test_exact_statistics_agree_with_an_independent_float_computation(self):
        rows = read_csv(ROOT / 'examples/signal_groups/data/signals.csv'); r = analyze(rows, 'mom_20', 'fwd_5d_bp', 3)
        ordered = sorted(rows, key=lambda x: (x['mom_20'], x['ticker'], x['date'])); n = len(ordered); size, extra = divmod(n, 3); start = 0
        for g in range(3):
            k = size + (1 if g < extra else 0); chunk = ordered[start:start + k]; start += k
            m = statistics.mean(x['fwd_5d_bp'] for x in chunk); h = sum(1 for x in chunk if x['fwd_5d_bp'] > 0) / k; e = r['groups'][g]
            self.assertAlmostEqual(m, e['mean_bp']['numerator'] / e['mean_bp']['denominator']); self.assertAlmostEqual(h, e['hit_rate']['numerator'] / e['hit_rate']['denominator'])
        self.assertEqual(r['rows_used'], 240)
    def test_hand_computed_case(self):
        t = analyze([{'s': 1, 'o': 10}, {'s': 2, 'o': -10}, {'s': 3, 'o': 30}, {'s': 4, 'o': 50}], 's', 'o', 2)
        self.assertEqual(t['groups'][0]['mean_bp'], {'numerator': 0, 'denominator': 2}); self.assertEqual(t['spread_top_minus_bottom_bp'], {'numerator': 160, 'denominator': 4})
        with self.assertRaises(ValueError): analyze([{'s': 1, 'o': 1}], 's', 'o', 2)


class CandidateRuleThroughTheClient(unittest.TestCase):
    def test_same_conclusion_different_history_different_set(self):
        live, excluded, reinstated = RULE.live_set('MET', []); self.assertEqual([c['id'] for c in live], ['other-horizon', 'finer-groups', 'placebo-signal'])
        history = [{'seq': 10, 'theme': 'TH-S0', 'rejections': [{'id': 'finer-groups', 'reason': 'later', 'reconsider_when': 'new_documents'}], 'documents_after': False}]
        live, excluded, reinstated = RULE.live_set('MET', history, 'TH-S1'); self.assertEqual([c['id'] for c in live], ['other-horizon', 'placebo-signal']); self.assertEqual(excluded[0]['id'], 'finer-groups')
        history[0]['documents_after'] = True; live, excluded, reinstated = RULE.live_set('MET', history, 'TH-S1')
        self.assertEqual([c['id'] for c in live], ['other-horizon', 'finer-groups', 'placebo-signal']); self.assertEqual(reinstated[0]['id'], 'finer-groups'); self.assertEqual(excluded, [])
        direction = [{'seq': 11, 'theme': 'TH-S0', 'rejections': [{'id': 'placebo-signal', 'reason': 'later', 'reconsider_when': 'new_direction'}], 'documents_after': False}]
        live, excluded, reinstated = RULE.live_set('MET', direction, 'TH-S1'); self.assertEqual(reinstated[0]['id'], 'placebo-signal')
        live, excluded, reinstated = RULE.live_set('MET', direction, 'TH-S0'); self.assertEqual(excluded[0]['id'], 'placebo-signal')
        never = [{'seq': 12, 'theme': 'TH-S1', 'rejections': [{'id': 'reject', 'reason': 'x', 'reconsider_when': 'never'}, {'id': 'coarser-groups', 'reason': 'x', 'reconsider_when': 'never'}], 'documents_after': True}]
        live, excluded, reinstated = RULE.live_set('NOT_MET', never, 'TH-S1'); self.assertIn('reject', [c['id'] for c in live]); self.assertEqual([x['id'] for x in excluded], ['coarser-groups'])
    def test_gather_history_reads_selection_records(self):
        sel = {'seq': 5, 'body': {'result': {'theme': 'TH-S0', 'rejections': [{'id': 'a', 'reason': 'r', 'reconsider_when': 'always'}]}}}
        h = RULE.gather_history([sel], [{'seq': 7}]); self.assertEqual(h, [{'seq': 5, 'theme': 'TH-S0', 'rejections': sel['body']['result']['rejections'], 'documents_after': True}])
    def test_client_analysis_module_uses_only_the_standard_library_and_the_package(self):
        tree = ast.parse((ROOT / 'client/arh_client/analysis.py').read_text()); names = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import): names.update(a.name.split('.')[0] for a in n.names)
            if isinstance(n, ast.ImportFrom) and n.level == 0: names.add((n.module or '').split('.')[0])
        self.assertTrue(names <= set(sys.stdlib_module_names) | {'__future__'}, names)


class Experience(unittest.TestCase):
    name = 'test-signal-' + os.urandom(3).hex()
    @classmethod
    def tearDownClass(cls): shutil.rmtree(RUNS / cls.name, ignore_errors=True)
    def test_the_whole_demonstration(self):
        from examples.signal_groups.demo import Demo
        report = Demo(self.name, quiet=True).run()
        self.assertEqual(report['status'], 'PASS', report['lines'][-12:])
        for name, ok in report['checks'].items():
            with self.subTest(name): self.assertTrue(ok, name)
        self.assertEqual(report['state']['N'], 7); self.assertEqual(report['state']['themes'], ['TH-S0', 'TH-S1', 'TH-S2'])
        self.assertLess(report['timings']['first_admitted_direction_s'], 120); self.assertEqual(report['line_groups']['script'], 55)


class OwnCsvThroughTheCommandLine(unittest.TestCase):
    name = 'test-own-' + os.urandom(3).hex()
    @classmethod
    def tearDownClass(cls): shutil.rmtree(RUNS / cls.name, ignore_errors=True)
    def test_own_table_recorded_historical_and_the_loop_completed(self):
        from examples.signal_groups.__main__ import main
        csv = RUNS / (self.name + '.csv'); csv.write_text(OWN_CSV); self.addCleanup(lambda: csv.unlink(missing_ok=True))
        direct = analyze(read_csv(csv), 'sig', 'out_bp', 3)
        # 1. a new run: own file in, expectation recorded first, the host runs the analysis, candidates shown
        r1 = main(['--name', self.name, '--csv', str(csv), '--signal', 'sig', '--outcome', 'out_bp', '--expect', '>= 30', '--minimum-n', '10', '--origin', 'typed into tests/integration/test_signal_groups.py', '--quiet'])
        self.assertEqual(r1['status'], 'OK', r1['lines']); self.assertEqual(r1['run_status'], 'recorded'); self.assertEqual(r1['metric'], direct['spread_top_minus_bottom_bp'])
        self.assertEqual(r1['documents'], [{'seq': r1['documents'][0]['seq'], 'class': 'historical', 'origin': 'typed into tests/integration/test_signal_groups.py'}])
        self.assertEqual(r1['conclusion'], 'MET'); self.assertEqual(r1['candidates'], ['other-horizon', 'finer-groups', 'placebo-signal']); self.assertEqual(r1['N'], 5)
        ro = open_local(RUNS / self.name)
        try:
            v = ro.view(); self.assertEqual(ro.mode, 'live'); self.assertEqual(v['charter']['class'], 'historical'); self.assertEqual(v['labels']['data'], 'historical documents the Principal imports')
            inv = v['investigations'][0]; self.assertLess(inv['design']['seq'], inv['result']['seq']); self.assertTrue(inv['result']['settled']); self.assertEqual(v['next'][0]['op'], 'select')
            exp = (ro.c.experiment()['sources']); self.assertEqual(next(iter(exp.values()))['document']['class'], 'historical')
        finally: ro.close()
        # 2. the selection, proposal and check; 3. the Principal's decision; 4. the run shown after reopening
        r2 = main(['--run', self.name, '--choose', 'placebo-signal', '--reason', 'a spread the placebo shows too would mean nothing', '--next', 'Does a placebo column show the same spread?', '--quiet'])
        self.assertEqual(r2['status'], 'OK', r2['lines']); self.assertEqual(r2['check'], 'PASS'); self.assertTrue(r2['transition'].startswith('TR-'))
        r3 = main(['--run', self.name, '--admit', r2['transition'], '--reason', 'placebo first', '--quiet'])
        self.assertEqual(r3['status'], 'OK', r3['lines']); self.assertTrue(r3['applied']); self.assertEqual(r3['N'], 6)
        r4 = main(['--run', self.name, '--quiet'])
        self.assertEqual(r4['status'], 'OK'); self.assertEqual(r4['N'], 6); self.assertTrue(any('direction TH-S1' in l for l in r4['lines']), r4['lines'])
        # a second design under the new direction cites the same historical document and records its revision
        r5 = main(['--run', self.name, '--signal', 'out_bp', '--outcome', 'sig', '--expect', '< 1', '--quiet'])
        self.assertEqual(r5['status'], 'OK', r5['lines']); self.assertIn(r5['conclusion'], ('MET', 'NOT_MET')); self.assertTrue(any('[TH-S1]' in l for l in r5['lines']))
        # the demonstration hook is not on this path
        self.assertFalse((RUNS / self.name / 'work').exists())
