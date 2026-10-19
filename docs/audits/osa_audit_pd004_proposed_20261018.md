# OSA Audit of PD-004 as Proposed (revision 3)

Status: **AUDIT — EVIDENCE, NOT DOCTRINE. Authorizes nothing. Certifies
nothing.**

As-of: 2026-10-19. Subject:
[PD-004, proposed, revision 3](../decisions/principal_decision_004_exploratory_capital_standings.md).
Revision 1 of this audit (2026-10-18) found record revision 1 bounded
with one declared `ΔA`. Revision 2 (2026-10-19) audited the replacement
of the deadline event by a clock read at admission. Revision 3 audits the
answer to the Principal's final challenge: that authority and time may
change between an admission read and the Paper Book commit.

Reconciliation standard: ANF and the seven authority invariants;
CPOC's canonical lifecycle and five negative invariants (fin123-core
`8175d504`); the Evidence clock as the sole time authority (Constitution
§III.5); PD-002's order-set and witness-mark rules (§III.10, §III.5,
I-13, I-15); the Principal's three principles and four required
invariants of 2026-10-19.

## Executive disposition

**B+ — BOUNDED. One declared `ΔO` (the fill confirmation record) and two
declared `ΔA`, all explicit; no contradiction with revision 4; every
residual stated with its owner. Recommended for the Principal's decision
on its own terms.** Seven defects found across revisions 2 and 3 were
repaired inside PD-004's scope (R-1 to R-7). Nothing outside the scope
was touched.

## 1. The Principal's final challenge, answered

| Required invariant | How revision 3 meets it | Where |
| --- | --- | --- |
| Opening authority, time, limits and allocation currentness valid at the logical admission point, not merely at an earlier read | The bracketing contract: a condition holds at a commit when it holds at a read before and a read after; sound because the clock advances and the Applied History is append-only, so "not yet `T`" and "`A` in force" are monotone. Limits are not monotone and are checked at the pre-witness; U-8 stays open and is not claimed | §PD-004.2 bracketing, items 3 and 5 |
| Opening fills independently satisfy current allocation authority and expiry conditions | A fill of an `OPENING` order is `PROVISIONAL` at commit and `EFFECTIVE` only on a confirmation read that shows `A` in force and `t < T`; otherwise `UNESTABLISHED`, terminal, counted for nothing. The order's validity is a precondition, never a substitute | §PD-004.4 fill and confirmation rows; cases 10 to 12 |
| The expiry obligation persists through cancellation, partial flattening and recovery until the terminal state | Obligation redefined as a predicate on the terminal state (no open orders, no `PROVISIONAL` fills, positions zero under `FLATTEN`); the expiry set is open-ended and its existence discharges nothing | §PD-004.5; case 4 |
| Reducing orders admissible without a clock only against verified positions, allocation authority and risk constraints; no reversal or new exposure as reduction | `REDUCING` orders and fills need a pre-witness of the Applied History and Paper Book heads: `A` in force, limits, positions from `EFFECTIVE` fills, and the same-side working position, which judges a sell against the worst case that every open sell fills and no open buy does | §PD-004.3, §PD-004.4 |
| Smallest serialization or authority contract, no implementation mechanism | Per-ledger total order by sequence (already in I-8) plus pre- and post-witness reads recorded on Paper Book records; no lock, transaction, queue or scheduler named | §PD-004.2 |
| If not expressible in the current model, declare the exact missing transition and the delta | The missing transition is the post-witness: a commit that records a read taken after another commit. Declared as `ΔO` +1 Paper Book record kind (fill confirmation) | §PD-004.10 |
| Do not assume checks and commits are instantaneous | Stated in E-5 and §PD-004.4; the straddle cases are traced rather than assumed away | Cases 10 to 12 |

### The three test cases

| Case | Trace | Result |
| --- | --- | --- |
| 1. Read before expiry, commit after | Order: pre-witness `t_1 < T`, commit after `T`. The order is open; its fills are gated by their own brackets; the expiry set cancels it. Fill: pre-witness `t_1 < T`, commit after `T`, confirmation `t_2 ≥ T` → `UNESTABLISHED`. Fill: pre-witness and commit before `T`, confirmation after `T` → also `UNESTABLISHED`, because the bracket cannot distinguish the two from durable authority | No exposure after `T` counts. A lawful paper fill may be discarded; stated as the accepted cost (§PD-004.8) |
| 2. Opening order admitted under `A`; successor revokes `A` before the opening fill commits; order not cancelled | Fill pre-witness at `N_1 + 1` → refused `ALLOCATION_NOT_IN_FORCE`. Or fill `PROVISIONAL` at `N_1`, confirmation at `N_1 + 1` → `UNESTABLISHED`. The order is cancelled by the first set under the successor | No exposure under a revoked allocation; the fill is judged on its own bracket, not the order's |
| 3. Cancels committed, death before flattening, restart with the expiry set present | Terminal state not established (positions nonzero) → obligation outstanding; the fresh process confirms any `PROVISIONAL` fill, then appends `REDUCING` orders to the existing set; a duplicate cancel is refused `ORDER_CLOSED`; a second set is refused `DUPLICATE` | The obligation survived the cancels and the death because nothing but the terminal state discharges it |

## 2. Findings

| Ref | Mode | Finding | Disposition |
| --- | --- | --- | --- |
| P4-1 | Time authority | Does the admission read, or the confirmation read, create a second clock? | NO. One clock; two boundaries read it. The confirmation records what the clock answered after a commit the Paper Book itself ordered; the Paper Book keeps no clock. `ΔA` (2) declares the read right regardless |
| P4-2 | Time authority | Can a Paper Book commit be placed in time at all without a second clock? | Only as an interval between two reads; the record says so and builds on it rather than against it. This mirrors the doctrine's treatment of availability (§III.5: an interval, never a single time) |
| P4-3 | Absence | Does any rule admit on the absence of a record? | NO. Every opening admission and every confirmation is a positive read; the obligation is a positive predicate; the only absence consulted is the absence of a duplicate key, an idempotency question |
| P4-4 | Trigger independence | Expiry with the Runner, the Observation function, or both dead | YES: the obligation reads neither (cases 1, 2, 8) |
| P4-5 | Trigger independence | Expiry witnessed with the Execution function dead | Not durably; nothing can open or become effective meanwhile (cases 3, 12) |
| P4-6 | Semantics | Opening exposure and reversal | CLOSED: per instrument, away from or through zero, on the same-side working position (R-7); single crossing orders refused; the beyond-zero leg judged from zero |
| P4-7 | Semantics | Can exposure arise after `T` or under a revoked allocation through a fill? | CLOSED (R-3, revision 3): a fill is `EFFECTIVE` only when bracketed; a straddling fill is `UNESTABLISHED` |
| P4-8 | Semantics | Multiple versions in one instrument | Per version for expiry, quota and class; portfolio for limits; whether net limits may refuse a version-level `REDUCING` order is limit content the Principal sets |
| P4-9 | Authority | Hidden authority in the Execution function's expiry duty? | DECLARED as `ΔA` (1) |
| P4-10 | Authority | Hidden authority in the Paper Book boundary's reads? | DECLARED as `ΔA` (2) |
| P4-11 | Authority | Is the confirmation a hidden second commit boundary or a boundary originating records? | NO. It is a Paper Book record committed by the Paper Book boundary on the Execution function's call, about a Paper Book commit; the Execution function remains the only caller; the Evidence boundary originates nothing. It is declared as `ΔO` because it is a new record kind |
| P4-12 | Authority | Free `CANCEL` during outages? | REJECTED; cancels belong only to a superseding set, the first set under a newer allocation, or the expiry set |
| P4-13 | Duplicate authority | "Expired", the projection, the expiry set, the obligation, the standing Transition | One owner each; "expired", the obligation, the terminal state and fill standing are `DERIVED`; allocation changes only at Apply |
| P4-14 | Resurrection | Restart after a superseding allocation | Old-key `REPLACE` refused; position re-targeted only under the new key (cases 9, 11) |
| P4-15 | Resurrection | Second expiry set; restart making a `PROVISIONAL` fill `EFFECTIVE` from memory | Both refused by construction: one set per `TransitionId`; standing decided only by a fresh read (case 12) |
| P4-16 | Evidence preservation | Refusals, cancels, late fills, unestablished fills, incomplete flatten | All Paper Book facts under the label with reasons; the non-conformance rule keeps every one out of grounding |
| P4-17 | Fail-closed | Admitted without a clock read | `REDUCING` orders and fills against verified heads; lawful `CANCEL`s. Nothing opens; no opening fill becomes effective; no expiry set; `PROVISIONAL` fills stay provisional and freeze their instrument |
| P4-18 | Fail-closed | Admitted with the Applied History unreachable | Nothing; with the Paper Book unreachable, nothing written |
| P4-19 | Quota | Index derivation | By rank among the version's Decisions, including `DECLINED` and `FAILED`, with closure `N` at or above the Apply |
| P4-20 | Uniformity | Read required without an expiry? | For every `OPENING` order and fill; the witness and bracket always exist |
| P4-21 | Liveness | Can a `PROVISIONAL` fill freeze an instrument indefinitely? | Only while the clock or Applied History is unreachable; one read resolves it; the freeze is fail-closed and visible. A frozen instrument under an expired allocation is still an outstanding obligation and is resolved by the same read |
| P4-22 | Scope | Theme, Hypothesis, Strategy identity, research evidence, discovery and formation rules | Untouched; Decisions and the decision-implied record unaffected by standing |
| P4-23 | Scope | Numbers in the Constitution | None; parameters listed in §PD-004.11 |
| P4-24 | Two cases | Momentum and forward under one rule set | Momentum now exercises an `EFFECTIVE` and an `UNESTABLISHED` fill at the expiry edge, quota, split, Runner death, duplicate recovery; forward exercises expiry with no Decisions, Observation death and a residual from an incomplete flatten. No rule serves one case only; no sequence collides with T-A to T-G or the forward audit's timeline |
| P4-25 | fin123-core §5, §9, §11 | Decisions fixed at commitment; classes never merged; exploratory never a grounding series | Unchanged by PD-004 |

## 3. Repairs made across revisions 2 and 3

| Ref | Defect | Repair |
| --- | --- | --- |
| R-1 | Witness-bounding claim assumed every Evidence record carries a time | Bounded by timed records; precision stated as their density |
| R-2 | Intent class judged on fills alone misclassified a split reversal's second leg | Judged on the working position; superseded by R-7 |
| R-3 | A pre-expiry `OPENING` order could fill after `T` while the Execution function was dead | Revision 2: fill admission gated by a read. Revision 3: the fill is bracketed and `EFFECTIVE` only when both reads satisfy the conditions |
| R-4 | Cancels on supersession by a newer allocation used but not permitted | Cancel rule names the first set under a newer allocation |
| R-5 | Quota index silent on `DECLINED` and `FAILED` | They count |
| R-6 | Read required only where an expiry exists | Required for every `OPENING` order and fill |
| R-7 | Working position counted opposite-side open orders, so a sell could pass as reducing against an unfilled buy | Same-side working position: worst case for the reduction claim |

## 4. ANF check

| Invariant | Finding |
| --- | --- |
| Singular decision authority | Allocation content: Applied History. The instant: the Evidence boundary's clock. Orders, fills, confirmations, intent class, pre-witnesses, refusals, the expiry set: Paper Book. Positions, working positions, fill standing, "expired", the obligation, the terminal state, the quota index: `DERIVED` |
| Classified representation closure | Every carrier classed in §3 of the record; a read is `EPHEMERAL` until a boundary records it; the recorded time value is a `RECEIPT` of the clock's answer; the Execution function's copies are `EPHEMERAL` |
| Exclusive governed commit boundary | Unchanged: Apply, Evidence commit, Paper Book commit (orders, fills, now confirmations), each with its one caller set |
| Temporal and binding closure | Every order bound to a pre-witness; every opening fill to a pre-witness and a confirmation; sets by key to an applied Transition; expiry to an instant in applied content and reads at or after it |
| Owner-resolved consumption | Exploratory capital from the pool at Apply; quota by Decisions on the Evidence ledger |
| Legacy isolation | Not implicated |
| Constitutional failure closure | Refusals preserved with reasons: `ALLOCATION_NOT_IN_FORCE`, `CLOCK_UNAVAILABLE`, `EXPIRED`, `QUOTA_EXHAUSTED`, `LIMIT`, `REVERSAL_SPLIT_REQUIRED`, `LEDGER_UNREACHABLE`, `ORDER_CLOSED`, `NO_SET`, `NOT_YET_DUE`, `EXPIRY_SET_OPENING`, `DUPLICATE`, `PROVISIONAL_PENDING`; and the terminal standing `UNESTABLISHED` |

## 5. CPOC check (design; not executed; not certified)

| Negative invariant (fin123-core) | How PD-004 meets it |
| --- | --- |
| Transient-authority leakage | The obligation, the terminal state and fill standing are predicates over ledgers and a fresh read; no flag, timer or memory (cases 3, 4, 12) |
| Mutable-present substitution | A fill's standing is fixed by its own two reads; a later head never re-judges it; superseded allocations are refused (cases 9, 11) |
| Resurrection | One expiry set per `TransitionId`; closed orders refuse fills; `UNESTABLISHED` is terminal; a restart cannot promote a `PROVISIONAL` fill from memory |
| Cross-surface disagreement | Projection, boundary and Execution function derive from the same ledgers and the same kind of read; a surface without a read says "not established" |
| Process-local continuation | Every case continues in a fresh process from ledger coordinates; concurrent dischargers are resolved by the boundary's idempotency |

## 6. Residuals and open items, with owners

| Item | Standing | Owner |
| --- | --- | --- |
| P4-R1 Promptness of discharge during Execution-function death | Not guaranteed; exposure cannot grow after `T`; cancel and flatten wait for a live process | Principal: operating expectation in the Execution Authorization |
| P4-R2 Paper fill rule | Undefined; PD-004 needs only that fills are commits the Execution function presents | Plan step 7, with U-8 |
| P4-R3 Clock monotonicity and read provenance | Doctrine assumes one monotone clock; an implementation that substitutes a local clock is caught only where timed records straddle the read | Plan step 8 CPOC witness; implementation conformance later |
| P4-R4 Portfolio net limits versus version-level flatten | Principal's limit content | Principal, limits Transition |
| P4-R5 `UNESTABLISHED` discards a straddling fill that may in fact have been lawful | Accepted for the paper book as a measurement artifact; a live venue would need its own time authority, outside this record | Principal, on admission; live execution later |
| P4-R6 Limits at a moving head (U-8) | Not monotone; checked at the pre-witness only; PD-004 does not close it | Plan step 7 |
| UD-3 `NON-REPRODUCIBLE` versions and `EXPLORATORY` capital | Open | Principal, with U-1 |
| UD-5, UD-10 pool size, caps, lifetime cap | Limits, not text | Principal |
| UD-14 Paper Book clock | Closed by rejection if PD-004 is admitted | Principal |
| FR-12 | Closed by reference if PD-004 is admitted | Principal |
| D-17 Decide-to-Apply death; N-1 genesis | Unchanged | As registered |

## 7. Admission recommendation

PD-004 revision 3 is coherent against Constitution revision 4. It
declares one new record kind and two authority changes explicitly; uses
one clock and reads it from two boundaries; places every Paper Book
commit in time and authority as an interval rather than a point; makes
exposure effective only when its bracket proves the allocation in force
and expiry not yet passed; keeps the expiry obligation alive until the
terminal state; judges reduction against the worst case; and states what
it cannot guarantee. **Recommend the Principal admit PD-004 revision 3 as
its own record, before `ES-1`**, deciding at the same time the
`UNESTABLISHED` choice and the fail-open on reducing orders.

## 9. Final focused review before admission (2026-10-19)

Subject: PD-004 revision 3 with the internal-simulator clarification
(§PD-004.15). Question: does the clarification require authority beyond
the delta the Principal approved, and does any of the seven cases reveal
an unresolved constitutional conflict?

**Authority check.** The simulator is the Execution function's fill
rule under its existing Authorization; cash and P&L join positions as
`DERIVED` from `EFFECTIVE` fills; conservative accounting of provisional
fills is a refinement of the admission rules; reproducibility of
confirmation is already a property of a derived standing. No committer,
right, clock or admission authority is added. **No stop.**

| Case | Momentum `SV-8.1` / `TR-355` | Forward `SV-40.1` / `TR-415` | Verdict |
| --- | --- | --- | --- |
| 1. Fill proposal → confirmation → effective position | 03-19 17:29:10 fill of an opening order in name R, pre-witness `(17:29:10, E, 71)`, `PROVISIONAL`; confirmation `(17:29:12, E', 71)`: `TR-355` in force, `t_2 < T` → `EFFECTIVE`; position at sequence 1 102 includes it | 12-22 15:31 opening fill, bracketed `15:31:04` and `15:31:05`, `TR-415` in force → `EFFECTIVE`; the 16:00 reducing fill is `EFFECTIVE` at commit | One definition; recomputable from the two witnesses and the allocation content |
| 2. Fill proposal → unestablished → preserved record | 17:29:59 fill, confirmation `17:30:02 ≥ T` → `UNESTABLISHED`; preserved, labelled, counts for nothing; the flatten order is derived from `EFFECTIVE` fills only | Not exercised by the forward timeline; the rule is identical | A durable operational record, never execution, never deleted |
| 3. Expiry between pre- and post-witness | As case 2: the bracket cannot show the fill preceded `T`; `UNESTABLISHED` | A 15:30 fill on the day of a mid-session `T` would meet the same rule | Fail-closed; no instantaneity assumed |
| 4. Allocation revocation during confirmation | A Principal retirement `TR-357` applied at 72 between a fill's pre-witness at 71 and its confirmation at 72: `TR-355` not in force at `N_2` → `UNESTABLISHED`; the order is cancelled by the first set under `TR-357` | `TR-416` applied at 66 during a confirmation: same | The Applied History is append-only; in force at both reads proves in force throughout, and the converse refuses |
| 5. Concurrent provisional fills consuming the same risk capacity | Two opening fills in names R and S, both `PROVISIONAL`, gross limit with 1 unit of room: the first is admitted against the limit counting nothing provisional; the second is admitted against the limit counting the first as filled; if that breaches, refused `LIMIT`. Serial by Paper Book sequence | Two versions, one instrument: each version's provisional fill counts toward portfolio gross for the other | No two provisional fills can together exceed a limit either alone respects. Limits changing meanwhile: U-8, open by the Principal's direction |
| 6. Process death before confirmation; fresh process | Process dies after the 17:29:59 fill's commit; the fresh process finds it `PROVISIONAL`, calls confirm; the read is `17:40 ≥ T` → `UNESTABLISHED`; derivation for name R was frozen until then | 12-30 16:00 reducing fill is `EFFECTIVE` at commit; nothing to confirm; a provisional opening fill from 15:30 would be confirmed by the fresh process at its read | Standing decided by the later read, never by the fresh process's belief |
| 7. Reducing exposure with the clock unavailable | 03-12 17:02 Decision set with the Evidence boundary unreachable: `OPENING` refused `CLOCK_UNAVAILABLE`; the sell 40 in Q admitted `REDUCING` against `EFFECTIVE` long 40, `TR-355` in force at 68, limits at 68; the sell 30 refused `OPENING`; `CLOCK_UNAVAILABLE` recorded on the admitted order's witness | The 16:00 flatten with the clock unreachable: reducing fills `EFFECTIVE` at commit; the position goes to zero | Permitted only against established positions, authority and limits; no reversal or new exposure passes as reduction |

**Two verifications.** No `UNESTABLISHED` fill affects a confirmed
position or performance figure: positions, cash, exposures, P&L and the
executed record are defined over `EFFECTIVE` fills, and the Evaluation
non-conformance rule refuses any grounding series that includes
exploratory figures at all. No later confirmation rewrites historical
authority: a confirmation appends a post-witness; the fill, order,
pre-witness and every position stated at an earlier sequence are
unchanged; a position is stated at a sequence and includes only fills
`EFFECTIVE` at that sequence.

**Result: no unresolved constitutional conflict. The clarification is
within the approved delta. Admission may proceed.**

## 8. What this audit does not establish

That any process will discharge an obligation promptly, that a paper
fill rule will be realistic, that the clock an implementation presents
is the one the doctrine names, or that the interval between two reads
will be short enough for the paper book to be useful as a measurement
instrument. It establishes that the proposed rules are internally
consistent, that every fact has one owner, that nothing is assumed
instantaneous, that every failure leaves a visible record, and that the
ontology and authority changes are named rather than hidden.
