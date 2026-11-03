"""CHECK-L-1: the evaluator under the Checker identity.

Uses the client checking toolkit for the common and class criteria and
supplies the Theme motivation validator: recompute the cited analysis from
the cited documents and design with this module's own code, verify the
conclusion against the recorded expectation, the order of design before
attempt, the settlement, and that the selection chose among the candidates
the evidence produced. Verifies arithmetic and order, not judgment.
"""
from __future__ import annotations
import re
from arh_client.checking import evaluate as toolkit_evaluate
from arh_client.protocol import digest


def _passes(row, conds):
    for c in conds:
        v = row.get(c['field'])
        if 'equals' in c and v != c['equals']: return False
        if 'contains' in c and not (isinstance(v, str) and c['contains'].lower() in v.lower()): return False
        for k, op in (('at_least', lambda a, b: a >= b), ('at_most', lambda a, b: a <= b), ('greater_than', lambda a, b: a > b), ('less_than', lambda a, b: a < b)):
            if k in c and not (type(v) is int and op(v, c[k])): return False
    return True


def recount(spec, docs):
    """Independent implementation of the two analyses. Returns (metric, n)."""
    if spec['kind'] == 'term-count':
        hits = 0
        for d in docs:
            text = d['text']; flags = 0 if spec.get('case_sensitive') else re.IGNORECASE
            if any(re.search(r'(?<!\w)' + re.escape(t) + r'(?!\w)', text, flags) for t in spec['terms']): hits += 1
        return {'numerator': hits, 'denominator': len(docs)}, len(docs)
    if spec['kind'] == 'table-stat':
        rows = [r for d in docs for r in d['rows'] if _passes(r, spec.get('filter', []))]; n = len(rows); stat = spec['stat']
        if stat == 'count': return n, n
        if stat == 'ratio': return {'numerator': sum(1 for r in rows if _passes(r, spec.get('numerator', []))), 'denominator': n}, n
        values = [r[spec['column']] for r in rows]
        return (sum(values) if stat == 'sum' else {'numerator': sum(values), 'denominator': n}), n
    raise ValueError('unsupported analysis')


def compare(metric, expectation):
    """MET, NOT_MET or INCONCLUSIVE, exactly as the researcher's declared rule computes it."""
    def ratio(x): return (x['numerator'], x['denominator']) if isinstance(x, dict) else (x, 1)
    a, b = ratio(metric); c, d = ratio(expectation['value'])
    if b == 0 or d == 0: return 'INCONCLUSIVE'
    lhs, rhs = a * d, c * b; op = expectation['comparator']
    met = {'>=': lhs >= rhs, '>': lhs > rhs, '<=': lhs <= rhs, '<': lhs < rhs, '==': lhs == rhs}[op]
    return 'MET' if met else 'NOT_MET'


def validate_motivation(ctx):
    docs = ctx['documents']; records = ctx['records']; ev = ctx['evidence']; proposer = ctx['proposer']
    if proposer == 'Principal' and not records:
        # A Principal control theme at startup cites the charter document only; the toolkit already verified the closure.
        return bool(docs) and all(d['body'].get('class') == 'historical' for d in docs)
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
    if any(d['body'].get('class') != 'historical' for d in docs): return False
    attempt = ev.get(analysis['body']['attempt'])
    if attempt is None or attempt['kind'] != 'ATTEMPT' or attempt['actor'] != proposer or attempt['seq'] <= design['seq']: return False
    if not any(e['kind'] == 'SETTLEMENT' and e['body']['attempt'] == attempt['seq'] for e in ev.values()): return False
    refs = {(r['sequence'], r['sha256']) for r in attempt['body']['input']['input_refs']}
    if (design['seq'], design['sha256']) not in refs or not cited <= refs: return False
    metric, n = recount(design['body']['analysis'], [d['body']['document'] for d in docs])
    if res.get('metric') != metric or res.get('n') != n: return False
    if analysis['body']['reproducibility']['result_hash'] != digest(res): return False
    expectation = design['body']['expectation']
    expected = 'INCONCLUSIVE' if n < expectation.get('minimum_n', 1) else compare(metric, expectation)
    if analysis['body'].get('conclusion', {}).get('state') != expected: return False
    sel = selection['body']['result']
    if sel.get('analysis') != {'seq': analysis['seq'], 'sha256': analysis['sha256']}: return False
    if sel.get('chosen') not in {c['id'] for c in sel.get('candidates', [])}: return False
    if set(c['id'] for c in sel['candidates']) - {sel['chosen']} != {r['id'] for r in sel.get('rejections', [])}: return False
    return True


def evaluate(snapshot, transition_id, actor, grant, attempt, profile):
    return toolkit_evaluate(snapshot, transition_id, actor, grant, attempt, profile, validate_motivation=validate_motivation)
