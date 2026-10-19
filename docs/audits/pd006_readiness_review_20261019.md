# PD-006 Admission-Readiness Review and the D-10/D-11 Sequence

Status: **AUDIT — EVIDENCE, NOT DOCTRINE. Authorizes nothing. Admits
nothing.**

As-of: 2026-10-19. Subject:
[PD-006, proposed](../decisions/principal_decision_006_replaceable_tools_and_first_prototype.md),
read against Constitution revision 5, PD-001 to PD-004 (admitted),
PD-005 (proposed, revision 3), the initial audit's D-10 and D-11, PD-002.3
(N-1) and the adopted OSA/CPOC rules. Governing engineering principle as
the Principal stated it: **build what makes New Speedway different;
reuse or simulate everything else.**

## 1. The four decisions in PD-006 §PD-006.4

| # | Decision, verbatim subject | Alternatives | Consequences | Delta | Recommendation |
| --- | --- | --- | --- | --- | --- |
| 1 | Admit principle 10 in Part IX ("Tools are replaceable") and the adoption-record standard | (a) Admit as drafted. (b) Keep it in the plan only, not the Constitution. (c) Strengthen to name tool classes in Part VII | (a) The burden of proof for custom components becomes constitutional and binds the implementation plan. (b) Weaker: a plan rule is advisory and could be waived by a later plan. (c) Over-specifies; Part VII already classes the carriers that matter (market data store `CACHE`, backtest outputs `EPHEMERAL`) | `ΔO` 0; `ΔS` one Part IX principle and one adoption-record standard; `ΔA` 0 | **(a).** It restates I-6, I-13 and Part VII for architecture and adds only a preference order and a burden of proof. No OSA concern |
| 2 | Adopt the first-prototype target in plan step 9 | (a) Adopt with the two demonstrations of §PD-006.3. (b) Keep step 9 as the full responsibility graph before any prototype. (c) Prototype the execution path first | (a) Step 9's first deliverable becomes the fact-to-authority map for the loop the proofs touch, and the component list with the OSA requirement each satisfies. (b) Delays any demonstration until every object is mapped. (c) Demonstrates the part least different from existing systems | Plan change only; `0/0/0` | **(a).** One concern, stated in §2: a prototype target is not implementation authorization |
| 3 | Decide every registration by hand in the first prototype, or draft D-11 first | (a) Draft D-11 first: delegated admission of routine Hypothesis registrations and successor research motions under fixed budgets and independent Checks. (b) The Principal decides each. (c) Delegate everything short of constitutional change | (a) Autonomous research inside approved limits, which is the stated goal; every policy decision attributable to the policy's admission. (b) Ten agents stall on one human; the proof demonstrates a bottleneck. (c) Capital, Standards, Authorizations and Theme funding leave the Principal's hands, contrary to the direction | D-11 is `ΔA` by construction: a decision right moves from the Principal to an admitted policy for named classes | **(a)**, with the reservation list of §3 |
| 4 | Admit `ConstitutionVersion 1` before the prototype, or authorize a bounded prototype against revision 5 | (a) Admit CV-1 after PD-005, D-10/D-11 and N-1, then authorize the narrow implementation. (b) Authorize a bounded demonstration against the draft now, with its own declared delta. (c) Prototype without either | (a) The demonstration runs under an admitted Constitution and can carry conformance claims later. (b) Lawful as an experiment if the authorization says the draft governs it and nothing it produces has standing; cannot carry conformance claims; must be re-run under CV-1 for any. (c) Violates `AGENTS.md` and plan rule 1 | (a) `0/0/0` for the prototype against CV-1. (b) `0/0/0` against the draft, plus one Principal authorization | **(a)** as the path, **(b)** as the fallback only if the sequence in §4 stalls. A zero delta is not implementation authorization in either case |

### OSA concerns raised by PD-006 as a whole

- **A zero Constitutional Delta is not implementation authorization.** PD-006 proposes a plan target; code requires a separate authorization naming the subject, the components, the draft or version it runs under, and the standing of everything it produces (none, for a demonstration). The record should say this in its own text when revised for admission.
- **Synthetic data and sequential reveal.** The record now states both rules (§PD-006.3). The Checker contract from D-10 must make "authored knowing the period" a Check finding, or the proofs will drift toward calling sequential replay prospective.
- **Backtester outputs as Research Record content.** A run's closure must name the data store read, its as-of and the parameters, or the family reconciliation `ES-1` R-4 requires cannot be computed. This is Research Record content already (§III.5), not a new field.
- **No new object was needed.** PD-006 adds no object and the proofs use only existing kinds. The review found no defect that would justify expanding the model.

## 2. What the two proofs must demonstrate

Stated in full in PD-006 §PD-006.3. In one line each: Proof 1 shows
the governed loop (lineage memory, budgets, negative evidence,
independent Checks, succession at zero, cumulative replacement of
contradicted Hypotheses) with every backtest labelled Historical
Reconstruction and no standing earned. Proof 2 shows question
generation from a synthetic development (screens, hops, motivation
closure, competing Hypotheses under one `EXPERIMENT DESIGN`, an
`INCUBATING` Strategy at zero, a `SELECTION` record choosing the next
question) with formation evidence disjoint from resolution and no
forward record claimed. Neither needs the Runner, Decisions, the Paper
Book or PD-004's expiry rules.

## 3. Reuse instead of build

| Capability | Reuse or simulate | Why no OSA requirement forces a build |
| --- | --- | --- |
| Backtesting and historical replay | One existing backtester, any | Its outputs are `EPHEMERAL` until committed as Research Record content; the closure and class are recorded by the committer, not computed by the tool |
| Market and synthetic data | A market data store as `CACHE`; a synthetic generator as a declared source under an Observation Authorization for Proof 2 | The Observation function commits what it retrieves; the generator establishes nothing |
| Paper fills and stress simulation | Not needed for Proofs 1 and 2; when needed, any simulator under the Execution function's fill rule | PD-004.15: simulated fills are proposals the boundary admits; the simulator owns nothing |
| Agents | Hosted model providers | Provenance on the Agent Design Version (PD-002.6); never authority; substitution is a governed event |
| Storage of the three ledgers | Any append-only store that gives a total order and refuses duplicates | The OSA requirement is one commit boundary per ledger with sequence, idempotency and refusal; that is a property to verify, not a reason to build |
| Scheduling, queues, process supervision | Any | CPOC requires continuation from ledgers alone; no scheduler state is authoritative |

What is built because nothing else supplies it: the commit boundaries
with their admission rules (Evidence commit with witness marks and
caller restriction; Apply with base-version refusal and pinning; the
Paper Book boundary later), the Check record form, and the derived
views the doctrine names (lineage memory, family, selection history).
Each is justified by a named requirement in Parts III to V.

## 4. The design sequence, reconciled against the documents

| Step | Principal's order | Actual standing | Reconciled |
| --- | --- | --- | --- |
| 1 | Complete PD-005's cost clarification and admission | The clarification is applied (PD-005 revision 3); admission is a Constitutional Transition proposed by the Principal | Decide PD-005 |
| 2 | Review and decide PD-006 | This review | Decide the four questions |
| 3 | Design D-10 and D-11 together | Both open since the initial audit; D-10 now also carries U-10 (Outcome committer), UD-4 (Checker extraction) and FR-4's Check contract; `ES-1`'s cost verification and family reconciliation are Check content that D-10's contract must hold | §5 below |
| 4 | Resolve N-1 and remaining bootstrap authority | PD-002.3 names the candidate: Apply sequence 0 is the Constitutional Transition admitting CV-1, decided by the Principal with the Checker requirement waived for sequence 0 only; sequences 1 onward are the first Authorizations. D-17 (death between Decide and Apply) and D-12 (reservation) are the other step-4 items; D-12 bears on Proof 1's budgets | After D-10/D-11, because the first Authorizations granted at genesis must name the Checker class and any policy |
| 5 | Admit CV-1 after its independent audit | Plan steps 6 to 9 remain; steps 6 (loops) and 7 (paper controls) are largely written by PD-002 to PD-004 and `ES-1`; step 8 (CPOC journey) and step 9 (responsibility graph) are not | An independent audit of the whole draft, then admission; steps 8 and 9 can be bounded to the two proofs' scope for CV-1 and widened later by Constitutional Transition |
| 6 | Design and authorize the narrow prototype | A separate implementation plan with its own delta and an explicit authorization | Only after 5, or under the §1 decision 4 fallback |

The distinction the Principal drew holds throughout: a bounded
demonstration may run under the draft by explicit authorization and
produces nothing with standing; a constitutionally admitted system runs
under CV-1 and may carry conformance claims after executed OSA and CPOC
evidence. Neither follows from a zero delta.

## 5. D-10 and D-11: the smallest decisions, documentation only

No governing rule is drafted here; this is the list and its order.

| # | Decision | Depends on | Owner |
| --- | --- | --- | --- |
| D-10.a | Independence sufficiency: whether a consequential Check by an agent requires a different model provider from the proposer's, or a Checker-only lineage that never proposes, or a human | None | Principal |
| D-10.b | The Check record contract: what every Check observes and records (the boundary-ledger form adopted from fin123-core), including the `ES-1` items (class, `N_eff` method sequence, family reconciliation, cost evidence, stress floor, `a*`), FR-4's restatement finding, and "authored knowing the period" | D-10.a | Principal; drafted as a Part V and §III.8 change |
| D-10.c | Who may reproduce a Decision and who may commit an Outcome (U-10): Checker Authorization only, or a function on a "resolution set complete" trigger | D-10.a | Principal |
| D-10.d | Checker extraction (UD-4): deferred unless Proof 2 needs document resolution, which it does not | D-10.b | Principal, later |
| D-11.a | The policy classes admitted first: Hypothesis registration within an active Theme's budget and the proposer's scopes; successor research motions (Research Record kinds, `SELECTION`, `EXPERIMENT DESIGN`) within budget; successor Agent Design registration without any Authorization change | D-10.a, D-10.b (a policy decides only on a Check that passed) | Principal |
| D-11.b | The reservation list, fixed: constitutional change, Authorization grant or amendment, Evaluation Standards, Theme registration and funding outside an existing grant, every Allocation, every retirement of a Strategy Version | None | Principal |
| D-11.c | Attribution and revocation: every policy decision records the policy's admitting Transition; the Principal may suspend a policy by a Transition, after which its class reverts to the Principal; a policy decision against a failed Check is impossible by construction | D-11.a | Principal |
| D-11.d | Policy evidence: what a class must have shown before it is delegated (for the first prototype, nothing but the Check contract; later, a record of Principal decisions agreeing with Checks) | D-11.a | Principal |
| D-12 | Reservation of research budget at proposal, which Proof 1's ten agents will hit | D-11.a | Principal, plan step 4 |

Delta of the pair, in advance: D-10 is `ΔS` (independence definition,
Check content) and possibly `ΔA` if reproduction or Outcome commit
moves to a function; D-11 is `ΔA` by construction and is the first
"admitted policy" the Constitution's empty slot was reserved for.

## 6. The next decision needed

Decide PD-005 (the Constitutional Transition admitting `ES-1.0`), then
the four PD-006 questions in §1. The first drafting work after that is
D-10.a and D-11.a together, because every other item in §5 depends on
one of them.
