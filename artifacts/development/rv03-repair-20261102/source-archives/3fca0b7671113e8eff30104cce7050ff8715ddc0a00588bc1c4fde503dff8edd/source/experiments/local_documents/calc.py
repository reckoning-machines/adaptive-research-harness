"""LOCAL-CALC-1: the host-run calculator.

Receives every admitted input: the committed documents and the one committed
EXPERIMENT DESIGN record. Runs the design's declared analysis and returns
per-document detail, a summary and the metric the design names. All numbers
are exact integers or integer ratios; nothing here decides anything.
"""
from __future__ import annotations
import hashlib
import json
import re


def canonical(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
def digest(v): return hashlib.sha256(canonical(v)).hexdigest()


def _holds(row, conditions):
    for c in conditions:
        v = row.get(c['field'])
        if 'equals' in c:
            if v != c['equals']: return False
        elif 'contains' in c:
            if not isinstance(v, str) or c['contains'].lower() not in v.lower(): return False
        else:
            if type(v) is not int: return False
            name, bound = next((k, c[k]) for k in ('at_least', 'at_most', 'greater_than', 'less_than') if k in c)
            if name == 'at_least' and not v >= bound: return False
            if name == 'at_most' and not v <= bound: return False
            if name == 'greater_than' and not v > bound: return False
            if name == 'less_than' and not v < bound: return False
    return True


def term_count(spec, docs):
    terms = spec['terms']; per = []
    for d in docs:
        text = d['document'].get('text')
        if not isinstance(text, str): raise ValueError('term-count needs text documents')
        hay = text if spec.get('case_sensitive') else text.lower()
        counts = {t: len(re.findall(r'(?<!\w)' + re.escape(t if spec.get('case_sensitive') else t.lower()) + r'(?!\w)', hay)) for t in terms}
        per.append({'item_id': d['document']['item_id'], 'file': d['document']['file']['name'], 'counts': counts, 'total': sum(counts.values()), 'any': any(counts.values())})
    with_any = sum(1 for p in per if p['any'])
    summary = {'documents': len(per), 'documents_with_any': with_any, 'total_occurrences': sum(p['total'] for p in per), 'per_term': {t: sum(p['counts'][t] for p in per) for t in terms}}
    return per, summary, {'numerator': with_any, 'denominator': len(per)}, len(per)


def table_stat(spec, docs):
    rows = []; per = []
    for d in docs:
        r = d['document'].get('rows')
        if not isinstance(r, list): raise ValueError('table-stat needs row documents')
        passing = [x for x in r if _holds(x, spec.get('filter', []))]
        per.append({'item_id': d['document']['item_id'], 'file': d['document']['file']['name'], 'rows': len(r), 'passing': len(passing)}); rows += passing
    stat = spec['stat']; n = len(rows)
    if stat == 'count': metric = n
    elif stat == 'ratio': metric = {'numerator': sum(1 for x in rows if _holds(x, spec.get('numerator', []))), 'denominator': n}
    else:
        col = spec['column']; values = [x.get(col) for x in rows]
        if any(type(v) is not int for v in values): raise ValueError('column ' + col + ' must be integer in every passing row')
        metric = sum(values) if stat == 'sum' else {'numerator': sum(values), 'denominator': n}
    summary = {'documents': len(per), 'rows_passing': n, 'stat': stat, 'column': spec.get('column')}
    return per, summary, metric, n


ANALYSES = {'term-count': term_count, 'table-stat': table_stat}


def calculate(inputs):
    docs = [x for x in inputs if x['kind'] == 'OBSERVATION']
    designs = [x for x in inputs if x['kind'] == 'RESEARCH_RECORD' and x['body'].get('kind') == 'EXPERIMENT DESIGN']
    if len(designs) != 1 or not docs: raise ValueError('INVALID_INPUT')
    design = designs[0]; spec = design['body'].get('analysis') or {}
    if spec.get('kind') not in ANALYSES: raise ValueError('UNSUPPORTED_ANALYSIS')
    per, summary, metric, n = ANALYSES[spec['kind']](spec, [d['body'] for d in docs])
    return {'analysis': spec, 'per_document': per, 'summary': summary, 'metric': metric, 'n': n,
            'inputs': [{'seq': d['seq'], 'sha256': d['sha256']} for d in docs], 'design': {'seq': design['seq'], 'sha256': design['sha256']},
            'input_sha256': digest([d['body']['document'] for d in docs]), 'class': 'historical', 'synthetic': False}
