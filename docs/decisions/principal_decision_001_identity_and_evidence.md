# Principal Decision Record 001 — Identity and Evidence Foundations

Status: **ADMITTED 2026-10-18 by the Principal, for D-03, D-07 and D-08
including the dependent D-02 and D-05 consequences, subject to the
clarifications below.** The Constitution as a whole remains a draft; this
record admits only these dispositions.

## Principal's clarifications on admission (2026-10-18)

These control where they differ from the proposed text below.

1. **D-07.** The admitted Transition history is authoritative for population
   membership, standing, allocation, limits and currentness. Population
   State is a derived projection with no independent authority. Historical
   interpretation uses the Constitution and Evaluation Standards effective
   at the original admission. The Paper Book remains separately
   authoritative for paper orders and fills.
2. **D-03.** Economic proposition identity is governed by explicit meaning
   boundaries. Implementation may change without changing economic
   identity, but equivalence must be independently established. Lineage
   never automatically transfers evidence, fitness or capital authority.
3. **D-08.** Prospective evidence requires independently established
   information availability, prediction commitment and outcome
   availability. Publication schedules may inform availability but cannot
   establish it alone. Where precedence cannot be demonstrated, refuse
   prospective classification. I-2 is revised accordingly.

Directions for later design work, not admitted dispositions:

- **D-12** must distinguish research resources consumed during execution
  from capital and allocation budgets consumed at admission. The mechanism
  is not to be resolved prematurely.
- Forward-research origin is not itself a disqualifying risk category.
  Uncertain strategies are governed by evidence, uncertainty and portfolio
  risk.
- **D-10, D-11 and D-17** remain design directions, not admitted
  constitutional dispositions.

Applied to the Constitution in revision 2 of 2026-10-18; re-audited in
[the PD-001 re-audit](../audits/osa_reaudit_pd001_20261018.md).

## Proposed text as submitted

Subjects: audit defects D-07, D-03, D-08, with D-02 and D-05 resolved as
consequences; early direction on D-10, D-11, D-17; one standing design rule.

Source: [initial OSA audit](../audits/initial_osa_audit.md);
[Constitution draft](../doctrines/new_speedway_constitution.md).

## PD-001. Authority of history (D-07)

**Disposition.** The admitted Transition history is the sole authority for
governed state. Population State at version N is a reproducible projection
of that history and is classified `DERIVED`. "Current" means the projection
at the head of the applied history.

**Defect this corrects in the draft.** The summary table lists "Population
State (standing)" and "Population State (standing, allocation)" as
authorities while §III.6 says the applied Transition subsequence defines
Population State. That is two names for one authority at best and two
authorities at worst. The revision replaces every authority-column reference
to Population State with "applied Transition history, projected as
Population State".

**Pinning rule.** Every applied Transition records the `ConstitutionVersion`
and `EvaluationStandardVersion` in force at its Apply. Replay interprets each
Transition under its pinned versions. Today's Constitution never reinterprets
yesterday's authorized decision. A Constitutional Transition changes the
interpretation of Transitions applied after it only.

**Consequences for other sections.** Materialized Population State records
are `DERIVED` or `CACHE` and may be discarded. Recovery is replay to the head
under pinned versions. Challenge 10 (accidental restoration) is answered by
the pinning rule plus I-11. The alternative (state versions authoritative,
Transitions as receipts) is rejected and preserved in the audit.

**Two-case test.**
- *Traditional:* a 12-1 month momentum Strategy Version is allocated at
  Transition 300 under Evaluation Standard v2. Standard v3 later changes the
  Sharpe window. Replay of Transition 300 still shows the v2 assessment it
  was decided on; the v3 assessment appears only as a new Evaluation at a
  later state.
- *Forward:* a dealer-gamma Hypothesis is admitted at Transition 310 under
  Constitution v1, which permits a non-price resolution source. Constitution
  v2 later tightens source rules. Transition 310 remains lawful as applied;
  a new Hypothesis under the same Theme must meet v2.

**Constitutional Delta (relative to the draft).**

```text
ΔO: NONE. No object added or removed.
ΔS: Population State meaning narrowed to "projection of applied history".
ΔA: Authority for membership, standing, allocation, limits and currentness
    moves from "Population State" as drafted to the applied Transition
    history. Apply remains the single commit boundary.
New representation: pinned ConstitutionVersion and
    EvaluationStandardVersion on each applied Transition (part of the
    AUTHORITATIVE record, not a new carrier).
```

## PD-002. Economic identity (D-03)

**Disposition.** An Economic Proposition declares five immutable boundaries
at registration:

| Boundary | Meaning |
| --- | --- |
| Mechanism | The inefficiency or behavior exploited, or "none claimed" for an empirical Strategy |
| Prediction target | What the Strategy claims will happen: the observable and its direction |
| Market or domain | Instruments, universe, venue |
| Horizon | The holding or prediction horizon band |
| Payoff | What is earned when the claim is right, and the shape of loss when it is wrong |

`Proposition delta: NONE` is lawful only when all five boundaries are
unchanged. Any change to any boundary is `Proposition delta: NEW`: a new
`EconomicPropositionId`, successor at zero, lineage preserved.
Implementation facts (parameter values, rebalance frequency, signal
construction, execution rules) may change within a proposition unless the
change moves a boundary. The Checker verifies the declaration against the
five boundaries, which makes challenge 3 checkable rather than arguable.

**Two-case test.**
- *Traditional:* momentum, US large-cap equities, 1 to 3 month horizon,
  long-short payoff. Changing the lookback from 12-1 to 6-1 is `NONE`
  (parameter within the mechanism). Changing the universe to small caps is
  `NEW` (market boundary moved).
- *Forward:* mechanism "dealer hedging flow amplifies realized variance",
  target "realized exceeds implied", market "index options and futures",
  horizon "5 sessions", payoff "long variance". Replacing the variance
  instrument with a directional index position is `NEW` (payoff moved),
  even if the signal is identical.

**Constitutional Delta.**

```text
ΔO: NONE. EconomicPropositionId already exists in the draft.
ΔS: Economic Proposition gains five required immutable boundaries.
ΔA: NONE. Checker verifies; Principal decides disputes, as drafted.
```

## PD-003. The evidence clock (D-08, resolving D-02 and D-05)

**Disposition.** Three times are recorded, each with a named authority:

| Time | Meaning | Authority |
| --- | --- | --- |
| Information availability time | When a source's value for a period became knowable, per the source's declared publication rule | The resolution source declaration made at Hypothesis or Strategy Version registration |
| Prediction commitment time | When the Prediction was committed | The Evidence commit boundary's declared clock, never the proposer's |
| Outcome observation time | When the resolving value was taken from the source | The Evidence commit boundary, bound to the Market Observation it took |

A Prediction is **Contemporaneous Forward Record** only if its commitment
time precedes the information availability time of every value needed to
resolve it. Otherwise it is **Historical Reconstruction**. The system never
asks the proposer which class applies.

**D-02, straddling windows.** A window is forward only if no part of it had
become available at commitment. A window with any available part is
Historical Reconstruction in full. A proposer who wants a forward record
commits before the window opens.

**D-05, source revisions.** The resolution source declaration states which
print resolves the Prediction: first print or a named final. The Outcome
binds the Market Observation of that print. A later restatement is a new
Market Observation; it does not alter the Outcome and cannot be used to
recompute it.

**Two-case test.**
- *Traditional:* daily close prices, available at the exchange's published
  close time. A Prediction for Friday's close committed Thursday is forward;
  committed Friday after the close it is reconstruction, even if no Outcome
  has been committed yet.
- *Forward:* dealer gamma estimates published by source S at 18:00 each
  session. A Prediction for Monday committed Monday 17:30 is forward; at
  18:30 it is reconstruction. If S later restates Monday's value, the
  Outcome stands on the print the declaration named.

**Constitutional Delta.**

```text
ΔO: NONE unless the Resolution Source declaration is promoted to a governed
    object at plan step 2; this record keeps it as a required part of
    Hypothesis and Strategy Version registration.
ΔS: Evidentiary class determination now has an exact rule.
ΔA: The Evidence commit boundary's declared clock becomes the authority for
    commitment and observation time. No new carrier.
```

## Early direction, not yet dispositioned

These are the Principal's directions for later plan steps. They bind the
design direction and will be dispositioned in their own decision records.

- **D-10, Checker independence (plan step 5).** Independence is not a
  property of names, lineages or model providers. It comes from separate
  decision authority, evaluation rules the implementing agent cannot change
  (I-7), and evidence the implementing agent cannot rewrite (the Evidence
  ledger's commit boundary). The Checker contract will be specified in those
  terms.
- **D-11, Principal bottleneck (plan step 5).** The target is an autonomous
  process, not human approval of every experiment. The Principal will
  authorize bounded admission policies under which routine Transition
  classes are admitted without a per-instance decision. Changing a policy or
  widening authority is a separate approval, always by the Principal.
- **D-17, crash before Apply (plan step 4).** Three durable standings are
  distinguished: a verified proposal (`CHECKED PASS`), an admitted change
  (`DECIDED ADMITTED`, a durable event on the Transition ledger), and an
  effective change (`APPLIED`). After a crash the system must know which of
  the three holds, must not lose an admitted Transition, and must not apply
  it twice. This is the first CPOC witness to write.

## Standing design rule adopted

> A document can be internally consistent and still describe the wrong
> system.

OSA audits establish constitutional coherence. Investment usefulness is
established by examples. Every major schema decision is tested against at
least two cases: a traditional price and volume research experiment, and a
forward-research Theme that generates new Hypotheses and Strategies. This
rule is added to the plan.

## What happens on admission

1. Revise the Constitution: summary table authority column; §III.6 (history
   as authority, projection, pinning); §III.3 (five boundaries); §III.5 and
   I-2, I-3 (three times, class rule, print declaration); §VII (materialized
   state as `DERIVED` or `CACHE`); T-A, T-B worked examples re-run under the
   two-case test.
2. Re-audit the revision for ownership and semantic conflicts introduced by
   the change, and close D-02, D-03, D-05, D-07, D-08 in the register with
   references to this record.
3. Only then open plan step 3 (authority and change budgets).
