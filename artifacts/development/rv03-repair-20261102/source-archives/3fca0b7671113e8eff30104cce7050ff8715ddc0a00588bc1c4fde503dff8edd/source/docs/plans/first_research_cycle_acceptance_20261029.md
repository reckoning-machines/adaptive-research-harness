# Adaptive Research Harness — Research-Cycle Acceptance Evidence

Status: **PROPOSED EXECUTABLE SPECIFICATION — NO TESTS IMPLEMENTED OR RUN.**

Revision 2, 2026-10-29. Includes the latest setup packet S01–S08 and the
[reconciled contracts](research_cycle_reconciled_20261029/contracts.md).
Separate exact-artifact run approval is required before any acceptance
genesis; build approval permits only non-initializing validation.

Date: 2026-10-29. Companion to the
[implementation plan](first_research_cycle_implementation_20261029.md).
The admitted [CV1](../doctrines/new_speedway_constitution.md) governs. This
specification adds no authority, defaults or certification standing.

## 1. How the future witnesses must run

Start each scenario from empty ledgers through the exact checked setup, or
from a preserved lawful setup produced by those commands under the same
approved build/run inventory. Never initialize merely because artifact
hashes have been measured after a build approval. An isolated test
database may repeat the journey from empty; it does not invoke re-genesis
inside an existing history. Never manufacture balances, Check results,
membership or binding state through direct SQL writes. Fixture clock advances
and synthetic response-loss/failure controls cannot dictate admission results.

Use executable tools with pinned bytes. Their deterministic calculation and
explicit simulated usage are inputs to the real boundaries. A separate
observer recomputes accounting and verifies the ledger trace, including the
absence of prohibited effects. Every case must assert records and identities,
not only a return code. CLI output, inspection API and reconstructed projection
must agree for the same exact subject and as-of marks.

Acceptance data must state: build/commit, CV1 digest and `ES-1.0`, interpreter
and SQLite versions, OS/filesystem/storage settings, authenticated role
mapping, complete setup packet digest, tool/design/method hashes, initial
heads, schedule/fault placement, observed terminal records and fresh-process
identities. Preserve failed runs as evidence alongside later successes.

“Refusal” below means a durable refusal at the appropriate available boundary.
If storage is unavailable, the client gets an operational unknown/unavailable
response and no permission. It must not report a persisted refusal that does
not exist. Once reachable, inspect exact durable state before continuing.

## 2. Enforcement witnesses

| ID | Stimulus | Expected durable result | Prohibited effect |
| --- | --- | --- | --- |
| R01 | Authenticated researcher calls `FENCE`, submits a Check, impersonates Principal, or invokes Apply-role binding endpoints | Boundary refuses the out-of-role operation with actor/request attribution; no authorized effect. An unauthenticated transport is rejected before role resolution and is not a fabricated CV1 Transition | A client role label or knowledge of an ID grants authority |
| R02 | Two authorized callers race distinct reservations whose individual amounts fit but sum exceeds remaining spendable budget; neither independently violates its lineage cap | Serialized Evidence order admits one and preserves the other's budget refusal. Remaining capacity and liabilities recompute from that order | Both reserve the same remaining units; negative spendable budget; a cache wins admission |
| R03 | Same settlement delivered with a lost response, then resent with same key; also submit a fresh command key for the same attempt | Original-key delivery resolves to the original event. New submission records `ALREADY_SETTLED`; actual replaces pending maximum only once | Two charges, double release, or a second settlement reopens the attempt |
| R04 | Admit a pending attempt, then Principal fences and a checked revocation applies; original grantee submits valid settlement | Fence and revocation remain in their different ledgers; settlement is accepted under the former-grantee exception. Pending maximum becomes actual; new attempts/reservations refuse | Revocation erases liabilities or prevents lawful settlement; retained authentication confers new spending rights |
| R05 | Settlement has wrong caller, attempt/grant linkage, unit, negative/non-finite amount or missing provenance | Preserved `INVALID_SETTLEMENT`; pending liability remains at maximum | Invalid submission frees headroom or changes attribution |
| R06 | Controlled tool fails after admitted dispatch and returns an exact failure receipt with simulated usage | Negative Research Record plus one valid settlement; no result-dependent Check claims successful computation | Failure disappears, produces an invented result or means zero charge by default |
| R07 | Kill/disconnect after attempt admission with dispatch outcome uncertain | `PENDING` remains at maximum. Recover exact receipt and settle, or settle `UNKNOWN` at maximum. Before replacement dispatch establish old worker/service-generation and channel quiescence; rerun uses a separately admitted dispatch index | Absence of a response proves no work occurred; same attempt is blindly redispatched for free |
| R08 | Fence occurs before a retry; separately test an attempt admitted before the fence but dispatched afterward | New retry refused `FENCED`. Pre-fence admitted attempt retains its consumed dispatch permission and can settle under CV1 | Blanket cancellation of already-admitted permission; post-fence new admission |
| R09 | Synthetic adversarial charge exceeds its admitted maximum, then try more work under an existing open reservation | Actual overrun counted in full; grant and lineage totals include it; new attempt obeys headroom/cap and `OVERSPENT` checks | Old reservation allowance defeats current headroom; negative remainder offsets overrun. This injects an accounting failure case, not proof of external caps |
| R10 | Close or expire a reservation with a pending attempt | Only never-attempted allowance released; pending maximum retained, later settlement valid | Closed reservation removes pending liability or a successor resets lineage usage |
| R11 | Another lawful Transition advances the head after Check, or after decision | Stale Check/approval cannot Apply. Preserve old records; append new Check and decision at new base before any later lawful Apply | Silent proposal mutation, old `PASS` treated as approval of a new state, stale Apply |
| R12 | Proposer attempts its own Check, a same-lineage Checker checks, or first Checker checks a subject forbidden by its grant | Independence/own-subject condition fails; no usable `PASS`; costs attributed to the actual caller only if lawful work was admitted | A different worker name/model alone establishes independence; proposer grant funds independent verification |
| R13 | Synthetic result is submitted as scientific support for standing, or a tool tries to commit an Observation | Unsupported standing operation has no mutation route; wrong Evidence caller is refused; synthetic provenance retained | `SUPPORTED`, `CONTRADICTED`, capital or forward credit arises from synthetic success |
| R14 | Propose incomplete registration: missing resolution source/grace, inconsistent selection/method binding, reused formation observation as resolution input, or undeclared restatement | Checker produces criterion-level known failure where determinable; no Apply. Genuine missing constitutional meaning is separately recorded as `STOP`, not guessed | Filling missing semantics with code defaults; treating every failed predicate as a constitutional stop |
| R15 | Read exact earlier subject/version after later work and restart | Original bytes, pinned versions, refusals and results remain readable; as-of projection agrees across surfaces | Mutable-present substitution, silent result overwrite or negative evidence deletion |
| R16 | Attempt nonempty-store genesis or bundle extra grants into Apply 0 | Refusal/constitutional stop under the exact genesis restriction; no extra Apply 0 | Reusable waiver, direct fixture seeding or resetting an existing history |

For R02, arrange remaining capacity by earlier lawful commands, not a database
balance edit. Use distinct eligible grantees and values within each cap. The
winner may vary; the invariant and records may not. Exercise both possible
arrival orders with explicit barriers rather than probabilistic sleeps.

## 3. Binding, invalidation and recovery races

CV1 §III.5/§III.8 is the oracle. The two ledgers may share SQLite but the
intermediate states below must exist as separately durable commits.

| ID | Schedule | Expected durable result | Prohibited effect |
| --- | --- | --- | --- |
| B01 | `BIND`, process death, fresh continuation with unchanged lawful conditions | One Apply cites that bind; its consumption is derived from Apply alone | Waiting for or writing a separate Evidence completion/release to make consumption real |
| B02 | `BIND`; later Evidence `FENCE`, no revocation/base change; Apply | Registration may Apply if all Apply-side conditions remain satisfied. Reservation stays closed; new spending refuses | Rechecking BIND-time open/unfenced eligibility as an extra Apply condition, or reopening the fenced reservation |
| B03 | `BIND`; checked grant revocation applies; old registration attempts Apply | Apply refusal and `BINDING_INVALIDATED(..., APPLY_REFUSED, ...)` commit atomically; later release cites that invalidation | A binding bypasses inactive grant/current-base checks, or refusal commits without its required disposition |
| B04 | Clock equals `t_b + interval`, then exceeds it; request elapsed invalidation | Equality cannot invalidate on elapsed ground. Strictly later request records verified `(t,E)`, interval and requester; may invalidate if no Apply won | Local timer/old receipt substitutes for clock; interval is an automatic release or Apply deadline |
| B05 | Eligible Apply and eligible elapsed invalidation race; force each winner in separate runs | Exactly one terminal disposition for that bind. Apply-first excludes invalidation; invalidation-first excludes Apply citing it | Both terminal facts; phantom consumed bind or resurrection after restart |
| B06 | Apply-side condition fails; kill inside refusal/invalidation transaction | Either both records durable or neither; recovery handles the surviving lawful state | Refusal without invalidation or invalidation missing its refusal evidence |
| B07 | Invalidation committed; kill before `RELEASE`; fresh process releases | Bind remains frozen until release; release proves the exact durable invalidation and ends freeze under ordinary expiry/fence rules | Expiry alone releases, or an uncommitted invalidation request is enough |
| B08 | Applied binding, then duplicate Apply, duplicate release attempt or delayed old invalidation | No repeat Apply; no release of consumed binding; no terminal invalidation of an applied Transition | Duplicate membership, released consumed funding or destructive cleanup of history |
| B09 | Old bind invalidated/released; fresh eligible bind; delayed operations on old bind | Each disposition remains bound to its own Evidence sequence; old Apply refuses; fresh bind may independently Apply | Old release frees fresh binding; any binding reference is treated as interchangeable |
| B10 | Required Transition read unavailable while checking release, reservation usage or next attempt; recover later | Dependent operation refuses/unavailable with no release/spend. Later exact reads reconstruct applied/invalidated/frozen standing | Cache, acknowledgment or service memory votes for unfrozen state |
| B11 | Reservation expiry passes while bound; try attempt/close, then consume or invalidate/release | Frozen attempt/close refused. Expiry is read under ordinary rules after freeze ends; no automatic liveness guarantee | Spending during freeze; revive expired reservation; promise bounded release during outage |
| B12 | BIND; independently checked Principal P-1 suspension for AU-RP-1 applies; old policy-decided registration continues | Atomic Apply refusal + invalidation cites policy suspension and changed head; RELEASE reads exact invalidation. Old decision cannot ground a new bind. Fresh Check/decision required; P-1 remains unavailable while suspended | Binding bypasses suspension; recheck alone reenables P-1; synthetic population edits simulate the suspension |

## 4. Process-death matrix

Use real terminated OS processes, identify old/new PIDs and never pass old
in-memory state into recovery. Kill client, tool and service at their relevant
boundaries. Repeat the final historical verification after another service
death. An exception catch, new Python object or graph restart within one
interpreter is not the process boundary witness.

| Kill point | What a fresh process must find and do |
| --- | --- |
| Before reservation commit / after commit before reply | No committed reservation, or exactly the durable reservation; same request key resolves without creating two |
| Before attempt commit / after commit before dispatch | No admitted attempt means no work. Durable pending attempt means liability. Fresh recovery never redispatches that attempt in this profile. Establish old-generation/channel quiescence before a new funded retry; preserve uncertainty and settle exact receipt or UNKNOWN |
| Tool ran, before response or result commit | Preserve uncertainty at maximum until valid receipt/`UNKNOWN` settlement; never infer a negative result or zero cost from silence |
| After evidence commit, before settlement | Result/failure bytes remain; pending maximum survives; continue valid settlement |
| After settlement commit, before reply | Lookup returns the exact settlement; new-key duplicate refuses; accounting unchanged |
| After Check, before decision | Check is preserved; current base/authority/criteria determine whether a new decision is lawful; no Check-as-Apply shortcut |
| After decision, before bind | Re-read current conditions; obtain binding only if eligible |
| After bind / during Apply refusal transaction / after invalidation before release | Exercise B01, B06 and B07 separately; do not hide them inside one transaction |
| After Apply, before reply or reservation close | Membership exists once, bind consumed by Apply; return its reference and continue only ordinary reservation rules |
| During Principal control continuation | Direct Principal authority remains direct; no invented Principal grant or research reservation requirement; independent Check remains required |
| Clock provider unavailable, or all components restart | Time-dependent operation has no permission until declared clock available with preserved timeline; no local fallback or expiry reset |

The final independent reader must reconstruct exact membership, active grants,
fences, committed/reserved totals, frozen bindings, pending attempts, preserved
failures and next permitted operation. Bindings are allowed to remain frozen
when authority is unavailable; that safe lack of progress is not a failure of
the declared contract or evidence of a new cancellation right.

## 5. Tool replacement and boundary isolation

| ID | Exercise | Required observation and prohibited effect |
| --- | --- | --- |
| T01 | A completes lawful work, then B processes the same closure through a new funded attempt | Distinct tool hashes and attempts, retained A evidence, independently verified expected calculation and charges. No replacement of subject identity, grant, old result or admission standard |
| T02 | Both tools receive an over-budget or unauthorized request | Refusal occurs before dispatch for each; independent tool invocation counts show no unauthorized work. A post-work logging hook cannot satisfy this |
| T03 | B returns a forged approval, Observation or larger grant in its result bytes | Bytes may be preserved as untrusted research output; no corresponding authority, Observation or Apply is created |
| T04 | Tool swap while earlier work is pending and a registration binding is frozen | Old liabilities and binding survive; B cannot settle A's attempt under an unrelated caller or use the frozen reservation for new work |
| T05 | Different tool not named in the grant/design, or silent provider/model substitution | Request does not execute; obtain lawful successor design/grant or stop under D-14. A/B compatibility is not permission to run any tool |
| T06 | Researcher/tool OS identity attempts to open/write database, read Principal/Checker credentials or change installed service code | OS denies access in the reference arrangement. Record tested identities and file/transport permissions. Cooperative same-UID unit tests do not count as security isolation |
| T07 | Researcher sends Checker/Principal identity in request over its own authenticated connection | Transport attribution remains researcher; boundary refuses privileged effect. Possessing a payload with a valid Check reference does not confer its author's rights |

Safe retry of an admitted library command means returning its durable effect
or refusing a new duplicate without a second effect. It does **not** mean a
tool action ran exactly once. The uncertain-dispatch case must show that a
fresh attempt can incur another charge, and a fence can forbid that retry.
An unknown original may still dispatch: replacement work is not a safe retry
until the approved host supervisor establishes quiescence. Even then a new
attempt can incur another charge; quiescence does not prove nonexecution.
Explicit simulated receipts and accounting must be labelled as such on every
report. No external-billing guarantee is demonstrated.

## 6. Completion record

The future report must include a matrix for R01–R16, B01–B12, C01–C07, S01–S08, the process-death
points and T01–T07: executed/pass/fail/not-executed, durable sequence references,
observed values, prohibited effects checked, relevant build/config hashes and
limits of the observation. Include the worked cycle from the implementation
plan with actual query output and independent recomputation. Required cases
cannot disappear into a general “tests pass” summary.

Identify the boundary authority ledger and decision-surface comparisons:
Transition currentness from Applied History, research accounting from grants
and Evidence, pending/frozen state from both ledgers, and each UI/CLI/query
projection with its exact as-of marks. Classify CPOC as required for these
paths. Use the adopted certification vocabulary only with the exact executed
subject and evidence; no project-wide certification follows automatically.

Completion means all required witnesses agree with CV1, no unresolved
authority/meaning was filled by code, and another fresh process can inspect
the retained history and continue lawfully. The next expansion still requires
its own plan and Principal admission. `ΔO/ΔS/ΔA` of this specification is
`0/0/0`; it records no execution or test result.


## 7. Added reconciliation witnesses

Retain S01–S08 of the [Checker contract](research_cycle_admission_20261029/checker_contract.md).
S01 must show sixteen computed, separately funded startup Checks totaling
4.00 for CK-A on the fault-free path; no gate supplies predefined approval.
S06 must actually exercise CK-B on a CK-A/grant-chain subject. The B12
policy control uses the precise supported payload and funded Check specified
in the corrections, not a direct flag edit.

| ID | Stimulus | Expected durable/observable result | Prohibited effect |
| --- | --- | --- | --- |
| C01 | Start two core instances; pause the first across commit/handoff while starting the second | Lifetime OS lock excludes the second before sockets/dispatch. Concurrent legitimate requests to the first still rely on durable actor/key uniqueness in the owning event transaction | A timeout/PID file transfers writer or dispatcher authority; SQLite writer serialization claimed to serialize external actions |
| C02 | Concurrent same-key same-bytes and same-key different-bytes commands, lost replies and fresh service; also repeat under a new key | One original command event/receipt; conflicting payload refused; new-key domain duplicates preserve their CV1 refusal. Exact negative result survives restart | Two Research Records created by one command retry, second charge, snapshot absence treated as a completed negative outcome |
| C03 | Two tool-run requests with different transport keys for one admitted attempt; kill after claim before handoff and after handoff before receipt | One durable dispatch-claim receipt suppresses duplicate handoff. The pending maximum survives ambiguous death; no claim or marker substitutes for settlement | Same admitted maximum buys two concurrent invocations; claim treated as proof work completed or failed |
| C04 | Old core dies while tool worker is paused immediately before execution or has queued input; replacement core is live | Retry of same work refuses WORKER_NOT_QUIESCENT. Supervisor stops exact old generations/descendants, discards channels, records attributable quiescence. Then exact receipt or UNKNOWN settlement and a new funded dispatch index; both historical liabilities remain accounted | Missing marker, timeout, cancellation request, reused PID or fresh process alone proves non-dispatch; old worker resumes after replacement is treated as safe |
| C05 | Two proposals predict same next Evidence sequence; another Observation wins; kill between proposal and conditional reservation; lose reservation reply | Only the exact matching conditional reservation can use the prospective sequence. Stranded proposals and refusals remain immutable. Exact-key lookup finds the committed reservation or a new proposal is required; Checker rejects wrong-kind/grant/actor/purpose at that sequence | Client ReservationId introduced, old proposal edited, purpose-only search swaps funding, another sequence silently substituted |
| C06 | Clock outage with valid pending settlement; then try fresh reserve/attempt/BIND/elapsed invalidation; attempt far-future expiry and rollback clock | Settlement once from permitted caller, pending maximum replaced by actual without expiry inference. Time-dependent actions refuse. Supplied expiry beyond t+7 days refuses; omitted expiry computed. Restored clock below durable high-water refuses | Liability remains unpayable solely due to clock outage; cached time authorizes spending; expiry reset/reversal or client chooses unlimited duration |
| C07 | Driver tries to supply a proposal as AD-R1, sends acting_as/P-1/Observation fields, or service recovery invokes grantee methods; run actual registered researcher on success/failure inputs | Peer attribution remains actual sender; only pinned researcher derives legitimate proposal from committed Research Record. Recover only through owned roles. Trace links executable hash → peer/design → attempt → Research Record → proposal; negative input prevents positive proposal | Test driver masquerades as research, recovery manufactures actor authority, caller-supplied P-1 label creates a decision |

C04 must include a paused old worker that really could dispatch if released,
not only a process already known dead. In the failure branch the observer
checks that neither the replacement nor any post-quiescence old channel
executes. In a separate uncertain-history branch old work already ran;
UNKNOWN/new-attempt accounting must retain the old maximum as well as new
cost. This demonstrates the difference between no future old dispatch and
proof of no past execution. A well-formed pre-fence attempt known not sent in
an uninterrupted process remains eligible for its original single dispatch.

Host evidence is required for R01, R12, caller-attribution portions of R04/R13,
T06/T07 and C01/C04/C07. Cooperative tests may verify logic under an assumed
actor; they cannot certify that actor or exclude another process. A Python
private constructor for caller context is an engineering guard, not security.

Do not enforce one Research Record per attempt to satisfy C02: two genuinely
separate lawful commands may record different claims about the same work.
Only duplicate delivery of the same command is deduplicated. The reader must
reconstruct the original records, refusal history and ownership boundaries.
