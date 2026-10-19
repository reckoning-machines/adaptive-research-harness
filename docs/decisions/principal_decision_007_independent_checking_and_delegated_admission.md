# Principal Decision Record 007 — Independent Checking, Bounded Autonomous Admission, Concurrent Budgets

Status: **PROPOSED FOR ADMISSION. Not admitted.** Depends on PD-001 to
PD-004 (admitted, Constitution revision 5) and on PD-005 (`ES-1`,
proposed) for the Check content it names. Carries a declared `ΔA`:
the first admitted policy. Changes no Constitution text until admitted.

Date: 2026-10-19

Subjects: D-10 (sufficiency of Checker independence; carries U-10
Outcome committer, UD-4 Checker extraction, FR-4 Check contract); D-11
(the Principal bottleneck; the empty "admitted policy" slot of Part V);
D-12 (research budget reservation and concurrent consumption).

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
   Authorization and budget; base state current at the time of Check.
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
| **Classes delegated** | (i) **Hypothesis registration**; (ii) **successor Agent Design Version registration** that requests no Authorization (membership only; the successor can do nothing until the Principal grants one) |
| **Both research paths** | A Hypothesis is admissible under `P-1` when its `motivated_by` set contains either an **active Theme** within the proposer's Research Authorization, or a **`SearchFamily` within the Authorization's declared empirical or discovery scope** with no Theme (PD-003.5's empirical path). Neither path is privileged |
| **Conditions, all required at Apply** | (a) An independent Check record with result `PASS` under the criteria pinned at the Transition's base (PD-007.1); (b) the funding Authorization active, with remaining budget (grant minus consumed minus reserved, PD-007.3) not less than the declared budget; (c) the proposer's Authorization in scope for the Theme or family; (d) the base state current, or the Transition re-checked at the new base with `PASS`; (e) no `STOP`, no pending escalation on the subject, no suspension of `P-1`; (f) the Hypothesis is not a restatement (a `NOT MET` on FR-4 is a `FAIL`, so this follows from (a)) |
| **Reserved to the Principal** | Constitutional Transitions; Authorization grant, amendment and revocation; Evaluation Standards; Theme registration and any Theme funding outside an approved grant; every Allocation of any purpose; retirement or supersession of a Strategy Version; Hypothesis standing changes; Strategy Version registration (a candidate for a later policy `P-2`, not delegated now); every `STOP` |
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
ΔA: The decision right for Hypothesis registration and for
    Authorization-free successor Agent Design registration moves from
    the Principal to policy P-1 for every instance meeting P-1's
    conditions, revocably. No other right moves. The Checker gains no
    decision right: P-1 decides on a PASS; the Checker records one.
```

---

## PD-007.3. D-12 — Concurrent research budgets: the smallest rule

Ten agents under one Authorization can overspend it in two ways:
committing Research Records that together exceed the grant, and
proposing Transitions whose declared budgets together exceed what
remains. Three rules, no queue:

1. **Refusal at the ceiling, by sequence.** The Evidence commit boundary
   refuses a Research Record whose consumption would take the
   Authorization's consumed total, at the head at commit, above the
   grant; the refusal is preserved with the record. Consumption is
   serialized by Evidence sequence, which the boundary already assigns
   (I-8), so two agents cannot both succeed past the ceiling.
2. **Reservation by derivation.** The declared research budget of a
   proposed, undecided Transition is a **reservation**, `DERIVED` over
   the Transition ledger: remaining budget = grant − consumed
   (Research Records) − reserved (declared budgets of proposed
   Transitions not yet decided or refused). The Check and `P-1`'s
   condition (b) read remaining budget with reservations; Apply
   re-reads it. A reservation ends at Decide (consumed on Apply as
   capital and allocation budgets already are; released on reject,
   stop or refusal). No reservation record exists; nothing new is
   written.
3. **Per-grantee cap.** A Research Authorization may declare a cap per
   grantee lineage within the grant; the commit boundary applies rule 1
   against the cap as well as the grant. Content of the Authorization,
   set by the Principal.

Dependencies: D-11 (condition (b) reads rule 2); genesis (the first
Authorizations carry the grants and caps); plan step 4's remaining
items (D-17, which is unaffected). `ΔO` none; `ΔS` the Evidence commit
boundary's refusal rule, the derived reservation, the optional cap;
`ΔA` none, since refusal at a boundary is the existing invariant.

---

## PD-007.4. Ten agents, one Authorization: the rules together

Illustrative. `AU-40` grants 600 units to ten Agent Design Versions
`AD-21.1` to `AD-30.1` with a cap of 100 per lineage, Themes `TH-14`
and `TH-15`, and an empirical scope for family `SF-9`. Checker `CK-A3`
(`CHECKER` lineage `AD-40`, Authorization `AU-41`, provider different
from the proposers' by `AU-41`'s content). `P-1` admitted at `N=80`.

| Event | What happens | Rule |
| --- | --- | --- |
| Day 1: eight agents commit backtest Research Records (Historical Reconstruction, dataset `DS-7@hash`, cutoff 2026-06-30, backtester `bt-2.3@hash`, reproducibility binding) consuming 40 units each | 320 consumed; `AD-23.1`'s third record would take its lineage to 120: refused at the ceiling, preserved | D-12 rule 1 and 3 |
| Day 2: `AD-21.1` proposes `HY-301` under `TH-14` (budget 20) and `AD-27.1` proposes `HY-302` in `SF-9` with no Theme (budget 20), both at base 84 | Reserved 40; remaining 600 − 320 − 40 = 240 | D-12 rule 2 |
| `CK-A3` checks `HY-301`: criteria pinned at 84; closure read; FR-4 `MET`; `authored knowing the period` recorded for the two cited backtests; `PASS`. Checks `HY-302`: the family's trials reconciled against consumption; `PASS` | Two Check records appended | D-10 |
| Apply `HY-301` at 84 → 85 under `P-1`: conditions (a) to (f) hold; `decider = P-1 (TR-610)`. Apply `HY-302`: base 84 stale; re-checked at 85; `PASS`; 85 → 86 | Two registrations without a Principal act, each attributed | D-11 |
| Day 3: `AD-24.1` proposes `HY-303` restating `HY-299` (rejected on reconstruction last week) without a declared difference | `CK-A3`: FR-4 `NOT MET`; `FAIL`; `P-1` decides nothing | D-10, D-11 |
| Day 4: `AD-25.1` proposes `HY-304` whose resolution source `SRC-Q` is under no Observation Authorization at base | `CK-A3`: the criterion needs an authority the Constitution does not supply for this source: `NOT DETERMINABLE`; `STOP`; to the Principal, who may grant a successor Observation Authorization | D-10, I-14 |
| Day 5: `AD-28.1` proposes a successor `AD-28.2` requesting no Authorization; `CK-A3` (not in lineage `AD-28`) `PASS`; applied under `P-1`; `AD-28.2` can do nothing until the Principal grants `AU-4x` | Membership delegated; authority not | D-11 |
| Day 6: `AD-22.1` proposes `TR-620`, Allocation of purpose `EXPLORATORY` to `SV-41.1` | Reserved to the Principal; `P-1` is not named for it; the Transition waits for the Principal | D-11 reservation list |
| Day 7: the Principal suspends `P-1` for `AU-40` by `TR-625` after `CK-A3`'s verification yield shows two passed registrations later found non-conforming | From 91 onward, `AU-40`'s registrations revert to the Principal; `HY-301` and `HY-302` stand | D-11 revocation; I-11 |

---

## PD-007.5. Decisions for the Principal

| Question | Proposal |
| --- | --- |
| Admit the three-condition definition of independence, with provider as provenance and an Authorization option | Yes |
| Admit the Check record form as the only carrier of a Check | Yes |
| Outcome committer stays open to any authorized party, with the Checker's duty to commit expected-but-missing Outcomes before a citing Check | Yes; closes U-10 without a new function |
| Admit `P-1` for Hypothesis registration (both paths) and Authorization-free successor Agent Design registration, with the reservation list as stated | Yes |
| Strategy Version registration: reserved now, candidate `P-2` later | Reserve |
| D-12: refusal at the ceiling by sequence; reservation by derivation; optional per-grantee cap; no queue | Yes |
| Checker extraction (UD-4) | Defer |
