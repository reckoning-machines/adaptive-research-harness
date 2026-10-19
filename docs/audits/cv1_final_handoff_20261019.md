# Final Handoff to Codex — Whole-Design Review of the Propagated Design before `ConstitutionVersion 1`

Status: **HANDOFF — EVIDENCE, NOT DOCTRINE. Authorizes nothing;
certifies nothing.** Prepared by Claude at the Principal's direction,
2026-10-19.

## 1. Exact baseline

| Item | Value |
| --- | --- |
| Repository, branch | `speedway`, `main` |
| Baseline commit | `4407723` — "Admit PD-010 revision 4 (independent audit repairs); Constitution revision 11; preserve Codex audits; author's propagation check" |
| Governing text | [`docs/doctrines/new_speedway_constitution.md`](../doctrines/new_speedway_constitution.md), revision 11, status `DRAFT — NOT ADMITTED` |
| Admitted decision under review | [PD-010](../decisions/principal_decision_010_codex_audit_repairs.md) revision 4, admitted 2026-10-19 (document-phase) against SHA-256 `a47dad4069d06bbb469c300ef27361952b82193357edd1244d2edeecd2f723d2`, verified identical before the admission block was recorded; the block was then prepended, so the file's digest now differs from the reviewed one by that block alone |
| Prior baseline | `895f953` (revision 10; the one your original audit and the three PD-010 reviews cite) |

Nothing was pushed. Genesis is not executed; no code, runtime,
certification or CPOC claim exists.

## 2. Changed documents at this baseline, relative to `895f953`

| Document | Change |
| --- | --- |
| `docs/doctrines/new_speedway_constitution.md` | Revision 11: PD-010 propagated in §7's order. Touched: header; Summary table; §III.4 Provenance; §III.5 Prediction and Outcome rows, the reservation block (rewritten: Checker funding, attempt predicates, settlement validation, accounting, `BINDING`), evidentiary classes (`CLASS PENDING`); §III.6; §III.7 (hop default, grant content, triggers, resolution grace, fence before revoking either class, Checker caller rights); §III.8 (lifecycle, Check record items 3 to 6, the Apply binding bullet, Continuation, Independence); §III.10 (reducing bound, beyond-zero leg, refusal list, `FLATTEN_ON_QUOTA` removed, `REDUCE` re-execution); I-4; I-13; Part V (reservation row, `BIND`/`RELEASE` row, Hypothesis registration, Allocation with `REDUCE`, Limits row, standing row, Agent Design registration proposer, Authorization row, `P-1` (b), Genesis coordinates); Part VI (T-A, T-B, T-C reworked; T-D renumbered; T-F/T-G annotated); Part VII rows; Part IX principles 4 and 10; Part X R-3, R-8, §3, §4, §6; closing delta |
| `docs/decisions/principal_decision_010_codex_audit_repairs.md` | Admission block prepended; proposal history unchanged below it |
| `docs/decisions/principal_decision_004…`, `_005…`, `_007…`, `_008…`, `_009…` | A dated "Amended by PD-010" section appended to each; no historical text rewritten |
| `docs/audits/pd010_propagation_check_20261019.md` | New: the author's consistency check (finding-to-clause map; replays; interactions). Not the independent audit |
| `docs/audits/cv1_whole_design_audit_checklist_20261019.md` | Item 11 reworded per C-3 |
| `docs/audits/independent_preimplementation_design_audit_20261019.md`, `pd010_revision2_binding_review_20261019.md`, `pd010_revision3_binding_review_20261019.md`, `pd010_revision4_bounded_check_20261019.md` | Your audits, committed unchanged |
| `AGENTS.md`, `docs/plans/document_first_design.md` | Routing to revision 11, this handoff and the propagation check |

## 3. Finding-to-clause map

The map from B-1 to B-10, C-1 to C-7, R3-1 and R3-2 to the operative
clauses of revision 11, with the paper replays of the failed
transitions and the genesis funding chain, is
[§1 and §2 of the propagation check](pd010_propagation_check_20261019.md).
It is the author's claim, not evidence of closure; please treat it as a
reading guide and verify each entry against the text.

## 4. What this review must assess

The bounded binding check of revision 4 closed R3-1 and R3-2 at
proposal level. It did not close the original audit, and no author's
check can. This review assesses the **complete propagated design and
its interactions**, in particular:

1. Whether each of B-1 to B-10 is closed by the operative text, not by
   PD-010's description of it, under the original audit's adversarial
   traces and its two proof walks (Proof 1 evolutionary research; Proof
   2 development, Theme formation and competing Hypotheses).
2. The genesis walk from the empty system to ordinary operation under
   PD-009 as amended (sequence 17 deleted; `AU-OBS-1` without tools;
   `AU-CK-A` content; empty-ledger coordinates), including the first
   lawful independent Check and its funding.
3. Interactions the propagation created or touched: the `BINDING`
   bullet with `FENCE`, expiry, `OVERSPENT`, Checker grants, `P-1` (b)
   and the Continuation rule; the accounting with the lineage cap;
   `REDUCE` with the expiry obligation and the reducing bound; the
   cutoff rule with `CLASS PENDING`, the Checker's Outcome duty and
   R-3; the Prediction witness read with `P-1`; the Part VII carrier
   classes against the seven authority invariants.
4. Whether the declared delta is complete and no propagation step
   introduced policy or authority beyond PD-010's admitted choices
   (ΔO +1; ΔS as listed; ΔA +4), and whether the historical records'
   amendment notes preserve the distinction between a document-phase
   admission and an executed Constitutional Transition.
5. The whole-design [checklist](cv1_whole_design_audit_checklist_20261019.md)
   items, with item 11 as reworded.

## 5. Known open items, not part of PD-010

D-14 (provider as identity; fixed for the prototype by C-6); U-1
(grounding for a `NON-REPRODUCIBLE` version); U-8 (limits at a moving
head; plan step 7); real-provider output caps (PD-009 §5; unresolved
until a per-provider decision); `FR-0` as the provisional fill rule,
granted with the first Execution Authorization. No unresolved
substantive choice was isolated during propagation; if the review finds
one, it is the Principal's.

## 6. Constraints on the reviewer and the author

The review is evidence; it admits nothing. The author will not alter
the review. Any repair the review requires goes through a new proposed
decision record with its own declared delta, the Principal's admission,
and re-propagation, never through a silent edit of governing text.

## 7. Added for review (2026-10-19, after `fced833`): the prospect-facing architecture and the review package

The Principal directed a prospect-facing [`architecture.md`](../../architecture.md)
at the repository root, a root [`README.md`](../../README.md) and a
proposed [package manifest](../package/cv1_review_package_manifest.md).
These are explanatory; they introduce no policy and hold no authority.
Please add to the review:

1. **Fidelity.** Whether every statement in `architecture.md` about the
   design is supported by the clause it links to, and whether any
   simplification changes a meaning (in particular §5 Controls, §6 the
   runtime-checkpoint statement, and §8's practical implications of
   D-14, U-1, U-8, the provider-cap assumption and the fill-rule grant).
2. **Reuse claims.** Whether §6's table presents any candidate as a
   commitment, names a product without verified capability, or implies
   that a tool could hold a governed fact; and whether each "decisive
   acceptance criterion" is checkable against the Constitution rather
   than against the author's preference.
3. **Readiness claims.** Whether the document anywhere claims
   implementation, selection, certification, an executed witness or
   admission of `ConstitutionVersion 1`; it is intended to claim none.
4. **Package contents.** Whether the manifest's inclusions suffice to
   understand every admission (decision records with their amendment
   notes, pre-admission audits and re-audits, your four audits
   unchanged), whether its exclusions drop anything a reader needs, and
   whether every relative link inside the included files resolves
   within the package. The Principal's design proposal (`.docx`, with
   figures) is included at the Principal's direction as reference
   material that governs nothing.
5. **The author's consistency check** of links, terminology and
   readiness claims is
   [architecture_consistency_check_20261019.md](architecture_consistency_check_20261019.md);
   treat it as a claim to verify.

The final submission package is not built until this review and the
Principal's admission of `ConstitutionVersion 1` are complete.
