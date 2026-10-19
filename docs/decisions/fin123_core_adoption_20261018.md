# Adoption of the fin123-core Engineering Discipline

Status: **ADOPTION RECORD — DOCUMENT-FIRST PHASE. Records what New Speedway
adopts from fin123-core and what it does not. Grants no implementation
authority.**

Date: 2026-10-18

## Source

| Item | Value |
| --- | --- |
| Repository | `~/dev/fin123-core` (IRIS) |
| Commit read | `8175d504998bf682170847119a866d7f5e7df8fd` (2026-10-15) |
| Entry point read | `AGENTS.md` (root router) |

Every path below is relative to the fin123-core root at that commit. The
doctrine was taken from the linked source documents, not from filenames or
from the founding brief's summary.

## Sources read and what each supplies

| Source path | Standing in fin123-core | What New Speedway adopts |
| --- | --- | --- |
| `AGENTS.md` | Current root router | Router shape: jurisdiction, authority rule, progressive disclosure table, stop conditions, same-scope conflict procedure, root-document jurisdiction list |
| `docs/engineering_operating_contract.md` | Current engineering operating contract (effective 2026-08-16, CC amendment 2026-08-18) | The five rules; `Audit -> Plan -> Implement -> Verify` as working functions; the mandatory authority sweep in Audit; the **Constitutional Delta** in Plan with its mandatory Authority Delta; the constitutional stop condition; the architectural budget; anti-metastasis |
| `docs/top_doctrines/iris_constitutional_coherence_doctrine.md` | Current constitution (CC-HD-001..006, 2026-08-18) | Constitutional Coherence (ontological, semantic, authority, developmental); OSA; **Authority Normal Form**; the exact six representation classes `AUTHORITATIVE`, `DERIVED`, `CACHE`, `RECEIPT`, `LEGACY_ONLY`, `EPHEMERAL`; Working/staged as lifecycle standing, not classes; the seven authority invariants; rules for lawful change and migration |
| `docs/top_doctrines/iris_cross_process_operational_continuity_doctrine.md` | Current companion conformance doctrine (2026-08-27) | The exact meaning of **CPOC**: the temporal and process-boundary conformance obligation, subordinate to scoped authority, that proves an already-lawful state survives persistence, process death, reconstruction, continuation and historical verification; its canonical lifecycle; its negative invariants (transient-authority leakage, mutable-present substitution, resurrection, cross-surface disagreement, process-local continuation) |
| `docs/top_contracts/iris_cpoc_certification_contract.md` | Current conformance contract | Qualifying process boundary; boundary authority ledger; decision-surface matrix shape; required negative witnesses; evidence record; standing vocabulary (`OSA PASS/FAIL`, `CPOC PASS/FAIL`, `CERTIFIED`, `IMPLEMENTED NOT CERTIFIED`, `STOPPED`) |
| `docs/decisions/iris_constitutional_coherence_phase_2b_human_adjudication.md` | Admitted human decision record | The form of a human admission record and the rule that documentary admission authorizes documentary work only |
| `docs/decisions/iris_accumulating_analytical_working_decision.md` | Decision record | The compact `ΔO / ΔS / ΔA` Constitutional Delta notation with persistence, writer, selector and representation lines |
| `docs/templates/iris_osa_cpoc_certification_section.md` | Template | The rule that a prose `CERTIFIED` is not certification evidence |
| `docs/top_doctrines/method_forward_evidentiary_doctrine.md` | Controlling top doctrine (2026-07-28, amended 2026-08-12) | Immutability of an admitted explanation; prediction committed before the answer is known and fixed at commitment; outcome evaluates a prediction, never the explanation directly; a successor begins at zero; the two evidentiary classes **Historical Reconstruction** and **Contemporaneous Forward Record**, reported separately and never summed; historical replay integrity |
| `docs/top_doctrines/canonical_explanatory_state_doctrine.md` §Semantic Budget | Top doctrine | The distinction that a semantic budget is not tokens, time or cost |
| `docs/top_doctrines/iris_knowledge_evolution_control_architecture_doctrine.md` | Controlling top doctrine | Only the separation principle: the component that proposes does not admit, the component that admits does not investigate, and provider substitution is a governed event. The four IRIS components themselves are not adopted |
| `docs/audits/iris_constitutional_coherence_authority_topology_audit.md` | Phase 1 audit (evidence) | Audit form: executive disposition, graded thresholds, the governed-fact-to-authority graph |
| `docs/current_work.md`, `docs/CORPUS.md` §1 | Routing and historical | The authority ladder (doctrine governs; audits, reports and changelogs are evidence) |

## Standards that apply to New Speedway

1. **Constitutional Coherence and Authority Normal Form** apply to every
   governed fact New Speedway defines. Duplication of representation is
   permitted; duplication of authority is not.
2. **The six representation classes** are adopted exactly. No seventh class
   is created. Candidate, staged and working remain lifecycle standing.
3. **The engineering motion** `Audit -> Plan -> Implement -> Verify` applies
   prospectively to every change, including changes to these documents.
   During the document-first phase, Implement means editing governed
   documents, and Verify means the adversarial OSA review.
4. **The Constitutional Delta** (`ΔO`, `ΔS`, `ΔA`) is mandatory in every Plan
   and every consequential Transition record. The normal budget is
   `ΔO=0, ΔS=0, ΔA=0`.
5. **The constitutional stop condition** applies: a touched governed fact
   without a determinable owner, authority, commit boundary, historical
   carrier or classification stops the work and returns it to the Principal.
6. **CPOC** keeps its source meaning. It is applied to New Speedway's own
   transitions (allocation, order, evaluation, recovery), is subordinate to
   New Speedway's scoped authorities, and never creates authority. It is not
   used as a portfolio coherence check, a composition check, or a general
   reliability category.
7. **Certification vocabulary**: `CERTIFIED` requires executed OSA and CPOC
   evidence for the exact subject. Nothing in the document-first phase is
   certified; the lawful standing of these documents is `DRAFT — NOT
   ADMITTED`.
8. **Forward-evidentiary rules**: trust is earned, not inherited;
   commitments precede outcomes; the two evidentiary classes are never
   merged.
9. **Anti-metastasis**: no subordinate process doctrine, generation scheme or
   certification ontology is created for New Speedway. Amend the governing
   documents directly.

## Not adopted

- IRIS product ontology: Model, Version, Branch, Working, W1, Method, R3/R4,
  Run, Result, Formula, Application, Workspace, Repository, Publication, PM.
- IRIS state ownership and the G1 semantic-authority register rows.
- IRIS deployment, release and certification runner machinery, the AAPL
  reference witness, Excel and Render procedures.
- The four-component IRIS/SBCLEMG/Provider/Analyst architecture as a product
  design. Its separation-of-roles principle is adopted; its objects are not.
- Any claim of implementation conformance that fin123-core makes about
  itself.

## Constitutional Delta of this adoption

```text
ΔO: NONE for fin123-core. New Speedway defines its own ontology in
    docs/doctrines/new_speedway_constitution.md.
ΔS: NONE for fin123-core terms. CPOC, OSA, Authority Normal Form and the
    representation classes keep their source meaning.
ΔA: NONE. This record grants no authority. The New Speedway Principal
    (the human owner) is the only authority that can admit the constitution.
```
