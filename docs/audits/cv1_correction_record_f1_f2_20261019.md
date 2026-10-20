# Author's Correction Record — Final Independent Review Findings F-1 and F-2

Status: **AUTHOR'S RECORD — EVIDENCE, NOT DOCTRINE. Not independent.
Closes nothing on its own authority; the findings are closed only when
the independent reviewer says so.** Author: Claude, who wrote the
corrected text. Date: 2026-10-19.

Subject: findings F-1 and F-2 of the
[final independent review](cv1_final_independent_review_20261019.md)
(Codex, reviewed commit `f77fe92`, Constitution revision 11), corrected
as Constitution revision 12 in the working tree (uncommitted; no commit
is authorized for this round). All five independent audits are
unchanged. The Principal's uncommitted edits to `README.md` and
`architecture.md` are preserved untouched.

Rule applied, as the Principal directed: a correction is applied
directly only where it faithfully propagates a choice PD-010 already
admitted, with the basis recorded; anything that is a new choice is
isolated in [PD-011](../decisions/principal_decision_011_proposed_confirmations.md)
for the Principal's approval and is not adopted.

## F-1. Principal authority through the full lifecycle

### Conflicting operative clauses at revision 11

| Clause | Conflict |
| --- | --- |
| §III.8 Check record item 4 | Direct Principal authority was allowed for an enumerated list (grants, limits, Constitutional Transitions, Theme registration, Allocation) that omitted Agent Design Version registration, which Part V and PD-009 require the Principal to propose at sequences 3 to 13 |
| §III.8 Check record item 1; record form item 1 | "proposer and Authorization" with no branch for an act with none |
| §III.8 Continuation (D-17) | "for every class, the Authorization active … no expiry of the Authorization passed" with no branch for a control act, so an interrupted Principal grant could not be continued on an unchanged head |
| Part V | Permitted the Principal to propose registrations but stated no lifecycle-wide authority predicate for control acts |

### Basis for treating this as propagation

PD-010 §1 defined a **Principal control act** by actor and funding
("Who: Principal; funded by: the Principal's own authority, cited
directly; reservation purpose: none; not metered") and admitted, as
choice 2, the applicability rule that makes the Authorization and
budget tests inapplicable to it; the parenthetical list in revision 11
was an incomplete transcription of that definition. PD-009 (admitted)
requires Principal-proposed registrations with no Research
Authorization. Carrying one admitted applicability rule through Check,
Decide, Apply and continuation moves no right and creates none.

### Replacement text (revision 12)

- §III.8 record form item 1 and Check record item 1: "proposer and
  its Authorization or, for a Principal control act, the Principal's
  own authority".
- §III.8 Check record item 4: a Principal control act is "any
  Transition the Principal proposes that declares no metered research
  consumption, whatever its class"; the Principal's own authority is
  cited directly; no Authorization, reservation or binding test
  applies; the independent Check and every other criterion of the
  class apply unchanged.
- §III.8 Continuation: three branches, each stated: a delegated class
  (every `P-1` condition, no suspension); a proposal under an
  Authorization (active and unexpired at the head); a Principal control
  act (the Principal's own authority, neither granted, expired nor
  revoked, so the remaining conditions decide).
- Part V, new paragraph **Principal control acts** before "Admitted
  policy": the classes, the predicate at every lifecycle point, the
  `N/A` lines, the unchanged independent Check, the Principal as
  decider, continuation on an unchanged head, and the Checker's own
  funded verification kept separate.

### Replay of the review's counterexamples

| Case | Result under revision 12 |
| --- | --- |
| Applies 0 to 2 valid; the Principal proposes `AD-R1.0` at sequence 3 | Check: class Agent Design Version registration; proposer the Principal, authority its own, cited; Authorization and budget lines `N/A`; Checker `AD-CK-1.0` not in any proposer's lineage; provenance and method commitment present; closure `(E, 2, N/A — no Paper Book)`; `PASS`. The Principal decides. Apply 3. The Checker's reservation and attempt for the Check are on `AU-CK-A` as for any Check |
| The Checker passes the `AU-OBS-1` grant; the Principal decides; the process dies before Apply 1 with the head at 0 | Continuation: base still the head; a Principal control act, so no Authorization or funding predicate applies; no `STOP`, no suspension in play; Apply 1 proceeds citing the existing Check and decision. Nothing is re-checked or re-decided; had the head moved, re-check under C-2's rule |
| A Research Agent's registration under `P-1`, interrupted before Apply | Unchanged: the delegated branch, with its Authorization active and the Apply binding |

### Bypass and breadth check

The correction adds no proposer, decider or class. A control act still
requires the independent Check with every class criterion, the
Principal's decision, a current base and the ordinary refusals. `P-1`
is untouched: a Principal-proposed registration is decided by the
Principal, not by policy. A Checker's cost for checking a control act
is funded from the Checker's grant. The sequence-0 waiver is unchanged.
Nothing lets an agent cite the Principal's authority.

Delta of the correction: `ΔO` 0; `ΔS` the five clauses above; `ΔA` 0.

## F-2. Partial reductions with residual breaches

### Conflicting operative clauses at revision 11

| Clause | Conflict |
| --- | --- |
| Part V Allocation row, `REDUCE` criterion (iii) | Admits a residual breach that cannot be eliminated in one step |
| I-10 | Unconditionally required the resulting projection to satisfy every limit |
| §III.10 Admission rules | A Decision-set `REDUCING` order admitted only when "limits hold" |
| §III.10 Limits bullet | Refused any order "that would breach a limit in force at the head", which a sell into a persisting breach does on a literal reading |
| Part V Allocation row, criterion (iv); §III.10 Expiry bullet | Required re-execution to the lower target that the gates above could refuse |

### Basis for treating this as propagation

PD-010 choice 9, admitted, carries criteria (iii) "every limit usage is
non-increasing and no new instrument exposure is created; … admits only
the [residual breach]" and (iv) "the Execution function re-executes to
the lower target under the new key". The admitted policy therefore
already requires the Check to admit a residual breach and the Paper
Book to execute the reduction; I-10 and the two Paper Book gates were
left unconditional in propagation. The Principal's direction for this
round restates the same bound: a verified partial reduction may leave
an existing breach but cannot create or worsen risk, and the exception
never extends to opening or increasing exposure.

### Replacement text (revision 12)

- I-10: one bounded qualification: a `REDUCE` whose projection lowers
  or leaves unchanged every limit usage, creates no breach, worsens
  none and adds no instrument exposure satisfies the invariant with the
  residual breach recorded; no other class, and no Transition that
  increases any exposure, is admitted into a breaching projection.
- Part V Allocation row, criterion (i): composition legality "under
  I-10 as qualified for `REDUCE`", with the usage test stated.
- §III.10 Admission rules: a Decision-set `REDUCING` order is admitted
  when the allocation is in force and "the limit test of the Limits
  bullet below holds".
- §III.10 Limits bullet: the test is on the change the order's full
  fill makes, not on the resulting state: refused `LIMIT` when it would
  raise any usage above its limit or raise a usage already above its
  limit (new or worsened breach); admitted when it lowers or leaves
  unchanged every usage, the residual breach reported; no `OPENING`
  order into or within a breach; the Principal's limit content still
  decides whether a portfolio net limit may refuse a version-level
  reducing order that raises net usage within the limit.

### Replay of the review's counterexample

Limit 5; current exposure and target 10; the Principal proposes
`REDUCE` to 6.

| Stage | Result under revision 12 |
| --- | --- |
| Check | (i) every usage at 6 is lower than at the head, no breach appears, none worsens: `MET` under I-10 as qualified; (ii) standing unchanged, never higher; (iii) residual breach of 1 recorded, no new or worsened risk; (iv) the residual execution obligation named; the Check is independent (the Principal is the proposer and holds no lineage; the Checker acts under its own grant); `PASS` |
| Apply | Base current; the Principal decides; the projection carries the residual breach of 1 as a recorded fact; allocation 6, standing unchanged |
| Execution | Re-execution under the new key derives sell 4 (`REDUCING`). Limit test: full fill lowers the usage from 10 to 6; it raises nothing above a limit and worsens nothing: **admitted**; the residual breach of 1 is a reported Paper Book fact. Fill admitted within the reducing bound; `EFFECTIVE` at commit |
| Reduction to zero | `REDUCE` to 0: (i) to (iv) as above with no residual; sell 10 admitted; standing `INCUBATING`; the obligation is discharged by the terminal state |
| A version-level reduction that raises portfolio net usage above its limit (the short leg of a hedge) | Check (iii): a usage increases: a worsened or new risk, `NOT MET`, `FAIL`; the Principal proposes a smaller or different reduction. If it reached the Paper Book under some other allocation, the order's full fill would raise net usage above its limit: refused `LIMIT` |
| An `OPENING` order while a breach persists | Refused `LIMIT` as before; the qualification never reaches opening exposure |
| Recovery after Apply, before any order | A fresh process derives the obligation from allocation 6 versus confirmed position 10; sell 4 admitted on the same test; a stale-base Transition is refused as always |

### Bypass and breadth check

The qualification is bounded to `REDUCE`, to usages that fall or stay
flat, and to breaches that already existed; it admits no opening or
increase, it changes no standing, it keeps the Principal as sole
proposer and decider, the independent Check, the stale-base refusal,
the reducing bound at fill admission and every expiry obligation. U-8
(limits moving between witnesses) is untouched: the test is at the
pre-witness as before. A portfolio net limit's power to refuse a
version-level reducing order within the limit remains the Principal's
limit content.

Delta of the correction: `ΔO` 0; `ΔS` the four clauses above; `ΔA` 0.

## Also corrected in this round

| Item | Treatment |
| --- | --- |
| T-H illustration (review §7, nonblocking) | The reversal in name Q now derives the to-zero leg only; the beyond-zero leg is derived at zero and then refused `QUOTA_EXHAUSTED`. Propagation of B-8. The earlier propagation check's claim that T-H had been updated was wrong and is left standing as historical evidence; this record is the correction |
| Binding interval value for `AU-RP-1` (review §6) | The PD-009 amendment note no longer states a one-day value as if admitted; the value is proposed grant content for genesis, PD-011 A-2 |
| Prediction witness read scope (review §6) | Narrowed to `HypothesisId`, PD-010's exact wording, by the Principal's A-1 direction; the broader alternative is marked superseded in PD-011 |

## F-2, second pass: the execution exception gated on an applied `REDUCE`

The [bounded follow-up](cv1_revision12_bounded_followup_20261019.md)
closed F-1's cases and found the first-pass Limits bullet overbroad: it
admitted any usage-lowering order into a persisting breach, with no
requirement that the order execute a checked, Principal-decided
`REDUCE`. Also removed, as the follow-up asked: the unsupported
"Strategy Version registration" example from Part V's control-act list
(Part V's row names only a Research Agent as proposer).

### Conflicting clause and replacement

| Clause | First pass (overbroad) | Second pass |
| --- | --- | --- |
| §III.10 Limits bullet | Any order whose full fill lowers or leaves unchanged every usage admitted despite a persisting breach | The ordinary rule restated (an order whose full fill would breach a limit, a persisting breach included, is refused `LIMIT`); one exception, the **`REDUCE` execution exception**, available only when at the pre-witness (a) the order's set is keyed to an applied Allocation Transition of purpose `REDUCE` in force at `N_1`, (b) that `REDUCE`'s obligation is outstanding and the order executes toward its target and not past it, (c) the order is `REDUCING`, and (d) the full fill lowers or holds every usage and raises none above its limit. Decision sets under an unchanged allocation and expiry sets cannot claim it; no `OPENING` order into or within a breach under either rule |
| §III.10 Admission rules | Decision-set `REDUCING` orders referred to the limit test generally | Referred to the Limits bullet with the exception available only to a set keyed to an applied `REDUCE` |

The attribution uses the existing set key `TransitionId:StateVersion:…`,
which names the applied Allocation Transition; no new object or
linkage is created. Basis: PD-010 choice 9, criteria (iii) and (iv),
whose admitted scope is the `REDUCE` Allocation and its re-execution,
and the Principal's direction of 2026-10-19.

**The exact changed predicate**, at the Paper Book admission boundary:

```text
admit despite a persisting breach  iff
  set.TransitionId is an applied Allocation of purpose REDUCE in force at N_1
  ∧ obligation(REDUCE) outstanding ∧ |pos_after_full_fill − target| < |pos_confirmed − target|
    ∧ full fill does not pass the target
  ∧ order.class = REDUCING
  ∧ ∀ limit L: usage_L(after full fill) ≤ usage_L(head) ∧ ¬(usage_L(after) > L ∧ usage_L(after) > usage_L(head))
otherwise the ordinary rule: refuse LIMIT if the full fill would leave any limit breached.
```

### Replays

| Case | Sequence | Result |
| --- | --- | --- |
| Checked, Principal-decided, applied `REDUCE` 10 → 6 against limit 5 | Check (i) to (iv) `PASS`; the Principal decides; Apply at `N` records target 6, standing unchanged. The Execution function re-executes under key `TR-R:N:<seq>`, deriving sell 4 `REDUCING`. At the pre-witness: the set's Transition is the applied `REDUCE`, in force at `N`; obligation outstanding (confirmed 10, target 6); full fill leaves 6, toward and not past the target; usage 10 → 6, nothing raised above a limit | **Admitted.** Residual breach of 1 reported. Fill admitted within the reducing bound, `EFFECTIVE` at commit |
| Partial fill and restart | Sell 4 fills 2 (position 8); the process dies. A fresh process reads allocation 6 versus confirmed 8: obligation outstanding; it appends a `REPLACE` for the remainder 2 under the same key. Pre-witness: same `REDUCE`, obligation outstanding, full fill leaves 6, usage 8 → 6 | **Admitted** on the same predicate; a duplicate order under the same `OrderId` refused `DUPLICATE`. At position 6 the obligation is discharged and no further order is derived under the key; an order that would take the position below 6 fails (b) and falls to the ordinary rule, refused `LIMIT` while the breach persists |
| Ordinary Strategy Decision targeting 6 under an unchanged `QUALIFIED` allocation, no `REDUCE` | Decision set keyed `TR-Q:N:<DecisionSeq>`; sell 4 `REDUCING` derived. At the pre-witness the set's Transition is a `QUALIFIED` Allocation, not a `REDUCE`: condition (a) fails; the ordinary rule applies; the full fill leaves exposure 6 against limit 5, a persisting breach | **Refused `LIMIT`**, preserved. Exposure stays 10 and the breach is a reported fact; Part X R-8 requires `Reduce`, which is the Principal's `REDUCE` act. A restart derives the same order and meets the same refusal |
| Expiry set under an `EXPLORATORY` allocation while a breach persists | Set keyed `TR-E:N:EXPIRY`; the Transition is not a `REDUCE` | The exception is unavailable; the ordinary rule decides; the obligation stays outstanding and reported; the route is a `REDUCE` to zero by the Principal, whose own re-execution carries the residual |
| `OPENING` order of any set while a breach persists | Condition (c) fails | Refused `LIMIT` under either rule |

### Bypass and breadth check

The exception is reachable only through a set keyed to an applied
`REDUCE`, which exists only after an independent Check and the
Principal's decision; it admits only `REDUCING` orders toward that
`REDUCE`'s target; it never admits an opening or increase; it leaves
the ordinary rule in force for every other set; U-8, the reducing
bound, provisional-fill accounting and expiry obligations are
unchanged. `ΔO` 0; `ΔS` the two clauses; `ΔA` 0.

## What this record does not establish

That F-1 and F-2 are closed. That is the independent reviewer's
finding to make on the follow-up handoff. Nothing here is committed,
admitted, certified or executed.

## Digests of the corrected working tree (second pass)

| File | SHA-256 |
| --- | --- |
| `docs/doctrines/new_speedway_constitution.md` | `c56a9cf50a7e9efadad8f2f2be6605e82c758f18d4096ba07eaaf86a8f8b7a64` |
| `docs/decisions/principal_decision_011_proposed_confirmations.md` | `0c792df4b8b5a63c88302da5215c4ee32e1ceaa9e5a0b4aacffd92603f19f686` |
| `docs/audits/cv1_followup_handoff_20261019.md` | `68bdb5c3594bb0fcc02eb0cb400ee1cd127b8b73e82d51e3a580d8ae27d4d6a6` |
| `README.md` | `67985fc5cc06e9eac6d8a2eb78d2be20a9b33331f6acdeb136fe1e6f7063826e` |
| `architecture.md` | `11d9d87a24839794e1d7811853dcf33d789864c087df45e5db475694b6761c79` |
| `docs/package/cv1_review_package_manifest.md` | `44fb711255f27dd09f25abd2d0d6bbf1690faaaa7b1b22f67fa7cb3411a03796` |

No commit; the digests identify the working tree the handoff names.
