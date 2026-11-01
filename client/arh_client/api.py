"""The everyday interface: research concepts in, results with their evidence out.

    research = arh_client.api.connect(project='examples/memo_returns', run='/tmp/arh-run')
    result = research.analysis(join, inputs=[...], expectation={...}, budget='memo-tests', operation='join-1')()

A scientist supplies an analysis function, its inputs, an expectation and
an evaluator, and names each piece of work. They get back the result, its
evidence reference, its conclusion, its check status and any refusal with
what to do about it. Reservations, attempts, permission, receipts,
settlement and recovery happen underneath, journaled per operation so a
process that dies resumes the same operation from its recorded progress.
An attempt whose outcome was lost is settled at its maximum and replaced
only on an explicit request the host admits after quiescence. The same
operation identity resumes; a new identity is new work. Nothing here
approves anything: a decision is the Principal's, under the Principal's
identity, and a check is the evaluator's, under its own.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import re
from .protocol import require, HarnessError
from .results import Ref, Outcome
from .research import ReceiptStore
from .analysis import AnalysisResearcher, OWN, evaluator as make_evaluator
from .operations import OperationStore, resolve_stage
from .project import Project
from .refusals import explain


@dataclass
class Refusal:
    """A governed refusal, with what it means and what to do next."""
    code: str
    detail: str
    meaning: str
    next_action: str
    stage: str | None = None
    @classmethod
    def of(cls, outcome, stage=None):
        meaning, action = explain(outcome.reason or outcome.status); return cls(outcome.reason or outcome.status, outcome.detail or '', meaning, action, stage)
    def as_dict(self): return {'code': self.code, 'detail': self.detail, 'meaning': self.meaning, 'next_action': self.next_action, 'stage': self.stage}
    def __str__(self): return f'{self.code}: {self.meaning} {self.next_action}'


@dataclass
class Result:
    """What one analysis produced. status is recorded, refused, uncertain or failed."""
    status: str
    operation: str | None = None
    design: Ref | None = None
    evidence: Ref | None = None
    attempt: int | None = None
    execution: str | None = None
    conclusion: dict | None = None
    outputs: dict | None = None
    refusal: Refusal | None = None
    links: dict = field(default_factory=dict)
    @property
    def ok(self): return self.status == 'recorded'
    @property
    def metric(self): return (self.conclusion or {}).get('metric')
    @property
    def n(self): return (self.conclusion or {}).get('n')
    @property
    def state(self): return (self.conclusion or {}).get('state')
    def as_state(self):
        return {'kind': 'analysis', 'status': self.status, 'operation': self.operation, 'design': self.design.as_dict() if self.design else None, 'evidence': self.evidence.as_dict() if self.evidence else None,
                'attempt': self.attempt, 'execution': self.execution, 'conclusion': self.conclusion, 'outputs': self.outputs, 'refusal': self.refusal.as_dict() if self.refusal else None, 'links': self.links}
    @classmethod
    def from_state(cls, d):
        r = d.get('refusal'); return cls(d['status'], d.get('operation'), Ref.from_dict(d['design']) if d.get('design') else None, Ref.from_dict(d['evidence']) if d.get('evidence') else None,
                                        d.get('attempt'), d.get('execution'), d.get('conclusion'), d.get('outputs'), Refusal(r['code'], r['detail'], r['meaning'], r['next_action'], r.get('stage')) if r else None, d.get('links', {}))


@dataclass
class Proposal:
    """A selection recorded and proposed as the next direction. status is waiting_for_review or refused."""
    status: str
    operation: str | None = None
    selection: Ref | None = None
    transition: str | None = None
    theme: str | None = None
    refusal: Refusal | None = None
    links: dict = field(default_factory=dict)
    def as_state(self):
        return {'kind': 'proposal', 'status': self.status, 'operation': self.operation, 'selection': self.selection.as_dict() if self.selection else None, 'transition': self.transition, 'theme': self.theme,
                'refusal': self.refusal.as_dict() if self.refusal else None, 'links': self.links}


@dataclass
class Review:
    """Where a proposal stands: waiting_for_review, check_failed, decided (with the decision) or applied. A decision is not an application."""
    status: str
    transition: str
    check: str | None = None
    decision: str | None = None
    applied: bool = False
    head: int | None = None
    def as_dict(self): return {'review': self.status, 'transition': self.transition, 'check': self.check, 'decision': self.decision, 'applied': self.applied, 'head': self.head}


class History:
    """What this researcher has concluded, chosen and rejected, from the ledger."""
    def __init__(self, researcher): self.r = researcher
    def conclusions(self, where=None, state=None): return self.r.conclusions(where, state)
    def selections(self): return self.r.selections()
    def rejections(self): return self.r.rejections()


def _theme_number(theme): m = re.search(r'(\d+)$', theme); return int(m.group(1)) if m else 0


class Research:
    """The researcher's side of a project: analyses, calls, selections and review status."""
    def __init__(self, project: Project, connection, run=None, operations=None, rule=None):
        self.project = project; self.c = connection; self.run = Path(run) if run else None
        self.r = AnalysisResearcher(connection, rule=rule); self.history = History(self.r)
        base = Path(operations) if operations else (self.run / 'researcher' if self.run else Path('arh-researcher'))
        self.ops = OperationStore(base / 'operations'); self.receipts = ReceiptStore(base / 'receipts')
        self.run_name = self.run.name if self.run else None
    @property
    def langgraph(self):
        from .langgraph_nodes import Nodes
        return Nodes(self)

    # ----- inputs -----
    def documents(self, source=None, charter=False):
        """Committed documents, as references with their names and row counts. The run's charter is left out unless asked for."""
        formation = self.c.profile()['artifacts'].get('formation_cohort', {}).get('source'); out = []; seen_charter = False
        for e in self.r.documents(source):
            if not charter and not seen_charter and e['body']['source'] == formation: seen_charter = True; continue
            d = e['body']['document']; out.append({'ref': Ref('E', e['seq'], e['sha256']), 'seq': e['seq'], 'name': d.get('file', {}).get('name'), 'rows': len(d['rows']) if 'rows' in d else None, 'source': e['body']['source'], 'class': e['body'].get('class')})
        return out
    def resolve_inputs(self, inputs):
        """Sequences, Refs, reference dicts, Results, document entries or a source id meaning every document of that source."""
        if not isinstance(inputs, (list, tuple)): inputs = [inputs]
        out = []
        for x in inputs:
            if isinstance(x, str): out += [d['ref'].as_dict() for d in self.documents(x)]
            elif isinstance(x, Result): require(x.evidence is not None, 'NO_EVIDENCE', f'{x.operation} has no record to cite'); out.append(x.evidence.as_dict())
            elif isinstance(x, dict) and 'ref' in x: out.append(x['ref'].as_dict())
            else: out += self.r.refs([x])
        return self.r.refs(out)
    def links(self, **refs):
        if not self.run_name: return {}
        return {k: f'/runs/{self.run_name}/record/{v.ledger}/{v.sequence}' for k, v in refs.items() if v is not None}

    # ----- the work -----
    def analysis(self, fn, inputs, expectation=None, budget=None, operation=None, question=None, spec=None, theme=None, revises=None, hook=None):
        """A callable that runs fn's declared analysis over the inputs as one metered attempt and returns a Result. operation is its identity."""
        require(operation, 'OPERATION_REQUIRED', 'give the analysis a stable identity; the same identity resumes, a new one is new work')
        def run(): return self.run_analysis(operation, fn, inputs, expectation, question, spec, budget, theme, revises, hook)
        run.operation = operation; return run
    def run_analysis(self, operation, fn, inputs, expectation=None, question=None, spec=None, budget=None, theme=None, revises=None, hook=None):
        entry_tool = self.project.analysis(fn); tool = entry_tool['id']; kind = entry_tool.get('kind', tool)
        refs = self.resolve_inputs(inputs); spec = dict(spec or {}); spec.setdefault('kind', kind)
        question = question or f'{kind} over {len(refs)} inputs'; hook = hook or (lambda point: None)
        work = {'tool': tool, 'spec': spec, 'inputs': [{'sequence': r['sequence'], 'sha256': r['sha256']} for r in refs], 'expectation': expectation}
        entry = self.ops.begin(operation, 'analysis', work=work)
        require(entry.get('work') == work, 'OPERATION_MISMATCH', f'{operation} was begun for different work; the same identity resumes, new work needs a new identity')
        journal = (entry, self.ops); purpose = self.project.budget(budget)['purpose']
        d = resolve_stage(self.c, entry, 'design', lambda key: self.r.design(question, expectation, spec, refs, revises, theme, tool, key), self.ops)
        if not d.ok:
            self.ops.update(operation, status='refused'); return Result('refused', operation, None, None, refusal=Refusal.of(d, 'design'))
        out = self.r.run(d.ref.as_dict(), entry['keys'], hook, journal, purpose); self.ops.update(operation, status=out['status'])
        return self._result(operation, out, d.ref)
    def _result(self, operation, out, design_ref):
        rec = out.get('record'); evidence = rec.ref if rec is not None and rec.ok else None
        refusal = None
        if out['status'] == 'refused': refusal = Refusal.of(out['reservation'] if out.get('refused_at') == 'reserve' else out['attempt'], out['refused_at'])
        elif out['status'] == 'failed': refusal = Refusal.of(rec, 'record')
        attempt = out['attempt'].sequence if out.get('attempt') is not None and out['attempt'].ok else None
        return Result(out['status'], operation, design_ref, evidence, attempt, out.get('execution'), out.get('conclusion'), (out.get('receipt') or {}).get('result'), refusal,
                      self.links(design=design_ref, evidence=evidence))

    def call(self, fn, inputs, operation, budget=None, question='', tool=None, hook=None):
        """One metered call of a tool this process executes: fn(inputs, spec, claim) -> (result, actual). Its own attempt, receipt and identity."""
        tool = tool or self.project.tool_id(fn); refs = self.resolve_inputs(inputs)
        work = {'tool': tool, 'inputs': [{'sequence': r['sequence'], 'sha256': r['sha256']} for r in refs]}
        entry = self.ops.begin(operation, 'call', work=work)
        require(entry.get('work') == work, 'OPERATION_MISMATCH', f'{operation} was begun for different work')
        out = self.r.perform(tool, refs, entry['keys'], question or f'{tool} call', None, None, self.project.budget(budget)['purpose'], call=fn, store=self.receipts, hook=hook or (lambda p: None), journal=(entry, self.ops))
        self.ops.update(operation, status=out['status']); return self._result(operation, out, None)

    def retry(self, operation, fn=None, hook=None):
        """Replace an uncertain attempt of an operation, explicitly, after the host has confirmed quiescence. The original liability stays.

        fn is the same caller-executed function the operation ran, for a call; a host-run analysis needs none.
        """
        entry = self.ops.get(operation); require(entry is not None and entry.get('status') == 'uncertain', 'NOT_UNCERTAIN', f'{operation} has no uncertain attempt to retry')
        previous = Outcome.from_reply(entry['stages']['attempt']).sequence; n = entry.get('retries', 0)
        while True:
            # A refused replacement is final under its key; the next request is new work under a new identity.
            sub = self.ops.begin(f'{operation}/retry/{n}', 'retry', previous=previous)
            if sub['stages'].get('attempt', {}).get('status') == 'REFUSED': n += 1; continue
            break
        if n != entry.get('retries', 0): self.ops.update(operation, retries=n)
        att = resolve_stage(self.c, sub, 'attempt', lambda key: self.r.r.retry(previous, key), self.ops)
        if not att.ok: return Result('refused', operation, refusal=Refusal.of(att, 'retry'))
        from .research import Execution
        from .analysis import Inputs
        a = self.c.record('E', att.sequence); b = a['body']; ex = Execution(self.r.r, att.sequence, b['input_hash'], b['input']['tool_id'], b['maximum'])
        cited = [self.c.get(r) for r in b['input']['input_refs']]; spec = next(((x['body'].get('analysis') or {}) for x in cited if x['kind'] == 'RESEARCH_RECORD' and x['body'].get('kind') == 'EXPERIMENT DESIGN'), None) or dict(b['input'].get('parameters') or {})
        caller = (lambda claim: fn(Inputs(cited), spec, claim)) if fn is not None else None
        run = ex.run(caller, self.receipts if fn is not None else None, None, hook or (lambda p: None))
        if run['status'] == 'uncertain':
            resolve_stage(self.c, sub, 'settle', lambda key: ex.settle_unknown(key), self.ops); return Result('uncertain', operation, attempt=att.sequence, execution='uncertain')
        receipt = run['receipt']; design = next((self.c.get(r) for r in b['input']['input_refs'] if self.c.get(r)['kind'] == 'RESEARCH_RECORD' and self.c.get(r)['body'].get('kind') == 'EXPERIMENT DESIGN'), None)
        from .analysis import conclude, event_ref
        question = design['body']['question'] if design else 'retry'; conclusion = conclude(receipt['result'], design['body'].get('expectation') if design else None, question) if not receipt.get('error') else None
        refs = [r for r in b['input']['input_refs']]; extra = {'conclusion': conclusion, **({'design': event_ref(design)} if design else {})}
        rec = resolve_stage(self.c, sub, 'record', lambda key: self.r.r.research_commit(self.r.r.record_body(att.sequence, question, receipt['result'] if not receipt.get('error') else None, receipt.get('error'), refs, kind='plain', extra=extra), key), self.ops)
        resolve_stage(self.c, sub, 'settle', lambda key: ex.settle(receipt, key), self.ops); resolve_stage(self.c, sub, 'close', lambda key: self.r.r.close(b['reservation'], key), self.ops)
        self.ops.update(operation, status='recorded' if rec.ok else 'failed')
        return Result('recorded' if rec.ok else 'failed', operation, Ref.from_dict(event_ref(design)) if design else None, rec.ref if rec.ok else None, att.sequence, run['status'], conclusion, receipt['result'], None if rec.ok else Refusal.of(rec, 'record'))

    # ----- what next -----
    def candidates(self, result, theme=None): return self.r.candidates(self._evidence(result), theme)
    def _evidence(self, result):
        if isinstance(result, Result): require(result.evidence is not None, 'NO_EVIDENCE', 'the result has no record'); return result.evidence.as_dict()
        return self.r.refs([result])[0]
    def select(self, result, chosen, reason, question, operation, budget=None, theme=None):
        """Record the choice of the next investigation, with rejections, propose it as a Theme and fund it. chosen is a candidate id or 'own'."""
        ref = self._evidence(result); entry = self.ops.begin(operation, 'selection', analysis=ref)
        require(entry.get('analysis') == ref, 'OPERATION_MISMATCH', f'{operation} was begun for a different result')
        sel = resolve_stage(self.c, entry, 'select', lambda key: self.r.select(ref, chosen, reason, question, theme, key), self.ops)
        if not sel.ok: self.ops.update(operation, status='refused'); return Proposal('refused', operation, refusal=Refusal.of(sel, 'select'))
        mine = [e for e in self.c.history('T') if e['kind'] == 'PROPOSED' and e['actor'] == self.c.actor and e['body'].get('class') == 'THEME']
        theme_id = entry.get('theme') or f"TH-{self.project.data['short']}{max([_theme_number(e['body']['content']['ThemeId']) for e in mine] + [_theme_number(self.r.umbrella)]) + 1}"
        if not entry.get('theme'): self.ops.update(operation, theme=theme_id)
        b = self.project.budget(budget); pr = self.r.propose(sel.ref.as_dict(), theme_id, budget=b.get('proposal_budget', '1.00'), keys=entry['keys'], journal=(entry, self.ops))
        if not pr.ok: self.ops.update(operation, status='refused'); return Proposal('refused', operation, sel.ref, refusal=Refusal.of(pr, 'propose'))
        self.ops.update(operation, status='waiting_for_review', transition=pr.transition_id)
        return Proposal('waiting_for_review', operation, sel.ref, pr.transition_id, theme_id, None, self.links(selection=sel.ref))
    def review(self, transition_id):
        """Where a proposal stands on the Transition ledger. Reading it decides nothing."""
        ts = self.c.history('T'); checks = [e for e in ts if e['kind'] == 'CHECK' and e['transition_id'] == transition_id]
        decision = next((e for e in ts if e['kind'] == 'DECISION' and e['transition_id'] == transition_id), None)
        applied = next((e for e in ts if e['kind'] == 'APPLIED' and e['transition_id'] == transition_id), None)
        check = checks[-1]['body']['result'] if checks else None
        if applied: status = 'applied'
        elif decision: status = 'decided'
        elif check == 'FAIL': status = 'check_failed'
        else: status = 'waiting_for_review'
        return Review(status, transition_id, check, decision['body']['decision'] if decision else None, bool(applied), applied['body']['n'] if applied else None)


class Evaluator:
    """The evaluator's side: a Checker identity that checks proposals with the team's recompute function."""
    def __init__(self, project, connection, recompute, rule=None, kind=None):
        from .checking import Checker
        self.project = project; self.c = connection; self.checker = Checker(connection, evaluate_fn=make_evaluator(recompute, rule, kind))
    def check(self, transition_id): return self.checker.check(transition_id)
    def pending(self):
        """Proposals with no check yet."""
        ts = self.c.history('T'); checked = {e['transition_id'] for e in ts if e['kind'] == 'CHECK'}
        return [e['transition_id'] for e in ts if e['kind'] == 'PROPOSED' and e['transition_id'] not in checked]


class Owner:
    """The Principal's side: the clock, decide and apply. Nothing a researcher or a graph does reaches this."""
    EPOCH_MS = 1793232000000   # 2026-10-29T00:00:00.000Z, the generated setup's clock epoch
    def __init__(self, project, connection, run=None):
        from .principal import Principal
        self.project = project; self.c = connection; self.p = Principal(connection); self.run = run
    def advance_to(self, date):
        """Advance the synthetic clock past the end of the period that holds date (YYYY-MM-DD), so documents of that date can be committed."""
        from .host import HostControl
        import datetime
        require(self.run is not None, 'RUN_REQUIRED', 'the clock is advanced through the run\'s control socket')
        target = int((datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.datetime(2026, 10, 29)).total_seconds() * 1000) + 86400000 + 1000
        current = self.c.clock()['t'] - self.EPOCH_MS
        if target > current: HostControl.from_file(Project.connection_file(self.run)).tick(target)
        return self.c.clock()
    def decide(self, transition_id, decision='ADMITTED', reason='Principal decision'):
        ts = self.c.history('T'); checks = [e for e in ts if e['kind'] == 'CHECK' and e['transition_id'] == transition_id]; require(bool(checks), 'NO_CHECK', transition_id)
        return self.p.decide(transition_id, checks[-1]['seq'], decision, reason)
    def apply(self, transition_id):
        ts = self.c.history('T'); d = next((e for e in ts if e['kind'] == 'DECISION' and e['transition_id'] == transition_id and e['body']['decision'] == 'ADMITTED'), None)
        require(d is not None, 'NOT_DECIDED', transition_id); return self.p.apply(transition_id, d['seq'])
    def admit(self, transition_id, reason='Principal decision'):
        d = self.decide(transition_id, 'ADMITTED', reason); return d if not d.ok else self.apply(transition_id)


class Importer:
    """The Observation function's side: documents in, with their provenance."""
    def __init__(self, project, connection):
        from .principal import Observer
        self.project = project; self.c = connection; self.o = Observer(connection)
    def import_file(self, source, path, date, origin, note=None, name=None):
        from .principal import historical_document
        raw = Path(path).read_bytes(); doc = historical_document(raw, name or Path(path).name, origin, note=note)
        if self.c.experiment()['sources'][source]['document'].get('class', 'synthetic') == 'synthetic': doc.update({'class': 'synthetic', 'synthetic': True})
        return self.o.observe(source, doc, date)


def connect(project, role='researcher', run=None, operations=None, recompute=None, rule=None, kind=None):
    """Open a project under one role: Research for the researcher, Evaluator for the checker, Owner for the Principal, Importer for the observer."""
    project = project if isinstance(project, Project) else Project.load(project)
    require(run is not None, 'RUN_REQUIRED', 'name the run directory or its connection file')
    connection = project.connect(role, run)
    if role == 'researcher': return Research(project, connection, run, operations, rule)
    if role == 'checker': require(recompute is not None, 'RECOMPUTE_REQUIRED', 'an evaluator needs the recompute function'); return Evaluator(project, connection, recompute, rule, kind)
    if role == 'principal': return Owner(project, connection, run)
    return Importer(project, connection)
