"""AD-L1.0: the researcher the workbench drives on the Principal's behalf.

The Principal states a question, an expectation and an analysis. This program
commits the design, funds and records the attempt, lets the host run the
calculator, records the result with its conclusion against the expectation,
derives the next-step candidates from that conclusion by a declared rule,
records the Principal's selection, and proposes the next investigation as a
Theme. It proposes; the evaluator verifies and the Principal permits.
"""
from __future__ import annotations
from copy import deepcopy
import time
from arh_client import Researcher, Execution, Connection, event_ref
from arh_client.research import expected_maximum
from arh_client.protocol import digest, amount

STEP = 'analyze-documents'; TOOL = 'LOCAL-CALC-1'; PARAMETERS = {'analysis_from': 'design'}; SOURCE = 'SRC-LOCAL-DOC'; UMBRELLA = 'TH-L0'
COMPARATORS = ('>=', '>', '<=', '<', '==')

CANDIDATE_RULE = {
    'MET': [
        {'id': 'extend', 'question': 'Does the result hold on documents not yet examined?', 'why': 'A met expectation on this set says nothing about the next set.'},
        {'id': 'sharpen', 'question': 'Does a stricter expectation still hold on the same documents?', 'why': 'A loose expectation is easy to meet.'},
        {'id': 'alternative', 'question': 'What else would produce the same pattern?', 'why': 'The pattern may have a cause the analysis did not measure.'}],
    'NOT_MET': [
        {'id': 'revise-expectation', 'question': 'Was the expectation wrong rather than the idea?', 'why': 'The documents may support a weaker or different claim.'},
        {'id': 'change-analysis', 'question': 'Would a different measurement of the same question decide it?', 'why': 'The analysis may not capture what the question asks.'},
        {'id': 'reject', 'question': 'Record the conclusion as rejected and ask a different question.', 'why': 'The evidence went against the expectation.'}],
    'INCONCLUSIVE': [
        {'id': 'add-documents', 'question': 'Does the result change with more documents?', 'why': 'Fewer documents than the design required.'},
        {'id': 'relax-minimum', 'question': 'Is a smaller minimum defensible for this question?', 'why': 'The minimum was set before seeing how many documents exist.'}],
}


def compare(metric, expectation):
    def ratio(x): return (x['numerator'], x['denominator']) if isinstance(x, dict) else (x, 1)
    a, b = ratio(metric); c, d = ratio(expectation['value'])
    if b == 0 or d == 0: return 'INCONCLUSIVE'
    lhs, rhs = a * d, c * b; op = expectation['comparator']
    return 'MET' if {'>=': lhs >= rhs, '>': lhs > rhs, '<=': lhs <= rhs, '<': lhs < rhs, '==': lhs == rhs}[op] else 'NOT_MET'


class LocalResearcher:
    def __init__(self, connection): self.r = Researcher(connection); self.c = connection

    # ----- reads -----
    def documents(self): return self.r.documents(SOURCE)
    def records(self, kind=None):
        return [e for e in self.c.history('E') if e['kind'] == 'RESEARCH_RECORD' and e['actor'] == self.c.actor and (kind is None or e['body'].get('kind') == kind)]

    # ----- 1. design: the expectation before the analysis -----
    def design(self, question: str, expectation: dict, analysis: dict, document_refs: list, revises=None, theme: str | None = None, key: str | None = None):
        """Commit an EXPERIMENT DESIGN citing the documents it will analyse. No attempt, no charge."""
        assert expectation.get('comparator') in COMPARATORS and 'value' in expectation and isinstance(expectation.get('statement'), str), 'expectation needs comparator, value, statement'
        assert analysis.get('kind') in ('term-count', 'table-stat'), 'analysis kind'
        refs = [event_ref(self.c.get(r)) if 'raw_sha256' not in r else r for r in document_refs]
        result = {'question': question, 'expectation': expectation, 'analysis': analysis, 'documents': [{'seq': r['sequence'], 'sha256': r['sha256']} for r in refs], 'theme': theme or UMBRELLA, 'recorded_at': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())}
        body = self.r.record_body(None, question, result, None, refs, kind='EXPERIMENT DESIGN', parameters={'theme': theme or UMBRELLA}, revises=revises,
                                  tool={'id': TOOL, 'planned': True}, claims=[{'kind': 'QUESTION', 'text': question}, {'kind': 'ASSUMPTION', 'text': expectation['statement']}],
                                  extra={'expectation': expectation, 'analysis': analysis})
        return self.r.research_commit(body, key or Connection.new_key())

    # ----- 2. run: reserve, attempt, host-run calculation, record, settle -----
    def run(self, design_ref, keys: dict | None = None):
        """Fund and run one analysis of a committed design. Returns a dict with the outcomes of each step; refused steps stop it."""
        keys = keys or {k: Connection.new_key() for k in ('reserve', 'attempt', 'record', 'settle', 'close')}
        design = self.c.get(design_ref); refs = [self.c.get(d) for d in design['body']['closure']['refs']]
        docs = [event_ref(e) for e in refs if e['kind'] == 'OBSERVATION']; dref = event_ref(design)
        maximum = amount(expected_maximum(self.r.step(STEP), len(docs)))
        out = {'keys': keys, 'design': dref, 'documents': len(docs)}
        res = self.r.reserve(maximum, {'kind': 'Theme', 'id': UMBRELLA}, keys['reserve']); out['reservation'] = res
        if not res.ok: out['status'] = 'refused'; out['reason'] = res.reason; return out
        att = self.r.attempt(res.sequence, STEP, TOOL, docs + [dref], PARAMETERS, maximum, keys['attempt']); out['attempt'] = att
        if not att.ok: out['status'] = 'refused'; out['reason'] = att.reason; return out
        ex = Execution(self.r, att.sequence, att.input_hash, TOOL, maximum); run = ex.run(); out['execution'] = run['status']
        if run['status'] == 'uncertain':
            out['settlement'] = ex.settle_unknown(keys['settle']); out['status'] = 'uncertain'; return out
        receipt = run['receipt']; result = receipt['result']; error = receipt.get('error')
        conclusion = None
        if not error:
            exp = design['body']['expectation']; n = result['n']
            state = 'INCONCLUSIVE' if n < exp.get('minimum_n', 1) else compare(result['metric'], exp)
            conclusion = {'state': state, 'metric': result['metric'], 'n': n, 'expectation': exp, 'rule': 'exact comparison of the metric with the expectation by cross-multiplication; INCONCLUSIVE below minimum_n',
                          'text': f"{design['body']['question']} Expectation {exp['statement']}: {state}."}
        body = self.r.record_body(att.sequence, design['body']['question'], result if not error else None, error, docs + [dref], kind='plain',
                                  claims=[{'kind': 'REPORTED', 'document': dref, 'location': '/', 'text': 'Design and expectation recorded before the attempt'},
                                          {'kind': 'INTERPRETATION', 'reported': [0], 'text': conclusion['text'] if conclusion else 'Analysis failed; no conclusion'}],
                                  extra={'design': dref, 'conclusion': conclusion})
        rec = self.r.research_commit(body, keys['record']); out['record'] = rec
        out['settlement'] = ex.settle(receipt, keys['settle']); out['closed'] = self.r.close(res.sequence, keys['close']).ok
        out['conclusion'] = conclusion; out['status'] = 'recorded' if rec.ok else 'failed'; return out

    # ----- 3. candidates from the evidence, the Principal's choice recorded -----
    def candidates(self, analysis_ref):
        rec = self.c.get(analysis_ref); conclusion = rec['body'].get('conclusion')
        if not conclusion: return []
        return deepcopy(CANDIDATE_RULE[conclusion['state']])
    def select(self, analysis_ref, chosen: str, reason: str, next_question: str, key: str | None = None):
        """Record which candidate the Principal chose and why the others were not, as a SELECTION citing the analysis."""
        rec = self.c.get(analysis_ref); cands = self.candidates(analysis_ref); ids = {c['id'] for c in cands}
        assert chosen in ids, 'chosen candidate must come from the evidence'
        result = {'analysis': {'seq': rec['seq'], 'sha256': rec['sha256']}, 'candidates': cands, 'chosen': chosen, 'reason': reason, 'next_question': next_question,
                  'rejections': [{'id': c['id'], 'reason': 'Not selected: ' + reason} for c in cands if c['id'] != chosen], 'conclusion': rec['body']['conclusion']['state']}
        aref = event_ref(rec)
        body = self.r.record_body(None, 'Which investigation follows from this result?', result, None, [aref], kind='SELECTION', parameters={'rule': 'candidate set by conclusion state'},
                                  tool={'id': TOOL, 'planned': False}, claims=[{'kind': 'INTERPRETATION', 'reported': [0], 'text': f'Chose {chosen}: {reason}'}])
        return self.r.research_commit(body, key or Connection.new_key())

    # ----- 4. propose the next investigation -----
    def propose(self, selection_ref, theme_id: str, predecessor_theme: str | None = None, budget: str = '1.00', keys: dict | None = None):
        keys = keys or {'propose': Connection.new_key(), 'fund': Connection.new_key()}
        sel = self.c.get(selection_ref); a = sel['body']['result']['analysis']; analysis = self.c.get({'ledger': 'E', 'sequence': a['seq'], 'sha256': a['sha256']})
        design = self.c.get(analysis['body']['design']); docs = [self.c.get(r) for r in design['body']['closure']['refs']]
        refs = [{k: v for k, v in event_ref(e).items() if k != 'raw_sha256'} for e in docs + [design, analysis, sel]]
        s = sel['body']['result']; conclusion = analysis['body']['conclusion']
        content = {'ThemeId': theme_id, 'predecessor': predecessor_theme, 'statement': s['next_question'],
                   'motivation_closure': {'N': self.c.state()['N'], 'refs': refs},
                   'typed_claims': [{'kind': 'REPORTED', 'text': f"Metric {conclusion['metric']} over n={conclusion['n']}; expectation {conclusion['expectation']['statement']}"},
                                    {'kind': 'INTERPRETATION', 'text': conclusion['text']},
                                    {'kind': 'QUESTION', 'text': s['next_question']},
                                    {'kind': 'ASSUMPTION', 'text': 'Historical reconstruction on the Principal\'s documents; no forward standing.'}],
                   'selection_basis': {'uncertainty': s['next_question'], 'decision_it_could_change': 'Which design the Principal commits next.',
                                       'experiment': f"Candidate {s['chosen']} chosen from {len(s['candidates'])} the conclusion produced.", 'value_estimate': 'UNESTIMATED',
                                       'value_basis': 'No investment-economic inference from historical reconstruction alone.', 'cost_estimate_units': budget, 'time_estimate_ms': 600000,
                                       'horizon': 'The next design.', 'stopping_rule': 'When the next conclusion is recorded.', 'origin': {'selection_record': refs[-1], 'reason': s['reason']}}}
        return self.r.propose_theme(content, budget, keys['propose'], keys['fund'], predecessor=None)
