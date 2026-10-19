# OSA Re-audit after Admission of PD-004

Status: **AUDIT — EVIDENCE, NOT DOCTRINE. Authorizes nothing. Certifies
nothing. No CPOC witness has been executed.**

As-of: 2026-10-19, revision 5 of the
[Constitution](../doctrines/new_speedway_constitution.md), after
[PD-004](../decisions/principal_decision_004_exploratory_capital_standings.md)
revision 3 with the internal-simulator clarification was admitted
against the revision 4 text reconciled for PD-002 and PD-003
(re-audits [PD-002](osa_reaudit_pd002_20261018.md) and [PD-003](osa_reaudit_pd003_20261018.md)).
The pre-admission audit and its final focused review are
[osa_audit_pd004_proposed_20261018.md](osa_audit_pd004_proposed_20261018.md).

Scope, as directed: the ontology, semantic and authority changes PD-004
introduces, checked for conflict with revision 4, with PD-001 to PD-003
as admitted, and with the adopted fin123-core doctrine (ANF; the seven
authority invariants; CPOC's negative invariants). Budget: the admitted
`ΔO` +1 (Fill Confirmation), the listed `ΔS`, and `ΔA` confined to the
Execution Authorization's trigger set and the Paper Book boundary's
clock read. Not in scope: `ES-1`, D-10, D-11, plan step 7.

## Executive disposition

**A− — COHERENT WITHIN THE ADMITTED BUDGET. No unresolved constitutional
conflict. One definition of an effective fill. Four consistency repairs
made inside the budget; open items carried with owners.**

## Changes applied in revision 5

| Section | Change | Source |
| --- | --- | --- |
| Header | Revision 5 note; FR-12 and UD-14 closed; draft status unchanged | Admission text |
| Part II Roles | Execution function: expiry instants as triggers; proposes simulated fills by its fill rule; may not open exposure under an expired or superseded allocation | PD-004 `ΔA` 1; §PD-004.15 |
| Part III summary | Paper Book row: Fill Confirmation identity; positions from confirmed fills; Confirmation commit | `ΔO` +1 |
| §III.3 | Capital standing bullet: `INCUBATING`, `EXPLORATORY`, `QUALIFIED`; label; non-conformance rule; no threshold | PD-004.1 |
| §III.5 | Clock read defined: a duty of the Evidence boundary, commits nothing, `EPHEMERAL` until recorded; what a read establishes; no local clock | PD-004.2 |
| §III.6 | Exploratory pool as a limit; "in force" defined; expiry does not end an allocation, Apply does; derived expired projection | PD-004.5 |
| §III.7 | Execution Authorization content: fill rule (internal simulator; plan step 7), permitted triggers, promptness expectation without authority | `ΔA` 1; §PD-004.15 |
| §III.10 | Rewritten: identity with Fill Confirmation; authority incl. reads; sets, cancels on newer allocation, re-execution to zero, expiry set; intent class on the same-side working position with provisional fills counted conservatively; admission witness and bracketing; provisional simulated fill versus confirmed execution fact; admission rules with reason codes; expiry obligation and terminal state; idempotency incl. confirmations; limits with provisional consumption and U-8 open; incomplete flatten | PD-004.2 to .5, .15 |
| Part IV | I-8 adds Confirmation commit; I-12 names fills and confirmations as Paper Book facts and positions from confirmed fills; I-13 names the Paper Book boundary's reads | PD-004 |
| Part V | Allocation row content and Check; new Standing Transition after expiry row; Order row renamed to include Fill Confirmation, triggers and admission rules | PD-004 |
| Part VI | T-H added (momentum expiry and recovery); forward case adopted by reference; T-B's fills now proposed, admitted provisional and confirmed | PD-004.9 |
| Part VII | Rows: admission witness; provisional simulated fill; fill standing; unestablished fill; positions, cash, exposures, P&L from `EFFECTIVE` fills at a sequence; derived class, index, standing, obligation, terminal state; Execution function working state | PD-004.15 |
| Part VIII | Governance diagram: expiry instants, proposed fills and confirmations, clock-read edge; new sequence diagram for T-H | PD-004.6 |
| Closing delta | PD-004 admitted scope | Admission text |

Not changed, by design: §III.1, §III.2, §III.4, §III.8, §III.9, Part VI
T-A, T-C to T-G, the evolutionary and concurrent-admission diagrams.
PD-004 adds no research, discovery, formation or evidentiary rule.

## Consistency repairs made inside the budget

| Ref | Finding | Repair |
| --- | --- | --- |
| R-15 | §III.3 declared input kinds and forward record, §III.5 closure marks, and T-B said "fills" where the Principal's clarification requires confirmed fills | "own confirmed fills"; "executed record from confirmed fills"; "positions derived from confirmed fills at or below `F`"; T-B's fills proposed, admitted provisional and confirmed |
| R-16 | T-H's Before and After rows named state 68 for both the base and the Apply | Base state 67; `TR-355` applied at 68 |
| R-17 | Verified, not repaired: §III.10's same-side working position counts a `PROVISIONAL` fill as confirmed on its own side, per §PD-004.15 rule 2 | None needed |
| R-18 | Part V had no row for the standing Transition after expiry, which PD-004.5 names | Row added: Principal or admitted policy proposes; Checker verifies the expiry set, refusals, cancels, confirmations, residual |
| R-19 | Part VII had no carrier for cash and P&L, which the clarification names | Positions, cash, exposures and P&L in one row, `DERIVED` from `EFFECTIVE` fills at a sequence |

## Conflict checks

| Check | Result |
| --- | --- |
| Does the Paper Book have one unambiguous definition of an effective fill? | YES. §III.10: a fill of an `OPENING` order is `EFFECTIVE` when its confirmation's post-witness and its pre-witness both show the allocation in force and, where declared, `t < expiry_time`; a fill of a `REDUCING` order is `EFFECTIVE` at commit. Every other mention of positions, cash, exposures, P&L, closure marks, declared inputs and the executed record now says confirmed fills (R-15) |
| Can an unestablished fill affect a confirmed position or a performance figure? | NO. Positions and the executed record are defined over `EFFECTIVE` fills; Part VII denies the unestablished fill any place in them; the non-conformance rule refuses any grounding series with an exploratory figure at all |
| Can a later confirmation rewrite historical authority? | NO. A confirmation appends a post-witness; §III.10 says a position is stated at a Paper Book sequence and includes only fills `EFFECTIVE` at that sequence; no earlier record changes |
| Is there a second clock anywhere? | NO. §III.5 keeps the Evidence clock as the only clock; §III.10 says the Paper Book keeps none; the witness time value is a `RECEIPT` |
| Does any rule admit on the absence of a record? | NO. Every opening admission, every confirmation and the obligation predicate rest on positive reads; `Observation` records are not consulted for time |
| Are checks and commits anywhere assumed instantaneous? | NO. §III.10 states the interval, the monotone-condition rule and the logical admission point; limits are explicitly excluded (U-8) |
| Does the simulator create a new committer? | NO. Fills are proposed by the Execution function's fill rule under its Authorization and committed by the Paper Book boundary; the Fill Confirmation is committed by the boundary on the function's call. Part V names one caller |
| Does the Execution function gain any right PD-002.4 denies? | NO. It may act on an instant no Decision produced (declared `ΔA` 1); it still runs no Strategy, commits no Evidence, and may not open exposure after expiry or under a superseded allocation |
| Does PD-001's authority rule survive? | YES. Allocation, standing, expiry content and the pool are Applied History facts; "expired" is `DERIVED`; only Apply changes allocation |
| Does PD-002 survive? | YES. Decision commit, closure, witness marks, order sets and `REPLACE` unchanged; the closure's Paper Book mark now counts confirmed fills, which narrows nothing a Decision could lawfully read |
| Does PD-003 survive? | YES. Nothing in §III.1, §III.2, §III.5's document rules or §III.7's feed rules changed |
| Can a provisional fill create excess exposure? | NO. It counts as filled for every exposure check and consumes limit capacity by Paper Book sequence; it blocks further derivation for its version and instrument |
| Can a reversal pass as reduction? | NO. Same-side working position; single crossing orders refused |
| Can the expiry obligation be discharged by a record? | NO. Only the terminal state or supersession |
| Two-case consistency | T-H (momentum) in Part VI; the forward case by reference to PD-004.9; both run under §III.10 without a special case |
| ANF, seven invariants | One owner per fact (table in PD-004 §3, now mirrored in Part VII); every carrier classed; boundaries unchanged but for the new record kind on the existing Paper Book boundary; bindings by key, sequence and witness; consumption at Apply and by sequence; legacy not implicated; fourteen refusal reasons and one terminal standing preserved |
| CPOC negative invariants | Transient-authority leakage: none, obligations and standings are predicates over ledgers and a fresh read. Mutable-present substitution: a fill's standing is fixed by its own two reads. Resurrection: one expiry set, one confirmation, closed orders refuse fills, `UNESTABLISHED` terminal. Cross-surface disagreement: one derivation. Process-local continuation: every case continues from ledger coordinates |
| Stop conditions | Every identity, kind, meaning, commit boundary and authority touched was proposed in PD-004 and decided by the Principal; none was established by the revision |

## Open items preserved, with owners

| Item | Standing | Owner |
| --- | --- | --- |
| U-8 limits at a moving head | Open by the Principal's direction; witnesses establish nothing about non-monotone limits | Plan step 7 |
| Paper fill methodology (D-09 remainder) | Not invented; Execution Authorization content | Plan step 7 |
| P4-R1 promptness of discharge during Execution-function death | Operating expectation, no authority | Principal, Execution Authorization |
| P4-R3 clock monotonicity and read provenance | Implementation conformance; witness at plan step 8 | Plan step 8 |
| P4-R4 portfolio net limits versus version-level flatten | Limit content | Principal |
| P4-R5 `UNESTABLISHED` may discard a lawful paper fill | Accepted as a measurement artifact of the simulator | Principal, recorded |
| UD-3 `NON-REPRODUCIBLE` versions and `EXPLORATORY` capital | Open | Principal, with U-1 |
| UD-5, UD-10 pool size, caps, lifetime cap | Limits | Principal |
| U-1 to U-7, U-10 (PD-002); FR-4, FR-6, FR-8, FR-9, UD-4, UD-11, UD-12 (PD-003); D-06, D-10, D-11, D-12, D-14, D-17, N-1, N-2, N-4, N-6 | Unchanged | As registered |

Closed by this admission, by reference: FR-12, UD-14.

## Readiness for `ES-1`

The Evaluation Standard can now be drafted against a stable object
model: Decisions and their derived reproduction standing (PD-002), the
decision-implied record at a Standard-declared notional (PD-002), the
executed record from confirmed fills under a capital standing and label
(PD-004), typed claims, search families and selection bases (PD-003),
and the two evidentiary classes (PD-001). `ES-1` carries U-6, FR-6,
FR-8, FR-9, UD-11, UD-12 and the forward-event minimum, notional and
`UNESTIMATED` treatment. Nothing in revision 5 blocks it. The
constitutional route is a Constitutional Transition proposed by the
Principal, declared `ΔO/ΔS/ΔA`, with a Checker.

## What this re-audit does not establish

That any simulator will fill realistically, that an implementation will
present the clock the doctrine names, that confirmations will arrive
promptly enough for the paper book to measure anything, or that any
process survives death as specified. It establishes that revision 5 is
internally consistent on the subjects PD-004 admitted, within the
admitted delta, with one definition of an effective fill and every open
item named and owned. The Constitution remains `DRAFT — NOT ADMITTED`.
Nothing is certified.
