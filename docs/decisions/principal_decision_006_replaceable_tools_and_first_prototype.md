# Principal Decision Record 006 — Replaceable Tools and the First Prototype

Status: **ADMITTED 2026-10-19 by the Principal (document-phase admission), revision 2, the four decisions of §PD-006.4 as directed.** Applied to the Constitution as revision 7 and re-audited in [osa_reaudit_pd006_20261019.md](../audits/osa_reaudit_pd006_20261019.md). Admission text, as approved:

```text
ADMITTED 2026-10-19 by the Principal (document-phase admission): PD-006
revision 2, decisions 1 to 4.
(1) Principle 10, Tools are replaceable, as a New Speedway-specific
    standard: build the governed evolutionary process; reuse commodity
    computation.
(2) The two demonstrations: evolutionary historical research, then
    Forward Research and Themes. Historical replay and synthetic data
    never become prospective investment evidence.
(3) Delegated research admission requires D-10 and D-11 first.
(4) ConstitutionVersion 1 preferred before implementation; a bounded
    demonstration against the draft is a separately authorized
    fallback. A zero Constitutional Delta is not implementation
    authorization.
This is a document-phase admission, not a claim that a Constitutional
Transition executed before genesis.
Constitutional Delta: ΔO none. ΔS: Part IX principle 10; §III.5 content
of Historical Reconstruction research records; §III.5 rule that
reconstruction and synthetic data reject candidates but establish no
contradiction or fitness. ΔA none. Plan content: step 9 target and the
two proofs. Adoption record: a dated New Speedway standards section.
```

Prior content follows. Drafted
from the Principal's direction of 2026-10-19. Changes no Constitution
text until admitted; proposes one New Speedway operating principle
(Part IX) and one plan change. Depends on nothing beyond Constitution
revision 5. Revision 2 (2026-10-19) records the Principal's direction on
the four choices of §PD-006.4 and corrects Proof 1's evidentiary claim,
D-11's scope and the content of backtest Research Records, as directed.

Date: 2026-10-19 (revision 1: same day)

## PD-006.1. The rule, as the Principal stated it

> Commodity computational capabilities should be adopted as replaceable
> tools wherever possible. No external tool owns governed investment
> state, establishes its own evidence, or grants itself authority. Build
> custom infrastructure only when an OSA requirement cannot be satisfied
> through an existing component.

Proposed as **Part IX, principle 10, "Tools are replaceable"**, in those
words, with one sentence of consequence:

> A tool's output becomes Evidence only when a party authorized for that
> kind commits it at the Evidence boundary; until then it is `EPHEMERAL`
> or `CACHE` (Part VII), and a tool that cannot be replaced without loss
> of governed state has been allowed to own it.

This is a **New Speedway standard, dated 2026-10-19, originating with
the Principal**. It does not come from fin123-core and the
[adoption record](fin123_core_adoption_20261018.md) is not rewritten as
though it did; on admission that record gains a dated section, "New
Speedway standards added after adoption", listing principle 10 with its
source as this decision. The rule is also added to
[plan step 9](../plans/document_first_design.md) as the burden of proof
for any custom component: name the OSA requirement no existing component
satisfies. The Principal's governing engineering statement: *build what
makes New Speedway different; reuse or simulate everything else.*
Backtesting, historical replay, paper fills, market data and stress
simulation are replaceable tools; New Speedway owns Themes, Hypotheses,
Strategies, Agent Designs, Evidence, lineage, Authorizations,
Transitions and capital decisions.

### OSA consequences

| Question | Finding |
| --- | --- |
| Does the rule conflict with revision 5? | NO. It restates, for architecture, what I-6 (authority is granted), I-13 (derived representations have no vote) and Part VII (market data store `CACHE`; backtest outputs `EPHEMERAL`) already require. Its new content is a preference order, adopt before build, and a burden of proof |
| What counts as a tool? | Backtesters, data vendors and stores, hosted model providers, schedulers, databases, message systems, simulators, notebooks. Each may carry a governed fact as `CACHE`, `DERIVED`, `RECEIPT` or `EPHEMERAL`; none is `AUTHORITATIVE` for anything, none commits Evidence, none decides |
| Does it bear on provider substitution? | YES, consistently with PD-002.6 and D-14: the provider is provenance on the Agent Design Version, never authority; substituting it is a governed event (adoption record, separation principle), not a loss of state |
| Delta | `ΔO` none. `ΔS` one Part IX principle; one dated New Speedway standard appended to the adoption record; one plan rule; the backtest Research Record content below. `ΔA` none |
| What must a backtest Research Record identify? | The exact historical dataset or snapshot (identity and content hash), the source cutoff (the as-of beyond which nothing was read), every parameter, the backtester's version and content hash, and a **reproducibility binding**: the closure under which a second run must yield the same result hash. This is Research Record content under §III.5 (closure, typed claims); the backtester owns none of it |

## PD-006.2. The first prototype, redirected

The Principal's preference: demonstrate ten agents generating,
challenging and replacing Hypotheses through one simple backtester,
rather than spend a week building a better backtester.

This is a **Historical Reconstruction loop**, and the doctrine is exact
about what it can and cannot show. It can show the governance loop
working: Themes and Hypotheses proposed under Authorizations with
budgets, Research Records with closures and typed claims, search
families and selection bases, lineage memory that no successor can
shed, Checks that refuse restatements and unreconciled families,
registrations decided and preserved, negative results kept, successors
at zero. It cannot show an edge, and no backtest it runs grounds any
standing (I-2, I-3, doctrine §9). **Historical Reconstruction can reject
a research candidate and motivate succession; it cannot establish
prospective contradiction or fitness.** A Hypothesis set aside on
reconstruction is *rejected as a candidate* or *abandoned*, with the
negative Research Record preserved; it is not `CONTRADICTED`, a standing
earned only from forward Outcomes under `ES-1`. That is the correct
content of a first prototype: the asset being tested is the governed
process, not a strategy.

What the prototype as described requires, from the Constitution as it
stands:

| Requirement | Why | Status |
| --- | --- | --- |
| `ConstitutionVersion 1` admitted, or a Principal authorization of a bounded prototype with its own declared `0/0/0` delta against revision 5 | `AGENTS.md`: no application code until the Constitution is coherent in documents; the plan admits an implementation plan only after step 9 and admission | Open; the Principal's decision |
| Ten Agent Design Versions under Research Authorizations with discovery scope, budgets and a declared method class | §III.4, §III.7; agents hold no authority of their own | Expressible now |
| A Checker, human or an Agent Design Version under a Checker Authorization, independent of every proposer's lineage | Part V: every registration is checked | D-10 (Checker sufficiency) is open; a human Checker needs no decision |
| A decider for every Hypothesis registration and standing change | Part V: the Principal, or an admitted policy; no policy exists | **Ten agents replacing Hypotheses will produce more registrations than a human decides by hand.** Either the Principal decides each, or D-11 (admitted policy) is drafted first. D-11 is therefore the gating decision for this prototype, ahead of plan step 7. Delegated registration must serve both Hypotheses under active Themes and Hypotheses in authorized empirical search families with no Theme (PD-003.5's empirical path) |
| The backtester as a replaceable tool | PD-006.1: its runs are Research Record content of class Historical Reconstruction under a declared closure; it commits nothing | Expressible now |
| Observations for the backtests | A declared source under an Observation Authorization, retrieved by the Observation function, or a market data store read as `CACHE` for research with nothing established | Expressible now |
| Genesis (N-1) | The first Transition has no base; the bootstrap must be stated before any ledger exists | Open; plan step 4 or 8 |

Not required by this prototype: the Strategy Runner, Decisions, the
Paper Book, PD-004's expiry machinery, `ES-1`'s Strategy outputs. They
are exercised by a second prototype once a forward record is wanted.
`ES-1`'s Hypothesis and Agent Design outputs are exercised by the first.

### Proposed plan change

Plan step 9 gains a **first prototype target**: the minimum governed
research loop above, on commodity components, with the implementation
plan's first deliverable a mapping of every governed fact the loop
touches to one authority, one commit boundary and classified carriers,
and a list of the components adopted with the OSA requirement each
satisfies. Ordering of the remaining decisions: PD-005 (`ES-1`), then
D-11 with D-10 (plan step 5), then N-1 (genesis), then `ConstitutionVersion 1`.

## PD-006.3. Two demonstrations (Principal direction, 2026-10-19)

The purpose of both is to demonstrate the operating system, not alpha.
Both run on the same governed state and authority rules. Neither needs
streaming data, broker integration, exchange simulation or a custom
backtesting framework.

**Proof 1, evolutionary research.** Ten Research Agents (Agent Design
Versions under Research Authorizations with budgets, discovery scope
and method class) propose, challenge, test, mutate and retire
Hypotheses through one replaceable backtester over historical or
synthetic data. Must demonstrate: research abandonment and candidate rejection on
reconstruction, each preserved as a negative Research Record; lineage
memory that no successor can shed (I-5); budgets consumed and refused at
the ceiling; independent Checks that refuse restatements, unreconciled
families and out-of-scope closures; agent succession at zero with memory
intact; replacement of rejected candidates by new ones, with the
rejected ones kept. Evidentiary rule: every backtest is Historical
Reconstruction even when data is revealed sequentially, because the
Hypothesis was authored knowing the period; it can reject a candidate
and motivate succession but establishes no prospective contradiction and
no fitness; synthetic data tests system behavior and never becomes
prospective market evidence. No evidentiary standing is manufactured;
every Evaluation says so. Each backtest Research Record identifies the
exact dataset or snapshot, the source cutoff, the parameters, the
backtester version and its reproducibility binding (§PD-006.1).

**Proof 2, forward research and Themes.** Agents encounter a previously
unseen, synthetic market development through a declared feed (PD-003:
screens, hop rule, `DOCUMENT` Observations with closures), investigate
it within discovery scope, register a Theme with a motivation closure
and selection basis, develop competing Hypotheses under one
`EXPERIMENT DESIGN`, write an executable Strategy Version (registered,
`INCUBATING`, zero capital), and select the next research question as a
`SELECTION` Research Record with estimates or `UNESTIMATED`. Must
demonstrate: that the system generates questions from a development
rather than searching price relationships; formation evidence kept
disjoint from resolution sets; typed claims; the selection history
derivable in full. Because the development is synthetic, its
"resolution" is a test of the machinery, labelled as such; no
Contemporaneous Forward Record is claimed.

Neither proof exercises the Strategy Runner, Decisions, the Paper Book
or PD-004's expiry rules; a third demonstration would, once a genuine
forward window is wanted.

## PD-006.4. Decisions for the Principal, with the Principal's direction of 2026-10-19

Directions are recorded; admission is a separate act.

| Question | Proposal | Principal's direction |
| --- | --- | --- |
| Admit principle 10 in Part IX as a New Speedway-specific standard | Yes | **Admit**, as a New Speedway-specific standard |
| Adopt the two narrow prototype demonstrations (§PD-006.3) as the step 9 target | Yes | **Adopt** |
| Decide every registration by hand in the first prototype, or draft D-11 (admitted policy) first | Draft D-11 with D-10 first | **Draft delegated admission and independent checking before implementation** (PD-007) |
| Admit `ConstitutionVersion 1` before the prototype, or authorize a bounded prototype against revision 5 | Admit `ConstitutionVersion 1` after PD-005, PD-007 and N-1; a bounded authorization is the fallback | **Prefer an admitted CV-1 before code**, with a separately authorized, non-conforming demonstration as fallback. A zero Constitutional Delta is not implementation authorization in either case |
