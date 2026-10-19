# Independent Pre-implementation Design Audit — New Speedway

Status: **AUDIT — EVIDENCE, NOT DOCTRINE. OSA FAIL for the reviewed
revision. Authorizes no repair or implementation. No certification.**

Date: 2026-10-19. Auditor: Codex, independently reviewing the design
authored by Claude. This review used no subordinate agents.

## Disposition and baseline

**Not ready to freeze.** Revision 10 expresses a sound separation of
research, investment evidence and decision authority, but does not yet
form a coherent executable specification. The first ordinary Check has
unsatisfied funding and record requirements. Budget accounting, admission
across ledgers, evidence resolution and paper execution also have concrete
failed transitions. Removing the TENTATIVE markers did not remove these
defects.

| Baseline | Verified |
| --- | --- |
| Branch | `main` |
| Design commit | `2f24eb2cdf3e3da82f72b023631f8f925cb9670a` |
| HEAD / handoff commit | `895f953aca14e440c1593db8f0f7088da0556cb2` |
| Difference between the commits | Only `docs/audits/cv1_audit_handoff_20261019.md` added; governing design unchanged |
| Constitution | Revision 10, draft, not admitted as `ConstitutionVersion 1` |
| Working tree at entry | Clean; no unrelated changes to preserve |
| Operating standing | Document-phase admissions only; no genesis, selected runtime, implementation or executed CPOC witness |

The repository's `AGENTS.md` was read first. The Constitution, admitted
decision provisions and PD-009 genesis specification were read before
using the handoff, checklist or previous audit conclusions. Admission
clarifications and exclusions were distinguished from historical proposal
text. The adopted ANF and CPOC doctrines and relevant forward-evidence
rules were also checked at fin123-core commit `8175d504`. Earlier audit
grades supply no premise of this report.

The scope is the existing [whole-design checklist](cv1_whole_design_audit_checklist_20261019.md),
including its two research paths and recovery cases. Its references to
revision 9, proposed PD-009 and outstanding D-06 are historical; this
review uses revision 10. These are document traces, not executed tests.

References below use **C** for the
[Constitution](../doctrines/new_speedway_constitution.md). PD references
identify the numbered decision record and exact section. All proposed
repairs remain proposals. The audit itself changes no ontology, meaning,
authority or governing text: `ΔO/ΔS/ΔA = 0/0/0`.

## Authority and investment meaning

The intended authority map is economical and largely explicit. The
following distinctions survive independent inspection; the findings
below identify where their operating contracts do not.

| Governed fact | Owner and boundary | Denied alternative authority / qualification |
| --- | --- | --- |
| Proposed Theme, Hypothesis, Strategy and Agent Design content | Transition ledger, Propose | Candidate content establishes only what was proposed |
| Membership, standing, allocation, limits and current versions | Applied History, Apply | Population State and rankings are derived; B-2, B-4 and B-10 affect admission |
| Grant, scope, grantee, expiry and tool permissions | Principal's Authorization content, Authorization Transition | An Agent Design, lineage or provider grants nothing; B-1 affects Checker consumption |
| Reservations, attempts, settlements and funding stop | Evidence ledger, Evidence commit | Research plans, invoices before recording and runtime checkpoints have no vote; B-3 affects arithmetic |
| Source meaning, revision and retrieval plan | Observation Authorization, Authorization Transition | Vendor endpoints and retrieval caches do not choose source meaning |
| Retrieved values, bytes and witnessed receipt | Evidence ledger, Observation-only commit | Source publication times are receipt content, not independent time authority |
| Prediction and resolution | Evidence ledger, authorized commits | Hypothesis standing changes only at Apply; B-5 affects completion and unique resolution |
| Strategy output for an event | Evidence ledger, Runner-only commit | Neither the Research Agent nor backtester commits a Decision; one Decision per event |
| Independent Check | Transition lifecycle, Check boundary | Immutable record under pinned criteria; C-7 and B-7 address independence and evidence closure |
| Reproduction records and standing | Checker-only Evidence commit; standing derived from records | Runner cannot certify itself; disputed results go to the Principal |
| Evaluation and methods governing a window | Evaluation derived; commitments on registration or Evidence records | No score allocates capital; B-6 affects temporal binding |
| Orders, fills and confirmations | Paper Book, Execution-only commits | Targets and positions remain separate; B-8 and B-9 affect expiry safety |
| Constitution text and currentness | Constitutional proposal content; currentness at Apply | A repository copy cannot independently select the governing version |

Hypotheses compete through their own Predictions and Outcomes; Strategy
Versions through their own forward decision-implied records; Agent
Designs through research contribution. Profit does not validate a causal
explanation. Economic-proposition equivalence requires unchanged meaning
boundaries and an independent finding, not just a proposer label.
Succession preserves rejected work and family history while starting
performance credit at zero. These distinctions are substantive, not
merely vocabulary.

Historical reconstruction and synthetic observations cannot establish
prospective contradiction, fitness or alpha. Exploratory simulator fills
measure operational behavior and simulator-relative shortfall, not
achievable execution costs. ES-1's floors are operational, not power
claims. Search-family reconciliation, precommitted methods, conservative
cost scenarios and instrument-class stress floors bound claims without
pretending to eliminate selection bias or unknown tails.

## Blocking findings

“Blocking” means that a transition the design permits or requires cannot
be completed unambiguously under its own rules. The recommended repairs
use existing records and boundaries; none requires a new service or
governed object.

### B-1 — Critical: the Checker has a grant but no complete funding path

**Location:** C §III.5 “Research budget reservation, attempts, settlement
and the funding stop”; §III.7 Content, Budget ownership and Authority;
Part V reservation/attempt row; [PD-008](../decisions/principal_decision_008_research_budget_reservation.md)
§3; [PD-009](../decisions/principal_decision_009_genesis.md) §§2, 3, 3a, 5.

**Conflict:** Reservations and attempts require a Research Authorization,
while a CHECKER lineage may hold none. `AU-CK-A` supplies 60 units but no
lawful way to reserve them. Merely adding “or Checker” leaves reservation
purposes restricted to Themes, research families or pending registrations,
and leaves the fence/revocation contract restricted to Research grants.
The bounded synthetic provider is declared under `AU-OBS-1`, which does
not exist until after the first Check that needs it.

**Failed transition:** At state 0, `AD-CK-1.0` tries to fund a Check of the
Observation Authorization grant. Its reservation caller is forbidden;
the check of an Authorization grant is not a pending registration; and
the tool declaration is in the proposal it is supposed to check. The
Checker cannot borrow its future Observation function's permission or
give itself a Research Authorization.

**Smallest repair:** Complete the same funding protocol for Checker
grants, including permitted verification purposes, unit rules, pending
liabilities, caps, expiry, fences and settlement. Put the initial
Checker's tools and tiers in `AU-CK-A` at sequence 0, and each later
consumer's tools in its own grant. Preserve the three-item bootstrap;
do not add an Observation Authorization to its waiver.

**Decision / OSA:** Principal decision required. This changes semantics
and expressly permitted callers; extending the Principal's funding-stop
exception to Checker grants is also authority scope. The handoff's U-A
repair cannot safely be described as only three wording changes with
`ΔA=0`. U-A and U-B are independently confirmed and consolidated here.

### B-2 — Critical: the universal Check form blocks Principal-led initialization

**Location:** C §III.8 Record form, Check record and Continuation;
Part V Genesis; [PD-007](../decisions/principal_decision_007_independent_checking_and_delegated_admission.md)
§PD-007.1 Check record item 4; PD-009 §§2–3.

**Conflict:** Every class must be within the proposer's Authorization
and cite a research reservation. PD-007 further specifies a reservation
for the pending registration. PD-009 gives the Principal no Authorization
and explicitly does not meter human review. Its first act after genesis
is an Authorization grant, not a research registration. The Check also
requires `(E,N,F)` even though the genesis description supplies no Paper
Book for these proofs. No applicable-field rule distinguishes an empty
or inapplicable book from an unreachable authority.

**Failed transition:** Even after B-1 is repaired and the Checker pays
for its own work, the Check of `AU-OBS-1` cannot satisfy the separate
proposer-budget line. A zero declared cost does not create the mandatory
named reservation. Substituting the Checker's reservation would fund the
wrong actor and purpose. Treating absent `F` as an outage also stops it.

**Smallest repair:** State applicability in the existing record form:
Principal authority is cited directly; zero research consumption on a
Principal control act needs no proposer reservation; a paid Check uses
its own reservation independently. Carry those distinctions into Apply
and restart. Define the empty or inapplicable Paper Book binding for
these non-execution Checks without allowing fallback when a required
ledger is unreachable.

**Decision / OSA:** Principal decision required on the applicability
rule; semantic repair, with any actual exemption from admission
requirements explicitly admitted. It does not waive independent Check.
The funding-chain narrative in the handoff does not close this defect.

### B-3 — High: the five-state arithmetic is not closed under settlement

**Location:** C §III.5 Settlement and Five states;
PD-008 §3 “Five states, all derived, none counted twice”; PD-009 §3a cap.

**Conflict:** PD-008 defines open reserved allowance as reservation amount
minus settled consumption minus pending maxima, without a nonnegative
bound. Overruns must nevertheless count in full. An underrun is said to
be released at settlement, while that formula restores it to the open
reservation. PD-009's cap says “reserved plus settled” without explicitly
including liabilities remaining after a reservation closes.

**Counterexamples:** With grant 100, reserve 10 and settle its sole
10-unit attempt at 20 while the reservation remains open. The literal
formula gives reserved allowance −10, consumption 20 and spendable 90,
instead of 80. `OVERSPENT` does not help: 20 is below the grant. Conversely,
settling at 6 leaves 4 reserved by the formula but “released” by the
prose. With a 100-unit lineage cap in a larger pool, closing a reservation
with 100 pending leaves neither open reserved allowance nor settled
consumption; excluding that liability from the cap permits another 100.

**Smallest repair:** Define nonnegative remaining allowance and release
amounts, count overruns without offsetting negative allowance, specify
whether an underrun returns to the open reservation or directly to the
grant, and include pending maxima in aggregate cap usage after closure.
Treat released allowance as an accounting movement or historical figure,
not a second balance disjoint from spendable units that already include
the release.

**Decision / OSA:** Principal semantic decision required, particularly
for underrun reuse. Owners and record kinds need not change. Provider
uncertainty explains an overrun; it does not excuse undercounting it.

### B-4 — High: Apply-time funding conditions lack an ordering contract

**Location:** C §III.8 Continuation; Part V `P-1` conditions (b), (d),
(e); PD-008 §3 funding-stop ordering and §6; PD-009 §7;
[PD-004](../decisions/principal_decision_004_exploratory_capital_standings.md)
§PD-004.2 Bracketing.

**Missing obligation:** Reservations, attempts and fences are correctly
ordered on one Evidence sequence. `P-1` and D-17 additionally require a
reservation to remain open and unfenced **at Apply**, on another ledger.
The design expressly supplies no cross-ledger atomicity. A read alone
does not establish that condition at the later Apply. Unlike opening
fills, no bracket or other ordering contract is stated for this case.

**Counterexample:** Apply reads reservation R open at E=100 and base N=10
current. The Principal commits a fence at E=101, closing R; no revocation
Transition has applied. The registration then applies at N=11 using the
earlier read. Its base is still current, yet the reservation was closed
before Apply. Reservation expiry or an overrun settlement can similarly
invalidate the earlier read without changing N. Restart does not solve
the interval between the final read and Apply.

**Smallest repair:** Specify what establishes and records the logical
ordering of final admission against Evidence-side funding invalidation
and the Evidence clock. Either preserve the stated at-Apply requirement
with an explicit synchronization/refusal contract, or admit a precisely
weaker read-time permission rule. The auditor chooses neither technology
nor permission model.

**Decision / OSA:** Principal decision required on temporal semantics
and, if weakened, the permission boundary. Do not repair this by silently
allowing a workflow engine's checkpoint to become the admission authority.
Already-admitted external attempts remain a separate case and may finish.

### B-5 — High: Outcome completion lacks a deadline and a canonical one-result rule

**Location:** C §III.5 Outcome and Reproduction; Part X §§2, 4, 6;
[PD-002](../decisions/principal_decision_002_predictions_decisions_observation.md)
F-2; PD-007 §PD-007.1 Outcome committer.

**Missing obligations:** An unavailable member becomes `UNRESOLVABLE`
at “the Standard's deadline,” but ES-1 specifies no resolution deadline
or rule for deriving one. The design requires exactly one Prediction
per Outcome, not at most one canonical Outcome per Prediction. It lacks
the duplicate/refusal rule supplied explicitly for Strategy Decisions.

**Failed transitions:** A declared print never arrives. Two Checkers
cannot determine when they must commit the missing Outcome rather than
continue waiting. Separately, two authorized resolvers can race and each
commit a correctly recomputed Outcome for the same Prediction. R-3's
count of resolved Outcomes has no stated uniqueness rule preventing
double counting; a later value after an `UNRESOLVABLE` record also needs
an explicit refusal to become a second resolution.

**Smallest repair:** Supply a Standard-owned deadline rule, with any
source-specific parameters fixed before commitment, and a canonical
resolution/uniqueness rule keyed to the existing Prediction. Specify
late values and duplicate attempts without rewriting the original
Outcome. Checker completion and Evaluation counting must use that rule.

**Decision / OSA:** Principal decision required for Standard semantics
and the resolution cardinality constraint; declare the identity effect
as well if the chosen repair changes an identity rule. No new Outcome
service or object is needed.

### B-6 — High: initial method commitments and scored events use incomparable sequences

**Location:** C §III.5 Evaluation; Part X §3; PD-005 §3 Method commitment,
table and rules 1–3.

**Conflict:** The initial method is registration content fixed at Apply
on the Transition ledger. A successor method is an Evidence record.
The rule selects the latest commitment with sequence below the first
scored event, which is on the Evidence ledger. No shared sequence domain
or cross-ledger binding for the initial method is defined.

**Counterexample:** A Strategy registers at Apply sequence 200 while
Evidence is at 20, then makes its first Decision at E=21. Its initial
method was lawfully fixed first, but `200 < 21` is false. Reversing the
relative ledger sizes can make an invalid chronological comparison look
valid. Raw integers cannot prove precommitment across independent ledgers.

**Smallest repair:** Reference commitments by ledger and record identity.
Use the admitted registration as the initial baseline and specify the
existing-ledger binding that establishes it preceded eligible events;
compare successor Evidence commitments to Evidence events within their
own sequence. State that a Hypothesis's relevant event is the Prediction
commitment, not an arbitrarily delayed Outcome or scoring operation.

**Decision / OSA:** Principal semantic/binding decision required. This
does not require a method registry, global clock or global sequence.

### B-7 — High: cost verification offers an undeclared evidence-entry route

**Location:** C Part X §3 Cost verification (b), versus §III.8 Independence
and Part II Checker role; PD-005 §3 rule 5(b); PD-007 §PD-007.1.

**Conflict:** Cost evidence may be read from Market Observations **or
recorded in the Check with provenance**. The latter permits external
material to enter during Check, while the independence contract requires
the Check to read only previously committed records by ledger and
sequence. Market Observation commit is Observation-only.

**Counterexample:** A Checker reads a current vendor fee page, copies its
fees into the Check with a URL and approves a cost model. The cost clause
accepts that route; the immutable-evidence rule forbids its input. A
second reader cannot reconstruct the same bytes from the Check's closure.

**Smallest repair:** Require the underlying market evidence to be
committed through the existing Observation route first; the Check cites
it and records the verification finding. If a separate ingestion right
is desired, it must instead be expressly proposed and admitted.

**Decision / OSA:** Reconciliation to PD-007's admitted closed-evidence
rule requires no new authority. Retaining the alternative would require
a Principal decision on authority, not just a provenance field.

### B-8 — High: an order class does not guarantee that its eventual fill reduces exposure

**Location:** C §III.10 Intent class, Provisional simulated fill and
Admission rules; PD-004 §§PD-004.3–PD-004.4.

**Conflict:** Intent is classed at order admission using same-side
working position. Every fill of an order labelled `REDUCING` is then
effective without a clock bracket. The contract does not require its
actual fill to remain reducing at the Paper Book head.

**Counterexample:** With position +40, admit a reversal as sell 40
(`REDUCING`) then sell 30 (`OPENING`, judged from the working position
zero). Before expiry T, the second order fills and confirms first,
leaving +10. After T, before cancellation, the sell-40 order fills.
It is still open and its allocation is still in force: expiry does not
supersede it. The reducing-fill rule makes the fill effective immediately,
leaving −30. Exposure crossed zero after expiry without an opening-fill
bracket. Same-side order admission alone did not prevent this ordering.

**Smallest repair:** At fill admission, prove the proposed effective
quantity still reduces the confirmed position without crossing zero;
otherwise refuse, bound the quantity, or require the opening conditions
under an explicitly admitted rule. Do not inherit an unconditional
clock exemption from the order's earlier label. State the ordering or
quantity restriction for reversal legs.

**Decision / OSA:** Principal semantic/admission repair required. This
is not U-8's accepted moving-limit limitation and occurs even with fixed
limits and an internal simulator.

### B-9 — High: `FLATTEN_ON_QUOTA` can derive orders that admission always refuses

**Location:** C §III.10 Expiry and Admission rules; §III.7 Execution
triggers; PD-004 §PD-004.5 Two bounds and §PD-004.4 expiry-set rows.

**Conflict:** The optional instruction permits deriving the expiry set
when the first Decision exceeds the quota. The expiry-set admission
rules still require a clock read at or after calendar expiry for cancels
and flatten orders; the outstanding-obligation predicate also uses T.

**Failed transition:** Quota is exhausted on Monday, T is Friday, and
`FLATTEN_ON_QUOTA` is specified. The function derives Monday's expiry
set, but its cancels and reductions fail `NOT_YET_DUE`. If the process
dies, the stated expiry predicate supplies no outstanding Monday
obligation for the fresh process to discharge.

**Smallest repair:** Either remove this optional instruction for the
prototype or specify quota exhaustion as an alternative due condition
consistently in derivation, admission and recovery. Calendar expiry must
remain independent of future Decisions.

**Decision / OSA:** Principal semantic decision required. Existing
Execution authority already names quota triggers; no new object needed.

### B-10 — High: reducing an unsafe qualified allocation is forced through qualification gates

**Location:** C Part X R-8 and §4 `Reduce or suspend`; Part V Allocation
and Standing Transition after expiry rows; §III.10 Qualified/expiry rules;
PD-005 §5.

**Conflict:** ES-1 requires reduction when limits or stress no longer
justify exposure. Every Allocation is nevertheless `EXPLORATORY` or
`QUALIFIED`; the latter requires the qualification floor and other
qualification evidence. The explicit zero-allocation standing path is
“after expiry,” but qualified allocations need not expire.

**Failed transition:** A version qualified under an earlier Standard
has 20 effective Decisions and no expiry. A new Standard raises the
floor to 40; an Evaluation now requires reducing its exposure. A
Principal proposal to zero it cannot meet the qualified Allocation
floor. An exploratory pool of zero excludes the other purpose, and
there is no expired allocation for the named standing path. A
Constitutional exception should not be necessary to stop this exposure.

**Smallest repair:** Add a bounded reduction/zeroing branch to the
existing Allocation contract, with the Principal as decider and
independent verification of its risk effect and residual execution
obligation. Qualification requirements govern acquiring qualified
exposure; specify which requirements apply when withdrawing it. Do not
assume a standing label by itself liquidates the Paper Book.

**Decision / OSA:** Principal semantic and transition-scope decision
required. No new capital object or emergency infrastructure is proposed.

## Nonblocking clarifications and reconciliation

These do not justify inventing authority. Where admitted provisions
already settle the answer, the repair is documentary reconciliation.

| Ref / severity | Exact location and conflict | Concrete consequence | Smallest repair; Principal / OSA effect |
| --- | --- | --- | --- |
| C-1 — Medium: stale worked text and ownership summaries | C Part IX principle 4; §III Summary/§III.6 Applied History/Part VII budget rows; I-4; Part VI T-A, T-B, T-C and T-F/T-G adopted from PD-002 | Principle 4 still says all budgets are consumed at Apply and reservation is open. T-A declares a 10-18 commitment forward although its resolution set includes 10-16 values. T-B allocates 15 to a zero-record successor without exploratory purpose/expiry or qualification. T-C compresses separate registration, grant and revocation into one state and omits the required fence. Adopted PD-002 examples raise allocation from an Evaluation with only a few Decisions, including unverified/missing ones. I-4 still mentions a continuity claim removed by PD-009 | Reconcile current summaries and rework the illustrative traces under admitted rules; mark earlier decision examples historical where superseded. For T-A either move commitment before every resolving member or label the full window historical. No new Principal decision or OSA change if existing decisions are applied exactly; these examples currently prove none of their conflicting claims |
| C-2 — Medium: sequence and recheck conventions | C §III.6 “first N Transitions,” §III.8 immutable proposal and changed-base continuation; Part V Genesis; PD-009 §7 | State 0 contains genesis although “first 0” implies empty; a recheck at N+1 is required while the immutable proposal still carries base N. Readers need to distinguish original proposal base from the base of the effective Check and decision | State the sequence-zero projection convention and the append-only binding from recheck to redecision/Apply, without mutating proposal history. Clarify the initial clock declaration and empty-ledger coordinates in the genesis record. Existing continuation rights are admitted; any different lifecycle/identity rule requires the Principal |
| C-3 — Low: numerical placement | C §III.7 hop depth default 2; Part X R-8 “two consecutive”; checklist item 11 | The literal-placement check fails beyond the handoff's named hop depth. Identifiers, cardinalities, sequence zero and example amounts also make a literal ban on all numbers unusable | Preserve PD-003's admitted default as explicit provisional Authorization content or ask the Principal to relocate/remove it; cross-reference the decay count to §6. Distinguish tunable policy constants from identities and examples in the checklist. No new numerical choice is made here; U-C is confirmed as organization, not a bootstrap failure |
| C-4 — Medium: refusal vocabulary and Checker proposal scope | C §III.8 Independence, Check record; Part V Agent Design registration row; PD-007 §PD-007.1 and §PD-007.5 refused example | A CHECKER may propose its successor and a criterion change in one clause, but “nothing but its own successor” and the proposer table do not align. Known `FENCED`/`OVERSPENT` is sometimes treated as `NOT DETERMINABLE`, elsewhere `NOT MET`; a Principal-only decision requirement is not a missing ontology | Reconcile permitted proposals, route criterion changes to Principal-only constitutional decisions, and consistently distinguish a known failed gate from constitutional indeterminacy. Preserve refusals. Existing rights can be transcribed without a new decision; widening them requires one |
| C-5 — Medium: classification timing and ambiguous dispatch | C §III.5 availability classes and Attempt; PD-002 §PD-002.1 derived class; PD-008 §3 Retries; PD-009 §7(4) | For a nonstructural source, a future absence witness is unavailable at Prediction commitment. The text does not say when the irrevocable class finding is finalized. A `PENDING` attempt likewise does not distinguish a crash before dispatch from a crash after dispatch | State when classification becomes determinable without relabelling established historical evidence. For recovery, apply PD-008's existing unknown-effect rule: lack of a response is not proof of no dispatch; an uncertain retry needs a fresh funded attempt. No new dispatch permission is needed; choosing a different classification lifecycle needs the Principal |
| C-6 — Medium: provider substitution and physical storage terminology | C §III.4 Provenance leaves D-14 open; Part IX principle 10; PD-006 §PD-006.1 tool table | Changing a hosted model under the same registered design is not licensed merely because tools are replaceable. Conversely, calling a database a tool must not imply that the logical authoritative ledgers cannot be stored in one | For this prototype keep the declared design/provider binding fixed; stop before any substitution lacking an admitted identity/binding rule. Clarify that replaceable software may host Speedway's ledger boundary without acquiring independent decision rights. A new provider identity/substitution rule requires the Principal and may change OSA; technology selection does not |
| C-7 — Medium: own-subject Checker routing must not be inferred from proposer independence | C §III.8 Independence; Part V Authorization row; PD-007 §PD-007.1; PD-009 §§1–3 | A Principal-proposed change to `AU-CK-A` could pass the three generic independence tests when checked by `AD-CK-1.0`: it is not the proposer or in the proposer's lineage. PD-009 separately and expressly routes changes concerning the first Checker to the second; that admitted restriction, not the three tests alone, excludes this case | Carry PD-009's restriction explicitly into `AU-CK-A`'s scope despite its broad “Check every class” description. No new decision or OSA change is needed to express the admitted initial routing. A general own-subject restriction for all future Checkers would need a Principal authority decision; it must not be invented by this audit |

The handoff's statement that only the hop default is a numerical literal
outside §X.6 is therefore too narrow. The default is admitted in PD-003;
its location does not confer an additional agent right.

## Genesis walk: empty system to ordinary operation

This is a conditional walk, not a claim that the blockers have been
repaired. It identifies the first failed step and continues on paper to
expose later dependencies.

| Step | Required durable fact or action | Audit result |
| --- | --- | --- |
| Empty system | No admitted actors or grants; initialize the declared ledger/clock conventions | Record conventions need C-2; an agent cannot infer its own authority from repository access |
| Apply 0 | Principal admits exactly CV1 text, initial CHECKER registration and `AU-CK-A`; independent Check waived only for those three items | The exception is bounded and avoids an infinite regress of Checkers. B-1 requires tools and the usable funding contract in this already-enumerated grant. Initial registration must also carry the required method commitment and provenance |
| Before Check 1 | Initial Checker reserves, pre-records an attempt, then consumes its own permitted tool budget | Currently blocked by B-1. No future source declaration, real-provider assumption or self-granted permission can fill the gap |
| Check / Decide / Apply 1 | Principal proposes `AU-OBS-1`; Checker verifies committed proposal under CV1; Principal decides; Apply records the grant; Checker settles its attempt | Currently also blocked by B-2. A repaired path has distinct proposer authority and Checker cost, and commits source permissions before any retrieval |
| Observation starts | Observation function commits declared source results and synthetic feed records; no agent or Checker substitutes for it | Lawful after sequence 1; synthetic provider/tool permission and synthetic market-source permission are different facts |
| Limits and registrations 2–12 | Checked Principal limit act, then ten checked Agent Design registrations with initial commitments | Limits are admitted in PD-004 §3/§PD-004.11 but missing as an explicit Part V row: transcribe the existing Principal/Check/Apply contract. No limit or registration is an unrecorded setup operation |
| Second Checker 13–14 | First Checker checks the second's registration and grant; Principal decides both | Permissible separate lineage. Carry the admitted own-subject routing into grant content as C-7 explains |
| Research grant 15 / Theme 16 | Principal grants pooled scopes and budgets, then registers `TH-G1` with committed motivation closure and selection basis | The grant may name the pending Theme, but reservations whose purpose requires an active Theme wait until it is active. Empirical/discovery work needs its own admitted scope, not Theme inheritance |
| Policy act 17 | Checked Principal constitutional act identifies the prototype's use of `P-1` | CV1 already contains P-1; identify sequence 17's exact scope change and decision attribution rather than silently admitting the same unversioned policy twice. No agent gains rights from registration alone |
| Ordinary operation | Research reservations, attempts, settlements, Evidence and checked registrations | B-3/B-4 remain material. No Runner or Execution Authorization is granted. Empty execution state grants no permission to create orders |

The first lawful independent Check is thus achievable with the existing
roles, but **not as currently written**. It needs no second human and no
additional unchecked bootstrap act. A separate authorized Checker is
required before a change concerning the first; a second lineage cannot
be manufactured after the first has become unable to authorize its use.

## Full walks of the two proposed proofs

### Proof 1 — evolutionary historical research

Subject: [PD-006 §PD-006.3](../decisions/principal_decision_006_replaceable_tools_and_first_prototype.md),
with PD-009's actors and grant. All following steps depend on repaired
genesis and accounting.

1. The ten admitted designs run only under the pooled Research grant,
   in their Theme or empirical/discovery scopes. Each reservation is
   admitted against the same serialized remaining pool and its cap.
2. Each backtest has a pre-recorded attempt. The replaceable tool reads
   a named historical snapshot under a cutoff and returns an output.
   The authorized Research Agent commits the dataset/hash, parameters,
   tool version/hash, reproducibility binding and result; the tool
   commits no Evidence and awards no standing. Actual consumption is
   settled even when the run failed.
3. A losing candidate can be rejected before registration or abandoned
   in a negative Research Record. It never becomes `CONTRADICTED` from
   those results. If an already-admitted Hypothesis is to be retired,
   that is a checked Principal standing act; an agent's abandonment
   record alone does not remove population membership. Any cited
   Evaluation reports no forward grounding and may not manufacture a
   historical falsification.
4. For a registration, the proposer names an open purpose-matched
   reservation, motivation closure, selection basis, method commitment,
   declared resolution sources and family history. A source still must
   be active at the base even though the motivating backtest is historical.
5. The independent Checker checks scope, restatement, family
   reconciliation and evidence content; a bad proposal is preserved as
   a refusal. A passing Hypothesis registration can be decided by P-1
   only if its final funding and base conditions hold. Two proposals
   at one base require recheck/redecision for the second after the first
   applies. B-4 cannot be replaced by a cached “PASS.”
6. Registering a successor Hypothesis creates a new exact subject with
   zero forward record. It does not automatically retire an admitted
   predecessor; a Principal standing act is required where retirement
   is intended. Rejected candidates remain on the Transition ledger;
   they were never population members to retire.
7. A Research Agent can propose its own successor Agent Design, checked
   by a different lineage and registered under P-1 without rights. To
   run it, the Principal must grant a new Authorization. Replacing or
   narrowing the pooled grant requires its prior fence and checked
   successor grant. Pending predecessor liabilities remain charged to
   the predecessor grant; no reservation or forward credit transfers.
8. At the ceiling, another reservation is refused; after interruption,
   pending maxima remain until settlement. An ambiguous provider retry
   has its own dispatch index and funded attempt. A fence refuses new
   attempts but allows already-admitted attempts to complete. Read
   negative records and ledger-derived lineage/family history after
   reopening; do not restore an agent memory snapshot as authority.

**What follows:** This can demonstrate accountable search, preserved
negative results, refusal at a metered ceiling and lawful succession.
It cannot demonstrate forward Hypothesis falsification, earned Agent
Design fitness, profitability or autonomous authority transfer. The
phrase “retire Hypotheses” in the proof does not expand P-1's two rights.
No executed result presently demonstrates even the bounded conclusions.

### Proof 2 — development, Theme formation and competing Hypotheses

1. After its Authorization exists, the Observation function retrieves
   the synthetic feed under its enumeration contract and commits
   COMPLETE/PARTIAL/failure results and document bytes. The feed is
   synthetic in the source declaration, not relabelled later by a score.
2. Authorized agents reserve and attempt screening work, then commit
   typed SCREEN and formation records with closures. Missing expected
   screens remain visible; the proof does not infer absence from a
   failed or partial feed retrieval.
3. Any follow-up locator must occur in already committed bytes and
   satisfy feed, domain, depth, count and unit constraints. The
   Observation function retrieves and commits it. A hop cannot become
   a resolution source merely because it was useful for formation.
4. The new Theme is a checked Principal registration with motivation
   closure and selection basis. P-1 does not admit Themes. PD-009's
   Theme grant names `TH-G1`; a newly discovered Theme does not
   automatically enter that scope. The Principal must authorize any
   newly needed Theme funding. Superseding the existing Research grant
   entails fence, Check, successor grant and fresh reservations.
5. Before Predictions, commit one EXPERIMENT DESIGN specifying the
   competing claims' common resolution set. Each Hypothesis has its
   own immutable statement, falsifier, sources, methods and selection
   basis. Competing registrations can use P-1 if scoped and funded,
   with stale-base rechecks. Their shared shocks and search family do
   not become independent trials through separate identities.
6. Commit Predictions before the designated synthetic resolving data,
   with formation records excluded from their resolution sets. Then
   observe and resolve deterministically. Every result remains
   synthetic/historical machinery evidence even if revealed sequentially.
   Missing prints expose B-5; synthetic timing does not excuse it.
7. A Research Agent proposes an executable Strategy Version with exact
   artifact, proposition, declared inputs/trigger and method commitments.
   A Checker performs the registration executions against a closed test
   input and finds reproducibility; the Principal decides registration.
   P-1 cannot decide it. It enters `INCUBATING`, allocation zero.
8. There is no Runner grant, so registration produces no Strategy
   Decisions. There is no Execution grant, so there are no orders or
   fills. Registration test executions are not forward Decisions and
   must not be counted as a performance record.
9. Commit the next-question SELECTION record with its full alternatives,
   estimates or `UNESTIMATED`, rejections, closure and revisit rule under
   an Authorization permitting that record. If a separate SELECTION
   method lineage is used, register and authorize it first. It proposes
   research; it does not fund itself. Later records provide the fate of
   rejected alternatives; the initial selection alone cannot prove those
   future outcomes or estimate accuracy.

**What follows:** This can demonstrate the trace from a development to
questions, competing claims, an executable candidate and an attributable
next selection. It does not establish that an agent discovered something
outside its training knowledge, that a synthetic result is prospective
market evidence, or that the Strategy works. It does not exercise
Decision reproduction in operation, execution, expiry or investment
learning from genuine forward data. Neither proof closes B-8–B-10 by
omitting the Paper Book.

## Adversarial ordering and recovery checks

| Ordering on paper | Required outcome / independent assessment |
| --- | --- |
| Two agents reserve the last 10 units | Evidence sequence admits at most one; the second is refused. This contract is sufficient without selecting a database |
| Reservation expires with an attempt pending | Only unused allowance releases; the pending maximum remains. Settlement is allowed after expiry/fence/revocation. B-3 concerns the exact subsequent arithmetic |
| Attempt admitted, then fence, then dispatch | Lawful completion under the admission already consumed; a fence is not a promise to cancel external work already admitted |
| Fence, then new attempt or retry using an old reservation | Refuse `FENCED`, even if the Applied History still shows active. This is a sound same-ledger ordering |
| Provider dispatch, process death, no provider answer | Pending effect unknown; another dispatch needs another funded attempt unless an enforceable provider deduplication mechanism supplies the declared guarantee. Exactly-once is not inferred |
| Grant 100, reservation 10, actual 20 while open | B-3: negative reserved allowance must not conceal the excess. A bounded synthetic provider's happy path alone does not exercise this branch |
| Check PASS, unchanged Apply head, fence or expiry before Apply | B-4: unchanged N is insufficient and an earlier Evidence read does not establish final eligibility |
| Two allocations individually legal at one base | First Apply advances N; second must recheck composition and redecide. No stale-base restoration is lawful |
| Opening simulated fill straddles expiry or allocation supersession | Confirmation cannot establish the bracket, so fill is terminal `UNESTABLISHED` and excluded from positions; preserved as an operational record |
| Reversal legs fill in the opposite order | B-8: recorded order class alone cannot justify effective reducing execution after T |
| Quota exhausted before T with `FLATTEN_ON_QUOTA` | B-9: the required set cannot admit its orders under the calendar-only due rules |
| T-H / PD-004 recovery after cancels or partial flatten | Terminal-state obligation, not set existence, keeps recovery alive. Fresh reads derive residuals and replacements; duplicate set/order identities refuse. These positive cases do not cover B-8's fill ordering |
| T-D process death between Decision and order | Derive from the committed Decision, current allocation and Paper Book; the set key prevents duplicate creation. A stale cached allocation cannot resume execution |
| Qualified exposure requires reduction after Standard changes | B-10: the reduction must not require fresh qualification it can no longer earn |

For units the system meters at a declared constant, a correctly enforced
pre-attempt gate can support a hard ceiling. A real provider cap is an
external enforcement assumption, not a Speedway guarantee. Uncapped
charges allow estimates and full accounting only and are prohibited at
genesis. An overrun injection can test accounting; it cannot simultaneously
be evidence that a supposedly bounded provider never overruns.

## Accepted prototype limitations and reuse

These limitations can remain without expanding this audit into a
production-readiness program. Their labels do not excuse the blocking
contradictions above.

| Limitation | Boundary accepted for this audit |
| --- | --- |
| No runtime, workflow engine, database or backtester selected | Contracts may precede technology. Nothing in this review requires a particular product or custom implementation |
| No implementation or CPOC evidence | Every control remains specified on paper. An eventual fresh-process witness must reconstruct exact subjects and lawful continuation, then verify history; ordinary tests or a persisted workflow checkpoint alone do not establish CPOC |
| No genuine forward market evidence in either proof | Historical and synthetic results cannot qualify capital or earn prospective fitness. Demonstrating machinery is an appropriate prototype objective |
| Real-provider cap enforcement unresolved | Use only the admitted bounded synthetic provider and metered local work until a named real-provider assumption is separately accepted. No vendor-invoice guarantee follows |
| Observation function's own costs not covered by the research meter | The declared grant bounds named research consumption, not total system expense. A claim of a total expenditure ceiling would need a further funding rule |
| Checker fallibility and incomplete discovery of hidden trials | Independence and immutable evidence do not imply infallibility or complete disclosure. Verification yield and named gaps remain visible; provider diversity is supplementary |
| Declared-source availability only | A feed absence witness establishes absence within its contract, not universal absence across every channel or freedom from model leakage |
| U-8 moving portfolio limits | The admitted pre-witness limitation remains explicit; no claim of atomic limit enforcement across ledgers is accepted. It is outside the two proofs and must be revisited before a broader execution guarantee |
| No real execution and no prompt liquidation during total outage | Simulator-only fills can be unestablished; live venue facts cannot be discarded on that basis. Expiry obligation can survive without guaranteeing timely execution or liquidity |
| Provisional floors, stress calibration and single Principal | These bound the prototype's decisions; they do not establish statistical efficacy or autonomous handling of Principal-only decisions |

Reuse is permitted and desirable. An agent runtime may perform reasoning;
a workflow engine may schedule/retry tasks; a database may persist the
logical ledgers; a backtester may compute reconstructions. Their outputs
and checkpoints do not independently establish currentness, funding,
evidentiary class or permission. Each external dispatch must respect the
attempt contract, each Evidence result must enter through its authorized
caller, and fresh work must consult the governed state. Replacing a tool
must preserve exact history and bindings. No defect found here requires
building a new agent runtime, workflow engine or backtester.

## Coverage against the supplied checklist

| # | Independent result for revision 10 |
| --- | --- |
| 1 Authority map | FAIL: B-1, B-5, B-6, B-7; intended owners otherwise separable as mapped above; C-1/C-6 need reconciliation |
| 2 Commit restrictions | FAIL: Checker funding and cost-evidence routes conflict with permitted callers; B-1/B-7 |
| 3 Decision rights | FAIL: universal control-act gates and reduction path; B-2/B-10. C-7 clarifies admitted Checker routing. P-1 itself delegates only two registration decisions and no grant rights |
| 4 Time | FAIL for complete design: B-4/B-6/B-8/B-9. One Evidence clock and interval witnesses are otherwise correctly distinguished from publication times and local timers |
| 5 Evidence classes | Core separation holds; worked examples contradict it (C-1), and completion/binding needs B-5/B-6. No synthetic, reconstructed or exploratory figure can ground prospective fitness |
| 6 Budgets | FAIL: B-1/B-3/B-4. Funding stop versus revocation and three guarantee tiers are otherwise useful distinctions |
| 7 Recovery | FAIL as a complete specification: B-4/B-8/B-9; positive T-D/T-H and PD-008 cases traced above. Checklist's PD-009 §6 reference concerns methods; D-17 is §7 |
| 8 Refusals | PARTIAL: refusal preservation is general and explicit; missing completion gates and inconsistent result vocabulary need B-5 and C-4. No claim that every previous refusal label is consistently carried forward |
| 9 Closures / both research paths | FAIL end to end until B-1/B-2/B-5/B-6/B-7 are repaired; current worked examples also need C-1. Conditional full proof walks above expose required Principal acts |
| 10 TENTATIVE markers | Satisfied as marker removal only; D-06's inherited-credit permission is removed by PD-009. Residual I-4 wording needs C-1. Marker absence proves no coherence |
| 11 Numbers | Literal pass condition not met; C-3. Admitted defaults and provisional constants are not newly authorized by this audit |
| 12 Genesis | FAIL: B-1/B-2; bounded sequence-zero waiver and specific second-Checker routing are admitted, but the first Check cannot yet proceed |
| 13 Reuse | Satisfied as an architectural direction, with C-6 clarifying physical storage and governed provider substitution. No runtime choice required for this audit |
| 14 Record-set consistency | PARTIAL: baseline, admission headers and principal amendments present; actual propagated text retains C-1 contradictions. Earlier “no conflict” re-audits are not conformance evidence |
| 15 What is not claimed | Satisfied in this report: document-phase admissions only, no genesis, implementation, CPOC or certification; no investment efficacy claim |

## Final disposition

**Not ready.** Repair B-1 through B-10 under the Principal's decisions
where indicated, reconcile the current examples and summaries, and
re-run the bounded failed transitions before freezing CV1. The first
priority is a lawful initial Check, followed by exact budget accounting
and final admission ordering. Evidence completion and paper-execution
defects remain part of the whole-design audit even though the first two
proofs do not trade.

This is an **OSA FAIL for design coherence at revision 10**. It is not
an implementation-conformance judgment: there is no implementation to
test, and CPOC is unexecuted. A repaired coherent design would still not
establish investment efficacy, profitable alpha or reliable execution
costs. This audit admits nothing and does not execute genesis.
