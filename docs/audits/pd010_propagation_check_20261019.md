# PD-010 Propagation Consistency Check (author's check)

Status: **AUTHOR'S CONSISTENCY CHECK — EVIDENCE, NOT DOCTRINE. This is
not the independent whole-design audit, closes no finding on its own
authority, and certifies nothing.** Author: Claude, who also wrote the
propagated text. Codex's final whole-design review of the propagated
design follows this check and is the independent assessment.

Date: 2026-10-19.

Subject: [Constitution revision 11](../doctrines/new_speedway_constitution.md)
after propagation of [PD-010](../decisions/principal_decision_010_codex_audit_repairs.md)
revision 4 (admitted 2026-10-19; reviewed digest
`a47dad4069d06bbb469c300ef27361952b82193357edd1244d2edeecd2f723d2`,
verified identical before the admission was recorded). Findings are
those of the [independent audit](independent_preimplementation_design_audit_20261019.md)
(B-1 to B-10, C-1 to C-7) and the [review of revision 3](pd010_revision3_binding_review_20261019.md)
(R3-1, R3-2). All three Codex audits and the
[bounded check](pd010_revision4_bounded_check_20261019.md) are unchanged.

Propagation order followed, as PD-010 §7 states: Group 1 with C-7 and
the Limits row; Group 2 with C-2; Group 3 with C-5 and B-7; Group 4;
C-1, C-3, C-4, C-6 and the PD-009 sequence change. Historical decision
records were not rewritten; each carries a dated "Amended by PD-010"
section naming what the Constitution now supersedes.

## 1. Finding-to-clause map

**C** is the Constitution at revision 11.

| Finding | Operative clause(s) after propagation | Author's result |
| --- | --- | --- |
| B-1 Checker funding | C §III.5 `RESERVATION` (Research **or Checker** Authorization; verification purposes; cost never cross-charged); `FENCE` (names either class); §III.7 Content (grant content for both classes, own tools and tiers, binding interval, verification purposes, subjects not to check); §III.7 Budget ownership and Authority (fence before revoking either class; Checker holders commit reservation, attempt and settlement records); Part V `RESERVATION`, attempt and settlement row; Part V Genesis paragraph (the sequence-0 Checker Authorization names tools, tiers, cap, expiry and purposes); PD-009 amendment note (`AU-OBS-1` declares no tool; `AU-CK-A` content) | Closed in text |
| B-2 Check form at initialization | C §III.8 Check record item 3 (`F = N/A — no Paper Book`; `LEDGER_UNREACHABLE` stops) and item 4 (Principal control act cites its own authority; budget line applies only to metered proposals, `N/A — no metered consumption` otherwise; the Checker's cost in item 5); Part V Authorization row Check | Closed in text |
| B-3 Five-state arithmetic | C §III.5 Accounting bullet (`C = S + P`; committed total, reserved total, headroom, spendable, released allowance; `OVERSPENT` iff `ΣC > grant`; lineage sums include closed reservations' pending maxima; underrun disposition); Attempt bullet (allowance, headroom and cap all required; `GRANT_EXHAUSTED`, `CAP_EXHAUSTED`); Settlement bullet (validation, single effect) | Closed in text; replay §2.3 |
| B-4 At-Apply funding conditions | C §III.5 `BINDING` bullet (eligibility at `BIND`; effects of later fence, expiry, overrun; freeze standing, four cases; `RELEASE` after durable invalidation; deriving consumption by I-13 read; fresh binding; declared tradeoff); §III.8 Lifecycle addition and the "Apply binding, terminal disposition and invalidation" bullet (Apply admission; the two invalidation grounds with their evidence; mutual exclusion; interval meaning; continuation role; authority declared); §III.8 Continuation (funding clause replaced); Part V `BIND`/`RELEASE` row and `P-1` (b); Part VII rows; I-13 sentence | Closed in text; replays §2.4 |
| B-5 Outcome deadline and uniqueness | C §III.7 Source Declaration (resolution grace, per source, no default); Part X §6 Observation cutoff rule; §III.5 Prediction row (cutoffs pinned) and Outcome row (function of ledger and cutoffs; computation time irrelevant; one Outcome per `PredictionId`, `DUPLICATE_OUTCOME`; Checker duty due at the cutoff); Part V Hypothesis registration Check (sources with a grace) | Closed in text; replay §2.5 |
| B-6 Method commitment sequences | C Part X §3 (registration commitment governs unless a successor `EXPERIMENT DESIGN` has lower Evidence sequence than the event; comparison within one ledger); §III.5 Prediction row (witness read refuses a Prediction of an unadmitted subject) | Closed in text; replay §2.6 |
| B-7 Cost evidence route | C Part X §3 cost verification (b) (Market Observations under declared sources only; uncited evidence cannot be cited; no source → unverified → `Qualify` withheld); Part V Allocation Check ("checked against Market Observations"); PD-005 amendment note | Closed in text |
| B-8 Reducing fill after expiry | C §III.10 Provisional fill bullet (reducing bound at the head; excess refused `REDUCING_BOUND`; no fill inherits reduction); Intent class bullet (beyond-zero leg derived only at zero, never after expiry); refusal list | Closed in text; replay §2.8 |
| B-9 `FLATTEN_ON_QUOTA` | C §III.10 Expiry bullet (option removed; quota refuses opening and does not expire); §III.7 Execution Authorization triggers (quota exhaustion removed); Part V Allocation content; PD-004 amendment note | Closed in text; replay §2.9 |
| B-10 Reducing qualified exposure | C Part V Allocation row (`REDUCE` content; Principal-only; Check items (i) to (iv): standing never higher, residual breach versus new or worsened risk, residual execution obligation, Apply liquidates nothing); "Standing Transition after expiry or `REDUCE` to zero" row; §III.6 (withdrawing allocation versus flattening positions); §III.10 Expiry bullet (re-execution to the lower target under the new key); Part X §4 `Reduce or suspend` | Closed in text; replay §2.10 |
| C-1 Stale worked text | C Summary table and Part VII (capital and allocation budget consumption); Part IX principle 4; I-4; T-A (reservation named; `BIND` cited at Apply; commitment 2026-10-15 15:50; cutoffs; duplicate Outcome refused); T-B (registration, `EXPLORATORY` allocation, `REDUCE` and retirement of the predecessor); T-C (registration, fence, grant, revocation as four acts; control acts' budget line `N/A`); T-D sequence numbers follow; T-F/T-G annotated historical | Applied |
| C-2 Sequence and re-check conventions | C §III.6 (projection at 0 is the state after Apply 0); §III.8 Lifecycle (a re-check appends a Check naming its base; decision and Apply cite it; proposal never rewritten); Part V Genesis paragraph (empty ledgers; first closure `E` at head, `N = 0`, `F = N/A`) | Applied |
| C-3 Numerical placement | C §III.7 hop rule (default 2 labelled a provisional Authorization default admitted by PD-003); Part X R-8 refers the count to §6; §6 Decay flags row carries "two consecutive" as a provisional constant; checklist item 11 reworded | Applied |
| C-4 Refusal vocabulary; Checker proposals | C §III.8 Independence (successor and a `STOPPED` Constitutional Transition); Check record item 6 (known failed gate is `NOT MET` → `FAIL`; `STOP` only for constitutional indeterminacy); Part V Agent Design registration proposer; PD-007 amendment note (Day 4 example corrected) | Applied |
| C-5 Classification timing; dispatch ambiguity | C §III.5 evidentiary classes (`CLASS PENDING` until the Outcome binds; finalized then, never changed); Part X R-3 (finalized Outcomes only); §III.5 Attempt (lack of a response is not proof of no dispatch; uncertain retry is a fresh funded attempt) | Applied |
| C-6 Provider substitution; storage | C §III.4 Provenance (provider and model version fixed to the Agent Design Version for the prototype; substitution `STOPPED` until a rule is admitted; D-14 stays open); Part IX principle 10 (a replaceable store may host the ledgers; hosting confers no decision right) | Applied |
| C-7 Own-subject routing | C §III.7 Content (subjects a Checker may not check as Authorization content); §III.8 Independence (not inferred from the three conditions); PD-009 amendment note (`AU-CK-A` verification purposes exclude Transitions concerning `AD-CK-1.0` or `AU-CK-A`) | Applied |
| R3-1 Freeze semantics | C §III.5 `BINDING` bullet: freeze standing in four exhaustive cases; consumed ends the freeze from the Apply alone; no "live"; a fence's accounting release distinguished from binding `RELEASE`; deriving consumption by an I-13 read with `LEDGER_UNREACHABLE` refusal; after consumption the ordinary rules, original grantee and expiry, successor inherits nothing, liabilities survive closure; Part VII derived-standing row | Closed in text; trace §2.4 case 5 |
| R3-2 Invalidation authority | C §III.8 binding bullet (the Transition commit boundary alone; two grounds with recorded evidence: failed condition and cited authority; exact `BIND`, interval, requesting role, verified clock receipt; "ownership of a ledger is not the grant"); closing delta `ΔA` items 3 and 4; Part VII carrier rows (`AUTHORITATIVE`, `DERIVED`, `RECEIPT`) | Closed in text |

Sweep of superseded wording in the Constitution after propagation:
"five budget states" and "five states": none remain. "open at Apply":
none. `FLATTEN_ON_QUOTA`: only the header and the §III.10 removal note.
"budget consumption" without the capital-and-allocation qualifier: none
in the Summary table or Part VII. "live" binding: none. "Proposal-time
reservation is an open question": none. "recorded in the Check with
provenance": none.

## 2. Replays on paper

### 2.1 Genesis funding chain

| Step | Durable fact or act | Governing clause | Result |
| --- | --- | --- | --- |
| Empty system | No ledgers hold a record; the Evidence clock is the boundary's declared clock from its first read | Part V Genesis paragraph | Conventions stated; no authority inferred from repository access |
| Apply 0 | `ConstitutionVersion 1` text; `AD-CK-1.0` registered with provenance and its contribution-measure commitment; `AU-CK-A` with 60 units, tools (bounded synthetic provider tier 2, metered local compute tier 1), uncapped calls forbidden, cap 60, reservation expiry 7 days, verification purposes excluding its own subject | Part V Genesis; §III.7 Content; PD-009 as amended | Waiver bounded to this content; the grant is usable |
| Before Check 1 | The Principal proposes `TR-1` (`AU-OBS-1`, sources and feeds only). `AD-CK-1.0` commits `RESERVATION` 4 under `AU-CK-A`, purpose "Check of `TR-1`": Checker Authorization active at head 0; no fence; spendable 60 ≥ 4; cap 60 holds | §III.5 `RESERVATION` | Admitted |
| Attempt | Pre-record (reservation, "check", hash of `TR-1`, dispatch 0), maximum 3, on the synthetic provider named in `AU-CK-A`: allowance 4 ≥ 3; headroom 60 ≥ 3; cap holds; not frozen | §III.5 Attempt | Admitted |
| Check 1 | Proposer authority: the Principal's own, cited; budget line `N/A — no metered consumption`; closure `(E = 3, N = 0, F = N/A — no Paper Book)`; Authorization-row criteria; item 5 cites the Checker's attempt; `PASS` | §III.8 Check record | A Check in the required form |
| Decide, Apply 1 | A control act; no `BIND` is requested because no metered consumption is declared | §III.8 binding bullet (applies to Transitions declaring metered consumption) | Applied at 1 |
| Settlement | The Checker settles at 2 units with the provider's record; `C` for the reservation becomes 2; the reservation closes by `CLOSED` or at expiry | §III.5 Settlement, Accounting | Admitted once |
| Interruption after the attempt | Restart finds the `PENDING` attempt; settles or dispatches it under its consumed permission; `TR-1` waits checked or unchecked | §III.5 Attempt (resume versus admit) | Nothing re-admitted from memory |
| Sequences 2 to 16 | Limits (Part V Limits row); ten registrations; second Checker and `AU-CK-B`; `AU-RP-1` with a binding interval; `TH-G1`; ordinary operation from 17 | Part V; PD-009 as amended (sequence 17 deleted) | Each a checked Principal act or ordinary operation |
| First budgeted Apply | A Hypothesis registration under `P-1`: the proposer's reservation with purpose "pending registration `TR-x`" is bound at `BIND`, the Apply cites it; the Checker's own reservation for the Check is never bound | §III.5 `BINDING`; §III.8; `P-1` (b) | Applies; the Checker's cost stays on its own grant |

### 2.2 Check applicability (B-2)

A Principal control act at any sequence: item 4's budget line reads
`N/A — no metered consumption`; `F` reads `N/A — no Paper Book` until an
Execution Authorization has been applied, a finding derived from the
Applied History, then a real head. A Check that cannot read a ledger
that exists records `LEDGER_UNREACHABLE` and stops; it never substitutes
`N/A`.

### 2.3 Accounting (B-3)

Grant 100; `R1` 50, `R2` 50: reserved total 100, spendable 0, headroom
100. `R1`'s attempt (max 50) settles at 60: `C1 = 60`, overrun 10,
usage 60; committed total 60; reserved total 110; headroom 40. `R2`'s
attempt of 50: allowance 50 ≥ 50 but headroom 40 < 50 → refused
`GRANT_EXHAUSTED`. An attempt of 40 under `R2`: admitted; headroom 0;
every further attempt refused. It settles at 45: committed 105 > 100 →
`OVERSPENT`; new reservations and attempts refused; valid settlements
admitted. Lineage cap 100 with a closed reservation holding 100
pending: `Σ C_lineage = 100` → `CAP_EXHAUSTED` until settlement lowers
it. Original B-3 cases: `R` 10, attempt 10 settled at 20: allowance 0,
overrun 10, usage 20, headroom 80. Settled at 6 while open: allowance
4, usage 10, headroom 94; at close released 4, spendable 94.
Settlement duplicate: `ALREADY_SETTLED`, no change; malformed:
`INVALID_SETTLEMENT`, liability unchanged.

### 2.4 Apply binding (B-4, R3-1, R3-2)

Interval 10; `BIND` at `E_b = 101`, `t_b = 0`.

| Case | Deciding record | Result under revision 11 |
| --- | --- | --- |
| `BIND` → `FENCE` 102 → Apply | `BIND` 101; the Apply; the `FENCE` | Applies; `R` closed by the fence, attempts `FENCED`; liabilities settle; successor grant inherits nothing. A revocation applied first refuses the Apply and invalidates atomically (`APPLY_REFUSED`, condition: Authorization inactive, citing the revocation's Apply) |
| Early witness → pause → invalidation → `RELEASE` → delayed Apply | `BINDING_INVALIDATED(101, INTERVAL_ELAPSED, {101, 10, role, (11, 120)})` at `n_i = 12` | Delayed Apply refused `BINDING_INVALIDATED`; `RELEASE(101, 12)` admitted after the read of `n_i`; fresh `BIND` possible |
| Apply wins | The Apply | Invalidation refused `ALREADY_APPLIED`; `RELEASE` refused `NO_INVALIDATION`; consumed; freeze ended at the Apply |
| Invalidation wins | The invalidation | Apply refused `BINDING_INVALIDATED`; `R` frozen pending release until a continuation-role `RELEASE`; a fence may close it meanwhile |
| Death after Apply (R3-1 continuation) | The Apply | `R` 10, expiry 20, Apply at `t = 1`: at `t = 2` the Evidence boundary reads the Transition ledger, finds the Apply, consumed; the original grantee's attempt of 3 is admitted under ordinary checks; `CLOSED` releases 7 and keeps the pending 3; first read at `t = 21` with no attempt closes `R` on expiry releasing 10; Transition ledger unreachable → `LEDGER_UNREACHABLE`, nothing spent or released. No `RELEASE` after Apply |
| Death after invalidation | The invalidation | Every Apply of 101 refuses; `R` frozen pending release with no promised maximum; one `RELEASE` by a continuation-role process; a second refused `ALREADY_RELEASED` |
| Old invalidated, fresh created, old resumes | Invalidation of 101; `BIND` 131 | Apply(101) refused `BINDING_INVALIDATED`; `RELEASE(131)` without invalidation refused `NO_INVALIDATION`; Apply(131) consumes; re-invalidating 101 refused `DUPLICATE` or `ALREADY_APPLIED` |
| Settlement after revocation | The first valid settlement | Admitted once at 7; duplicate `ALREADY_SETTLED`; malformed `INVALID_SETTLEMENT` |

Allowance check: allowance leaves the freeze only by the Apply (into
the ordinary rules) or by `RELEASE` after an invalidation that refuses
every later Apply of that binding; a fence's accounting release goes
into an unreservable grant; expiry is unread while frozen.

### 2.5 Observation cutoff (B-5)

Member `M`, period ends day 10, grace 2 days, cutoff day 12. `VALUE`
day 11, Outcome computed day 20: resolved. No `VALUE` by day 12, `VALUE`
day 13, no Outcome yet: `M` not observed; the canonical Outcome,
whenever committed, is `UNRESOLVABLE` naming `M`. Two Checkers commit on
days 12 and 14: the second refused `DUPLICATE_OUTCOME`. A Checker dying
mid-computation commits nothing; the next computes the same function.
A source without a declared grace: the Checker refuses the
registration.

### 2.6 Method commitment (B-6)

Registration at Apply 200, Evidence 20; first Decision at `E = 21` with
closure `N = 200`: the registration commitment governs. A Prediction for
an unadmitted Hypothesis is refused at the Evidence boundary's witness
read. A successor `EXPERIMENT DESIGN` at `E = 300` governs events with
sequence above 300 only.

### 2.7 Cost evidence (B-7)

A Checker reading a vendor page during a Check cannot cite it. With no
Market Observation for an instrument class's spreads, the cost
criterion is `NOT DETERMINABLE` on the cost line only, which withholds
`Qualify` under (f) rather than stopping the Check.

### 2.8 Reversal and reducing bound (B-8)

Position +40; sell 40 `REDUCING` admitted; sell 30 not derived. Fill 40
before `T`: position 0; sell 30 derived with a read `t < T`. After `T`
nothing is derived. Sell 40 filled only 10 (+30) and `T` passed: a later
fill of sell 40 is bounded to 30, excess refused `REDUCING_BOUND`.
Death between the to-zero fill and the beyond-zero derivation: on
restart the position is zero and `T` has passed; nothing is derived.

### 2.9 Quota (B-9)

Quota exhausted Monday, `T` Friday: no set derived Monday; opening
refused `QUOTA_EXHAUSTED` all week; Friday's read `t ≥ T` derives the
expiry set; a Wednesday restart finds no obligation.

### 2.10 `REDUCE` (B-10)

A version `QUALIFIED` at 10 with a limit breach under stress; the
Principal proposes `REDUCE` to 6 (zero would breach a portfolio net
limit through a hedge's short leg, a worsened risk). The Checker
records the residual breach at 6 and no new risk; Apply: allocation 6,
standing unchanged; the Execution function derives `REDUCING` orders to
the 6 target, each fill bounded. A later `REDUCE` to 0 follows when the
hedge is unwound. An `EXPLORATORY` allocation reduced to 0:
`INCUBATING`; its expiry obligation is superseded by the new target,
which the re-execution duty carries. Death after Apply and before any
order: restart derives the obligation from allocation versus confirmed
position.

### 2.11 PD-004 cases re-run under revision 11

T-H (Part VI): the reversal in name Q is now sell 40 `REDUCING` with
sell 30 not derived until the position is zero, instead of derived and
refused; each flatten fill after `T` is bounded by the reducing bound;
no `FLATTEN_ON_QUOTA` branch exists at 03-12 and the expiry set is
derived only at the 17:30:40 read. The recovery at 17:40, the
`DUPLICATE` and `ORDER_CLOSED` refusals and the standing Transition at
72 are unchanged. The forward case of PD-004 §PD-004.9 (expiry with no
Decisions scheduled; Observation function dead; residual from an
incomplete flatten) is unchanged: it derives from allocation, clock
read and confirmed position, none of which PD-010 touched.

### 2.12 Interactions

| Interaction | Result |
| --- | --- |
| `BIND` and a fence on a Checker Authorization | Never meet: Checker reservations are never bound |
| Headroom predicate and Checker grants | Per Authorization; a Checker's overrun exhausts its own grant only |
| `REDUCE` to zero and the expiry obligation | The re-execution obligation supersedes it; both derive from allocation versus confirmed position; keyed sets prevent a double flatten |
| Reducing bound and `REDUCE` re-execution | Fills toward the lower target bounded at the head |
| Cutoff rule and `CLASS PENDING` | The class finalizes when the Outcome binds; the cutoff fixes when that must happen; R-3 counts finalized Outcomes |
| Prediction witness read and `P-1` | A Hypothesis admitted at Apply `N` can have Predictions from the first Evidence commit witnessing `N` |
| Restart | `BIND`, `BINDING_INVALIDATED`, `RELEASE`, cutoffs, the reducing bound and the `REDUCE` target are ledger or clock facts; the continuation rule reads them |

## 3. What this check did not do, and what remains open

This check did not grade the design, did not execute any witness, and
did not re-derive the two proof walks of the independent audit; those
are for Codex's final review. No unresolved substantive choice appeared
during propagation; every clause written applies an admitted choice of
PD-010 or transcribes an admitted decision, and none introduces policy
or authority beyond the admitted delta.

Open items that predate PD-010 and remain, each with its owner: D-14
(provider as identity; fixed for the prototype by C-6); U-1 (what else
might ground a `NON-REPRODUCIBLE` version); U-8 (limits at a moving
head; plan step 7); real-provider output caps (PD-009 §5, unresolved
until a per-provider decision); `FR-0` as the provisional fill rule,
granted later. Genesis is not executed; `ConstitutionVersion 1` is not
admitted; nothing is certified.
