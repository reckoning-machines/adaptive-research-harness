# External Researcher Integration - Profile, Client, Host and a LangGraph Example

Status: **PLAN FOR DISPOSABLE SYNTHETIC DEVELOPMENT UNDER THE ADDENDUM'S WORKFLOW PARAGRAPH. CV1 UNCHANGED. CONSTITUTIONAL DELTA 0/0/0. NO APPROVAL PACKET FOLLOWS.**

Date: 2026-11-01, revised the same day with the Principal's four
corrections, the wording fix on what a profile may name, and the follow-on
note in section 9. This plan answers the
[integration readiness audit](../audits/langgraph_integration_readiness_audit_20261101.md)
and the Principal's brief it examines. It is implemented directly, as the
[build approval addendum](../decisions/first_research_cycle_build_approval_addendum_20261029.md)
and the [workbench working rule](../decisions/workbench_authorization_20261030.md)
direct for routine prototype work. The
[implementation report](../implementation/langgraph_integration_20261101.md)
records what was built and tested.

Governing baseline: [CV1, revision 12](../doctrines/new_speedway_constitution.md)
as [admitted](../decisions/cv1_admission_20261019.md). CV1 governs if this
plan conflicts with it. If any step below needs a new identity rule,
owner, evidentiary class, Transition class, Authorization, budget or
Standard, work on that step stops and the question returns to the
Principal; the rest continues.

## 1. Milestone

A data science team can install one Python package, point it at a running
local harness, supply a researcher written in LangGraph and an experiment
of their own, and obtain through the core the same enforcement the
synthetic cycle has, without editing enforcement code. One working example
demonstrates it end to end with a deterministic fake provider and no
credentials. The original synthetic example keeps working unchanged in
behaviour.

Out of scope: real providers or spending, OS isolation claims, a general
independent reader for arbitrary experiments, the Paper Book, public
release, license selection, any change to admitted records.

## 2. Shape of the build

| Piece | Location | What it is |
| --- | --- | --- |
| Experiment profile | `adaptive_research_harness/experiment.py`; `experiments/synthetic_flow/experiment.json`; `examples/langgraph_headlines/setup/experiment.json` | Loader and closed validator registry in the core; one profile per experiment, frozen into the bundle as `bundle/experiment.json` |
| Core reads the profile | `rules.py`, `dispatch.py`, `tool_worker.py`, `engine.py`, `profile.py`, `service.py`, `__main__.py` | Literals from audit section 2 replaced by profile lookups. Refusal codes unchanged |
| Local host | `adaptive_research_harness/local_host.py` | Token-ingress core and tool workers as processes, connection file, clock, quiescence proofs, restart. Moved from `acceptance/local.py`, which keeps its fixture behaviour by importing it |
| Build | `build_support/freeze.py` | Freezes from a setup descriptor (setup, artifacts, experiment, optional cohort catalog, extra files). Default descriptor is the synthetic packet plus its profile. Roles, step catalogs and tool executables derive from the setup and profile |
| Client | `client/` distribution `adaptive-research-harness-client`, import `arh_client` | Standard library only. Protocol, connection, research lifecycle, checking toolkit, principal and observation helpers, startup. `arh_client.langgraph_adapter` behind an optional extra |
| Example | `examples/langgraph_headlines/` | Setup and profile, fake provider, LangGraph researcher, evaluator, one runner command |
| Tests | `tests/component/test_experiment.py`, `tests/integration/test_langgraph_example.py` | Profile and rule boundaries without processes; the six demonstrations through real processes |
| Documents | `client/README.md` (install and integration guide), `BUILD.md`, `runbook.md`, `architecture.md` section | What the team supplies, what the core enforces, how failures and retries work |

## 3. The profile

`experiment.json` fields, all data:

- `ExperimentId`, `version`.
- `genesis`: `{design, grant}` named in the bundle's setup. `engine.genesis`
  expects exactly these.
- `steps`: ordered list. Each has `name`, `kind` (`research` or `check`),
  `tools` permitted, `inputs` (`count`, record `kind`, `form`),
  `parameters` (exact object the attempt must carry), `input_limit_bytes`,
  and either `tariff` (research) or `maximum` (check). A tariff is
  `{measure: rows, limit, bands: [{up_to, maximum}]}` or
  `{measure: rows, limit, per_unit}`. The core computes the expected
  maximum and refuses `INVALID_ESTIMATE` on mismatch, as now.
- `tools`: id to `{execution: core | caller, module, callable, label,
  uid, provider_work}`. `module` is either a dotted name of an installed
  package module or a file path relative to the experiment file's own
  directory; a file module is copied into the bundle and both forms are
  hashed into `tool_executables`. `provider_work` is `ends_with_caller`
  for computation that cannot outlive the process that invoked it, or
  `may_outlive_caller` for a remote provider that accepts a request and
  keeps working. `label` and `uid` serve the host and the Linux templates.
- `sources`: SourceId to `{period_ms, item_id: {prefix}, window: {start,
  end}, document: {synthetic: true, max_bytes}, extraction: {validator,
  ...parameters}}`. The only validator in this milestone is `row-ratio`,
  a declarative row filter with typed fields, a uniqueness key, a
  denominator filter and a numerator filter. It reproduces the `SRC-SYN`
  extraction rule exactly and serves the headline source.

The core never imports experiment code into its enforcement process.
The tool declarations name modules so that a worker process the host
starts, or the caller that holds the attempt, can load them, and so that
their bytes are pinned in the inventory. `rules`, `engine`, `model`,
`storage` and `dispatch` read only the hashes. What the profile cannot do:
change who may reserve, attempt, check, decide or apply, change the
criteria set, turn off the receipt binding, declare a non-synthetic
source, select a validator that is not in the core's registry, or be read
differently by two callers. It is bundle content under the inventory;
changing it changes the build identity and a running core never reloads
it.

## 4. The client

`arh_client` modules and the operations the integration uses:

| Module | Public interface |
| --- | --- |
| `protocol` | `canonical`, `decode`, `digest`, `units`, `amount`, `request(path, value)` |
| `connection` | `Connection.from_file(path, actor)`; `call`, `committed`, `query`, `outcome(key)` for a lost reply, `profile()`, `closure()`, `state()`, `budget(grant)`, `obligations()`, `history(ledger)`, `get(ref)` |
| `research` | `Researcher(connection)`: `formation(source_sha)`, `reserve`, `attempt`, `Execution` with `claim`, `execute(fn)`, `finish`, `settle`, `reconcile`, `research_commit`, `close`, `propose`, `fund`, `retry`. Every command takes a caller-persisted key |
| `checking` | `evaluate(snapshot, transition_id, actor, grant, attempt, profile, recompute)`: the common and class criteria; `recompute` is the experiment-specific hypothesis validator the team supplies. `run_check(connection, transition_id, evaluate)`: reserve, attempt, claim, compute, finish, check-commit or negative record, settle, close |
| `principal` | `Principal(connection)`: `propose_control`, `decide`, `policy_decide`, `apply`, `fence`, `recover`, `observe(source, document, form)`, `startup(observer, checker)` |
| `host` | `HostControl.from_file(connection_path)`: `tick`, `quiesce(generation, provider_disposition)`, `stop`, over the host's control socket with the Principal token. The host itself is started from the checkout; the client never imports the core |
| `langgraph_adapter` | `GovernedState` TypedDict, `keys_node`, `governed_nodes(researcher, provider)` returning the node functions a graph composes. Imports LangGraph lazily |

Request keys are version-4 UUIDs generated in a dedicated graph node and
checkpointed before the node that uses them, so a re-run node re-sends
the same key and receives the original receipt. `tool-run` is not a keyed
command and its reply is never cached by the core or stored in graph
state: permission to execute exists only in the one fresh
`PERMISSION_CONSUMED` reply, and the client's `claim` treats every other
reply, including a replay of the exact request that once succeeded, as
no permission.

Installation is proved in a clean environment. The client distribution
depends on nothing outside the standard library and is installed from
`client/`; the host runs from the checkout and is documented separately.
The example is run from a directory outside the checkout against a host
started inside it.

## 5. Execution lifecycle through the client

1. `reserve` under the research grant for a declared purpose.
2. `attempt` with step, tool, input references, exact parameters and the
   tariff maximum. Refused before anything runs if the allowance, grant,
   lineage cap, fence, expiry, tool permission or estimate fails.
3. `claim`: `tool-run`. For a `caller` tool the core records a durable
   claim and returns `PERMISSION_CONSUMED` exactly once. A repeat of the
   same request returns `IN_PROGRESS_OR_UNCERTAIN` or the registered
   receipt. A replayed permission is not permission.
4. `execute`: only on a fresh `PERMISSION_CONSUMED`. The caller sends the
   claim identity to its provider, writes the receipt durably in its own
   state before returning, then `finish` registers it with the core,
   which refuses a different receipt for the same claim.
5. On re-entry with `IN_PROGRESS_OR_UNCERTAIN`: if the caller's durable
   receipt exists, `finish` it. Otherwise ask the provider for its own
   record of the claim; a provider that deduplicates by claim returns the
   completed result, which is finished as above. Otherwise the response
   is lost and execution may have occurred or may still be occurring.
   `reconcile` settles `UNKNOWN` at the admitted maximum and commits a
   negative research record. The provider is not called again for that
   attempt. Settlement is accounting; it cancels nothing.
6. `settle` at the receipt's actual, `research_commit`, `close`.
7. `retry` opens a new attempt with the next `dispatch_index` and
   therefore a new claim. The core admits it only when the predecessor is
   settled and a quiescence proof written by the host names the caller
   generation that held the earlier claim as gone. For a tool declared
   `may_outlive_caller` the proof must also record a provider disposition
   for the earlier claim that establishes the earlier work can no longer
   execute: `COMPLETED` with the provider's result, or `CANCELLED` with
   the provider's acknowledgement. Provider deduplication is not such a
   disposition. It belongs to step 5, where a lookup by the original claim
   recovers the original operation under its original identity. It never
   authorizes a new claim, because the original and the replacement would
   be different operations to the provider and both could execute. A
   provider guarantee covering both identities would have to be declared
   explicitly; none is declared in this milestone. A dead caller alone
   leaves the attempt uncertain and the retry refused
   `WORKER_NOT_QUIESCENT`.
8. `propose` and `fund` register a hypothesis citing the research record.
   Checking and admission are other actors' work.

## 6. The example

Experiment `HEADLINE-SENT-1`. Two sources. `SRC-NEWS-SYN` publishes a
daily synthetic cohort of 24 headlines, each with a row id and the text
only. `SRC-RET-SYN` publishes, one day later, the next-day return in basis
points for each row id. Step `classify-headlines` sends the headline
document and nothing else to `FAKE-LLM-1`, a deterministic caller-executed
provider that labels each headline bullish or bearish from a fixed lexicon
and charges 0.02 units per row. The provider keeps its own durable record
keyed by claim, answers a lookup for a claim it completed, and honours a
cancellation that discards any late completion; it is declared
`may_outlive_caller`. The classification research record carries the
labels and their counts. After the clock passes the returns period and
the Observation function commits the returns document, the researcher
commits a second research record that joins its recorded labels to the
committed returns and reports how many bullish labels preceded a positive
return. The hypothesis template asks whether at least three in five
bullish-labelled headlines precede a positive next-day return in the next
cohort. The evaluator recomputes the join from the recorded labels and
the committed returns and states that this verifies the arithmetic and
the join, not the labels.

Actors: Principal and Observation function in the runner process, the
researcher graph in its own process with a SQLite checkpointer, the
evaluator in its own process under the Checker identity. One host holds
the tokens. No OS isolation is claimed.

Demonstrations the runner performs and prints:

1. Startup through generic startup, each control checked by the evaluator.
2. A research job that reserves, attempts, claims, classifies, records,
   settles, then after the returns arrive joins, proposes and funds; the
   evaluator passes it; `P-1` admits; Apply registers it.
3. A reservation beyond the grant refused `BUDGET_EXCEEDED` and an attempt
   beyond its allowance refused `ALLOWANCE_EXCEEDED`, with the provider's
   durable call counter unchanged.
4. The researcher identity attempting `check-commit`, `decide`, `apply` of
   an undecided proposal, `fence` and a `LIMITS` proposal, each refused
   and preserved.
5. Interruption and loss, each with the provider call counter checked:
   a job killed after its receipt is durable, resumed with no second call;
   the exact successful claim request replayed after the crash, answered
   without permission and without a call; a job killed after the provider
   completed but before the caller's receipt was durable, resumed by
   provider lookup with no second call; a job killed before the provider
   recorded anything, resumed into reconciliation with `UNKNOWN` at
   maximum, its retry refused after the host records the dead caller, and
   admitted only after the provider's cancellation is recorded.
6. A job whose joined record overstates its count, proposed, checked
   `FAIL` on recomputation, `policy-decide` refused, head unchanged.
7. The synthetic example run unchanged.

## 7. Tests

- Component, no processes: profile loading and refusal of malformed
  profiles; tariff bands and per-unit maxima; step, tool and parameter
  admission under both profiles through `Rules` with fabricated views;
  `row-ratio` reproduces the `SRC-SYN` extraction on the formation
  cohort and on mutated rows; `finish` refuses a conflicting receipt;
  retry evidence for `caller` tools.
- Integration, real processes: the demonstrations above as assertions on
  ledger records, budgets and the provider counter, including the replayed
  claim request and the provider-outlives-caller case; generic startup on
  the synthetic bundle reproduces N=16 with the same transition ids.
- Package boundary: a clean virtual environment installs the client from
  `client/`, and the example runs from a copy outside the checkout against
  a host started inside it, importing only `arh_client`.
- Regression: the existing unit, component, workbench and acceptance
  suites. Fixture cases adapted only where a literal they relied on moved
  into the profile.

## 8. Limits to state in the deliverable

Cooperative tokens, caller-reported receipts for `caller` tools, no OS
isolation, synthetic data only, the reader covers the synthetic experiment
only, LangGraph pinned to the tested major version, the host runs from the
checkout, and nothing here is a production genesis.

## 9. Follow-on, not built here: the Principal's own documents and researcher

Two different follow-ons, stated separately.

**A new synthetic experiment needs configuration only.** A third setup
directory holds a `setup.json` declaring one source, an Observation grant
for it, one researcher design and grant, one Checker design and grant, a
theme and limits; a `designs_and_methods.json` with the hypothesis
template, methods and tool specifications; an `experiment.json` with the
steps, the tariff and the source's period, item and extraction rules;
and the documents, committed as `DOCUMENT` Observations of that source by
the Observation function through the client. The researcher is any
program using `arh_client.research` under the researcher token, LangGraph
or not; the evaluator is any program using `arh_client.checking` under
the Checker token. No core change.

**Research on the Principal's real documents needs a small implementation
extension, and the documents keep their actual provenance.** They are not
to be labelled synthetic to pass validation. The extension is a declared
input class, `historical`, for documents that are real material read
after the fact, carrying no prospective evidence and earning no forward
standing, which CV1 already classes as Historical Reconstruction. The
exact places that would change, each a few lines, none changed here:

| Where | Today | Extension |
| --- | --- | --- |
| `experiment.py` source rule | `document.synthetic` must be `true` | `document.class` is `synthetic` or `historical`; a historical source declares `synthetic: false` in its grant declaration |
| `rules.do_observation_commit` | `DOCUMENT` requires `synthetic: true` in the document and stamps `synthetic: true` on the Observation | Requires the document's declared class to equal the source rule's class and stamps that class |
| `rules.do_research_commit` | Requires `synthetic: true` | Requires the record's class to match the classes of the inputs it cites and to be `historical` when any input is |
| `dispatch.finish`, `rules.do_settle` | Receipts declare `synthetic: true`; settlements are in `simulated_research_units` | Receipt and settlement carry the provider's declared unit; a real provider needs the cap and billing decision the admission record lists |
| Checker toolkit | `sources` and `closure` criteria require synthetic sources and the synthetic classification string | Accept the historical class and state it in the Check context |

Each of these is a change to what an evidentiary record means, so it
goes to the Principal as one small decision before it is built. A real
provider behind the researcher additionally needs the provider identity
and cap decisions, D-14 and the provider caps, and the controlled-access
placement of its credential. Until then real documents are not run
through this path.
