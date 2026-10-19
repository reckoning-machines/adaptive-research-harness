# Document-First Design Plan

Status: **PROPOSED PLAN — DOCUMENTATION ONLY. Authorizes no code, tests,
infrastructure, frameworks, dependencies or service selection.**

Date: 2026-10-18

Governs: the order in which the New Speedway design is completed in
documents, from the
[constitution draft](../doctrines/new_speedway_constitution.md) and the
[initial OSA audit](../audits/initial_osa_audit.md).

## Motion

Each step runs `Audit -> Design -> Challenge -> Repair -> Re-audit` on its
subject. Implement means editing the governing documents; Verify means an
adversarial OSA review recorded as an audit. A step is complete when its
exit criterion holds and every defect it owns is either repaired or
explicitly deferred by the Principal with a reason.

The constitutional budget for every step is declared below. Because the
Constitution is not yet admitted, each step's `ΔO/ΔS/ΔA` is relative to the
draft, and all of it is admitted only when the Principal admits
`ConstitutionVersion 1` at the end.

## Steps

### 1. Governed objects and identity

- Resolves: D-01 (Theme revision), D-09 (Paper Book), D-14 (provider in
  Agent Design identity).
- Produces: amended Part III with every identity rule stated, including
  what is in each content hash.
- Exit: every object has one identity rule, one immutability rule, and a
  worked example of succession.
- Budget: `ΔO` may be non-zero (object list may shrink or the Paper Book
  may be removed); `ΔS=0`, `ΔA=0`.

### 2. Relationships, lineage and evidence

- Resolves: D-02 (straddling windows), D-03 (proposition invariants), D-05
  (source revision), D-06 (continuity claims), D-08 (the clock).
- Produces: the Economic Proposition invariant list; the resolution-source
  declaration (schedule, first-print or final); the class-determination
  rule; a decision on whether continuity claims exist.
- Exit: for any Prediction, a reader can determine its class and its
  resolution rule from the records alone, without the proposer's label.
- Budget: `ΔS` non-zero within the draft; `ΔO=0` unless a Resolution Source
  becomes a governed object; `ΔA=0`.

### 3. Authority and change budgets

- Resolves: the Authorization content schema; the exact meaning of each
  budget kind; what a Research Authorization may forbid (for example,
  repeating closed questions).
- Produces: Part II budget table and §III.7 completed; the first draft
  Authorization for a Research Agent and a Checker, as worked examples.
- Exit: every Transition class names who may propose, check and decide,
  and the Authorization that permits each, with no "any authorized" left.
- Budget: `ΔA` non-zero within the draft (this step is where the authority
  map is finished); `ΔO=0`, `ΔS=0`.

### 4. State transitions and concurrency

- Resolves: D-07 (sequence vs state authority), D-12 (reservation), D-17
  (interruption between Decide and Apply).
- Produces: the Transition lifecycle as commit events; the replay rule
  (which Constitution version interprets each historical Transition); the
  base-version and composition rules as a decision table; a reservation
  decision.
- Exit: every one of the twelve challenges has a transition-level trace
  that a reader can follow from ledgers alone; T-D and the Decide/Apply
  interruption are written as before/after records.
- Budget: `ΔO` possibly non-zero (a Reservation object); `ΔA` non-zero if
  the authority of history moves; `ΔS=0`.

### 5. Independent evaluation and certification

- Resolves: D-10 (Checker independence), D-11 (admitted policy).
- Produces: the Checker contract (what a check must observe and record,
  mirroring the fin123-core boundary authority ledger); the first candidate
  policy class and the evidence it needs; the standing vocabulary New
  Speedway uses (`OSA PASS/FAIL`, `CPOC PASS/FAIL`, `CERTIFIED`,
  `IMPLEMENTED NOT CERTIFIED`, `STOPPED`) applied to Transitions.
- Exit: a consequential Transition record template exists and the three
  worked transitions T-A to T-C are rewritten against it.
- Budget: `ΔA` non-zero if policy admission is introduced; otherwise
  `0/0/0`.

### 6. Research and investment learning loops

- Produces: the loop as a sequence of Transition classes, with heterogeneous
  triggers (new Market Observation, Outcome resolution, Evaluation change,
  Principal challenge, scheduled review) and one invariant process; the
  forward-research path (Theme with no history) and the empirical-discovery
  path (Strategy with no Hypothesis) traced end to end; what "learned"
  means as a ledger fact.
- Exit: both paths reach a retired Strategy with preserved negative
  evidence, with every step a Transition in Part V.
- Budget: `0/0/0` expected.

### 7. Paper portfolio and human controls

- Produces: the Paper Book contract (order, fill, position derivation,
  target-versus-position reporting); the Principal's controls (limits,
  kill, revoke, freeze) as Transition classes; what the Principal sees and
  must decide daily.
- Exit: every control is a Transition with a record form; nothing is a
  side channel.
- Budget: `ΔO` non-zero if a control needs a new object; `ΔA=0`.

### 8. Recovery, replay and CPOC applicability

- Produces: the CPOC applicability classification for each Transition
  class; the canonical New Speedway continuity journey (register, predict,
  resolve, allocate, process death, order, process death, evaluate, retire,
  process death, historical read) as a witness specification; the negative
  witnesses (resurrection, stale materialization, duplicate order, stale
  base after restart).
- Exit: the journey is written in the fin123-core contract form (boundary
  ledger, decision-surface matrix, negative witnesses, evidence record)
  without naming any implementation.
- Budget: `0/0/0`. CPOC creates no authority.

### 9. Architecture derived from the completed state model

- Produces: the responsibility graph: which function owns each commit
  boundary, which are derived readers, where the agents run, what crosses
  which boundary. Still no technology selection.
- Exit: every governed fact in the constitution maps to exactly one
  authority, one commit boundary, and classified alternative carriers; the
  map is checked against the twelve challenges.
- Budget: `0/0/0`. Architecture may not change meaning.

Only after step 9 and the Principal's admission of `ConstitutionVersion 1`
does an implementation plan become proposable. That plan will be a separate
document with its own Constitutional Delta.

## Rules for every step

- No application code, tests, infrastructure, frameworks, dependencies or
  service selection.
- No database or orchestration design before step 9, and none then beyond
  the responsibility graph.
- Nothing becomes authoritative by being written down; standing comes only
  from the Principal's admission.
- Preserve failed designs: a rejected alternative stays in the audit with
  its reason.
- Prefer fewer objects. A step that adds an object must show the fact that
  would otherwise have no owner.
- Write in investment-management and systems-engineering language.
- Every major schema decision is tested against at least two cases: a
  traditional price and volume research experiment, and a forward-research
  Theme that generates new Hypotheses and Strategies. Coherence is not
  usefulness; a document can be consistent and describe the wrong system.

## Recommended next step

Principal direction of 2026-10-18 is recorded in
[decision record 001](../decisions/principal_decision_001_identity_and_evidence.md)
(admitted 2026-10-18 with clarifications). The Constitution was revised
and re-audited in
[the PD-001 re-audit](../audits/osa_reaudit_pd001_20261018.md). Next
decision: N-5 (what a Strategy Version predicts) with N-3, to close step 2.
That decision is drafted as
[decision record 002](../decisions/principal_decision_002_predictions_decisions_observation.md)
(PROPOSED FOR ADMISSION, revision 4 after Principal review, 2026-10-18;
not admitted; Constitution not yet revised by it). PD-002 and PD-003
(dispositions 1 to 5) were admitted 2026-10-18 and applied as Constitution
revisions 3 and 4, each re-audited. PD-004 (capital standings, exploratory
expiry, the bracketing contract, Fill Confirmation, recovery) was
admitted 2026-10-19 with the internal-simulator clarification and
applied as Constitution revision 5, re-audited. `ES-1` is drafted as
[decision record 005](../decisions/principal_decision_005_es1_evaluation_standard.md)
(PROPOSED, 2026-10-19; audit `docs/audits/es1_osa_audit.md`), resolving
U-6, FR-6, FR-8, FR-9, UD-11 and UD-12 if admitted by Constitutional
Transition. PD-005 (`ES-1.0`, now Part X) and PD-006 were admitted 2026-10-19 as
document-phase admissions and applied as revisions 6 and 7, each
re-audited. PD-008 (D-12: `RESERVATION`, attempts, settlement, the `FENCE` funding
stop) was admitted 2026-10-19 and applied as revision 8, re-audited.
PD-007 (D-10, D-11: independent checking; policy `P-1`) was admitted
2026-10-19 and applied as revision 9, re-audited. PD-009 (genesis content, D-17, D-06 removal) was admitted 2026-10-19
and applied as revision 10. The independent whole-design audit against
[the checklist](../audits/cv1_whole_design_audit_checklist_20261019.md)
is conducted separately by the Principal's auditor from the
[audit handoff](../audits/cv1_audit_handoff_20261019.md); its findings
and the Principal's decisions on them precede any admission of
`ConstitutionVersion 1`. Genesis is not executed; no code
is authorized. Implementation
planning, when it comes, evaluates existing agent runtimes and workflow
engines against one concrete budget, interruption, revocation, retry and
evidence-admission sequence (Principal direction, 2026-10-19); framework
selection is deferred. Step 9's first prototype
target is PD-006 §PD-006.3; it authorizes no code. The Principal's direction of 2026-10-19
(replaceable tools; a first prototype of ten agents replacing
Hypotheses through one simple backtester) is drafted as
[decision record 006](../decisions/principal_decision_006_replaceable_tools_and_first_prototype.md)
(PROPOSED, with the two demonstrations in its §PD-006.3) and, if
admitted, gives step 9 a first prototype target and makes D-11 the
gating decision for it. The reconciled sequence and the smallest D-10
and D-11 decisions are in
[the PD-006 readiness review](../audits/pd006_readiness_review_20261019.md).

Earlier recommendation, superseded by that record:
Step 1 and step 2 together, because D-03, D-07 and D-08 are the three
decisions on which steps 4 and 5 depend, and D-03 and D-08 belong to step 2
while D-07 belongs to step 4 but must be decided earlier. The concrete
deliverable is a Principal decision record admitting or reversing the eight
tentative choices in the audit, followed by a constitution revision and a
re-audit.
