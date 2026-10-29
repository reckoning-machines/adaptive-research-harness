# Adversarial Code Audit — First Research-Cycle Build

Status: **AUDIT EVIDENCE — STATIC CODE AUDIT PLUS AUTHORIZED NON-INITIALIZING CHECKS; NO LINUX ISOLATION, GOVERNED RECOVERY OR ACCEPTANCE BEHAVIOUR CERTIFIED.**

Date: 2026-10-29. Reviewer: Claude (Fable 5.1), at the Principal's
direction. Subject: the implementation under `adaptive_research_harness/`,
`acceptance/`, `isolation/`, `build_support/` and `tests/`, read against
the admitted [CV1](../doctrines/new_speedway_constitution.md), the
[reconciled contracts](../plans/research_cycle_reconciled_20261029/contracts.md),
the [build approval addendum](../decisions/first_research_cycle_build_approval_addendum_20261029.md),
[BUILD.md](../../BUILD.md) and the
[run packet](../builds/first_cycle_20261029/run_approval_packet.md).
This file sits outside the built inventory. No implementation, test,
approval or admitted record was modified. No dependency was installed and
no host was provisioned.

## 1. Three things the reader must separate

| Layer | What it is | Standing |
| --- | --- | --- |
| Approved specification | CV1; contracts.md; the admission packet; the addendum's D1–D3 | Admitted or approved text |
| Implemented behaviour | The Python under the inventory, read line by line below | Built; enforces what the code says, not what the packet says |
| Executed evidence | 43 unit/component checks (re-run here); 18 cooperative development runs produced by another actor during this audit under `artifacts/development/` | Build-host evidence only; OS isolation unverified; Linux gate never exercised |

**The reported inventory digest does not match the tree.** The packet,
`validation.json` and `host_readiness_20261029.json` cite
`eec2f3dc42a7fbbb89ed77e07103bd86a5744dd285cb7a0794de49f51de8ff4c`. That
digest verified when this audit began. Mid-audit a second actor modified
`service.py`, `dispatch.py`, `profile.py`, `tool_worker.py`,
`acceptance/runtime.py`, `acceptance/reader.py`, added `acceptance/local.py`,
regenerated the bundle, and appended a workflow-supersession paragraph to
the addendum. The current `inventory.json` hashes to
`c5543493fce234a1596abcabc9a69bc3900496badc54572e7f2d05918fa682e7`, lists
101 files, and verifies internally. The three records above are therefore
stale against the tree. See F5.

**Gate.** The brief required no Apply 0, no governed startup and no
disposable acceptance history from this audit. None was run by this audit.
The addendum's new paragraph now authorizes disposable development runs;
the other actor used it. This audit's own execution stayed within the
original gate.

## 2. Commands actually run and their outcomes

| Command | Outcome |
| --- | --- |
| `git status --short`, `git log --oneline -8`, file inventory | HEAD `75036e0`; build tree untracked; `test.py` zero bytes |
| `shasum -a 256 run_bundle/inventory.json` | `eec2f3dc…` at start; `c5543493…` after the tree changed |
| `python3 build_support/verify.py` | `PASS`, 100 inventory files at start; `PASS`, 101 files against the regenerated inventory |
| `python3 -m compileall -q adaptive_research_harness acceptance isolation build_support tests` | exit 0 |
| `python3 -m unittest discover -s tests -t . -v` | 43 tests, OK, twice (before and after the tree changed) |
| `python3 -m acceptance --list` | 51 cases, 20 death points, two forced orders, `NOT_EXECUTED` |
| `python3 -m adaptive_research_harness --help` | usage printed |
| Read-only JSON inspection of `setup.json`, `designs_and_methods.json`, `roles.json` | Grant, tool, design and clock fields listed in §4 |
| Fabricated pure-function probe in the scratchpad over `rules`, `model`, `checkers.a`, `actors.invocation` | No Store, Engine, socket or genesis constructed. Principal control act and P-1 Hypothesis path admitted through `Rules`; wrong-bind Apply refused `WRONG_BINDING`; `invalidate-request` records `requester='@Apply'` whatever the caller |
| Read-only inspection of `artifacts/development/run-1/*.json` and `latest/E01.json` | 18 cooperative cases `PASS` under `c5543493…`, `os_isolation: UNVERIFIED` |

Build host: macOS arm64, Python 3.12.3, SQLite 3.54.0, APFS. Not the
target host.

## 3. Findings

Severity: High blocks initialization approval; Medium must be fixed or
investigated before completion; Low is improvement. Verdict: CONFIRMED by
static trace or probe; PLAUSIBLE where behaviour depends on a path this
audit could not execute; GATED where only the Linux run can show it.

### F1. High, CONFIRMED. An Apply refusal invalidates a binding that belongs to a different Transition

`adaptive_research_harness/engine.py:137-144`;
`adaptive_research_harness/rules.py:278-280`.

Failure sequence. `TR-A` and `TR-B` are both `DECIDED ADMITTED` under
`P-1`. `TR-B` holds `BIND E_b`, state `FROZEN`. The proposer of `TR-A`,
or the Principal, submits `apply {transition_id: TR-A, decision: d_A,
bind: E_b}`. `rules.do_apply` raises `WRONG_BINDING` because the bind
names `TR-B`. The engine's refusal branch tests only `payload['bind'] in
v.binds and binding_state == 'FROZEN'` and appends
`BINDING_INVALIDATED(E_b, APPLY_REFUSED, reason=WRONG_BINDING)` with
`transition_id = TR-B`, plus a `dispositions` row. `TR-B`'s binding is now
terminally invalidated by an Apply of another Transition, can be
`RELEASE`d by anyone (F2), and its proposer must re-check and rebind.
`engine.command` admits the call because the caller is `TR-A`'s proposer.
A dormant researcher with any decided proposal can do this to the active
researcher.

Violated contract. CV1 §III.8 lines 1156-1160: the boundary appends
`BINDING_INVALIDATED(E_b, …)` iff `E_b` is a `BIND` of the `TR` being
applied; lines 1173-1176: no party holds a discretionary right to cancel
a binding. contracts.md: "unique terminal disposition for the right
binding".

Smallest correction. In `engine.py:138` require
`v.binds[payload['bind']]['body']['transition_id'] == payload['transition_id']`
and exclude refusal codes raised before Apply-side evaluation
(`WRONG_BINDING`, `NO_PROPOSAL`, `NOT_DECIDED`, `UNAUTHORIZED`,
`BIND_NOT_APPLICABLE`). Regression test: two bound candidates; apply
`TR-A` citing `E_b`; assert `REFUSED WRONG_BINDING`, exactly one ref,
`obligations.bindings[E_b] == 'FROZEN'`, and `TR-B` then applies citing
`E_b`.

### F2. Medium, CONFIRMED. `invalidate-request`, `release`, `policy-decide` and `recover --continue` accept any registered design and misattribute the requester

`engine.py:101-104, 115-118`; `rules.py:297-303, 305-310, 245-249`;
`service.py:71-85`.

Failure sequence. `AD-R2.0`, dormant but authenticated, submits
`invalidate-request {bind: E_b}` for `AD-R1.0`'s registration once the
interval has elapsed. `_commit` sets `acting='@Apply'` for every caller in
`v.designs`; the event is committed with `requester: '@Apply'`. The same
caller then commits `RELEASE`. Only the operational `command` column
retains the real caller. The probe confirmed the recorded requester is
`'@Apply'` regardless of caller.

Violated contract. CV1 lines 1162-1167: elapsed invalidation is "on an
attributable request from a process acting in the Apply-boundary
continuation role, recording … the requesting role". contracts.md: "only
the internal Apply role requests binding/release"; `host_and_protocol.md`
line 207 names the requester as recorded content.

Smallest correction. In `engine.command` gate these four operations as
`apply` already is: `actor == 'Principal' or actor == proposer of the
bind's Transition`; record `requester` as the authenticated actor and
`acting_role='@Apply'`. Regression test: `AD-R2.0` requests invalidation,
release and policy-decide on `AD-R1.0`'s Transition; assert `ERROR
UNAUTHORIZED` with no Transition event; assert a lawful request records the
real requester.

### F3. Medium, CONFIRMED. The fixture commits driver-built proposals and reservations under the researcher's identity with no adversarial mark

`service.py:152-155`; `acceptance/local.py:118`;
`acceptance/cases.py:24-29, 217-235`.

Failure sequence. `adversarial-command` forwards any of `propose`,
`reserve`, `attempt`, `settle`, `research-commit` with an arbitrary payload
from the researcher's process under `AD-R1.0`. `negative_proposal` and
`C05` do exactly that, and `C05` leaves a driver-built proposal `COMMITTED`
and funded. The `PROPOSED` event is byte-indistinguishable from the
program's output; the `case` string is a request-level label, not ledger
content. Nothing prevents the driver from then obtaining a Check, a `P-1`
decision and an Apply for such a proposal.

Violated contract. contracts.md, executable actors: "The test driver … may
not construct a proposal and submit it using the researcher's identity.
Test mutation requests remain explicit adversarial inputs, never
attributed as successful researcher output."

Smallest correction. Add an actor-side `propose-mutated` operation that
derives from the program's own candidate and writes
`content.adversarial_case` into the immutable proposal; refuse
`adversarial-command` for `propose` and `research-commit`; have the reader
assert that every `PROPOSED` by a design either carries that mark or cites
a committed `RESEARCH_RECORD` by the same actor. Regression test:
`adversarial-command propose` returns `INVALID_CASE`; the C05 and R14
schedules pass through `propose-mutated`.

### F4. Medium, CONFIRMED. Checker funding is admitted for a forbidden subject; `forbidden_subjects` grant content is never read

`rules.py:11-24`; `model.py:118-121`; grant content in `setup.json`.

Failure sequence. S06 and R12: `AD-CK-1.0` reserves 0.25 under `AU-CK-A`
with purpose "Check of TR concerning AU-CK-A", admits an attempt, computes
and only then is refused `OWN_SUBJECT` at `check-commit`. The grant is
charged for a verification purpose it never held. `rules.independence`
hardcodes two patterns; the grant's `forbidden_subjects` list is
decorative, and both Checkers only test that it is non-empty.

Violated contract. CV1 §III.5 lines 663-669: a Checker reservation's
purpose must be a verification purpose the Authorization declares; §III.7
lines 986-988: the subjects a holder may not check are Authorization
content.

Smallest correction. Evaluate `independence(v, actor, g, proposal)` inside
`View.scope` for `Check` purposes so the reservation is refused
`PURPOSE_OUT_OF_SCOPE`; bind the own-subject predicate to a structured
`forbidden_subjects` field. Regression test: own-subject reservation
refused; `budget AU-CK-A committed` unchanged; no attempt exists.

### F5. Medium, CONFIRMED. The reported inventory is stale, and the local fixture regenerates the inventory as a side effect

`acceptance/local.py:231-232` calls `freeze()` on every invocation.
`validation.json`, `host_readiness_20261029.json` and the packet cite
`eec2f3dc…`; the tree now carries `c5543493…`. `BUILD.md` says passing
checks do not approve a changed build; the fixture nonetheless rewrites the
candidate digest whenever it runs. Smallest correction: remove `freeze()`
from the runner, make it assert `verify_files` against the committed
inventory instead, and re-issue validation and packet records for the
digest the Principal is asked to approve. Regression: a run with a modified
module fails `ARTIFACT_CHANGED` rather than silently re-freezing.

### F6. Medium, CONFIRMED. One refused genesis permanently poisons the store

`engine.py:172-174`. A malformed or mistyped first genesis appends a
`REFUSAL` to the Transition ledger. Every later genesis sees
`v.transitions` non-empty and refuses `GENESIS_SCOPE`; the store can never
reach Apply 0. CV1 line 1685 says every ledger is empty before Apply 0; the
implementation makes a preserved pre-genesis refusal part of that ledger.
Smallest correction: keep pre-genesis refusals in the `requests` receipt
only, or let genesis proceed when the only Transition events are
`@genesis-refused` refusals. Regression: refused genesis followed by exact
genesis commits Apply 0.

### F7. Medium, CONFIRMED. The independent reader cannot expose most admission defects

`acceptance/reader.py:17-41`. It checks sequence contiguity, body hashes,
applied-`n` contiguity, consumed-versus-invalidated disjointness,
settlement uniqueness and committed totals. It would pass with F1's
cross-Transition invalidation, with an `APPLIED` that cites no `PASS`
Check at its base, with an Apply citing another Transition's `BIND`, with a
`BIND` whose reservation purpose is not its Transition, with an attempt
above allowance or cap, and with a `RESERVATION` whose `funding_ref`
differs from the proposal. Add those reconstructions; they need only the
`history` API already used. Most case assertions in `cases.py` read
`budget` and `obligations`, which are the implementation's own `View`.

### F8. Medium, CONFIRMED. B10 as specified cannot be exercised, and no path yields `LEDGER_UNREACHABLE` or a constitutional `STOP`

`cases.py` B10 stops the whole core and asserts a connection error. With
both ledgers in one SQLite file no Transition-ledger-only outage exists, so
`LEDGER_UNREACHABLE` is never raised (grep: only re-raised at
`engine.py:132`). Neither Checker ever emits `NOT DETERMINABLE`, so
`rules.py:230`'s `STOP` derivation and `STOP_PENDING` are dead. The
completion report must say B10 was substituted and R14's `STOP` branch is
unreachable rather than listing them as executed.

### F9. Low, PLAUSIBLE. Lineage cap aggregates reservations under every grant

`model.py:107-113`. With a lineage filter the grant filter is skipped, so a
lineage's usage under a superseded grant counts against the successor
grant's cap for ever. Conservative, but after `AU-RP-1` is superseded the
same lineage may never fund again. Decide whether the cap is per grant and
make the sum match.

### F10. Low, CONFIRMED. Some refusals are returned as operational errors and not preserved

`engine.py:92-93` (`UNAUTHORIZED`, `NO_PROPOSAL` on apply) and `:114`
(`NOT_INITIALIZED`) raise before `_commit`'s refusal path. CV1 §III.7
line 1058: every refusal is preserved. `R01` accepts `ERROR`, so the
acceptance run cannot tell the difference.

### F11. Low, CONFIRMED. The core holds its write transaction across tool IPC

`dispatch.py:33-47` issues `describe` to the tool socket inside `BEGIN
IMMEDIATE` and `engine.lock`. A paused or hung tool stalls every command
for up to the 30 s socket timeout. Move `describe` before the transaction.

### F12. Low, CONFIRMED. A second run-permission route now exists in the production module

`profile.py:33-41` `development_permission` grants `allow_apply_zero` on a
`DISPOSABLE.json` marker and file verification only. No systemd entry point
calls it; `acceptance/local.py:77` does. It is inside the inventory and
must stay unreachable from `run_core`; a `require(sys.platform != 'linux'
or os.getuid() != 20000)` guard would make that explicit.

### F13. Low, CONFIRMED. Local fixture evidence is weaker than its trace suggests

`acceptance/local.py:31-45, 55-67, 88-93, 205-211`. Identity is a shared
token plus a caller-supplied `pid`; `local_quiescence` uses `os.kill(pid,
0)` and is subject to pid reuse; `artifact-probe` mutates the in-memory
hash and so always refuses; the "independent reader" runs in the driver
process. All 18 recorded passes carry `os_isolation: UNVERIFIED`, which is
correct. R01, R12, R13, T06 and T07 therefore prove ledger logic only.

### F14. Low, CONFIRMED. Tariffs and bounds are duplicated between grant content and code

`rules.py:142, 148, 150, 336`; `checkers/a.py:80`, `checkers/b.py:68`.
Checker cost 0.25, research tariff 1.00/2.00, threshold 2, the seven-day
duration and the observation period window are literals. Both are
inventory-covered, so no unbound input exists, but a lawful grant change
alone would be refused by code.

### F15. Low, CONFIRMED. The unit suite never executes most admission predicates

No test calls `do_attempt`, `do_propose`, `do_check_commit`, `do_decide`,
`do_policy_decide`, `do_bind`, `do_apply`, `do_release` or
`do_research_commit`. The 43 checks cover encoding, tools, `View`
arithmetic, a few `Rules` entries, Checker criteria and the carrier. The
probe and the cooperative runs now exercise those predicates; the unit
suite should too.

### F16. Low, PLAUSIBLE. Unreadable `/proc` is treated as a dead process

`host.py:17-19` returns `False` on any `Refusal`, so with `hidepid` or a
transient read error a live old worker is treated as quiescent. Fail
closed: propagate the error as `WORKER_NOT_QUIESCENT`.

### F17. Low, CONFIRMED. Inventory and fingerprint gaps

`isolation/host_fingerprint.py:20-29` hashes only modules loaded at import
of seven entry points and the interpreter binary. Shared libraries
(`libpython`, `libsqlite3`) and lazily imported stdlib modules (`uuid`,
`tempfile`, `concurrent.futures`, `pwd`, `grp`) are not covered. The
`ATTEMPT` body carries `admission_generation` (`engine.py:128`), host pid,
start ticks and boot id, inside an authoritative Evidence record.

### F18. Info. Checker independence hardcodes the A1 exception

`checkers/a.py:46-47`, `checkers/b.py:42-43` fail `independence` for any
Checker that declares a provider, rather than reading the grant's
`provider_diversity` content. Correct for this build, wrong for any later
grant with a real provider.

## 4. Answers to the seven questions

1. **Bootstrap and actors.** The ten-design setup completes through the
   public commands in cooperative mode: the 18 development traces show
   `N=16`, sixteen `PASS` Checks by `AD-CK-1.0`, `AU-CK-A` committed 4.00.
   The probe admitted both a Principal control act and a `P-1` Hypothesis
   through `Rules`. Researcher and Checker logic runs in the actor's own
   process from a committed closure, and `check-commit` must equal the
   finished receipt. Checks cover all six supported classes. No canned
   approval exists; F3 is the bypass that does.
2. **Authority and isolation.** Peer UID to actor to every command is
   traced in `service.py:47-52`; tools cannot reach the core socket or
   database by group and directory mode; the clock accepts reads from the
   core only. F2 is the authority gap. All isolation claims are GATED.
3. **Accounting and transactions.** Predicates and writes share
   `BEGIN IMMEDIATE` under `engine.lock`; `View` is rebuilt from events;
   `requests`, `applied`, `dispositions` and `dispatch_claims` carry
   durable uniqueness; the lifetime `flock` excludes a second core. The
   `dispatch_claims` receipt gates `TOOL_RECEIPT` settlements and
   `check-commit` equality; it is a receipt used as an anti-forgery check,
   with `UNKNOWN` settlement always available. F4 and F9 are the gaps.
4. **Funding references and admission.** Prospective reference is
   enforced literally (`rules.py:88-93`), collisions strand the proposal,
   and C05 exercises both orders. Stale base, recheck, suspension, `BIND`,
   atomic refusal plus invalidation and `RELEASE` are implemented. F1 is
   the incorrect terminal disposition.
5. **Dispatch and recovery.** Claim before handoff; `UNCERTAIN_OLD_ATTEMPT`
   refuses every pre-restart attempt; replacement work requires a
   root-written quiescence receipt naming the old core and worker
   generations. Quiescence proves no future dispatch, not no execution, as
   the code and `BUILD.md` state. F11, F16 noted. Never resuming an
   undispatched attempt is a deliberate liveness trade.
6. **Checker and test independence.** Checkers import only `encoding` and
   `contracts`, enforced by a test. Checker A's recomputation mirrors tool
   A's algorithm and B's mirrors tool B's; a shared threshold defect would
   survive. Oracles: F7 and F13.
7. **Inventory.** Verified; F5, F12 and F17 are the gaps.

## 5. Blockers before requesting initialization approval

- F1: cross-Transition invalidation.
- F2: role-free invalidation, release and policy-decide with misattributed requester.
- F3: driver-built proposals attributed to the researcher.
- F5: re-freeze the inventory once, re-issue validation and packet for the digest actually proposed, and stop the runner regenerating it.

## 6. Defects the gated acceptance runs must investigate

- F4: own-subject reservation cost and `forbidden_subjects` binding.
- F6: refused-genesis poisoning (add a case before R16).
- F7: strengthen the independent reader before it is cited as evidence.
- F8: record B10 and the `STOP` branch as substituted or unreachable.
- F9: lineage cap across grants, exercised after a supersession.
- F10: preserved versus operational refusals in R01.
- F16: unreadable `/proc` on the target host.

## 7. Nonblocking improvements

F11, F12, F13, F14, F15, F17, F18.

## 8. Disposition

**Ready for gated runtime validation after the four named fixes in §5.**
The core enforces the reservation, attempt, settlement, fence, prospective
funding, Check, decision, binding and Apply contracts it claims, with one
confirmed contract violation (F1) and one authority gap (F2) that are each
a few lines to correct. The acceptance programs can expose most violations
but not the ones in F7, and their attribution of driver-built proposals
(F3) must be fixed before any run is cited as researcher evidence. Linux
UID, socket and cgroup isolation, governed recovery on the target host, and
every death schedule remain unexecuted and unverified; the eighteen
cooperative passes are build evidence under `os_isolation: UNVERIFIED`.

`ΔO/ΔS/ΔA` of this audit: **`0/0/0`**. It adds evidence only.
