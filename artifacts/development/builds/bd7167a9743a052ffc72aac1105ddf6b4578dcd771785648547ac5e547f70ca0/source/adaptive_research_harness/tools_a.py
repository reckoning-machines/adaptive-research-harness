"""Synthetic calculator A: direct row iteration, with explicit simulated charge."""
from .encoding import canonical, raw_digest, Refusal


def calculate(document):
    raw=canonical(document)
    if len(raw)>16777216:raise Refusal('INPUT_TOO_LARGE')
    rows=document.get('rows')
    if not isinstance(rows,list) or len(rows)>4096:raise Refusal('INVALID_INPUT')
    counts=dict(n=0,k=0,n_large=0,k_large=0);seen=set()
    for r in rows:
        if not isinstance(r,dict) or not isinstance(r.get('event_id'),str) or r['event_id'] in seen:
            raise Refusal('INVALID_INPUT')
        seen.add(r['event_id'])
        if type(r.get('spike')) is not bool or type(r.get('selling')) is not bool or type(r.get('size_units')) is not int or not 0<=r['size_units']<=10:
            raise Refusal('INVALID_INPUT')
        if r['spike']:
            counts['n']+=1;counts['k']+=int(r['selling'])
            if r['size_units']>=2:counts['n_large']+=1;counts['k_large']+=int(r['selling'])
    return dict(counts,input_sha256=raw_digest(raw),synthetic=True)
