"""SIGNAL-GROUPS-1: the host-run tool. Wraps signal_groups.analyze without changing it.

Receives every admitted input: the committed CSV documents and the one
EXPERIMENT DESIGN record whose analysis names the signal, the outcome and
the number of groups. Returns the script's result plus the metric the
design compares, the spread between the top and bottom groups.
"""
from __future__ import annotations
import hashlib
import json
from examples.signal_groups.signal_groups import analyze


def canonical(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def calculate(inputs):
    docs = [x for x in inputs if x['kind'] == 'OBSERVATION']
    designs = [x for x in inputs if x['kind'] == 'RESEARCH_RECORD' and x['body'].get('kind') == 'EXPERIMENT DESIGN']
    if len(designs) != 1 or not docs: raise ValueError('INVALID_INPUT')
    design = designs[0]; spec = design['body'].get('analysis') or {}
    if spec.get('kind') != 'signal-groups': raise ValueError('UNSUPPORTED_ANALYSIS')
    rows = [r for d in docs for r in d['body']['document'].get('rows', [])]
    result = analyze(rows, spec['signal'], spec['outcome'], int(spec.get('groups', 3)))
    cls = 'historical' if any(d['body'].get('class') == 'historical' for d in docs) else 'synthetic'
    return dict(result, analysis=spec, metric=result['spread_top_minus_bottom_bp'], n=result['rows_used'],
                inputs=[{'seq': d['seq'], 'sha256': d['sha256']} for d in docs], design={'seq': design['seq'], 'sha256': design['sha256']},
                input_sha256=hashlib.sha256(canonical([d['body']['document'] for d in docs])).hexdigest(), **{'class': cls}, synthetic=cls == 'synthetic')
