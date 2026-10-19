# OSA Re-audit after Admission of PD-002

Status: **AUDIT — EVIDENCE, NOT DOCTRINE. Authorizes nothing. Certifies
nothing.**

As-of: 2026-10-18, revision 3 of the
[Constitution](../doctrines/new_speedway_constitution.md), after
[PD-002](../decisions/principal_decision_002_predictions_decisions_observation.md)
revision 4 was admitted with the clarifications in the approved
[admission text](../decisions/admission_text_pd002_pd003_20261018.md).

Scope, as directed: the authority and semantic changes PD-002 introduces,
checked for conflict with the revision 2 text that remains, with PD-001's
admitted rules, and with the fin123-core doctrine adopted at `8175d504`
(Authority Normal Form; the seven authority invariants; the forward
evidentiary rules; CPOC's continuation rule). Budget: the admitted
`ΔO/ΔS/ΔA` of PD-002 and nothing beyond it. Not in scope: PD-003 (applied
next), PD-004, `ES-1`, D-10, D-11.

## Executive disposition

**A− — COHERENT WITHIN THE ADMITTED BUDGET. No unresolved constitutional
conflict. Two consistency repairs made inside the budget; eight open items
carried with owners.**

## Changes applied in revision 3

| Section | Change | Source |
| --- | --- | --- |
| Header | Revision 3 note; draft status unchanged | |
| Part II Roles | Observation function, Strategy Runner, Execution function added; distinct in authority, not necessarily in process | PD-002.2, PD-002.4; clarification (b) |
| Part III summary | Evidence row: callers restricted by kind; Paper Book row: Execution function sole caller | PD-002.2, .4 |
| §III.2 | Resolution rule over a declared resolution set; sources by `SourceId` active at base | PD-002 F-2, F-1 |
| §III.3 | Prediction target defined; artifact content includes declared inputs, trigger, frozen model; executability as closure to exposures; declared inputs and trigger; reproducibility class Checker-found; forward record defined; PD-001.2 citation | PD-002.1 |
| §III.4 | Provenance bullet: training cutoff, never evidence of freedom from leakage; D-14 open | PD-002.6 |
| §III.5 | Rewritten: Evidence clock as the only clock; table with Strategy Decision, Outcome over a bound set, Observation results and two times, reproduction records; Decision rules (event, output, closure, witness marks, reproduction); availability interval; class rule to the lower bound; negative evidence extended; PD-001.3 citation | PD-002.1, .2 |
| §III.7 | Five Authorization classes; content incl. Evidence kinds permitted; Observation plan; Runner standing rule; Source Declaration identity and revision; base-state rule; commit-right exclusions; refusal at commit boundaries | PD-002.2, .4, .5 |
| §III.8 | Ordinary commits restricted to the callers Part V names | PD-002.4 |
| §III.10 | Rewritten: set key; order types; remainder; cancel; re-execution; idempotency; limits; Execution function sole caller | PD-002.1, .4 |
| Part IV | I-2 to the lower bound; I-3 includes Decisions; I-8 names order types and callers; I-12 three facts; I-13 reads and witness reads; I-15 added | PD-002.1, .2 |
| Part V | Evidence commit split four ways with U-10 noted; Strategy Version registration Check extended; Paper Book row | PD-002.2, .4; clarification (a) |
| Part VI | T-A Check and Then rows (bound set, `AU-02b` at base 41); T-B Then row (Decision, set key); T-D rewritten; T-F and T-G adopted by reference | PD-002 F-1, F-2, F-3 |
| Part VII | Observation row reworded; availability interval, Decision, reproduction record, derived records, function working state rows; Paper Book row | PD-002 |
| Part VIII | Governance diagram: Functions subgraph; restricted Evidence edges; Runner and Execution edges | PD-002.4 |
| Closing delta | PD-002 admitted scope stated; U-10 no change | Clarification (a) |

## Consistency repairs made inside the budget

| Ref | Finding | Repair |
| --- | --- | --- |
| R-13 | I-8 named "Order and Fill commit" while §III.10 now has `REPLACE` and `CANCEL`; I-8 also did not say the boundary admits only named callers | I-8 reworded; within PD-002's admitted `ΔS` on order types and commit restrictions |
| R-14 | T-B's new Decision used illustrative sequence 2 507, which T-G (PD-002's timeline) assigns to `SD-7001` | T-B renumbered to 2 470 |

## Conflict checks

| Check | Result |
| --- | --- |
| Does any remaining revision 2 text still let a Research Agent commit a Market Observation or a Decision? | No. Roles, §III.7 and Part V all restrict; §III.8 says ordinary commits are caller-restricted |
| Does the Runner gain any right PD-002.4 denies? | No. Roles and §III.7 reproduce the denial list; the Runner appears in no proposer or checker column of Part V |
| Is the Execution function's trigger set still "committed Decisions" only? | Yes. §III.10 derives sets from Decisions; nothing in revision 3 lets it act on any other record. PD-004's deadline-event trigger is not present |
| Does any section still bind an Outcome to one Observation? | No. §III.5 table, T-A and Part VII use the bound set |
| Does any section still say "earliest retrieval is evidence of availability" as sufficient? | No. §III.5 and Part VII carry the interval; I-2 requires the lower bound |
| Is the Evidence clock the only clock? | Yes, stated in §III.5. No Paper Book clock was introduced |
| Does the witness read create authority? | No. I-13 names it as a read; §III.5 states the monotone-bound claim only |
| Does the one-order-per-allocation rule survive anywhere? | No. §III.10, I-12, T-B, T-D and Part VII use the set key |
| Does PD-001's authority rule survive intact? | Yes. §III.6 untouched; Applied History remains the applied subsequence of the one Transition ledger; Population State `DERIVED`; pinning unchanged |
| Does PD-002 touch `ES-1`, D-10 or D-11? | No. Reproduction sufficiency and the Outcome committer are routed to D-10 in Part V and §III.5 |
| Two-case consistency | T-A (forward) and T-B (traditional) both now have a bound-set Outcome or a Decision with closure and set key; T-F and T-G are the full tests by reference |
| ANF, seven invariants | One authority per new fact; carriers classed in Part VII; commit boundaries unchanged and caller-restricted; closures and keys bind by sequence; capital consumption unchanged; legacy not implicated; new refusals preserved (second Decision per event, closure above a witnessed head, commit outside Authorization, duplicate set or order, overfilling `REPLACE`, limit breach) |
| fin123-core forward doctrine | §5 (execution artifact; fixed at commitment) and §6 (declined is a claim) are reflected in Decisions; §9 two classes unchanged; reproduction standing orthogonal to class |
| CPOC continuation | T-D reconstructs from ledgers by key; no flag; D-17 still open |

## Open items preserved, with owners

| Item | Standing | Owner |
| --- | --- | --- |
| U-1 non-reproducible grounding | Open; `STOPPED` path in §III.3 | Principal, if wanted |
| U-2 cross-ledger simultaneity | Open by design; narrowed; §III.5 states the claim | Principal, plan step 9 |
| U-3 / D-10 Checker sufficiency, who may reproduce | Open; Part V and §III.5 route to D-10 | Principal, plan step 5 |
| U-4 / N-4 undeclared channels | Open; narrow reading in §III.5 | Principal |
| U-5 / D-17 Decide-to-Apply death | Open; T-D names it | Principal, plan step 4 |
| U-6 `ES-1` content | Undrafted | Principal, Constitutional Transition |
| U-7 / N-1 genesis | Bootstrap issue; no example claims replay from 0 | Principal, plan step 4 or 8 |
| U-8 limits at a moving head | Open; §III.10 cites it | Plan step 7 |
| U-10 Outcome committer | Deferred, no change; Part V says so | Principal, with D-10 |
| D-06 continuity claim | TENTATIVE in §III.5; removal recommended earlier; not in PD-002's budget | Principal |
| D-01, D-09, D-11, D-12, D-14, N-2, N-6 | Unchanged | As registered |

## What this re-audit does not establish

That any of this runs, replays or recovers. It establishes that revision
3 is internally consistent on the subjects PD-002 admitted, within the
admitted delta, with every open item named and owned. The Constitution
remains `DRAFT — NOT ADMITTED`.
