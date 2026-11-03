"""Additional build-only probes. No governed initialization, no role provisioning."""
from copy import deepcopy
from pathlib import Path
import ast
import json
import os
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from adaptive_research_harness.encoding import digest,canonical,Refusal
from adaptive_research_harness.storage import Store
from adaptive_research_harness.rules import Rules
from adaptive_research_harness.profile import Profile
from adaptive_research_harness.clock import SyntheticClock,durable_write
from .fabricated import Input,profile,ROOT


class BoundaryComponents(unittest.TestCase):
    def test_real_process_death_only_operational_receipts_empty_governed_ledgers(self):
        # This tests SQLite's carrier, not any R/B/C process-death witness.
        for committed in (False,True):
            with self.subTest(committed=committed),tempfile.TemporaryDirectory() as d:
                path=Path(d)/'empty.sqlite'
                code='''import os,signal,sys
from adaptive_research_harness.storage import Store
s=Store(sys.argv[1])
with s.transaction():
 s.remember('BUILD-PROBE','receipt','fixed',{'status':'COMPONENT_ONLY','refs':[]})
 if sys.argv[2]=='before':os.kill(os.getpid(),signal.SIGKILL)
os.kill(os.getpid(),signal.SIGKILL)
'''
                child=subprocess.run([sys.executable,'-c',code,str(path),'after' if committed else 'before'],cwd=ROOT,capture_output=True)
                self.assertEqual(child.returncode,-signal.SIGKILL,child.stderr)
                s=Store(path);self.assertEqual(s.lookup('BUILD-PROBE','receipt') is not None,committed)
                self.assertEqual(s.events('E'),[]);self.assertEqual(s.events('T'),[]);s.close()
    def test_receipt_reconstruction_from_fabricated_commit_envelopes(self):
        x=Input();e=x.reservation();e['command']={'actor':'AD-R1.0','request_id':'probe','request_hash':'fixed','position':0}
        with tempfile.TemporaryDirectory() as d:
            s=Store(Path(d)/'empty.sqlite')
            with patch.object(s,'events',side_effect=lambda ledger:[e] if ledger=='E' else []):
                result=s.lookup('AD-R1.0','probe','fixed');self.assertEqual(result['refs'][0]['sequence'],e['seq'])
                with self.assertRaises(Refusal):s.lookup('AD-R1.0','probe','changed')
            self.assertEqual(s.events('E'),[]);self.assertEqual(s.events('T'),[]);s.close()
    def test_clock_file_rollback_fails_against_durable_receipts(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'clock.json';config=profile().setup['clock'];c=SyntheticClock(p,config);c.initialize();c.advance(999)
            durable_write(p,{'epoch':config['epoch'],'tick':0})
            with self.assertRaises(Refusal) as caught:SyntheticClock(p,config).read()
            self.assertEqual(caught.exception.code,'CLOCK_ROLLBACK')
    def test_supported_source_extraction_and_listing(self):
        x=Input();rules=Rules(x.profile);g=x.profile.grants['AU-OBS-1'];src=next(s for s in g['source_declarations'] if s['content']['SourceId']=='SRC-SYN')
        doc=x.profile.artifacts['formation_cohort']['content'];period={'start':doc['period_start'],'end':doc['period_end']}
        p={'grant':'AU-OBS-1','source':'SRC-SYN','revision':src['SourceRevision'],'form':'COMPLETE','period':period,'item_id':doc['item_id'],'document':None,'slot':x.now,'window':period,'items':[doc['item_id']]}
        self.assertEqual(rules.execute(x.view(),'Observation function','observation-commit',p,x.now)[0]['kind'],'OBSERVATION')
        p['items']=[]
        with self.assertRaises(Refusal):rules.execute(x.view(),'Observation function','observation-commit',p,x.now)
        p.update(form='DOCUMENT',document=doc);p.pop('items');p.pop('window');e=x.add('E','OBSERVATION',p,'Observation function')
        p.update(form='VALUE',document=None,document_ref={'ledger':'E','sequence':e['seq'],'sha256':e['sha256']},value={'numerator':2,'denominator':2})
        self.assertEqual(rules.execute(x.view(),'Observation function','observation-commit',p,x.now)[0]['body']['value'],{'numerator':2,'denominator':2})
        p['value']['numerator']=1
        with self.assertRaises(Refusal):rules.execute(x.view(),'Observation function','observation-commit',p,x.now)
    def test_narrower_grant_denies_removed_right(self):
        x=Input();v=x.view();v.grants['AU-RP-1']['may_commit_evidence'].remove('RESERVATION')
        with self.assertRaises(Refusal):Rules(x.profile).execute(v,'AD-R1.0','reserve',{'grant':'AU-RP-1','amount':'1.00','purpose':{'kind':'Theme','id':'TH-G1'}},x.now)
    def test_inventory_detects_modified_artifact(self):
        p=profile()
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'sample';path.write_bytes(b'original');p.inventory={'files':[{'path':'sample','sha256':digest('unrelated')}]}
            with self.assertRaises(Refusal):p.verify_files(d)
    def test_runtime_catalog_has_executable_schedules(self):
        from acceptance.catalog import CASES,DEATH_POINTS
        from acceptance import cases
        self.assertEqual(len(CASES),51)
        self.assertTrue(all(callable(getattr(cases,c,None)) for c in CASES))
        self.assertEqual(len(DEATH_POINTS),20)
        for name in ('runtime.py','cases.py','death.py','reader.py'):
            tree=ast.parse((ROOT/'acceptance'/name).read_text())
            imports=[n.module or '' for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
            self.assertFalse(any('tests' in n or n.endswith(('storage','model','rules','engine')) for n in imports))
    def test_templates_have_process_isolation_controls(self):
        paths=list((ROOT/'isolation/generated').glob('*.service'));self.assertEqual(len(paths),18)
        for path in paths:
            if path.name=='harness-supervisor.service':continue
            raw=path.read_text()
            for directive in ('KillMode=control-group','PrivateNetwork=yes','ProtectSystem=strict','NoNewPrivileges=yes','RestrictAddressFamilies=AF_UNIX','Restart=no'):
                self.assertIn(directive,raw)
