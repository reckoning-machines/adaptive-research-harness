"""AD-S1.0: the researcher that runs the signal-groups script through ARH on the Principal's behalf.

Design records the expectation first. Run funds the attempt, lets the host
run the tool, records the result with its conclusion, settles. Candidates
come from the conclusion and the history by the declared rule in
candidates.py. The Principal's choice is recorded with its rejections and
their reconsideration conditions, and the next investigation is proposed
as a Theme. The researcher proposes; the evaluator verifies; the Principal
decides.
"""
from __future__ import annotations
from copy import deepcopy
import json
import os
import time
from pathlib import Path
from arh_client import Researcher, Execution, Connection, event_ref
from arh_client.research import expected_maximum
from arh_client.protocol import digest, amount
from examples.signal_groups.candidates import live_set, gather_history

STEP = 'analyze-signal'; TOOL = 'SIGNAL-GROUPS-1'; PARAMETERS = {'analysis_from': 'design'}; SOURCE = 'SRC-SIG-SYN'; UMBRELLA = 'TH-S0'
COMPARATORS = ('>=', '>', '<=', '<', '==')


def compare(metric, expectation):
    def ratio(x): return (x['numerator'], x['denominator']) if isinstance(x, dict) else (x, 1)
    a, b = ratio(metric); c, d = ratio(expectation['value'])
    if b == 0 or d == 0: return 'INCONCLUSIVE'
    lhs, rhs = a * d, c * b; op = expectation['comparator']
    return 'MET' if {'>=': lhs >= rhs, '>': lhs > rhs, '<=': lhs <= rhs, '<': lhs < rhs, '==': lhs == rhs}[op] else 'NOT_MET'


class SignalResearcher:
    def __init__(self, connection): self.r = Researcher(connection); self.c = connection
    def documents(self): return self.r.documents(SOURCE)
    def records(self, kind=None):
        return [e for e in self.c.history('E') if e['kind'] == 'RESEARCH_RECORD' and e['actor'] == self.c.actor and (kind is None or e['body'].get('kind') == kind)]

    def design(self, question, expectation, analysis, document_refs, revises=None, theme=None, key=None):
        assert expectation.get('comparator') in COMPARATORS and 'value' in expectation and isinstance(expectation.get('statement'), str)
        assert analysis.get('kind') == 'signal-groups' and analysis.get('signal') and analysis.get('outcome')
        refs = [event_ref(self.c.get(r)) if 'raw_sha256' not in r else r for r in document_refs]
        result = {'question': question, 'expectation': expectation, 'analysis': analysis, 'documents': [{'seq': r['sequence'], 'sha256': r['sha256']} for r in refs], 'theme': theme or UMBRELLA, 'recorded_at': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())}
        body = self.r.record_body(None, question, result, None, refs, kind='EXPERIMENT DESIGN', parameters={'theme': theme or UMBRELLA}, revises=revises,
                                  tool={'id': TOOL, 'planned': True}, claims=[{'kind': 'QUESTION', 'text': question}, {'kind': 'ASSUMPTION', 'text': expectation['statement']}],
                                  extra={'expectation': expectation, 'analysis': analysis})
        return self.r.research_commit(body, key or Connection.new_key())

    def run(self, design_ref, keys=None, hook=lambda point: None):
        """Fund and run one analysis. keys may be supplied and persisted by the caller so that a re-run resumes rather than repeats."""
        keys = keys or {k: Connection.new_key() for k in ('reserve', 'attempt', 'record', 'settle', 'close')}
        design = self.c.get(design_ref); refs = [self.c.get(d) for d in design['body']['closure']['refs']]
        docs = [event_ref(e) for e in refs if e['kind'] == 'OBSERVATION']; dref = event_ref(design)
        maximum = amount(expected_maximum(self.r.step(STEP), len(docs))); out = {'keys': keys, 'design': dref, 'documents': len(docs)}
        res = self.r.reserve(maximum, {'kind': 'Theme', 'id': UMBRELLA}, keys['reserve']); out['reservation'] = res
        if not res.ok: out['status'] = 'refused'; out['reason'] = res.reason; return out
        att = self.r.attempt(res.sequence, STEP, TOOL, docs + [dref], PARAMETERS, maximum, keys['attempt']); out['attempt'] = att
        if not att.ok: out['status'] = 'refused'; out['reason'] = att.reason; return out
        hook('after_attempt')
        ex = Execution(self.r, att.sequence, att.input_hash, TOOL, maximum); run = ex.run(); out['execution'] = run['status']
        hook('after_execution')
        if run['status'] == 'uncertain':
            out['settlement'] = ex.settle_unknown(keys['settle']); out['status'] = 'uncertain'; return out
        receipt = run['receipt']; result = receipt['result']; error = receipt.get('error'); conclusion = None
        if not error:
            exp = design['body']['expectation']; n = result['n']
            state = 'INCONCLUSIVE' if n < exp.get('minimum_n', 1) else compare(result['metric'], exp)
            conclusion = {'state': state, 'metric': result['metric'], 'n': n, 'expectation': exp, 'rule': 'exact comparison of the spread with the expectation by cross-multiplication; INCONCLUSIVE below minimum_n',
                          'text': f"{design['body']['question']} Expectation {exp['statement']}: {state}."}
        body = self.r.record_body(att.sequence, design['body']['question'], result if not error else None, error, docs + [dref], kind='plain',
                                  claims=[{'kind': 'REPORTED', 'document': dref, 'location': '/', 'text': 'Design and expectation recorded before the attempt'},
                                          {'kind': 'INTERPRETATION', 'reported': [0], 'text': conclusion['text'] if conclusion else 'Analysis failed; no conclusion'}],
                                  extra={'design': dref, 'conclusion': conclusion})
        rec = self.r.research_commit(body, keys['record']); out['record'] = rec
        out['settlement'] = ex.settle(receipt, keys['settle']); out['closed'] = self.r.close(res.sequence, keys['close']).ok
        out['conclusion'] = conclusion; out['status'] = 'recorded' if rec.ok else 'failed'; return out

    def candidates(self, analysis_ref, theme=None):
        """The live candidate set for this conclusion given the history, with what was excluded or reinstated and why."""
        rec = self.c.get(analysis_ref); conclusion = rec['body'].get('conclusion')
        if not conclusion: return {'candidates': [], 'excluded': [], 'reinstated': [], 'history_used': []}
        earlier = self.records('SELECTION'); docs = self.documents(); theme = theme or UMBRELLA
        history = gather_history(earlier, docs, theme); live, excluded, reinstated = live_set(conclusion['state'], history)
        return {'candidates': live, 'excluded': excluded, 'reinstated': reinstated, 'history_used': [{'ledger': 'E', 'sequence': e['seq'], 'sha256': e['sha256']} for e in earlier], 'theme': theme}

    def select(self, analysis_ref, chosen, reason, next_question, theme=None, key=None):
        rec = self.c.get(analysis_ref); c = self.candidates(analysis_ref, theme); ids = {x['id'] for x in c['candidates']}
        assert chosen in ids, 'chosen candidate must be in the live set'
        result = {'analysis': {'seq': rec['seq'], 'sha256': rec['sha256']}, 'candidates': c['candidates'], 'excluded': c['excluded'], 'reinstated': c['reinstated'], 'history_used': c['history_used'],
                  'theme': c['theme'], 'chosen': chosen, 'reason': reason, 'next_question': next_question,
                  'rejections': [{'id': x['id'], 'reason': 'Not selected: ' + reason, 'reconsider_when': x['reconsider_when']} for x in c['candidates'] if x['id'] != chosen], 'conclusion': rec['body']['conclusion']['state']}
        body = self.r.record_body(None, 'Which investigation follows from this result?', result, None, [event_ref(rec)], kind='SELECTION', parameters={'rule': 'candidates.py live_set over the conclusion and the history'},
                                  tool={'id': TOOL, 'planned': False}, claims=[{'kind': 'INTERPRETATION', 'reported': [0], 'text': f'Chose {chosen}: {reason}'}])
        return self.r.research_commit(body, key or Connection.new_key())

    def propose(self, selection_ref, theme_id, predecessor_theme=None, budget='1.00', keys=None):
        keys = keys or {'propose': Connection.new_key(), 'fund': Connection.new_key()}
        sel = self.c.get(selection_ref); a = sel['body']['result']['analysis']; analysis = self.c.get({'ledger': 'E', 'sequence': a['seq'], 'sha256': a['sha256']})
        design = self.c.get(analysis['body']['design']); docs = [self.c.get(r) for r in design['body']['closure']['refs']]
        refs = [{k: v for k, v in event_ref(e).items() if k != 'raw_sha256'} for e in docs + [design, analysis, sel]]
        s = sel['body']['result']; conclusion = analysis['body']['conclusion']
        content = {'ThemeId': theme_id, 'predecessor': predecessor_theme, 'statement': s['next_question'], 'motivation_closure': {'N': self.c.state()['N'], 'refs': refs},
                   'typed_claims': [{'kind': 'REPORTED', 'text': f"Spread {conclusion['metric']} over n={conclusion['n']}; expectation {conclusion['expectation']['statement']}"},
                                    {'kind': 'INTERPRETATION', 'text': conclusion['text']}, {'kind': 'QUESTION', 'text': s['next_question']},
                                    {'kind': 'ASSUMPTION', 'text': 'Reconstruction on committed rows; no forward standing.'}],
                   'selection_basis': {'uncertainty': s['next_question'], 'decision_it_could_change': 'Which design the Principal commits next.',
                                       'experiment': f"Candidate {s['chosen']} chosen from {len(s['candidates'])}; {len(s['excluded'])} excluded by earlier rejections.", 'value_estimate': 'UNESTIMATED',
                                       'value_basis': 'No investment-economic inference from reconstruction alone.', 'cost_estimate_units': budget, 'time_estimate_ms': 600000,
                                       'horizon': 'The next design.', 'stopping_rule': 'When the next conclusion is recorded.', 'origin': {'selection_record': refs[-1], 'reason': s['reason']}}}
        return self.r.propose_theme(content, budget, keys['propose'], keys['fund'])
