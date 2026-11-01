"""CHECK-M-1: the evaluator under the Checker identity. What counts as a valid result is recompute; the record checks are the client's."""
from arh_client.analysis import evaluator
from examples.memo_returns.tools import join


def recompute(inputs, spec, result):
    again = join(inputs, spec)
    return all(result.get(k) == again[k] for k in ('column', 'n', 'k', 'metric', 'per_memo', 'memos_scored'))


evaluate = evaluator(recompute, None, kind='tone-return-join')
