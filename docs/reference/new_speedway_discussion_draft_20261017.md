# New Speedway — Client Discussion Draft (17 October 2026)

Status: **REFERENCE — CLIENT-FACING DRAFT. Not doctrine. Not governed.
Filed 2026-10-18 by the Principal for comparison against the
Constitution.** Where this draft and the
[Constitution](../doctrines/new_speedway_constitution.md) differ, the
Constitution governs the design; proposed corrections to this draft are in
[the forward research design plan](../plans/forward_research_design_plan.md).

Text below is as supplied by the Principal on 2026-10-18. Tables were
tab-separated in the original and are rendered as Markdown tables. Figures
are not included.

---

Codename: New Speedway
An operating system for an evolving investment process
Reckoning Machines | Discussion draft for Brett and David | 17 October 2026

## New Speedway

Here is something nobody could do before generative AI.

Build a quantitative investment operating system that can run and improve its own research process.

It can investigate changes in the world, generate hypotheses about how markets might react, write and test trading strategies, and design better agents to replace the ones doing the research.

Three ideas:

1. Decay is a feature, not a failure. Every edge is temporary. Strategies should come and go. So should the research methods that discover them.
2. State, not Agents. The durable asset is the record of what the system believed, tested, traded, and learned. Every consequential change has a budget and must fit the rules governing the investment system.
3. Forward Research and Themes. Traditional quant searches historical data for relationships that might persist. New Speedway also asks what is changing now, what might happen next, and how those changes could show up in prices and money flows.

The trading remains quantitative. What changes is how the system finds ideas worth testing.

A faster quant OODA loop is useful, but it largely scales the existing research process. The larger ambition is a system that can evolve its research methods and decide which new questions about markets are worth asking.

The strategies are disposable. The research process, its evidence, and its ability to evolve are the assets.

## RESEARCH – CURRENT STATE OF THE FIELD

TLDR: the parts exist but nobody's put it all together.

Automated quant research, evolutionary coding and self-improving agents are already real.

The design question is whether they can become one investment process that keeps learning as conditions change. Sources reviewed 17 October 2026.

### Automated quantitative research

An automated quant loop is an existing capability.

R&D-Agent-Quant links hypothesis generation, coding, backtesting and feedback. It searches across factors and models and adapts its research direction. [1]

My note: This is close to our separation of research freedom from evaluation authority:

Sadeghi's October 2026 working paper, Agents Propose, Code Decides, describes agents building an equity alpha model under fixed evaluation rules. Its abstract reports frozen data and predefined acceptance criteria. [2]

My note: This is close to what our first two levels require:

Google - AutoScientist-Quant goes further: it treats quant research as one budgeted evolutionary search, with shared memory, search decisions and protected evaluation windows. [7]

### Evolution of code and research agents

AlphaEvolve uses language models to modify algorithms and evaluators to select improvements. It demonstrates that this evolutionary process can solve computational problems. [3]

My note: our challenge is different: in markets, the conditions under which a solution works can disappear.

The Darwin Gödel Machine evolves the coding agents themselves and retains an archive of alternatives. Its evidence comes from coding benchmarks. [4]

My note: this gives us a precedent for making the research machinery replaceable.

### Other thoughts

Bailey and coauthors show how selecting among many historical trials can produce attractive backtests that fail out of sample. [5]

Adaptive conformal inference can help maintain long-run prediction coverage as distributions change. [6] It offers a way to monitor forecast uncertainty.

Our proposed difference is not more agents or faster back tests but rather the gen-ai coding angle: one "governed" record linking forward themes, testable hypotheses, trading strategies, agents that can improve themselves, and the capital decisions that follow.

## 2 Design principles

1 Expect decay
Assume that strategies and research methods will stop working. Monitor the evidence, investigate deterioration and reduce or retire exposure under agreed rules. Detection will sometimes follow losses.

2 Evaluate each population separately
Judge a hypothesis by its predictions, a strategy by its economics and portfolio contribution, and an agent by the quality and cost of its research. A correct hypothesis can produce a losing strategy, and a profitable strategy can have the wrong explanation.

3 Preserve the original claim
A changed hypothesis gets a new identity linked to its parent. Keep each exact strategy and agent version. Descendants can use earlier work, but must earn their own evidence and authority.

4 Allow both discovery paths
Forward research and themes start with changes in mechanisms, flows, positioning or market structure and turn them into testable ideas. Empirical research starts with a pattern in the data. Both paths are valid. An unexplained pattern should remain unexplained until evidence supports a mechanism.

5 Record what learning changed
Learning must change something: a belief, the next experiment, an allocation or the research method. Record the change and its basis. The loop can learn this way without retraining a model.

6 Match evidence to consequence
Allow speculative themes. Require testable hypotheses and executable strategies. Apply portfolio limits even on paper. Moving to real capital requires a separate decision.

7 Give humans visibility and control
Show the work, its cost, its failures and the decisions it produces. Let people pause, redirect or stop it. Record their interventions alongside the system's decisions.

8 Netting Risk: Check the combined portfolio
Two good strategies can make one bad portfolio. Check shared exposure and budgets when changes are admitted, including other changes accepted in the meantime.

## 3 The nine durable objects

The first four are the things that evolve. The other five preserve what happened and govern what may happen next. An agent run is just an actor, it is not the enduring state. Predictions, experiments and observations are records within Evidence.

| Object | Required content | Admission or mutation rule |
| --- | --- | --- |
| Theme | Scope, questions, sources, owner and research budget. | May be speculative; revisions retain prior scope. |
| Hypothesis | Immutable claim, conditions, universe, horizon, comparator and disconfirmation test. | Material meaning change creates a descendant identity. |
| Strategy | Economic purpose; exact signal, sizing, execution, cost and risk specifications. | Executable revisions; explicit rationale or empirical origin. |
| Agent design | Research method, model, instructions, tools, evaluation policy and permitted capabilities. | Successors are evaluated before expanded use; each assignment is attributable. |
| Evidence | Commitment, experiment, data manifest, observation or assessment; exact subject references. | Append-only; corrections and invalidations point to originals. |
| Population state | Membership, lifecycle, budgets, paper allocations and exposure snapshot. | Derived from admitted transitions; revisioned and replayable. |
| Authorization | Actor, permitted actions, scope, limits, expiry and issuer. | No implicit inheritance or self-expansion. |
| Transition | Before-state, proposal, affected objects, checks, decision and resulting state. | Admission considers the actual current population. |
| Constitution | Object meanings, relationship meanings, invariants and mutation rights. | Separately versioned; explicit human approval for changes. |

### What survives a rewrite

Lineage identity can survive a complete change in code, but Strategy identity cannot silently survive a material change in the economic idea or trading contract.

Revisions remain exact meaning that retirement never removes the evidence.

### Evidence is more than a result cache

Keep the exact question, data, information cutoff, evaluation rule and related trials and link each conclusion to the evidence behind it. Reusing an old result saves work, but it does not add evidence.

## 4 Lineage and evidence answer different questions

Lineage tells us where an idea came from. Evidence tells us what we have learned about it. One hypothesis can motivate several strategies and several hypotheses can motivate one strategy.

Those connections must remain explicit.

Figure 1. Illustrative explanatory graph. H1 and H2 can motivate the same strategy. Evidence explicitly identifies its subject but does not automatically validate the whole connected graph.

| Relationship | Precise meaning |
| --- | --- |
| motivated_by | A source of rationale - does not establish that the rationale is correct. |
| tests or evaluates | An experiment or assessment bears on exact subject revisions under a stated protocol. |
| descends_from | Ancestry only; no transfer of confidence, permissions or capital. |
| produced_by | Attribution to a specific agent run and design revision - no certification implied. |
| overlaps_exposure | A measured or hypothesized shared risk, with source, date and uncertainty. |

These relationships form a graph, not a family tree. Shared ancestry does not make two strategies independent, and separate ancestry does not make them diversified.

## 5 Every change must fit its authority and budget

Figure 2. A proposal becomes operational only after independent checks and composition against current state. Rejections remain part of the record. HIL acts through authorized transitions.

### Agents can change the population within agreed rules

The Constitution defines what objects mean and who may change them. An agent can create a hypothesis or revise a strategy within those rules, but it cannot redefine evidence, widen its authority or change the standard by which its own work is judged… those changes require explicit approval.

### Evaluation is separate from proposal

A proposer cannot certify its own success – we will evaluate its work under rules fixed before the result. Another agent can challenge the reasoning, but agreement between agents is no substitute for a test.

### Check changes together

Check each proposed change against the population the moment it is admitted, and if another strategy has used the remaining risk budget, the second proposal must be rechecked. Reason: Two valid back tests can create one bad portfolio.

This is a composition and authority check, not CPOC. Cross-Process Operational Continuity asks a different question: after process death, can the system recover its lawful next action using durable state alone? Paper orders, positions and research decisions must survive restart without duplication or rewritten history. Neither check proves the strategy has an edge.

## 6 A worked research example

A hypothetical research program on forced selling by volatility-targeting funds.

### Theme and committed hypothesis

Theme T1 asks whether changing volatility-control participation creates predictable equity selling.

H1 states: when a prespecified volatility-targeting model calls for an exposure reduction in its top historical decile, next-session signed equity-flow pressure will be more negative than a predeclared matched baseline.

The formula, sample rules, data proxy, cutoff and test horizon are frozen before the observation window begins.

If direct flow observations are unavailable, the system records a proxy limitation. A negative equity return alone does not establish that volatility-targeting investors sold. Missing observations are marked "not scored."

### Two strategies and separate assessments

| Object | Test | Possible result and response |
| --- | --- | --- |
| H1 | Does the prespecified flow relationship appear prospectively? | Support rises if the flow test passes but causal attribution can remain uncertain. |
| S1 | Trade anticipated pressure after the signal is available, net of modeled costs. | Flow effect exists but S1 loses after costs: reduce or retire S1; retain the H1 evidence. |
| S2 | Trade a reversal under separately committed exhaustion conditions. | S2 profits while H1 fails: preserve the P&L, challenge its rationale and investigate alternatives. |
| Agent A2 | Compare its competing-explanation method with A1 on new, matched tasks. | Promotion depends on research quality and cost, not its count of appealing backtests. |

### What happens when the explanation changes

If evidence suggests the effect occurs only during liquidity withdrawal, create H3 with that narrower condition, but importantly, H1 and its failed predictions remain. Earlier data can motivate H3, but cannot also be presented as validation of H3.

### A simpler first demonstration using RSI

Translate "test RSI" into a fixed formula, universe, availability time, holding period, baseline and cost model. Record every parameter trial in one search family.

A successful demo would show the system specifying the question, running it reproducibly, rejecting or qualifying the result, and choosing the next experiment from the accumulated evidence. No favorable backtest required.

## 7 Evidence determines what to investigate next

Figure 3. Agent designs, hypotheses and strategy implementations evolve on distinct lineage paths. An agent can produce a successor hypothesis without altering the original claim.

### Choose the next experiment

Research new ideas, replication and challenges to existing beliefs.

Prioritize work that could change a decision enough to justify its cost.

Record why it was selected, then judge whether that choice was useful.

At Pfizer, I used value of information to decide what was worth learning next. The same question applies here, though the complication is that markets and the research opportunity set keep changing.

The policy for choosing research must, therefore, be tested and replaced like any other method.

### Control repeated searching and information leakage

Record when source information became available, when it was ingested, when a prediction was committed, when its outcome became observable, and when evaluation feedback was released. Track every failed trial and every exposure to held-out results. Related experiments share a search-family identity – but spawning another agent does not reset the search history.

Freeze evaluation rules before each forward window. Compare method revisions on new tasks with matched budgets and data access. Historical replay remains useful for engineering, but an LLM may already know historical events. Fresh forward observations provide the strongest practical separation.

Conformal methods may monitor forecast uncertainty and realized coverage where suitable. [6]

## 8 Humans must be able to follow and direct the work

HIL: We need to see what the system is doing while it runs. For any material decision, we should be able to inspect the evidence, the alternatives and the uncertainty, then intervene if needed.

| Operator view | What it must answer | Available action |
| --- | --- | --- |
| Live work | What is running, queued, stalled or waiting? Why was it selected? Who owns it? | Pause, cancel, reprioritize or inspect a run. |
| Research graph | Which ideas are new, supported, challenged or superseded? What changed since yesterday? | Open exact claims, ancestry and conflicting evidence. |
| Decision record | What was proposed, accepted or rejected, by which rule and evaluator? | Require review, annotate or propose an authorized reversal. |
| Evidence timeline | What was known and committed before the outcome? Is data stale, revised or missing? | Inspect sources, replay a result or invalidate defective evidence. |
| Paper portfolio | What positions exist, why, and with what gross, net, factor and shared-flow exposure? | Freeze new orders, adjust approved limits or request paper liquidation. |
| Spend and health | Tokens, tool charges, compute, run duration, failures and remaining budget. | Cap a branch or the whole system; stop new work. |

### Show material changes first

The home view shows active work, material changes, open decisions, portfolio exposure and daily spend. A daily digest links to the same records. Alerts focus on budget exhaustion, stale data, repeated failures, an invalidated result, a breached limit or an assessment change that affects allocation. Routine tool chatter stays in drill-down logs.

### Make interventions explicit

Pause stops new work and new paper orders. Cancel requests termination of running work and reports whether it succeeded. Paper liquidation is a separate recorded action. A return to an earlier strategy revision creates a new transition - it never deletes intervening evidence. Display acknowledgement, scope, time and resulting state for every intervention.

### Set the bounds and supervise

Within approved bounds, routine research and paper operation proceed automatically. Humans approve initial scope and limits, new data access, material evaluator changes, authority expansion and any move to real capital and can inspect or intervene at any time. A human override records who acted and why.

## 9 What paper trading should teach us

Start on paper to answer two questions: is the system making better research decisions, and how much trading activity does it produce?

### Important: Evaluate research quality separately from simulated performance

Look for precise questions, honest treatment of failed tests and sensible choices about what to investigate next.

Check whether the system changes its mind when the evidence changes.

A decision not to trade is a useful thing to know.

Use cost ranges until we know enough about the trading activity.

### Measure the activity before sizing execution

| What to observe | Why it matters later |
| --- | --- |
| Trading frequency and clustering | Average activity can hide bursts of simultaneous orders or amendments. |
| Turnover and holding periods | Frequent trading creates different cost and execution demands from slow rebalancing. |
| Order sizes and traded instruments | Liquidity, venues, financing and execution requirements depend on what is traded and how much. |
| Gross and net strategy activity | Opposing strategy orders may offset at portfolio level. Both views are needed to understand activity and costs. |
| Timing sensitivity | An edge that survives delayed execution has different infrastructure needs from one that disappears quickly. |
| Shared exposure and stress behavior | Different agents or hypotheses can generate the same economic trade at the same moment. |

### Live execution is a separate system requirement

Live trading requires an API-driven market and execution system that can handle the volume.

We do not yet know how much this system will trade, so a commission estimate – too early to tell. The same applies to spread, slippage, market impact, financing and borrow costs. Actual fills will still need to be tested. I've seen beautiful paper systems completely choke for a week or two before standing up cleanly.

## 10 Sources

The cited work supports the research discussion. The schema and examples describe the proposed New Speedway design.

[1] Li et al. R&D-Agent-Quant. 2025; revised 25 September 2025; NeurIPS 2025. Hypothesis, development and feedback loop. https://arxiv.org/abs/2505.15155

[2] Erfan Sadeghi. Agents Propose, Code Decides. Written 5 October 2026; posted 7 October 2026. SSRN working paper. Review limited to the accessible abstract. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7568638

[3] Novikov et al. AlphaEvolve. 16 June 2025. Evolutionary coding with automated evaluators. https://arxiv.org/abs/2506.13131

[4] Zhang et al. Darwin Godel Machine. First submitted 29 May 2025; revised 12 March 2026. Evolution of coding agents. https://arxiv.org/abs/2505.22954

[5] Bailey, Borwein, López de Prado and Zhu. The probability of backtest overfitting. Journal of Computational Finance, 2017. Author manuscript in UC repository. https://escholarship.org/uc/item/4w1110bb

[6] Gibbs and Candès. Adaptive Conformal Inference Under Distribution Shift. 2021. Online prediction sets and long-run coverage. https://arxiv.org/abs/2106.00170

[7] Li et al. AutoScientist-Quant: Self-Evolving Coding Agents for Automatic Research in Quantitative Investment. 5 August 2026. Budget-aware research search, shared memory and protected evaluation. https://arxiv.org/abs/2608.28632

[8] OpenAI. GPT-5.6 Terra and Sol API pricing, accessed 17 October 2026. Terra $2 input / $12 output per million text tokens; Sol $4 / $20, below long-context thresholds. https://developers.openai.com/api/docs/pricing

## 11 Time and Money: Start on paper, then decide what to spend

I built Pfizer's model in 48 hours. I would aim for a New Speedway demonstration in two or three focused days and a narrow, supervised paper system within one to three weeks. That is a software schedule, not a claim that we discovered alpha!

| Stage | Rough elapsed time | What the period could establish |
| --- | --- | --- |
| First working demonstration | A few focused days | One question carried through a test, evidence record and next research decision, with human visibility. |
| Supervised paper system | Approximately 1–3 weeks from start | A coherent research loop and observable paper portfolio operating within agreed limits. |
| Initial forward review | Approximately 4–12 weeks of paper observation | Research usefulness, trading activity, operating behavior and early prospective evidence. |

### Token allowance, not a token bill

For the demonstration, allow roughly 3–10 million input tokens and 0.5–2 million output tokens. Through the supervised paper system, allow roughly 20–100 million input and 4–20 million output tokens, cumulative.

These are unmeasured development allowances; actual usage depends on how much code agents rewrite and how often they rerun tests.

At current published GPT-5.6 Terra API rates, that cumulative paper allowance would cost about $90–$440 in text tokens; using GPT-5.6 Sol throughout would be about $160–$800.

Tool calls, data, compute and premium service tiers are extra. Tokens are not the main development cost but we should measure them during the first demonstration and revise the budget. [8]

Let the evidence determine the test period: Frequent effects may yield evidence quickly while rare liquidity events may take months.

The review date is a checkpoint where the number and variety of independent observations determine what we can conclude.

At the first review, decide whether the research is useful and the proposed trading merits further work.

### Size the next investment from the paper results

Agent count alone tells us nothing about cost and a promising back test is not a reason to build execution infrastructure. So, on first principles, start with a paper system we can inspect, then decide what to build next.
