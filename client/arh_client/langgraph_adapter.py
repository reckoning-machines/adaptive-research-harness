"""LangGraph graphs over the governed lifecycle. LangGraph is imported only when a graph is built.

The adapter supplies the node functions and the state schema. The team
supplies an ExperimentSpec: which step and tool to run, how to call its
provider, how to build its research record, and optionally how to derive a
later record and propose from it. Request keys are generated in the first
node and checkpointed before any node that uses them. Permission to execute
is the fresh PERMISSION_CONSUMED reply inside the execute node; it is never
placed in graph state.
"""
from __future__ import annotations
from typing import Annotated, Any, Callable, TypedDict
import operator
from .connection import Connection
from .research import Researcher, Execution, ReceiptStore, event_ref, expected_maximum, amount
from .protocol import HarnessError

KEYS = ('reserve', 'attempt', 'settle', 'record', 'close', 'derive', 'propose', 'fund')


class GovernedState(TypedDict, total=False):
    """Graph state carried through every node. Ledger references and keys live here; permission never does."""
    job: str
    options: dict
    keys: dict
    formation: dict
    reservation: int
    attempt: int
    attempt_input_hash: str
    maximum: str
    execution: str
    receipt: dict
    record: dict
    settlement: dict
    closed: bool
    derived: dict
    proposal: dict
    status: str
    reason: str
    log: list


class GraphState(GovernedState, total=False):
    log: Annotated[list, operator.add]


class ExperimentSpec:
    """What the team supplies. Each callable receives the Researcher and the current state."""
    def __init__(self, *, step: str, tool: str, parameters: dict, purpose: dict, reserve_amount: str, source: str,
                 provider: Callable[[dict, dict, dict], tuple], provider_lookup: Callable[[int, str], Any] | None,
                 build_record: Callable[[Researcher, GovernedState, dict], dict], question: str,
                 derive: Callable[[Researcher, GovernedState], dict] | None = None,
                 build_proposal: Callable[[Researcher, GovernedState], dict] | None = None, proposal_budget: str | None = None,
                 hook: Callable[[str], None] = lambda point: None):
        self.step = step; self.tool = tool; self.parameters = parameters; self.purpose = purpose; self.reserve_amount = reserve_amount; self.source = source
        self.provider = provider; self.provider_lookup = provider_lookup; self.build_record = build_record; self.question = question
        self.derive = derive; self.build_proposal = build_proposal; self.proposal_budget = proposal_budget; self.hook = hook


def _refused(r): return not r.ok


def research_nodes(researcher: Researcher, spec: ExperimentSpec, store: ReceiptStore):
    """Node functions for the metered research job: prepare, reserve, attempt, execute, report."""
    def prepare(state):
        keys = state.get('keys') or {k: Connection.new_key() for k in KEYS}
        doc = researcher.formation(spec.source, (state.get('options') or {}).get('item_id'))
        return {'keys': keys, 'formation': event_ref(doc), 'status': 'prepared', 'log': [f'inputs: {spec.source} E{doc["seq"]}']}
    def reserve(state):
        o = state.get('options') or {}
        r = researcher.reserve(o.get('reserve_amount', spec.reserve_amount), spec.purpose, state['keys']['reserve'])
        if _refused(r): return {'status': 'refused', 'reason': r.reason, 'log': [f'reserve refused {r.reason}']}
        return {'reservation': r.sequence, 'status': 'reserved', 'log': [f'reservation E{r.sequence}']}
    def attempt(state):
        doc = researcher.c.get(state['formation']); rows = doc['body']['document'].get('rows', [])
        maximum = amount(expected_maximum(researcher.step(spec.step), len(rows)))
        r = researcher.attempt(state['reservation'], spec.step, spec.tool, [state['formation']], spec.parameters, maximum, state['keys']['attempt'])
        if _refused(r): return {'status': 'refused', 'reason': r.reason, 'maximum': maximum, 'log': [f'attempt refused {r.reason}']}
        return {'attempt': r.sequence, 'attempt_input_hash': r.input_hash, 'maximum': maximum, 'status': 'attempted', 'log': [f'attempt E{r.sequence} maximum {maximum}']}
    def execute(state):
        ex = Execution(researcher, state['attempt'], state['attempt_input_hash'], spec.tool, state['maximum'])
        doc = researcher.c.get(state['formation'])['body']['document']
        outcome = ex.run(lambda claim: spec.provider(doc, spec.parameters, claim), store, spec.provider_lookup, spec.hook)
        out = {'execution': outcome['status'], 'log': [f'execution {outcome["status"]}']}
        if 'receipt' in outcome: out['receipt'] = outcome['receipt']
        return out
    def report(state):
        ex = Execution(researcher, state['attempt'], state['attempt_input_hash'], spec.tool, state['maximum'])
        if state.get('execution') == 'uncertain':
            s = ex.settle_unknown(state['keys']['settle'])
            body = researcher.record_body(state['attempt'], spec.question, None, 'RESPONSE_LOST', [state['formation']],
                                          claims=[{'kind': 'ASSUMPTION', 'text': 'Permission was consumed and no receipt exists anywhere; execution may have occurred; liability kept at the admitted maximum'}])
            rec = researcher.research_commit(body, state['keys']['record'])
            return {'settlement': s.raw, 'record': rec.raw, 'status': 'reconciled', 'log': [f'settled UNKNOWN at {state["maximum"]}; negative record committed']}
        receipt = state['receipt']; body = spec.build_record(researcher, state, receipt)
        rec = researcher.research_commit(body, state['keys']['record'])
        s = ex.settle(receipt, state['keys']['settle'])
        c = researcher.close(state['reservation'], state['keys']['close'])
        ok = rec.ok and s.ok
        return {'record': rec.raw, 'settlement': s.raw, 'closed': c.ok, 'status': 'recorded' if ok else 'failed', 'reason': None if ok else rec.reason or s.reason,
                'log': [f'record {rec.status} settlement {s.status} actual {receipt["actual"]}']}
    return {'prepare': prepare, 'reserve': reserve, 'attempt': attempt, 'execute': execute, 'report': report}


def proposal_nodes(researcher: Researcher, spec: ExperimentSpec):
    """Node functions for the later job: derive a record from committed evidence, propose and fund."""
    def prepare(state):
        keys = state.get('keys') or {k: Connection.new_key() for k in KEYS}; return {'keys': keys, 'status': 'prepared'}
    def derive(state):
        body = spec.derive(researcher, state)
        if body is None: return {'status': 'no_candidate', 'log': ['no candidate']}
        r = researcher.research_commit(body, state['keys']['derive'])
        if _refused(r): return {'status': 'failed', 'reason': r.reason, 'log': [f'derived record refused {r.reason}']}
        return {'derived': r.ref.as_dict(), 'status': 'derived', 'log': [f'derived record E{r.sequence}']}
    def propose(state):
        content = spec.build_proposal(researcher, state)
        r = researcher.propose_hypothesis(content, spec.proposal_budget, state['keys']['propose'], state['keys']['fund'])
        if _refused(r): return {'status': 'failed', 'reason': r.reason, 'log': [f'proposal refused {r.reason}']}
        funded = r.raw.get('funded', False)
        return {'proposal': {'transition_id': r.transition_id, 'funding_ref': r.raw.get('funding_ref'), 'funded': funded, 'funding_reason': r.raw.get('funding', {}).get('reason')},
                'status': 'proposed' if funded else 'stranded', 'log': [f'proposed {r.transition_id} funded {funded}']}
    return {'prepare': prepare, 'derive': derive, 'propose': propose}


def build_research_graph(researcher: Researcher, spec: ExperimentSpec, store: ReceiptStore, checkpointer=None):
    from langgraph.graph import StateGraph, START, END
    State = GraphState
    nodes = research_nodes(researcher, spec, store); g = StateGraph(State)
    for name, fn in nodes.items(): g.add_node(name, fn)
    g.add_edge(START, 'prepare'); g.add_edge('prepare', 'reserve')
    g.add_conditional_edges('reserve', lambda s: 'attempt' if s.get('status') == 'reserved' else END, {'attempt': 'attempt', END: END})
    g.add_conditional_edges('attempt', lambda s: 'execute' if s.get('status') == 'attempted' else END, {'execute': 'execute', END: END})
    g.add_edge('execute', 'report'); g.add_edge('report', END)
    return g.compile(checkpointer=checkpointer)


def build_proposal_graph(researcher: Researcher, spec: ExperimentSpec, checkpointer=None):
    from langgraph.graph import StateGraph, START, END
    State = GraphState
    nodes = proposal_nodes(researcher, spec); g = StateGraph(State)
    for name, fn in nodes.items(): g.add_node(name, fn)
    g.add_edge(START, 'prepare'); g.add_edge('prepare', 'derive')
    g.add_conditional_edges('derive', lambda s: 'propose' if s.get('status') == 'derived' else END, {'propose': 'propose', END: END})
    g.add_edge('propose', END)
    return g.compile(checkpointer=checkpointer)
