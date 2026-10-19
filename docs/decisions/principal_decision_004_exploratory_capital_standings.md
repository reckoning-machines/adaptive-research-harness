# Principal Decision Record 004 — Exploratory Capital, Expiry and Recovery

Status: **ADMITTED 2026-10-19 by the Principal: revision 3 with the
internal-simulator clarification (§PD-004.15), as written.** Admission
was conditional on the final focused OSA review
([audit §9](../audits/osa_audit_pd004_proposed_20261018.md)) finding no
unresolved constitutional conflict; it found none. Applied to the
Constitution as revision 5 of 2026-10-19 and re-audited in
[osa_reaudit_pd004_20261019.md](../audits/osa_reaudit_pd004_20261019.md).
Admission text, as approved:

```text
ADMITTED 2026-10-19 by the Principal: PD-004 revision 3, dispositions
PD-004.1 to PD-004.14, with the clarification of §PD-004.15.

Principal decision: New Speedway uses an internal paper-trading
simulator initially. External broker paper accounts and live execution
are outside the current design.

Clarifications on admission:
(a) Simulated opening fills are provisional until independently
    confirmed under the Paper Book's governing rules. Only confirmed
    fills contribute to positions, cash, exposures and P&L.
(b) Unestablished fills remain durable operational records, never
    silently deleted and never counted as completed execution.
(c) Pending provisional fills are accounted for conservatively when
    evaluating additional orders; they cannot be ignored to create
    excess exposure.
(d) Fill confirmations are independently reproducible from the recorded
    admission witnesses and authoritative state.
(e) Reducing orders remain permitted without a clock read under the
    bounded rules, provided positions, allocation authority and
    applicable limits can be established.
(f) U-8 stays open: pre- and post-witnesses do not establish atomicity
    of changing portfolio limits.
(g) The simulator's fill methodology remains plan step 7 content.

Constitutional Delta admitted:
ΔO: +1 Paper Book record kind: Fill Confirmation, bound to one FillId.
ΔS: as PD-004.10, with §PD-004.15's refinements: provisional simulated
    fill distinguished from confirmed execution fact; positions, cash,
    exposures and P&L from confirmed fills only; conservative accounting
    of provisional fills; confirmation standing as a deterministic
    function of recorded witnesses and applied content; the fill rule
    as Execution Authorization content.
ΔA: (1) Execution Authorization triggers extend to the expiry instants
    of applied allocations established by a clock read; (2) the Paper
    Book commit boundary reads the Evidence clock at admission. No time
    authority created; no admission authority moves.

Closed by this admission: FR-12, UD-14.
Open items preserved with owners: U-8 (limits at a moving head, plan
step 7); paper fill methodology (plan step 7); P4-R1, P4-R3, P4-R4,
P4-R5; UD-3, UD-5, UD-10; D-17, N-1; and every item of the PD-002 and
PD-003 re-audits.
```

Prior content follows. Depends on PD-002 and
PD-003 (dispositions 1 to 5), both admitted and applied in Constitution
revision 4. Revision 2 (2026-10-19) replaced revision 1's deadline-event
mechanism after the Principal's first-principles challenge. Revision 3
(2026-10-19) answers the Principal's final challenge, that authority and
time may change between an admission read and the Paper Book commit, with
the bracketing contract of §PD-004.2 and the fill confirmation record;
earlier revisions are preserved in the focused audit.

Date: 2026-10-19 (revision 1: 2026-10-18)

Subjects: FR-12 (capital standings); exploratory expiry; opening,
reducing and reversing exposure; recovery of execution obligations after
process death; UD-3, UD-5, UD-10, UD-14.

Sources: [Constitution revision 4](../doctrines/new_speedway_constitution.md)
§III.5 (the Evidence clock), §III.6, §III.7, §III.10, I-8, I-12, I-13,
I-15, Part V, T-D; [PD-002](principal_decision_002_predictions_decisions_observation.md)
(witness marks; order sets; the Execution function); the adopted CPOC
doctrine and certification contract (fin123-core `8175d504`); the
Principal's brief of 2026-10-19; focused audit
[osa_audit_pd004_proposed_20261018.md](../audits/osa_audit_pd004_proposed_20261018.md).

## 1. The investment requirement

A Strategy Version with no forward record must be able to trade paper
capital so that fill quality, turnover, order clustering, timing
sensitivity and implementation shortfall can be measured before any
claim of edge exists, and that activity must never read as edge. The
capital is bounded in amount, in the number of Decisions that may open
exposure, and in time. When the time bound passes, no new exposure may be
opened by any process, open orders are withdrawn, and the position is
closed unless the Principal has explicitly authorized a bounded hold.
When a process dies at any point, a fresh process must be able to prove
what it still owes from the ledgers alone, without duplicating an order
or reviving a superseded state. The doctrine must satisfy that
requirement; it may not reshape it to fit an ontology.

Three principles are preserved throughout:

- The Applied History owns allocations and limits. Expiry, quota,
  instruction and pool are allocation content. Nothing else defines them.
- The Paper Book owns orders and fills. Positions are derived from fills.
  No ledger rewrites another.
- CPOC proves that a lawful obligation survives process death. It does
  not establish that an allocation was lawful or that a Strategy has an
  edge; those are OSA and Evaluation questions respectively.

## 2. Defects repaired

| Ref | Defect | Found by | Repair |
| --- | --- | --- | --- |
| E-1 | PD-003 revision 3 bounded an exploratory allocation by a Decision count. A count limits Decisions; it establishes no calendar expiry and guarantees no flattening when the Runner dies | Principal, 2026-10-18 | Two bounds, separated: a quota and an elapsed-time expiry (§PD-004.5) |
| E-2 | "Opening exposure" written as an increase in absolute position admits a reversal from long to short | Principal, 2026-10-18 | Opening defined per instrument as away from or through zero; reversals must be split at zero (§PD-004.3) |
| E-3 | Revision 1 established expiry by a **deadline event**: the first Observation record witnessed at or after `T`. The admission check treated the *absence* of such a record as proof the allocation was unexpired. Absence of a record is not evidence of the time; with the Observation function dead the window never closes; and the mechanism coupled expiry to market-data arrival | Principal, 2026-10-19 | Currency is established by a **positive read of the Evidence clock at order admission**, recorded on the order (§PD-004.4). The deadline event is withdrawn as the mechanism |
| E-4 | Revision 1's admission check (c) used the Decision's commitment time, a previously committed timestamp, as evidence that the allocation remained unexpired at admission | Principal, 2026-10-19 | No previously committed time is used for currency. Only the admission read is |
| E-5 | Revision 2 took one read before the commit and treated it as the commit's time and authority. Between that read and the commit, `T` may pass or the allocation may be revoked; a read cannot be simultaneous with a commit on another ledger | Principal, 2026-10-19 | A Paper Book commit's time and authority standing is an **interval** bracketed by a read before and a read after; an opening fill is effective only when both reads satisfy the conditions (§PD-004.2, bracketing). Checks and commits are not assumed instantaneous |
| E-6 | Revision 2 judged intent class on the working position including opposite-side open orders, so a sell could pass as reducing against an unfilled buy | This review | Class is judged on the **same-side working position**: a sell against the position if every open sell fills and no open buy does, and symmetrically (§PD-004.3) |
| E-7 | Revision 2 defined the expiry obligation as discharged when an expiry set existed; cancels then death left the set present and the position open | Principal, 2026-10-19 | The obligation is outstanding until the **terminal state** is established, whatever records exist (§PD-004.5) |

## 3. What exists, and who owns it

Nothing new exists. Every fact below is carried by a ledger the
Constitution already names, under the owner it already has.

| Fact | Owner | Commit boundary | Other carriers and class |
| --- | --- | --- | --- |
| Capital standing of a Strategy Version: `INCUBATING`, `EXPLORATORY`, `QUALIFIED` | Applied History (content of the Allocation Transition that set it) | Apply | Population State: `DERIVED` |
| Exploratory pool; per-version cap | Applied History (a limit) | Apply (a limits Transition by the Principal) | Projection: `DERIVED` |
| Allocation content: amount, purpose, `expiry_time T`, optional `quota_events`, instruction (`FLATTEN`; `HOLD` with `hold_expiry_time`; optional `FLATTEN_ON_QUOTA`) | Applied History | Apply | Projection: `DERIVED`; any copy held by the Execution function: `EPHEMERAL` |
| The instant | The Evidence commit boundary's declared clock (§III.5: the only clock) | None; the clock is read, never committed | A **clock read** held by any function: `EPHEMERAL` until recorded by a commit boundary on its own record |
| Admission witness on an order: `(t_w, E_w, N_w)` | Paper Book (an execution fact: when and against what this boundary admitted this order) | Order commit | The time value is a `RECEIPT` of the clock's answer; the Paper Book keeps no clock |
| Order intent class: `OPENING`, `REDUCING`, `CANCEL` | Paper Book (set by the boundary at admission from the same-side working position at its head) | Order commit | None |
| **Confirmation** of a fill: a record naming the `FillId` and carrying a read `(t_2, E_2, N_2)` taken after that fill's commit | Paper Book | Confirmation commit (by the boundary, on the Execution function's call) | None |
| Fill standing: `PROVISIONAL`, `EFFECTIVE`, `UNESTABLISHED` | None | None | `DERIVED` from the fill's pre-witness, its intent class and its confirmation |
| Expiry set, key `TransitionId:StateVersion:EXPIRY` | Paper Book | Order commit | None |
| Refusals with reason; fills; cancels; late fills refused | Paper Book | Order and Fill commit | None |
| Strategy-level and portfolio-level positions | None | None | `DERIVED` from `EFFECTIVE` fills |
| "Expired" standing; outstanding expiry obligation; incomplete flatten | None | None | `DERIVED` from the Applied History, the Paper Book and a clock read |
| Decision index under an allocation | None | None | `DERIVED` from the Evidence ledger: the rank of the Decision among the version's Decisions, including `DECLINED` and `FAILED`, whose closure `N` is at or above the allocation's Apply sequence |
| Same-side working position | None | None | `DERIVED` from `EFFECTIVE` fills and the open remainders of same-side orders |
| Terminal state of an expired allocation | None | None | `DERIVED`: no open orders under the allocation, no `PROVISIONAL` fills, every version-level position zero (under `FLATTEN`) |

---

## PD-004.1. Capital standings

| Standing | Allocation | Entered by | Produces | May ground |
| --- | --- | --- | --- | --- |
| `INCUBATING` | Zero | Strategy Version registration; or a standing Transition after expiry | Decisions; decision-implied record at the Standard's notional; reproduction records | Qualification once `ES-1`'s forward-event minimum is met |
| `EXPLORATORY` | Bounded, from the Principal-declared **exploratory pool** (a limit in the Applied History), within a per-version cap, with a required `expiry_time` and an optional `quota_events` (PD-004.5) | Allocation Transition of purpose `EXPLORATORY`, stating the measurement purpose per Transition, the expiry, the quota if any and the instruction; checked for pool capacity and composition (I-10); cites no performance Evaluation | Executed record **labelled `EXPLORATORY`** | Implementation shortfall, fill quality, turnover and operational measurement only |
| `QUALIFIED` | Evidence-qualified | Allocation Transition of purpose `QUALIFIED` citing an Evaluation under the Standard in force at base whose grounding series is the forward decision-implied record | Executed record, qualified | Further allocation within limits |

Visibility without claim. Every exploratory executed fact, including
refusals, cancels, late fills, expiry flattening and incomplete
flattening, appears in every Evaluation and report under the label. An
Evaluation whose grounding series includes any of them is non-conforming,
and a Transition citing it is refused at Check. No Transition, Evaluation
or report may describe an exploratory record as evidence of an edge. The
Decisions themselves are unaffected by the standing: the decision-implied
record is computed from Decisions at the Standard's notional whether or
not exploratory capital was allocated. No numerical threshold is set
here.

---

## PD-004.2. Time: reading the clock versus owning it

§III.5 states that the Evidence commit boundary's declared clock is the
only clock in the doctrine. PD-002 made that boundary read the heads of
the Applied History and the Paper Book at Decision commit and record
them as witness marks, under I-13's rule that reading an authoritative
ledger is open to every function. PD-004 applies the same rule in the
other direction.

**Clock read.** A clock read is the answer the Evidence commit boundary
gives when asked the instant: the pair `(t, E)`, the instant `t` its
declared clock shows and the Evidence sequence `E` at its head at that
answer. A read is a read: it commits nothing to the Evidence ledger,
assigns a time to no Evidence fact, and is `EPHEMERAL` in the hands of
whoever took it. The Evidence boundary does not originate records to
answer it. A function that cannot obtain a read has no time and acts as
such (rules below); it never substitutes a local clock, a prior read, or
a previously committed timestamp.

**Admission witness.** The Paper Book commit boundary takes a clock read
inside every order admission and records on the order `t_w` and `E_w`
from the read and `N_w`, the Applied History head it read for the
allocation and limits. The witness is a Paper Book fact: *this boundary
admitted this order at this instant of the one clock, against this head*.
It is not an Evidence fact and resolves nothing. Because both ledgers are
append-only, the witness is checkable from durable records: the latest
timed Evidence record at or below `E_w` carries a time at or before
`t_w`, and the first timed record committed after `E_w` carries a time at
or after `t_w`. The check is as fine as the density of timed records and
no finer. A witness the ledgers contradict is a defect, visible to any
reader. Answering a read is a duty of the Evidence commit boundary; it
originates no record and decides nothing.

**Why this is not a second time authority.** One clock exists and one
boundary owns it. The Paper Book boundary reads it, as the Evidence
boundary already reads the Paper Book head. Owning *when an order was
admitted* is the Paper Book's existing authority over execution facts;
owning *what time it is* stays where §III.5 put it. If the Principal
regards the clock as something other than an authoritative ledger for the
purposes of I-13, the read right is declared below as `ΔA` so that the
decision is explicit.

**What a read establishes.** A read at `t ≥ T` establishes that `T` has
passed. A read at `t < T` establishes that it had not, at that instant.
The absence of any record establishes nothing, and no rule below relies
on absence.

### Bracketing: the serialization contract

The only serialization in the doctrine is the one each ledger already
has: a commit boundary totally orders its own commits by sequence. No
cross-ledger atomicity exists, and none is assumed. A read of the clock
or of the Applied History is therefore always strictly before or
strictly after a Paper Book commit, never at it. The contract that makes
conditions hold *at* a commit without pretending otherwise:

1. **Pre-witness.** The boundary takes a read before the commit and
   records it on the record: `(t_1, E_1, N_1)`.
2. **Post-witness.** For a commit whose validity depends on a condition
   still holding, the boundary takes a read *after* the commit and
   records it on a **confirmation** record that names the commit:
   `(t_2, E_2, N_2)`. The confirmation's own instant needs no bracket: it
   is after the commit by construction, and that is all it claims.
3. **Monotone conditions.** "`T` has not passed" and "allocation `A` is
   in force" can turn false and never true again, because the clock
   advances and the Applied History is append-only. Such a condition
   holding at both witnesses holds at every instant between them, and so
   at the commit. That is the logical admission point: **a condition is
   established at a commit when it holds at the commit's pre-witness and
   at its post-witness.**
4. **One-sided conditions.** "`T` has passed" needs only a pre-witness
   `t_1 ≥ T`; it cannot stop being true.
5. **Non-monotone conditions.** Limits can be raised as well as lowered;
   they are checked at the pre-witness and U-8 (limits at a moving head)
   stays open. PD-004 does not claim to close it.
6. **Standing.** A commit awaiting its post-witness is `PROVISIONAL`. A
   confirmation whose read satisfies the conditions makes it `EFFECTIVE`;
   one whose read does not makes it `UNESTABLISHED`, a terminal standing:
   the commit happened, is preserved, and counts for nothing, because
   whether it preceded expiry or revocation cannot be shown from durable
   authority. A `PROVISIONAL` commit is confirmed by whichever process
   next calls the boundary for it; the standing is decided by that later
   read, never by any process's belief about when the commit happened.

Which commits are bracketed is decided by what creates exposure. An
order creates none; a fill does. Orders therefore carry a pre-witness
only; **every fill of an `OPENING` order is bracketed**; fills of
`REDUCING` orders are `EFFECTIVE` at commit. The logical admission point
of exposure is the confirmation of the fill.

---

## PD-004.3. Opening, reducing and reversing exposure

Positions are per Strategy Version per instrument, derived from the fills
of orders in sets keyed to any Allocation Transition of that version.
Portfolio positions per instrument are their sum. Both count `EFFECTIVE`
fills only. The **same-side working position** for an order is the
position the version would hold if every open order on the same side as
that order filled and no open order on the other side did: for a sell,
position plus open sell remainders; for a buy, position plus open buy
remainders (for a `REPLACE`, excluding its parent's remainder). It is
the worst case for the claim that the order reduces exposure. All three
are `DERIVED`.

An order's **intent class** is set by the Paper Book commit boundary at
admission, from the signed Strategy-level same-side working position at
its head, and recorded on the order:

- `OPENING`: the order's full fill would move the signed position away
  from zero, or through zero.
- `REDUCING`: the full fill would move the same-side working position
  toward zero without crossing. An order that is not provably reducing
  is `OPENING`; nothing passes as reduction by assuming an opposite-side
  order will fill.
- `CANCEL`: withdraws an open order; creates no exposure.

A `REPLACE` is classed afresh at the head it is admitted against; the
parent's class is not inherited. The Execution function must derive any
target that crosses zero as two orders, one to zero and one beyond; the
boundary refuses a single order whose full fill would cross zero
(`REVERSAL_SPLIT_REQUIRED`) so that every order has exactly one class.

| Case | Strategy-level class | Treatment |
| --- | --- | --- |
| Flat → long | `OPENING` | Needs current authority, time and quota (PD-004.4) |
| Flat → short | `OPENING` | Same |
| Long → larger long | `OPENING` | Same |
| Long → smaller long | `REDUCING` | Admitted on allocation in force and limits; no clock read required |
| Long → short through zero | Two orders: `REDUCING` to zero, `OPENING` beyond | Classed in order against the same-side working position: sell 40 against long 40 reaches zero, `REDUCING`; sell 30 against long 40 with 40 of open sells is judged from zero, `OPENING`. The second is refused whenever opening is refused; the first is not. A reversal cannot pass as reducing because the resulting absolute position is smaller |
| Flat, open buy 10 unfilled, then sell 10 | `OPENING` | Judged against the same-side working position (flat; the open buy is opposite-side and does not count); a sell here would open a short if the buy never fills |
| Partially filled `OPENING` order, then expiry | The `EFFECTIVE` filled part is position; a `PROVISIONAL` fill is confirmed first; the open remainder is withdrawn by `CANCEL` in the expiry set; the position is flattened by `REDUCING` orders | A fill of an `OPENING` order is `EFFECTIVE` only when bracketed before `T` (PD-004.4), so the position cannot grow after expiry even if no cancel has been committed; a fill that straddles `T` is `UNESTABLISHED`; a fill presented after the cancel is refused (`ORDER_CLOSED`); all are preserved |
| Cancel committed, another fill arrives | Decided by Paper Book sequence, not by time | As above; the refused fill is a Paper Book fact under the label |
| Two Strategy Versions, one instrument | Each has its own position and class; expiry and quota are judged per version | A flatten that is `REDUCING` for its version may move the portfolio net away from zero. Expiry is judged at the version; limits are judged at the portfolio from derived portfolio positions. Whether net limits may refuse a version-level `REDUCING` order is limit content the Principal sets (§6) |

The Paper Book preserves, under the label: every order with its intent
class and witness; every fill; every cancel; every refusal with its
reason; and, by derivation, every incomplete flatten (an expiry set with
unfilled reducing remainder and no live `REPLACE`). It rewrites neither
allocation nor position history: a position is always the sum of fills,
and a target is always the allocation times the Decision's weights.

---

## PD-004.4. Order admission

At every order admission the Paper Book commit boundary reads the
Applied History head `N_w` (the version's allocation in force, its
content, and the limits in force), its own head (positions and open
orders), and a clock read `(t_w, E_w)`; it records all three on the
order. An allocation is **in force** when it is applied and no later
applied Transition has changed the version's allocation or standing.

| Order | Admitted only when | Refused with reason when |
| --- | --- | --- |
| `OPENING`, in a Decision set keyed to allocation `A` | (a) `A` is in force at `N_w`; (b) a clock read was obtained and, where `A` declares `expiry_time`, `t_w < expiry_time` (a read is required for every `OPENING` order, with or without an expiry, so that the rule is uniform and the witness always exists); (c) where `quota_events` is declared, the Decision's index under `A` is within it; (d) no limit in force at `N_w` is breached; (e) the order does not cross zero | `ALLOCATION_NOT_IN_FORCE`; `CLOCK_UNAVAILABLE`; `EXPIRED`; `QUOTA_EXHAUSTED`; `LIMIT`; `REVERSAL_SPLIT_REQUIRED`; `LEDGER_UNREACHABLE` (Applied History or Paper Book) |
| `REDUCING`, in a Decision set | (a) and (d). A clock read is taken and recorded if available; `CLOCK_UNAVAILABLE` is recorded, not refused. Where a read is available and `t_w ≥ expiry_time`, refused: after expiry only the expiry set may reduce | `ALLOCATION_NOT_IN_FORCE`; `LIMIT`; `EXPIRED`; `LEDGER_UNREACHABLE` |
| `CANCEL` | The order is open at the Paper Book head and the cancel belongs to a set the Execution function may derive: a newer Decision's set (supersession, §III.10), the first set derived under a newer allocation of the same version, or the expiry set | `ORDER_CLOSED`; `NO_SET` |
| **Fill** of an `OPENING` order | Admitted `PROVISIONAL` when the order is open, no fill of the version in that instrument is `PROVISIONAL`, and a pre-witness was obtained with `A` in force at `N_1` and, where `A` declares `expiry_time`, `t_1 < expiry_time`. In a paper book a fill is a commit the Execution function presents from its fill rule, so the boundary gates it exactly as it gates the order | `ORDER_CLOSED`; `CLOCK_UNAVAILABLE`; `EXPIRED`; `ALLOCATION_NOT_IN_FORCE` |
| **Confirmation** of a `PROVISIONAL` fill | Always admitted on the Execution function's call: the boundary takes a read after the fill's commit and records it. Standing follows: `EFFECTIVE` when `A` is in force at `N_2` and `t_2 < expiry_time` (where declared); otherwise `UNESTABLISHED`. The boundary issues the confirmation call itself immediately after admitting the fill; if the process dies first, the next caller confirms | `CLOCK_UNAVAILABLE` or `LEDGER_UNREACHABLE` leave the fill `PROVISIONAL`; nothing is written |
| **Fill** of a `REDUCING` order | The order is open; a pre-witness of the Applied History and Paper Book heads was obtained with `A` in force at `N_1`. `EFFECTIVE` at commit; no clock read required | `ORDER_CLOSED`; `ALLOCATION_NOT_IN_FORCE`; `LEDGER_UNREACHABLE` |
| `REDUCING`, in the expiry set of `A` | (a); a clock read was obtained and `t_w ≥ flatten_time` (`expiry_time` under `FLATTEN`; `hold_expiry_time` under `HOLD`); (d) subject to the Principal's limit content for reducing orders | `ALLOCATION_NOT_IN_FORCE`; `CLOCK_UNAVAILABLE`; `NOT_YET_DUE`; `LIMIT` |
| `CANCEL`, in the expiry set of `A` | (a); a clock read with `t_w ≥ expiry_time` | `CLOCK_UNAVAILABLE`; `NOT_YET_DUE` |
| Any order in the expiry set classed `OPENING` | Never | `EXPIRY_SET_OPENING` |
| A second set with an existing key, a second expiry set for the same `TransitionId`, a second order with an existing `OrderId` | Never | `DUPLICATE` (I-8, §III.10) |
| Any order while the Paper Book head is unreachable | Never; nothing is written | CPOC refuse-not-fallback |

While any fill of a version in an instrument is `PROVISIONAL`, the
Execution function derives no further order for that version in that
instrument and the boundary refuses one (`PROVISIONAL_PENDING`): the
position is not yet known. Confirmation is one read away whenever the
clock and the Applied History are reachable.

Fail-closed, stated plainly: without a clock read nothing opens, no
`OPENING` fill becomes effective, and nothing is flattened under expiry; with the Applied History unreachable
nothing is admitted at all; with the Paper Book unreachable nothing is
written. `REDUCING` orders in a Decision set are the one deliberate
fail-open: they are admitted without a clock read because withdrawing
risk under an allocation in force is the safer error; they are still
admitted only against `EFFECTIVE` fills at the Paper Book head, the
allocation in force at the Applied History head, the limits in force
there, and the same-side working position, so no reversal or new
exposure passes as reduction. The Principal decides that choice
(§PD-004.13).

**The logical admission point.** For an order it is its commit, judged
at its pre-witness; an order that straddles `T` or a revocation is
harmless: it cannot fill effectively and the expiry set or the
successor's first set cancels it. For exposure it is the fill's
confirmation: an opening fill is `EFFECTIVE` only when the allocation
was in force and `T` had not passed at both the read before its commit
and the read after. Nothing in this record assumes a check and a commit
are instantaneous.

The Decision's commitment time plays no part in admission. A Decision
committed before `T` whose order reaches the boundary after `T` is
refused; a Decision committed after `T` is a lawful Evidence fact and is
scored in the decision-implied record, but no set is derived for it.

---

## PD-004.5. Expiry

### Two bounds, separated

| Bound | Declared as | Limits | Established by |
| --- | --- | --- | --- |
| **Decision quota** `quota_events` | A count in the allocation content; optional | How many Decisions under the allocation may open exposure | The Decision's index under the allocation, read from the Evidence ledger at admission |
| **Elapsed-time expiry** `expiry_time T` | An instant on the Evidence clock in the allocation content; required for every `EXPLORATORY` allocation; permitted on any allocation | When opening ends and, under `FLATTEN`, when the position is closed | A clock read at or after `T` |

Quota exhaustion without expiry refuses opening and holds the position
until `T`; it does not expire the allocation. The optional instruction
`FLATTEN_ON_QUOTA` lets the Execution function derive the expiry set on
the first Decision whose index exceeds the quota; that trigger depends on
a Decision and is therefore never the default.

### The expiry obligation

For an allocation `A` with `expiry_time T`, the **expiry obligation** is
outstanding whenever all of: `A` is in force; a clock read shows
`t ≥ T`; and the **terminal state** is not established. The terminal
state under `FLATTEN` is: no open order under any set keyed to `A`; no
`PROVISIONAL` fill under `A`; and every Strategy-level position of the
version zero, from `EFFECTIVE` fills. Under `HOLD` before
`hold_expiry_time` it is: no open order and no `PROVISIONAL` fill. The
obligation is a derived predicate over the Applied History, the Paper
Book and one read. It depends on no Decision, no Observation, no order
attempt and no process's memory, and **it is not discharged by the
existence of an expiry set, a cancel, or any other record**: only the
terminal state discharges it, or the supersession of `A`, after which
the successor's own rules carry the residual.

The Execution function's standing duty under its Authorization is to
discharge every outstanding expiry obligation it finds, in the ledgers it
reads, whenever it runs. On restart it finds the same obligations by the
same reads. The content of the discharge:

1. Derive the **expiry set**, key `A.TransitionId : N_w : EXPIRY`,
   containing a `CANCEL` for every open order of every set keyed to `A`
   (the boundary admits them on a read `t_w ≥ T`).
2. Under `FLATTEN` (the default), add to the set one `REDUCING` order per
   instrument with a nonzero Strategy-level position at the Paper Book
   head, to zero. Under `HOLD`, add none until `hold_expiry_time`.
3. No fill of an `OPENING` order is admitted on a read at or after `T`
   (PD-004.4), so the position to flatten is fixed by the fills admitted
   before `T`; fills of `REDUCING` orders continue. Where a flatten
   remainder changes, the function derives `REPLACE` orders from fills at
   the head under PD-002's `REPLACE` rule. A remainder that would cross
   zero is refused (`REVERSAL_SPLIT_REQUIRED`) and re-derived from the new
   head.
4. The expiry set is **open-ended**: one per `TransitionId`, refused on
   a second; orders are appended to it whenever the obligation is
   outstanding (cancels for anything open, `REDUCING` orders for any
   residual, `REPLACE` for remainders), each refused only on a duplicate
   `OrderId`. A set opened under `HOLD` is the same set to which the
   flatten orders are later added. Before appending, the function
   confirms any `PROVISIONAL` fill under `A`, because the residual is
   not known until it does.
5. After expiry the function derives no Decision set under `A`. Decisions
   continue to be committed by the Runner and scored; they produce no
   orders.

### `HOLD`, the bounded exception

Permitted only when the Allocation Transition, or a successor Transition
decided by the Principal, states the reason, a `hold_expiry_time` after
`expiry_time`, and the exit conditions. The exit conditions are for the
Principal, who may end the hold early by a Transition; the Execution
function acts only on instants. No opening under hold; no Decision sets
under hold; cancels at `expiry_time`; flatten at `hold_expiry_time`.

### The standing Transition, the backstop

A standing Transition (Part V, retirement or supersession; proposer the
Principal or an admitted policy; Checker verifies the expiry set, the
refusals, the cancels and the residual position) records allocation zero
and standing `INCUBATING`. Until it applies, the projection shows
`EXPLORATORY (expiry_time T; expired per read at t; expiry set present
or absent; residual)`, derived. Only Apply changes the allocation. After
Apply, the Execution function treats a residual position under an
allocation of zero as a target of zero: it derives `REDUCING` orders
under the new key by §III.10's re-execution rule. This is how a position
left by a dead Execution function, an unreachable clock or an incomplete
flatten is closed when the Principal decides to close it, and it needs
no new mechanism.

### Qualified allocations

Carry no expiry unless the Principal declares one. Every rule above
applies to any allocation that declares `expiry_time` or
`quota_events`.

---

## PD-004.6. Recovery

Every case uses the record form the brief requires. "Provable" means the
lawful next action follows from the Applied History, the Evidence ledger,
the Paper Book and at most one clock read, with no process memory.

| Case | Before | Authorized action | Durable records at interruption | Interruption | Reconstructed state | Lawful next action | Provable |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Runner dies before `T` | `A` in force, `T` ahead; Decisions to index k; sets admitted; positions open | Nothing: the Runner has no capital duty | Decisions ≤ k; sets; fills | Runner process ends; later events have no Decision (derivable as missing) | Position stands; no Decision set is derived without a Decision | At `T` the Execution function discharges the obligation: cancels, flattens. Nothing about expiry waited on the Runner | Yes |
| 2. Observation function stops before `T` | As above; no new Observations | Nothing for expiry | Last Observation record | No slot records after the stop | Absence witnesses and ledger-event triggers stop; expiry is unaffected because no rule reads Observation records for time | At `T`, discharge as in case 1 | Yes. Revision 1 failed this case |
| 3. Execution function dies immediately before `T` | `A` in force; open `OPENING` orders; position | Discharge at `T` | Sets, orders, fills to the death | Process ends at `T − ε`; `T` passes with no process | Any `OPENING` order, and any fill of an `OPENING` order, that any process presents after `T` is refused on the pre-witness (`EXPIRED`); a fill whose pre-witness was before `T` and whose confirmation is after is `UNESTABLISHED`; the position is frozen at the `EFFECTIVE` fills; the open orders stay open but cannot fill effectively; no cancel, no flatten | On restart: confirm any `PROVISIONAL` fill; read `A`, clock `t ≥ T`; terminal state not established → derive the expiry set from the head | Yes. Cancel and flatten during the outage are not guaranteed (§8); growth of exposure after `T` is excluded |
| 4. Execution function dies after committing the cancels, before flattening, and restarts with the expiry set present (the Principal's case 3) | Expiry set opened with `CANCEL`s at `t_1 ≥ T` | Add flatten orders | Expiry set with cancels | Process ends | Expiry set exists; no reducing orders in it; positions from `EFFECTIVE` fills nonzero; terminal state **not** established, so the obligation is outstanding exactly as before the cancels | Confirm any `PROVISIONAL` fill; append `REDUCING` orders to the existing set from the head. A second `CANCEL` for a closed order is refused (`ORDER_CLOSED`), preserved. The obligation persisted through the cancellation and the death because it is defined by the terminal state, not by the set's existence | Yes |
| 5. Paper Book unavailable at `T` | `A` in force | Discharge | Nothing new | Paper Book boundary unreachable across `T` | Nothing written; obligation outstanding | When the Paper Book is reachable: discharge; the witness records the actual admission instant, so "expired at `T`, acted at `t_w`" is visible | Yes, once reachable; nothing before |
| 6. Two recovery processes attempt the same flatten | Expiry obligation outstanding | Discharge, once | Nothing yet | Two fresh processes derive the same set | Both present key `A:N:EXPIRY` and orders `.1`, `.2`… | The first commit wins; the second is refused `DUPLICATE` and preserved with both process identities. If they read different `N_w`, the second expiry set is still refused: one per `TransitionId` | Yes (I-8, §III.10 idempotency) |
| 7. Late fill after cancellation | Expiry set with cancels | None | Cancel at sequence s | A fill for the cancelled order is presented at sequence > s | Order closed at s | Fill refused `ORDER_CLOSED`, preserved under the label. A fill at sequence < s stands only if its own read was before `T` (an `OPENING` fill) or the order was `REDUCING`; the flatten remainder is then re-derived by `REPLACE` | Yes, by sequence and by read |
| 8. Expiry while no Decisions are scheduled for days | `A` in force; residual 0.2 units from a partial 16:00 flatten on the last qualifying day; no decision events over the holiday | Discharge at `T` | Residual fills | None, or any | Obligation outstanding at the first read ≥ `T`, whatever the Runner's calendar | Expiry set: no cancels needed; one `REDUCING` order. No Decision, Observation or order attempt was needed | Yes |
| 9. A new Allocation Transition supersedes `A` during expiry processing | Expiry set with open flatten remainder; `TR-new` for the same version applied at `N+1` | Continue under the authority in force | Expiry set under `A`; fills | Apply of `TR-new` between a `REPLACE` derivation and its admission | `A` no longer in force at `N+1`; the `REPLACE` keyed to `A` is refused `ALLOCATION_NOT_IN_FORCE`; the position stands under the version | Under `TR-new`: if allocation zero, re-execute to flat under the new key; if a `QUALIFIED` allocation, cancel open orders of `A`'s sets and re-execute the standing Decision at `N+1` under the new key (§III.10). No order is resurrected; the expiry set stays as history | Yes (I-9 at Apply; §III.10 re-execution) |
| 10. Pre-witness before `T`, commit after `T` (the Principal's case 1) | `A` in force; `OPENING` order open; fill presented with pre-witness `t_1 = T − 1 s` | Admit the fill | Fill `PROVISIONAL` with its pre-witness | The clock passes `T` between the pre-witness and the fill's commit, or between the commit and the confirmation read | The confirmation read shows `t_2 ≥ T` | Fill `UNESTABLISHED`: preserved, counted for nothing. Had the order itself straddled `T`, it would be an open order that cannot fill effectively, cancelled by the expiry set. Either way no exposure arises after `T`, and no instantaneity is assumed | Yes: by the bracket, from two durable reads |
| 11. Opening order admitted under `A`; successor Transition revokes `A` before the opening fill commits; the order not yet cancelled (the Principal's case 2) | `A` in force at `N_1`; `OPENING` order open | Admit the fill | Order with pre-witness `N_1` | `TR-new` (allocation zero, or `QUALIFIED`) applied at `N_1 + 1` between the order's admission and the fill's pre-witness, or between the fill's pre-witness and its confirmation | First sub-case: the fill's pre-witness reads `N_1 + 1`, `A` not in force → refused `ALLOCATION_NOT_IN_FORCE`. Second sub-case: the fill is `PROVISIONAL`; its confirmation reads `N_1 + 1`, `A` not in force → `UNESTABLISHED` | The order stays open until the first set under `TR-new` cancels it (PD-004.4, `CANCEL` row); the position is from `EFFECTIVE` fills only; the fill's validity is judged independently of the order's. No exposure is created under a revoked allocation | Yes: the Applied History is append-only, so "in force at `N_1` and at `N_2`" proves in force throughout |
| 12. Execution function dies between a fill's commit and its confirmation | `A` in force; fill `PROVISIONAL` | Confirm | Fill with pre-witness; no confirmation | Process ends | `PROVISIONAL` fill found by the fresh process; no further order for that version and instrument is derivable until confirmed | The fresh process calls confirm; the boundary reads now; `EFFECTIVE` if `A` in force and `t < T` still, else `UNESTABLISHED`. The standing is decided by the read, not by the fresh process's guess about when the fill happened. If the clock is unreachable the fill stays `PROVISIONAL` and the instrument stays frozen | Yes |

### Sequence: expiry, process death, recovery

```mermaid
sequenceDiagram
  participant AH as Applied History
  participant RUN as Strategy Runner
  participant EVB as Evidence boundary (clock)
  participant EX1 as Execution process 1
  participant PB as Paper Book boundary
  participant EX2 as Execution process 2 (fresh)

  Note over AH: TR-355 applied at N=68: EXPLORATORY 1 unit to SV-8.1, expiry_time T, FLATTEN
  RUN->>EVB: Decision SD (closure N=68)
  EX1->>PB: Set TR-355:68:SD, order .1 OPENING
  PB->>EVB: clock read
  EVB-->>PB: (t_w < T, E_w)
  PB-->>EX1: admitted; pre-witness (t_1, E_1, 68)
  PB-->>PB: fill .1 partial (seq 1 101), PROVISIONAL, pre-witness t_1 < T
  PB->>EVB: clock read (after the fill's commit)
  EVB-->>PB: (t_2 < T, E_2)
  PB-->>PB: confirmation of fill 1 101 (seq 1 102): EFFECTIVE
  PB-->>PB: fill .1 partial (seq 1 103), PROVISIONAL, pre-witness t_1 < T
  Note over EX1: process 1 dies at T − ε, before fill 1 103 is confirmed
  Note over EVB: T passes; no record is needed for it to pass
  Note over PB: any OPENING order, or fill of one, presented now is refused EXPIRED on the read
  PB-->>PB: fill for .1 presented (seq 1 104): refused EXPIRED on its pre-witness
  Note over EX2: fresh process; receives only ledger coordinates
  EX2->>AH: read head: TR-355 in force, T, FLATTEN
  EX2->>PB: read head: open order .1; fill 1 103 PROVISIONAL
  EX2->>PB: confirm fill 1 103
  PB->>EVB: clock read
  EVB-->>PB: (t_2 ≥ T, E_2)
  PB-->>PB: confirmation (seq 1 108): UNESTABLISHED; position = EFFECTIVE fills only
  EX2->>EVB: clock read
  EVB-->>EX2: (t ≥ T, E)
  Note over EX2: obligation outstanding: terminal state not established
  EX2->>PB: Set TR-355:68:EXPIRY: CANCEL .1; REDUCING .2 to zero
  PB->>EVB: clock read
  EVB-->>PB: (t_w ≥ T, E_w)
  PB-->>EX2: admitted; .1 closed at seq 1 110; .2 open
  PB-->>PB: fill for .1 presented at seq 1 112: refused ORDER_CLOSED
  PB-->>PB: fill .2 partial (seq 1 115)
  Note over EX2: process 2 dies during flatten
  Note over EX2: process 3 (not drawn): obligation still outstanding (position nonzero); appends REPLACE .2r to the existing EXPIRY set from EFFECTIVE fills at head; a second EXPIRY set is refused
  Note over AH: TR-356 (standing Transition) applied later: allocation 0, INCUBATING; any residual is executed to flat under TR-356's key
```

---

## PD-004.7. CPOC witnesses (design only; nothing is certified)

CPOC applicability for PD-004: `REQUIRED` — an allocation's expiry and
flattening obligation, the admission witness, and the expiry set are
persisted authority whose lawful continuation crosses process boundaries.

Journey, in the contract's form:

```text
fresh ledgers
→ Apply EXPLORATORY allocation A (T, quota, FLATTEN)
→ Decision; Decision set admitted with pre-witness t_1 < T; partial fill
  bracketed EFFECTIVE; second partial fill PROVISIONAL
→ PROCESS DEATH (Execution)
→ fresh process: reopen A, Paper Book head; confirm the PROVISIONAL fill
  (read t ≥ T → UNESTABLISHED); clock read t ≥ T
→ reconstruct: obligation outstanding (terminal state not established)
→ expiry set: CANCEL, REDUCING; partial fill
→ PROCESS DEATH (Execution)
→ fresh process: expiry set present; REPLACE remainder from fills at head
→ Apply standing Transition (allocation 0)
→ PROCESS DEATH
→ fresh process: residual to flat under the new key; historical read shows
  the labelled exploratory record, every refusal and every cancel
```

Boundary authority ledger at each restart: Applied History head and the
allocation in force with its content; the Evidence head and the clock
read with its bounding records; the Paper Book head, open orders, fills,
expiry set presence; derived positions at the Strategy and portfolio
levels; the derived obligation predicate; process identities.

Required negative witnesses:

- an `OPENING` order presented after `T` by any process, including a
  surviving Runner's, is refused on the read, never admitted on the
  absence of a record;
- an expiry set presented with a read `t_w < T` is refused `NOT_YET_DUE`;
- a second expiry set for the same `TransitionId`, from a second
  process, is refused `DUPLICATE`;
- a fill presented after its order's cancel is refused `ORDER_CLOSED`;
- a fill of an `OPENING` order presented on a read at or after `T` is
  refused `EXPIRED`, with or without a cancel;
- a fill whose pre-witness precedes `T` or a revocation and whose
  confirmation follows it is `UNESTABLISHED` and counts for nothing; a
  restart cannot make it `EFFECTIVE`;
- a `PROVISIONAL` fill blocks derivation for its version and instrument
  until a fresh read confirms it; no process's memory confirms it;
- an expiry set with cancels and no flatten does not discharge the
  obligation after restart; the terminal state does;
- a sell against an unfilled opposite-side buy is classed `OPENING`;
- a `REPLACE` keyed to a superseded allocation is refused
  `ALLOCATION_NOT_IN_FORCE`; a restart never re-targets a position from
  a superseded set;
- a materialized projection saying "unexpired" cannot admit an order;
  only a fresh read can;
- a boundary that cannot obtain a clock read admits no `OPENING` order
  and no expiry set; it does not use a local clock, a cached read or the
  Decision's commitment time;
- a witness `(t_w, E_w)` is consistent with the Evidence records at and
  after `E_w`; an inconsistent witness is detected by the historical
  read.

These witnesses test existing authority. None creates any.

---

## PD-004.8. What cannot be guaranteed during total process failure

- Real-time cancellation or flattening at `T`. While the Execution
  function is dead, the position stands and open orders stay open. What
  *is* guaranteed: no process can open exposure under the allocation
  after `T`, and no `OPENING` order can fill after `T`, because every
  admission, of an order or of a fill, is a positive read; and the
  obligation is derivable by the first process that reads.
- Durable witness of expiry during an Evidence-boundary outage. The
  clock keeps time; the ledgers cannot show it until a read succeeds.
  Nothing opens anywhere in the system meanwhile, since every opening
  order needs a read.
- Any admission while the Applied History is unreachable, and any write
  while the Paper Book is unreachable.
- The standing of a fill whose confirmation is delayed by an outage past
  `T` or past a revocation. It becomes `UNESTABLISHED` even if, in fact,
  it preceded both; the doctrine prefers to discard a possibly lawful
  paper fill over counting a possibly unlawful one. In a paper book that
  is a measurement artifact, recorded as such. A live venue's fill could
  not be discarded and would need the venue's time, a different time
  authority; live execution is outside this record.
- Flattening at all if the Principal's limit content lets a portfolio
  net limit refuse a version-level `REDUCING` order; then the refusal is
  the visible fact and the standing Transition is the route.

The doctrine guarantees lawfulness and derivability, not promptness.
Promptness is an operating expectation the Principal may state in the
Execution Authorization; it is not constitutional text and it creates no
authority.

---

## PD-004.9. Two Strategies through the same rules

### Traditional momentum: `SV-8.1`, allocation `TR-355`

| Step | Record | Rule |
| --- | --- | --- |
| 2027-01-29 | `TR-355` applied at `N=68`: `EXPLORATORY` 1 unit to `SV-8.1`, purpose "measure fills and Friday clustering", `quota_events 5`, `expiry_time 2027-03-19 17:30`, `FLATTEN`. `CK-A2`: pool capacity; composition; purpose, expiry, quota stated; cites no Evaluation. Principal admits | PD-004.1; Part V |
| Fridays 02-05 to 03-05, 17:02 | Decisions index 1 to 5 (closure `N=68`). Sets `TR-355:68:<seq>`; every order carries witness `(t_w < T, E_w, 68)`; `OPENING` and `REDUCING` orders admitted; name Q goes flat → long 40 (`OPENING`) on 02-19 | PD-004.4 (a) to (e) |
| 03-12 17:02 | Decision index 6 > 5. Set derived; `OPENING` orders refused `QUOTA_EXHAUSTED`; `REDUCING` admitted. Q target −30: derived as two orders, sell 40 (`REDUCING`, admitted) and sell 30 (`OPENING`, refused). Q ends flat, not short | PD-004.3 split; PD-004.5 quota without expiry |
| 03-15 | Runner process dies. The 03-19 event will have no Decision; derivable as missing | Case 1 |
| 03-19 17:30 | `T`. The Execution function's next read, 17:30:40, shows `t ≥ T`; no set `TR-355:*:EXPIRY`. It derives the expiry set: `CANCEL` for two open orders of set `:2 9xx`; `REDUCING` orders to zero in the eleven names still held. Witness `(17:30:41, E_w, 71)` (two unrelated Transitions applied since 68). A fill of one of those orders bracketed at 17:29:10 and 17:29:12 is `EFFECTIVE`; a fill with pre-witness 17:29:59 whose confirmation read 17:30:02 is `UNESTABLISHED`; a fill presented at 17:30:50 is refused `EXPIRED`; the flatten order for that name is derived from the `EFFECTIVE` fills | PD-004.5; case 4 |
| 03-19 17:33 | Execution process dies with three flatten orders partially filled. Fresh process at 17:40: expiry set present; derives `REPLACE` for each remainder from fills at the head; a late fill presented for a cancelled order is refused `ORDER_CLOSED` | Cases 4, 6, 7 |
| 03-22 | `TR-356` (standing Transition, proposer Principal; `CK-H1` verifies the expiry set, six refusals, two cancels, residual 0) applied at `N=72`: allocation 0, `INCUBATING`. Had a residual remained, the next Execution read would derive `REDUCING` orders under `TR-356:72:<seq>` to a target of zero | PD-004.5 backstop |
| Later | `EV-2xx` shows the exploratory executed record, labelled: fills, clustering of Friday 17:02 orders, the quota refusals, the reversal refusal, the expiry flatten and its shortfall. Grounding series: the decision-implied record only | PD-004.1 |

### Forward product rebalancing: `SV-40.1`, allocation `TR-415`

| Step | Record | Rule |
| --- | --- | --- |
| 8e, 2026-12-18 | `TR-415` applied at `N=63`: `EXPLORATORY` 1 unit to `SV-40.1`, purpose "measure fill quality and timing sensitivity of 15:30 entries", `quota_events 10`, `expiry_time 2027-01-04 09:00`, `FLATTEN` | PD-004.1 |
| Qualifying days 12-21 to 12-30 | 15:30 Decisions (index 1 to 7) open; 16:00 Decisions flatten. Each 15:30 `OPENING` order carries `t_w < T`; each 16:00 order is `REDUCING`. On 12-30 the 16:00 flatten is partially filled in an illiquid name: residual 0.2 units stands | PD-004.4 |
| 12-31 to 01-03 | No qualifying days; no decision events. The Observation function's 12-31 feed slot returns `RETRIEVAL_FAILED` and then it stops. Nothing about expiry reads it | Cases 2, 8 |
| 01-04 09:00 | `T`. First Execution read at 09:00:05: obligation outstanding. Expiry set `TR-415:63:EXPIRY`: no open orders, one `REDUCING` order for the 0.2 residual. Admitted with witness `(09:00:06, E_w, 65)` (serial admission moved the head to 65 over the holiday). Filled at the open | PD-004.5 |
| 01-04 15:30 | A qualifying day; the Runner commits Decision index 8. The Execution function derives no set: `A` expired. The Decision is scored in the decision-implied record | PD-004.5 rule 5 |
| 9b, 01-06 | `TR-416` applied `65 → 66`: allocation 0, `INCUBATING`; Checker verified the expiry set and that the residual was closed | Backstop |
| 9d, 01-20 | `EV-200`: exploratory record labelled, including the holiday residual and its flatten shortfall; excluded from grounding; `TR-420` (`QUALIFIED` 3) cites the decision-implied record only | PD-004.1 |

Both cases run under one set of rules. The momentum case exercises the
quota, the reversal split, Runner death and duplicate recovery; the
forward case exercises expiry with no Decisions scheduled, Observation
function death and a residual from an incomplete flatten.

---

## PD-004.10. Constitutional Delta

```text
ΔO: +1 Paper Book record kind: the fill confirmation, bound to a
    FillId, carrying a read taken after that fill's commit. Declared as
    ΔO because it is a new kind of entry on an existing ledger, not
    merely new content of an existing kind; no new object, ledger,
    identity rule or relationship. Capital standings, expiry, quota and
    instruction are allocation content; the pool is a limit; the
    admission witness and intent class are order content; the expiry
    set is an order set with a reserved suffix; fill standing is derived.

ΔS: §III.3 Strategy: capital standings. §III.5 Evidence: the clock read
    defined; a read commits nothing and assigns no Evidence time.
    §III.6: exploratory pool as a limit; the "in force" definition.
    §III.10 Paper Book: admission witness (t_w, E_w, N_w) on orders and
    fills; intent class on the working position; opening per instrument
    away from or through zero; mandatory split at zero; admission rules
    per class with reason codes; the bracketing contract (pre-witness,
    post-witness, monotone conditions, logical admission point); fills
    of OPENING orders PROVISIONAL until confirmed, EFFECTIVE or
    UNESTABLISHED by the confirmation read; positions from EFFECTIVE
    fills; same-side working position; PROVISIONAL_PENDING refusal;
    CANCEL on supersession by a newer allocation; the expiry obligation
    defined by the terminal state and the expiry set open-ended;
    expiry set keyed
    TransitionId:StateVersion:EXPIRY, one per TransitionId; cancel closes
    an order at its sequence and a later fill is refused; positions per
    version per instrument; re-execution to a target of zero under an
    allocation of zero; incomplete flatten as a derived fact.
    Part IV, I-13: the Paper Book commit boundary's reads of the Applied
    History head and the Evidence clock at admission are reads; refusal
    when unreachable. Part V: Allocation Transition content (purpose,
    expiry_time, quota_events, instruction FLATTEN default, HOLD bounded
    with hold_expiry_time, FLATTEN_ON_QUOTA optional); Order row names
    the expiry trigger; standing Transition after expiry; Evaluation
    non-conformance when an exploratory figure enters a grounding series.
    Part VI: T-H (the momentum expiry and recovery case above).
    Part VII: admission witness (Paper Book fact; time value a RECEIPT of
    the clock's answer); expired standing, obligation and incomplete
    flatten DERIVED; the Execution function's copy of allocation content
    EPHEMERAL.

ΔA: Two items, declared as authority so that neither hides in a duty.
    (1) Execution Authorization: permitted triggers extend from
        "committed Decisions" (PD-002.4) to "committed Decisions, and
        the expiry_time, hold_expiry_time and, where declared, quota
        exhaustion of an applied allocation, as established by a clock
        read". The Execution function may act on an instant no Decision
        produced. It gains no commit right beyond the Paper Book facts it
        already commits and no right to open exposure.
    (2) Paper Book commit boundary: reads the Evidence commit boundary's
        clock at admission and records the read. Declared as a read right
        in case the clock is not regarded as an authoritative ledger
        under I-13. It assigns no Evidence time, creates no clock and
        decides nothing but its own admission.
    No time authority is created. No admission authority moves. No
    Research, Checker, Observation or Runner Authorization gains or loses
    a right.
```

---

## PD-004.11. Parameters the Principal sets outside the Constitution

| Parameter | Where |
| --- | --- |
| Exploratory pool size; per-version cap; lifetime cap on exploratory cycles per version (UD-10) | Limits Transition |
| `expiry_time`; `quota_events`; instruction; measurement purpose | Each `EXPLORATORY` Allocation Transition |
| `HOLD` reason, `hold_expiry_time`, exit conditions | The Allocation Transition or a successor decided by the Principal |
| Whether portfolio net limits may refuse a version-level `REDUCING` order; per-instrument exposure limits | Limits Transition |
| Whether a `NON-REPRODUCIBLE` version may hold an `EXPLORATORY` allocation (UD-3) | Check content of the Allocation Transition, by Principal decision |
| Promptness expectation for discharging expiry obligations | Execution Authorization, as an operating expectation |
| The paper fill rule (how a paper order fills against Observations) | Plan step 7; not PD-004 |

No number appears in the Constitution.

---

## PD-004.12. Alternatives rejected and preserved

| Alternative | Why rejected |
| --- | --- |
| Deadline event (revision 1): the first Observation record witnessed at or after `T` | Its existence proves `T` passed; its absence proves nothing, yet revision 1 admitted on absence. Couples expiry to the Observation plan and fails when the Observation function is dead. An Observation record at or after `T` remains valid corroboration that `T` passed; it is no longer the mechanism |
| A Paper Book clock (UD-14) | A second time authority; forbidden by the Principal and by §III.5 |
| An Evidence-boundary timer that commits "deadline" records | The boundary would originate records from a process-local timer; a new role |
| Flattening by the Runner | Contradicts PD-002.4: the Runner may not touch capital or the Paper Book |
| Decision-count expiry (PD-003 revision 3) | No calendar expiry; no flatten on a dead Runner |
| Admit on the Decision's commitment time | A previously committed timestamp says nothing about the instant of admission |
| Free `CANCEL` by the Execution function during outages | A discretionary right outside any trigger; rejected to keep the trigger set exact. Consequence accepted: open orders may fill during a clock outage |
| Flatten everything when time cannot be established | Acts on an allocation still in force without authority to end it; the fail-closed action is to refuse opening, not to close |
| Automatic expiry in the projection without a standing Transition | Only Apply changes allocation |
| Treat the pre-witness as the commit's time and authority (revision 2) | A read is never simultaneous with a commit on another ledger; the gap admits exposure after `T` or under a revoked allocation |
| Use the next Paper Book record's pre-witness as the post-witness (implicit chaining) | Delays confirmation until some unrelated commit happens, and gives that record a meaning it was not committed to carry |
| Have the Evidence boundary stamp Paper Book commits | The Evidence boundary would originate records for another ledger's events; a new role and a hidden second commit boundary |
| Bracket orders as well as fills | Adds a record per order and establishes nothing more: an order creates no exposure, cannot fill effectively after `T` or revocation, and is cancelled |

---

## PD-004.13. Decisions for the Principal

| Question | Proposal |
| --- | --- |
| Admit `ΔA` (1), the trigger extension | Yes; it is the smallest change that makes expiry independent of the Runner |
| Admit `ΔA` (2), the clock read at admission | Yes; it replaces absence with a positive read and creates no clock |
| `REDUCING` orders in a Decision set admitted without a clock read (fail-open on risk reduction) | Yes, as drafted; the alternative strands a Strategy that wants to cut risk during a clock outage |
| `FLATTEN_ON_QUOTA` optional; `HOLD` bounded with its own instant | As drafted |
| Observation slot-density limit recommended in revision 1 | Withdrawn; no rule reads Observation records for expiry |
| UD-14 (Paper Book clock) | Close by rejection on admission; the Paper Book reads the one clock |
| `ΔO` +1: the fill confirmation record | Admit; it is the only way a commit on one ledger can be shown to precede a change on another without a second clock or an assumption of instantaneity |
| `UNESTABLISHED` discards a straddling paper fill rather than counting it | As drafted; the alternative counts exposure that may have arisen after expiry or revocation |

## PD-004.14. What happens on admission

Constitution revision for §III.3, §III.5, §III.6, §III.10, I-13, Part V,
Part VI (T-H), Part VII; PD-003's exploratory rows (momentum table; 8e,
9b, 9d) replaced by PD-004.9; FR-12 closed by reference; UD-14 closed by
rejection; re-audit for the clock read, the bracketing contract, the confirmation
record, the admission rules per intent class, and the twelve recovery
cases; then `ES-1` with FR-6 and FR-8.

---

## PD-004.15. Internal-simulator clarification (Principal, 2026-10-19)

New Speedway executes paper orders on an **internal simulator**: the
Execution function's fill rule, named in its Execution Authorization,
proposes fills against the Paper Book under the rules above. External
broker paper accounts and live venues are outside the design; nothing
here claims to hold for them.

| Term | Meaning |
| --- | --- |
| **Provisional simulated fill** | A fill the fill rule proposed for an `OPENING` order and the Paper Book boundary admitted with a pre-witness. An operational record of what the simulator proposed and when the boundary admitted it. Not execution. Contributes to no position, cash, exposure or P&L |
| **Confirmed execution fact** | A fill whose confirmation record carries a post-witness satisfying the bracket, or a fill of a `REDUCING` order (effective at commit). The only kind of fill that contributes to positions, cash, exposures and P&L |
| **Unestablished fill** | A fill whose confirmation does not satisfy the bracket. A durable operational record, preserved under the label, never deleted, never counted as completed execution, shown in the exploratory record as a simulator artifact |

Rules added by the clarification:

1. **Positions derive from confirmed fills.** Wherever this record or
   the Constitution says positions, cash, exposures or P&L derive from
   fills, it means `EFFECTIVE` fills. There is one definition of an
   effective fill, above, and no other carrier may count a fill.
2. **Conservative accounting of provisional fills.** For any check that
   could permit exposure (intent class, limits, opening admission), a
   `PROVISIONAL` fill of the same version and instrument counts as if
   filled; for any claim of reduction it counts as unfilled. The
   `PROVISIONAL_PENDING` refusal remains: no further order for that
   version and instrument is derived until confirmation. Across
   instruments and versions, provisional fills consume limit capacity as
   if filled, so two provisional fills cannot together exceed a limit
   that either alone respects: the second is admitted against the first
   by Paper Book sequence.
3. **Reproducible confirmation.** A fill's standing is a deterministic
   function of its pre-witness, its confirmation's post-witness and the
   applied allocation's content (`expiry_time`, in force at `N_1` and
   `N_2`). Any reader recomputes it from the ledgers; the confirmation
   record asserts nothing a reader cannot verify.
4. **No rewriting.** A confirmation never changes the fill, the order,
   the pre-witness or any earlier record; it appends the post-witness
   and the standing follows. A later confirmation of an earlier fill
   cannot alter positions already derived at a `StateVersion` and Paper
   Book sequence before it: a position is always stated at a sequence,
   and includes only fills `EFFECTIVE` at that sequence.
5. **Reducing without a clock** stays as PD-004.4: admitted only against
   `EFFECTIVE` positions, the same-side working position with provisional
   fills counted conservatively, the allocation in force and the limits
   at the Applied History head.
6. **U-8 open.** Limits can change in either direction between a
   pre-witness and a post-witness; the bracket establishes nothing about
   them. Checked at the pre-witness only.
7. **Fill methodology** (how the simulator decides a fill from
   Observations) is plan step 7 content and is not defined here.

Constitutional Delta of this clarification: `ΔO` none beyond the Fill
Confirmation already declared; `ΔS` the refinements above; `ΔA` none.
The simulator is a method of the Execution function under its existing
Authorization, not a new committer.
