"""The signal-groups example: the script verified on its own, then the whole experience through ARH with history-shaped candidates and an interrupted attempt resumed."""
from pathlib import Path
import os
import shutil
import statistics
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'client'))
from examples.signal_groups.signal_groups import analyze, read_csv
from examples.signal_groups.candidates import live_set, gather_history
from workbench.local_session import RUNS


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


class CandidateRule(unittest.TestCase):
    def test_same_conclusion_different_history_different_set(self):
        live, excluded, reinstated = live_set('MET', []); self.assertEqual([c['id'] for c in live], ['other-horizon', 'finer-groups', 'placebo-signal'])
        history = [{'seq': 10, 'theme': 'TH-S0', 'current_theme': 'TH-S1', 'rejections': [{'id': 'finer-groups', 'reason': 'later', 'reconsider_when': 'new_documents'}], 'documents_after': False}]
        live, excluded, reinstated = live_set('MET', history); self.assertEqual([c['id'] for c in live], ['other-horizon', 'placebo-signal']); self.assertEqual(excluded[0]['id'], 'finer-groups')
        history[0]['documents_after'] = True; live, excluded, reinstated = live_set('MET', history)
        self.assertEqual([c['id'] for c in live], ['other-horizon', 'finer-groups', 'placebo-signal']); self.assertEqual(reinstated[0]['id'], 'finer-groups'); self.assertEqual(excluded, [])
        direction = [{'seq': 11, 'theme': 'TH-S0', 'current_theme': 'TH-S1', 'rejections': [{'id': 'placebo-signal', 'reason': 'later', 'reconsider_when': 'new_direction'}], 'documents_after': False}]
        live, excluded, reinstated = live_set('MET', direction); self.assertEqual(reinstated[0]['id'], 'placebo-signal')
        never = [{'seq': 12, 'theme': 'TH-S1', 'current_theme': 'TH-S1', 'rejections': [{'id': 'reject', 'reason': 'x', 'reconsider_when': 'never'}], 'documents_after': True}]
        live, excluded, reinstated = live_set('NOT_MET', never); self.assertIn('reject', [c['id'] for c in live])


class Experience(unittest.TestCase):
    name = 'test-signal-' + os.urandom(3).hex()
    @classmethod
    def tearDownClass(cls): shutil.rmtree(RUNS / cls.name, ignore_errors=True)
    def test_the_whole_experience(self):
        from examples.signal_groups.__main__ import Demo
        report = Demo(self.name, quiet=True).run()
        self.assertEqual(report['status'], 'PASS', report['lines'][-12:])
        for name, ok in report['checks'].items():
            with self.subTest(name): self.assertTrue(ok, name)
        self.assertEqual(report['state']['N'], 7); self.assertEqual(report['state']['themes'], ['TH-S0', 'TH-S1', 'TH-S2'])
        self.assertLess(report['timings']['first_admitted_direction_s'], 120); self.assertEqual(report['line_counts']['signal_groups.py'], 55)
