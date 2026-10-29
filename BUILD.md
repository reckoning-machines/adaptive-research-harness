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

No real spending, providers, trading, Paper Book, framework adapters, public
release or license selection is included. Arbitrary scientific prose and a
general-purpose constitution interpreter remain outside capability.
