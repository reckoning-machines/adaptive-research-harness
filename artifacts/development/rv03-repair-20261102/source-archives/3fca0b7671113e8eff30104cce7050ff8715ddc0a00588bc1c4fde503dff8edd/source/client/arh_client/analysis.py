"""Connect one analysis function to ARH.

A team supplies four things. The analysis function. The inputs, as
documents imported and a design naming what to compute over them. The
budget, in the setup. The evaluation function that says what a valid
result is. This module supplies the rest: the design record with its
expectation, the reservation, the attempt, the execution with its receipt,
the record with its conclusion, settlement and closure, resumable stages
when a journal is supplied, the candidate rule over the history, the
selection record with its rejections, the Theme proposal, the host-tool
wrapper and the record checks an evaluator makes before the team's own
recomputation. The researcher decides what to investigate, through a
candidate table or a question of its own. The evaluator decides what
counts as a valid result, through recompute. Standard library only.

A result is the analysis function's own dictionary, recorded whole.
'metric' and 'n' are optional; when present, a conclusion is computed
against the design's expectation, and the record says RECORDED otherwise.
"""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import os
import time
from .protocol import digest, amount, canonical, require, units
from .connection import Connection
from .results import Outcome, Ref
from .research import Researcher, Execution, event_ref, expected_maximum
from .checking import evaluate as toolkit_evaluate

COMPARATORS = ('>=', '>', '<=', '<', '==')
CONDITIONS = ('new_documents', 'new_direction', 'always', 'never')
STATES = ('MET', 'NOT_MET', 'INCONCLUSIVE', 'RECORDED')
KEY_NAMES = ('reserve', 'attempt', 'record', 'settle', 'close')
OWN = 'own'   # a selection naming the researcher's own next question rather than a candidate


class Inputs:
    """The admitted inputs of one attempt, as research code sees them: documents, earlier records and the design."""
    def __init__(self, records):
        self.all = list(records)
        self.documents = [x for x in self.all if x['kind'] == 'OBSERVATION']
        self.design = next((x for x in self.all if x['kind'] == 'RESEARCH_RECORD' and x['body'].get('kind') == 'EXPERIMENT DESIGN'), None)
        self.records = [x for x in self.all if x['kind'] == 'RESEARCH_RECORD' and x is not self.design]
    @property
    def rows(self): return [r for d in self.documents for r in d['body']['document'].get('rows', [])]
    @property
    def texts(self): return [(d['body']['document']['file']['name'], d['body']['document']['text']) for d in self.documents if 'text' in d['body']['document']]
    @property
    def results(self): return [r['body'].get('result') for r in self.records]
    @property
    def cited(self): return [{'seq': x['seq'], 'sha256': x['sha256']} for x in self.documents + self.records]
    @property
    def document_class(self): return 'historical' if any(x['body'].get('class') == 'historical' for x in self.documents + self.records) else 'synthetic'
    def document(self, name): return next(d for d in self.documents if d['body']['document'].get('file', {}).get('name') == name)


def compare(metric, expectation):
    """MET, NOT_MET or INCONCLUSIVE by exact cross-multiplication. Values are integers or {'numerator','denominator'}."""
    def ratio(x): return (x['numerator'], x['denominator']) if isinstance(x, dict) else (x, 1)
    a, b = ratio(metric); c, d = ratio(expectation['value'])
    if b == 0 or d == 0: return 'INCONCLUSIVE'
    lhs, rhs = a * d, c * b; op = expectation['comparator']
    return 'MET' if {'>=': lhs >= rhs, '>': lhs > rhs, '<=': lhs <= rhs, '<': lhs < rhs, '==': lhs == rhs}[op] else 'NOT_MET'


def conclude(result, expectation, question):
    """The conclusion a result supports. RECORDED without an expectation; INCONCLUSIVE without a metric and count or below minimum_n."""
    metric = result.get('metric') if isinstance(result, dict) else None; n = result.get('n') if isinstance(result, dict) else None
    if expectation is None: state = 'RECORDED'; rule = 'no expectation was recorded; the result stands as recorded'
    elif metric is None or type(n) is not int: state = 'INCONCLUSIVE'; rule = 'the result carries no metric or count to compare with the expectation'
    else:
        state = 'INCONCLUSIVE' if n < expectation.get('minimum_n', 1) else compare(metric, expectation)
        rule = 'exact comparison of the metric with the expectation by cross-multiplication; INCONCLUSIVE below minimum_n'
    text = f'{question} ' + (f"Expectation {expectation['statement']}: {state}." if expectation else 'Recorded without an expectation.')
    return {'state': state, 'metric': metric, 'n': n, 'expectation': expectation, 'rule': rule, 'text': text}


def check_expectation(expectation):
    require(expectation.get('comparator') in COMPARATORS and 'value' in expectation and isinstance(expectation.get('statement'), str), 'INVALID_EXPECTATION', str(expectation))


def measure_count(step, cited):
    """The count the step's tariff meters, over the cited inputs."""
    measure = step['tariff']['measure']; docs = [e for e in cited if e['kind'] == 'OBSERVATION']
    if measure == 'documents': return len(docs)
    if measure == 'rows': return sum(len(e['body']['document'].get('rows', [])) for e in docs)
    size = sum(e['body']['document'].get('file', {}).get('bytes', len(canonical(e['body']['document']))) for e in docs); return -(-size // 1024)


def persisted_keys(path, names=KEY_NAMES):
    """Keys for one piece of work, written to path before first use, so a re-run sends the same keys and resumes."""
    path = Path(path)
    if path.exists(): return json.loads(path.read_text())
    keys = {k: Connection.new_key() for k in names}; path.parent.mkdir(parents=True, exist_ok=True); tmp = path.with_suffix('.new')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as f: f.write(json.dumps(keys)); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path); return keys


class CandidateRule:
    """What to investigate next, by conclusion state, with each rejection's reconsideration condition.

    table: {'MET': [...], 'NOT_MET': [...], 'INCONCLUSIVE': [...], 'RECORDED': [...]}, each entry {'id', 'question', 'why', 'reconsider_when'}.
    reconsider_when is 'new_documents', 'new_direction', 'always' or 'never'. A candidate rejected under one
    selection stays out of later sets until its condition is met. An entry with always_available true is never
    held back; use it for the choice to record a conclusion as rejected and stop.
    """
    def __init__(self, table):
        for state, entries in table.items():
            require(state in STATES, 'INVALID_CANDIDATE', state)
            for e in entries: require(e.get('id') and e.get('question') and e.get('reconsider_when') in CONDITIONS, 'INVALID_CANDIDATE', str(e))
        self.table = deepcopy(table)

    def live_set(self, state, history, current_theme=None):
        """(candidates, excluded, reinstated) for a conclusion state, given earlier selections earliest first.

        history entries: {'seq', 'theme', 'rejections': [{'id', 'reason', 'reconsider_when'}], 'documents_after': bool}.
        """
        base = deepcopy(self.table.get(state, [])); excluded = []; reinstated = []
        for cand in list(base):
            if cand.get('always_available'): continue
            prior = [h for h in history if any(r['id'] == cand['id'] for r in h['rejections'])]
            if not prior: continue
            last = prior[-1]; rej = next(r for r in last['rejections'] if r['id'] == cand['id'])
            cond = rej.get('reconsider_when', cand['reconsider_when'])
            met = (cond == 'new_documents' and last['documents_after']) or (cond == 'new_direction' and last['theme'] != current_theme) or cond == 'always'
            if met: reinstated.append({'id': cand['id'], 'rejected_in': last['seq'], 'condition': cond}); continue
            excluded.append({'id': cand['id'], 'rejected_in': last['seq'], 'reason': rej['reason'], 'condition': cond}); base.remove(cand)
        return base, excluded, reinstated

    @staticmethod
    def gather_history(selections, documents):
        """Earlier SELECTION records as history entries, with whether documents arrived after each."""
        return [{'seq': s['seq'], 'theme': s['body']['result'].get('theme'), 'rejections': s['body']['result'].get('rejections', []),
                 'documents_after': any(d['seq'] > s['seq'] for d in documents)} for s in selections]


def _ref(e): return {'ledger': 'E', 'sequence': e['seq'], 'sha256': e['sha256']}


class AnalysisResearcher:
    """The research lifecycle for declared analyses under one researcher identity.

    The research steps, their tools and parameters, the sources and the umbrella Theme come from the frozen
    profile. rule, a CandidateRule, is optional: without one, a selection names the researcher's own next
    question. analysis_kind, when set, is the 'kind' every design's analysis must name. Every command takes
    keys the caller may persist first; with a journal, every stage is resumable.
    """
    rule: CandidateRule | None = None
    analysis_kind: str | None = None

    def __init__(self, connection, rule=None, analysis_kind=None):
        self.c = connection; self.r = Researcher(connection)
        self.rule = rule if rule is not None else self.rule; self.analysis_kind = analysis_kind or self.analysis_kind
        exp = connection.experiment(); self.steps = [s for s in exp['steps'] if s['kind'] == 'research']
        require(bool(self.steps), 'CAPABILITY_UNSUPPORTED', 'the experiment declares no research step')
        self.sources = list(exp['sources']); self.umbrella = connection.profile()['setup']['theme']['content']['ThemeId']

    # ----- what the profile declares -----
    @property
    def source(self): return self.sources[0]
    def tools(self): return [t for s in self.steps for t in s['tools']]
    def step_of(self, tool):
        step = next((s for s in self.steps if tool in s['tools']), None); require(step is not None, 'TOOL_NOT_DECLARED', tool); return step
    def default_tool(self):
        tools = self.tools(); require(len(tools) == 1, 'TOOL_REQUIRED', 'the experiment declares several tools; name one'); return tools[0]

    # ----- reading -----
    def documents(self, source=None): return self.r.documents(source)
    def records(self, kind=None):
        return [e for e in self.c.history('E') if e['kind'] == 'RESEARCH_RECORD' and e['actor'] == self.c.actor and (kind is None or e['body'].get('kind') == kind)]
    def refs(self, items):
        """Ledger references from sequences, Refs, reference dicts or records."""
        out = []
        for x in items:
            if isinstance(x, int): x = {'ledger': 'E', 'sequence': x, 'sha256': self.c.record('E', x)['sha256']}
            elif isinstance(x, Ref): x = x.as_dict()
            elif isinstance(x, dict) and 'seq' in x and 'body' in x: x = _ref(x)
            if 'raw_sha256' not in x: x = event_ref(self.c.get(x))
            out.append(x)
        return out

    # ----- the design -----
    def design(self, question, expectation, analysis, inputs, revises=None, theme=None, tool=None, key=None):
        """Record the question, the expectation and the analysis over the inputs, before any attempt. Returns the Outcome."""
        if expectation is not None: check_expectation(expectation)
        if self.analysis_kind: require(analysis.get('kind') == self.analysis_kind, 'UNSUPPORTED_ANALYSIS', str(analysis.get('kind')))
        tool = tool or self.default_tool(); self.step_of(tool); refs = self.refs(inputs); theme = theme or self.umbrella
        result = {'question': question, 'expectation': expectation, 'analysis': analysis, 'inputs': [{'seq': r['sequence'], 'sha256': r['sha256']} for r in refs],
                  'theme': theme, 'tool': tool, 'recorded_at': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())}
        claims = [{'kind': 'QUESTION', 'text': question}] + ([{'kind': 'ASSUMPTION', 'text': expectation['statement']}] if expectation else [])
        body = self.r.record_body(None, question, result, None, refs, kind='EXPERIMENT DESIGN', parameters={'theme': theme}, revises=revises, tool={'id': tool, 'planned': True},
                                  claims=claims, extra={'expectation': expectation, 'analysis': analysis})
        return self.r.research_commit(body, key or Connection.new_key())

    # ----- the work -----
    def _stager(self, keys, journal):
        if journal is None: return lambda name, send: send(keys[name])
        from .operations import resolve_stage
        entry, store = journal; return lambda name, send: resolve_stage(self.c, entry, name, send, store)

    def perform(self, tool, inputs, keys=None, question='', expectation=None, design=None, purpose=None, parameters=None,
                call=None, store=None, lookup=None, hook=lambda point: None, journal=None, replacements=1):
        """Reserve, attempt, execute, record, settle and close one unit of metered work on the inputs.

        design is the design record when the work is a designed analysis; the attempt then cites it and the
        record carries a conclusion against its expectation. call(inputs, spec, claim) executes a tool the
        caller runs, with store keeping its receipts; a tool the host runs needs neither. journal is
        (entry, OperationStore) from arh_client.operations; every stage then resumes rather than repeats.
        replacements is how many controlled replacements the reservation leaves room for.
        """
        keys = keys or {k: Connection.new_key() for k in KEY_NAMES}; stage = self._stager(keys, journal)
        step = self.step_of(tool); parameters = parameters if parameters is not None else (step.get('parameters') or {})
        cited = [self.c.get(r) for r in self.refs(inputs)]; refs = [event_ref(e) for e in cited]
        if design is not None: refs = refs + [event_ref(design)]
        maximum = amount(expected_maximum(step, measure_count(step, cited))); purpose = purpose or {'kind': 'Theme', 'id': self.umbrella}
        # The reservation holds room for the attempt and for `replacements` controlled replacements of it, should the
        # outcome be lost; what is not used is released at close, and an uncertain attempt leaves the rest reserved.
        held = amount(units(maximum) * (1 + replacements))
        out = {'keys': keys, 'inputs': len(cited), 'tool': tool, 'maximum': maximum, 'reserved': held}
        res = stage('reserve', lambda key: self.r.reserve(held, purpose, key)); out['reservation'] = res
        if not res.ok: out.update(status='refused', reason=res.reason, detail=res.detail, refused_at='reserve'); return out
        att = stage('attempt', lambda key: self.r.attempt(res.sequence, step['name'], tool, refs, parameters, maximum, key)); out['attempt'] = att
        if not att.ok: out.update(status='refused', reason=att.reason, detail=att.detail, refused_at='attempt'); return out
        if att.input_hash is None:
            a = self.c.record('E', att.sequence); att.input_hash = a['body']['input_hash']; att.raw['input'] = a['body']['input']
        hook('after_attempt')
        ex = Execution(self.r, att.sequence, att.input_hash, tool, maximum)
        spec = (design['body'].get('analysis') if design is not None else None) or dict(parameters)
        caller = (lambda claim: call(Inputs(cited + ([design] if design is not None else [])), spec, claim)) if call is not None else None
        run = ex.run(caller, store, lookup, hook); out['execution'] = run['status']
        hook('after_execution')
        if run['status'] == 'uncertain':
            out['settlement'] = stage('settle', lambda key: ex.settle_unknown(key)); out['status'] = 'uncertain'; return out
        receipt = run['receipt']; result = receipt['result']; error = receipt.get('error'); out['receipt'] = receipt
        conclusion = conclude(result, expectation, question) if not error else None; dref = event_ref(design) if design is not None else None
        claims = ([{'kind': 'REPORTED', 'document': dref, 'location': '/', 'text': 'Design and expectation recorded before the attempt'}] if dref else
                  [{'kind': 'REPORTED', 'document': refs[0], 'location': '/', 'text': 'Cited committed input'}]) + \
                 [{'kind': 'INTERPRETATION', 'reported': [0], 'text': conclusion['text'] if conclusion else 'Analysis failed; no conclusion'}]
        extra = {'conclusion': conclusion}
        if dref: extra['design'] = dref
        rec = stage('record', lambda key: self.r.research_commit(self.r.record_body(att.sequence, question, result if not error else None, error, refs, kind='plain', claims=claims, extra=extra), key))
        out['record'] = rec; hook('after_record')
        out['settlement'] = stage('settle', lambda key: ex.settle(receipt, key)); out['closed'] = stage('close', lambda key: self.r.close(res.sequence, key)).ok
        out['conclusion'] = conclusion; out['status'] = 'recorded' if rec.ok else 'failed'
        if not rec.ok: out['reason'] = rec.reason; out['detail'] = rec.detail
        return out

    def run(self, design_ref, keys=None, hook=lambda point: None, journal=None, purpose=None):
        """Fund and run one design: the tool it names over the inputs it cites. Keys persisted by the caller make a re-run resume rather than repeat."""
        design = self.c.get(design_ref); b = design['body']
        out = self.perform(b['tool']['id'], b['closure']['refs'], keys, b['question'], b.get('expectation'), design, purpose, hook=hook, journal=journal)
        out['design'] = event_ref(design); out['documents'] = out['inputs']; return out

    # ----- what next -----
    def candidates(self, analysis_ref, theme=None):
        """The live candidate set for a recorded conclusion, with what the history excluded or reinstated and why. Empty without a rule."""
        rec = self.c.get(analysis_ref); conclusion = rec['body'].get('conclusion'); theme = theme or self.umbrella
        empty = {'candidates': [], 'excluded': [], 'reinstated': [], 'history_used': [], 'theme': theme}
        if not conclusion or self.rule is None: return empty
        earlier = self.records('SELECTION'); history = self.rule.gather_history(earlier, self.documents())
        live, excluded, reinstated = self.rule.live_set(conclusion['state'], history, theme)
        return {'candidates': live, 'excluded': excluded, 'reinstated': reinstated, 'history_used': [_ref(e) for e in earlier], 'theme': theme}

    def select(self, analysis_ref, chosen, reason, next_question, theme=None, key=None):
        """Record the chosen candidate, or 'own' for a question of the researcher's own, with every other candidate rejected and its condition."""
        rec = self.c.get(analysis_ref); c = self.candidates(analysis_ref, theme); ids = {x['id'] for x in c['candidates']}
        require(chosen == OWN or chosen in ids, 'NOT_A_CANDIDATE', chosen)
        result = {'analysis': {'seq': rec['seq'], 'sha256': rec['sha256']}, 'candidates': c['candidates'], 'excluded': c['excluded'], 'reinstated': c['reinstated'], 'history_used': c['history_used'],
                  'theme': c['theme'], 'chosen': chosen, 'reason': reason, 'next_question': next_question, 'conclusion': (rec['body'].get('conclusion') or {}).get('state'),
                  'rule': 'CandidateRule.live_set over the conclusion and the history' if self.rule is not None else None,
                  'rejections': [{'id': x['id'], 'reason': 'Not selected: ' + reason, 'reconsider_when': x['reconsider_when']} for x in c['candidates'] if x['id'] != chosen]}
        body = self.r.record_body(None, 'Which investigation follows from this result?', result, None, [event_ref(rec)], kind='SELECTION',
                                  parameters={'rule': result['rule'] or 'the researcher\'s own question'}, tool={'id': rec['body']['tool']['id'], 'planned': False},
                                  claims=[{'kind': 'INTERPRETATION', 'reported': [0], 'text': f'Chose {chosen}: {reason}'}])
        return self.r.research_commit(body, key or Connection.new_key())

    def propose(self, selection_ref, theme_id, predecessor_theme=None, budget='1.00', keys=None, journal=None):
        """Propose the selected investigation as a Theme, funded from the Research grant. Admission needs a check and the Principal."""
        keys = keys or {'propose': Connection.new_key(), 'fund': Connection.new_key()}
        sel = self.c.get(selection_ref); a = sel['body']['result']['analysis']; analysis = self.c.get({'ledger': 'E', 'sequence': a['seq'], 'sha256': a['sha256']})
        cited = [self.c.get(r) for r in analysis['body']['closure']['refs']]
        refs = [{k: v for k, v in event_ref(e).items() if k != 'raw_sha256'} for e in cited + [analysis, sel]]
        s = sel['body']['result']; conclusion = analysis['body'].get('conclusion') or {}
        content = {'ThemeId': theme_id, 'predecessor': predecessor_theme, 'statement': s['next_question'], 'motivation_closure': {'N': self.c.state()['N'], 'refs': refs},
                   'typed_claims': [{'kind': 'REPORTED', 'text': f"Metric {conclusion.get('metric')} over n={conclusion.get('n')}; " + (f"expectation {conclusion['expectation']['statement']}" if conclusion.get('expectation') else 'no expectation recorded')},
                                    {'kind': 'INTERPRETATION', 'text': conclusion.get('text', 'Recorded result')}, {'kind': 'QUESTION', 'text': s['next_question']},
                                    {'kind': 'ASSUMPTION', 'text': 'Reconstruction on committed inputs; no forward standing.'}],
                   'selection_basis': {'uncertainty': s['next_question'], 'decision_it_could_change': 'Which design the Principal commits next.',
                                       'experiment': f"Candidate {s['chosen']} chosen from {len(s['candidates'])}; {len(s['excluded'])} excluded by earlier rejections.", 'value_estimate': 'UNESTIMATED',
                                       'value_basis': 'No investment-economic inference from reconstruction alone.', 'cost_estimate_units': budget, 'time_estimate_ms': 600000,
                                       'horizon': 'The next design.', 'stopping_rule': 'When the next conclusion is recorded.', 'origin': {'selection_record': refs[-1], 'reason': s['reason']}}}
        if journal is None: return self.r.propose_theme(content, budget, keys['propose'], keys['fund'])
        from .operations import resolve_stage
        entry, store = journal
        pr = resolve_stage(self.c, entry, 'propose', lambda key: self.r.propose('THEME', theme_id, content, budget, self.r.next_evidence_sequence(), key), store)
        if not pr.ok: return pr
        proposal = self.c.get(pr.ref); pr.transition_id = proposal['transition_id']; funding_ref = proposal['body']['funding_ref']
        f = resolve_stage(self.c, entry, 'fund', lambda key: self.r.fund(pr.transition_id, budget, funding_ref, key), store)
        pr.raw['funding'] = f.raw; pr.raw['funding_ref'] = funding_ref; pr.raw['funded'] = f.ok; return pr

    # ----- history, as research code asks for it -----
    def conclusions(self, where=None, state=None):
        """Recorded conclusions of this researcher, filtered by analysis fields ({'signal': 'mom_20'}) or by state."""
        designs = {d['seq']: d for d in self.records('EXPERIMENT DESIGN')}; out = []
        for a in self.records('plain'):
            d = (a['body'].get('design') or {}).get('sequence')
            if d not in designs: continue
            spec = designs[d]['body'].get('analysis') or {}; c = a['body'].get('conclusion') or {}
            if where and any(spec.get(k) != v for k, v in where.items()): continue
            if state and c.get('state') != state: continue
            out.append({'design': _ref(designs[d]), 'analysis': _ref(a), 'question': designs[d]['body']['question'], 'spec': spec, 'expectation': designs[d]['body'].get('expectation'),
                        'conclusion': c, 'result': a['body'].get('result'), 'failure': a['body'].get('failure'), 'theme': designs[d]['body'].get('parameters', {}).get('theme'), 'revises': designs[d]['body'].get('revises')})
        return out
    def selections(self):
        return [{'selection': _ref(s), 'analysis': s['body']['result']['analysis'], 'chosen': s['body']['result']['chosen'], 'reason': s['body']['result']['reason'],
                 'next_question': s['body']['result']['next_question'], 'theme': s['body']['result'].get('theme'), 'rejections': s['body']['result'].get('rejections', [])} for s in self.records('SELECTION')]
    def rejections(self):
        """Every rejected candidate with its condition and whether the condition is met now."""
        docs = self.documents(); out = []
        for s in self.records('SELECTION'):
            later = any(d['seq'] > s['seq'] for d in docs)
            for r in s['body']['result'].get('rejections', []):
                cond = r.get('reconsider_when', 'never')
                out.append({'id': r['id'], 'reason': r['reason'], 'condition': cond, 'rejected_in': s['seq'], 'theme': s['body']['result'].get('theme'), 'documents_after': later,
                            'reconsider_now': cond == 'always' or (cond == 'new_documents' and later)})
        return out


def host_tool(analysis, kind=None):
    """calculate(inputs) for a tool the host runs with interface 'inputs', from analysis(inputs, spec).

    analysis receives an Inputs object (documents, rows, texts, earlier records and the design) and the
    design's analysis, and returns a dict: the result, recorded whole. 'metric' and 'n' are optional and
    give the conclusion against the expectation. The wrapper adds the inputs cited, the design, the input
    hash and the document class. The returned callable carries .kind.
    """
    def calculate(inputs):
        designs = [x for x in inputs if x['kind'] == 'RESEARCH_RECORD' and x['body'].get('kind') == 'EXPERIMENT DESIGN']
        if len(designs) != 1: raise ValueError('INVALID_INPUT')
        design = designs[0]; spec = design['body'].get('analysis') or {}
        if kind is not None and spec.get('kind') != kind: raise ValueError('UNSUPPORTED_ANALYSIS')
        inp = Inputs(inputs)
        if not inp.documents and not inp.records: raise ValueError('INVALID_INPUT')
        result = analysis(inp, spec)
        if not isinstance(result, dict): raise ValueError('INVALID_RESULT')
        cls = inp.document_class
        return dict(result, analysis=spec, inputs=inp.cited, design={'seq': design['seq'], 'sha256': design['sha256']},
                    input_sha256=hashlib.sha256(canonical([x['body'] for x in inp.documents + inp.records])).hexdigest(), **{'class': cls}, synthetic=cls == 'synthetic')
    calculate.kind = kind; calculate.analysis = analysis; return calculate


def check_records(ctx, recompute, rule=None, kind=None):
    """The record checks for a Theme motivated by one design, its analysis and one selection of the proposer.

    The design preceded the attempt, the attempt settled, the record cites exactly the committed inputs,
    the result hash holds, recompute(inputs, spec, result) accepts the result, the conclusion follows the
    expectation, and the selection's candidate set is what the rule gives for the history it cites, or
    names the researcher's own question when there is no rule.
    """
    docs = ctx['documents']; records = ctx['records']; ev = ctx['evidence']; proposer = ctx['proposer']
    if proposer == 'Principal' and not records: return bool(docs)
    designs = [r for r in records if r['body'].get('kind') == 'EXPERIMENT DESIGN']
    selections = [r for r in records if r['body'].get('kind') == 'SELECTION']
    plain = [r for r in records if r['body'].get('kind') == 'plain']
    if len(designs) != 1 or len(selections) != 1: return False
    design, selection = designs[0], selections[0]
    analyses = [r for r in plain if (r['body'].get('design') or {}).get('sequence') == design['seq']]
    if len(analyses) != 1: return False
    analysis = analyses[0]; others = [r for r in plain if r is not analysis]
    if any(r['actor'] != proposer for r in (design, analysis, selection)): return False
    if design['body'].get('failure') or analysis['body'].get('failure'): return False
    res = analysis['body']['result']
    if res.get('design') != {'seq': design['seq'], 'sha256': design['sha256']}: return False
    cited = {(i['seq'], i['sha256']) for i in res.get('inputs', [])}
    if cited != {(x['seq'], x['sha256']) for x in docs + others}: return False
    attempt = ev.get(analysis['body']['attempt'])
    if attempt is None or attempt['kind'] != 'ATTEMPT' or attempt['actor'] != proposer or attempt['seq'] <= design['seq']: return False
    if not any(e['kind'] == 'SETTLEMENT' and e['body']['attempt'] == attempt['seq'] for e in ev.values()): return False
    refs = {(r['sequence'], r['sha256']) for r in attempt['body']['input']['input_refs']}
    if (design['seq'], design['sha256']) not in refs or not cited <= refs: return False
    spec = design['body'].get('analysis') or {}
    if kind is not None and spec.get('kind') != kind: return False
    if not recompute(Inputs(docs + others + [design]), spec, res): return False
    if analysis['body']['reproducibility']['result_hash'] != digest(res): return False
    expected = conclude(res, design['body'].get('expectation'), design['body']['question'])['state']
    if (analysis['body'].get('conclusion') or {}).get('state') != expected: return False
    sel = selection['body']['result']
    if sel.get('analysis') != {'seq': analysis['seq'], 'sha256': analysis['sha256']}: return False
    if rule is None:
        return sel.get('chosen') == OWN and sel.get('candidates', []) == [] and sel.get('rejections', []) == []
    earlier = [ev[h['sequence']] for h in sel.get('history_used', []) if h['sequence'] in ev and ev[h['sequence']]['sha256'] == h['sha256']]
    if len(earlier) != len(sel.get('history_used', [])): return False
    all_docs = [e for e in ev.values() if e['kind'] == 'OBSERVATION' and e['body'].get('form') == 'DOCUMENT']
    live, excluded, reinstated = rule.live_set(expected, rule.gather_history(earlier, all_docs), sel.get('theme'))
    if [c['id'] for c in live] != [c['id'] for c in sel.get('candidates', [])]: return False
    if [x['id'] for x in excluded] != [x['id'] for x in sel.get('excluded', [])]: return False
    chosen = sel.get('chosen')
    if chosen != OWN and chosen not in {c['id'] for c in live}: return False
    if {c['id'] for c in live} - {chosen} != {r['id'] for r in sel.get('rejections', [])}: return False
    return True


def evaluator(recompute, rule=None, kind=None):
    """The evaluate function a Checker design registers, from the team's recompute and the researcher's rule, if any.

    recompute(inputs, spec, result) -> bool says whether the recorded result is what the analysis gives on the
    committed inputs. That is what counts as a valid result. The record checks are check_records.
    """
    def validate(ctx): return check_records(ctx, recompute, rule, kind)
    def evaluate(snapshot, transition_id, actor, grant, attempt, profile):
        return toolkit_evaluate(snapshot, transition_id, actor, grant, attempt, profile, validate_motivation=validate)
    return evaluate
