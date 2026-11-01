# Adaptive Research Harness private prototype

A constitutional harness for evolving investment hypotheses, strategies and
research agents. The Principal authorizes autonomous disposable synthetic
build/test runs in the [decision addendum](docs/decisions/first_research_cycle_build_approval_addendum_20261029.md).
Separate build/host-digest approvals are superseded. Runtime grants, budgets,
independent checking, decisions and Apply boundaries remain enforced.

From the repository root, run the complete example with standard Python 3.12:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m acceptance.local --example
```

The command creates a labelled disposable SQLite database, executes the retained
ten-design startup through actual commands and computed Checks, runs researcher
AD-R1, registers its derived hypothesis through independent Check/P-1/Apply,
and adapts its next experiment from the result. The researcher detects that the
large-event result rests on one shock, records the failed generalization, then
uses tool B for a complementary-cohort control: 6/10 selling rows rather than
2/2 in the large-event group. The original claim, selection rationale and
negative control result remain immutable. Both Checkers recompute the contrast. It prints the question, counts, cost,
evidence and next permitted action. All charges are simulated; no provider or
network service is contacted. Synthetic results earn no forward standing.

Run cooperative integration and actual process-death schedules with:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m acceptance.local --jobs 4
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -v
```

Each invocation records an automatic code inventory and complete covered-source
snapshot under `artifacts/development/builds/<digest>/`. Each run has a unique
bundle and report directory; earlier reports are retained. Reports identify the
exact inventory, tested files, snapshot and retained disposable database path.
Changing source during a run fails verification. Hashes supply traceability,
not manual approval. Older records predating source snapshots remain historical
and cannot be retroactively upgraded to exact-source evidence.

The local fixture runs core, researchers, Checkers, tools and final reader in
separate processes. It reuses the real core command handler, SQLite, accounting,
actor programs and tool implementations. Same-user fixture tokens assume a
trusted driver and fixed actor code; they provide **no OS isolation guarantee**.
Linux peer-UID, file, namespace and cgroup enforcement requires the separate
Linux arrangement. No VM is currently available; T06 remains unexecuted.

B10 uses a whole-core outage as a **substitution**, not a demonstration of
Transition-ledger-only read failure. The narrow Checker language has no supported
input reaching constitutional NOT DETERMINABLE/STOP; that branch is **unreachable**.
Cooperative identity cases establish application behavior only. Reports state
these limits rather than counting the missing coverage as passed.

The core lives in `adaptive_research_harness/`: `engine`/`rules` enforce commit
boundaries, `model` supplies rebuildable views, and `storage` preserves immutable
events plus command receipts. `dispatch` gates handoff by admitted attempts and
durable claims. Fresh recovery never redispatches an old uncertain attempt;
replacement requires evidence the original generations/queues cannot still act.
Pending liabilities survive interruption and settle at actual or UNKNOWN maximum.
Receipt lookup does not block behind running work.

Researcher programs derive proposals from their own committed Research Records.
Explicit mutation operations retain adversarial origin and cannot be admitted.
Checker reservations reject forbidden subjects before charging. Checkers compute
from actual committed closure in separate code, importing neither core admission
predicates nor research-tool calculations. The independent reader separately
reconstructs Check/decision/Apply links, funding, spending admission, binding
and invalidation relationships. Evidence records pin their admission heads so
equal clock instants are not mistaken for cross-ledger ordering.

Only the Principal-operated internal Apply continuation can request elapsed
invalidation, RELEASE, delegated decisions or recovery continuation. Proposers
can request ordinary Apply of their own decided proposals; they do not acquire
general continuation privileges. Events preserve the authenticated requester
and the acting role. Pre-genesis refusals are operational receipts: they neither
poison nor relax the empty-governed-ledger requirement.

The public CLI remains `python3 -m adaptive_research_harness command OP --actor ID
--request FILE`. Protected Linux units use fixed UIDs and peer credentials;
knowing an actor string confers nothing. Root/operator and installed core code
are trusted; direct same-UID embedding is not a security boundary. Linux
installation templates remain unexecuted. They require a dedicated disposable
Ubuntu/ext4 host, not a production machine. No exact-digest approval is required
for these authorized disposable development runs.

## Local research workbench

Authorized by the [workbench authorization](docs/decisions/workbench_authorization_20261030.md)
and planned in the [workbench plan](docs/plans/local_research_workbench_20261030.md).
From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m workbench --port 8765
```

Open `http://127.0.0.1:8765/`. The server binds to loopback only and uses
nothing outside the standard library. `python3 -m workbench --demo` runs the
same cycle headless: three cohorts, an interrupted run resumed, a copy under
a differing build opened read-only.

The page starts a run on one of three declared synthetic cohorts in
`workbench/cohorts.json`, shows the research sequence as eight stages linked
to the ledger records they rest on, renders the rows, counts, the
researcher's recorded reasons and candidates, the budget per grant, and puts
accounting, refusals, the independent reader and raw records behind
expandable sections. Starting a run freezes a bundle, starts core and tool
workers as processes and runs the ten-design startup, exactly as
`acceptance.local` does. Every step is one existing actor operation or
Principal command; the page's list of next steps is derived from the ledgers
and is a convenience. The core enforces permission and current state when a
step executes, and refusals stay on the ledger.

Variant cohorts are second Observations of the same `SRC-SYN` item
`cohort-2026-10-28` with different rows, which the source declaration
already classes as new Observations. `independent-shocks` sends the
researcher down its reproduction branch: tool B recomputes the same rows,
which the page labels an independent calculation and not independent
evidence. `control-survives` meets the two-thirds diagnostic, shown as the
researcher's rule rather than a statistical test.

A bundle's `inventory.json` names the source bytes only, and its digest is
the build identity; working-tree status and the build environment sit beside
it in `build_metadata.json`, outside the digest, so identical source yields
one identity. Each variant document carries its own name, its edits and the
formation content hash, and states that it is neither corroboration of the
admitted cohort nor a replacement of it.

State is retained in place under `artifacts/development/workbench/<run>/`.
A run reopens live when every file in its bundle inventory matches the
current tree, so an interrupted run continues from the next permitted step
without repeating computation, charges or admission. After any covered
source change, earlier runs open read-only from SQLite with the reader's
reconstruction and nothing can be continued. Limits: the workbench process
holds every actor token, as the acceptance fixture does, and makes no OS
isolation claim; `fixture.json` holds the session tokens while a run is live
and is removed on close, so a crashed server leaves it behind until the run
is reopened or closed; quiescence proofs on resume rest on recorded process
ids no longer running, which is fixture evidence, not host evidence.

No real spending, providers, trading, Paper Book, framework adapters, public
release or license selection is included. Arbitrary scientific prose and a
general-purpose constitution interpreter remain outside capability.

## Experiment profile, client, host and the LangGraph example

Authorized as disposable synthetic development under the addendum's
workflow paragraph, audited in the
[integration readiness audit](docs/audits/langgraph_integration_readiness_audit_20261101.md),
planned in the [integration plan](docs/plans/langgraph_integration_20261101.md)
and reported in the
[implementation report](docs/implementation/langgraph_integration_20261101.md).

The synthetic experiment's shape now lives in
`experiments/synthetic_flow/experiment.json` and is frozen into every bundle
as `bundle/experiment.json`: permitted steps, the tools each step may use,
tariffs, the Check cost, source period and item rules, the extraction
validator and the genesis pair. `rules`, `dispatch`, `tool_worker`,
`engine` and `freeze` read it; the literals they carried before are gone.
A profile selects validators by name from a closed registry in
`adaptive_research_harness/experiment.py` and cannot name code for the
enforcement process. The core process never imports experiment code. Tool
modules named in a profile are imported only by a worker the host starts
(`execution: core`) or by the caller that holds the attempt
(`execution: caller`); their bytes are pinned in the inventory.

A caller-executed tool consumes a durable claim through `tool-run`, which
answers `PERMISSION_CONSUMED` exactly once, registers its receipt through
`tool-finish`, which refuses a second different receipt for the same claim,
and settles at the receipt or at the maximum with `UNKNOWN` provenance. A
replacement attempt for such a tool needs a host proof that the caller
generation which held the claim is gone, and for a tool declared
`may_outlive_caller` a recorded provider disposition for that claim,
`COMPLETED` or `CANCELLED`. Provider deduplication recovers the original
claim under its own identity and never authorizes a new one.

`adaptive_research_harness/local_host.py` is the cooperative host the
acceptance fixture and the workbench always used, now runnable on its own:
`python3 -m adaptive_research_harness.local_host --setup DIR --run DIR`
freezes a bundle from a setup directory, starts the core and core-run tool
workers as processes, writes a connection file with one token per actor and
serves a control socket for clock advance, quiescence proofs and stop. One
host process holds every token; this is no OS isolation.

`client/` is the installable client, `arh_client`, standard library only,
with the public surface and its documentation in `client/README.md`.
`examples/langgraph_headlines/` is a complete experiment supplied from
outside the core: a setup directory, a deterministic fake provider declared
`may_outlive_caller`, a LangGraph researcher with a SQLite checkpointer, an
evaluator built on the client checking toolkit and a runner. Run it with
`.venv/bin/python -m examples.langgraph_headlines` after installing the
client with its `langgraph` extra. It prints the research result and
thirteen control decisions. Its receipts are the researcher's own statements:
accounting, not enforcement over what that process spends. The independent
reader under `acceptance/reader.py` reconstructs the synthetic experiment
only; the headline experiment's arithmetic is checked by its registered
evaluator, which is a registered design and not an independent reader.

The historical bundle under `docs/builds/first_cycle_20261029/run_bundle/`
predates the profile and is left as it was. Bundles without
`experiment.json` open read-only in the workbench. Component tests freeze a
disposable bundle from the current tree instead.

## Research on the Principal's own documents

Directed by the [local documents record](docs/decisions/local_documents_research_20261101.md)
and reported in the
[implementation report](docs/implementation/local_documents_research_20261101.md).

A source rule declares its documents `synthetic` or `historical`. A
historical document keeps its file name, content hash, size, media type,
declared origin and receipt time; the ledger stamps the class and refuses
a synthetic label on a historical source. A research record citing a
historical input is historical. Research records of kind `EXPERIMENT
DESIGN` and `SELECTION` may be committed without an attempt, so an
expectation is recorded before the analysis that tests it. A step's inputs
are declared as shapes, so an attempt can cite several documents and the
one design record that pins its analysis, and the tariff may be measured
in rows, documents or kilobytes. A source may hold many items per period,
identified by the document content hash. A host-run tool declared
`interface: inputs` receives every admitted input.

`experiments/local_documents/` holds the setup, profile, host-run
calculator (`term-count`, `table-stat`), evaluator and researcher program.
`workbench/local.html` and `workbench/local_session.py` drive it: charter,
imports, designs with expectations, host-run analyses with conclusions,
candidates derived from the conclusion by the researcher's declared rule,
recorded selections, Theme proposals, independent checks, Principal
decisions, revisions, stop and resume. The evaluator recomputes each cited
analysis with its own code and fails a Theme whose conclusion does not
recompute. Everything runs in the workbench process under separate tokens.
No OS isolation. No forward standing.

