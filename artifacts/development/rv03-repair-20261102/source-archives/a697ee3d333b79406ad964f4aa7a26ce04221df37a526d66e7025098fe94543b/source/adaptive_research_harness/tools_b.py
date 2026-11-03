"""Synthetic calculator B: independent set implementation; never imports A."""
from .encoding import canonical, raw_digest, Refusal


def calculate(document):
    raw=canonical(document);rows=document.get('rows')
    if len(raw)>16777216:raise Refusal('INPUT_TOO_LARGE')
    if not isinstance(rows,list) or len(rows)>4096:raise Refusal('INVALID_INPUT')
    try:
        ids=[r['event_id'] for r in rows]
        if not all(isinstance(x,str) for x in ids) or len(set(ids))!=len(ids):raise Refusal('INVALID_INPUT')
        if not all(type(r['spike']) is bool and type(r['selling']) is bool and
                   type(r['size_units']) is int and 0<=r['size_units']<=10 for r in rows):raise Refusal('INVALID_INPUT')
        a={r['event_id'] for r in rows if r['spike']}
        b={r['event_id'] for r in rows if r['selling']}
        c={r['event_id'] for r in rows if r['size_units']>=2}
    except (KeyError,TypeError) as exc:raise Refusal('INVALID_INPUT') from exc
    return {'n':len(a),'k':len(a&b),'n_large':len(a&c),'k_large':len(a&b&c),
            'input_sha256':raw_digest(raw),'synthetic':True}
