# Feasibility, Coherence and Public Library Audit

Status: **AUDIT EVIDENCE — NO IMPLEMENTATION OR TECHNOLOGY SELECTION AUTHORIZED.**

Date: 2026-10-29. Reviewer: Codex. Scope: the current repository's design,
executable material, integration boundaries and suitability for a public
library for governed agent research and internal paper simulation.

## 1. Disposition

**The admitted design is a credible foundation for the intended library.
The repository does not yet contain an implemented constitutional harness
that another developer can install or exercise. The next work is core
implementation behind explicit interfaces, following an admitted
implementation plan. Package extraction and documentation alone would not
close the gap.**

This conclusion follows from inspecting the working tree, including
untracked files, rather than assuming that the October 19 status remains
accurate. The executable presentation illustrates a research cycle. It
does not implement the spending, evidence, admission or recovery contracts.

CV1's research and internal paper-simulator scope is suitable for a first
release. Live trading is a separate expansion and is not a missing feature
of that release. The relevant integration question is whether research
engines and fill computation can be replaced while Speedway retains all
governed records and enforces the same rules.

The architectural answer is yes: the Constitution already separates tool
computation from commit authority. The operational answer remains unproven:
there is no implementation, adapter conformance evidence or executed
continuity witness in this checkout.

## 2. Evidence and limits of this review

| Subject | Reviewed evidence |
| --- | --- |
| Repository | HEAD `75036e0685e1e30b4bd430f88f4df7e64e1abbee`, plus working-tree files at review time |
| Governing baseline | [Constitution revision 12](../doctrines/new_speedway_constitution.md), SHA-256 `c56a9cf50a7e9efadad8f2f2be6605e82c758f18d4096ba07eaaf86a8f8b7a64`, matching the [CV1 admission](../decisions/cv1_admission_20261019.md) |
| Design explanations | [README](../../README.md), [architecture](../../architecture.md), [document-first plan](../plans/document_first_design.md) |
| Design closure | [Final independent review](cv1_final_independent_review_20261019.md), [bounded follow-up](cv1_revision12_bounded_followup_20261019.md), [closure review](cv1_revision12_closure_20261019.md), admitted decisions and outstanding parameters |
| Reuse and demonstrations | [PD-006](../decisions/principal_decision_006_replaceable_tools_and_first_prototype.md), [PD-009](../decisions/principal_decision_009_genesis.md), including their later amendment notes |
| Executable material | Presentation HTML, including the untracked [research story](../presentations/demo/new_speedway_research_story.html), SHA-256 `6667d2006c68ab7fc8c63c844490a1a8fef9cf71d604d80f9668e925df975840`; root `test.py` is zero bytes |
| Engineering discipline | [Adoption record](../decisions/fin123_core_adoption_20261018.md); the original CPOC doctrine read at fin123-core commit `8175d504998bf682170847119a866d7f5e7df8fd`, path `docs/top_doctrines/iris_cross_process_operational_continuity_doctrine.md` |

Inventory used `git ls-files`, `git status --short --untracked-files=all`,
`git submodule status` and `rg --files --hidden --no-ignore` excluding
`.git`. No application package, dependency manifest, ledger implementation,
adapter implementation, executable conformance suite or submodule was found.
Existing presentation edits and untracked files were preserved.

This is source inspection and document analysis. No application tests or
CPOC witnesses were run because there is no harness to execute. No claim
is made about another checkout, unpublished code or a remote deployment.
The coherence assessment builds on CV1's prior closure and examines the
library boundary; it is not a new exhaustive whole-design certification.

LangGraph and MiroFish primary documentation/source were inspected on
2026-10-29. External links below describe candidate surfaces, not selected
dependencies. Their moving documentation and `main` branches are not a
version-pinned compatibility certification. An implementation plan must
pin and recheck the actual versions.

## 3. What is actually implemented

The three categories in this audit are deliberately different:

- **Implemented and demonstrated:** executable enforcement supported by
  observed results, including relevant refusal and recovery paths.
- **Designed but incomplete:** the governing behavior is stated, but its
  implementation or demonstration is missing.
- **Unresolved:** behavior, authority, interface details or required
  configuration still need a decision or specification.

**No constitutional rule qualifies as implemented and demonstrated in the
reviewed repository.** That is an absence of implementation evidence, not
a report that an existing harness failed its tests.

| Capability | Category | Evidence and remaining work |
| --- | --- | --- |
| Authorized callers and exclusive commit boundaries | Designed but incomplete | Constitution Parts II, III and V specify roles. No executable caller validation or protected writer exists |
| Reserve, attempt, settle, fence and lineage caps | Designed but incomplete | §III.5 specifies ordering, overruns and duplicate settlement refusals. No implementation exercises them |
| Propose, Check, Decide, Apply; stale-base refusal | Designed but incomplete | §III.8 and Part V specify lifecycle, independence and `P-1`. No transition engine exists |
| Binding, invalidation and release after interruption | Designed but incomplete | §III.5 and §III.8 specify the cross-ledger protocol. No race or process-death evidence exists |
| Observations, closures, Predictions, Outcomes and evidence classes | Designed but incomplete | §III.5 specifies ownership and timing. No ingestion or classification boundary exists |
| Reproduction and `ES-1.0` evaluations | Designed but incomplete | Parts III and X specify requirements. No evaluator or independent recomputation implementation exists |
| Strategy Runner and Paper Book | Designed but incomplete | §III.10 defines orders, provisional fills, confirmation, expiry and reduction. No runner or execution ledger exists |
| Public package, APIs and adapters | Unresolved interfaces; implementation absent | No import surface, storage protocol, adapter contract, release manifest or compatibility policy exists |
| Genesis settings, provider substitution and moving-limit behavior | Unresolved within stated constraints | Specific outstanding items appear in §8 below; they must not be filled with inferred defaults |

The presentation contains real JavaScript, but its behavior is scripted:

- `initial()` creates ordinary mutable objects and arrays. `setStatus()`
  assigns status directly; `ev()` pushes display text into an array.
- `SCENES` assigns `s.budget.reserved` and `s.budget.spent` to fixed numbers.
  There is no reservation admission, attempt identity, cap calculation or
  competing caller to reject.
- The approval scene sets `checked = true` and records a prewritten human
  approval. It neither authenticates the Principal nor runs an independent
  Checker against committed evidence.
- `stateAt(t)` rebuilds those scripted scenes from `initial()`. Seeking or
  replaying the animation does not reopen durable governed state after
  process death. It demonstrates no lawful recovery or pending liability.

These observations are visible around lines 104–112, 119–218 and 446–484
of the research-story file at the digest above. Its own
[README](../presentations/demo/README.md) correctly labels it a presentation
demo, not the system. Browser presentation behavior was not runtime-tested
in this audit.

There is also a public-explanation correction to make before using this
story as onboarding: it calls synthetic results “Supported,” including
seven of nine events, and calls S1 registered before later saying it was
never registered. Those labels must not be presented as CV1 standing.
Synthetic results earn no forward standing; Part X also imposes an
effective-observation floor of twelve for Hypothesis standing decisions.
This is presentation ambiguity, not a newly discovered defect in CV1.

## 4. Coherence and suitability

The design has a consistent organizing principle: **agents generate
proposals and computational results; governed boundaries establish which
facts may be committed and which changes take effect.** Four separations
make it useful beyond a single agent workflow:

1. A design's identity and its permission to act are separate. A successor
   can be registered without inheriting authority or performance credit.
2. Evidence, evaluation and admission are separate. A favorable backtest,
   model response or Evaluation cannot allocate capital.
3. Allocation, Strategy Decision and execution are separate. A target
   change does not pretend that positions have already changed.
4. Durable authority and runtime memory are separate. Restart must recover
   permission from records, including liabilities and refusals.

The difficult cases are specified rather than hidden: uncertain dispatch
does not prove that no spending occurred; settlement can survive revocation;
binding eligibility differs from permission for new spending; a frozen
binding has no promised release time; and a lawful partial reduction must
be attributed to an applied `REDUCE`. These are substantive contracts for
a harness, not merely prompts for well-behaved agents. See Constitution
§III.5–§III.10 and the closure review.

No new blocking contradiction in those reviewed boundaries was established
here. Their complexity remains an implementation risk. Serialization,
cross-ledger reads and interruption behavior will require more care than
connecting an agent framework. Document closure does not measure throughput,
Checker quality or the cost of retaining complete evidence.

For a public library, the strongest initial product is **a CV1 implementation
for agent research and paper simulation**. It need not begin as a universal
constitution interpreter. `ES-1.0`, the evidence classes, research lineage
and the Paper Book are investment-specific semantics worth retaining.
Packaging them into modules need not change their authority. Allowing
arbitrary plugins to redefine them would require a separate constitutional
assessment, not just an extension API.

Deterministic checks can enforce identities, sequencing, caps and allowed
callers. Judgments such as whether a hypothesis is a restatement or a
statistical method satisfies the Standard still require the independent
Checker's recorded work. Structural independence is enforceable; universal
correctness of an LLM Checker is not established by the design. The public
claim should be inspectable enforcement of the declared process.

## 5. Concrete public-library contract to specify

The following is a proposed interface boundary derived from CV1. It is
neither an existing API nor admission of a new object or decision right.
Names, serialization and transports remain implementation-plan work.

| Boundary | What an adopter supplies | What Speedway must own and enforce |
| --- | --- | --- |
| Initialization | Principal identity binding; exact CV1 text; initial Checker design and complete grant | Exact sequence-zero content and one-time waiver; refusal of re-genesis; durable historical versions |
| Authority | Attributable callers and Principal-issued grants, scopes, units, caps, expiry and tool tiers | Role checks at each commit; current grant state; independent Checker routing; no grant by an agent |
| Research and tools | Agent designs, tool implementations, input artifacts, cost estimates and usage evidence | Reservation and attempt admission before consumption; settlement, refusals and lineage accounting; immutable committed results |
| Observations | Source Declarations, retrieval implementations, raw bytes, extraction rules and retrieval completeness facts | Observation-only commit route; source/version binding, clock receipts, provenance and absence-witness rules |
| Proposals and Checks | Immutable proposal content, declared base/delta, independently produced Check and appropriate decision | Check shape and applicable criteria, caller separation, current-base checks, `P-1` scope, binding protocol and exclusive Apply |
| Strategies and evaluation | Executable artifacts, declared inputs/triggers, reproducibility bindings, precommitted statistical methods | Closed-input Decision commits, independent reproduction records, version-bound evaluations and no automatic capital promotion |
| Simulation | Fill computation under the fill rule named in an Execution Authorization | Execution-only Paper Book calls; order/set identity, limits, expiry, provisional fills, confirmations and derived positions |
| Persistence and clock | A conforming durable store and an implementation of the Evidence boundary's clock | Logical ledger sequencing, atomic refusal/disposition operations, authoritative head reads and replay under pinned versions |
| Inspection | Queries naming subjects and historical/as-of positions | Readable records, refusal reasons, source references, outstanding obligations and reproducible projections |

Public commands need explicit caller attribution, exact governed subject,
the applicable Authorization or direct Principal authority, and the
base/closure/identity fields the corresponding CV1 operation requires.
Responses need to distinguish a committed result from a preserved refusal
and from a transport failure whose commit status is unknown. A lost response
must lead to an exact record lookup before retry, not an assumed rollback.
Protocol details for that distinction have not been specified.

The library must not expose an unrestricted “append event” API to agent
code. A durable storage adapter may carry the three logical ledgers, but
it may not select currentness, waive admission or reinterpret records.
Three logical ledgers do not require three services or three databases.
The physical arrangement is still unselected.

| Guarantee a conforming release could offer | Present standing and boundary |
| --- | --- |
| Unauthorized and stale requests are refused at the responsible commit | Designed, not implemented. Applies to operations through the protected boundary |
| Concurrent callers cannot reserve the same remaining unit | Designed, not demonstrated. Requires serialized Evidence admission |
| Admitted attempts and liabilities survive restart; settlement affects accounting once | Designed, not demonstrated. External execution is not automatically exactly once |
| Budget ceilings match the declared guarantee tier | Designed, not demonstrated. Uncapped provider charges support estimate admission and overrun accounting, not a hard ceiling |
| Evidence classes and historical meanings cannot be rewritten by a later workflow | Designed, not demonstrated. Stored versions, closures and clock behavior must support the claim |
| Replacing a tool preserves governed records and admission rules | Required by PD-006; no replacement witness exists |
| Recovery derives the next lawful action without old process memory | Required continuity behavior; no CPOC witness exists |

An embedding contract must state its trust assumptions. A caller with raw
database write privileges, unrestricted provider credentials or permission
to alter enforcement code can bypass a cooperative in-process wrapper.
Role strings in a request do not authenticate a Principal. The plan must
specify how trusted caller identity, credentials and exclusive writers are
enforced for its supported deployment. This is a concrete prerequisite for
an enforcement claim, not a proposal to introduce new governed identities
or a requirement to build a hosted platform.

## 6. Integration hooks

### Framework-neutral hooks

Every integration needs the same small set of boundary operations:

| Hook | Required behavior |
| --- | --- |
| Before metered work | Reserve under the correct Research or Checker grant; commit the attempt and maximum before dispatch; refuse work when admission fails |
| After work, failure or cancellation | Preserve result/negative evidence and settle with valid attribution and provenance; retain uncertain liabilities; cancellation alone proves no refund |
| Before consuming external information | Use declared Observation routes when information will be cited; retain exact committed inputs and tool versions |
| Before changing governed state | Submit a proposal, independent Check and authorized decision; only the Apply boundary establishes the change |
| After restart | Read current ledgers and exact attempt/transition identities; distinguish undispatched, uncertain, settled, applied and invalidated cases according to their records |
| Before simulated execution | Route candidate fills through the Execution function and Paper Book admission; never import a simulator's position as authoritative |

A callback that logs tool activity after it happens is insufficient. The
critical interception is before consumption or commitment. Nested calls,
SDK retries and subprocesses must be included in the integration's spending
coverage; otherwise the adapter cannot claim complete enforcement.

### LangGraph: plausible orchestration adapter, optional

LangGraph provides checkpointed graph state and separate stores.
Its interrupt mechanism supports pausing for input and resuming with
`Command(resume=...)`. The interrupted node restarts from its beginning,
so preceding code can execute again. These are useful orchestration
capabilities, not Speedway admission rules. Sources:
[persistence](https://docs.langchain.com/oss/python/langgraph/persistence),
[interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts).

Proposed integration:

- Put metered model/tool calls behind the pre-dispatch attempt boundary.
  Re-entering a node first looks up the governed attempt rather than
  automatically issuing another request.
- Carry ledger references in graph state. A thread ID is an orchestration
  identifier, not a substitute for an Authorization or Transition identity.
- Use interrupts to obtain user input, then submit an attributable decision
  through Speedway. A resumed `true` value does not establish Principal
  authority. Recheck the base and current admission conditions on resumption.
- Use separate proposer and Checker execution contexts with their own
  grants; changing a graph node's label to “checker” establishes nothing.
- Treat graph replay/time travel as workflow behavior. It cannot rewind
  applied history, restore spending permission or duplicate a settlement.

Acceptance requires crash/retry and stale-approval witnesses through the
actual adapter. Neither LangGraph nor a particular checkpointer is required
to implement the core, and neither is selected here.

### MiroFish: optional research/simulation producer

“MiroFish” here means [666ghj/MiroFish](https://github.com/666ghj/MiroFish).
The inspected project exposes simulation creation/start and result-reading
routes, including configuration and action history. Its execution script
uses OASIS and CAMEL model construction; it is a candidate source of scenario
research, not an identified replacement for the Paper Book's fill rule.
Sources: [simulation API](https://raw.githubusercontent.com/666ghj/MiroFish/main/backend/app/api/simulation.py),
[simulation script](https://raw.githubusercontent.com/666ghj/MiroFish/main/backend/scripts/run_parallel_simulation.py).

The source reveals an integration trap: wrapping only MiroFish's
[`LLMClient`](https://raw.githubusercontent.com/666ghj/MiroFish/main/backend/app/utils/llm_client.py)
does not establish coverage of the CAMEL/OASIS model path in the simulation
script. Each metered path, its retries and any other paid service must be
accounted for before claiming a governed run. A maximum number of simulation
rounds alone is not a demonstrated charge bound.

Proposed adapter work is to bind a run's seed material to committed input
references; preserve configuration, prompts, model/tool provenance and raw
results; fund the work under the appropriate grant; and commit its outputs
through an authorized research caller. Simulated consensus, personas and
reports do not become independent Checks, observed market Outcomes or
forward performance evidence. Generated material can motivate a later
Prediction that is committed and resolved under CV1's own rules.

MiroFish is not required for a first release. No stable Speedway-compatible
SDK, complete cost interception, deterministic replay or governed stop
mechanism was established by this bounded inspection. Those are adapter
acceptance questions. A plain controlled research tool is enough to prove
the integration boundary first.

Dependency distribution also needs an explicit choice: inspected LangGraph
source carries an [MIT license](https://github.com/langchain-ai/langgraph/blob/main/LICENSE),
while inspected MiroFish carries
[AGPL-3.0](https://raw.githubusercontent.com/666ghj/MiroFish/main/LICENSE).
No distribution model or license-compatibility conclusion is selected here.
An optional external adapter does not by itself settle those questions.

## 7. Replaceable simulator: the decisive first-release test

CV1 §III.10 and PD-006 allow reusable fill computation while retaining an
internal governed Paper Book. This is the right boundary for the first
release. The simulator proposes fills; it does not grant funding, commit
observations, decide admission or overwrite positions.

The proposed public simulator contract should identify the exact order and
permitted input closure, the fill rule bound by the Execution Authorization,
the computation version/configuration and its candidate output. Detailed
wire fields remain to be specified. Any metered computation must use its
lawful funding route; the Execution role cannot be given Research Evidence
write rights merely to simplify integration. If a chosen simulator requires
a funding or caller relationship CV1 does not supply, that is a stop for
the implementation plan to resolve.

Two kinds of replacement must be distinguished. Replacing computation while
preserving the authorized fill rule is an implementation compatibility
question. Changing the fill rule is an Authorization-content change through
the Principal's checked grant process. Neither may silently rewrite earlier
fills or their interpretation.

Proposed acceptance witnesses, **none executed**:

| Witness | Required result |
| --- | --- |
| Replace simulator A with B | The same governed history remains readable; neither adapter acquires write authority; any changed rule is separately authorized |
| Replay the same candidate output | No duplicate effective fill or position effect |
| Supply an invalid, excessive, expired or wrong-order fill | Paper Book refuses or leaves it ineffective under the applicable rule; evidence is preserved |
| Kill after provisional fill, before confirmation | A fresh process reads the durable fill and current witnesses; it does not assume confirmation from a simulator response |
| Replace the simulator during an outstanding reduction | The target, confirmed position, pending orders and residual obligation are reconstructed from ledgers |
| Retry or cancel metered simulation work | Spending still follows attempt, liability and settlement rules; stopping the simulator does not erase cost |
| Substitute an external simulated position snapshot | It cannot override positions derived from confirmed fills |

Different lawful fill rules may produce different execution paths. The
replacement guarantee concerns retained authority and enforcement, not
identical simulated returns. Removing the presentation's scripted outcomes
would not supply this contract or these witnesses.

## 8. Unresolved items and the release stages they affect

| Item | What remains to decide or supply | Scope affected |
| --- | --- | --- |
| Implementation authorization | Admit a bounded plan with its own delta and authority/representation mapping | Any core implementation |
| Genesis content | Numerical `AU-RP-1` binding interval; complete Checker/Observation/Research grants; exact design hashes, provenance and commitments; `SRC-E` and `SRC-SYN` declarations including extraction and resolution grace | First governed research demonstration |
| Public interfaces | Command/result schemas, deterministic encoding and hashing details, authenticated caller binding, unknown-commit recovery, storage/clock contracts and compatibility behavior | Reusable library core; meaning or identity changes require Principal resolution |
| Provider changes, D-14 | Prototype keeps registered provider/model fixed; substitution under that design stops until a rule is admitted | Real-provider adapters and later upgrades; no silent fallback model |
| Provider caps | Provider-specific acceptance of cap and billing assumptions before treating real calls as capped | Real paid providers; synthetic/metered demonstration can proceed under its own accepted settings |
| Non-reproducible strategies, U-1 | Current Standard offers no capital-qualification route | Supported first-release restriction, not a requirement to invent a route |
| Execution setup | First Execution Authorization and `FR-0` fill-rule content; Runner setup and required sources | Paper-simulation stage; not the two initial research demonstrations |
| Moving limits, U-8 | Exact behavior when limits change between execution witnesses | Paper-simulation claims; a release must either resolve it or explicitly retain CV1's pre-witness limitation without claiming stronger protection |
| Distribution and maintenance | Package layout, license, public docs, supported versions, contribution/review policy, vulnerability reporting and release evidence | Public release |

The [admission record](../decisions/cv1_admission_20261019.md) is the source
for the pre-genesis parameters and standing restrictions. This audit chooses
none. A missing parameter is not necessarily an incoherent contract: many
are deliberately owned by the Principal and supplied for a deployment.

## 9. What to build next, in evidence order

The inventory rules out extracting a working core or merely documenting an
existing implementation. The proposal is to implement the core with a
reusable boundary from the start, without first building a separate product
application. This order is advisory and awaits the required admitted plan.

| Stage | Work | Evidence needed to move on |
| --- | --- | --- |
| 1. Specify the executable boundary | Map existing facts and callers to operations, store requirements, representations and failure responses; supply genesis content; evaluate commodity components | Every touched fact retains its owner and commit boundary; interface choices introduce no undeclared meaning or authority |
| 2. Implement the research core | Transition and Evidence ledgers, clock, grants, attempt accounting, independent Check, `P-1`, binding/recovery and query projections | Budget races, fence ordering, overrun/duplicate settlement, stale bases, unauthorized calls and binding races produce the specified records |
| 3. Execute the admitted demonstrations | PD-006's evolutionary research and synthetic development/Theme paths using bounded tools | Complete successful and refused paths, preserved negative evidence, unfunded successors refused, and actual process death followed by reconstruction and continuation |
| 4. Add the internal paper cycle | Runner, closed Decisions, independent reproduction, Paper Book, authorized fill computation, expiry and `REDUCE` | Confirmed-position derivation, refusal/reversal/expiry cases, outstanding reduction recovery and the simulator-replacement witnesses above |
| 5. Release the library | Installable package, one documented storage implementation, tool contracts, examples, optional framework adapters and compatibility policy | A clean consumer environment can run the supported examples and refusal/recovery cases without repository-internal assumptions |

CPOC evidence must use real process death and a fresh process, reopening
the exact subject, continuing lawfully and later verifying history. A
new object in the same interpreter or an animation reset is insufficient.
Evidence must identify the exact build, governed versions, boundary records,
decision surfaces and negative witnesses. The research stages can establish
bounded evidence before the Paper Book exists; their success would not
certify the later paper cycle automatically.

The most valuable early integration exercise is one metered tool that
reserves, attempts, produces evidence, is interrupted, settles, receives a
Check and reaches or is refused at Apply. Then replace the tool and repeat.
This establishes the library boundary before investing in multiple agent
frameworks. LangGraph is a reasonable candidate adapter to evaluate next;
MiroFish is optional until a specific scenario-research use justifies its
broader call coverage and distribution work.

No calendar estimate is supported by this repository. The dominant work
is the commit and continuity machinery, followed by Paper Book correctness
and verification. Adapter syntax, packaging and onboarding are smaller
tasks once those boundaries exist. Forward market evidence takes its own
observation time, but a governance library release need not demonstrate
investment returns to demonstrate correct enforcement.

## 10. Audit effect and final finding

Only this audit is added. `ΔO/ΔS/ΔA = 0/0/0`: no governed object, meaning,
authority, runtime, dependency or Evaluation Standard is changed or
selected. The admitted Constitution bytes remain unchanged. Recommended
interfaces and release witnesses are proposed work, not new doctrine.

**Feasible and coherent within the admitted research and internal paper
scope; not yet an implemented or demonstrated public library.** The next
concrete deliverable is an admissible core implementation plan with the
public boundary specified, followed by executed enforcement and continuity
evidence. Public adoption depends on making those boundaries usable and
verifiable, with replaceable tools that cannot bypass them.
