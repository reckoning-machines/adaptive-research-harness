"""Integration through real processes: the headline example's demonstrations, the generic startup on the synthetic bundle, and the package boundary.

The LangGraph parts need an interpreter with the client and its langgraph
extra installed; .venv/bin/python is used when present and the tests skip
otherwise. The generic startup test needs only the standard library and the
client source.
"""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
VENV = ROOT / '.venv' / 'bin' / 'python'
sys.path.insert(0, str(ROOT / 'client'))


def langgraph_python():
    candidate = os.environ.get('ARH_LANGGRAPH_PYTHON') or (str(VENV) if VENV.exists() else None)
    if not candidate: return None
    probe = subprocess.run([candidate, '-c', 'import arh_client, langgraph, langgraph.checkpoint.sqlite'], capture_output=True)
    return candidate if probe.returncode == 0 else None


class HeadlineExample(unittest.TestCase):
    def test_every_demonstration_holds(self):
        python = langgraph_python()
        if not python: self.skipTest('no interpreter with arh_client[langgraph]; create .venv as the client README says')
        run_dir = ROOT / 'artifacts' / 'development' / 'langgraph' / ('test-' + os.urandom(4).hex())
        proc = subprocess.run([python, '-m', 'examples.langgraph_headlines', '--run', str(run_dir), '--quiet'], cwd=ROOT, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), capture_output=True, text=True, timeout=900)
        report = json.loads((run_dir / 'report.json').read_text())
        self.assertEqual(report.get('status'), 'PASS', report.get('error') or proc.stderr[-2000:])
        self.assertEqual(proc.returncode, 0)
        expected = ['startup through checked controls', 'classification recorded and settled', 'returns document committed one period later',
                    'overstated count fails the independent Check and is not admitted', 'researcher cannot approve its own proposal or change its rules',
                    'honest proposal passes Check, P-1 admits, Apply registers', 'over-budget work refused before the provider runs',
                    'killed after the durable receipt: resumed, no second provider call', 'replaying the successful claim request grants no permission',
                    'killed after the provider completed, before the receipt: recovered by lookup under the original claim',
                    'killed with no record anywhere: reconciled at the maximum, liability kept, no second call',
                    'replacement refused until the caller is gone and the provider operation is cancelled', 'replacement attempt executed once and settled']
        for name in expected:
            with self.subTest(name): self.assertTrue(report['demonstrations'].get(name), name)
        self.assertEqual(report['N'], 6); self.assertEqual(report['research']['joined']['k_bullish_up'], 9); self.assertEqual(report['budgets']['AU-RH-1'], '2.40')
        self.assertEqual(report['refusals']['decide'], 'UNAUTHORIZED'); self.assertEqual(report['refusals']['propose LIMITS'], 'UNAUTHORIZED')
        shutil.rmtree(run_dir, ignore_errors=True)

    def test_example_runs_from_outside_the_checkout(self):
        """The package boundary: a copy of the example in a temporary directory, importing only arh_client, against a host started in the checkout."""
        python = langgraph_python()
        if not python: self.skipTest('no interpreter with arh_client[langgraph]')
        with tempfile.TemporaryDirectory(prefix='arh-external-') as d:
            shutil.copytree(ROOT / 'examples' / 'langgraph_headlines', Path(d) / 'langgraph_headlines', ignore=shutil.ignore_patterns('__pycache__'))
            run_dir = Path(d) / 'run'
            proc = subprocess.run([python, '-m', 'langgraph_headlines', '--harness', str(ROOT), '--run', str(run_dir), '--quiet'], cwd=d, env={k: v for k, v in os.environ.items() if k != 'PYTHONPATH'} | {'PYTHONDONTWRITEBYTECODE': '1'}, capture_output=True, text=True, timeout=900)
            self.assertEqual(proc.returncode, 0, proc.stderr[-3000:])
            report = json.loads((run_dir / 'report.json').read_text()); self.assertEqual(report['status'], 'PASS')


class GenericStartup(unittest.TestCase):
    def test_generic_startup_reproduces_the_synthetic_sixteen(self):
        """arh_client.startup against the synthetic bundle yields the same sixteen transitions as acceptance.runtime.startup_records."""
        from adaptive_research_harness.local_host import LocalHost
        from build_support.freeze import freeze
        from arh_client import connect, Principal, Observer, Checker, startup
        from adaptive_research_harness.checkers import a as checker_a
        run = ROOT / 'artifacts' / 'development' / 'run-bundles' / ('startup-' + os.urandom(4).hex()); bundle = run / 'bundle'; freeze(bundle)
        host = LocalHost(bundle, run / 'state'); host.start()
        try:
            principal = Principal(connect(host.connection_path, 'Principal')); observer = Observer(connect(host.connection_path, 'Observation function'))
            checker = Checker(connect(host.connection_path, 'AD-CK-1.0'), evaluate_fn=checker_a.evaluate)
            def check(tr):
                r = checker.check(tr); self.assertEqual(r.result, 'PASS', r.criteria); return r.check_sequence
            s = startup(principal, observer, check, tick=host.tick)
            self.assertEqual(s['N'], 16); self.assertEqual([x['transition_id'] for x in s['transitions']], [f'TR-{i}' for i in range(1, 17)])
            self.assertEqual([x['subject'] for x in s['transitions']], ['AU-OBS-1', 'initial_limits'] + [f'AD-R{i}.0' for i in range(1, 11)] + ['AD-CK-2.0', 'AU-CK-B', 'AU-RP-1', 'TH-G1'])
            c = principal.c; self.assertEqual(c.budget('AU-CK-A')['committed'], '4.00')
            kinds = [e['kind'] for e in c.history('E')]; self.assertEqual(kinds.count('OBSERVATION'), 3); self.assertEqual(kinds.count('RESERVATION'), 16)
        finally:
            host.close(); shutil.rmtree(run, ignore_errors=True)
