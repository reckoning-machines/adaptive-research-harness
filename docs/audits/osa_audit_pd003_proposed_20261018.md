# OSA Audit of PD-003 as Proposed

Status: **AUDIT — EVIDENCE, NOT DOCTRINE. Authorizes nothing.** Revision
4 (2026-10-18): audits
[PD-003 revision 4](../decisions/principal_decision_003_forward_research_formation.md),
dispositions PD-003.1 to PD-003.5. PD-003.6 was separated into PD-004
after the Principal found a remaining OSA defect in the event-count
expiry; its audit is
[osa_audit_pd004_proposed_20261018.md](osa_audit_pd004_proposed_20261018.md).
Findings P3-11, P3-12, P3-15, P3-16, P3-22, P3-24, P3-25 and P3-26 below
now belong to that audit and are kept here as history only.

As-of: 2026-10-18. Scope: the six dispositions, checked for duplicate
authority, information leakage, proposer influence on resolution, omitted
failures, cross-ledger currentness, time authority, two-case consistency,
and the Principal's directions. Not in scope: PD-002's own open items;
Group B (FR-6, FR-8, `ES-1`); D-10, D-11.

Reconciliation standard: ANF and the seven authority invariants; I-9; the
forward evidentiary rules (fin123-core §5, §9, §11).

## Executive disposition

**PD-003.1 to PD-003.5: B+ — READY FOR ADMISSION AFTER PD-002. No open
contradiction.** These five dispositions add no object, no commit right
and no clock; every new fact has one owner; `ΔA` is confined to two
scopes within the Authorization object.

**PD-003.6: SEPARATED.** The event-count expiry of revision 3 was found
defective by the Principal (no calendar expiry; no flattening when the
Runner is dead; reversal not covered by the opening-exposure rule). The
repair is in PD-004 and carries a declared `ΔA`. Feed absence witnesses now
require a complete retrieval within a declared enumeration contract. The
empirical path carries a complete selection history without a Theme, and
may state `UNESTIMATED`. Checker extraction is withdrawn to a future
proposal.

## Findings carried from revision 1 (unchanged unless noted)

| Ref | Mode | Finding | Disposition |
| --- | --- | --- | --- |
| P3-1 | Duplicate authority | Feed item and hop retrieval of one locator | NO: two receipts, one owner |
| P3-2 | Duplicate authority | `SCREEN` view and lineage memory | NO: both `DERIVED` |
| P3-3 | Duplicate authority | `DOCUMENT` receipt plus deterministic `VALUE` from one retrieval | ACCEPTABLE: the `VALUE` names its document and revision; reproducible |
| P3-4 | Leakage | Motivation closure member also a resolution member | CLOSED by disjointness |
| P3-5 | Leakage | Later sequence gamed by delayed hop | CLOSED: lower availability bound required; hops excluded from resolution sets |
| P3-6 | Proposer influence | Extraction rule fitted to a result | CLOSED: rule is `SourceRevision` content pinned at commitment; never retrospective; `NOT_EXTRACTABLE` is a committed fact |
| P3-7 | Proposer influence | Checker adjudication | **WITHDRAWN from the record** by direction; carried as a future proposal with D-10. The independence rule drafted in revision 1 is preserved here: not the proposer, not the lineage, did not check the Hypothesis registration |
| P3-8 | Omitted failures | Selection method records only chosen candidates | CLOSED: full candidate set with rejections |
| P3-9 | Omitted failures | Unscreened feed items invisible | CLOSED in revision 2: declared screening cadence; expected screens derivable; gaps counted in evaluation; gaps invalidate nothing else |
| P3-10 | Currentness | Selection estimates depend on `StateVersion` read | CLOSED: closure |
| P3-11 | Exploratory leakage | Label omitted in a report | CLOSED: label is an Applied History fact; non-conforming Evaluation refused at Check |
| P3-12 | Exploratory leakage | Repeated exploratory cycles | BOUNDED by pool, cap, expiry; lifetime cap is a limit (UD-10) |
| P3-13 | Two-case consistency | Burden on the momentum path | NO; revision 2 adds the selection basis to both paths equally |
| P3-14 | Stop conditions | New rules proposed, not established | Correct |

## New findings in revision 2

| Ref | Mode | Finding | Disposition |
| --- | --- | --- | --- |
| P3-15 | Time authority | Revision 1 let an expired `EXPLORATORY` allocation keep generating orders until its expiry Transition applied. Revision 2 closed it with an Evidence-clock "time witness", which made refusal depend on a later record arriving and would have required the Paper Book boundary to read a clock it does not have | CLOSED in revision 3: expiry is a decision-event count; the Paper Book commit boundary establishes currentness and count at order admission from records that must already exist; refuses opening exposure otherwise, including when a ledger is unreachable (I-13); no clock, no witness, no new authority. Applied History remains the sole allocation authority because every rule is content of an applied Transition |
| P3-16 | Time authority | `HOLD` leaves a position without an allocation authority to change it until the standing Transition | BOUNDED as directed: `HOLD` only as an explicitly authorized exception with reason, its own `expiry_events` and exit conditions; no opening exposure under it; `FLATTEN` after; the held position is a visible Paper Book fact. `FLATTEN` is the default |
| P3-17 | Evidence timing | Revision 1 let any prior feed slot establish absence, including partial, failed or late retrievals, and for items outside the feed's coverage | CLOSED: enumeration contract as meaning fields; feed retrieval records `COMPLETE`, `PARTIAL`, `RETRIEVAL_FAILED`; absence only from `COMPLETE` within contract and window, at the witnessed time; absence from the declared source distinguished from availability elsewhere (N-4 narrow reading stands) |
| P3-18 | Duplicate authority | Feed retrieval record and the feed items it returned: two Observations per retrieval | ACCEPTABLE: the retrieval record is an Observation of the feed (completeness and window); items are Observations of documents; different facts, one owner, cross-referenced by slot |
| P3-19 | Omitted failures | The empirical path had no place for alternatives, unsuccessful trials, reason and budget | CLOSED: selection basis on Strategy Version registration; `SearchFamily` label; Checker verifies cited trials are in the family |
| P3-20 | Invented precision | A required value estimate forces a number without basis | CLOSED: `UNESTIMATED` with reason is lawful; `ES-1` decides treatment; nothing penalizes it here |
| P3-21 | Authority | Hop depth 2 under the discovery scope could widen access through chains of links | BOUNDED: depth, count, fixed unit grant and the Observation Authorization's domain list all apply; the chain is recorded in the hop marker; the audit example shows a depth-2 domain refusal |
| P3-22 | Authority | Does the Execution function's expiry duty create a right? | NO: refusal, cancel and flatten are derivations from an applied Transition's content under the existing Execution Authorization; the function proposes and admits nothing |
| P3-23 | Semantics | `SearchFamily` as a label risks becoming an identity rule by use | NOTED: it is Research Record content grouped by a derived view; two records with the same label and different lineages are two families in the view unless the Standard says otherwise. If a governed family identity is ever needed, that is a `ΔO` decision for the Principal, not an inference |
| P3-24 | Time authority | Could the Paper Book commit boundary be given its own clock for calendar expiry? | REJECTED for the initial Constitution: the doctrine's only clock is the Evidence commit boundary's, and the Constitution and PD-002 never declared one for the Paper Book; declaring one would be a new time authority, which the Principal forbade. Consequence stated in the record: calendar bounds on exploratory allocations are expressed as event counts or by Transition. Carried as UD-14 in case a later Principal decision wants a Paper Book clock |
| P3-25 | Omitted failures | A dead Runner after the `N`th Decision leaves a position with no flatten trigger | VISIBLE, not hidden: no opening exposure can be admitted; the position, the missing Decision (derivable from the trigger declaration) and the incomplete flattening are facts; the standing Transition or the next admission attempt flattens. The Principal's clarification accepts this as a visible fact rather than inventing a trigger |
| P3-26 | Duplicate authority | The Execution function's refusal and the Paper Book boundary's refusal both exist | NO: one is the function declining to derive (recorded as its own act); the other is the boundary refusing an admitted order (preserved by the boundary). Both are Paper Book facts about different acts; the boundary's refusal is the one that binds |

## Verification against the Principal's directions

| Direction | Where satisfied |
| --- | --- |
| Hop depth 2 under domain, count and resource limits | PD-003.1 discovery scope; hop rule |
| Deterministic extraction only; Checker extraction future, dependent on D-10 | PD-003.3; `ΔA` for extraction withdrawn |
| Exploratory purpose per Allocation Transition | PD-003.6 standings table |
| Discovery units as a fixed grant | PD-003.1 discovery scope |
| D-01 accepted: succession without re-parenting | PD-003.4 |
| Expired allocation must not retain order permission; refusal established at order admission from existing records; no dependence on a later record; no new time authority; no implicit execution right; `FLATTEN` default, `HOLD` bounded exception; no new opening exposure after expiry; cancellation, late fills and incomplete flattening visible; only Apply changes allocation | PD-003.6 expiry table and OSA consequence; P3-15, P3-16, P3-22, P3-24, P3-25, P3-26 |
| Absence witness only from complete coverage; failed, partial or delayed retrievals establish nothing; declared-source absence versus other channels | PD-003.1 completeness table and rules 1 to 4; P3-17 |
| Empirical Strategy keeps selection history without Theme or Hypothesis: alternatives, unsuccessful trials, reason, budget; `UNESTIMATED` lawful; AIE optional | PD-003.5; two-case test; P3-19, P3-20 |
| Screening cadence: missing screens visible and counted, without invalidating unrelated research | PD-003.1 discovery scope; P3-9 |

## ANF check

| Invariant | Finding |
| --- | --- |
| Singular decision authority | Feed items, feed retrieval records, hops, screens, formation records, selection records, time witnesses, refusals, cancel and flatten sets, capital standings: one owner each |
| Classified representation closure | `SCREEN` view, lineage memory, search-family view, selection outcome, expired-held projection, labelled executed record: `DERIVED`; stored bytes `RECEIPT` |
| Exclusive governed commit boundary | Unchanged; callers restricted per kind; no new committer |
| Temporal and binding closure | Closures by sequence; resolution by pinned revision and completeness-based lower bound; expiry by decision-event count against applied content, no clocks compared; selection by `StateVersion` |
| Owner-resolved consumption | Discovery units under the fixed grant; Theme units under the Theme Authorization; exploratory capital from a limit at Apply; budget-consumed figures `DERIVED` |
| Legacy isolation | Not implicated |
| Constitutional failure closure | New refusals, each preserved: hop outside scope, depth, count, units, domain, or locator not in cited bytes; resolution member in motivation closure or from a source without a deterministic rule; `PARTIAL` or failed retrieval cited as absence; order set from a Decision after expiry; Evaluation with exploratory grounding; Strategy registration citing trials outside its family |

## Open items carried

| Ref | Subject | Who decides |
| --- | --- | --- |
| UD-4, Checker extraction authority | Future proposal with D-10 | Principal |
| UD-10 | Lifetime cap on exploratory cycles per version | Principal, as a limit |
| UD-11 | Whether `SELECTION OUTCOME` is scheduled or computed on citation | `ES-1` |
| UD-12 | Treatment of `UNESTIMATED` and of search-family trial counts | `ES-1` (Group B) |
| UD-13 | `FLATTEN` default; `HOLD` bounded exception | DECIDED by the Principal's clarification; closed |
| UD-14 | Whether the Paper Book commit boundary should ever carry a declared clock (calendar expiry; fill timing analysis) | Principal, later; a new time authority if ever introduced |

## Admission recommendation

PD-003 revision 4 (dispositions 1 to 5) is ready for admission after
PD-002. No constitutional blocker remains within its scope. PD-004 is
not ready and stays proposed; see its audit.

## What this audit does not establish

That feeds will carry what matters, that deterministic extraction will be
available for the sources that matter, or that any selection method
selects well. It establishes that PD-003 as proposed has one owner per
fact, satisfies the directions, and does not alter PD-001 or PD-002.
