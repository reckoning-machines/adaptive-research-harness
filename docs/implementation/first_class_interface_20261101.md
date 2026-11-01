# Implementation Report - A First-Class Interface for Research Code and LangGraph

Status: **IMPLEMENTATION RECORD OF DISPOSABLE DEVELOPMENT. CV1 UNCHANGED. CONSTITUTIONAL DELTA 0/0/0. NO REAL PROVIDER OR SPENDING. GENERATED DATA LABELLED SYNTHETIC.**

Date: 2026-11-01. Implements the
[first-class interface plan](../plans/first_class_interface_20261101.md)
with the five corrections recorded in its section 8, after the
[interface audit](../audits/first_class_interface_audit_20261101.md).

## 1. What was built

Six client modules, nothing in the core.

| Module | Lines | What it holds |
| --- | --- | --- |
| `arh_client/api.py` | 304 | `connect(project, role, run)`; `Research` with `analysis`, `call`, `retry`, `select`, `review`, `documents`, `history`; `Result`, `Proposal`, `Review`, `Refusal`; `Evaluator`, `Owner`, `Importer` |
| `arh_client/langgraph_nodes.py` | 103 | Node factories `analysis`, `selection`, `review`, `retry`, the in-node `call`, `result`, `await_review`; `GraphState` whose namespaces merge by operation |
| `arh_client/operations.py` | 80 | The operation journal: keys made once and written with fsync before use, every reply written after; `resolve_stage` resolves a key with no recorded reply against the core before sending again |
| `arh_client/project.py` | 60 | `project.json`: experiment, sources, analyses, roles, budgets by name; `write_setup`, `connect(role, run)` |
| `arh_client/dev.py` | 92 | `up` and `down`: setup written if missing, bundle frozen, host started, startup signed, connection printed |
| `arh_client/refusals.py` | 43 | The meaning and next action for each refusal and error code, the runbook's table as data |

`arh_client/analysis.py` grew from 275 to 416 lines: an `Inputs`
object, results recorded whole with `metric` and `n` optional, the rule
optional with the researcher's own question as the selection, `perform`
for any tool over any inputs with resumable stages, history queries, and
room in each reservation for one controlled replacement. The generator
now reads the project description. Nothing in
`adaptive_research_harness/` changed.

## 2. The corrections, as built

1. **Operation identity before any side effect.** Every operation has a
   journal entry under the run directory. Its keys exist before the first
   call. Each stage's reply is written after it. A node that dies between
   a call and the journal write leaves a key with no reply; on restart
   `resolve_stage` asks the core what became of the key and sends again
   only when the core never saw it. The journal is outside the LangGraph
   checkpoint. Demonstrated by killing the scoring node after its second
   call and the join node after its record, both before the node
   returned; neither call nor attempt was repeated.
2. **Explicit identity.** `operation` is required on every analysis,
   call and selection. The same identity resumes; the journal refuses an
   identity reused for different work (`OPERATION_MISMATCH`); a
   replacement is `research.retry`, which uses the core's controlled
   replacement under the original identity with the next dispatch index,
   and each refused replacement request gets a fresh key. Graph
   namespaces merge by operation; parallel branches named `join` and
   `placebo` ran one attempt each after a kill in their superstep.
3. **Decision and application separated.** `Review.status` is
   `waiting_for_review`, `check_failed`, `decided` with the decision, or
   `applied`. The review node pauses on `waiting_for_review` and again on
   `decided`, and the graph proceeds only on `applied`.
4. **Results broader than a metric.** A result is the function's own
   dictionary, recorded whole; without `metric` and `n` the conclusion is
   `RECORDED`. `history.conclusions(where={'column': 'next_day_bp'})`
   filters on the analysis specification. The scalar path is unchanged
   for the signal-groups example.
5. **Nested accounting.** A node wrapped as an analysis is one metered
   attempt. The scoring node is an uncharged grouping that makes six
   metered calls through `research.langgraph.call`, each its own
   attempt, receipt and journal entry. The two forms are not combined.

The candidate rule is optional. Without one, `select` records `'own'`
with an empty candidate set and the evaluator's record check accepts
that form; with one, the earlier behaviour holds.

## 3. The test the plan set

`examples/memo_returns/`, a two-source analysis through LangGraph. Six
memos scored for tone, one metered call each, through a deterministic
stand-in for a model call that the researcher process runs. The scores
joined to a returns table in two parallel branches, the next-day column
with the expectation that at least half the positive-tone memos are
followed by a positive return, and the prior-day column as a placebo
with the expectation of no such relation. The scientist's own next
question proposed as a Theme. The graph paused for review.

| Written by | Files | Lines |
| --- | --- | --- |
| The scientist, research code | `research.py`, `tools.py`, `provider.py`, `evaluator.py`, `graph.py` | 136 |
| The scientist, configuration | `project.json` | 33 |
| Process entry, the same for any graph | `job.py` | 54 |
| Demonstration, not needed to run a graph | `__main__.py`, `make_data.py` | 160 |
| The client, written once | `api.py`, `langgraph_nodes.py` | 407 |

The criterion was that the connection be mostly research code and a
short configuration, with no new job runner, recovery implementation or
setup generator. The research code is 136 lines and the configuration
33. `job.py` opens the connection, the checkpointer and the graph and
decides whether to start, resume or answer a pause; it holds no
recovery logic, which is the client's. No generator was written. The
criterion is met.

The demonstration, `python3 -m examples.memo_returns`, retained as
`artifacts/development/memo_returns/demo-20261101-memo-returns/`:

| Step | What happened |
| --- | --- |
| Up | One call: setup, bundle, host, startup signed, N 5, 0.7 s |
| Import | Six memos and one returns table, both sources, labelled synthetic |
| Killed after two calls | Both calls journaled before the node returned; the resumed node repeated neither |
| Killed inside the fourth call | After the provider counted it, before any receipt. On resume the call was uncertain, settled at its maximum, and its replacement refused `WORKER_NOT_QUIESCENT` |
| Quiescence proven | The host confirmed the dead process gone; the replacement was admitted with dispatch index 1. Six memos, seven calls, seven attempts, one authorized repeat |
| Killed after the join's record | Before the node returned. The record was on the ledger and in the journal |
| Resumed in parallel | Join 3/3 MET, placebo 1/3 MET, one attempt each |
| Proposal | The scientist's own question, `TH-M1`, graph paused `waiting_for_review` |
| Checks | A deliberately wrong evaluator FAIL, the right one PASS |
| Resume before a decision | Paused again; the researcher's own `decide` refused `UNAUTHORIZED` |
| Decision | Recorded; the graph paused on `decided`, not applied |
| Application | The graph finished on `applied`, N 6 |
| Reopen | The same `up` call reopened the run; the finished graph reported the same state and started nothing |

The whole sequence took 8.4 seconds.

## 4. Verification

| Suite | Result |
| --- | --- |
| Unit, component, workbench and integration tests | 100 tests OK, eight new in `tests/integration/test_memo_returns.py` |
| Acceptance | 77 cases PASS |
| Signal-groups example | demonstration PASS, the own-CSV command line PASS, setup files byte-identical from `project.json` |
| Memo-returns example | demonstration PASS, every step above asserted |

The setup files of both examples regenerate byte-identical from their
project files. The signal-groups researcher is now a function, so its
design's entry point changed and the retained run was regenerated.

## 5. Limits

The provider is a deterministic stand-in, and its calls are counted by
the example, not by ARH. Calls a node makes outside the call wrapper are
invisible to ARH, and a caller-reported receipt is accounting. A
reservation holds room for one replacement; a second lost outcome of
the same attempt needs a new reservation and is a refusal today. The
headline example keeps its hand-written setup; the generator does not
yet write hypothesis templates. `dev up` needs the checkout, because the
host runs from it. Graph pauses use LangGraph's interrupt; a graph run
without a checkpointer cannot pause. No person was timed.

## 6. Files

New: `client/arh_client/{api,langgraph_nodes,operations,project,dev,refusals}.py`,
`examples/memo_returns/` with its data and setup, `examples/signal_groups/project.json`,
`tests/integration/test_memo_returns.py`, this report. Changed:
`client/arh_client/{analysis,setup,__init__}.py`,
`examples/signal_groups/{tool,evaluator,researcher,make_setup}.py` and its setup,
`client/README.md`, `runbook.md`, `README.md`, `BUILD.md`, `.gitignore`,
the plan's section 8.
