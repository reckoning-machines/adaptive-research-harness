"""TONE-JOIN-1: the host-run tool. The join, and the one call that connects it. Research code."""
from __future__ import annotations
from arh_client.analysis import host_tool


def join(inputs, spec):
    """Over positive-tone memos, the fraction followed by a positive value of the design's return column. Exact ratio."""
    column = spec.get('column', 'next_day_bp'); returns = {r['memo_id']: r[column] for r in inputs.rows}
    scores = [r for r in inputs.results if r and 'tone' in r]
    per_memo = [{'memo_id': s['memo_id'], 'tone': s['tone'], 'return_bp': returns.get(s['memo_id'])} for s in scores]
    positive = [s for s in scores if s['tone'] > 0]
    k = sum(1 for s in positive if isinstance(returns.get(s['memo_id']), int) and returns[s['memo_id']] > 0); n = len(positive)
    return {'column': column, 'n': n, 'k': k, 'metric': {'numerator': k, 'denominator': n}, 'per_memo': per_memo, 'memos_scored': len(scores)}


calculate = host_tool(join, kind='tone-return-join')
