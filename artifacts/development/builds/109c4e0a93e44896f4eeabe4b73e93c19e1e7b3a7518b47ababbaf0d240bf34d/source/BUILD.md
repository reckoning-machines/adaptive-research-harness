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
