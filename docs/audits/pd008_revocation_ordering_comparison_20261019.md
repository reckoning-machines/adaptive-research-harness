# PD-008 Revocation Ordering: Alternatives A and B

Status: **COMPARISON — EVIDENCE, NOT DOCTRINE. Decides nothing.** Principal's choice, 2026-10-19: **Alternative A**, prepared as PD-008 revision 4 (document revision authorized; not admission, not implementation).
Prepared 2026-10-19 at the Principal's direction, with
[PD-008 revision 3](../decisions/principal_decision_008_research_budget_reservation.md)
held and PD-007 untouched. The question: when the Principal revokes a
Research Authorization, what ordering between **attempt admission**
(an Evidence commit) and **revocation** (an Apply) do the existing
owners and boundaries establish, and which policy should the paper
prototype adopt? External provider execution is outside every ordering
boundary in both alternatives.

## The two ledgers and the one fact that matters

An attempt is admitted at the Evidence commit boundary, which totally
orders Evidence by sequence (I-8). A revocation is applied at the
Applied History boundary, which totally orders Transitions by Apply
sequence. The two orders are not related to each other by anything in
the Constitution: a commit on one and an Apply on the other have no
defined "before". Any policy that says "an attempt precedes a
revocation" must either **put both events on one ledger** (A) or
**define precedence by a recorded witness and accept the gap** (B).

## Alternative A: an enforced common ordering

**Mechanism, the smallest compatible with existing owners.** Revocation
of a Research Authorization is made effective for funding by a record
**on the Evidence ledger**: a Research Record of kind `FENCE`, committed
by the Principal under the Principal's own authority (Part V, other
Evidence commit), naming the `AuthorizationId`. From the fence's
sequence onward the Evidence boundary refuses every `RESERVATION` and
every `PENDING` attempt under that Authorization (`FENCED`); settlements
remain admissible above it. Because attempts and the fence are on one
ledger, their order is exact: an attempt with sequence below the fence
precedes the revocation and may dispatch and settle; one presented
above it is refused. The revocation Transition itself is unchanged in
owner and boundary: it records the Authorization's standing in the
Applied History, and its Check verifies that a fence for the
Authorization exists (the Checker reads the Evidence ledger, as every
Check does); Apply refuses a revocation without one. Order of the
Principal's two acts: fence, then Transition.

The Evidence boundary keeps its PD-002 read of the Applied History head
as a second refusal (`AUTHORIZATION_INACTIVE` where the head already
shows the revocation); that read is no longer what establishes
ordering, so none of revision 3's additions is needed: no outstanding
permission, no read-to-commit interval, no straddler view, and **no
Apply witness read of the Evidence head**.

**Crash behavior.**

| Death | State | Recovery |
| --- | --- | --- |
| Agent process dies after its own (ephemeral) read, before presenting the attempt | Nothing committed, nothing dispatched | A fresh process presents the attempt; the boundary orders it against any fence at commit. No permission survived the process because none existed outside a commit |
| Agent dies after the attempt commits, before dispatch | A `PENDING` attempt below any later fence | Dispatch is lawful under the committed attempt; the fence, if one later appears, does not reach it; settlement follows. This is the only "permission that survives": a committed record, not a read |
| Principal commits the fence, dies before the revocation Transition | Authorization active in the Applied History, fenced on the Evidence ledger | Fail-closed: nothing under it is funded; the standing is completed by the Transition on recovery; the state is visible as "active, fenced" |
| Principal proposes the Transition without a fence | Check `FAIL` (no fence); or Apply refused | The Principal commits the fence and re-proposes |
| Evidence boundary crashes mid-commit | The commit either exists with its sequence or does not | Ordinary ledger atomicity; nothing partial |

**What A does not order.** The provider's execution. An attempt below
the fence may have its request executed after the fence; that is
external and settles under the attempt. Nothing changes here from
revision 3.

**OSA delta of A.**

```text
ΔO: +1 Research Record kind FENCE (Evidence ledger; committed by the
    Principal), in addition to RESERVATION. Justification: the one fact
    that orders funding against revocation must live on the ledger
    that orders attempts; no existing record carries it.
ΔS: the Evidence boundary refuses RESERVATION and PENDING attempts at
    or above a fence for the Authorization; settlements admissible
    above it; revocation or amendment of a Research Authorization
    requires a prior fence, verified at Check, refused at Apply
    without one. Revision 3's outstanding permission, read-to-commit
    interval, t_r and t_c beyond PD-002's existing stamp, the
    straddler view and the Apply witness read are withdrawn as
    unnecessary.
ΔA: NONE. The Principal exercises the revocation right it already
    holds through two acts instead of one; no other party gains or
    loses a right; the Evidence boundary's refusal is the existing
    invariant applied to one more record.
```

## Alternative B: a bounded permission from the authorization read

**Mechanism.** As revision 3: the Evidence boundary reads the Applied
History head inside the attempt commit; a witness below the
revocation's Apply sequence is admitted and defined to precede it; one
at or above is refused. The read confers a permission for one commit by
the reading boundary within its own read-to-commit interval.

**Additional exposure, stated plainly.** Every attempt whose boundary
read fell before the revocation's Apply but whose commit fell after it
is admitted, dispatched and charged. The number of such attempts is
bounded only by the attempt rate across every agent under the
Authorization multiplied by the boundary's read-to-commit interval;
each is bounded by its estimated maximum for metered units and
provider-capped calls, and unbounded above the estimate for uncapped
calls. A revocation under B therefore stops funding one read-interval
late, per boundary, and the doctrine cannot say exactly which attempts
fell inside that interval (below).

**Expiry and process death.** The permission exists only inside the
boundary's commit; it is not a durable fact. An operation interrupted
after the read and before the commit has no permission: a fresh process
presents a fresh commit, and the boundary takes a fresh read by
construction. An operation interrupted after the commit holds a
committed attempt, which is lawful to dispatch under B exactly as under
A. A declared maximum read-to-commit interval bounds the window in time
but cannot order it against the Apply.

**The straddler claim, corrected.** Revision 3 said an attempt with
witness below the revocation and Evidence sequence above the Evidence
head the Apply witnessed was "committed after the revocation witnessed
the Evidence ledger". That is not exact ordering. The Apply's witness
read happens before the revocation itself commits; Evidence can advance
between that read and the Apply. An attempt committed in that gap has a
sequence above the witnessed head and was nonetheless committed before
the revocation applied. The two ledger references therefore identify
**potential overlap**: an attempt with sequence at or below the
witnessed head certainly preceded the revocation; one above it may have
preceded it or not. The view is conservative in one direction only, and
no clock or record is added here to recover exact chronology. Under B
the Apply witness read is optional: it refines visibility, it does not
establish lawfulness, and lawfulness under B is by the witness
definition alone.

**OSA delta of B.**

```text
ΔO: +1 Research Record kind RESERVATION (as PD-008 revision 2).
ΔS: as revision 3: precedence defined by the attempt's witness against
    the revocation's Apply sequence; outstanding permission and its
    scope; the optional read-to-commit interval; the potential-overlap
    view, corrected as above, if the Apply witness read is kept.
ΔA: NONE claimed; the Apply witness read, if kept, is reported for the
    Principal's classification (ΔS by the PD-002 precedent, or ΔA +1
    read right). If the read is dropped, nothing to classify.
```

## Three sequences

Grant `AU-40`; agent `AD-21.1`; reservation `R-11`. Illustrative
sequence numbers.

**Normal sequence (identical under A and B).**
`R-11` reserved at `E = 3 100` (boundary read: `AU-40` active at head
94) → attempt A-1 `PENDING` at `E = 3 105`, max 5 → dispatch → provider
responds → settlement at `E = 3 140`, actual 4, releasing 1 →
`R-11` closed at `E = 3 160`, remainder released.

**Contested revocation.**

| Step | A | B |
| --- | --- | --- |
| The Principal decides to revoke `AU-40` | Commits `FENCE(AU-40)` at `E = 3 150` | Proposes `TR-630` |
| Attempt A-2 presented by the boundary at `E = 3 149` | Admitted: below the fence; dispatches; settles later | Admitted if its read saw head < 95 |
| `TR-630` checked and applied | Check verifies the fence at 3 150; Apply at `R = 95` | Apply at `R = 95` |
| Attempt A-3 presented at `E = 3 151` with a read that saw head 94 | Refused `FENCED`, exactly, regardless of what its read saw | **Admitted**: witness 94 < 95, under outstanding permission; dispatches and charges |
| Attempt A-4 with a read that saw head 95 | Refused `FENCED` (and `AUTHORIZATION_INACTIVE`) | Refused `AUTHORIZATION_INACTIVE` |
| What the Principal can say afterward | Every attempt at or above 3 150 was refused; every one below it preceded the revocation | Every attempt whose read saw 95 was refused; some attempts committed after `TR-630` applied were admitted; which ones is not exactly knowable |

**Recovery after death before attempt commit.** Under both: the agent
read the head (ephemerally), prepared attempt A-5, and died before
presenting it. Nothing is on any ledger; nothing was dispatched. A fresh
process presents A-5; the boundary commits it with a fresh read. Under
A it is ordered against the fence at its own sequence: admitted below,
refused above. Under B it is admitted or refused by the fresh read's
witness. In neither case does anything from the dead process survive.

## Recommendation

**Alternative A** for the paper prototype. It is simpler in every
dimension that matters here: one new record and one refusal rule in
place of a permission semantics, an interval constant, a corrected
overlap view and a read whose classification is open; exact ordering on
the ledger that already orders attempts; fail-closed crash behavior in
every case; nothing that depends on how fast a boundary commits; and no
need to describe to the Principal which attempts slipped through,
because none can. Its cost is one extra act by the Principal when
revoking, which a Check enforces. The Apply witness read is not needed
under A and its classification can be dropped rather than deferred.

If A is chosen, PD-008 revision 4 would: add `FENCE`; withdraw
revision 3's outstanding permission, interval, instants beyond PD-002,
straddler view and Apply witness read; restate case 6 as the fence
sequence above; and report `ΔO` +2 (`RESERVATION`, `FENCE`), `ΔS` as
listed, `ΔA` none. PD-007 would be unaffected except that `P-1`'s
condition (b) reads a reservation below any fence.
