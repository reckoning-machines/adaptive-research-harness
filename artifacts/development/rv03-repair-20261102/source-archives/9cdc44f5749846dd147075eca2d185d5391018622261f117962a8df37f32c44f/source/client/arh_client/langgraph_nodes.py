"""LangGraph nodes over the everyday interface. LangGraph is imported only where a graph pauses.

    research = arh_client.api.connect(project=..., run=...)
    graph.add_node('join', research.langgraph.analysis(join, inputs=..., expectation=..., budget='memo-tests', operation='join'))
    graph.add_node('next', research.langgraph.selection(choose, operation='next'))
    graph.add_node('review', research.langgraph.review('next'))

Every node writes one namespace in graph state, state['arh'][operation],
and namespaces merge by operation, so two analyses in one graph or one
analysis in parallel branches never overwrite each other. The identity is
the research code's, given as a string or a function of the state;
nothing relies on a LangGraph branch key. The durable record of what a
node did lives in the researcher's operation journal, not in the
checkpoint: a node killed before its first return finds its own attempt
there on restart and recovers rather than repeats. A node wrapped as an
analysis is one metered attempt. A node that makes calls through call()
is an uncharged grouping; each call is its own attempt with its own
identity. Reading a review decides nothing; a resumed graph approves
nothing.
"""
from __future__ import annotations
from typing import Annotated, TypedDict
from .protocol import require
from .api import Result, Proposal


def merge_operations(a, b):
    out = dict(a or {})
    for k, v in (b or {}).items(): out[k] = {**out.get(k, {}), **(v or {})}
    return out


class GraphState(TypedDict, total=False):
    arh: Annotated[dict, merge_operations]


def operation_of(state, operation):
    op = operation(state) if callable(operation) else operation; require(isinstance(op, str) and op, 'OPERATION_REQUIRED', 'an operation needs an identity'); return op


def _value(x, state): return x(state) if callable(x) else x


class Nodes:
    def __init__(self, research): self.research = research

    def analysis(self, fn, inputs, expectation=None, budget=None, operation=None, question=None, spec=None, theme=None, revises=None, hook=None):
        """A node that runs one metered analysis and writes its Result under its operation."""
        require(operation, 'OPERATION_REQUIRED', 'give the analysis a stable identity')
        def node(state):
            op = operation_of(state, operation)
            r = self.research.run_analysis(op, fn, _value(inputs, state), _value(expectation, state), question, _value(spec, state), budget, theme, _value(revises, state), hook)
            return {'arh': {op: r.as_state()}}
        node.__name__ = f'analysis[{operation if isinstance(operation, str) else "dynamic"}]'; return node

    def call(self, fn, inputs, operation, budget=None, question='', tool=None, hook=None):
        """Inside a node you write: one metered call with its own identity. Returns a Result; the node decides what to keep in state."""
        return self.research.call(fn, inputs, operation, budget, question, tool, hook)

    def result(self, state, operation):
        """The Result an earlier node wrote under an operation."""
        d = (state.get('arh') or {}).get(operation); require(d is not None, 'NO_RESULT', f'no result under {operation}'); return Result.from_state(d)

    def selection(self, choose, operation, budget=None, theme=None):
        """A node that records the next investigation. choose(state) returns {'result', 'chosen', 'reason', 'question'}; result is an operation name or a Result."""
        def node(state):
            op = operation_of(state, operation); c = choose(state)
            res = c['result'] if isinstance(c['result'], Result) else self.result(state, c['result'])
            p = self.research.select(res, c.get('chosen', 'own'), c['reason'], c['question'], op, budget, theme)
            return {'arh': {op: p.as_state()}}
        node.__name__ = f'selection[{operation}]'; return node

    def review(self, operation, pause=True, until='applied'):
        """A node that reads where the proposal under operation stands.

        With pause, the graph interrupts while the proposal is waiting for review, and again while it is decided but
        not yet applied when until is 'applied', since a decision is not an application. Resuming re-reads the
        ledger and decides nothing. A failed check or a rejection ends the wait.
        """
        def waiting(rv): return rv.status == 'waiting_for_review' or (until == 'applied' and rv.status == 'decided' and rv.decision == 'ADMITTED')
        def node(state):
            d = (state.get('arh') or {}).get(operation) or {}; tr = d.get('transition'); require(tr, 'NO_PROPOSAL', f'{operation} has no proposal')
            rv = self.research.review(tr)
            while pause and waiting(rv):
                # Each resume answers one interrupt; the ledger is re-read and, if nothing changed, the graph pauses again.
                from langgraph.types import interrupt
                interrupt({'operation': operation, 'transition': tr, 'review': rv.status, 'decision': rv.decision,
                           'note': 'Waiting for an independent check, a Principal decision and its application. Resuming re-reads the ledger; it approves nothing.'})
                rv = self.research.review(tr)
            return {'arh': {operation: {**d, **rv.as_dict()}}}
        node.__name__ = f'review[{operation}]'; return node

    def await_review(self, operation):
        """A conditional-edge function: 'applied', 'decided', 'check_failed' or 'waiting_for_review' for the proposal under operation."""
        def route(state):
            d = (state.get('arh') or {}).get(operation) or {}; return d.get('review') or self.research.review(d['transition']).status
        return route

    def retry(self, operation, hook=None):
        """A node that replaces the uncertain attempt under operation, after the host has confirmed quiescence."""
        def node(state):
            r = self.research.retry(operation, hook); return {'arh': {operation: r.as_state()}}
        node.__name__ = f'retry[{operation}]'; return node
