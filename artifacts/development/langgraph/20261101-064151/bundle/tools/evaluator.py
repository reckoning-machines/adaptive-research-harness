"""CHECK-H-1: the team's evaluator, run under the Checker identity.

Uses the client checking toolkit for the common and class criteria and
supplies the one experiment-specific validator: recompute the join of the
recorded labels to the committed returns. That verifies the arithmetic and
the join. It does not verify the labels, which only the provider produced.
"""
from __future__ import annotations
from arh_client.checking import evaluate as toolkit_evaluate
from arh_client.protocol import digest


def recompute(ctx):
    docs = ctx['documents']; records = ctx['records']; proposer = ctx['proposer']; ev = ctx['evidence']
    headlines = next((d for d in docs if 'headline' in d['body']['document']['rows'][0]), None)
    returns = next((d for d in docs if 'next_day_return_bp' in d['body']['document']['rows'][0]), None)
    labels_rec = next((r for r in records if 'labels' in (r['body'].get('result') or {})), None)
    joined = records[-1]
    if not (headlines and returns and labels_rec) or joined is labels_rec: return False
    if labels_rec['actor'] != proposer or joined['actor'] != proposer: return False
    if labels_rec['body'].get('failure') or joined['body'].get('failure'): return False
    lab = labels_rec['body']['result']; res = joined['body']['result']
    if lab['input_sha256'] != digest(headlines['body']['document']): return False
    if labels_rec['body']['reproducibility']['result_hash'] != digest(lab) or joined['body']['reproducibility']['result_hash'] != digest(res): return False
    # The labels rest on a funded attempt that was settled; the arithmetic is not accepted on an unsettled claim.
    attempt = labels_rec['body']['attempt']
    if not any(e['kind'] == 'SETTLEMENT' and e['body']['attempt'] == attempt for e in ev.values()): return False
    rows = {r['row_id']: r['next_day_return_bp'] for r in returns['body']['document']['rows']}
    ids = {r['row_id'] for r in headlines['body']['document']['rows']}
    if set(rows) != ids or {x['row_id'] for x in lab['labels']} != ids: return False
    bull = [x['row_id'] for x in lab['labels'] if x['label'] == 'bullish']; bear = [x['row_id'] for x in lab['labels'] if x['label'] == 'bearish']
    expected = {'n_bullish': len(bull), 'k_bullish_up': sum(1 for i in bull if rows[i] > 0), 'n_bearish': len(bear), 'k_bearish_down': sum(1 for i in bear if rows[i] < 0)}
    if any(res.get(k) != v for k, v in expected.items()): return False
    if res.get('passes') != (expected['n_bullish'] > 0 and 5 * expected['k_bullish_up'] >= 3 * expected['n_bullish']): return False
    if res.get('labels_record', {}).get('sequence') != labels_rec['seq'] or res['labels_record'].get('sha256') != labels_rec['sha256']: return False
    return True


def evaluate(snapshot, transition_id, actor, grant, attempt, profile):
    return toolkit_evaluate(snapshot, transition_id, actor, grant, attempt, profile, recompute=recompute)
