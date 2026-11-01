"""A local-documents research run in the workbench: the Principal's own files, designs, analyses and next investigations.

Live: a LocalHost over the local_documents experiment, with the Principal,
Observation, researcher and Checker identities held in this process under
separate tokens. The researcher proposes; the evaluator verifies; the
Principal decides. Every action is one client operation the core admits or
refuses. Read-only: the retained ledgers without a core.
"""
from pathlib import Path
import json
import sys
import time
import uuid
from adaptive_research_harness.encoding import decode, require, Refusal
from adaptive_research_harness.clock import durable_write
from adaptive_research_harness.profile import Profile
from adaptive_research_harness.local_host import LocalHost
from . import records
from .session import RUNS, manifest, inventory_matches, now_ms

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'client'))
SETUP = ROOT / 'experiments' / 'local_documents'
SOURCE = 'SRC-LOCAL-DOC'; RESEARCHER = 'AD-L1.0'; CHECKER = 'AD-CK-L1.0'
LABELS = {'researcher': 'the Principal through AD-L1.0, a fixed program', 'data': 'historical documents the Principal imports', 'store': 'disposable SQLite',
          'isolation': 'OS isolation unverified', 'charges': 'simulated research units; nothing billed', 'standing': 'historical reconstruction; no forward standing'}
EPOCH_MS = 1793232000000   # 2026-10-29T00:00:00.000Z


def period_end_tick(date):
    import datetime
    d = datetime.datetime.strptime(date, '%Y-%m-%d'); epoch = datetime.datetime(2026, 10, 29)
    return int((d - epoch).total_seconds() * 1000) + 86400000 + 1000


def derive(es, ts):
    """Documents, investigations and the permitted next actions, from ledger records alone."""
    ei = {e['seq']: e for e in es}
    docs = [e for e in es if e['kind'] == 'OBSERVATION' and e['body'].get('form') == 'DOCUMENT' and e['body'].get('source') == SOURCE]
    def doc_view(e):
        d = e['body']['document']; f = d.get('file', {}); p = d.get('provenance', {})
        return {'seq': e['seq'], 'sha256': e['sha256'], 'item_id': d.get('item_id'), 'name': f.get('name'), 'media_type': f.get('media_type'), 'bytes': f.get('bytes'),
                'file_sha256': f.get('sha256'), 'origin': p.get('origin'), 'received_at': p.get('received_at'), 'note': p.get('note'), 'class': d.get('class'),
                'content': 'rows' if 'rows' in d else 'text', 'rows': len(d['rows']) if 'rows' in d else None, 'period': d.get('period_start', '')[:10]}
    charter = doc_view(docs[0]) if docs else None
    rr = [e for e in es if e['kind'] == 'RESEARCH_RECORD' and e['actor'] == RESEARCHER]
    designs = [e for e in rr if e['body'].get('kind') == 'EXPERIMENT DESIGN']
    analyses = [e for e in rr if e['body'].get('kind') == 'plain']
    selections = [e for e in rr if e['body'].get('kind') == 'SELECTION']
    proposals = [e for e in ts if e['kind'] == 'PROPOSED' and e['actor'] == RESEARCHER and e['body'].get('class') == 'THEME']
    settled = {e['body']['attempt'] for e in es if e['kind'] == 'SETTLEMENT'}
    investigations = []; next_actions = []
    for d in designs:
      b = d['body']; base = {'design': {'seq': d['seq'], 'sha256': d['sha256']}, 'question': b['question'], 'expectation': b.get('expectation'), 'analysis': b.get('analysis'),
                             'documents': [r['sequence'] for r in b['closure']['refs']], 'revises': (b.get('revises') or {}).get('sequence'), 'theme': b.get('parameters', {}).get('theme'),
                             'recorded_at': (b.get('result') or {}).get('recorded_at')}
      # Every analysis record citing the design is shown, in order: a re-run, a revision of the conclusion or a forgery all stay visible.
      cited = [a for a in analyses if (a['body'].get('design') or {}).get('sequence') == d['seq']]
      for an in (cited or [None]):
        item = dict(base)
        if an:
            ab = an['body']; item['result'] = {'seq': an['seq'], 'sha256': an['sha256'], 'metric': (ab.get('result') or {}).get('metric'), 'n': (ab.get('result') or {}).get('n'),
                                                'summary': (ab.get('result') or {}).get('summary'), 'per_document': (ab.get('result') or {}).get('per_document'), 'failure': ab.get('failure'),
                                                'conclusion': ab.get('conclusion'), 'settled': ab.get('attempt') in settled}
            sel = next((s for s in selections if (s['body'].get('result') or {}).get('analysis', {}).get('seq') == an['seq']), None)
            if sel:
                sb = sel['body']['result']; item['selection'] = {'seq': sel['seq'], 'sha256': sel['sha256'], 'chosen': sb['chosen'], 'reason': sb['reason'], 'next_question': sb['next_question'], 'candidates': sb['candidates'], 'rejections': sb['rejections']}
                pr = next((p for p in proposals if ((p['body']['content'].get('selection_basis') or {}).get('origin') or {}).get('selection_record', {}).get('sequence') == sel['seq']), None)
                if pr:
                    tid = pr['transition_id']; checks = [e for e in ts if e['kind'] == 'CHECK' and e['transition_id'] == tid]
                    decision = next((e for e in ts if e['kind'] == 'DECISION' and e['transition_id'] == tid), None)
                    applied = next((e for e in ts if e['kind'] == 'APPLIED' and e['transition_id'] == tid), None)
                    item['proposal'] = {'transition_id': tid, 'seq': pr['seq'], 'theme': pr['body']['content']['ThemeId'], 'statement': pr['body']['content']['statement'],
                                        'checks': [{'seq': c['seq'], 'result': c['body']['result'], 'not_met': [k for k, v in c['body']['criteria'].items() if v['status'] != 'MET']} for c in checks],
                                        'decision': {'seq': decision['seq'], 'decision': decision['body']['decision'], 'reason': decision['body'].get('reason')} if decision else None,
                                        'applied': {'seq': applied['seq'], 'n': applied['body']['n']} if applied else None}
                    if not checks: next_actions.append({'op': 'check', 'transition': tid, 'design': d['seq'], 'label': 'Run the independent check', 'actor': CHECKER})
                    elif checks[-1]['body']['result'] == 'PASS' and not decision: next_actions.append({'op': 'decide', 'transition': tid, 'design': d['seq'], 'check': checks[-1]['seq'], 'label': 'Decide: admit or reject this direction', 'actor': 'Principal'})
                    elif decision and decision['body']['decision'] == 'ADMITTED' and not applied: next_actions.append({'op': 'apply', 'transition': tid, 'design': d['seq'], 'decision': decision['seq'], 'label': 'Apply the admitted direction', 'actor': 'Principal'})
                else: next_actions.append({'op': 'propose', 'selection': sel['seq'], 'design': d['seq'], 'label': 'Propose the chosen investigation as the next direction', 'actor': RESEARCHER})
            elif item['result'].get('conclusion'):
                next_actions.append({'op': 'select', 'analysis': an['seq'], 'design': d['seq'], 'label': 'Choose the next step from the evidence', 'actor': RESEARCHER})
        else: next_actions.append({'op': 'run', 'design': d['seq'], 'label': 'Run the analysis the host calculator performs', 'actor': RESEARCHER})
        investigations.append(item)
    pending = [e['seq'] for e in es if e['kind'] == 'ATTEMPT' and e['seq'] not in settled]
    themes = [p['body']['content']['ThemeId'] for p in proposals]
    refusals = [{'seq': e['seq'], 'ledger': 'E' if 'form' not in e['body'] and e in es else 'T', 'actor': e['actor'], 'op': e['body'].get('op'), 'reason': e['body'].get('reason'), 'detail': e['body'].get('detail')} for e in es + ts if e['kind'] == 'REFUSAL']
    return {'charter': charter, 'documents': [doc_view(e) for e in docs[1:]], 'investigations': investigations, 'next': next_actions, 'pending_attempts': pending,
            'proposed_themes': themes, 'refusals': refusals, 'counts': {'E': len(es), 'T': len(ts)}}


class LocalRun:
    kind = 'local'
    def __init__(self, run_dir):
        self.run_dir = Path(run_dir); self.bundle = self.run_dir / 'bundle'; self.state = self.run_dir / 'state'; self.host = None; self.mode = 'live'; self.closed = False
        import threading; self.lock = threading.RLock()
    # ----- construction -----
    @classmethod
    def create(cls, charter_text, name=None, charter_name='charter.md'):
        from build_support.freeze import freeze
        name = name or time.strftime('%Y%m%d-%H%M%S') + '-local-' + uuid.uuid4().hex[:6]
        run_dir = RUNS / name; require(not run_dir.exists(), 'RUN_EXISTS', name); (run_dir / 'state').mkdir(parents=True)
        inventory = freeze(run_dir / 'bundle', SETUP)
        durable_write(run_dir / 'workbench.json', {'run': name, 'kind': 'local', 'created_ms': now_ms(), 'inventory_sha256': inventory, 'bundle': str((run_dir / 'bundle').relative_to(ROOT)), 'status': 'starting', 'labels': LABELS, 'charter_name': charter_name})
        s = cls(run_dir)
        try:
            s.start()
            from arh_client import historical_document, startup
            charter = historical_document(charter_text.encode(), charter_name, 'the Principal', note='run charter')
            startup(s.principal, s.observer, s.passing_check, tick=s.host.tick, formation_content=charter, formation_date='2026-10-28')
            s.note(status='live', started_ms=now_ms())
        except BaseException:
            s.close(status='failed'); raise
        return s
    @classmethod
    def resume(cls, run_dir):
        ok, reason = inventory_matches(Path(run_dir) / 'bundle'); require(ok, 'INVENTORY_MISMATCH', reason or '')
        s = cls(run_dir)
        try: s.start(); s.note(status='live', resumed_ms=now_ms())
        except BaseException: s.close(status='closed'); raise
        return s
    def start(self):
        from arh_client import connect, Principal, Observer, Checker
        from experiments.local_documents.researcher import LocalResearcher
        from experiments.local_documents.evaluator import validate_motivation
        self.host = LocalHost(self.bundle, self.state); self.host.start(); conn = self.host.connection_path
        self.principal = Principal(connect(conn, 'Principal')); self.observer = Observer(connect(conn, 'Observation function'))
        self.checker = Checker(connect(conn, CHECKER), validate_motivation=validate_motivation); self.researcher = LocalResearcher(connect(conn, RESEARCHER))
        self.c = self.principal.c
    def passing_check(self, tr):
        r = self.checker.check(tr); require(r.result == 'PASS', 'STARTUP_CHECK_FAILED', json.dumps(r.criteria)); return r.check_sequence
    def note(self, **fields):
        m = manifest(self.run_dir); m.update(fields); durable_write(self.run_dir / 'workbench.json', m)
    def close(self, status='closed'):
        with self.lock:
            if self.closed: return
            self.closed = True
            if self.host: self.host.close()
            try: self.note(status=status, closed_ms=now_ms())
            except OSError: pass
    # ----- reading -----
    def records(self): return self.c.history('E'), self.c.history('T')
    def record(self, ledger, seq): return self.c.record(ledger, seq)
    def view(self):
        es, ts = self.records(); d = derive(es, ts); st = self.c.state()
        budgets = {}
        for g in st['active']:
            try: budgets[g] = self.c.budget(g)
            except Exception as exc: budgets[g] = {'error': str(exc)}
        return {'run': self.run_dir.name, 'kind': 'local', 'mode': 'live', 'status': 'live', 'inventory_sha256': self.host.profile.inventory_hash, 'labels': LABELS,
                'state': {'N': st['N'], 'themes': sorted(st['themes']), 'active': st['active']}, 'clock': self.c.clock(), 'budgets': budgets, **d}
    def reader(self): return {'status': 'NOT_AVAILABLE', 'reason': 'The independent reader covers the synthetic experiment only. The evaluator under AD-CK-L1.0 recomputes each analysis a Theme cites.'}
    # ----- acting: each call is one client operation under one identity -----
    def tick_to(self, date):
        current = self.c.clock()['t'] - EPOCH_MS; target = period_end_tick(date)
        if target > current: self.host.tick(target)
    def import_document(self, name, raw, origin, note=None, date=None):
        from arh_client import historical_document
        date = date or time.strftime('%Y-%m-%d', time.gmtime()); self.tick_to(date)
        return self.observer.observe(SOURCE, historical_document(raw, name, origin, note=note), date)
    def design(self, question, expectation, analysis, documents, revises=None, theme=None):
        refs = [{'ledger': 'E', 'sequence': int(s), 'sha256': self.c.record('E', int(s))['sha256']} for s in documents]
        rev = {'ledger': 'E', 'sequence': int(revises), 'sha256': self.c.record('E', int(revises))['sha256']} if revises else None
        return self.researcher.design(question, expectation, analysis, refs, revises=rev, theme=theme)
    def run(self, design_seq): return self.researcher.run({'ledger': 'E', 'sequence': int(design_seq), 'sha256': self.c.record('E', int(design_seq))['sha256']})
    def candidates(self, analysis_seq): return self.researcher.candidates({'ledger': 'E', 'sequence': int(analysis_seq), 'sha256': self.c.record('E', int(analysis_seq))['sha256']})
    def select(self, analysis_seq, chosen, reason, next_question):
        return self.researcher.select({'ledger': 'E', 'sequence': int(analysis_seq), 'sha256': self.c.record('E', int(analysis_seq))['sha256']}, chosen, reason, next_question)
    def propose(self, selection_seq):
        es, ts = self.records(); n = 1 + sum(1 for e in ts if e['kind'] == 'PROPOSED' and e['actor'] == RESEARCHER)
        return self.researcher.propose({'ledger': 'E', 'sequence': int(selection_seq), 'sha256': self.c.record('E', int(selection_seq))['sha256']}, f'TH-L{n}')
    def check(self, transition_id): return self.checker.check(transition_id)
    def decide(self, transition_id, decision, reason):
        require(decision in ('ADMITTED', 'REJECTED'), 'INVALID_DECISION')
        es, ts = self.records(); checks = [e for e in ts if e['kind'] == 'CHECK' and e['transition_id'] == transition_id]; require(bool(checks), 'NO_CHECK')
        r = self.principal.decide(transition_id, checks[-1]['seq'], decision, reason)
        if r.ok and decision == 'REJECTED': self.release_funding(transition_id)
        return r
    def apply(self, transition_id):
        es, ts = self.records(); d = next((e for e in ts if e['kind'] == 'DECISION' and e['transition_id'] == transition_id and e['body']['decision'] == 'ADMITTED'), None); require(d is not None, 'NOT_DECIDED')
        r = self.principal.apply(transition_id, d['seq'])
        if r.ok: self.release_funding(transition_id)
        return r
    def release_funding(self, transition_id):
        es, ts = self.records(); p = next(e for e in ts if e['kind'] == 'PROPOSED' and e['transition_id'] == transition_id)
        try: self.researcher.r.close(p['body']['funding_ref'], None)
        except Exception: pass


class LocalReadOnly:
    kind = 'local'
    def __init__(self, run_dir, reason):
        self.run_dir = Path(run_dir); self.m = manifest(run_dir); self.reason = reason; self.mode = 'read-only'
        self.es, self.ts, self.claims = records.load_readonly(self.run_dir / 'state' / 'harness.sqlite')
    def view(self):
        d = derive(self.es, self.ts)
        return {'run': self.run_dir.name, 'kind': 'local', 'mode': 'read-only', 'read_only_reason': self.reason, 'status': 'complete', 'inventory_sha256': self.m.get('inventory_sha256'), 'labels': LABELS,
                'state': {'N': max((e['body']['n'] for e in self.ts if e['kind'] == 'APPLIED'), default=None), 'themes': sorted({p['body']['content']['ThemeId'] for p in self.ts if p['kind'] == 'PROPOSED' and p['body'].get('class') == 'THEME'})}, 'clock': None, 'budgets': {}, **d, 'next': []}
    def records(self): return self.es, self.ts
    def record(self, ledger, seq):
        rows = self.es if ledger == 'E' else self.ts; e = next((x for x in rows if x['seq'] == seq), None); require(e is not None, 'NO_RECORD'); return e
    def reader(self): return {'status': 'NOT_AVAILABLE', 'reason': 'read-only run'}
    def close(self, status=None): pass


def open_local(run_dir):
    ok, reason = inventory_matches(Path(run_dir) / 'bundle')
    return LocalRun.resume(run_dir) if ok else LocalReadOnly(run_dir, reason)
