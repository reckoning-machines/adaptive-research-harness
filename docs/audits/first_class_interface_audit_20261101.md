# Interface Audit - A First-Class Interface for Research Code and LangGraph

Status: **AUDIT EVIDENCE - A DESIGN PROPOSAL CHECKED AGAINST THE REPOSITORY, WITH FINDINGS. AUTHORIZES NOTHING.**

Date: 2026-11-01. Auditor: Claude (Fable 5.1), checking a design
discussion the Principal forwarded against the repository at `9642c29`.
The discussion proposes a world-class interface to ARH from LangGraph and
ordinary research code, structured so that data scientists write research
code and ARH handles the controls around it. The proposal is quoted where
its claims are checked. Each finding names the code that would change.

## 1. Disposition

The proposal is sound and mostly consistent with what the repository
already enforces. Its three layers exist in outline. Its everyday
interface does not exist. The LangGraph adapter recovers an interrupted
attempt correctly for one sequential graph and nothing more. Four of the
proposal's requirements are met by the core today and must be kept as
they are. Seven are gaps in the client and the adapter. One is a limit of
the trust model that no interface can remove and that the interface must
state.

## 2. The proposal

"A first-class interface would let data scientists keep writing ordinary
research code and ordinary LangGraph graphs. ARH would handle the research
controls around them. They should understand what they are authorizing
and checking without having to implement reservations, receipts or
recovery." Three layers: research code for data scientists, integration
adapters that are maintained, and the core for ARH maintainers. "Your
existing client and new analysis.py are the foundation of the middle
layer." The everyday interface should revolve around research concepts.
A scientist supplies an analysis function, its inputs, an expectation and
an evaluator and receives the result, its evidence reference, its check
status and any refusal. Administrative setup comes from a reusable project
configuration. The illustrative shape:

```python
research = arh.connect(project="signal-research")
graph.add_node("test_signal", research.langgraph.analysis(run_backtest, inputs=backtest_inputs, expectation=expected_result, budget="signal-tests"))
graph.add_node("submit_result", research.langgraph.proposal(make_proposal))
```

The evaluator is registered separately under its own identity. The
adapter must understand execution, recognize the original attempt on
resume and recover its receipt before deciding whether any execution is
permitted, handle parallel branches, distinguish a new experiment from a
retry, translate outcomes into distinct graph states, and never treat a
resume as an approval. A node with five provider calls needs controls
around each call. Data scientists still code the scientific decisions, and
ARH offers history queries without requiring the candidate table or a
subclass. Ordinary functions, explanatory errors, results linked to
evidence, one-command local setup, and the lower-level client retained.
The test: connect a second, structurally different analysis through
LangGraph with mostly research code and a short configuration.

## 3. The three layers, as they stand

| Layer | Proposed owner | What exists at `9642c29` | Lines |
| --- | --- | --- | --- |
| Research code | Data scientists | Headline example: `build_record`, `derive`, `build_proposal` in `examples/langgraph_headlines/researcher.py`. Signal groups: the analysis function, the candidate table, `recompute`, in four files | 54 and 69 |
| Integration | Maintained adapters | `client/arh_client/`: `research.py` (lifecycle, `Execution.run`, `ReceiptStore`), `analysis.py` (design, run, candidates, selection, proposal, host-tool wrapper, evaluator record checks), `langgraph_adapter.py` (`ExperimentSpec`, five research nodes, three proposal nodes), `checking.py` (criteria toolkit, `Checker`), `principal.py`, `setup.py` (generator), `host.py` | 1508 |
| Core | ARH maintainers | `adaptive_research_harness/` with the local host; the core never imports experiment or client code | |

The middle layer is where the proposal says it should be. What it
exposes is the problem. `ExperimentSpec` takes a step, a tool, parameters,
a purpose, a reservation amount, a source, a provider callable, a record
builder and a question. Those are ARH's concepts. The proposal's node
takes a function, its inputs, an expectation and a budget name. Those are
research concepts. `analysis.py` is closer, with `design` taking a
question, an expectation and an analysis, but it is not reachable from a
graph, and its runner is the example's command line.

## 4. Claims checked against the code

**Evaluator separately registered under its own identity; attaching a
function to a graph does not let the graph approve its own output.** Met
by the core, not by the interface. `checking.evaluate` records
`independence` as not met unless the actor holds an active Checker grant
on a lineage other than the proposer's and holds no Research grant.
`rules.py` refuses a decision without a passing check at the current base
and refuses the proposer's own check. The headline example's demonstration
"a researcher refused when it tries to approve its own proposal" exercises
it. Nothing an adapter does can change this. The interface must say so
rather than implement it.

**The adapter must recognize the original attempt on resume and recover
its receipt before any execution is permitted.** Met for one sequential
graph. The `execute` node calls `Execution.run`, which claims permission
first. The core answers `PERMISSION_CONSUMED` only once per attempt; after
an interruption the answer is `RECEIPT`, `IN_PROGRESS_OR_UNCERTAIN` or
`UNKNOWN`, and `run` then looks for the receipt the host holds, then the
caller's durable store, then the provider's own record, and executes
nothing. Keys are made in `prepare` and checkpointed before use, so a
re-run node sends the same key and the core returns the original outcome.
The headline demonstration kills the job at three points and resumes each
without a second provider call. This is the piece the proposal most
wanted, and it is there.

**Parallel branches.** Not handled. `GovernedState` holds one
`reservation`, one `attempt`, one `receipt` and one `keys` dict with a
fixed set of names. Two analysis nodes in one graph, or one node in two
branches, would overwrite each other's state and send the same keys for
different work, which the core refuses as `REQUEST_KEY_CONFLICT`. Each
analysis needs its own namespace in state, keyed by node and branch.

**A deliberate new experiment versus a retry.** Not distinguished by the
adapter. Today a new LangGraph thread is a new experiment and the same
thread is a resume, by convention in `run_job`. `Researcher.retry` exists
in the client with the next dispatch index after quiescence, but no node
calls it. A retry is the same input hash under the same reservation; a
new experiment is a new design or new inputs and so a new input hash. The
adapter can tell them apart from the ledger and does not.

**Distinct graph states for waiting for review, budget exhausted and
execution uncertain.** Partly. The adapter's `status` values are
`prepared`, `reserved`, `attempted`, `refused`, `recorded`, `reconciled`,
`failed`, `derived`, `proposed`, `stranded` and `no_candidate`. Budget
exhaustion is `refused` with `reason` `BUDGET_EXCEEDED` or
`GRANT_EXHAUSTED`. Execution uncertainty is `reconciled`, after the
liability is settled at the maximum and a negative record committed.
Waiting for review has no state because the proposal graph ends at
`proposed` and nothing in the adapter reads the Transition ledger for a
check or a decision.

**Resuming a graph must not constitute an approval.** Met by the core.
Approval is a Principal decision under the Principal token, or policy
P-1 for routine registrations, and the adapter runs under the researcher
token, which cannot decide. A graph that resumes can at most re-send the
proposal key and get the original outcome. The adapter should state this
and test it; it does not today.

**A node with five provider calls needs controls around each call.** A
limit of the trust model, stated in the README and the architecture. One
attempt yields one permission and one receipt. Calls a researcher makes
inside a node are invisible to ARH, and the receipt is the caller's own
accounting. To account for each call, each must be its own attempt, with
its own claim and receipt, or the work must move to a tool the host runs.
The interface can make per-call attempts easy. It cannot discover
activity it is not told about, and must say so where it describes the
node wrapper.

**History queries and reusable patterns without the candidate table or a
subclass.** Partly. `AnalysisResearcher` takes `rule` as a constructor
argument, so a subclass is not required by the class. It is required by
the setup, because the generated design's `entrypoint` is loaded as a
class and constructed with a connection alone, in
`workbench/local_session.py`. The rule itself is required: `RULE_REQUIRED`
is raised without one, so a researcher who chooses the next question by
other means cannot use the class. History is reachable through
`Connection.history`, `Researcher.documents` and
`AnalysisResearcher.records`, as raw ledger records. There is no query
that answers "what did I conclude about this signal" or "which candidates
did I reject and why" without walking records.

**Ordinary functions should work without inheritance.** Met by
`host_tool` and `evaluator`, which take functions. Not met for the
researcher, as above.

**Errors should explain the failed operation and how to resolve it.**
Partly. Every refusal carries a code and a detail string and is preserved
on the ledger. The runbook's refusals table says what each code means and
what to do. The `Outcome` and `RefusedError` objects do not carry that
text, and the adapter's `reason` field is the code alone.

**Results should link directly to readable evidence and decisions.**
Partly. Every result carries a `Ref` with ledger, sequence and hash, and
the workbench pages render records by sequence. No result carries a path
or URL to the page that shows it.

**A local development setup should take one command.** Partly. The
workbench is one command. A host against an experiment directory is one
command. The experiment directory itself comes from `write_setup` called
by a hand-written `make_setup.py`, and the own-CSV command line writes one
for one example only. There is no command that takes a project
configuration and produces a running host with a setup.

**Advanced users should retain access to the lower-level client.** Met.
`Researcher`, `Execution`, `Checker`, `Principal`, `Observer` and
`Connection` are public and documented.

**Administrative setup from a reusable project configuration.** Not met.
Each example has its own `make_setup.py`. Budgets are amounts in grants,
not names. Actors are tokens in a connection file chosen by role name at
`connect`. The proposal's `budget="signal-tests"` needs a configuration
that maps a name to a grant, a purpose and a maximum.

## 5. The proposed test, costed today

Connecting a second, structurally different analysis through LangGraph
at `9642c29` would need, beyond the research code:

| Item | Today | Lines in the headline example |
| --- | --- | --- |
| An `ExperimentSpec` naming step, tool, parameters, purpose, amount, source, provider, record builder | hand written | 5 |
| A record builder that calls `record_body` with claims | hand written | 7 |
| A job runner opening the connection, the receipt store and the checkpointer and deciding resume by thread | hand written | 15 |
| A setup description through `write_setup` | hand written | 25 to 50 |
| An evaluator through `checking.evaluate` with a recompute function | hand written | 20 to 60 |
| A per-process entry with arguments | hand written | 10 |

About 80 to 150 lines that are not research code, and every one of them
is the same shape as the headline example's. That is the proposal's own
criterion for "more plumbing belongs in the adapter", and it is met.

## 6. Findings

| | Finding | Severity | Where it changes |
| --- | --- | --- | --- |
| F-1 | The everyday interface is expressed in ARH concepts, not research concepts | High | new `arh_client` module over `analysis.py` and `langgraph_adapter.py` |
| F-2 | No project configuration; budgets, actors and sources are repeated per example in code | High | new configuration file and loader; `setup.py` |
| F-3 | The adapter holds one attempt per graph; parallel branches collide | High | `langgraph_adapter.py` state schema and node factories |
| F-4 | Retry and new experiment are told apart by thread convention, not by the ledger | Medium | `langgraph_adapter.py`; `Researcher.retry` |
| F-5 | No waiting-for-review state; the adapter never reads the Transition ledger after proposing | Medium | `langgraph_adapter.py` |
| F-6 | Budget exhaustion and execution uncertainty are folded into generic states | Low | `langgraph_adapter.py` |
| F-7 | The researcher class requires a rule and the setup requires a subclass | Medium | `analysis.py`, `setup.py`, `workbench/local_session.py` |
| F-8 | History is raw records; no query by signal, conclusion or rejection | Medium | new query helpers in `arh_client` |
| F-9 | Refusals carry codes, not resolution text; results carry refs, not links | Low | `results.py`, workbench routes |
| F-10 | No one-command local setup from a configuration | Medium | new command in `arh_client` using `local_host` and `setup.py` |
| F-11 | Per-call accounting inside a node is a trust-model limit, not stated at the node wrapper | Medium | adapter docstrings, client README |
| F-12 | Resume is not an approval; enforced by the core, not stated or tested in the adapter | Low | adapter docstring, one test |

## 7. What must not change

- Permission is the one fresh `PERMISSION_CONSUMED` reply and never
  lives in graph state or a checkpoint.
- Independence of the check is enforced by the core from grants and
  lineages, never by the adapter.
- Caller-reported receipts are accounting. The interface must not imply
  that wrapping a node limits what the node spends.
- Every refusal stays on the ledger. An interface that retries silently
  must still leave the refusal there.
- The core imports nothing from the client or an experiment.
- Deduplication recovers an operation under its original identity and
  never authorizes a new claim.

## 8. Recommendation

Build the interface the proposal describes as one new client module over
`analysis.py` and a second version of the LangGraph adapter, with a
project configuration the generator reads. Then run the proposal's test.
The plan is
[first_class_interface_20261101.md](../plans/first_class_interface_20261101.md).
