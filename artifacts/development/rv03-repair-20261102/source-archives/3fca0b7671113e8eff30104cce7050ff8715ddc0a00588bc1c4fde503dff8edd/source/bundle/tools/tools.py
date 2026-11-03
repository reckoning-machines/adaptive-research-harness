"""Independent deterministic evaluator for the RV-03 public-host regressions."""
from arh_client import evaluate as evaluate_criteria


def evaluate(snapshot, transition_id, actor, grant, attempt, profile):
    return evaluate_criteria(snapshot, transition_id, actor, grant, attempt, profile)


def calculate(*args, **kwargs):
    raise AssertionError('The negative step-kind fixture does not run research')


def researcher(*args, **kwargs):
    raise AssertionError('No researcher program runs in the Checker regression')
