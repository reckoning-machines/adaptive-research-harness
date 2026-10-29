# Adaptive Research Harness — First Working Research Cycle

Status: **PROPOSED IMPLEMENTATION PLAN — NOT ADMITTED; NO CODE AUTHORIZED.**

Revision 2, 2026-10-29: reconciled against the adversarial review and latest
setup packet. The [remaining decision packet](../decisions/first_research_cycle_build_decision_proposed_20261029.md)
separates build authorization from exact-artifact initialization/run approval.
The [reconciliation](../audits/adversarial_first_cycle_reconciliation_20261029.md)
records every disposition; the [implementation corrections](research_cycle_reconciled_20261029/contracts.md)
are part of this plan. No implementation is authorized by this edit.

Date: 2026-10-29. Description: **A constitutional harness for evolving
investment hypotheses, strategies and research agents.**

This plan answers the [feasibility audit](../audits/feasibility_coherence_public_library_20261029.md)
against the current docs-only checkout. It proposes a working core rather
than extraction of the scripted presentation. The
[naming direction](../decisions/project_rename_20261029.md) authorizes this
document, not its execution. The project remains private, with no license
selected and no public release proposed by this milestone.

Governing baseline: [CV1, revision 12](../doctrines/new_speedway_constitution.md),
SHA-256 `c56a9cf50a7e9efadad8f2f2be6605e82c758f18d4096ba07eaaf86a8f8b7a64`,
as [admitted](../decisions/cv1_admission_20261019.md). Historical titles and
identifiers remain valid. CV1 governs if this plan conflicts with it.

## 1. Exact milestone

Implement one private, single-host research cycle with one active Research
Agent Design, independent Checker execution, and two deterministic synthetic
tools. A caller reserves units, records an attempt before work, commits the
result or failure, settles simulated cost, proposes a Hypothesis registration,
obtains an independent Check and an authorized decision, and reaches Apply
or a preserved refusal. Kill the process at consequential boundaries, then
recover from durable records in a fresh process. Replace tool A with tool B
through the same interface and repeat without losing history or permissions.

The milestone includes hostile *requests* to the boundary and controlled
failure injection. It does not execute arbitrary hostile agent code. Its
supported security boundary and trusted operator are specified in §4.

Included transition classes are the ones needed for the admitted setup and
cycle: exact genesis, checked Observation/Checker/Research grant acts,
Agent Design registration, the initial limits and Theme registration,
Hypothesis registration under `P-1`, and checked grant revocation/supersession.
The narrow existing Principal
control suspending P-1 for AU-RP-1 is included for B12; general constitutional
interpretation or upgrades remain excluded.
Principal control acts retain their direct-authority path. Supporting Evidence
operations include declared synthetic observations, Research Records,
reservations, attempts, settlements, close, fence, bind and release. Transition
operations include immutable proposal, Check, decision, Apply, refusal and
binding invalidation. Unsupported classes have no mutation path.

Exclusions: Paper Book, Strategy Runner/Decisions, paper allocations and fill
simulation, live trading, real providers, network data retrieval, LangGraph
and MiroFish adapters, arbitrary code generation/execution, broad UI work,
general constitutional interpretation, constitution/Standard text upgrades, public
distribution and licensing. No forward-performance or investment-edge claim
is part of completion. Predictions, Outcomes and full `ES-1.0` evaluation
execution are deferred; Hypothesis registration must still carry their
required resolution and initial method commitments and pass every applicable
registration criterion. No `SUPPORTED` or `CONTRADICTED` standing is produced.

This is a smaller first slice toward PD-006's demonstrations, not completion
or replacement of either demonstration. A run that only logs spending or
accepts a hard-coded Check result does not meet the milestone.

## 2. CV1 prerequisites that cannot be removed

Use [PD-009](../decisions/principal_decision_009_genesis.md) as amended and
the admission record. Do not optimize startup by inserting already-active
rows or extending the genesis waiver.

| Setup | Required behavior |
| --- | --- |
| Before Apply 0 | Both logical ledgers empty; the Evidence boundary already answers from its declared clock. No Paper Book exists |
| Apply 0 | Principal applies exactly CV1, `AD-CK-1.0` and `AU-CK-A` under the one-time waiver. No research grant or other registration is bundled into it |
| Apply 1–2 | Checked `AU-OBS-1` and initial limits, with zero exploratory pool. First Check is funded by `AU-CK-A` alone; proposer budget is `N/A` |
| Apply 3–12 | Register the ten initial Research Agent Designs with exact artifacts, provenance and method commitments; only one needs to perform work in this milestone |
| Apply 13–14 | Register and authorize the second Checker lineage for own-subject routing, including changes concerning the first Checker/grant |
| Apply 15–16 | Checked `AU-RP-1` and `TH-G1`. Theme-bound work waits for the Theme's Apply. The pooled grant and lineage caps are not ten separate grants |
| Ordinary operation | Begins at 17. CV1 already admits `P-1`; do not reproduce the superseded extra policy-admission act |

Retain all ten initial registrations. CV1 itself fixes only the three-item
Apply-0 bootstrap, but the CV1 admission record explicitly names AD-R1.0
through AD-R10.0 as outstanding pre-genesis inputs. Removing them requires
an explicit Principal scope decision; none is approved or recommended for
this assignment. One researcher runs ordinarily; other registered grantees
participate only in bounded acceptance witnesses. Shared pool
600 and per-lineage cap 100 are recorded prototype settings; the current
accounting formula is CV1 §III.5, not an earlier table's shorthand.

The latest [setup](research_cycle_admission_20261029/setup.json) supplies the
300,000 ms binding interval, source declarations, grants and template content.
Build authorization approves these as specifications to implement; a separate
exact-artifact run approval must precede genesis. Templates are not built
Agent Design artifacts, and later measurement cannot stand in for that approval. An unset field
is an error with no fallback value. In particular, existing `SRC-E` cannot
silently change from its declared meaning to a synthetic feed. Use the
explicitly synthetic `SRC-SYN` route for this cycle and preserve the setup's
required `SRC-E` declaration without retrieving real data.

Hypothesis registration needs an active resolution source and testability,
selection basis, disjoint motivation/resolution inputs and a complete initial
method commitment. Omitting source setup because no Outcome is calculated
would make the registration unlawful. Checkers need their own reservations,
attempts and settlements even for bootstrap and Principal controls. Closure
`F` is `N/A — no Paper Book` only because no Execution Authorization has
ever applied; a missing reachable-ledger read is never represented as `N/A`.

## 3. Proposed modules and smallest storage arrangement

Recommendation, pending plan admission: Python with its standard-library
SQLite binding, one local database on a local filesystem, one trusted command
service, short-lived caller/Checker/tool processes and a thin CLI. No workflow
engine, message broker, web application or ORM is needed for the milestone.
Use the naming slug `adaptive-research-harness`; a Python module may use
`adaptive_research_harness`. This is an internal layout proposal, not a public
package release or a selection already made.

| Proposed module | Responsibility; representation |
| --- | --- |
| `contracts` | Typed requests/results and explicit CV1 record schemas, subject references, decimal units and encoding rules; no arbitrary policy loader |
| `authority` | Resolve authenticated actor to existing grantee/role; evaluate grant scope, independence and direct Principal authority from the authoritative records |
| `transitions` | Proposal/Check/decision commits, exclusive Apply, pinned interpretation and terminal binding invalidation; authoritative Transition boundary |
| `evidence` | Evidence commit, clock receipt, reservation/attempt/settlement/fence/binding admission; authoritative Evidence boundary |
| `projections` | Population, budgets, lineage, outstanding obligations and historical queries; `DERIVED`, rebuilt from ledger records |
| `storage.sqlite` | Transactional persistence of those boundaries' records, unique constraints and byte retrieval; no policy or independent authority |
| `tools` | Controlled synthetic A/B and a separately attributable Checker computation; all working state `EPHEMERAL`, returned tool records `RECEIPT` until lawfully committed |
| `service`, `client`, `cli` | Protected command ingress, identity attribution and response delivery; no client-selected currentness or unrestricted append command |
| `recovery` | Inspect obligations and continue only Apply-owned operations; actual Principal/grantee clients perform their own commands; no identity override |
| `verification` | Later executable witnesses and fresh-process runner; evidence only, never a repair writer |

Use separate append-only tables/sequences for Transition events and Evidence
events. Apply sequence `N` differs from Transition event sequence. Store
immutable proposal and artifact bytes with exact hashes in the same database
for this bounded volume; do not add a blob service. Applied History remains
the Transition ledger's applied subsequence. No writable Population State or
standalone authoritative budget balance exists. Materialized indexes and
projections must be disposable and reproducible.

Use the setup packet's WAL journaling, `synchronous=FULL`, foreign-key enforcement
and `BEGIN IMMEDIATE` for admission transactions. Confirm settings by reading
them back. Serialize read-predicate-and-append within each operation. SQLite
allows one concurrent writer and documents explicit transaction and rollback
behavior; this supports a small local writer arrangement. It does not supply
CV1 predicates or certify the application. Sources, consulted 2026-10-29:
[transactions](https://www.sqlite.org/lang_transaction.html),
[atomic commit](https://www.sqlite.org/atomiccommit.html),
[synchronous settings](https://www.sqlite.org/pragma.html#pragma_synchronous).

No open transaction spans tool execution or a human decision. `BIND`, Apply
or invalidation, and `RELEASE` remain separate durable commits even though
the two logical ledgers share a file. Only Apply-refusal plus its required
`BINDING_INVALIDATED` disposition is one atomic Transition commit. Co-location
must not collapse the cross-ledger protocol into an untestable happy path.
Read current heads afresh inside each admission transaction; a long-lived
read snapshot is not current authority. Storage contention may be retried
before effects; storage/clock unavailability must not turn into cached permission.

Milestone durability claims cover observed process death on the tested
filesystem/configuration. They do not assert survival of arbitrary hardware
failure or operator deletion. Pin actual interpreter/SQLite versions in the
verification record. No dependency is installed by this planning assignment.

## 4. Supported trust model

Trusted: the Principal, host administrator, installed boundary implementation,
declared clock implementation, operating-system access controls and database
engine. The operator can replace code or destroy data and is outside the
enforcement claim. The library is not proof against its owner.

Reference execution arrangement: a boundary service account exclusively owns
the database and its directory. Researcher, each Checker, Observation
function and Principal client have the distinct Linux UIDs specified in the
[host contract](research_cycle_admission_20261029/host_and_protocol.md).
Only the operator can install enforcement code or
alter the credential-to-actor binding. Local authenticated transport binds
the peer to an existing Principal/function/Agent Design identity; a request's
`actor` string is checked against that binding, never trusted on its own.
Credentials identify callers; ledger Authorizations still determine rights.

Researcher and Checker clients have read/query and scoped command access,
not database paths, service credentials or writable installed code. Tools
run with input bytes and a result channel only: no ledger connection,
Principal credential, peer's credential or unrestricted service channel.
Root-managed fixed tool units run under distinct unprivileged UIDs. Core
forwards requests over restricted sockets; it never launches a tool as its
own UID or loads agent-supplied Python. Runtime grantee clients execute their
pinned design programs, including proposal construction; a test driver cannot
compose outcomes under a researcher credential. Actual OS denial of database
read/write and credential access is acceptance evidence, not a role-label
assertion. Same-user development shortcuts are labelled cooperative test
mode and cannot satisfy the isolation acceptance case.

This deployment work belongs to the future admitted implementation scope;
no accounts, credentials or services are created now. Support one host/OS
arrangement first. Reusing its OS authentication and filesystem permissions
is simpler than inventing an identity provider or a hosted control plane.
The exact host mechanism is a plan-admission implementation choice.

The Checker reads committed closures through the API, runs independently
with its own grant and produces criterion-level observations. Proposer
memory, a `PASS` field supplied by the proposer and a different process name
are insufficient. CV1's lineage, grant, pinned-criteria and own-subject
restrictions all apply. PD-009's additional provider-diversity grant content
cannot honestly be satisfied by synthetic provider labels. The packet's
explicit A1 grant-supplement exception remains a Principal approval item;
all three CV1 independence conditions remain. No provider provenance is invented.

No provider secrets are required. Synthetic charge receipts demonstrate
accounting under controlled tools, not control of external billing. Future
real providers would need their own accepted cap/billing assumptions.

## 5. Proposed command and result contracts

These are operation names, not new governed objects. All fields inherit their
meaning from CV1; implementation schemas must enumerate required fields and
reject omitted grant content. Record references use ledger, sequence and exact
subject/version/content hash where applicable, never a mutable name such as
“latest hypothesis.” Principal control acts cite direct authority instead of
inventing a Principal Authorization.

Common request: protocol version, client request key, exact operation/payload,
claimed actor and applicable Authorization or direct Principal authority.
Ingress supplies authenticated peer attribution. A key is a transport retry
correlator scoped to the authenticated actor, not a new governed identity.
The accepted request digest/key is metadata on the existing ledger event;
any lookup index is `DERIVED`. Semantic identities remain CV1's own identities.

Common successful response: authoritative event references, exact subject,
relevant head/version and pinned rule versions; no implied permission for a
later operation. A refusal returns its durable record reference and CV1 reason.
Operational errors distinguish **no admission attempted**, **commit outcome
unknown**, and **authority unavailable**; they are not new Transition standings.
A process unable to write cannot claim it durably recorded a refusal. Queries
must expose this gap rather than invent a ledger event after the fact.

| Proposed command | Input and caller | Durable owner/boundary; result |
| --- | --- | --- |
| `genesis.apply` | Exact CV1 bytes/digest, initial Checker/design/grant; authenticated Principal | Transition Apply boundary; Apply 0 only, exact enumerated content; reject nonempty/re-genesis |
| `transition.propose` | Immutable proposal, `TransitionId`, base, class, mutation, declared delta/consumption, subject/artifact references and funding reference; permitted proposer | Transition ledger, Propose; proposal sequence, no population change |
| `research.reserve` | Existing Research/Checker grant, amount/unit, lawful purpose and bounded expiry; grantee. Identity is the committed Evidence sequence, not a client reservation ID | Evidence; `RESERVATION` or preserved refusal at current head/fence/cap |
| `research.attempt` | Reservation, step, input hash, dispatch index, estimate maximum/unit and pinned tool; grantee | Evidence; deterministic attempt tuple `(reservation, step, input hash, dispatch index)` with `PENDING` liability, or refusal before work |
| `research.record` | Typed claims, closure, result/failure bytes/hash, exact dataset snapshot/hash, source cutoff, parameters, tool version/hash, reproducibility binding, search family/lineage and attempt attribution; authorized Research/Checker caller for the kind | Evidence; immutable Research Record or refusal. This operation cannot commit an Observation or Check |
| `research.settle` | Exact still-pending attempt, amount/unit, provenance and reservation/grant linkage; original grantee including after close/revoke, or Principal | Evidence; one settlement effect or `ALREADY_SETTLED` / `INVALID_SETTLEMENT`. Above-maximum actual is counted in full |
| `research.close` | Reservation reference; original grantee under applicable rules | Evidence; `CLOSED`, releasing only unused allowance; pending liabilities remain; frozen close refused |
| `funding.fence` | Research/Checker Authorization reference; Principal only | Evidence; `FENCE` stops new funding by Evidence order, closes reservations, retains pending maxima and existing binding eligibility |
| `observation.commit` | Declared synthetic slot/source/revision, payload, provenance, claimed times and result form; Observation function | Evidence; boundary supplies receipt/time/sequence; source permissions verified. No client assigns witnessed time |
| `transition.check` | Transition, checked base, pinned CV1/ES-1, closure `(E,N,F)`, identity/independence evidence, every criterion finding and own funded work; independent Checker | Transition Check event, `PASS`/`FAIL`/`STOP` with the CV1 distinction, never an Apply |
| `transition.decide` | Exact proposal and Check, base, decision and deciding authority; authenticated Principal only; a caller may request evaluation of P-1 but only the Apply boundary/continuation may produce that decision | Transition decision event; a checked proposal is still unapplied |
| `transition.apply` | Decided Transition, Check/decision references, current base and any required binding; Apply role | Applied History append, or preserved refusal. Principal controls use direct authority and no research binding; metered registrations use the protocol below |
| `binding.invalidate` | Exact bind and attributable continuation request; clock receipt and grant interval for elapsed case | Transition boundary only; terminal `BINDING_INVALIDATED`, atomically excluding Apply of that binding |
| `binding.release` | Exact bind plus durable invalidation reference; Apply role only | Evidence; `RELEASE` after authoritative Transition read; no timeout-only release |
| `record.get`, `history.read`, `state.at` | Exact ledger/sequence or subject and as-of marks; read access | Read authoritative records; derive Population State at `N`; return pinned versions and evidence marks, not a new state carrier |
| `budget.read`, `obligations.list` | Grant/lineage/subject plus as-of/current selector | Derived accounting and pending/frozen/decided-unapplied obligations from reachable ledgers; label as-of marks |
| `command.lookup` | Authenticated actor + request key/digest and operation's semantic identity | Read ledger-backed result/refusal; absence is not proof a competing command cannot commit; never consult client memory as authority |
| `recovery.inspect`, `recovery.continue` | Exact subject references; service inspection/Apply continuation only. Principal settlement comes from Principal ingress; grantee operations from the actual grantee process | No recovery service may synthesize grantee or Principal attribution |

`BIND` is an internal Evidence operation called only by the Apply boundary
after a metered registration is decided. It is not a researcher endpoint.
Restrict `binding.*` transport routes to the installed continuation role;
ordinary readers cannot impersonate that role.

To fund a pending registration, use the proposed **prospective Evidence
sequence** construction in the [corrections](research_cycle_reconciled_20261029/contracts.md#reservation-reference-ordering).
It needs explicit Principal confirmation in the remaining decision packet.
A proposal names a numeric future Evidence sequence, never a client-created
reservation identity. Propose first, then conditionally append the reservation
at that sequence with purpose exactly this Transition. A collision or crash
may strand the proposal: preserve it and create a new proposal/reference;
never mutate the old proposal, rebind by purpose alone, or substitute a later
reservation. Check/Apply require the exact committed record and matching
actor/grant/purpose. Prediction of a number establishes no reservation.

### Retry and unknown commit outcome

Durable uniqueness on `(authenticated actor, request key)` commits with the
owning event(s), checking a digest of exact request bytes. Same-key same-bytes
returns the original receipt; changed bytes conflict. Domain uniqueness still
refuses a newly submitted duplicate attempt, settlement, bind or Apply.
Research Records may be plural per attempt; no new one-record-per-attempt
identity rule is invented. Never settle a library retry twice.

SQLite transactions serialize commits, not external actions. A process-lifetime
OS writer lock excludes a second service before it accepts commands. Per-attempt
durable dispatch-claim receipts serialize handoff; they suppress duplicates
and grant no authority. No lock/claim absence proves non-dispatch. After lost
response, repeat the same key or inspect exact durable effects. Do not use a
snapshot's absence to authorize a new effect.

Fresh recovery does not redispatch an old PENDING attempt in this milestone.
Before retrying the same work, the trusted host supervisor must establish that
the original service/worker generation and queued handoffs cannot still dispatch.
A lease timeout, PID number alone, missing receipt or cancellation request is
insufficient. Without quiescence, refuse replacement dispatch operationally,
retain liability, and permit lawful settlement/inspection. With quiescence,
recover an exact receipt or settle UNKNOWN at the admitted maximum; a rerun
uses a new dispatch index and fresh funded admission. Quiescence proves no
future old dispatch, not that old work never occurred. No exactly-once external
action guarantee is made. The detailed concurrency schedules are acceptance
cases C01–C07 in the revised specification.

### Deterministic checks and Checker judgments

The core deterministically checks role/grant scope, immutable identity and
hash bindings, sequence/head consistency, accounting, independent lineage,
required criteria/closures, current pinned versions and permitted decider.
It cannot establish substantive scientific validity just by validating JSON.

Each Checker independently recomputes from raw committed inputs without
importing A/B, the other Checker or core admission predicate implementations.
Cross-checking A with B alone is insufficient. The Checker recomputes tool results and examines testability,
declared difference/restatement, motivation/resolution separation, selection
basis and initial methods. For the milestone, use a registered deterministic
Checker design covering every startup class, in-scope grant revocation,
P-1 suspension control and the narrow synthetic hypothesis template. The
latest [Checker matrix](research_cycle_admission_20261029/checker_contract.md)
plus the corrections specifies criterion-level execution for each class.
It derives every finding from committed records and artifacts, not expected
test labels. Out-of-capability content produces no `PASS` and requires an
authorized capable Checker. Lack of checker capability is not automatically
a constitutional `STOP`: known failed criteria are `NOT MET`/`FAIL`; an
actual missing constitutional identity/meaning/authority is `NOT DETERMINABLE`
and `STOP` under §III.8. Preserve operational inability separately when no
valid Check can be completed. This bounded checker proves process mechanics,
not general natural-language scientific judgment.

## 6. Accounting, tool and clock interfaces

Keep units exact (decimal representation, no binary float rounding or NaN).
For each reservation, `C = settled actuals + pending maxima`. Open usage is
`max(reserved amount, C)`; closed usage is `C`. Grant committed total is
`ΣC`; reserved total is summed usage. Headroom is `max(grant−ΣC,0)`;
spendable is `max(grant−Σusage,0)`. An overrun never disappears through a
close, fence, successor or negative unused balance. Lineage caps include
closed pending liabilities. Implement these as derived queries from CV1
facts, not mutable counters with a separate repair path.

Before each dispatch, the boundary must have durably admitted its attempt.
The service may enqueue work only after commit. `tool.describe` returns the
installed tool/version/hash and supported deterministic input contract;
`tool.estimate` computes the maximum under the grant's rule;
`tool.run` accepts exact committed input bytes and attempt reference and
returns result/failure bytes, actual simulated usage and provenance.
`tool.receipt` may retrieve an exact previously recorded tool response, but
the response is only a receipt: an authorized settlement still passes the
Evidence boundary. The tool has no commit command or authority to expand a
grant. Limits on input size and fixed simulated charges belong to the
supplied tool/grant declarations, not undocumented constants in code.

A and B independently implement the same deterministic synthetic
calculation. Record distinct implementation hashes and retain both versions.
The supplied Agent Design and grants must explicitly permit both tools from
the outset for the interchange witness; otherwise first admit the required
successor design/grant. Tool replacement is never a license to substitute
the provider/model fixed to an Agent Design under D-14.

On a caught tool failure, commit negative Research Evidence and valid actual
simulated cost, including any nonzero failure charge. On lost/uncertain
dispatch, keep `PENDING` at the maximum. A pending record without response
does not prove no dispatch. Recovery may settle from an exact receipt, or
settle `UNKNOWN` at the admitted maximum. Any uncertain re-execution is a
fresh dispatch index with a newly funded attempt; after a fence it refuses.
Before such replacement dispatch, establish old-generation/channel quiescence
as specified in §5; no worker-liveness inference comes from a missing receipt.
Do not add a mutable “sent” flag that is treated as an authority. The
synthetic test driver can prove what ran for witness comparison, but that
driver's memory is never production recovery authority.

The storage interface supplies begin/commit/rollback, exact immutable reads,
head reads, ordered append and uniqueness enforcement to the two boundaries.
It does not expose generic append to clients. Historical schema readers
interpret the pinned versions; no migration may rewrite admitted content.
Use the exact canonical JSON/decimal/time rules already supplied in the
[host contract](research_cycle_admission_20261029/host_and_protocol.md), with
the corrections' defined attempt-step and input-byte contract. Retain raw
artifact bytes and do not normalize a governed statement.
Any change to CV1's identity meaning is a Principal stop, not a serializer
choice. These details exist before building; executable hashes are measured after building.

The clock interface is `read() -> (t,E)` served by the Evidence boundary.
It advances as a declared clock, not as a consequence of Evidence appends.
A clock read alone commits nothing. Use one controllable synthetic clock
provider for witnesses, external to the killed caller/service process, with
a declared timeline retained by the test supervisor across restarts. Only
the Evidence boundary answers it to callers. The supervisor may advance
time, never dictate a Check/Apply outcome. Failure to reach this clock means
no time; clients do not reuse a previous receipt or wall clock. Restarting
all components must preserve the declared clock timeline or refuse time-
dependent operations; it must not reset expiry. This is a synthetic-time
test arrangement, not a production clock assurance claim. Reads are
nondecreasing across restart; rollback below any durable witnessed time
refuses. Settlement requires no fresh clock read and establishes no expiry
closure; the corrections enumerate time-dependent operations and bounded
reservation expiry.

## 7. Binding and recovery algorithm

The Apply role reads only authoritative state to choose the next step:

1. If already applied, return its Apply reference and do not repeat it.
2. If the base changed, obtain a new Check and decision under the new base;
   preserve the immutable proposal and old Check/decision. No stale approval
   becomes current through transport retry.
3. For a metered registration, obtain `BIND(TR,R)` under §III.5. It requires
   an open eligible reservation and a decided, unapplied Transition with no
   outstanding prior binding/disposition release. Commit `BIND` separately.
4. At the Transition boundary, validate current base/Check, Authorization,
   `P-1` conditions and binding identity. Apply consumes that binding. On
   Apply-side refusal, atomically append refusal and its invalidation.
5. With no disposition, Apply may still win after the numerical interval;
   that interval allows an attributable invalidation request with a verified
   clock receipt and strict `t−t_b > interval`, not an automatic deadline.
6. A committed invalidation excludes later Apply of that binding. Only then
   may the Apply role commit `RELEASE` by reading the invalidation. An Apply
   consumes the binding without any Evidence completion or release record.
7. Derive subsequent reservation standing from both ledgers. An invalidated
   but unreleased binding remains frozen. Unreachable authority leaves it
   frozen and refuses dependent spending. Release revives neither a fenced
   grant nor an expired reservation. A fresh bind follows required recheck/
   decision and prior terminal disposition/release, never a local timeout.

Fences stop new attempts but do not retroactively erase an admitted attempt's
dispatch permission or a binding's funding eligibility. A fence alone may
leave registration eligible to Apply; revocation at the Applied History head
still defeats its Authorization predicate. Settlement remains admissible
after close, expiry, fence or revocation for a valid pending attempt and
permitted original caller. Recover these distinctions, not a generic
“everything cancelled” state.

Startup scans derive pending attempts, decided-unapplied transitions and
binding/release obligations. The service continues only Apply-boundary-owned acts. The authenticated
Principal can settle; grantee-owned work resumes only in that grantee's
pinned process. A new process name or role parameter conveys no authority. Inspection does not authorize dispatch,
release, funding, a Check or a Principal decision. Failures and refusals
remain available to historical readers even if later attempts succeed.

## 8. Worked cycle to implement

Question: **In a synthetic equity-flow corpus, does large forced selling
follow volatility spikes often enough to justify a narrower hypothesis?**
This is controlled research, not a trading decision or forward standing.

Use the latest setup packet's exact values; these remain build targets until
separate approval of the built run inventory. No label or expected result
may be inserted by a test driver.

1. After Apply 1 and before proposing TR-16, the authenticated Observation
   process commits the declared `SRC-SYN` formation corpus. TH-G1 cites its
   exact committed closure. Finish all checked setup through 16.
   Its hash, source revision and receipt are recorded. Researcher `AD-R1.0`
   has its active Theme scope and permitted A/B tools.
2. Researcher reserves 3 units for `TH-G1`. The boundary commits an attempt
   for A, maximum 1 unit, before dispatch. Tool A computes from twelve
   synthetic rows that selling follows eight events, with two large-selling
   cases; its result and a fixed 1-unit simulated charge are returned.
   The researcher submits its Research Record and settlement under its own
   authenticated identity; the boundaries commit exact bytes and 1-unit cost.
   Closing releases 2 unused units. Nothing is `SUPPORTED`.
3. Researcher proposes an immutable Hypothesis focused on the large-selling
   condition, naming a declared future synthetic resolution set distinct
   from formation inputs, falsifier, stopping rule, methods, selection basis,
   base and a prospective numeric Evidence-sequence funding reference. Then
   conditionally reserve 2 units at that sequence for the already-proposed
   Transition. A lost sequence race preserves refusal and requires a new
   proposal. Prior research cost remains on its own record.
4. Checker A reserves from its own grant, records its verification attempt,
   reads the committed closure and independently recomputes the result and
   each registration criterion. Its verification settles 0.25 simulated units.
   Its Check includes the historical/synthetic findings and can
   `PASS` registration without claiming forward evidence.
5. `P-1` decides only if its enumerated conditions hold. The Apply role
   obtains the registration `BIND`. Kill the service before Apply. A fresh
   service reads that binding and the decided Transition; if base, grant,
   policy and other admission conditions still hold, Apply commits exactly
   once. The binding is consumed by that Apply alone.
6. Query history, remaining funds and the admitted Hypothesis. The original
   grantee closes the consumed registration reservation when lawful; it is
   not donated to a new agent. Next permitted action is another funded
   research step. Prediction/Outcome execution is outside this milestone.
7. Invoke B on the same committed input under a new lawful attempt and its
   own 1-unit declared simulated charge. Preserve the A result and original
   registration. B's equivalence does not create a new membership or grant.
   Boundary refusals remain identical for unauthorized, unfunded and stale
   requests regardless of which tool is selected.

The competing branch deliberately applies another checked change before
step 5. The old base cannot Apply; refusal and binding invalidation are
durable where binding exists. The next permitted action is release, fresh
Check/decision and eligible rebind, not relabelling the old approval. A tool
failure branch records the error and charge, and makes no registration claim.
Every result above must be computed by the real core and tool interfaces;
the acceptance driver cannot assign status, budget or approval fields.

## 9. Implementation order and gates

| Cut | Deliverable | Required exit evidence |
| --- | --- | --- |
| 0. Build decision | Principal confirms remaining D1–D3 and authorizes coding against exact specification bytes | No initialization or execution of governed startup is authorized |
| 1. Build and offline validation | Implement boundaries, persistence, both Checkers, researcher, tools, fixture and isolation templates; run non-initializing unit/component tests | Freeze exact source/executable/config/design/tool/method hashes and schema/runtime/host inventory; deliver a concrete run-admission bundle |
| Gate R. Exact-artifact approval | Principal approves the produced immutable build/run manifest and exact startup/test scope | Required before ANY Apply-0 execution, including acceptance fixtures; no hash-filled template automatically authorizes itself |
| 2. Funded setup | Execute exact genesis and checked sequence through 16 | Sixteen computed/funded Checks, correct source timing, actual researcher attribution, no added waiver |
| 3. Controlled research | Exercise evidence, reservation, attempt, settlement, close/fence and both tools | Failure, uncertainty, shared-budget concurrency and post-revocation settlement evidence |
| 4. Registration | Check, internal P-1 decision, bind, Apply/refusal, invalidation/release | Current-base and policy-suspension rejection, reservation-reference collisions, both disposition race orders |
| 5. Fresh-process witnesses | Run original acceptance plus S/C/B12 amendments on the approved build | Actual process deaths, OS isolation, quiescence before replacement dispatch, historical inspection and complete report |

Dependency between cuts is logical, not a permission to fake funded bootstrap
while accounting is unfinished. Implement accounting primitives needed by
the first Checker before executing cut 2. Do not seed final membership,
balances or approvals through fixtures. Independent verification must inspect
the resulting ledger records and not rely only on the implementation's own
returned success flags.

The detailed [acceptance specification](first_research_cycle_acceptance_20261029.md)
is part of this proposed scope. CPOC is required for the bounded admission,
accounting and historical-continuation paths. It is used in the adopted
sense: lawful state survives persistence, real process death, reconstruction,
continuation, further death and historical verification. No CPOC PASS or
certification is claimed by writing the specification.

## 10. Decisions remaining before coding

The [single remaining decision record](../decisions/first_research_cycle_build_decision_proposed_20261029.md)
contains D1 (build now, separate exact-artifact run gate), D2 (prospective
Evidence-sequence reference with fail-closed collision), and D3 (the already
proposed synthetic Checker supplement and narrow initial tool grants).
All numerical setup, serialization, clocks and host choices are supplied;
no new open-ended architecture review is requested. Ten designs remain.
S7 is resolved by specifying a real deterministic researcher executable,
not granting authority to a human masquerading as that design.

The spec proposes no new governed identity or constitutional text. D2 is an
explicit ordering construction using CV1's existing Evidence-sequence identity,
not an authorization for client reservation IDs or purpose-only funding.
Any actual need to change CV1 meaning/authority remains a Principal stop.
Publication and licensing stay undecided and excluded.

## 11. Completion and next coding assignment

Complete only when the actual core executes the worked cycle and every
required acceptance case, including refusal, exact-once accounting effect,
unknown-commit recovery, both binding race outcomes, process death and tool
replacement; independent inspection reconstructs the same lawful state and
next action from durable records. The report must enumerate unsupported
operations and any failed witness. No failing required case is waived by
marking the package experimental.

Before adding paper simulation or framework adapters, obtain a bounded review
of those results and a separate admitted expansion plan. Research-cycle
completion does not establish CV1-wide implementation, both PD-006 proofs,
production security or investment performance.

Concrete next assignment, **after build approval**: implement cut 1, perform
offline validation without genesis, freeze the exact built artifact inventory,
and present the bounded Gate R approval. After that distinct approval, execute
cuts 2–5 against those bytes and retain the full acceptance evidence. This is
one implementation assignment with an artifact-approval gate, not another
planning round. No run occurs under approval of placeholders.

Declared plan budget: **`ΔO=0, ΔS=0, ΔA=0` relative to admitted CV1**.
No new domain objects, lifecycle transitions or decision rights. Persistence:
existing Transition and Evidence facts in a proposed transactional carrier.
Writers: their existing exclusive boundaries and authorized callers.
Selectors: authoritative heads and exact historical marks only. Representation:
ledger records `AUTHORITATIVE`; projections/indexes `DERIVED`/`CACHE`;
tool/clock responses `RECEIPT` or `EPHEMERAL` as CV1 specifies. This plan
itself remains a proposal and changes no governed standing.
