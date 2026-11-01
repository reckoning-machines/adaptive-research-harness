"""Connect one analysis function to ARH.

A team supplies four things. The analysis function the host runs. The
inputs, as documents imported and a design naming what to compute over
them. The budget, in the setup. The evaluation function that says what a
valid result is. This module supplies the rest: the design record with its
expectation, the reservation, the attempt, the execution with its receipt,
the record with its conclusion, settlement and closure, keys persisted so
a re-run resumes rather than repeats, the candidate rule over the history,
the selection record with its rejections, the Theme proposal, the host-tool
wrapper and the record checks an evaluator makes before the team's own
recomputation. The researcher still decides what to investigate, through
its candidate table and each selection. The evaluator still decides what
counts as a valid result, through recompute. Standard library only.
"""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import os
import time
from .protocol import digest, amount, canonical, require
from .connection import Connection
from .research import Researcher, Execution, event_ref, expected_maximum
from .checking import evaluate as toolkit_evaluate

COMPARATORS = ('>=', '>', '<=', '<', '==')
CONDITIONS = ('new_documents', 'new_direction', 'always', 'never')
KEY_NAMES = ('reserve', 'attempt', 'record', 'settle', 'close')


def compare(metric, expectation):
    """MET, NOT_MET or INCONCLUSIVE by exact cross-multiplication. Values are integers or {'numerator','denominator'}."""
    def ratio(x): return (x['numerator'], x['denominator']) if isinstance(x, dict) else (x, 1)
    a, b = ratio(metric); c, d = ratio(expectation['value'])
    if b == 0 or d == 0: return 'INCONCLUSIVE'
    lhs, rhs = a * d, c * b; op = expectation['comparator']
    return 'MET' if {'>=': lhs >= rhs, '>': lhs > rhs, '<=': lhs <= rhs, '<': lhs < rhs, '==': lhs == rhs}[op] else 'NOT_MET'


def conclude(result, expectation, question):
    """The conclusion a result supports against a recorded expectation. INCONCLUSIVE below minimum_n."""
    n = result['n']; state = 'INCONCLUSIVE' if n < expectation.get('minimum_n', 1) else compare(result['metric'], expectation)
    return {'state': state, 'metric': result['metric'], 'n': n, 'expectation': expectation,
            'rule': 'exact comparison of the metric with the expectation by cross-multiplication; INCONCLUSIVE below minimum_n',
            'text': f"{question} Expectation {expectation['statement']}: {state}."}


def check_expectation(expectation):
    require(expectation.get('comparator') in COMPARATORS and 'value' in expectation and isinstance(expectation.get('statement'), str), 'INVALID_EXPECTATION', str(expectation))


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

    table: {'MET': [...], 'NOT_MET': [...], 'INCONCLUSIVE': [...]}, each entry {'id', 'question', 'why', 'reconsider_when'}.
    reconsider_when is 'new_documents', 'new_direction', 'always' or 'never'. A candidate rejected under one
    selection stays out of later sets until its condition is met. An entry with always_available true is never
    held back; use it for the choice to record a conclusion as rejected and stop.
    """
    def __init__(self, table):
        for state, entries in table.items():
            require(state in ('MET', 'NOT_MET', 'INCONCLUSIVE'), 'INVALID_CANDIDATE', state)
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


class AnalysisResearcher:
    """The research lifecycle for one declared analysis under one researcher identity.

    The research step, its tool and parameters, the source and the umbrella Theme come from the frozen
    profile. A subclass sets rule, a CandidateRule, and may set analysis_kind, the 'kind' every design's
    analysis must name. Every command takes keys the caller may persist first; see persisted_keys.
    """
    rule: CandidateRule | None = None
    analysis_kind: str | None = None

    def __init__(self, connection, rule=None):
        self.c = connection; self.r = Researcher(connection); self.rule = rule or self.rule
        require(self.rule is not None, 'RULE_REQUIRED', 'an AnalysisResearcher needs a CandidateRule')
        steps = [s for s in connection.experiment()['steps'] if s['kind'] == 'research']
        require(len(steps) == 1, 'CAPABILITY_UNSUPPORTED', 'one research step expected'); step = steps[0]
        self.step = step['name']; self.tool = step['tools'][0]; self.parameters = step.get('parameters') or {}
        self.source = next(iter(connection.experiment()['sources'])); self.umbrella = connection.profile()['setup']['theme']['content']['ThemeId']

    def documents(self): return self.r.documents(self.source)
    def records(self, kind=None):
        return [e for e in self.c.history('E') if e['kind'] == 'RESEARCH_RECORD' and e['actor'] == self.c.actor and (kind is None or e['body'].get('kind') == kind)]

    def design(self, question, expectation, analysis, document_refs, revises=None, theme=None, key=None):
        """Record the question, the expectation and the analysis before any attempt. Returns the Outcome."""
        check_expectation(expectation)
        if self.analysis_kind: require(analysis.get('kind') == self.analysis_kind, 'UNSUPPORTED_ANALYSIS', str(analysis.get('kind')))
        refs = [event_ref(self.c.get(r)) if 'raw_sha256' not in r else r for r in document_refs]; theme = theme or self.umbrella
        result = {'question': question, 'expectation': expectation, 'analysis': analysis, 'documents': [{'seq': r['sequence'], 'sha256': r['sha256']} for r in refs],
                  'theme': theme, 'recorded_at': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())}
        body = self.r.record_body(None, question, result, None, refs, kind='EXPERIMENT DESIGN', parameters={'theme': theme}, revises=revises, tool={'id': self.tool, 'planned': True},
                                  claims=[{'kind': 'QUESTION', 'text': question}, {'kind': 'ASSUMPTION', 'text': expectation['statement']}], extra={'expectation': expectation, 'analysis': analysis})
        return self.r.research_commit(body, key or Connection.new_key())

    def run(self, design_ref, keys=None, hook=lambda point: None):
        """Fund and run one design. Keys persisted by the caller make a re-run resume rather than repeat."""
        keys = keys or {k: Connection.new_key() for k in KEY_NAMES}
        design = self.c.get(design_ref); cited = [self.c.get(d) for d in design['body']['closure']['refs']]
        docs = [event_ref(e) for e in cited if e['kind'] == 'OBSERVATION']; dref = event_ref(design)
        maximum = amount(expected_maximum(self.r.step(self.step), len(docs))); out = {'keys': keys, 'design': dref, 'documents': len(docs)}
        res = self.r.reserve(maximum, {'kind': 'Theme', 'id': self.umbrella}, keys['reserve']); out['reservation'] = res
        if not res.ok: out['status'] = 'refused'; out['reason'] = res.reason; return out
        att = self.r.attempt(res.sequence, self.step, self.tool, docs + [dref], self.parameters, maximum, keys['attempt']); out['attempt'] = att
        if not att.ok: out['status'] = 'refused'; out['reason'] = att.reason; return out
        hook('after_attempt')
        ex = Execution(self.r, att.sequence, att.input_hash, self.tool, maximum); run = ex.run(); out['execution'] = run['status']
        hook('after_execution')
        if run['status'] == 'uncertain':
            out['settlement'] = ex.settle_unknown(keys['settle']); out['status'] = 'uncertain'; return out
        receipt = run['receipt']; result = receipt['result']; error = receipt.get('error')
        conclusion = conclude(result, design['body']['expectation'], design['body']['question']) if not error else None
        body = self.r.record_body(att.sequence, design['body']['question'], result if not error else None, error, docs + [dref], kind='plain',
                                  claims=[{'kind': 'REPORTED', 'document': dref, 'location': '/', 'text': 'Design and expectation recorded before the attempt'},
                                          {'kind': 'INTERPRETATION', 'reported': [0], 'text': conclusion['text'] if conclusion else 'Analysis failed; no conclusion'}],
                                  extra={'design': dref, 'conclusion': conclusion})
        rec = self.r.research_commit(body, keys['record']); out['record'] = rec
        out['settlement'] = ex.settle(receipt, keys['settle']); out['closed'] = self.r.close(res.sequence, keys['close']).ok
        out['conclusion'] = conclusion; out['status'] = 'recorded' if rec.ok else 'failed'; return out

    def candidates(self, analysis_ref, theme=None):
        """The live candidate set for a recorded conclusion, with what the history excluded or reinstated and why."""
        rec = self.c.get(analysis_ref); conclusion = rec['body'].get('conclusion'); theme = theme or self.umbrella
        if not conclusion: return {'candidates': [], 'excluded': [], 'reinstated': [], 'history_used': [], 'theme': theme}
        earlier = self.records('SELECTION'); history = self.rule.gather_history(earlier, self.documents())
        live, excluded, reinstated = self.rule.live_set(conclusion['state'], history, theme)
        return {'candidates': live, 'excluded': excluded, 'reinstated': reinstated, 'history_used': [{'ledger': 'E', 'sequence': e['seq'], 'sha256': e['sha256']} for e in earlier], 'theme': theme}

    def select(self, analysis_ref, chosen, reason, next_question, theme=None, key=None):
        """Record the chosen candidate, the rejected ones with their reconsideration conditions, and the history used."""
        rec = self.c.get(analysis_ref); c = self.candidates(analysis_ref, theme)
        require(chosen in {x['id'] for x in c['candidates']}, 'NOT_A_CANDIDATE', chosen)
        result = {'analysis': {'seq': rec['seq'], 'sha256': rec['sha256']}, 'candidates': c['candidates'], 'excluded': c['excluded'], 'reinstated': c['reinstated'], 'history_used': c['history_used'],
                  'theme': c['theme'], 'chosen': chosen, 'reason': reason, 'next_question': next_question, 'conclusion': rec['body']['conclusion']['state'],
                  'rejections': [{'id': x['id'], 'reason': 'Not selected: ' + reason, 'reconsider_when': x['reconsider_when']} for x in c['candidates'] if x['id'] != chosen]}
        body = self.r.record_body(None, 'Which investigation follows from this result?', result, None, [event_ref(rec)], kind='SELECTION',
                                  parameters={'rule': 'CandidateRule.live_set over the conclusion and the history'}, tool={'id': self.tool, 'planned': False},
                                  claims=[{'kind': 'INTERPRETATION', 'reported': [0], 'text': f'Chose {chosen}: {reason}'}])
        return self.r.research_commit(body, key or Connection.new_key())

    def propose(self, selection_ref, theme_id, predecessor_theme=None, budget='1.00', keys=None):
        """Propose the selected investigation as a Theme, funded from the Research grant. Admission needs a check and the Principal."""
        keys = keys or {'propose': Connection.new_key(), 'fund': Connection.new_key()}
        sel = self.c.get(selection_ref); a = sel['body']['result']['analysis']; analysis = self.c.get({'ledger': 'E', 'sequence': a['seq'], 'sha256': a['sha256']})
        design = self.c.get(analysis['body']['design']); docs = [self.c.get(r) for r in design['body']['closure']['refs']]
        refs = [{k: v for k, v in event_ref(e).items() if k != 'raw_sha256'} for e in docs + [design, analysis, sel]]
        s = sel['body']['result']; conclusion = analysis['body']['conclusion']
        content = {'ThemeId': theme_id, 'predecessor': predecessor_theme, 'statement': s['next_question'], 'motivation_closure': {'N': self.c.state()['N'], 'refs': refs},
                   'typed_claims': [{'kind': 'REPORTED', 'text': f"Metric {conclusion['metric']} over n={conclusion['n']}; expectation {conclusion['expectation']['statement']}"},
                                    {'kind': 'INTERPRETATION', 'text': conclusion['text']}, {'kind': 'QUESTION', 'text': s['next_question']},
                                    {'kind': 'ASSUMPTION', 'text': 'Reconstruction on committed rows; no forward standing.'}],
                   'selection_basis': {'uncertainty': s['next_question'], 'decision_it_could_change': 'Which design the Principal commits next.',
                                       'experiment': f"Candidate {s['chosen']} chosen from {len(s['candidates'])}; {len(s['excluded'])} excluded by earlier rejections.", 'value_estimate': 'UNESTIMATED',
                                       'value_basis': 'No investment-economic inference from reconstruction alone.', 'cost_estimate_units': budget, 'time_estimate_ms': 600000,
                                       'horizon': 'The next design.', 'stopping_rule': 'When the next conclusion is recorded.', 'origin': {'selection_record': refs[-1], 'reason': s['reason']}}}
        return self.r.propose_theme(content, budget, keys['propose'], keys['fund'])


def host_tool(analysis, kind=None):
    """calculate(inputs) for a tool the host runs with interface 'inputs', from analysis(rows, spec).

    analysis receives every row of the committed documents and the design's analysis, and returns a dict
    holding 'metric', the value the expectation compares, and 'n', the rows it used, plus anything else
    worth recording. The wrapper adds the inputs cited, the design, the input hash and the document class.
    """
    def calculate(inputs):
        docs = [x for x in inputs if x['kind'] == 'OBSERVATION']
        designs = [x for x in inputs if x['kind'] == 'RESEARCH_RECORD' and x['body'].get('kind') == 'EXPERIMENT DESIGN']
        if len(designs) != 1 or not docs: raise ValueError('INVALID_INPUT')
        design = designs[0]; spec = design['body'].get('analysis') or {}
        if kind is not None and spec.get('kind') != kind: raise ValueError('UNSUPPORTED_ANALYSIS')
        rows = [r for d in docs for r in d['body']['document'].get('rows', [])]
        result = analysis(rows, spec)
        if not isinstance(result, dict) or 'metric' not in result or 'n' not in result: raise ValueError('INVALID_RESULT')
        cls = 'historical' if any(d['body'].get('class') == 'historical' for d in docs) else 'synthetic'
        return dict(result, analysis=spec, inputs=[{'seq': d['seq'], 'sha256': d['sha256']} for d in docs], design={'seq': design['seq'], 'sha256': design['sha256']},
                    input_sha256=hashlib.sha256(canonical([d['body']['document'] for d in docs])).hexdigest(), **{'class': cls}, synthetic=cls == 'synthetic')
    return calculate


def check_records(ctx, recompute, rule, kind=None):
    """The record checks for a Theme motivated by one design, one analysis and one selection of the proposer.

    The design preceded the attempt, the attempt settled, the record cites exactly the committed documents,
    the result hash holds, recompute(rows, spec, result) accepts the result, the conclusion follows the
    expectation, and the selection's candidate set is what the rule gives for the history it cites.
    """
    docs = ctx['documents']; records = ctx['records']; ev = ctx['evidence']; proposer = ctx['proposer']
    if proposer == 'Principal' and not records: return bool(docs)
    designs = [r for r in records if r['body'].get('kind') == 'EXPERIMENT DESIGN']
    analyses = [r for r in records if r['body'].get('kind') == 'plain' and 'metric' in (r['body'].get('result') or {})]
    selections = [r for r in records if r['body'].get('kind') == 'SELECTION']
    if len(designs) != 1 or len(analyses) != 1 or len(selections) != 1: return False
    design, analysis, selection = designs[0], analyses[0], selections[0]
    if any(r['actor'] != proposer for r in (design, analysis, selection)): return False
    if design['body'].get('failure') or analysis['body'].get('failure'): return False
    res = analysis['body']['result']
    if res.get('design') != {'seq': design['seq'], 'sha256': design['sha256']}: return False
    cited = {(i['seq'], i['sha256']) for i in res['inputs']}
    if cited != {(d['seq'], d['sha256']) for d in docs}: return False
    attempt = ev.get(analysis['body']['attempt'])
    if attempt is None or attempt['kind'] != 'ATTEMPT' or attempt['actor'] != proposer or attempt['seq'] <= design['seq']: return False
    if not any(e['kind'] == 'SETTLEMENT' and e['body']['attempt'] == attempt['seq'] for e in ev.values()): return False
    refs = {(r['sequence'], r['sha256']) for r in attempt['body']['input']['input_refs']}
    if (design['seq'], design['sha256']) not in refs or not cited <= refs: return False
    spec = design['body']['analysis']
    if kind is not None and spec.get('kind') != kind: return False
    rows = [r for d in docs for r in d['body']['document'].get('rows', [])]
    if not recompute(rows, spec, res): return False
    if analysis['body']['reproducibility']['result_hash'] != digest(res): return False
    expectation = design['body']['expectation']; n = res['n']
    expected = 'INCONCLUSIVE' if n < expectation.get('minimum_n', 1) else compare(res['metric'], expectation)
    if analysis['body'].get('conclusion', {}).get('state') != expected: return False
    sel = selection['body']['result']
    if sel.get('analysis') != {'seq': analysis['seq'], 'sha256': analysis['sha256']}: return False
    earlier = [ev[h['sequence']] for h in sel.get('history_used', []) if h['sequence'] in ev and ev[h['sequence']]['sha256'] == h['sha256']]
    if len(earlier) != len(sel.get('history_used', [])): return False
    all_docs = [e for e in ev.values() if e['kind'] == 'OBSERVATION' and e['body'].get('form') == 'DOCUMENT']
    live, excluded, reinstated = rule.live_set(expected, rule.gather_history(earlier, all_docs), sel.get('theme'))
    if [c['id'] for c in live] != [c['id'] for c in sel.get('candidates', [])]: return False
    if [x['id'] for x in excluded] != [x['id'] for x in sel.get('excluded', [])]: return False
    if sel.get('chosen') not in {c['id'] for c in live}: return False
    if {c['id'] for c in live} - {sel['chosen']} != {r['id'] for r in sel.get('rejections', [])}: return False
    return True


def evaluator(recompute, rule, kind=None):
    """The evaluate function a Checker design registers, from the team's recompute and the researcher's rule.

    recompute(rows, spec, result) -> bool says whether the recorded result is what the analysis gives on the
    committed rows. That is what counts as a valid result. The record checks are check_records.
    """
    def validate(ctx): return check_records(ctx, recompute, rule, kind)
    def evaluate(snapshot, transition_id, actor, grant, attempt, profile):
        return toolkit_evaluate(snapshot, transition_id, actor, grant, attempt, profile, validate_motivation=validate)
    return evaluate
