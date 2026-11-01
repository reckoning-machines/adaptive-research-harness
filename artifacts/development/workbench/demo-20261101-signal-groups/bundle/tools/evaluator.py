"""CHECK-S-1: the evaluator under the Checker identity.

What counts as a valid result is recompute: the same script re-run on the
committed rows and design gives the recorded spread, row count and groups.
The record checks, the design before the attempt, the settlement, the
cited inputs, the conclusion against the expectation and the candidate set
against the declared rule, are the client's. This checks reproducibility
and record integrity, not the research method.
"""
from arh_client.analysis import evaluator
from examples.signal_groups.signal_groups import analyze
from examples.signal_groups.candidates import RULE


def recompute(rows, spec, result):
    again = analyze(rows, spec['signal'], spec['outcome'], int(spec.get('groups', 3)))
    return result['metric'] == again['spread_top_minus_bottom_bp'] and result['n'] == again['rows_used'] and result['groups'] == again['groups']


evaluate = evaluator(recompute, RULE, kind='signal-groups')
