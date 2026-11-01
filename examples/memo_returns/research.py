"""The research code: what to score, what to expect, how to join, and what to ask next.

A scientist wrote this and nothing else about ARH. The lifecycle around
each piece of work is the client's. The scoring node makes one metered
call per memo and is otherwise an uncharged grouping. The two joins are
one metered attempt each. The selection names the scientist's own next
question; no candidate table is used.
"""
from __future__ import annotations
from arh_client.analysis import AnalysisResearcher
from arh_client.api import Result
from examples.memo_returns.provider import score

MEMOS = 'SRC-MEMO-SYN'; RETURNS = 'SRC-RET-SYN'; BUDGET = 'memo-tests'
EXPECT_JOIN = {'comparator': '>=', 'value': {'numerator': 1, 'denominator': 2}, 'minimum_n': 3, 'statement': 'at least half of the positive-tone memos are followed by a positive next-day return'}
EXPECT_PLACEBO = {'comparator': '<=', 'value': {'numerator': 1, 'denominator': 2}, 'minimum_n': 3, 'statement': 'positive tone shows no such relation to the prior-day return, which it cannot have caused'}
JOIN_QUESTION = 'Do positive-tone memos precede positive next-day returns?'
PLACEBO_QUESTION = 'Does positive tone relate to the prior-day return, which it cannot have caused?'


def researcher(connection): return AnalysisResearcher(connection)


def score_node(research, hook=lambda point: None):
    """One metered call per memo, each with its own identity. A resumed node finds the calls already made in the journal and repeats none."""
    def node(state):
        results = []
        for i, doc in enumerate(research.documents(MEMOS), 1):
            op = f"score/{doc['name']}"
            r = research.langgraph.call(score, [doc], operation=op, budget=BUDGET, question=f"What is the tone of {doc['name']}?")
            if r.status == 'uncertain':
                # The call may have run or may still be running. Replacement is explicit and the host must first confirm this process's predecessor is gone.
                r = research.retry(op, score)
                if not r.ok: raise RuntimeError(f'{op} is uncertain and its replacement was refused: {r.refusal}')
            results.append(r.as_state()); hook(f'after_call_{i}')
        status = 'recorded' if results and all(x['status'] == 'recorded' for x in results) else 'incomplete'
        return {'arh': {'score': {'kind': 'calls', 'status': status, 'results': results}}}
    return node


def join_inputs(state):
    """The returns table and every tone record the scoring node produced."""
    return [RETURNS] + [Result.from_state(x) for x in state['arh']['score']['results']]


def choose_next(state):
    """The scientist's next question, from both results. No candidate table; the choice is 'own'."""
    join = Result.from_state(state['arh']['join']); placebo = Result.from_state(state['arh']['placebo'])
    if join.state == 'MET' and placebo.state == 'MET':
        return {'result': 'join', 'chosen': 'own', 'reason': f'tone separates next-day returns ({join.metric}) and the placebo does not ({placebo.metric})', 'question': 'Does the tone relation hold on memos from the next quarter, scored before their returns are known?'}
    if join.state == 'MET':
        return {'result': 'join', 'chosen': 'own', 'reason': 'the placebo shows a relation too, so the memos may carry information about the past rather than the future', 'question': 'Is the tone relation a property of the memos rather than of the returns?'}
    return {'result': 'join', 'chosen': 'own', 'reason': f'the expectation was not met ({join.state})', 'question': 'Does a different lexicon or a longer horizon change the result?'}
