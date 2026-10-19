# Proposed Review Package Manifest — `ConstitutionVersion 1` Design

Status: **PROPOSED MANIFEST. No ZIP has been built.** The final
submission package follows the independent whole-design review and the
Principal's admission of `ConstitutionVersion 1`. Prepared 2026-10-19
against Constitution revision 11 (baseline commit `4407723`; handoff
`fced833`).

Packaging rule: the ZIP root mirrors the repository root, so every
relative link inside the included files resolves unchanged. Files are
included byte-for-byte as committed.

## Included

| Path | Why |
| --- | --- |
| `README.md` | Entry point and reading order |
| `architecture.md` | Prospect-facing explanation; governs nothing |
| `docs/doctrines/new_speedway_constitution.md` | The governing text, revision 11 |
| `docs/plans/document_first_design.md` | The order of work, the prototype target and the reuse constraint |
| `docs/plans/forward_research_design_plan.md` | The forward-research plan referenced by PD-003 |
| `docs/decisions/fin123_core_adoption_20261018.md` | What engineering discipline was adopted, from where, and what was not |
| `docs/decisions/principal_decision_001_identity_and_evidence.md` through `principal_decision_010_codex_audit_repairs.md` | Every admitted decision with its admission text; PD-004, PD-005, PD-007, PD-008 and PD-009 carry dated "Amended by PD-010" sections |
| `docs/decisions/admission_text_pd002_pd003_20261018.md`, `docs/decisions/admission_text_pd005_20261019.md` | Approved admission texts cited by the records |
| `docs/audits/initial_osa_audit.md` | The first audit; home of the open items D-14 and the decision register |
| `docs/audits/forward_research_osa_audit_20261018.md`, `osa_audit_pd003_proposed_20261018.md`, `osa_audit_pd004_proposed_20261018.md`, `osa_audit_pd007_proposed_20261019.md`, `osa_audit_pd008_proposed_20261019.md`, `es1_osa_audit.md`, `pd002_admission_readiness_20261018.md`, `pd006_readiness_review_20261019.md`, `pd008_revocation_ordering_comparison_20261019.md` | Pre-admission audits and comparisons cited by the records |
| `docs/audits/osa_reaudit_pd001_20261018.md` through `osa_reaudit_pd009_20261019.md` | Re-audits after each admission; home of U-1 and U-8 |
| `docs/audits/cv1_whole_design_audit_checklist_20261019.md`, `docs/audits/cv1_audit_handoff_20261019.md` | The checklist and the first handoff to the independent reviewer |
| `docs/audits/independent_preimplementation_design_audit_20261019.md`, `pd010_revision2_binding_review_20261019.md`, `pd010_revision3_binding_review_20261019.md`, `pd010_revision4_bounded_check_20261019.md` | The four independent audits, unchanged |
| `docs/audits/pd010_propagation_check_20261019.md`, `docs/audits/architecture_consistency_check_20261019.md` | Author's checks, labelled as such |
| `docs/audits/cv1_final_handoff_20261019.md` | The handoff for the final review, including §7 on this package |
| `docs/reference/new_speedway_design_proposal_20261019.docx` | The Principal's design proposal with figures, included at the Principal's direction; reference only |
| `docs/reference/new_speedway_discussion_draft_20261017.md` | Text transcription of the proposal; reference only |
| `docs/reference/es1_methods_note_20261019.md` | Illustrative methods for the Evaluation Standard; governs nothing |
| `docs/package/cv1_review_package_manifest.md` | This manifest |

After the final review, that review's document is added to
`docs/audits/` and listed here.

## Excluded, and why

| Excluded | Reason |
| --- | --- |
| `.git/` and any repository metadata | Repository internals |
| `AGENTS.md` | A router for agents working in the repository; its content is routing, not design. Every document it points to is included |
| Any local runtime data, caches, build output, environment files or credentials | None exist in the repository; the rule stands for the package |
| Scratch drafts outside the repository | Nothing outside the committed tree is packaged |
| Session or memory files of any authoring tool | Not part of the repository |

Nothing historical is excluded: every superseded record needed to
understand an admission is included with its amendment note, and no
audit is edited.

## Build instruction, for later

From the repository root at the admitted baseline, archive the listed
paths preserving directory structure. Verify before sending that every
relative link in the included Markdown resolves inside the archive (the
author's check script in
[architecture_consistency_check_20261019.md](../audits/architecture_consistency_check_20261019.md)
does this) and that the archive contains no path outside this list.
