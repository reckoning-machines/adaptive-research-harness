# Principal Decision Record 005 — ES-1, the Initial Evaluation Standard

Status: **ADMITTED 2026-10-19 by the Principal (document-phase admission): revision 3 with the cost clarification, the eight decisions of §10 as proposed.** Applied to the Constitution as revision 6 (Part X) and re-audited in [osa_reaudit_pd005_20261019.md](../audits/osa_reaudit_pd005_20261019.md). Admission text, as approved:

```text
ADMITTED 2026-10-19 by the Principal (document-phase admission), by Constitutional Transition:
PD-005 revision 3, Evaluation Standard ES-1.0, sections 2 to 7 as
written, with every constant in section 6 labelled PROVISIONAL.

Clarifications on admission:
(a) Internal simulator fills are modelled execution. They are never
    independent validation of achievable trading costs and never
    evidence of alpha. Cost verification rests on the committed cost
    model and sensitivity method, independently checked market
    evidence (observed spreads, volume, depth, fees) and the committed
    conservative scenarios. Validation of real execution costs belongs
    to a later, separately authorized execution phase.
(b) The floors N_eff >= 20 (Strategies) and N_eff >= 12 (Hypotheses)
    are operational floors and claim no statistical power.
(c) No statistical method is constitutional. Methods are committed
    before the window they judge, on registration content or an
    EXPERIMENT DESIGN Research Record, and replaced by a successor
    commitment governing later windows; recomputation of earlier
    windows is sensitivity analysis. No method register exists.
(d) One primary outcome per Evaluation; accompanying research questions
    create no standing. Qualification is at an allocation no greater
    than a*, the largest allocation at which no portfolio limit is
    breached under the stress set, with the stress floor from the
    instrument class and NOT ASSESSABLE where none exists.
(e) Nothing in this admission certifies any Evaluation, method or
    implementation.

Constitutional Delta admitted:
ΔO: NONE.
ΔS: §III.9: ES-1.0 content (ten requirements with applicability by
    population; method commitment; three output sets; six outcomes and
    the Transition classes each informs; provisional constants with
    bases; stress floor; NOT ASSESSABLE). §III.5 Evaluation: required
    content R-1 to R-10 with N/A marks; pinned methods; FIRST and the
    limit-breach rule. §III.5 Research Record kind EXPERIMENT DESIGN:
    meaning widened to carry a method commitment for a forward window.
    §III.2, §III.3, §III.4: initial method commitment as registration
    content; cost model and sensitivity method for Strategies. §III.3:
    explanatory standing DERIVED (FR-6). §III.4: evaluation by method
    class (FR-9). Part V: Hypothesis standing change, Allocation and
    Retirement Checks verify ES-1 conformance, including cost
    verification against market evidence with simulated fills excluded.
    Part VII: explanatory standing, outcome, a*, N_eff as DERIVED rows.
ΔA: NONE. No method, score, evaluator or commitment record gains a
    decision right; Check content is extended; the Principal and
    admitted policy remain the only deciders.

Closed by this admission: U-6, FR-6, FR-8, FR-9, UD-11, UD-12.
Open items preserved with owners: E1-R1 to E1-R6 (ES-1 audit); U-1;
UD-3; D-10, D-11, D-12, D-17, N-1; U-8 and the paper fill methodology
(plan step 7); every item of the PD-002, PD-003 and PD-004 re-audits.
```

Prior content follows. Revision 3 was proposed for
admission by a Constitutional Transition (§III.9, I-7); the document-phase admission above stands in for that Transition until genesis. Depends on PD-001
to PD-004, all admitted and applied in Constitution revision 5. No
Constitution text is changed by this record. Revision 2 (2026-10-19)
makes the five repairs the Principal directed: applicability by
population, pre-outcome method commitment, conditional portfolio
contribution, an independent stress floor, and the first-Evaluation
case. Revision 3 (2026-10-19) makes the Principal's cost clarification:
simulated fills are not evidence of achievable costs; cost verification
rests on committed cost models, independently checked market evidence
and conservative cost scenarios.

Date: 2026-10-19 (revision 1: same day)

Subjects: U-6 (`ES-1` content); FR-6 (mechanism on contradiction); FR-8
(forward events only; search-family counting); FR-9 (evaluation per
method class); UD-11 (`SELECTION OUTCOME` timing); UD-12 (`UNESTIMATED`
and family counts).

Sources: [Constitution revision 5](../doctrines/new_speedway_constitution.md)
§III.2, §III.3, §III.4, §III.5 (Evaluation record), §III.9, I-1, I-3,
I-4, I-7, Part V; fin123-core forward evidentiary doctrine §5, §6, §8,
§9, §10, §11 (adopted); the Principal's brief of 2026-10-19; focused
audit [es1_osa_audit.md](../audits/es1_osa_audit.md); non-authoritative
[methods note](../reference/es1_methods_note_20261019.md).

## 1. The question ES-1 answers

Given uncertain evidence, changing markets and potentially catastrophic
tails: investigate, incubate, allocate, reduce or retire? ES-1 is the
rule by which Evidence becomes an answer to that question for each of
three populations, separately. It does not answer it; a Transition does.
An Evaluation under ES-1 is `DERIVED`, recomputable, and changes
nothing by itself (§III.5, I-13).

Five principles, each a consequence of "trust is earned, never
inherited" (adopted):

1. Historical success is not prospective evidence. Historical
   Reconstruction is for discovery, debugging and rejection; it grounds
   nothing (I-2, I-3; doctrine §9).
2. Returns are not Gaussian. No requirement below assumes normality,
   independence, stable correlation or a universal tail law. Every
   method states what it cannot estimate.
3. Search history matters. The unit of evidence is the search family,
   not the surviving version. Renaming, re-parameterizing or succeeding
   creates no independence. Twenty outcomes from one shock are not
   twenty observations.
4. Decay is expected. Fitness is conditional on conditions and time;
   departure from expectation is a signal to investigate, not an
   automatic retirement.
5. Survival precedes optimization. Standalone economics and marginal
   portfolio contribution are both assessed; no score grants capital.

## 2. What is constitutional and what is replaceable

| Constitutional (changed only by Constitutional Transition) | Replaceable (versioned, pinned in each Evaluation, no authority) |
| --- | --- |
| The requirements R-1 to R-10 below: what every Evaluation must state, from what evidence, and how a Transition may use it | Estimators, Bayesian models, tail models, simulations, dependence and clustering methods, regime diagnostics, rankings, scenario generators |
| The evidence classes and their roles | The numerical values of provisional constants, once ES-1 is admitted, change by Constitutional Transition; their *methods* do not |
| The outputs each population's Evaluation must produce and the decisions each may inform | How an output is computed |
| Declaration, disclosure and verification duties; the rule that a qualifying method is committed before the window it judges | Which method is committed, and its successor for later windows |

A method is a versioned artifact with a content hash, named in the
Evaluation that uses it. Producing a score gives a method no standing. A
method that establishes qualifying evidence is committed before the
window it judges (§3, method commitment); a successor governs later
windows, and earlier results recomputed under it are sensitivity
analysis, shown beside the qualifying result (R-10). AIE and any other selection method remain
`SELECTION` lineages (PD-003.5); they inform choice and prove nothing.

## 3. The evaluation contract: ten requirements

Every Evaluation under ES-1 states the following. An Evaluation that
omits one is non-conforming, and a consequential Transition citing it is
refused at Check.

| Ref | Requirement | Answers |
| --- | --- | --- |
| **R-1 Claim** | The exact subject (`HypothesisId`, `StrategyVersionId` or `AgentDesignVersionId`); the claim as registered (resolution rule and falsifier; proposition boundaries, prediction target and declared stopping rule; method class and purpose); the closure `(E, N, F)`; `EvaluationStandardVersion`; every method version used with its hash | What was the original claim? |
| **R-2 Class** | Evidence partitioned by class. The **grounding series** is Contemporaneous Forward Record only. Historical Reconstruction is reported beside it, labelled, never summed, never grounding. An exploratory executed record (PD-004) informs shortfall and operational measures only | Was the evidence historical or prospective? |
| **R-3 Observations** | `N_raw`: resolved forward Outcomes (Hypothesis) or scored forward Decisions (Strategy). `N_eff`: an effective count by a declared method that clusters observations sharing a shock, an overlapping horizon or a common exposure, with `N_eff ≤ N_raw` and a statement of what the method cannot resolve. Minimums apply to `N_eff` | How many economically independent observations? |
| **R-4 Search** | The search family: every version, trial, Prediction and Research Record under the `SearchFamily` label and the lineage, successor lineages re-using the same target or mechanism, and the Theme's lineage memory; `T_total` trials and `T_forward` trials; the reconciliation of expected screens, events and consumption against recorded ones, with any gap named. The grounding evidence is adjusted for `T_total` by a declared method | How much searching produced this? |
| **R-5 Payoff** | For the scored quantity over the declared horizon: a central estimate, an uncertainty interval, and downside measures (empirical drawdown, worst-`k`, tail loss at declared levels), each by a declared method with its declared constants and their basis (doctrine §11), and a not-estimable statement. For Strategies: gross, model-net and break-even performance, and the net record under the committed conservative cost scenarios (§3, cost verification) | What do we believe about payoff, uncertainty, downside? |
| **R-6 Stress** | Results under the declared **stress set** in force (scenario classes, versioned), for the subject alone and for the portfolio with it: estimated loss, liquidity to exit, limit breaches; and an explicit list of conditions the evidence does not cover | What happens under stress and unfamiliar conditions? |
| **R-7 Contribution** | Conditional on the proposed allocation `a`, the existing population's exposures at the head, normal and each stressed condition, and declared liquidity and exit assumptions: the marginal change in portfolio payoff, drawdown and stress loss; the overlapped subjects named per condition; and **`a*`**, the largest allocation at which no portfolio limit in force is breached under the stress set. A subject may add in normal conditions and duplicate losses under stress; both are stated. Qualification is at `a ≤ a*` | What does it add, at what size, under which conditions? |
| **R-8 Change** | On a **first Evaluation**: no predecessor exists; the Evaluation commits, by the committed method, the predictive distribution and decision thresholds the next Evaluation will be judged against; finding `FIRST`. On every later Evaluation: realized outcomes since the predecessor compared with what it committed; finding `WITHIN` (ordinary losses inside the expected distribution: no outcome change on this ground), `DEPARTED` (outside the committed interval over the window: evidence of deterioration or misspecification; two consecutive → `Investigate`) or `OUTSIDE` (a single outcome beyond the committed tail bound: `Investigate` at once, the predictive model marked as failed); separately, a **limit breach** at the head or under the stress set at the current allocation requires `Reduce` regardless of any statistic, because limits are Applied History facts, not findings. The subject's declared stopping rule is applied. Retirement is never automatic after losses | Has the evidence changed enough to justify another action? |
| **R-9 Output** | One output from the population's output set (§4) with the reasons, and the Transition classes it may inform. Never a standing or allocation change | What may follow? |
| **R-10 Verification** | Recomputable from the closure by a Checker; method versions pinned and their commitment sequence below the window they judge; a successor method since the subject's previous Evaluation disclosed, with the qualifying result under the governing commitment and the recomputation shown as sensitivity; comparison across `EvaluationStandardVersion`s reported as a standard change, never as improvement | Can it be checked? |

### Applicability by population

One contract, applied by population. Each requirement is `APPLIES`,
applies in the stated form, or is `N/A`. An Evaluation marks every
`N/A` requirement with the population reason; an omitted requirement,
or a value invented to fill one, is non-conforming.

| Requirement | Hypothesis (belief) | Strategy (capital) | Agent Design (research contribution) |
| --- | --- | --- | --- |
| R-1 Claim | APPLIES: statement, resolution rule, falsifier, tolerance, stopping rule | APPLIES: proposition boundaries, prediction target, cost model, stopping rule | APPLIES: method class, purpose, Authorization scope and cadence |
| R-2 Class | APPLIES: forward Outcomes ground; reconstruction shown | APPLIES: forward decision-implied record grounds; reconstruction and exploratory record shown | APPLIES as: contribution counted only from research that resolved forward; reconstruction-only research reported, not credited |
| R-3 Observations | APPLIES: `N_raw`, `N_eff` over resolved Outcomes | APPLIES: over scored Decisions | `N/A`: research units are costs, not observations; coverage against cadence is reported instead |
| R-4 Search | APPLIES: Predictions and competing Hypotheses in the family | APPLIES: versions, trials, lineages, Themes | APPLIES: the lineage's own proposals, trials, rejections and screens, reconciled against consumption |
| R-5 Payoff | APPLIES as **calibration**: hit rate against tolerance, a declared scoring rule, declined-when-warranted; no payoff | APPLIES: central estimate, interval, downside, not-estimable statement | APPLIES as **contribution per unit**: forward-resolved research, questions closed (including negative), estimate error (`SELECTION`), verification yield (`CHECKER`), per unit consumed |
| R-6 Stress | `N/A`: the falsifier is the Hypothesis's stress; conditions it did not cover are listed under R-5 | APPLIES: stress set, stress floor, not-estimable statement | `N/A` |
| R-7 Contribution | APPLIES as: redundancy with competing Hypotheses over the same resolution set | APPLIES: conditional contribution and `a*` | APPLIES as: duplicated questions with other lineages (FR-4) |
| R-8 Change | APPLIES: `FIRST`, then calibration against the committed expectation | APPLIES in full, including the limit-breach rule | APPLIES as: contribution against the expectation declared in the previous Evaluation or the Authorization |
| R-9 Output | `SUPPORTED`, `CONTRADICTED`, `UNDETERMINED` | The six outcomes of §5 | `CONTINUE`, `REVISE`, `RETIRE` |
| R-10 Verification | APPLIES | APPLIES, with the cost verification below | APPLIES |

### Method commitment: fixed before the outcomes it judges

An evaluator may not choose a method after seeing the results it will
judge. The methods that establish qualifying evidence are therefore
committed before the forward window they govern resolves, on records
the ontology already owns:

| What is committed | Carrier (owner) | Commit boundary | When |
| --- | --- | --- | --- |
| The initial **method commitment** for a subject: the `N_eff` and dependence method; the multiplicity method over the family; the cost model (Strategies); the predictive-check method and its decision thresholds; the stress-set version and its calibration method (Strategies); the scoring rule (Hypotheses); the contribution measure (Agent Designs); each as a versioned artifact with content hash and declared constants with bases | Registration content of the Hypothesis, Strategy Version or Agent Design Version (Transition ledger: proposal content, §III.2 to §III.4) | The registration Transition (Propose; fixed at Apply) | Before the first forward event |
| A **successor method commitment**: the same content, naming the subject and the Evidence sequence from which it governs | A Research Record of kind `EXPERIMENT DESIGN` (Evidence ledger, §III.5), whose existing meaning, a precommitted design that precedes the evidence it governs, is widened to name methods for a forward window | Evidence commit, by the proposer or any authorized agent under its Authorization | Before the first scored event of the window it governs |

Rules:

1. An Evaluation that establishes qualifying evidence for a window uses
   the commitment in force for that window: the latest commitment whose
   sequence is below the window's first scored event. The Checker
   verifies the sequence (R-10).
2. A successor commitment governs only events after its commit. Earlier
   windows keep their own; the qualifying series is computed per window
   under its own commitment and the windows are reported together with
   the boundary named.
3. Recomputing earlier windows under a newer method is **sensitivity
   analysis**: shown, labelled, never qualifying evidence.
4. Nothing here is a registry, an authority or an immutable
   methodology. A method is replaced by committing a successor before
   the next window. Methods used only for `Investigate` questions need
   no commitment.
5. **Cost verification** (Strategies). New Speedway's fills are
   generated by an internal simulator under assumed execution rules
   (PD-004.15). They are not independent observations of achievable
   trading costs, and nothing below treats them as such.
   (a) The Strategy's **cost model** and its **cost-sensitivity
   method** (the conservative scenarios and how the decision-implied
   record is recomputed under them) are part of the method commitment,
   fixed before the forward window.
   (b) The Checker of a `QUALIFIED` Allocation Transition verifies the
   commitment sequence, then checks the model against **available
   market evidence**: observed bid-ask spreads, volume, depth and fees
   for the instruments and turnover concerned, read from Market
   Observations under a declared source or recorded in the Check with
   their provenance. The Checker distinguishes that evidence from
   modelled impact and from simulated fills, and states which component
   of the model rests on which.
   (c) The Evaluation reports, on the grounding series, **gross**,
   **model-net** and **break-even** performance (the cost per unit of
   turnover at which the net record is zero), and the net record under
   the committed conservative scenarios.
   (d) Exploratory paper fills (PD-004) establish operational behavior
   and **simulator-relative shortfall**: the difference between the
   decision-implied record and the simulated executed record under the
   simulator's rules. They validate no actual execution cost and
   establish no alpha; PD-004's "implementation shortfall" is read in
   this sense.
   (e) `Qualify` for bounded paper capital may proceed when the
   independently checked cost scenarios, the prospective evidence and
   the portfolio stress requirements support it together.
   (f) Where reasonable cost uncertainty, as bounded by the market
   evidence and the conservative scenarios, could eliminate the edge
   (the break-even cost lies within the checked range), the Evaluation
   says so and **withholds `Qualify`**; `Incubate` and `Explore on
   paper` remain lawful.
   (g) Validation of real execution costs belongs to a later,
   separately authorized execution phase and is outside this Standard.
   No cost engine is designed here.

## 4. Three populations, three output sets

No universal fitness score exists. Each population has its own outputs,
and I-1 forbids any of them from feeding another except through an
admitted Transition.

### Hypotheses compete for belief

Evidence: the Hypothesis's own committed forward Predictions and their
Outcomes; declined Predictions and whether declining was warranted;
calibration against the declared tolerance; `N_raw`, `N_eff`; the
family. Output: `SUPPORTED`, `CONTRADICTED` or `UNDETERMINED`, judged
against the falsifier and stopping rule fixed at registration. Informs:
Hypothesis standing change. A Strategy's profit never enters.

### Strategies compete for capital

Evidence: the decision-implied record (forward Decisions at the
Standard's notional, after the declared cost model) as the grounding
series; standalone economics (R-5); survivability (drawdown, liquidity,
leverage, concentration, tail loss under R-6); marginal contribution
(R-7); change (R-8); the executed record from confirmed fills under its
label for shortfall; reproduction standing of every Decision counted
(an `UNREPRODUCED` or `NON-REPRODUCIBLE` Decision grounds nothing,
§III.3). Output: one of the six outcomes of §5. Informs: Allocation,
standing Transitions, retirement. The explanatory Hypothesis's standing
is reported (§7, FR-6) and changes no minimum.

### Agent Designs compete on research contribution

Evidence, per unit of research budget consumed and by method class
(FR-9): `RESEARCH`: registrations that reached forward evidence,
questions closed including negative results, restatement refusals,
screening coverage against the discovery cadence; `SELECTION`: realized
value and cost of chosen candidates against the estimates given, the
later fate of rejected candidates, and estimate error or its absence
(`SELECTION OUTCOME`); `CHECKER`: defects later found in what it passed
and refusals later shown unwarranted. Output: `CONTINUE`, `REVISE` or
`RETIRE` as a recommendation on the lineage. Informs: Authorization
acts and successor registration, decided by the Principal. A lineage is
never credited with the profit of a Strategy it proposed (I-1); it is
credited with research that resolved forward, whichever way it resolved.

## 5. Outcomes and the Transitions they inform

| Outcome | Meaning under ES-1 | May inform | PD-004 reconciliation |
| --- | --- | --- | --- |
| **Investigate** | Uncertainty worth resolving: a named question, a budget, a stopping rule | A Research Authorization act; `EXPERIMENT DESIGN`; a Theme or Hypothesis registration | No capital |
| **Incubate** | Accumulate forward Decisions at zero allocation until `N_eff` reaches the minimum or the stopping rule ends it | Nothing required; the standing is `INCUBATING` | Decision-implied record accrues at the notional |
| **Explore on paper** | Bounded simulated execution for operational behavior and simulator-relative shortfall | An `EXPLORATORY` Allocation Transition (purpose, expiry, quota, instruction) | The exploratory executed record is labelled and never grounding, whatever it earned; it validates no execution cost; only the decision-implied record qualifies |
| **Qualify for allocation** | Grounding series meets the minimums; survivability within limits under the stress set; `ADDS`; proposal of capital subject to independent Check and portfolio limits | A `QUALIFIED` Allocation Transition citing the Evaluation | Checker refuses if any exploratory figure is in the grounding series |
| **Reduce or suspend** | R-6, R-7 or R-8 no longer justify current exposure, or a limit would be breached | An Allocation Transition reducing or zeroing; a standing Transition | Expiry rules unchanged |
| **Retire** | The declared stopping rule is met, or the falsifier is met | A retirement Transition; a Hypothesis standing change | The record is preserved in full |

An outcome is a recommendation. Capital and standing change only by an
applied Transition decided by the Principal or an admitted policy, after
an independent Check (§III.8, Part V). A Strategy is not retired by a
losing period; it is retired under its own stopping rule or by the
Principal.

## 6. Provisional constants of `ES-1.0`

Declared with their basis, labelled provisional, changed only by
Constitutional Transition once admitted. None is a universal constant.

| Constant | Provisional value | Basis | Applies to |
| --- | --- | --- | --- |
| Forward-event minimum for `Qualify` | `N_eff ≥ 20` scored forward Decisions, identical on every discovery path (FR-8) | An operational floor below which no qualification is proposed. It claims no statistical power: power depends on effect size, dependence, selection history and tail behavior, and `N_eff` itself depends on the committed method | Strategies |
| Forward-event minimum for `SUPPORTED` or `CONTRADICTED` | The registration's own stopping rule; never fewer than `N_eff ≥ 12` resolved Outcomes | Same: a floor, not a power claim | Hypotheses |
| Standard notional for the decision-implied record | One unit, where one unit is the portfolio's declared minimum allocation | Makes decision-implied and executed records comparable | Strategies |
| Cost model and cost-sensitivity method | Committed per Strategy before the window (spread, impact, fees; the conservative scenarios); the decision-implied record is reported gross, model-net and break-even, and net under the scenarios; checked against market evidence, never against simulated fills | Costs are part of the claim; simulated fills are not evidence of them | Strategies |
| Multiplicity adjustment | The grounding evidence must remain supportive after adjustment for `T_total` by the declared method; the method and its constants are named | fin123-core §11; Bailey-style deflation is one admissible method, not the rule | Strategies, Hypotheses |
| Stress set `SS-1.0` | Scenario classes: largest historical drawdown of the subject's market; a volatility regime shift; a liquidity gap (spread and depth shock); a discontinuity of three times the largest observed move in the grounding series; a correlated drawdown of the current population | Classes, not calibrated events; the "three times" multiplier is a declared, unfitted stress, not a forecast | Strategies, portfolio |
| **Stress floor** | Each scenario is calibrated no milder than the **instrument class** history over a declared long window (the class's largest drawdown, worst liquidity episode, and three times the class's largest move where that exceeds the subject's); the subject's own short record never sets the scale. Where neither the subject nor its instrument class has usable history, survivability is **`NOT ASSESSABLE`**: `Qualify` is refused; `Incubate` and `Explore on paper` remain lawful; the Evaluation says so | Sparse data must not produce a mild stress set; refusal is the honest answer | Strategies |
| Decay flag | `DEPARTED` when the realized series since the previous Evaluation falls outside the committed predictive interval at the declared level; `OUTSIDE` when any single outcome lies beyond the committed tail bound; two consecutive `DEPARTED` → `Investigate` | A pre-committed check, not a regime model | Strategies, Hypotheses |
| Survivability bound | A subject's stress loss under `SS-1.0` at the proposed allocation may not breach any portfolio limit in force | Limits are the Principal's; ES-1 only requires the test | Allocation proposals |
| `UNESTIMATED` | No penalty and no privilege in evaluating the subject; recorded in `SELECTION OUTCOME` as "no estimate given" (UD-12) | An honest absence is not a defect of the idea | All |
| `SELECTION OUTCOME` timing | Computed whenever the lineage's Agent Design Evaluation is computed, and whenever a Transition cites the selection (UD-11); no separate schedule | Two triggers already in the doctrine | Agent Designs |

## 7. Resolution of the carried items

| Item | Resolution proposed |
| --- | --- |
| U-6 | This record |
| FR-6 | The mechanism field stays immutable as declared (PD-001 boundary). **Explanatory standing** of a Strategy Version is `DERIVED` from the standing of the Hypotheses it cites: `MECHANISM_UNTESTED`, `MECHANISM_SUPPORTED`, `MECHANISM_CONTRADICTED`. ES-1 reports it, extends the stress set with "mechanism absent" when contradicted, and sets `Investigate`; it changes no evidentiary minimum, because a mechanism is a reason to expect persistence, not evidence of it. A proposer who wants a new mechanism registers a successor at zero |
| FR-8 | Forward events only; `N_eff` minimum identical on both paths; the family counted across versions, lineages and Themes; exploratory records never counted |
| FR-9 | Method-class evidence and outputs in §4 |
| UD-11 | Two triggers, §6 |
| UD-12 | `UNESTIMATED` neutral; `T_total` counts every trial in the family regardless of path or estimate |

## 8. Three cases, illustrative numbers

Each case states the evidence, the applicable requirements, the primary
outcome, what remains uncertain, and the permissible Transition. Numbers
are illustrative.

### A. Traditional momentum: one winner from a thousand

Family `SF-8`: 1,000 Historical Reconstruction variants of
cross-sectional momentum over ten years of monthly rebalancing; the
best, `SV-8.7`, shows a backtest Sharpe of 2.1.

| Field | Finding |
| --- | --- |
| Evidence | R-2: 120 monthly Historical Reconstruction returns; grounding series empty. R-3: `N_raw` 120, `N_eff` ≈ 35 under the committed clustering method (crash and recovery episodes; overlapping 12-1 horizons). R-4: `T_total` 1,000, `T_forward` 0; under the committed multiplicity method the expected best Sharpe with no edge, given the variants' correlation, is about 1.4; reconciliation of 1,000 trials against consumption under `AU-27` closes. R-7 at any `a`: decision-series correlation with `SV-5.4` (`EP-19`) ≈ 0.8 in normal and stressed conditions. R-8: `FIRST` |
| Applicable requirements | Strategy column of the matrix: all ten; R-5 and R-6 computed on an empty grounding series are reported as such, not from history |
| Primary outcome | **Investigate**: what does `SV-8.7` do that `EP-19` does not? If a declared difference exists, **Incubate** at zero with the family disclosed and the method commitment fixed at registration. At monthly events, `N_eff ≥ 20` takes years; a weekly variant clusters the same way. `Explore on paper` only for operational measurement and the cost evidence Qualify will need |
| Uncertain | Whether any forward edge exists; the backtest selected a candidate and nothing more |
| Permissible Transition | A Research Authorization act for the question; a Strategy Version registration with the family and method commitment; no Allocation of purpose `QUALIFIED` |

### B. Forward research: product rebalancing flows

Theme `TH-14`; Hypotheses `HY-140`, `HY-141`, `HY-142`; Strategy
`SV-40.1`, 15:30 entries on qualifying days; no relevant history.

| Field | Finding |
| --- | --- |
| Evidence | R-2: no history exists or is needed; the forward record is the grounding series from the first Decision. R-3 after 20 qualifying days: `N_raw` 20, `N_eff` ≈ 12 under the committed method (days cluster around the product's rebalance calendar). R-4: three Hypotheses, about 45 Predictions, one Strategy, `UNESTIMATED` value estimate, neutral. Hypotheses under R-5 as calibration: `HY-140` 14 of 20 held against a 65 % falsifier, `N_eff` 12 → `UNDETERMINED` (stopping rule 40 days); `HY-141` 6 of 20 → heading to `CONTRADICTED`; `HY-142` one Outcome → `UNDETERMINED`. Strategy: decision-implied record positive gross and model-net, all Decisions `REPRODUCED`; break-even cost 9 bp per unit of turnover. Cost check: observed 15:30 to 16:00 spreads and depth for the index instruments put the checked cost range at 3 to 7 bp, modelled impact 2 bp, so the break-even lies above the range and the net record survives the committed conservative scenario at 7 bp. The exploratory record (`TR-415`) shows 4 bp simulator-relative shortfall: operational behavior, not a cost observation. R-6: the instrument class (the index's late-session trading) supplies the stress floor; "the product changes its rebalance rule" and "flows are front-run" are listed as not estimable. R-7: adds at any `a` within limits; no population exposure to this product. R-8: `FIRST` |
| Applicable requirements | Hypotheses: R-6 `N/A`, R-5 as calibration, R-7 as redundancy (`HY-140` and `HY-141` compete over the same resolution set under one `EXPERIMENT DESIGN`). Strategy: all ten |
| Primary outcome | Hypotheses: `UNDETERMINED` until their stopping rules. Strategy: **Incubate** (`N_eff` 12 < 20). If by day 40 `HY-140` reaches `SUPPORTED` while `SV-40.1`'s net record is about zero, the mechanism is real and priced in by 15:30: Hypothesis standing change to `SUPPORTED`; the Strategy incubates to its stopping rule and then **Retire**; `HY-141`'s earlier window is the question that accompanies the outcome |
| Uncertain | Whether twelve effective events reflect the product's steady state; whether flows persist as the product grows |
| Permissible Transition | Hypothesis standing changes at their stopping rules; later a `QUALIFIED` Allocation of bounded paper capital at `a ≤ a*` if `N_eff ≥ 20`, the stress floor passes and the checked cost scenarios leave the edge intact; had the checked range reached 9 bp, `Qualify` would be withheld and `Incubate` continued; retirement under the stopping rule |

### C. A profitable Strategy with dangerous tails

`SV-22.3`, a liquidity-provision Strategy: 60 scored forward Decisions,
`N_eff` 45, mean +1.2 % per month at the notional, Sharpe 2.5, worst
month −3 %, drawdown 4 %. Allocation 10 is proposed.

| Field | Finding |
| --- | --- |
| Evidence | R-5: the record's own tail ends at −3 %; a power-law exponent fitted to 60 observations has an unusable interval and the Evaluation says "tail beyond the sample: not estimable from the record". R-6 with the stress floor from the instrument class: volatility regime shift, loss ≈ 12 % of allocation; liquidity gap, ≈ 25 % with three days to exit at the committed depth assumption; discontinuity at three times the class's largest move, ≈ 40 %; correlated drawdown with `SV-5.4` and `SV-14.1`. R-7 **conditional**: in normal conditions the subject's decision series is nearly uncorrelated with the population and adds at every `a` up to the concentration limit; under the liquidity gap and the discontinuity it duplicates the losses of `SV-5.4` and `SV-14.1`; portfolio stress loss at `a = 10` ≈ 18 % against a 15 % portfolio drawdown limit; at `a = 3` ≈ 11 %. **`a* = 3`**. R-8: `WITHIN`; nothing has departed, which is exactly what a tail not yet seen looks like |
| Applicable requirements | Strategy: all ten; cost model checked against observed spreads, volume, depth and fees for the instruments; break-even 18 bp against a checked range of 4 to 8 bp, so costs do not threaten the edge and the tail does |
| Primary outcome | **Qualify at `a ≤ 3`**, with a standing `Investigate` on liquidity depth accompanying it and creating no standing. The Sharpe and the mean informed nothing about size; `a*` did. Had `SV-22.3` already held 10, the finding would be a limit breach under the stress set and the primary outcome **Reduce** to 3, regardless of statistical confidence in the mean |
| Uncertain | The true tail; whether the exit assumption holds in the gap; whether the class history contains the relevant event at all. No fitted distribution is claimed to forecast the discontinuity |
| Permissible Transition | A `QUALIFIED` Allocation Transition of 3 citing the Evaluation (Checker: forward class, `N_eff`, family, cost verification, `a*`, no exploratory figure); or an Allocation Transition reducing 10 to 3 |

## 9. Constitutional Delta

```text
ΔO: NONE. Evaluations, SELECTION OUTCOME, EXPERIMENT DESIGN and the
    Evaluation Standard already exist (§III.5, §III.9). Outputs,
    explanatory standing, a*, N_eff and method commitments are
    Evaluation content, registration content, Research Record content
    or DERIVED views.
ΔS: §III.9 Evaluation Standards: ES-1.0 content as §2 to §7 (the ten
    requirements with their applicability by population; the method
    commitment rules; the population output sets; the outcome table and
    the Transition classes each informs; the provisional constants with
    their bases, including the stress floor and NOT ASSESSABLE).
    §III.5 Evaluation record: the required content R-1 to R-10 with
    N/A marks; method versions pinned; FIRST and the limit-breach rule
    in R-8. §III.5 Research Record, kind EXPERIMENT DESIGN: meaning
    widened from "names a resolution set; precedes every Prediction
    over it" to also "names a subject's method commitment for a forward
    window; precedes every scored event of that window". §III.2, §III.3,
    §III.4 registration content: the initial method commitment (and,
    for Strategies, the cost model, already named in §6). §III.3
    Strategy: explanatory standing DERIVED (FR-6). §III.4 Agent Design:
    evaluation by method class (FR-9). Part V: Hypothesis standing
    change, Allocation and Retirement Checks verify ES-1 conformance
    (grounding forward only; N_eff floor; family reconciliation; method
    commitment sequence; cost verification against market evidence with
    simulated fills excluded; gross, model-net, break-even and scenario
    results present; stress floor and a*; no exploratory figure in
    grounding; disclosed method changes).
    Part VII: explanatory standing, the outcome, a* and N_eff as DERIVED
    rows.
ΔA: NONE. No method, score, evaluator or commitment record gains a
    decision right. Method commitments are written by the proposer at
    registration and by authorized agents as Research Records, both
    existing rights; the Checker's duties are extended as content of
    the existing Check; the Principal and admitted policy remain the
    only deciders. No registry exists.
```

Gap check: every committed method has an owner (the Transition ledger
for registration content; the Evidence ledger for a successor
commitment) and a commit boundary (the registration Transition;
Evidence commit). No workaround was needed; the only semantic widening
is `EXPERIMENT DESIGN`, declared above. Should the Principal prefer a
distinct kind for method commitments, that is `ΔO` +1 Research Record
kind and is otherwise identical.

## 10. Decisions for the Principal

| Question | Proposal |
| --- | --- |
| Admit ES-1.0 as the first Evaluation Standard by Constitutional Transition, with every constant in §6 labelled provisional | Yes |
| `N_eff ≥ 20` and `N_eff ≥ 12` as operational floors with no power claim | As drafted; revise by Constitutional Transition once a forward record exists to argue from |
| Method commitment carried by registration content and by `EXPERIMENT DESIGN` Research Records, replaceable by a successor commitment before the next window, with no registry | As drafted; the alternative, a distinct Research Record kind, is `ΔO` +1 |
| Cost verification: cost model and sensitivity method committed before the window; the Checker verifies against market evidence (spreads, volume, depth, fees) and distinguishes modelled impact and simulated fills; gross, model-net, break-even and conservative-scenario results reported; `Qualify` withheld when cost uncertainty could eliminate the edge; real cost validation deferred to an authorized execution phase | As drafted (Principal's clarification of 2026-10-19) |
| Conditional contribution with `a*`; qualification at `a ≤ a*`; one primary outcome with accompanying questions that create no standing | As drafted |
| Stress floor from the instrument class; `NOT ASSESSABLE` refuses `Qualify` and leaves `Incubate` and `Explore on paper` lawful; the three-times scenario retained as an unfitted class | As drafted |
| FR-6: explanatory standing derived; no minimum changes | As drafted |
| Whether `Qualify` may ever be informed by a Historical Reconstruction series | No, on either path (FR-8) |

## 11. What ES-1 cannot establish

That an edge exists. It can establish that a forward record of a
declared size, honestly counted across its family and net of declared
costs, has not yet been falsified, and what it would take to falsify
it. It cannot estimate a tail the record has not seen, forecast an
unprecedented discontinuity, detect a regime change before it shows in
outcomes, or prove that an agent disclosed every trial; it can only make
each absence visible and refuse to reward it.
