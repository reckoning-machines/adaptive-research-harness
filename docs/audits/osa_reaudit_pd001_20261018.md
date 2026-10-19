# OSA Re-audit after Principal Decision Record 001

Status: **AUDIT — EVIDENCE, NOT DOCTRINE. Authorizes nothing.**

As-of: 2026-10-18, revision 2 of the
[Constitution](../doctrines/new_speedway_constitution.md), after
[PD-001](../decisions/principal_decision_001_identity_and_evidence.md) was
admitted with clarifications.

Scope, as directed: historical authority, evidence timing, duplicate
ownership, and consistency between the two worked cases (T-A forward
research, T-B traditional). Not in scope: the other defects of the
[initial audit](initial_osa_audit.md), which keep their standing there.

Reconciliation standard: each change is checked against the fin123-core
doctrine adopted at `8175d504`: Authority Normal Form (one canonical
authority and one governed commit boundary per governed fact; alternative
representations classified and without decision rights), the temporal and
binding closure invariant (historical truth from immutable history and
contemporaneous bindings, never mutable present), and the forward
evidentiary rules (commitment before the answer is known, two classes never
merged).

## Executive disposition

**B — BOUNDED GAPS, NARROWER THAN BEFORE.**

PD-001 removed the competing-authority language for state, gave economic
identity a checkable boundary, and replaced a sequence-number ordering with
an evidence-based clock. Four clarity defects introduced or exposed by the
revision were repaired in the same pass. Five new questions are open, two of
them consequential (N-3, N-5). D-02, D-03, D-05, D-07 and D-08 are closed.

## Doctrine changes made in revision 2

| Area | Change | Reconciled against |
| --- | --- | --- |
| Authority of state | New defined term **Applied History**: the applied subsequence of the one Transition ledger, `AUTHORITATIVE` for membership, standing, allocation, limits, capital consumption, currentness and pinned versions. **Population State** is a `DERIVED` projection with no authority. Every "Population State fact" phrase in Parts III to V replaced. | ANF singular authority; representation closure |
| Pinning | Each applied Transition records `ConstitutionVersion` and `EvaluationStandardVersion` at Apply; Check events record the versions they ran under; projection and replay use pinned versions; a later Constitution governs only later Transitions. I-11 extended. | Temporal and binding closure; CPOC mutable-present substitution |
| Economic identity | Five immutable boundaries (mechanism, prediction target, market or domain, horizon, payoff). `NONE` lawful only with all five unchanged **and** equivalence independently established by the Checker from the rule change. New bullet: lineage never automatically transfers evidence, fitness or capital authority. | Forward evidentiary doctrine §4 (a regenerated explanation is a different Method); ANF |
| Evidence clock | Three times with three authorities. Availability needs independent evidence (earliest Market Observation retrieval, pre-commitment absence); a schedule informs but cannot establish. Prospective only on demonstrated precedence; otherwise Historical Reconstruction with reason. Straddling windows are Historical in full. Print declared; restatements are new Market Observations. I-2 and I-3 rewritten. | Forward evidentiary doctrine §5, §9, §9.1 |
| Evidence records | Prediction gains commitment time; Outcome gains outcome availability time and binds exactly one Market Observation; Market Observation gains print and retrieval time. | RECEIPT classification |
| Budget ownership | Capital and allocation consumption owned by the Applied History at admission; research resource consumption owned by Research Records at execution; remaining of either kind `DERIVED`. | ANF; Principal direction on D-12 |
| Constitution text | Owned by the Transition ledger as the proposal content of the Constitutional Transition, like all proposed content; currentness by the Applied History. | ANF; one pattern for all proposed content |
| Evaluations | A consequential Transition may cite only an Evaluation under the Standard in force at its base; Checker verifies. | I-7; temporal closure |
| Worked cases | T-A is now the forward case with explicit times and the counterfactual that would make it Historical. T-B is now the traditional momentum case with the five boundaries and a `NEW` contrast. Both record pinned versions at Apply. | Two-case rule |
| Diagrams | Governance diagram ledger node renamed to Applied History with Population State as `DERIVED`; sequence diagram participant renamed; note rephrased as projection. | Consistency with Part III |

## Repairs made during this re-audit

| Ref | Check | Finding | Repair |
| --- | --- | --- | --- |
| R-9 | Duplicate ownership | Research budget consumption was carried both in Research Records (Evidence) and in the Applied History projection. Two carriers for one fact. | Applied History owns capital and allocation consumption; Research Records own research resource consumption. §III.6, §III.7. |
| R-10 | Duplicate ownership | "Admitted Constitution text" was named as its own authority, a second ownership pattern beside the Transition ledger that owns every other proposed content. | Constitution text is the Constitutional Transition's proposal content on the Transition ledger. Summary table, §III.9. |
| R-11 | Historical authority | Check events had no pinned versions, so a rejected Transition could not later show which Constitution rejected it. | Record form field 6 pins both versions at Check. §III.8. |
| R-12 | Historical authority | A Transition could cite an Evaluation under any Standard version, letting a stale or future standard inform admission. | Only the Standard in force at base may be cited; Checker verifies. §III.6. |

## New open questions

### N-1. Genesis — OPEN (Historical authority)

Pinning requires a Constitution in force at every Apply, including the
first. The draft has no genesis Transition. Example: Transition 1 registers
a Theme; what `ConstitutionVersion` does it pin? Candidate: Apply sequence 0
is a Constitutional Transition admitting `ConstitutionVersion 1` with the
Principal as proposer, checker-less by explicit exception recorded in the
Constitution itself. Deciding authority: Principal, plan step 4.

### N-2. One pin or two — OPEN (Historical authority, identity)

Evaluation Standards are constitutional (§III.9) yet pinned separately from
`ConstitutionVersion`. If a Standard version is a component of a
Constitution version, pinning both is redundant and the two pins can
disagree. Example: a Transition pinned `CV-2, ES-1` while `CV-2` contains
`ES-2`. Candidate: pin `ConstitutionVersion` only, and define each Standard
version as a named component of exactly one or more Constitution versions.
The Principal's clarification names both; this question is about carrier,
not meaning. Deciding authority: Principal, plan step 4.

### N-3. Independence of availability evidence — OPEN, CONSEQUENTIAL (Evidence timing, authority)

Availability is established by the earliest Market Observation retrieval.
If the proposing agent controls when retrieval happens, it can delay
retrieval, read the value elsewhere, commit a Prediction, and still show
"no value present" before commitment. Example: source S publishes at
18:00; the agent reads S's website at 18:05, commits at 18:10, and the
system's scheduled retrieval records 18:40. Precedence appears
demonstrated and is false. Candidate repair: Market Observation retrieval
runs only under an Observation Authorization that no proposer holds, on a
schedule the proposer cannot alter, and the retrieval schedule itself is an
Applied History fact. This is an authority design question and belongs to
plan step 3, but it bounds what D-08 can promise until then. Deciding
authority: Principal.

### N-4. Knowable through other channels — OPEN (Semantics)

I-2 classifies by availability of the resolving value from the declared
source. A value may be inferable earlier from undeclared channels (prices
during the session, a competing data vendor, news). The forward case is
most exposed: dealer gamma estimates can be approximated from public
open-interest data before S publishes. The narrow reading, that
"prospective" means committed before the resolving print was available, is
honest and checkable; the broad reading, committed before anything
informative existed, is not checkable. Recommend the narrow reading with the
limitation stated in the Evaluation Standard. Deciding authority:
Principal, plan step 2 close-out.

### N-5. What a Strategy Version predicts — OPEN, CONSEQUENTIAL (Two-case consistency, duplicate ownership)

The Evidence model binds Predictions to a `StrategyVersionId`, but T-B's
forward record is implicitly its paper performance, which lives in the
Paper Book and Market Observations, not in Predictions and Outcomes. Two
possible carriers of a Strategy's forward record, neither declared. In T-A
the Hypothesis record is clear; in T-B the Strategy record is not, so the
two cases are not yet consistent. Candidate: each rebalance emits a
Prediction (target positions at a commitment time) as an Evidence commit,
Outcomes resolve them against declared closes, and paper P&L from the Paper
Book is a `DERIVED` reconciliation of the same facts. Deciding authority:
Principal, plan step 2 close-out.

### N-6. Boundary granularity — OPEN (Semantics)

T-B's boundaries are stated at a level ("cross-sectional momentum") that
makes a 12-1 to 6-1 change `NONE`. A proposer who writes boundaries coarsely
maximizes `NONE`. The Checker at proposition registration must accept the
boundaries as specific enough, and nothing yet says what "specific enough"
is. Candidate: the Evaluation Standard sets minimum specificity per
boundary. Deciding authority: Principal, plan step 5.

## Standing changes to the initial register

| Defect | Standing | Reference |
| --- | --- | --- |
| D-02 | CLOSED | PD-003: straddling windows Historical in full |
| D-03 | CLOSED | PD-002: five boundaries, independent equivalence |
| D-05 | CLOSED | PD-003: declared print, restatements as new observations |
| D-07 | CLOSED | PD-001: Applied History authoritative, projection derived, pinning |
| D-08 | CLOSED, bounded by N-3 and N-4 | PD-003 |
| D-06 | OPEN, recommendation changed | With "lineage never automatically transfers evidence, fitness or capital authority" admitted, the continuity-claim mechanism has no lawful use. Recommend closing D-06 by removing it at the next decision |
| D-12 | OPEN, direction recorded | Execution-time research consumption versus admission-time capital consumption; mechanism deferred |
| D-10, D-11, D-17 | OPEN, direction recorded | Not admitted dispositions |

Constraint recorded from the Principal: forward-research origin is not a
disqualifying risk category. The earlier suggestion of a cap on capital in
forward-only Strategies is withdrawn. Uncertain Strategies are governed by
evidence, uncertainty and portfolio risk under the Evaluation Standard and
limits.

## Remaining contradictions

None found between sections of revision 2 on the four audited subjects.
The open questions above are gaps, not contradictions: each is a place
where the doctrine is silent, not two places where it disagrees.

## Next design decision

**N-5**, what a Strategy Version predicts and where its forward record
lives. It decides whether the traditional case and the forward case share
one evidence model, and it determines what the Paper Book is evidence of.
Until it is decided, T-B cannot be rerun under the evidence clock, and
plan step 2 cannot close. N-3 should be decided with it because both fix
what "independently established" means for a Strategy.
