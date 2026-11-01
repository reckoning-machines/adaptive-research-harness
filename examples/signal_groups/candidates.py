"""The researcher's declared rule for what to investigate next. The table is the decision; the machinery is the client's.

A candidate rejected under one selection stays out of later sets until its
reconsideration condition is met: new_documents, new_direction, always or
never. The choice to record a conclusion as rejected is always available.
"""
from arh_client.analysis import CandidateRule

TABLE = {
    'MET': [
        {'id': 'other-horizon', 'question': 'Does the spread hold for a different outcome horizon?', 'why': 'One horizon is one view of the same signal.', 'reconsider_when': 'new_documents'},
        {'id': 'finer-groups', 'question': 'Is the spread carried by the extremes or spread across the ranking?', 'why': 'Terciles hide where the relation lives.', 'reconsider_when': 'new_documents'},
        {'id': 'placebo-signal', 'question': 'Does a signal that should carry nothing show a spread of the same size?', 'why': 'A spread the placebo also shows is not evidence for the signal.', 'reconsider_when': 'new_direction'}],
    'NOT_MET': [
        {'id': 'coarser-groups', 'question': 'Does a two-group split show the relation the terciles did not?', 'why': 'The expectation may be sharper than the data allows.', 'reconsider_when': 'new_documents'},
        {'id': 'other-signal', 'question': 'Does another signal in the table do better on the same outcome?', 'why': 'The question may be right and the signal wrong.', 'reconsider_when': 'new_direction'},
        {'id': 'reject', 'question': 'Record the conclusion as rejected and ask a different question.', 'why': 'The evidence went against the expectation.', 'reconsider_when': 'never', 'always_available': True}],
    'INCONCLUSIVE': [
        {'id': 'add-rows', 'question': 'Does the result change with more rows?', 'why': 'Fewer rows than the design required.', 'reconsider_when': 'new_documents'},
        {'id': 'relax-minimum', 'question': 'Is a smaller minimum defensible for this question?', 'why': 'The minimum was set before seeing how many rows exist.', 'reconsider_when': 'never'}],
}

RULE = CandidateRule(TABLE)
