"""The researcher's declared rule for what to investigate next, read from the conclusion and the history.

Candidates depend on the conclusion state. A candidate rejected earlier
under the same direction stays out of the live set while its reconsideration
condition is unmet, and returns when the condition is met. The selection
record names the earlier records that shaped the set. The evaluator applies
the same rule to verify a selection followed it; that is consistency with
the declared rule, not independent judgment about the science.
"""
from __future__ import annotations
from copy import deepcopy

BASE = {
    'MET': [
        {'id': 'other-horizon', 'question': 'Does the spread hold for a different outcome horizon?', 'why': 'One horizon is one view of the same signal.', 'reconsider_when': 'new_documents'},
        {'id': 'finer-groups', 'question': 'Is the spread carried by the extremes or spread across the ranking?', 'why': 'Terciles hide where the relation lives.', 'reconsider_when': 'new_documents'},
        {'id': 'placebo-signal', 'question': 'Does a signal that should carry nothing show a spread of the same size?', 'why': 'A spread the placebo also shows is not evidence for the signal.', 'reconsider_when': 'new_direction'}],
    'NOT_MET': [
        {'id': 'coarser-groups', 'question': 'Does a two-group split show the relation the terciles did not?', 'why': 'The expectation may be sharper than the data allows.', 'reconsider_when': 'new_documents'},
        {'id': 'other-signal', 'question': 'Does another signal in the table do better on the same outcome?', 'why': 'The question may be right and the signal wrong.', 'reconsider_when': 'new_direction'},
        {'id': 'reject', 'question': 'Record the conclusion as rejected and ask a different question.', 'why': 'The evidence went against the expectation.', 'reconsider_when': 'never'}],
    'INCONCLUSIVE': [
        {'id': 'add-rows', 'question': 'Does the result change with more rows?', 'why': 'Fewer rows than the design required.', 'reconsider_when': 'new_documents'},
        {'id': 'relax-minimum', 'question': 'Is a smaller minimum defensible for this question?', 'why': 'The minimum was set before seeing how many rows exist.', 'reconsider_when': 'never'}],
}


def live_set(state, history):
    """history: list of {'seq', 'theme', 'rejections': [{'id','reason','reconsider_when'}], 'documents_after': bool} for earlier selections.

    current: {'theme': str}. Returns (candidates, excluded, reinstated), each a list.
    """
    base = deepcopy(BASE.get(state, [])); excluded = []; reinstated = []
    for cand in list(base):
        prior = [h for h in history if any(r['id'] == cand['id'] for r in h['rejections'])]
        if not prior: continue
        last = prior[-1]; rej = next(r for r in last['rejections'] if r['id'] == cand['id'])
        cond = rej.get('reconsider_when', cand['reconsider_when'])
        met = (cond == 'new_documents' and last['documents_after']) or (cond == 'new_direction' and last['theme'] != history_current_theme(history)) or cond == 'always'
        if met: reinstated.append({'id': cand['id'], 'rejected_in': last['seq'], 'condition': cond}); continue
        if cond == 'never' and rej['id'] == 'reject':
            continue   # rejecting is always available
        excluded.append({'id': cand['id'], 'rejected_in': last['seq'], 'reason': rej['reason'], 'condition': cond}); base.remove(cand)
    return base, excluded, reinstated


def history_current_theme(history):
    return history[-1].get('current_theme') if history else None


def gather_history(records, documents, current_theme):
    """Earlier SELECTION records of this researcher, with whether documents arrived after each and the direction they were made under."""
    out = []
    for s in records:
        body = s['body']['result']; later = any(d['seq'] > s['seq'] for d in documents)
        out.append({'seq': s['seq'], 'theme': body.get('theme'), 'current_theme': current_theme, 'rejections': body.get('rejections', []), 'documents_after': later})
    return out
