"""Focused build-audit regressions; disposable genesis is explicitly authorized."""
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from adaptive_research_harness.encoding import digest,Refusal,decode
from adaptive_research_harness.storage import Store
from adaptive_research_harness.engine import Engine
from adaptive_research_harness.clock import SyntheticClock
from adaptive_research_harness import host
from .fabricated import profile


class AuditRegressions(unittest.TestCase):
    def test_f6_rejected_genesis_preserved_without_poisoning_empty_ledgers(self):
        p=profile()
        with tempfile.TemporaryDirectory(prefix='arh-disposable-') as d:
            store=Store(Path(d)/'test.sqlite');clock=SyntheticClock(Path(d)/'clock.json',p.setup['clock']);clock.initialize()
            e=Engine(store,p,clock,{'inventory_sha256':p.inventory_hash,'allow_apply_zero':True})
            good={'constitution_sha256':p.setup['constitution']['sha256'],'design':p.designs['AD-CK-1.0'],'grant':p.grants['AU-CK-A']}
            import uuid
            key=str(uuid.uuid4());bad=dict(good,constitution_sha256='wrong')
            result=e.command('Principal',key,'genesis',bad)
            self.assertEqual(result['status'],'REFUSED');self.assertEqual(e.query('Principal','inspect-request',{'request_id':key}),result)
            self.assertEqual(store.events('E'),[]);self.assertEqual(store.events('T'),[])
            self.assertEqual(e.command('Principal',str(uuid.uuid4()),'genesis',good)['status'],'COMMITTED')
            self.assertEqual(e.query('Principal','state',{})['N'],0);store.close()
    def test_f16_unreadable_worker_is_not_proven_dead(self):
        with patch.object(host,'generation',side_effect=Refusal('GENERATION_UNAVAILABLE')):
            with self.assertRaises(Refusal) as caught:host.still_alive({'pid':os.getpid()})
            self.assertEqual(caught.exception.code,'WORKER_NOT_QUIESCENT')
    def test_f7_reader_rejects_apply_without_its_pass_check(self):
        from acceptance.reader import read
        source=Path('artifacts/development/latest/E01.json')
        if not source.exists():self.skipTest('requires a retained actual E01 history')
        report=json.loads(source.read_bytes());db=sqlite3.connect('file:'+report['state_directory']+'/harness.sqlite?mode=ro',uri=True);db.row_factory=sqlite3.Row
        records={}
        for ledger,table in [('E','evidence'),('T','transitions')]:
            records[ledger]=[]
            for row in db.execute('SELECT * FROM '+table+' ORDER BY seq'):
                row=dict(row);row['body']=decode(row['body']);row['command']=decode(row['command']) if row['command'] else None;records[ledger].append(row)
        db.close()
        class ReaderClient:
            def query(self,op,p):
                if op=='history':
                    rows=records[p['ledger']];upper=p.get('through',len(rows));page=[e for e in rows if p['after']<e['seq']<=upper][:p['limit']]
                    return {'records':page,'through':upper,'next_after':page[-1]['seq'] if page else p['after']}
                if op=='budget':return {'committed':{'AU-CK-A':'4.25','AU-RP-1':'2.00'}[p['grant']]}
        self.assertEqual(read(ReaderClient())['N'],17)
        last=next(e for e in reversed(records['T']) if e['kind']=='APPLIED');last['body']['check']=999999;last['sha256']=digest(last['body'])
        with self.assertRaises(AssertionError):read(ReaderClient())
