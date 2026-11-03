"""Live reopen rests on the execution identity: files that take part in a run or its recovery, and the recorded environment."""
from pathlib import Path
import json
import os
import shutil
import tempfile
import unittest
from adaptive_research_harness.encoding import Refusal, decode
from adaptive_research_harness.profile import Profile
from build_support.freeze import freeze

ROOT = Path(__file__).resolve().parents[2]


class ReopenIdentity(unittest.TestCase):
    def setUp(self):
        self.run = ROOT / 'artifacts' / 'development' / 'run-bundles' / ('identity-' + os.urandom(4).hex()); freeze(self.run / 'bundle')
        self.profile = Profile(self.run / 'bundle')
        self.tmp = tempfile.TemporaryDirectory(prefix='arh-identity-'); self.root = Path(self.tmp.name)
        for item in self.profile.inventory['files']:
            if item.get('root') == 'bundle': continue
            q = self.root / item['path']; q.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / item['path'], q)
    def tearDown(self):
        self.tmp.cleanup(); shutil.rmtree(self.run, ignore_errors=True)
    def test_the_inventory_names_what_takes_part(self):
        inv = self.profile.inventory; execution = {e['path'] for e in inv['execution_files']}; everything = {e['path'] for e in inv['files']}
        self.assertLess(len(execution), len(everything))
        for p in ('adaptive_research_harness/rules.py', 'client/arh_client/research.py', 'workbench/local_session.py', 'acceptance/local.py', 'experiments/synthetic_flow/experiment.json', 'bundle/experiment.json'):
            self.assertIn(p, execution, p)
        for p in ('tests/component/fabricated.py', 'BUILD.md', 'build_support/freeze.py', 'workbench/index.html', 'isolation/install.py'):
            self.assertIn(p, everything, p); self.assertNotIn(p, execution, p)
        env = decode((self.run / 'bundle' / 'environment.json').read_bytes()); self.assertIn('python', env)
        self.assertNotIn('bundle/environment.json', everything)
    def test_unrelated_edits_keep_a_run_live_and_execution_edits_do_not(self):
        self.profile.verify_execution(self.root); self.profile.verify_files(self.root)
        unrelated = self.root / 'tests' / 'component' / 'fabricated.py'; unrelated.write_bytes(unrelated.read_bytes() + b'\n# a test edit\n')
        self.profile.verify_execution(self.root)
        with self.assertRaises(Refusal) as ctx: self.profile.verify_files(self.root)
        self.assertEqual(ctx.exception.code, 'ARTIFACT_CHANGED')
        core = self.root / 'adaptive_research_harness' / 'rules.py'; core.write_bytes(core.read_bytes() + b'\n# a core edit\n')
        with self.assertRaises(Refusal) as ctx: self.profile.verify_execution(self.root)
        self.assertEqual(ctx.exception.code, 'ARTIFACT_CHANGED'); self.assertIn('rules.py', ctx.exception.detail)
    def test_a_changed_environment_opens_read_only(self):
        env_path = self.run / 'bundle' / 'environment.json'; env = decode(env_path.read_bytes())
        env['python'] = '3.0.0'; env_path.write_bytes(json.dumps(env, sort_keys=True).encode())
        with self.assertRaises(Refusal) as ctx: Profile(self.run / 'bundle').verify_execution(self.root)
        self.assertEqual(ctx.exception.code, 'ENVIRONMENT_CHANGED')
        env = decode(env_path.read_bytes()); env['python'] = __import__('platform').python_version(); env['packages'] = {'no-such-package-arh': '1.0'}
        env_path.write_bytes(json.dumps(env, sort_keys=True).encode())
        with self.assertRaises(Refusal) as ctx: Profile(self.run / 'bundle').verify_execution(self.root)
        self.assertEqual(ctx.exception.code, 'ENVIRONMENT_CHANGED'); self.assertIn('no-such-package-arh', ctx.exception.detail)
    def test_an_older_bundle_without_the_identity_falls_back_to_the_full_inventory(self):
        inv_path = self.run / 'bundle' / 'inventory.json'; inv = decode(inv_path.read_bytes()); inv.pop('execution_files'); inv.pop('execution_identity')
        inv_path.write_bytes(json.dumps(inv, sort_keys=True, separators=(',', ':')).encode() + b'\n')
        p = Profile(self.run / 'bundle'); p.verify_execution(self.root)
        unrelated = self.root / 'tests' / 'component' / 'fabricated.py'; unrelated.write_bytes(unrelated.read_bytes() + b'\n# edit\n')
        with self.assertRaises(Refusal): p.verify_execution(self.root)
