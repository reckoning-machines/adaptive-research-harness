"""The research lifecycle a researcher process drives: reserve, attempt, claim, execute, finish, settle, record, propose.

Every command takes a key the caller persisted first, so a repeated call
returns the original receipt. Permission to execute is only ever the one
fresh PERMISSION_CONSUMED reply to a claim; it is never stored or replayed.
"""
from __future__ import annotations
from pathlib import Path
import json
import os
from .protocol import digest, units, amount, HarnessError, require, canonical, decode, time_text
from .results import Outcome, Ref


def event_ref(e, ledger='E'):
    return {'ledger': ledger, 'sequence': e['seq'], 'sha256': e['sha256'], 'raw_sha256': digest(e['body'].get('document', e['body']))}


def invocation(profile, tool, step, refs, parameters):
    return {'schema_version': 1, 'tool_id': tool, 'tool_spec_hash': profile['artifacts']['tools'][tool]['content_sha256'],
            'executable_hash': profile['inventory']['tool_executables'][tool], 'step': step, 'parameters': parameters, 'input_refs': refs}


def expected_maximum(step_spec, row_count):
    """The tariff maximum the core will require, in hundredths."""
    t = step_spec['tariff']; require(0 <= row_count <= t['limit'], 'INVALID_ESTIMATE')
    if 'bands' in t: return units(next(b['maximum'] for b in t['bands'] if row_count <= b['up_to']))
    return row_count * units(t['per_unit'])


class ReceiptStore:
    """The caller's own durable receipts, one file per attempt, written with fsync before the core is told."""
    def __init__(self, directory): self.directory = Path(directory); self.directory.mkdir(parents=True, exist_ok=True)
    def path(self, attempt): return self.directory / f'attempt-{attempt}.json'
    def save(self, attempt, receipt):
        p = self.path(attempt); tmp = p.with_suffix('.new')
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, 'wb') as f: f.write(canonical(receipt)); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, p)
        d = os.open(self.directory, os.O_RDONLY)
        try: os.fsync(d)
        finally: os.close(d)
    def load(self, attempt):
        p = self.path(attempt); return decode(p.read_bytes()) if p.exists() else None


def _ref(r): return r.as_dict() if isinstance(r, Ref) else r


class Researcher:
    """The research lifecycle for one researcher identity. Every command returns an Outcome."""
    def __init__(self, connection): self.c = connection
    @property
    def actor(self): return self.c.actor
    def profile(self): return self.c.profile()
    def design(self):
        return next(d['content'] for d in self.profile()['artifacts']['designs'] if d['content']['AgentDesignVersionId'] == self.actor)
    def grant(self):
        """The active Research grant naming this actor."""
        s = self.c.state()
        for ident in s['active']:
            g = s['grants'][ident]
            if g['class'] == 'Research' and self.actor in g['grantee']: return g
        raise HarnessError('AUTHORIZATION_INACTIVE', 'no active Research grant names ' + self.actor)
    def step(self, name):
        spec = next((s for s in self.c.experiment()['steps'] if s['name'] == name), None); require(spec is not None, 'INVALID_STEP', name); return spec

    # ----- inputs -----
    def documents(self, source=None, item_id=None):
        """Committed DOCUMENT observations, earliest first, optionally for one source or item."""
        out = []
        for e in self.c.closure()['evidence']:
            if e['kind'] != 'OBSERVATION' or e['body']['form'] != 'DOCUMENT': continue
            if source and e['body']['source'] != source: continue
            if item_id and e['body']['item_id'] != item_id: continue
            out.append(e)
        return out
    def formation(self, source, item_id=None):
        docs = self.documents(source, item_id); require(bool(docs), 'FORMATION_MISSING', source); return docs[0]

    # ----- funding and attempts -----
    def reserve(self, amount: str, purpose: dict, key: str, expiry_ms: int | None = None, expected_sequence: int | None = None) -> Outcome:
        """Reserve budget under the active Research grant. Refusals: BUDGET_EXCEEDED, CAP_EXCEEDED, FENCED, PURPOSE_OUT_OF_SCOPE, AUTHORIZATION_EXPIRED."""
        p = {'grant': self.grant()['AuthorizationId'], 'amount': amount, 'purpose': purpose}
        if expiry_ms is not None: p['expiry_ms'] = expiry_ms
        if expected_sequence is not None: p['expected_sequence'] = expected_sequence
        return self.c.call('reserve', p, key)
    def attempt(self, reservation: int, step: str, tool: str, input_refs: list, parameters: dict, maximum: str, key: str, dispatch_index: int = 0, tier: int = 1) -> Outcome:
        """Record an attempt before any work. Refusals: ALLOWANCE_EXCEEDED, GRANT_EXHAUSTED, INVALID_ESTIMATE, TOOL_NOT_PERMITTED, INVALID_STEP, RESERVATION_EXPIRED."""
        refs = [_ref(r) for r in input_refs]; data = invocation(self.profile(), tool, step, refs, parameters)
        r = self.c.call('attempt', {'reservation': reservation, 'step': step, 'input': data, 'dispatch_index': dispatch_index, 'maximum': maximum, 'tier': tier}, key)
        r.input_hash = digest(data); r.raw['input'] = data; return r
    def attempt_record(self, seq: int) -> dict:
        e = self.c.record('E', seq); require(e['kind'] == 'ATTEMPT' and e['actor'] == self.actor, 'UNAUTHORIZED'); return e
    def retry(self, previous_attempt: int, key: str) -> Outcome:
        """A new attempt for the same work with the next dispatch index. Refusals: PENDING_PREDECESSOR, WORKER_NOT_QUIESCENT, DUPLICATE_ATTEMPT."""
        a = self.attempt_record(previous_attempt); b = a['body']
        same = [x for x in self.c.history('E') if x['kind'] == 'ATTEMPT' and x['body']['reservation'] == b['reservation']
                and x['body']['step'] == b['step'] and x['body']['input_hash'] == b['input_hash']]
        payload = {k: b[k] for k in ('reservation', 'step', 'input', 'maximum', 'tier')}; payload['dispatch_index'] = max(x['body']['dispatch_index'] for x in same) + 1
        r = self.c.call('attempt', payload, key); r.input_hash = b['input_hash']; r.raw['input'] = b['input']; return r
    def close(self, reservation: int, key: str) -> Outcome:
        """Release a reservation's unused allowance. Liabilities stay. Refusals: RESERVATION_BOUND, ALREADY_CLOSED."""
        return self.c.call('close', {'reservation': reservation}, key)

    # ----- records and proposals -----
    def research_commit(self, record: dict, key: str) -> Outcome:
        """Commit a research record built with record_body(). Refusals: UNAUTHORIZED, INVALID_CLOSURE, INCOMPLETE_RESEARCH_RECORD."""
        return self.c.call('research-commit', record, key)
    def record_body(self, attempt_seq: int | None, question: str, result: dict | None, failure: str | None, input_refs: list, kind: str = 'plain',
                    parameters: dict | None = None, claims: list | None = None, snapshot: dict | None = None, source_cutoff: str | None = None,
                    record_class: str | None = None, revises=None, tool: dict | None = None, extra: dict | None = None) -> dict:
        """A research record body in the shape the core admits, citing its exact inputs.

        attempt_seq is None for an EXPERIMENT DESIGN or SELECTION, which meters no work; then tool names the planned tool.
        record_class is 'synthetic' or 'historical'; when omitted it follows the cited documents. revises names an earlier
        record of yours that this one supersedes; both stay on the ledger. extra adds declared fields such as expectation,
        analysis, design or conclusion.
        """
        input_refs = [_ref(r) for r in input_refs]; closure = self.c.closure()
        cited = [self.c.get(r) for r in input_refs]; first = cited[0]['body'] if cited else {}
        classes = {e['body'].get('class', 'synthetic') for e in cited if e['kind'] in ('OBSERVATION', 'RESEARCH_RECORD')}
        cls = record_class or ('historical' if 'historical' in classes else 'synthetic')
        if attempt_seq is None:
            require(tool is not None, 'TOOL_REQUIRED', 'a record without an attempt names the planned tool')
            grant = self.grant()['AuthorizationId']; invocation_hash = None; params = parameters or {}
        else:
            a = self.attempt_record(attempt_seq); inp = a['body']['input']; grant = a['body']['grant']; invocation_hash = a['body']['input_hash']
            tool = tool or {'id': inp['tool_id'], 'spec_sha256': inp['tool_spec_hash'], 'executable_hash': inp['executable_hash']}
            params = parameters if parameters is not None else inp['parameters']
        default_claims = [{'kind': 'REPORTED', 'document': input_refs[0], 'location': '/rows' if first.get('document', {}).get('rows') is not None else '/', 'text': 'Cited committed input'},
                          {'kind': 'INTERPRETATION', 'reported': [0], 'text': 'Calculated result; historical reconstruction with no forward standing'}] if input_refs else []
        body = {'grant': grant, 'attempt': attempt_seq, 'question': question, 'result': result if result is not None else {'failure': failure},
                'failure': failure, 'closure': {'E': closure['E'], 'N': closure['N'], 'refs': list(input_refs)}, 'claims': claims or default_claims,
                'kind': kind, 'snapshot': snapshot or ({'identity': first.get('item_id', str(input_refs[0]['sequence'])), 'sha256': input_refs[0]['raw_sha256']} if input_refs else {'identity': question, 'sha256': digest(result or {})}),
                'source_cutoff': source_cutoff or first.get('document', {}).get('period_end') or time_text(closure['time_ms']),
                'parameters': params, 'tool': tool,
                'reproducibility': {'input_refs': list(input_refs), 'invocation_hash': invocation_hash, 'result_hash': digest(result) if result is not None else None, 'classification': 'Historical Reconstruction'},
                'synthetic': cls == 'synthetic', 'class': cls}
        if revises is not None: body['revises'] = _ref(revises)
        body.update(extra or {}); return body
    def propose(self, cls: str, subject: str, content: dict, budget: str, funding_ref: int, key: str, transition_id: str | None = None, predecessor: str | None = None) -> Outcome:
        """Propose a Transition under the Research grant; funding_ref is the Evidence sequence fund() will take next. Refusals: STALE_BASE, UNAUTHORIZED, SCOPE_VIOLATION, DUPLICATE_TRANSITION."""
        tr = transition_id or 'TR-' + key
        p = {'transition_id': tr, 'base': self.c.state()['N'], 'class': cls, 'subject': subject, 'content': content,
             'budget': budget, 'grant': self.grant()['AuthorizationId'], 'funding_ref': funding_ref, 'delta': {'O': 0, 'S': 0, 'A': 0}}
        if predecessor: p['predecessor_transition'] = predecessor
        r = self.c.call('propose', p, key); r.transition_id = tr; return r
    def next_evidence_sequence(self) -> int: return (self.c.clock()['E'] or 0) + 1
    def fund(self, transition_id: str, budget: str, expected_sequence: int, key: str) -> Outcome:
        """Reserve the proposal's budget at the exact sequence it named. Refusals: WRONG_RESERVATION, FUNDING_REFERENCE_TAKEN, BUDGET_EXCEEDED."""
        return self.reserve(budget, {'kind': 'Transition', 'id': transition_id}, key, expected_sequence=expected_sequence)
    def propose_theme(self, content: dict, budget: str, propose_key: str, fund_key: str, predecessor: str | None = None) -> Outcome:
        """Propose a THEME, the next investigation, and fund it. Admission needs a check and a Principal decision; P-1 does not cover Themes."""
        future = self.next_evidence_sequence()
        r = self.propose('THEME', content['ThemeId'], content, budget, future, propose_key, predecessor=predecessor)
        if r.ok:
            f = self.fund(r.transition_id, budget, future, fund_key); r.raw['funding'] = f.raw; r.raw['funding_ref'] = future; r.raw['funded'] = f.ok
        return r
    def propose_hypothesis(self, content: dict, budget: str, propose_key: str, fund_key: str) -> Outcome:
        """Propose a HYPOTHESIS and fund it. The returned Outcome is the proposal's; raw['funding'] holds the funding Outcome."""
        future = self.next_evidence_sequence()
        r = self.propose('HYPOTHESIS', content['HypothesisId'], content, budget, future, propose_key)
        if r.ok:
            f = self.fund(r.transition_id, budget, future, fund_key); r.raw['funding'] = f.raw; r.raw['funding_ref'] = future; r.raw['funded'] = f.ok
        return r


class Execution:
    """One admitted attempt that this caller executes itself."""
    def __init__(self, researcher, attempt_seq, input_hash, tool_id, maximum_text):
        self.r = researcher; self.attempt = attempt_seq; self.input_hash = input_hash; self.tool = tool_id; self.maximum = maximum_text
    @classmethod
    def from_record(cls, researcher, attempt_seq):
        a = researcher.attempt_record(attempt_seq); b = a['body']
        return cls(researcher, attempt_seq, b['input_hash'], b['input']['tool_id'], b['maximum'])
    def claim(self):
        """Ask for permission. PERMISSION_CONSUMED is given once; every other reply is not permission."""
        return self.r.c.query('tool-run', {'attempt': self.attempt})
    def receipt(self, result, actual_text, error=None):
        return {'attempt': self.attempt, 'input_hash': self.input_hash, 'tool_id': self.tool, 'actual': actual_text, 'synthetic': True, 'result': result, 'error': error}
    def finish(self, receipt): return self.r.c.query('tool-finish', {'attempt': self.attempt, 'receipt': receipt})
    def registered(self): return self.r.c.query('tool-receipt', {'attempt': self.attempt}).get('receipt')
    def settle(self, receipt: dict, key: str) -> Outcome:
        """Settle at the receipt's actual charge. Refusals: ALREADY_SETTLED, INVALID_SETTLEMENT."""
        return self.r.c.call('settle', {'attempt': self.attempt, 'actual': receipt['actual'], 'unit': 'simulated_research_units',
                                        'provenance': {'kind': 'TOOL_RECEIPT', 'receipt': receipt}}, key)
    def settle_unknown(self, key: str) -> Outcome:
        """Settle at the admitted maximum when the outcome is unknown. Accounting only: it cancels nothing at the provider."""
        return self.r.c.call('settle', {'attempt': self.attempt, 'actual': self.maximum, 'unit': 'simulated_research_units', 'provenance': {'kind': 'UNKNOWN'}}, key)

    def run(self, call=None, store=None, lookup=None, hook=lambda point: None):
        """Claim, execute, register. Idempotent against the core and the caller's durable store.

        call(claim) runs the provider for a fresh permission and returns (result, actual_text).
        lookup(attempt, input_hash) asks the provider for its own record of the
        original operation; a hit recovers that operation under its original
        identity. With no receipt anywhere the outcome is 'uncertain': the work
        may have run or may still be running, and nothing here calls it again.
        """
        reply = self.claim(); status = reply.get('status')
        if status == 'PERMISSION_CONSUMED':
            require(call is not None and store is not None, 'CLAIM_UNSUPPORTED', 'a caller-executed tool needs call and store')
            result, actual = call(reply['claim'])
            receipt = self.receipt(result, actual); store.save(self.attempt, receipt); hook('after_receipt')
            self.finish(receipt); return {'status': 'executed', 'receipt': receipt}
        if status == 'RECEIPT': return {'status': 'registered', 'receipt': reply['receipt']}
        if status in ('IN_PROGRESS_OR_UNCERTAIN', 'UNKNOWN'):
            held = self.registered()   # a host-run tool may hold the receipt the reply lost
            if held is not None: return {'status': 'recovered', 'receipt': held}
            local = store.load(self.attempt) if store is not None else None
            if local is not None: self.finish(local); return {'status': 'resumed', 'receipt': local}
            found = lookup(self.attempt, self.input_hash) if lookup else None
            if found is not None:
                receipt = self.receipt(found['result'], found['actual'], found.get('error')); store.save(self.attempt, receipt); self.finish(receipt)
                return {'status': 'recovered', 'receipt': receipt}
            return {'status': 'uncertain'}
        raise HarnessError('CLAIM_UNSUPPORTED', str(reply))
