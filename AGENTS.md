# New Speedway Repository Jurisdiction and Routing

Status: **ROOT ROUTER — DERIVATIVE, NOT DOCTRINE**

This file is the entry point for a participant working in this repository.
It routes to the governing documents, states the stop conditions, and says
what phase the work is in. It does not summarize the doctrine and does not
hold authority of its own.

## What New Speedway is

An operating system for an evolving quantitative investment process, in
which agents may generate research, write strategies and evolve their own
research methods, while every consequential change to the investment
process is authorized, budgeted, independently checked and recorded as
governed state. The doctrine is in
[the New Speedway Constitution](docs/doctrines/new_speedway_constitution.md).

## Phase

**Document-first design. No application code is authorized.** The system is
being built in documents until it is constitutionally coherent there. The
order of work is
[the document-first design plan](docs/plans/document_first_design.md).
Known defects and open decisions are in
[the initial OSA audit](docs/audits/initial_osa_audit.md).

The Constitution is a draft at revision 11 (PD-001 to PD-010 applied;
`ES-1.0` is Part X; policy `P-1`, the genesis clause and the Limits row
in Part V; the Apply binding in §III.5 and §III.8). **Current work:**
the independent audit
([Codex, 2026-10-19](docs/audits/independent_preimplementation_design_audit_20261019.md))
found OSA FAIL at revision 10; its repairs were admitted as
[PD-010](docs/decisions/principal_decision_010_codex_audit_repairs.md)
(revision 4, after Codex's reviews of
[revision 2](docs/audits/pd010_revision2_binding_review_20261019.md),
[revision 3](docs/audits/pd010_revision3_binding_review_20261019.md)
and the [bounded check of revision 4](docs/audits/pd010_revision4_bounded_check_20261019.md))
and propagated as revision 11, with an
[author's propagation check](docs/audits/pd010_propagation_check_20261019.md)
that is not the independent audit. Next: Codex's final whole-design
review of the propagated design, per the
[final handoff](docs/audits/cv1_final_handoff_20261019.md). The
Constitution is not admitted as `ConstitutionVersion 1`. Nothing in
this repository is certified, no CPOC witness has been executed, and no
Constitutional Transition has executed: admissions so far are
document-phase Principal admissions that stand in for genesis.

## Engineering discipline

New Speedway adopts the fin123-core engineering discipline: Constitutional
Coherence, Authority Normal Form, the six representation classes, the
`Audit -> Plan -> Implement -> Verify` motion, the Constitutional Delta
`ΔO/ΔS/ΔA` with a normal budget of `0/0/0`, the constitutional stop
condition, and CPOC in its source meaning. What was adopted, from which
exact source files at which commit, and what was deliberately not adopted,
is recorded in
[the adoption record](docs/decisions/fin123_core_adoption_20261018.md).
IRIS product ontology is not adopted. Read the source documents named
there when their exact wording matters; do not infer the discipline from
this file.

## Routing

| Question or work | Read |
| --- | --- |
| What exists, what it means, who owns it, what may change | [Constitution](docs/doctrines/new_speedway_constitution.md) |
| What is unresolved, and who decides it | First, the [final handoff](docs/audits/cv1_final_handoff_20261019.md) and the [author's propagation check](docs/audits/pd010_propagation_check_20261019.md) for PD-010; the [independent pre-implementation audit](docs/audits/independent_preimplementation_design_audit_20261019.md) with Codex's reviews of PD-010 [revision 2](docs/audits/pd010_revision2_binding_review_20261019.md), [revision 3](docs/audits/pd010_revision3_binding_review_20261019.md) and [revision 4](docs/audits/pd010_revision4_bounded_check_20261019.md); then the [Initial OSA audit](docs/audits/initial_osa_audit.md), then [PD-001 re-audit](docs/audits/osa_reaudit_pd001_20261018.md), then [forward research audit](docs/audits/forward_research_osa_audit_20261018.md); the re-audits after admission, [PD-002](docs/audits/osa_reaudit_pd002_20261018.md), [PD-003](docs/audits/osa_reaudit_pd003_20261018.md), [PD-004](docs/audits/osa_reaudit_pd004_20261019.md), [PD-005](docs/audits/osa_reaudit_pd005_20261019.md), [PD-006](docs/audits/osa_reaudit_pd006_20261019.md), [PD-008](docs/audits/osa_reaudit_pd008_20261019.md), [PD-007](docs/audits/osa_reaudit_pd007_20261019.md) and [PD-009](docs/audits/osa_reaudit_pd009_20261019.md); before `ConstitutionVersion 1`, the independent whole-design audit (conducted separately by the Principal's auditor) against its [checklist](docs/audits/cv1_whole_design_audit_checklist_20261019.md), with the [audit handoff](docs/audits/cv1_audit_handoff_20261019.md); each admitted record's pre-admission audit in `docs/audits/` (for PD-002, [readiness summary](docs/audits/pd002_admission_readiness_20261018.md); for PD-003, [audit](docs/audits/osa_audit_pd003_proposed_20261018.md); for PD-004, [audit](docs/audits/osa_audit_pd004_proposed_20261018.md)); for the proposed ES-1, [PD-005 audit](docs/audits/es1_osa_audit.md); for PD-006, [readiness review and D-10/D-11 sequence](docs/audits/pd006_readiness_review_20261019.md); for PD-007 (D-10, D-11), [audit](docs/audits/osa_audit_pd007_proposed_20261019.md); for PD-008 (D-12, admitted), its [pre-admission audit](docs/audits/osa_audit_pd008_proposed_20261019.md) and the [revocation-ordering comparison](docs/audits/pd008_revocation_ordering_comparison_20261019.md) |
| What to do next, in what order | [Document-first design plan](docs/plans/document_first_design.md); for forward research, [forward research design plan](docs/plans/forward_research_design_plan.md) |
| What the client was told; illustrative methods | `docs/reference/` (client drafts; the ES-1 methods note; not doctrine) |
| Which engineering standards apply and where they came from | [Adoption record](docs/decisions/fin123_core_adoption_20261018.md) |
| Decisions by the Principal | `docs/decisions/` (PD-001 to PD-010 admitted as document-phase admissions; historical records carry dated amendment notes where PD-010 superseded them; genesis not executed; approved admission texts for [PD-002 and PD-003](docs/decisions/admission_text_pd002_pd003_20261018.md) and [PD-005](docs/decisions/admission_text_pd005_20261019.md)) |

Directory jurisdiction:

- `docs/doctrines/` governs. A doctrine states what must be true.
- `docs/decisions/` records Principal admissions and reversals. A decision
  changes standing; a doctrine edit without one does not.
- `docs/audits/` is evidence. An audit authorizes nothing.
- `docs/plans/` proposes order and scope. A plan authorizes work only after
  a decision admits it.
- `docs/reference/` holds external or client-facing material filed for
  comparison. It governs nothing and is corrected to match the doctrine,
  never the reverse.

## Authority rule

Authority is scoped by exact governed fact. Do not infer it from a file
name, directory, recency, implementation behavior, a passing test, a
document's own claim, or an agent's capability. The Principal (the human
owner) is the only authority that can admit the Constitution, grant an
Authorization, change an Evaluation Standard, or authorize a non-zero
Constitutional Delta. An agent working in this repository holds no
authority unless an Authorization in `docs/decisions/` names it.

## Stop conditions

Stop and return the question to the Principal when progress would require
any of the following to be newly established:

- an identity or identity rule for a governed object;
- the owner, commit boundary or representation class of a governed fact;
- the meaning of an Economic Proposition change, an evidentiary class, or a
  resolution source;
- a lifecycle transition or Transition class not in the Constitution;
- an Authorization, budget, or Evaluation Standard;
- any `ΔO`, `ΔS` or `ΔA` other than zero.

Do not resolve a stop by writing code, by choosing a storage or
orchestration technology, by making a cache, branch, agent memory or test
result authoritative, or by picking the newest or most confident document.

## Same-scope conflict

If two documents answer the same question differently: identify the exact
subject; prefer the doctrine over the audit or plan; look for a decision in
`docs/decisions/` that admits one answer; distinguish an admitted answer
from a TENTATIVE one; if still ambiguous, stop.

## Rules for this phase

- No application code, tests, infrastructure, frameworks, dependencies or
  service selection.
- Preserve failed hypotheses, rejected transitions and negative evidence,
  in documents now and in ledgers later.
- Do not claim certification, coherence or admission because a document was
  written.
- Prefer fewer objects with precise meanings.
- Write concisely, in investment-management and systems-engineering
  language.
