# A First-Class Interface for Research Code and LangGraph - Plan

Status: **PLAN. PROPOSES ORDER AND SCOPE. AUTHORIZES NOTHING. CV1 UNCHANGED. CONSTITUTIONAL DELTA 0/0/0. NO REAL PROVIDER OR SPENDING.**

Date: 2026-11-01. Implements the recommendation of the
[interface audit](../audits/first_class_interface_audit_20261101.md),
which checked the Principal's forwarded design discussion against the
repository at `9642c29`. Findings are cited as F-1 to F-12.

## 1. The goal

A data scientist writes ordinary research code and ordinary LangGraph
graphs. They supply an analysis function, its inputs, an expectation and
an evaluator, and they receive the result, its evidence reference, its
check status and any refusal. ARH handles reservations, attempts,
permission, receipts, settlement and recovery around them. They
understand what they are authorizing and checking without implementing
any of it. Administrative setup comes from one project configuration.

The three layers stay as the audit found them. Research code belongs to
the data scientists. The integration layer is `arh_client`, maintained
with the core. The core enforces and is not touched by this plan.

## 2. Principles

- The everyday interface speaks in research concepts: analysis, inputs,
  expectation, evaluator, budget by name, result, evidence, check,
  refusal. ARH concepts stay available underneath.
- Ordinary functions. No subclass is needed anywhere.
- The evaluator is registered under its own identity. Nothing attached
  to a graph can approve what the graph produced. The core enforces this
  today and the interface states it.
- Permission never lives in graph state. An interrupted node recognizes
  its attempt and recovers its receipt before any execution is
  considered. A resumed graph approves nothing.
- A wrapper around a node accounts for the attempts the node declares.
  It does not discover activity it is not told about. The interface says
  so where the wrapper is documented.
- The lower-level client remains public.

## 3. Shape of the build

Three new pieces in `arh_client` and one revised one. Nothing in the
core.

### 3.1 Project configuration (F-2, F-10)

One file in an experiment directory, `project.json`, that names the
project, the roles and their identities, the sources and their classes,
the analyses as tools with their costs and tariffs, and the budgets by
name. A budget name maps to a grant, a purpose and a maximum. The
generator reads it and writes the three setup files, replacing the
hand-written `make_setup.py` in both examples.

`arh_client.project.Project.load(directory)` reads it.
`Project.connect(role)` opens the connection for a role from the run's
connection file. `Project.budget(name)` gives the grant, purpose and
maximum. One command, `python3 -m arh_client.dev up <directory>`, writes
the setup if it is missing, freezes a bundle, starts the local host and
prints the connection file. `down` stops it. This reuses `local_host` and
the generator and adds no service.

What the configuration may set is administrative: names, amounts,
sources, tools, tariffs. It cannot change what the core enforces. The
Principal still signs the grants at startup through the existing
sequence.

### 3.2 The research-concept interface (F-1, F-7, F-8)

`arh_client.research_api`, working name, reached as
`research = arh.connect(project=...)`.

| Call | What it does |
| --- | --- |
| `research.analysis(fn, inputs, expectation, budget)` | Returns a callable. Calling it records the design with the expectation, reserves under the named budget, attempts, executes through the host tool that wraps `fn` or the caller-executed tool `fn` is, records the result with its conclusion, settles and closes. Returns a `Result` |
| `Result` | `conclusion`, `metric`, `n`, `evidence` (the record's `Ref`), `design`, `check` (`None`, `PASS` or `FAIL` once a check exists), `refusal` (code, detail and resolution text), `links` (paths to the records on the workbench) |
| `research.inputs.documents(source, since=None)` | Committed documents as references |
| `research.history.conclusions(signal=None, state=None)` | Conclusions recorded by this researcher, by analysis field or state |
| `research.history.rejections()` | Candidates rejected, with reason, condition and whether the condition is met now |
| `research.next(result, chosen, reason, question)` | The selection record and the Theme proposal, returning the transition id |
| `research.evaluator(recompute)` | The `evaluate` a Checker registers, for the evaluator process |

Built on `AnalysisResearcher`, which loses `RULE_REQUIRED`: a rule is
optional, and `candidates` returns an empty set without one. The
candidate table remains one reusable pattern, not a requirement. The
generated design's entry point becomes a factory function, so a class is
no longer required (F-7).

### 3.3 The LangGraph adapter, second version (F-3 to F-6, F-11, F-12)

`research.langgraph.analysis(fn, inputs, expectation, budget)` returns a
node function. `research.langgraph.proposal(make_proposal)` returns a
node function. Both read and write one namespace in graph state, keyed by
the node name and, inside a branch, the branch key LangGraph gives, so two
analyses in one graph or one analysis in parallel branches never share a
reservation, an attempt or a key (F-3).

Execution. On entry the node reads its namespace. If an attempt exists it
asks the core what became of it and recovers the receipt from the host,
the durable store or the provider before anything else. Only with no
attempt does it reserve and attempt. Permission is requested inside the
node and never stored. This is `Execution.run` made explicit at node
entry rather than inside a later node.

Retry and new experiment (F-4). A node re-entered with the same inputs
and design is a resume. A retry, for work the core reports as settled at
the maximum with no receipt, is an explicit call,
`research.langgraph.retry(node)`, which uses `Researcher.retry` with the
next dispatch index after the host confirms quiescence and never before.
A new experiment is new inputs or a new expectation, which is a new design
record and a new input hash, and the node treats it as new work.

Outcome states (F-5, F-6). The node writes one of `recorded`,
`refused`, `budget_exhausted`, `execution_uncertain`, `waiting_for_review`,
`admitted`, `rejected` into its namespace. `waiting_for_review` is set by
the proposal node, which reads the Transition ledger for a check and a
decision, and a `research.langgraph.await_review(node)` conditional edge
returns the current state without advancing anything. A graph can pause
on it with LangGraph's interrupt. Resuming after the pause re-reads the
ledger; it decides nothing (F-12), and one test kills and resumes a graph
across a Principal decision to show it.

Provider calls inside a node (F-11). The node wrapper accounts for one
attempt. For a node that makes several provider calls,
`research.langgraph.call(provider, budget)` inside the node makes each
call its own attempt with its own claim and receipt under the same design.
The docstring and the client README say that calls not made through it
are invisible to ARH and that the receipt is the caller's own accounting.

### 3.4 Errors and links (F-9)

`RefusedError` and `Result.refusal` carry the code, the detail and one
line of resolution text from a catalogue in the client, the same text the
runbook's refusals table holds. `Result.links` carries the workbench paths
for the design, the record and, once it exists, the check and the
decision.

## 4. The test

Connect a second, structurally different analysis through LangGraph. Not
another signal-groups variant. A two-stage analysis over two sources: a
per-document text score over memos, joined to a table of returns in a
second node, with an expectation on the joined result, a placebo branch
run in parallel, and a proposal node that waits for review. The research
code is the scoring function, the join function, the expectation, the
recompute function and the choice of next question. The configuration is
one `project.json`.

The criterion is the proposal's own. If the connection is mostly research
code and a short configuration, the interface is working. If it needs
another job runner, recovery implementation or setup generator, that
plumbing moves into the adapter before the test is called passed. The
report states the lines in each layer, as the signal-groups report did.

## 5. Changes, in order

1. `project.json` and `arh_client.project`; the generator reads it; both
   examples' `make_setup.py` replaced by configurations that produce
   byte-identical setup files where the content is unchanged.
2. `python3 -m arh_client.dev up|down`.
3. `analysis.py`: rule optional, factory entry point, history helpers.
4. `arh_client.research_api` with `Result`, the refusal catalogue and
   links.
5. The adapter's second version beside the first. The headline example
   moves to it when its demonstrations pass unchanged; the first version
   is removed when nothing uses it.
6. The two-source example, its evaluator process and its test.
7. Documents: client README rewritten around the everyday interface with
   the lower-level client beneath it, runbook path for the new example,
   README's "what a team supplies" table, an implementation report with
   the layer counts.

## 6. Tests

- Project configuration round trip: the examples' setup files
  regenerated byte-identical.
- One command brings a host up against a configuration and down again.
- The research-concept call on the signal-groups analysis gives the
  same records the command line gives.
- Two analyses in one graph and one analysis in two parallel branches,
  each with its own reservation, attempt and keys, none colliding.
- A node killed after the receipt and before the record resumes and
  recovers without executing again, as the headline demonstrations do.
- Retry refused before quiescence and admitted after, with the dispatch
  index advanced and the original attempt's liability kept.
- A proposal node reaches `waiting_for_review`; the graph is killed; the
  Principal decides in a separate process; the graph resumes and reads
  `admitted` without having decided anything.
- A node with three calls through `call` yields three attempts and three
  receipts; a node with calls outside it yields one, and the test asserts
  that ARH saw one.
- The evaluator process under the Checker identity fails a Theme whose
  result does not recompute, and a graph that registers its own function
  as evaluator is refused `independence` by the check.
- Every refusal surfaced to research code carries resolution text.

## 7. Decisions, resolved

The three choices listed in the first draft were reviewed the same day
and found to be ordinary implementation choices within the scope already
given. Both pause styles are allowed and neither decides anything. One
attempt per metered call. The configuration proposes budget amounts, which
become authoritative only through the existing startup, where the
Principal signs the grants. No further approval round. None of this
changes the Constitution, an identity rule or a Transition class. If
building reaches a point where one would, the work stops and the question
returns to the Principal.

## 8. Corrections, 2026-11-01

Five corrections from the Principal's review of the first draft, folded
into the build. Each names what it changes above.

1. **Persist the operation identity before any side effect.** A node
   that designs, reserves and attempts and then dies before returning
   leaves nothing in a LangGraph checkpoint, and an empty namespace on
   restart would start the work again. The adapter keeps a durable
   operation journal of its own, outside the checkpoint: request keys and
   every ledger reference are written with fsync before the call that
   uses them and after the reply, for the outer operation and for each
   nested call. On entry a node reads the journal first. A key with no
   recorded reply is resolved by asking the core what became of it before
   it is sent again. Section 3.3 "Execution" reads accordingly, and the
   tests include a kill before the node's first successful return.
2. **Give each investigation an explicit identity.** The same inputs and
   expectation can mean a resume or a deliberate replication, and changed
   inputs can be an accidental mutation during recovery; an input hash
   cannot tell intent. Every operation carries a stable identity the
   research code gives it. The same identity resumes. A new identity is
   new work. A retry is the existing controlled replacement, after
   quiescence, under the original identity with the next dispatch index.
   Parallel branches carry identities the research code gives them, and
   state updates merge by identity so they cannot overwrite each other.
   Nothing relies on a LangGraph branch key. Section 3.3 "Retry and new
   experiment" is replaced by this.
3. **Separate the decision from its application.** ARH records a decision
   and, separately, an Apply that changes the accepted record. The review
   states are `waiting_for_review`, `check_failed`, `decided` with the
   decision, and `applied`. Work that needs accepted research proceeds
   only after `applied`. Section 3.3 "Outcome states" reads accordingly.
4. **Keep results broader than a metric and a count.** Research functions
   return tables, forecasts, fitted models and documents. The result is
   the function's own dictionary, recorded whole, with `metric` and `n`
   optional; a conclusion against an expectation is computed when they
   are present and the record says `RECORDED` otherwise. History queries
   filter on the analysis specification and a subject identifier, not on
   a signal. The scalar interface remains one supported pattern. Sections
   3.2 and 3.3 read accordingly.
5. **Define nested accounting.** A node wrapped as an analysis is one
   metered attempt. A node that makes metered calls through the call
   wrapper is an uncharged grouping; each call is its own attempt with its
   own durable identity and its own cost, and resuming the node repeats no
   call that already has a journal entry. The two forms are distinct and
   not combined in one node. Section 3.3 "Provider calls inside a node"
   reads accordingly.

The candidate rule, when absent, must still leave a working path. A
selection may name the scientist's or the agent's own next question, with
whatever candidates existed recorded as rejected, and the evaluator's
record check accepts that form. An empty candidate set with a membership
requirement is not a path.

The success criterion for the two-source example is the reviewer's: the
scientist writes the research and the evaluation, and the adapter handles
the lifecycle reliably, including the awkward interruption points.

## 9. Limits to state

The interface accounts for what research code declares. It does not
limit spending by a process that can reach a provider. There is still no
operating-system isolation. A result's check status is the Checker's
finding on reproducibility and record integrity, not an opinion on the
research. No person is timed by this plan.
