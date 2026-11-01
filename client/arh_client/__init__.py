"""Client for the Adaptive Research Harness local host.

Public, stable:
    connect, Connection, Outcome, Ref, HarnessError, RefusedError
    Researcher, Execution, ReceiptStore
    Checker, CheckResult
    Principal, Observer, startup
    HostControl
    langgraph_adapter (ExperimentSpec, build_research_graph, build_proposal_graph)
    analysis (AnalysisResearcher, CandidateRule, Inputs, host_tool, evaluator, persisted_keys)
    api (connect, Research, Result, Proposal, Review, Refusal, Evaluator, Owner, Importer)
    langgraph_nodes (Nodes, GraphState), reached as research.langgraph
    project (Project), operations (OperationStore), refusals (explain), dev (up, down)

Internal helpers (may change): arh_client.protocol, arh_client.checking.evaluate,
arh_client.research.invocation and event_ref, arh_client.principal.row_ratio.
Standard library only. Nothing here holds authority: every command is admitted
or refused by the core.
"""
from .protocol import HarnessError, canonical, decode, digest, units, amount
from .results import Outcome, Ref, RefusedError
from .connection import Connection, connect
from .research import Researcher, Execution, ReceiptStore, event_ref, invocation
from .checking import Checker, CheckResult, evaluate, run_check
from .principal import Principal, Observer, startup, historical_document
from .host import HostControl

__all__ = ['connect', 'Connection', 'Outcome', 'Ref', 'HarnessError', 'RefusedError', 'Researcher', 'Execution', 'ReceiptStore',
           'Checker', 'CheckResult', 'Principal', 'Observer', 'startup', 'historical_document', 'HostControl',
           'canonical', 'decode', 'digest', 'units', 'amount', 'event_ref', 'invocation', 'evaluate', 'run_check']
__version__ = '0.1.0'
