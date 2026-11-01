"""CHECK-S-1: the evaluator under the Checker identity.

For a Theme it re-runs the same script on the committed rows and design and
compares the result, verifies the conclusion against the recorded
expectation, that the design preceded the attempt and the attempt settled,
and that the selection's candidate set follows the declared rule applied to
the history it cites. This checks reproducibility and record integrity. It
does not independently validate the calculation or the research method.
"""
from __future__ import annotations
from arh_client.checking import evaluate as toolkit_evaluate
from arh_client.protocol import digest
from examples.signal_groups.signal_groups import analyze
from examples.signal_groups.candidates import live_set, gather_history


def compare(metric, expectation):
    def ratio(x): return (x['numerator'], x['denominator']) if isinstance(x, dict) else (x, 1)
    a, b = ratio(metric); c, d = ratio(expectation['value'])
    if b == 0 or d == 0: return 'INCONCLUSIVE'
    lhs, rhs = a * d, c * b; op = expectation['comparator']
    return 'MET' if {'>=': lhs >= rhs, '>': lhs > rhs, '<=': lhs <= rhs, '<': lhs < rhs, '==': lhs == rhs}[op] else 'NOT_MET'


def validate_motivation(ctx):
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
    spec = design['body']['analysis']; rows = [r for d in docs for r in d['body']['document'].get('rows', [])]
    again = analyze(rows, spec['signal'], spec['outcome'], int(spec.get('groups', 3)))
    if res.get('metric') != again['spread_top_minus_bottom_bp'] or res.get('n') != again['rows_used'] or res.get('groups') != again['groups']: return False
    if analysis['body']['reproducibility']['result_hash'] != digest(res): return False
    expectation = design['body']['expectation']; n = res['n']
    expected = 'INCONCLUSIVE' if n < expectation.get('minimum_n', 1) else compare(res['metric'], expectation)
    if analysis['body'].get('conclusion', {}).get('state') != expected: return False
    sel = selection['body']['result']
    if sel.get('analysis') != {'seq': analysis['seq'], 'sha256': analysis['sha256']}: return False
    # The candidate set must be what the declared rule gives for the history the selection cites.
    earlier = [ev[h['sequence']] for h in sel.get('history_used', []) if h['sequence'] in ev and ev[h['sequence']]['sha256'] == h['sha256']]
    if len(earlier) != len(sel.get('history_used', [])): return False
    all_docs = [e for e in ev.values() if e['kind'] == 'OBSERVATION' and e['body'].get('form') == 'DOCUMENT']
    history = gather_history(earlier, all_docs, sel.get('theme'))
    live, excluded, reinstated = live_set(expected, history)
    if [c['id'] for c in live] != [c['id'] for c in sel.get('candidates', [])]: return False
    if [x['id'] for x in excluded] != [x['id'] for x in sel.get('excluded', [])]: return False
    if sel.get('chosen') not in {c['id'] for c in live}: return False
    if {c['id'] for c in live} - {sel['chosen']} != {r['id'] for r in sel.get('rejections', [])}: return False
    return True


def evaluate(snapshot, transition_id, actor, grant, attempt, profile):
    return toolkit_evaluate(snapshot, transition_id, actor, grant, attempt, profile, validate_motivation=validate_motivation)
