# Principal Decision Record 007 — Independent Checking, Bounded Autonomous Admission, Concurrent Budgets

Status: **ADMITTED 2026-10-19 by the Principal (document-phase admission): revision 3, as written, with its declared delta.** Applied to the Constitution as revision 9 and re-audited in [osa_reaudit_pd007_20261019.md](../audits/osa_reaudit_pd007_20261019.md). Admission text, as approved:

```text
ADMITTED 2026-10-19 by the Principal (document-phase admission): PD-007
revision 3, D-10 (independent checking) and D-11 (bounded autonomous
admission, policy P-1), with the declared Constitutional Delta.

Clarifications on admission:
(a) Successor Agent Design registration, by the Principal or by P-1,
    grants no Authorization. A successor cannot inherit permission
    merely through lineage; it holds nothing until the Principal grants
    an Authorization by Transition.
(b) Neither delegated right can widen a budget, cap, scope, expiry,
    Authorization or reservation.
(c) This is a document-phase admission, not a claim that a
    Constitutional Transition executed before genesis.

Constitutional Delta admitted:
ΔO: NONE.
ΔS: §III.8 Independence: separate authority, protected standards,
    evidence the proposer cannot rewrite; provider as provenance and an
    Authorization option. §III.8 and Part V: the Check record form as
    the only carrier of a Check; FAIL versus STOP; the budget line
    (reservation covers the declared budget; remaining spendable
    recorded, never a second requirement). §III.5 and Part V: the
    Checker commits expected-but-missing Outcomes before a citing Check
    (U-10 closed); every grounding Decision REPRODUCED before PASS.
    Part V admitted policy P-1: two classes, six conditions,
    attribution, suspension, revocation, the empirical-path rule, the
    reservation list including FENCE.
ΔA: +1 admitted policy P-1: the decision right for Hypothesis
    registration within an authorized scope and for successor Agent
    Design registration without authority expansion moves from the
    Principal to P-1 for instances meeting its conditions, revocably.
    No other right moves; the Checker gains none.

Closed by this admission: D-10, D-11, U-10, U-3, FR-4 (Check contract).
Open: UD-4 (deferred); P7-R1, P7-R3; D-17, N-1 (genesis, PD-009
proposed); every earlier re-audit item.
```

Prior content follows. Revision
3 (2026-10-19) makes the two wording corrections found in the readiness
review against admitted PD-008 (the Check's budget line; `FENCE` in the
reservation list) and states that a registration never funds the same
obligation twice; the proposed delta is unchanged. Depends
on PD-001 to PD-006 (admitted, Constitution revision 7) and on
[PD-008](principal_decision_008_research_budget_reservation.md)
(proposed) for the reservation that policy `P-1`'s budget condition
reads. Carries a declared `ΔA`: the first admitted policy. Changes no
Constitution text until admitted. Revision 2 (2026-10-19): D-12 moved to
PD-008 after the Principal rejected reservation by derivation; `P-1`'s
budget condition rewritten; the two delegated rights stated explicitly
with the rule that neither may widen a budget or Authorization.

Date: 2026-10-19 (revisions 1 and 2: same day)

Subjects: D-10 (sufficiency of Checker independence; carries U-10
Outcome committer, UD-4 Checker extraction, FR-4 Check contract); D-11
(the Principal bottleneck; the empty "admitted policy" slot of Part V).
D-12 is PD-008.

Sources: Constitution revision 5 §III.4 (method class), §III.7, §III.8
(Independence, TENTATIVE), §III.9, I-6, I-7, I-9, I-13, I-14, Part V;
[initial audit](../audits/initial_osa_audit.md) D-10, D-11, D-12;
PD-002.4 (Runner), PD-003.5 (`CHECKER` method class), PD-005 §3 (Check
content); the fin123-core CPOC certification contract (boundary
authority ledger form, adopted); the Principal's brief of 2026-10-19;
focused audit
[osa_audit_pd007_proposed_20261019.md](../audits/osa_audit_pd007_proposed_20261019.md).

The goal, as the Principal stated it: autonomous research inside
approved limits, not human approval of every Hypothesis.

---

## PD-007.1. D-10 — Independent checking

### What independence is

A Check is independent when three things hold at once. None of them is
a property of a model provider.

| Condition | Meaning | Where it is enforced |
| --- | --- | --- |
| **Separate authority** | The Check is performed under a Checker Authorization granted by the Principal to a grantee that is not the proposer, did not act under the proposer's Authorization, and is not an Agent Design Version in the proposer's lineage (§III.8, kept). A `CHECKER` method-class lineage (PD-003.5) holds no Research Authorization and proposes nothing but its own successor, whose registration another Checker checks and the Principal decides | Authorization content; the Check boundary refuses a Check by an unqualified party |
| **Protected standards** | The Check is performed under the `ConstitutionVersion` and `EvaluationStandardVersion` in force at the Transition's `BaseStateVersion`, both named in the Check record. A Checker may not change, waive, add or reinterpret a criterion (I-7). A Check performed under other criteria is void, preserved, and grounds for the Principal to revoke the Checker Authorization. A Checker who believes a criterion is wrong proposes a Constitutional Transition, which is `STOPPED` until the Principal decides; the Check at hand is decided under the criteria as they stand | The Check record form; §III.9 |
| **Evidence the proposer cannot rewrite** | The Check reads only committed records, by ledger and sequence, within a declared closure `(E, N, F)` at or below the heads at the Check; the proposer's working memory, conversation, cache or uncommitted artifacts are not evidence and may not be cited. The Check record is appended to the Transition's lifecycle by the Checker and is immutable; the proposer cannot amend it, only propose again | I-13; the Transition ledger |

**Model provider.** A different provider from the proposer's does not
establish independence, and the same provider does not defeat it; what
decides is the three conditions above. The provider and version of
both parties are **provenance** recorded in the Check record (PD-002.6).
The Principal may, as content of a Checker Authorization, require a
provider different from the proposer's, or a human, for named Transition
classes; that is an Authorization choice, not a doctrine rule.

### The Check record

Every Check appends one record to the Transition's lifecycle, in this
form (the fin123-core boundary authority ledger, adopted in shape):

1. `TransitionId`, class, `BaseStateVersion`; proposer identity and
   Authorization.
2. Checker identity; Checker Authorization; provenance of both parties
   (provider, model version, training cutoff where an Agent Design).
3. `ConstitutionVersion` and `EvaluationStandardVersion` in force at the
   base; the closure read `(E, N, F)` with the Evidence-clock instant of
   the read.
4. Observations, one line per criterion of the class's Check column in
   Part V, each `MET`, `NOT MET` or `NOT DETERMINABLE`, citing the
   records by sequence. For every class: within the proposer's
   Authorization; base state current at the time of Check; and the
   **budget line**, which distinguishes two quantities and requires only
   the first: (i) the proposal's declared research budget is covered by
   the cited `RESERVATION`, read by sequence, which is open, below any
   `FENCE` for the Authorization, of amount at least the declared
   budget, and of purpose "pending registration" of this Transition;
   (ii) the Authorization's remaining spendable budget (PD-008's five
   states), read and recorded for attribution and never imposed as a
   second requirement, because the reservation already holds the
   obligation and a registration never funds the same obligation twice.
   For registrations: not a restatement of a closed question without a
   declared difference (FR-4); every cited Research Record's closure
   within the proposer's scopes; for a Historical Reconstruction
   research record, **authored knowing the period** recorded as a
   finding, so that no reconstruction is mistaken for a prospective
   result. For Transitions citing an Evaluation: the `ES-1` conformance
   items (class of the grounding series; `N_eff` and its committed
   method with its commitment sequence below the window; family
   reconciliation; cost evidence distinguished from modelled impact and
   simulated fills; stress floor and `a*`; no exploratory figure in
   grounding; disclosed method changes); the Checker's own recomputation
   of the Evaluation from its closure and whether it matched.
5. Reproduction records the Checker committed for this Check (below),
   by sequence.
6. Result: `PASS`, `FAIL` (every criterion determinable, at least one
   `NOT MET`, reasons named), or `STOP` (any criterion
   `NOT DETERMINABLE` because an identity, meaning, owner or authority
   the Constitution does not supply would be needed; I-14).
7. Escalation flag and reason, where set (below).

The Check record is the only carrier of a Check. A Check not in this
form is not a Check.

### Reproduction obligations

- Only a party under a Checker Authorization may commit a reproduction
  record (PD-002, kept). Reproduction standing stays `DERIVED` from the
  set of records.
- Before a Check `PASS` on a Transition whose cited Evaluation grounds
  on Strategy Decisions, every Decision in the grounding series must
  carry `REPRODUCED` standing; the Checker commits the missing
  reproduction records as part of the Check or returns `FAIL`.
- For `INCUBATING` versions with no citing Transition, reproduction is
  on a schedule the Checker Authorization declares (a sample or all);
  `ES-1` counts only `REPRODUCED` Decisions in any case.
- A reproduction that diverges is `UNREPRODUCED`; a disagreement between
  two Checkers' reproductions is `DISPUTED` and escalates.

### Outcome committer (U-10)

Outcomes stay committable by any authorized party, as drafted, because
an Outcome is a deterministic function over a bound set that any reader
recomputes. Two duties close the omission risk: expected Outcomes are
derivable from each Prediction's resolution set and the Observations
witnessed, and an Evaluation that finds an expected Outcome missing is
non-conforming; and **the Checker commits every expected-but-missing
Outcome of the subject before completing a Check that cites its
record**, under its Checker Authorization. No function on a
"set complete" trigger is created. `ΔA`: none; Outcome commit was
already open to the Checker.

### Checker extraction (UD-4)

Deferred. Neither prototype needs document resolution beyond
deterministic extraction (PD-003.3). Carried.

### Refusals and escalation to the Principal

| Event | Consequence |
| --- | --- |
| Check `FAIL` | Transition `CHECKED (FAIL)`, preserved; the proposer may propose again with a declared difference |
| Check `STOP` | Transition `STOPPED`, preserved; the question returns to the Principal; no policy may decide it; the proposer does not work around it (I-14) |
| Check by an unqualified party, or under criteria other than those pinned at base | Refused at the Transition ledger's Check boundary, preserved; grounds for revoking the Checker Authorization |
| `DISPUTED` reproduction | Escalated; the Principal decides, as PD-002 provides |
| A Checker that `PASS`es a Transition later found non-conforming | Recorded in the Checker lineage's Agent Design Evaluation as verification yield (`ES-1`); the Principal decides on the Authorization |
| Proposer and Checker disagree on proposition equivalence | The Principal decides (PD-001.2, kept) |

A Checker cannot legalize a proposal: it cannot change the criteria,
cannot cite uncommitted evidence, cannot act outside its Authorization,
and cannot decide; it can only record whether the criteria as pinned
were met.

---

## PD-007.2. D-11 — Bounded autonomous admission: policy `P-1`

### What an admitted policy is

A rule placed in the Constitution by Constitutional Transition (Part V,
"admitted policy") under which the Apply boundary admits a Transition of
a named class without a per-instance Principal decision, when and only
when every condition of the policy holds at Apply against the head
(I-9, re-checked). The decision is attributed to the policy's admitting
Transition and to the Check it rests on. A policy decides nothing on a
`FAIL`, nothing on a `STOP`, and nothing it was not named for.

### `P-1`, routine research admission

| Element | Rule |
| --- | --- |
| **The two delegated decision rights, exactly** | (i) **Hypothesis registration within an authorized scope**: the decision to admit a Hypothesis to the population when its funding Authorization, scope, reservation and Check all hold. (ii) **Successor Agent Design Version registration without authority expansion**: the decision to admit a successor to the population when it requests no Authorization. **Neither right may widen its own budget or Authorization**: a registration under `P-1` cannot increase a grant, a cap, a scope or an expiry, cannot create or amend an Authorization, and cannot reserve on its own behalf beyond the reservation the proposer already committed; any proposal that would do any of these is outside `P-1` and goes to the Principal |
| **Both research paths** | A Hypothesis is admissible under `P-1` when its `motivated_by` set contains either an **active Theme** within the proposer's Research Authorization, or a **`SearchFamily` within the Authorization's declared empirical or discovery scope** with no Theme (PD-003.5's empirical path). Neither path is privileged |
| **Conditions, all required at Apply** | (a) An independent Check record with result `PASS` under the criteria pinned at the Transition's base (PD-007.1); (b) the funding Authorization active, and the proposal's declared research budget covered by a **`RESERVATION` the proposer committed before the Check** (PD-008), named in the proposal, open at Apply, below any `FENCE`, of amount at least the declared budget, with purpose "pending registration" of this Transition; the already-reserved allowance is the funding, and remaining spendable budget is read for attribution only, never as a second requirement; on Apply the reservation's purpose binds to the registered Hypothesis; on rejection or stop the proposer closes it or it expires; (c) the proposer's Authorization in scope for the Theme or family; (d) the base state current, or the Transition re-checked at the new base with `PASS`; (e) no `STOP`, no pending escalation on the subject, no suspension of `P-1`; (f) the Hypothesis is not a restatement (a `NOT MET` on FR-4 is a `FAIL`, so this follows from (a)) |
| **Reserved to the Principal** | Constitutional Transitions; Authorization grant, amendment and revocation; committing a `FENCE` (the funding stop, PD-008); Evaluation Standards; Theme registration and any Theme funding outside an approved grant; every Allocation of any purpose; retirement or supersession of a Strategy Version; Hypothesis standing changes; Strategy Version registration (a candidate for a later policy `P-2`, not delegated now); every `STOP` |
| **Attribution** | The Transition's decision event records `decider = P-1 (TR-<admitting Transition>)`, the Check record's sequence, and the Apply sequence; the lifecycle reads `DECIDED (ADMITTED by policy P-1)` |
| **Revocation and suspension** | The Principal suspends or revokes `P-1`, for all classes or for a named Authorization, by a Transition; from its Apply the affected classes revert to the Principal; Transitions already applied under `P-1` stand (I-11). A revocation reaches Apply like any Transition; nothing is retroactive |
| **Ambiguity** | Any condition that cannot be determined from the ledgers, any Check `STOP`, any identity, meaning or authority question the policy text does not settle: the Transition is `STOPPED` and goes to the Principal. `P-1` interprets nothing |
| **Policy evidence before delegation** | For `P-1` at first admission: none beyond the Check contract (Principal's direction). For any later policy: a record of Principal decisions agreeing with Checks on the class, stated in the proposing Transition |

### Constitutional Delta of D-11

```text
ΔO: NONE. A policy is Constitution text and a decision attribution.
ΔS: Part V "admitted policy" filled for two classes; decision event
    attribution; suspension and revocation; the empirical-path
    admissibility rule.
ΔA: The decision right for Hypothesis registration within an
    authorized scope, and for successor Agent Design registration
    without authority expansion, moves from the Principal to policy P-1
    for every instance meeting P-1's conditions, revocably. Neither
    right can widen a budget, cap, scope, expiry or Authorization. No
    other right moves. The Checker gains no decision right: P-1 decides
    on a PASS; the Checker records one.
```

---

## PD-007.3. D-12 — moved to PD-008

Revision 1 proposed reservation by derivation over undecided proposals.
The Principal rejected it: a derived view of pending proposals is not an
atomic reservation, and a record written after execution cannot prevent
money already spent. The contract is now
[PD-008](principal_decision_008_research_budget_reservation.md): a
`RESERVATION` Research Record admitted exclusively by the Evidence
commit boundary against the grant at its sequence, `PENDING` attempts
before consumption, settlement, expiry by the clock, release, and
revocation at Apply. What this record keeps: `P-1`'s condition (b)
reads that reservation; the Check record's budget line cites it by
sequence; the per-grantee cap is Authorization content as PD-008 says.

### Dependencies on PD-008

| PD-007 item | Depends on PD-008 for |
| --- | --- |
| `P-1` condition (b) | The reservation's existence, openness and purpose binding |
| Check record item 4, "within the proposer's Authorization and budget" | Reading available and the cited reservation instead of a derived remainder |
| PD-007.4 example, days 1 and 2 | Reservations and refusals as PD-008 defines them |
| Escalation on `OVERSPENT` | An Authorization `OVERSPENT` under PD-008 rule 7 makes every proposal under it `STOP` until the Principal acts |

---

## PD-007.4. Ten agents, one Authorization: the rules together

Illustrative. `AU-40` grants 600 units to ten Agent Design Versions
`AD-21.1` to `AD-30.1` with a cap of 100 per lineage, Themes `TH-14`
and `TH-15`, and an empirical scope for family `SF-9`. Checker `CK-A3`
(`CHECKER` lineage `AD-40`, Authorization `AU-41`, provider different
from the proposers' by `AU-41`'s content). `P-1` admitted at `N=80`.

| Event | What happens | Rule |
| --- | --- | --- |
| Day 1: eight agents each commit a `RESERVATION` of 40, then `PENDING` attempts and settlements for backtest Research Records (Historical Reconstruction, dataset `DS-7@hash`, cutoff 2026-06-30, backtester `bt-2.3@hash`, reproducibility binding) | 320 reserved and settled; `AD-23.1`'s third reservation would take its lineage to 120: refused `CAP_EXCEEDED`, preserved | PD-008 rules 1, 2 |
| Day 2: `AD-21.1` commits `RESERVATION` 20 for "pending registration `HY-301`" under `TH-14`; `AD-27.1` commits `RESERVATION` 20 for "pending registration `HY-302`" in `SF-9`; both propose at base 84 naming their reservations | Available 600 − 320 − 40 = 240; each proposal's budget covered by a committed reservation | PD-008 rule 1; `P-1` (b) |
| `CK-A3` checks `HY-301`: criteria pinned at 84; closure read; FR-4 `MET`; `authored knowing the period` recorded for the two cited backtests; `PASS`. Checks `HY-302`: the family's trials reconciled against consumption; `PASS` | Two Check records appended | D-10 |
| Apply `HY-301` at 84 → 85 under `P-1`: conditions (a) to (f) hold; `decider = P-1 (TR-610)`. Apply `HY-302`: base 84 stale; re-checked at 85; `PASS`; 85 → 86 | Two registrations without a Principal act, each attributed | D-11 |
| Day 3: `AD-24.1` proposes `HY-303` restating `HY-299` (rejected on reconstruction last week) without a declared difference | `CK-A3`: FR-4 `NOT MET`; `FAIL`; `P-1` decides nothing | D-10, D-11 |
| Day 4: `AD-25.1` proposes `HY-304` whose resolution source `SRC-Q` is under no Observation Authorization at base | `CK-A3`: the criterion needs an authority the Constitution does not supply for this source: `NOT DETERMINABLE`; `STOP`; to the Principal, who may grant a successor Observation Authorization | D-10, I-14 |
| Day 5: `AD-28.1` proposes a successor `AD-28.2` requesting no Authorization; `CK-A3` (not in lineage `AD-28`) `PASS`; applied under `P-1`; `AD-28.2` can do nothing until the Principal grants `AU-4x` | Membership delegated; authority not | D-11 |
| Day 6: `AD-22.1` proposes `TR-620`, Allocation of purpose `EXPLORATORY` to `SV-41.1` | Reserved to the Principal; `P-1` is not named for it; the Transition waits for the Principal | D-11 reservation list |
| Day 7: the Principal suspends `P-1` for `AU-40` by `TR-625` after `CK-A3`'s verification yield shows two passed registrations later found non-conforming | From 91 onward, `AU-40`'s registrations revert to the Principal; `HY-301` and `HY-302` stand | D-11 revocation; I-11 |

---

## PD-007.5. Admission brief

**What an agent may do without asking the Principal each time.** Under
its Research Authorization and within its grant: reserve research
budget, pre-record attempts, run and settle research, commit Research
Records of every kind including `SELECTION`, `EXPERIMENT DESIGN` and
screens, commit Predictions and Evaluations; and, under policy `P-1`,
have two kinds of proposal admitted on an independent `PASS` with no
per-instance Principal act: a Hypothesis registration within its scope
(under an active Theme or in an authorized empirical family), and a
successor Agent Design registration that requests no Authorization. It
may also propose anything else; those proposals wait for the Principal.

**What independent Check remains required.** Every consequential
Transition, delegated or not: a Check record in the PD-007.1 form by a
Checker under a Checker Authorization outside the proposer's lineage,
under the criteria pinned at the Transition's base, reading only
committed records, with the budget line above, the restatement finding,
the "authored knowing the period" finding and, where an Evaluation is
cited, the `ES-1.0` conformance items. `P-1` decides nothing without a
`PASS`, nothing on a `STOP`, and nothing it is not named for.

**What remains exclusively the Principal's decision.** Constitutional
Transitions and Evaluation Standards; every Authorization grant,
amendment and revocation; committing a `FENCE`; Theme registration and
any Theme funding outside an approved grant; every Allocation of any
purpose; retirement or supersession of a Strategy Version; Hypothesis
standing changes; Strategy Version registration (candidate `P-2`,
later); every `STOP`; every `DISPUTED` reproduction; suspension or
revocation of `P-1` itself.

**Exact proposed delta.**

```text
ΔO: NONE. A policy is Constitution text and a decision attribution; the
    Check record is a Transition lifecycle event already provided for.
ΔS: §III.8 Independence: the three conditions (separate authority,
    protected standards, evidence the proposer cannot rewrite) replace
    the TENTATIVE definition; provider as provenance and an
    Authorization option. §III.8 and Part V: the Check record form as
    the only carrier of a Check; FAIL versus STOP; the budget line.
    §III.5 and Part V: the Checker's duty to commit expected-but-missing
    Outcomes before a citing Check; reproduction of every grounding
    Decision before PASS. Part V "admitted policy": P-1 for the two
    classes, its six conditions, attribution, suspension, revocation,
    the empirical-path admissibility rule, the reservation list.
ΔA: +1 admitted policy. The decision right for Hypothesis registration
    within an authorized scope, and for successor Agent Design
    registration without authority expansion, moves from the Principal
    to policy P-1 for every instance meeting its conditions, revocably.
    Neither right can widen a budget, cap, scope, expiry, Authorization
    or reservation. No other right moves; the Checker gains none; the
    Outcome committer is unchanged.
```

**One permitted example.** `AD-27.1`, under `AU-40` with empirical
scope `SF-9`, commits `RESERVATION` 20 (purpose "pending registration
`HY-302`"), then proposes `HY-302` at base 84, `motivated_by` {`SF-9`
trials}, no Theme. `CK-A3` (lineage `AD-40`, `CHECKER` class, `AU-41`)
checks at base 84: testability met; resolution sources active at base;
motivation closure disjoint from the resolution set; family reconciled
against consumption; not a restatement; budget line: the reservation is
open, below any fence, amount 20 ≥ declared 20, purpose matches;
remaining spendable 240 recorded. `PASS`. At Apply the base has moved
to 85; re-checked at 85, `PASS`; applied 85 → 86 with
`decider = P-1 (TR-610)`. The Principal did not act.

**One refused example.** `AD-24.1`, under the same `AU-40`, proposes
`HY-303` restating `HY-299` (rejected on reconstruction a week earlier)
without a declared difference, citing a reservation of amount 10 against
a declared budget of 15. `CK-A3`: restatement `NOT MET` (FR-4); budget
line `NOT MET` (reservation amount below the declared budget). `FAIL`,
preserved. `P-1` decides nothing. Had the budget line instead been
`NOT DETERMINABLE` because `AU-40` were `OVERSPENT` or fenced, the
result would be `STOP` and the question the Principal's.

## PD-007.6. Genesis choices that follow admission (plan step 4, with D-17)

No machinery is drafted here; these are the choices the genesis record
must make, in order, once PD-007 is admitted.

1. **Sequence 0.** The Constitutional Transition admitting
   `ConstitutionVersion 1`, proposed and decided by the Principal, with
   the Checker requirement waived by an exception in the version itself
   applicable only to sequence 0 (PD-002.3). Choice: whether the
   exception is a sentence in Part V or a clause of the admission text.
2. **The first Checker Authorization**, before any other, so that every
   later Transition can be checked: its grantee (a human, or a `CHECKER`
   lineage registered at sequence 0's text), its provenance rule, and
   whether it may reproduce and commit Outcomes.
3. **The first Observation Authorization**: Source Declarations, feed
   sources with enumeration contracts, the hop rule, the plan of slots,
   and the synthetic source for Proof 2.
4. **The first Research Authorizations**: grant in units, estimation
   rule and tier per provider, per-grantee cap, default reservation
   expiry, Themes and the empirical and discovery scopes, method class
   of each grantee; and the Agent Design registrations of the ten
   agents they bind to.
5. **`P-1`'s admitting Transition**, after the Checker and Research
   Authorizations exist, naming the Authorizations it applies to.
6. **Limits**: the exploratory pool, caps and portfolio limits, even if
   the first demonstrations allocate nothing.
7. **D-17, death between Decide and Apply.** Choice: a decided,
   unapplied Transition found on restart is applied if its base is still
   the head and re-checked otherwise (continuation), or is re-decided in
   every case. PD-007 narrows the window for delegated classes, where
   the decision is an Apply-time act, but the Principal-decided classes
   need the rule.
8. **The paper fill rule and `ES-1.0`'s method commitments** for the
   first registrations, so that no registration is checked without
   them.

Each is a Principal act with a record; none requires a new object, kind
or right beyond those already admitted or proposed.

## PD-007.7. Decisions for the Principal

| Question | Proposal |
| --- | --- |
| Admit the three-condition definition of independence, with provider as provenance and an Authorization option | Yes |
| Admit the Check record form as the only carrier of a Check | Yes |
| Outcome committer stays open to any authorized party, with the Checker's duty to commit expected-but-missing Outcomes before a citing Check | Yes; closes U-10 without a new function |
| Admit `P-1` for Hypothesis registration (both paths) and Authorization-free successor Agent Design registration, with the reservation list as stated, and the rule that neither delegated right can widen a budget or Authorization | Yes |
| Strategy Version registration: reserved now, candidate `P-2` later | Reserve |
| D-12 | Decided in PD-008; this record depends on it |
| Checker extraction (UD-4) | Defer |

## Amended by PD-010 (admitted 2026-10-19; Constitution revision 11)

This record is historical and is not rewritten. The following of its content is superseded or supplemented by [PD-010](principal_decision_010_codex_audit_repairs.md) as admitted; the Constitution's text governs.

- `P-1` condition (b): "open at Apply, below any `FENCE`" is replaced by the Apply binding: eligibility is established at `BIND` and the Apply cites a binding that is not invalidated (audit B-4).
- The Check record's item 3 gains `F = N/A — no Paper Book` and `LEDGER_UNREACHABLE`; item 4 distinguishes a Principal control act (authority cited directly; budget line `N/A — no metered consumption`) from a proposal declaring metered consumption (audit B-2).
- In the §PD-007.4 example, the Day 4 case (`SRC-Q` under no Observation Authorization at base) is a known failed gate: `NOT MET` and `FAIL`, not `NOT DETERMINABLE` and `STOP`; `STOP` is reserved for constitutional indeterminacy, and a Principal-only decision requirement is not a missing ontology (C-4). Likewise an `OVERSPENT` or fenced Authorization is `NOT MET`.
- A `CHECKER` lineage proposes nothing but its own successor and, as any agent may, a Constitutional Transition `STOPPED` until the Principal decides (C-4). A Checker Authorization may name subjects its holder may not check, as Authorization content (C-7).
