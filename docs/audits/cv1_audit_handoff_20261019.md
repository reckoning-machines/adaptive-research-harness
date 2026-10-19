# Audit Handoff for the Independent Whole-Design Audit before `ConstitutionVersion 1`

Status: **HANDOFF — EVIDENCE, NOT DOCTRINE. Authorizes nothing,
certifies nothing, audits nothing.** Prepared 2026-10-19 by the
drafting agent for the Principal's separate auditor. The independent
audit is not performed here; routine consistency and link checks were,
and their results are listed as unresolved issues for the auditor.

## 1. Subject

| Item | Value |
| --- | --- |
| Repository | `github.com/reckoning-machines/speedway`, branch `main` |
| Commit audited | `2f24eb2` ("Admit PD-009 … Constitution revision 10"); this handoff is committed immediately after it and changes no governed text |
| Constitution | `docs/doctrines/new_speedway_constitution.md`, **revision 10**, status `DRAFT PRODUCT DOCTRINE — NOT ADMITTED`; no TENTATIVE marker; `ES-1.0` is Part X; policy `P-1` and the genesis clause are in Part V |
| Standing of every admission so far | Document-phase Principal admissions that stand in for a Constitutional Transition until genesis; no Constitutional Transition has executed; no CPOC witness has run; nothing is certified |
| Engineering discipline | `docs/decisions/fin123_core_adoption_20261018.md` (fin123-core at `8175d504`), with the dated New Speedway standard "Tools are replaceable" appended |

## 2. Paths

| Role | Path |
| --- | --- |
| Router and stop conditions | `AGENTS.md` |
| Governing doctrine | `docs/doctrines/new_speedway_constitution.md` |
| Admitted decisions, in order | `docs/decisions/principal_decision_001_identity_and_evidence.md`; `…_002_predictions_decisions_observation.md`; `…_003_forward_research_formation.md` (dispositions 1 to 5); `…_004_exploratory_capital_standings.md`; `…_005_es1_evaluation_standard.md`; `…_006_replaceable_tools_and_first_prototype.md`; `…_007_independent_checking_and_delegated_admission.md`; `…_008_research_budget_reservation.md`; `…_009_genesis.md` |
| Approved admission texts | `docs/decisions/admission_text_pd002_pd003_20261018.md`; `docs/decisions/admission_text_pd005_20261019.md`; the others are in each record's status header |
| Genesis proposal (admitted as content; not executed) | `docs/decisions/principal_decision_009_genesis.md` |
| Audit checklist for this audit | `docs/audits/cv1_whole_design_audit_checklist_20261019.md` |
| Re-audits after each admission | `docs/audits/osa_reaudit_pd001_20261018.md` … `osa_reaudit_pd004_20261019.md`, `osa_reaudit_pd005_20261019.md`, `osa_reaudit_pd006_20261019.md`, `osa_reaudit_pd008_20261019.md`, `osa_reaudit_pd007_20261019.md`, `osa_reaudit_pd009_20261019.md` |
| Pre-admission audits and comparisons | `docs/audits/initial_osa_audit.md`; `forward_research_osa_audit_20261018.md`; `pd002_admission_readiness_20261018.md`; `osa_audit_pd003_proposed_20261018.md`; `osa_audit_pd004_proposed_20261018.md`; `es1_osa_audit.md`; `pd006_readiness_review_20261019.md`; `osa_audit_pd007_proposed_20261019.md`; `osa_audit_pd008_proposed_20261019.md`; `pd008_revocation_ordering_comparison_20261019.md` |
| Plans | `docs/plans/document_first_design.md`; `docs/plans/forward_research_design_plan.md` |
| Reference, non-authoritative | `docs/reference/new_speedway_discussion_draft_20261017.md`; `docs/reference/es1_methods_note_20261019.md` |

## 3. Unresolved issues found by the author's consistency check

These are not audit findings. They are inconsistencies the drafting
agent noticed while preparing this handoff, listed so the auditor can
confirm or dismiss them.

| Ref | Clauses | Issue | Smallest repair the author would propose | Delta if repaired |
| --- | --- | --- | --- | --- |
| U-A | §III.5 reservation block ("committed by the grantee under its **Research** Authorization"); §III.7 ("A **Research** Authorization's grant is stated in units…"); Part V `RESERVATION` row; PD-009 §3 (`AU-CK-A` 60 units, `AU-CK-B` 30 units) | A Checker's paid calls are consequential consumption requiring a reservation and a pre-recorded attempt under PD-008, but the reservation, attempt and grant-content rules name only Research Authorizations. The first Checker holds units it has no stated path to reserve or attempt against | Add "or Checker" in the three places; nothing else | `ΔS` three phrases; `ΔO` 0; `ΔA` 0 |
| U-B | PD-009 §2 row 1 (synthetic provider "as a declared tool" under `AU-OBS-1` at sequence 1); PD-009 §5; §III.7 (a grant names the tools it may consume and their tiers) | The first Checker's first paid Check is of sequence 1, the Transition that would declare the tool it runs on. The consuming Authorization must name its own tools, so `AU-CK-A` at sequence 0 should carry them | PD-009 record content: `AU-CK-A`, `AU-CK-B` and `AU-RP-1` each name their tools and tiers; `AU-OBS-1` declares sources, not provider tools | Record content; `ΔS` 0 |
| U-C | §III.7 "maximum hop depth (default 2)" (PD-003) | The one numerical literal outside Part X §6 | Label it provisional Authorization content, or accept as limitation L-1 | `ΔS` one word, or none |

## 4. Accepted prototype limitations

| Ref | Limitation | Accepted by |
| --- | --- | --- |
| L-1 | Hop depth default "2" is a literal in §III.7; Authorization content overrides it | PD-003 |
| L-2 | Real-provider output caps are unresolved; demonstrations run on a bounded synthetic provider and metered tools; no real-provider spending guarantee is claimed; uncapped calls are prohibited | PD-009 |
| L-3 | No genuine prospective market evidence exists at genesis; every Evaluation says so | PD-006, PD-009 |
| L-4 | No Strategy Runner, Execution function or Paper Book at genesis; PD-004 and the fill rule `FR-0` are paper-specified only | PD-009 |
| L-5 | The Observation function's own retrieval costs are unmetered; discovery units meter the requester's Research Records | Open, minor |
| L-6 | A `CHECKER` agent's blind spots are visible only through verification yield; a human or a different provider may be required by Authorization content | PD-007 |
| L-7 | One Principal; every reserved decision waits on one person | Principal |
| L-8 | Vendor invoices are not bounded; overruns are accounted in full, not prevented | PD-008 |
| L-9 | **Every guarantee in every document is paper-specified.** No runtime enforcement, replay, recovery, ordering or ceiling has been demonstrated by writing these documents; CPOC has no witness | All records |

## 5. The bootstrap funding chain

How the first Checker is funded before its first paid Check, as the
documents specify it after U-A and U-B are resolved; without them the
chain has the two gaps named above.

1. **Apply sequence 0** (Constitutional Transition, Principal, Check
   waived by the Part V genesis clause for this sequence and these
   three items only): the `ConstitutionVersion 1` text; the
   registration of `AD-CK-1.0` (method class `CHECKER`, provenance
   declared); and Checker Authorization `AU-CK-A` to it, whose content
   includes a grant of 60 units, the estimation rule, and the tools it
   may consume with their tiers (the bounded synthetic provider, tier 2
   by construction; metered local compute, tier 1). The grant is the
   Principal's act, part of the enumerated bootstrap; the Checker
   approves nothing about it.
2. **`AD-CK-1.0` commits a `RESERVATION`** against `AU-CK-A` on the
   Evidence ledger: an ordinary commit by the grantee, requiring no
   Check, admitted only if the grant covers it and no fence precedes it.
   This draws on a grant already made; it does not approve funding.
3. **`AD-CK-1.0` pre-records a `PENDING` attempt** within that
   reservation, naming the synthetic provider and an estimated maximum
   in units, admitted only within the reservation's remaining allowance.
4. **It performs the Check of sequence 1** (`AU-OBS-1`), appending the
   Check record, and **settles the attempt** with the actual units from
   the tool's record.
5. Every later paid Check follows steps 2 to 4. Anything concerning
   `AD-CK-1.0` itself (its successor, amendment or revocation) is
   checked by `AD-CK-2.0`, registered at sequence 13 and granted
   `AU-CK-B` at sequence 14, each checked by `AD-CK-1.0`, which is not in
   that lineage.
6. No exception is relied on beyond the sequence-0 waiver already
   admitted; no Checker approves its own funding; the Principal's grant
   at sequence 0 is the only source of the Checker's resources.

All of the above is paper-specified. None of it has been executed.

## 6. Routine checks performed for this handoff

- Every relative Markdown link under `docs/` and in `AGENTS.md`
  resolves to an existing file (checked at `2f24eb2`).
- Every admitted record's status header carries its approved admission
  text; every re-audit's change table names the sections the
  Constitution text shows changed.
- Fenced blocks in the Constitution balance; no TENTATIVE marker
  remains; `AGENTS.md` states revision 10.

What this handoff does not do: audit, certify, admit, execute genesis,
select infrastructure, or begin implementation.
