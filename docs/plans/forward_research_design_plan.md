# Forward Research Design Plan

Status: **PROPOSED PLAN — DOCUMENTATION ONLY. Authorizes no code, no
infrastructure, no revision of the Constitution, PD-001 or PD-002. Nothing
here is admitted.** Revision 2 (2026-10-18): aligned with revision 2 of
the audit after the Principal's four questions; adds the scope of PD-003.

Date: 2026-10-18

Governs: the smallest set of document changes that make forward research
constitutionally coherent, in the order they should be decided. Source of
defects: the
[forward research OSA audit](../audits/forward_research_osa_audit_20261018.md)
(FR-1 to FR-13; unresolved decisions UD-1 to UD-8). Dependencies: PD-002
(proposed) for Observation independence, the Runner, closures and
resolution sets; the Constitution revision 2 for everything else.

## 1. The smallest changes

Every change is a field, a form, a scope, a kind or a Check rule on an
existing object. No governed object is added. The Transition ledger
remains the single authority for admitted state; its applied subsequence
is the Applied History; Population State remains the derived projection.

### Group A. Immediate blockers (forward research cannot start without them)

| Ref | Change | Document and section | Delta |
| --- | --- | --- | --- |
| FR-10 (with FR-1) | Observation Authorization gains **feed sources** and the **hop rule** (depth, count, domains). Research Authorization gains a **discovery scope** (feeds it may screen, units not tied to a Theme, follow-up caps). Research Record kind `SCREEN` with dispositions `CANDIDATE`, `DEFERRED`, `REJECTED` and reasons. `SRC-ADHOC` withdrawn; every on-request retrieval cites the referencing feed item | §III.5 Evidence table (feed items, hop provenance); §III.7 Authorization content; Part V (Observation function retrieval under feeds); Part II budget table (research budget may include a discovery fraction) | `ΔA`: two scopes within the Authorization object, Principal-set; `ΔS`: Observation and Research Record content |
| FR-5 | Market Observation gains the **`DOCUMENT` form** (locator, content hash, claimed publication time, witnessed receipt, requesting Authorization for hops, stored bytes). Research Record gains a **closure** and **typed claims** (`REPORTED`, `INTERPRETATION`, `ASSUMPTION`, `QUESTION`, `PREDICTION_REF`); kinds `EXPERIMENT DESIGN` and `SELECTION` | §III.5; Part VII a `RECEIPT` row for stored bytes | `ΔS` |
| FR-11 | Hypothesis registration declares a **motivation closure**; no member of it, and no Observation below a Prediction's commitment sequence, may resolve that Prediction. Resolution-set members may be **document-sourced fields** with declared `SourceId`, period, field meaning, print rule and extraction rule. Extraction by the Observation function (deterministic rule in the Source Declaration) or by a Checker (**extraction record**, Evaluation-kind, Checker Authorization only); never by the proposer; `DISPUTED` on disagreement | §III.2 testability; §III.5 Prediction and Outcome rows; §III.7 Source Declaration (extraction rules; field meaning as a meaning field); Part V (extraction record commit) | `ΔS`; `ΔA`: one commit restriction |
| FR-3 | Hypothesis `motivated_by` is a **set** of Themes and Research Records; funding is exactly one Authorization; §III.1's one-Theme rule removed; I-5 read set-valued | §III.1, §III.2, I-5 | `ΔS` |
| FR-7 | Theme and Hypothesis registration carry a **selection basis** (uncertainty, decision it could change, experiment, value estimate with declared basis, cost, horizon, stopping rule) | §III.1, §III.2, §III.8 record form | `ΔS` |
| FR-12 | Strategy Version **capital standings** `INCUBATING`, `EXPLORATORY`, `QUALIFIED`; Allocation Transition gains a purpose and, for `EXPLORATORY`, a measurement statement and expiry; the **exploratory pool** as a Principal-declared limit; the `EXPLORATORY` label on executed records is constitutional; expiry by scheduled Transition; no numbers | §III.3 (standing), §III.6 (limits, pool), Part V (Allocation purposes; expiry Transition), Part VII (labelled executed record `DERIVED`) | `ΔS`; `ΔA = 0` |

Group A is one Principal decision record, **PD-003**. Aggregate delta:
`ΔO = 0`; `ΔS` in §III.1, §III.2, §III.3, §III.5, §III.6, §III.7, Part V,
I-5; `ΔA`: feed sources and hop rule on the Observation Authorization,
discovery scope on Research Authorizations, extraction records restricted
to Checker Authorizations. No admission authority moves; no agent or
function gains a commit right it lacks under PD-002.

### Group B. Needed before the first qualified allocation on a forward Strategy

| Ref | Change | Document and section | Delta |
| --- | --- | --- | --- |
| FR-6 | Mechanism boundary immutable as declared; explanatory standing `DERIVED` from cited Hypotheses; identity unchanged when the explanation fails | §III.3 boundary table; Part VII | `ΔS` |
| FR-8 | `ES-1` grounds qualification on forward events only, minimum per target type; trials counted across the search family; exploratory records never counted; treatment of unexplained Strategies | Evaluation Standard `ES-1` (PD-002 U-6), constitutional | Standard content |

### Group C. Can wait

| Ref | Change | Why it can wait |
| --- | --- | --- |
| FR-4 | Checker refuses a restatement of a contradicted Hypothesis without a declared difference | Belongs with the Checker contract (plan step 5, D-10) |
| FR-9 | Agent Design registration declares its method class | Matters once a second selection lineage exists; with D-14 |
| UD-7 (D-01) | Theme successor without re-parenting | Plan step 1 |
| UD-4 | Checker who extracted may not check the citing Transition | With D-10 |
| UD-3 | `EXPLORATORY` allocation for `NON-REPRODUCIBLE` versions | With PD-002 U-1 |
| UD-8 | Attribution of screening units to Themes they produced | With D-12 |
| AIE as a selection lineage | An Authorization act, `0/0/0`, after PD-003 | No constitutional text |
| UD-1, UD-2, UD-5 | Feed list and hop caps; discovery fraction; exploratory pool size | Numbers set in Authorizations and limits, not in the Constitution |

## 2. Order of decisions

1. **PD-002 admission** (proposed; pending).
2. **PD-003** (Group A), then Constitution revision 3 and a re-audit.
3. **`ES-1` drafting** with FR-6 and FR-8 (Group B) as a Constitutional
   Transition proposal.
4. Group C with the plan steps they belong to.

Nothing in this order touches the admitted PD-001 rules: the Transition
ledger's authority over admitted state and its Applied History
projection, the Economic Proposition boundaries, or the evidence clock.

## 3. Scope of PD-003: Forward Research Formation

Scope approved for drafting 2026-10-18. Drafted as
[PD-003, proposed for admission](../decisions/principal_decision_003_forward_research_formation.md)
with its [focused audit](../audits/osa_audit_pd003_proposed_20261018.md).
Not admitted. Revision 4 of the record covers dispositions 1 to 5 only;
PD-003.6 is now [PD-004](../decisions/principal_decision_004_exploratory_capital_standings.md) (admitted 2026-10-19 at revision 3 with the internal-simulator clarification; FR-12 closed),
proposed with its own `ΔA`; admission text awaiting approval is in
[admission_text_pd002_pd003_20261018.md](../decisions/admission_text_pd002_pd003_20261018.md).

| Element | Content |
| --- | --- |
| Title | PD-003: Discovery, Formation Evidence, Document Resolution and Capital Standings |
| Dispositions | PD-003.1 Discovery (FR-10, FR-1): feed sources, discovery scope, `SCREEN`, hop rule, `SRC-ADHOC` withdrawn. PD-003.2 Provenance (FR-5): `DOCUMENT` form, Research Record closure and typed claims, `EXPERIMENT DESIGN` and `SELECTION`. PD-003.3 Formation versus resolution (FR-11): motivation closure; document-sourced fields; extraction by function or Checker. PD-003.4 Explanatory graph (FR-3, FR-7): `motivated_by` set; selection basis. PD-003.5 Capital standings (FR-12): `INCUBATING`, `EXPLORATORY`, `QUALIFIED`; purpose; pool; label; expiry |
| Two-case test | Product-P sequence (audit §4.1, serially admitted) and the momentum path (audit §6) |
| Constitutional Delta | `ΔO = 0`. `ΔS` as in Group A. `ΔA`: feed sources and hop rule (Observation Authorization); discovery scope (Research Authorization); extraction records restricted to Checker Authorizations. Declared per disposition and in aggregate |
| Decisions the Principal must make on admission | Whether to keep the hop default at depth 1; whether extraction by Checker is permitted at all or only deterministic extraction by the function (narrower, safer, fewer sources); whether `EXPLORATORY` requires a stated purpose per allocation or per version; whether the discovery scope's units are a fraction or a fixed grant |
| Explicitly out of scope | FR-6 and FR-8 (Group B); `ES-1` numbers; D-10, D-11, D-12, D-14, D-17; N-1; U-1 to U-10 of PD-002 |
| Dependencies | PD-002 admitted first (Observation function, Runner, closures, resolution sets, `SourceId`/`SourceRevision`) |
| On admission | Constitution revision 3 in §III.1, §III.2, §III.3, §III.5, §III.6, §III.7, Part V, Part VII, I-5; T-F/T-G joined by the product-P sequence as T-H; re-audit for duplicate ownership between feed items, screens and formation records, for proposer influence on extraction, and for exploratory records leaking into qualification; FR-1, FR-3, FR-5, FR-7, FR-10, FR-11, FR-12, FR-13 closed by reference |

## 4. Diagrams

### 4.1 Theme → competing Hypotheses → Predictions → Strategies → Evidence

Solid edges are governed references recorded in proposals or Evidence.
Dashed edges are derived views. No edge transfers standing.

```mermaid
flowchart TB
  subgraph Discovery["Discovery and formation (never counts as test evidence)"]
    FEED["Feed items (DOCUMENT Observations)<br/>SRC-EDGAR-NEW, 41 items<br/>(Observation function, AU-02c)"]
    SCR["SCREEN record RR-390<br/>39 REJECTED, 1 DEFERRED, 1 CANDIDATE<br/>(AD-7.1 under discovery scope AU-31)"]
    HOP["Hop retrieval DO-2<br/>(cites DO-1; depth 1)"]
    RR400["Research Record RR-400<br/>typed claims, closure"]
    TH14["Theme TH-14<br/>selection basis; standing: active"]
    RR401["RR-401 EXPERIMENT DESIGN<br/>resolution set declared first"]
    FEED --> SCR --> HOP --> RR400 --> TH14 --> RR401
  end

  subgraph Belief["Belief competition (Hypotheses)"]
    HY140["HY-140<br/>close pressure, conditional"]
    HY141["HY-141<br/>anticipation / reversal"]
    HY142["HY-142<br/>adoption (document-sourced field)"]
    PR640["PR-640"]
    PR641["PR-641"]
    PR642["PR-642"]
    OC640["OC-640<br/>bound set {SRC-I 15:30, 16:00}"]
    OC642["OC-642<br/>DO-9 + R-P1 extraction (function)"]
    HY140 --> PR640 --> OC640
    HY141 --> PR641 --> OC640
    HY142 --> PR642 --> OC642
  end

  subgraph Capital["Capital competition (Strategy Versions)"]
    SV401["SV-40.1 / EP-44<br/>INCUBATING → EXPLORATORY → QUALIFIED"]
    SD["Strategy Decisions SD-40xx<br/>closure includes PR-64x (Runner)"]
    RP["Reproduction records (Checker)"]
    SV401 --> SD --> RP
  end

  RR401 -- "motivated_by" --> HY140
  RR401 -- "motivated_by" --> HY141
  RR400 -- "motivated_by" --> HY142
  TH14 -. "motivated_by (set)" .-> HY140
  HY140 -- "cited; no standing transfer" --> SV401
  PR640 -- "closure input only" --> SD
  OC640 -. "Evaluation (DERIVED)" .-> EV["EV-200<br/>pinned ES-1, closure"]
  SD -. "Evaluation (DERIVED)" .-> EV
  EV -. "cited by Transition" .-> TL["Transition ledger (Applied History)<br/>standing, allocation, purpose"]
```

### 4.2 Agent research and successor-agent evolution

```mermaid
flowchart LR
  subgraph Lineage["Agent Design lineage AD-7 (lineage memory: DERIVED over Research Records, incl. screens)"]
    AD71["AD-7.1<br/>method: research<br/>AU-31 (discovery) + AU-32 (TH-14)"]
    AD72["AD-7.2<br/>successor, zero contribution<br/>no Authorization until granted"]
    AD71 -. "proposes successor (T-C)" .-> AD72
  end

  AD71 -- "commits" --> RR["Research Records<br/>RR-390 screens, RR-400, RR-401, ..."]
  AD71 -- "proposes, each with its own base" --> TR["Transitions<br/>TR-400 Theme; TR-401/402/404 Hypotheses<br/>(serial, re-checked); TR-410 Strategy"]
  TR --> CK["Independent Check<br/>CK-H1 (AU-21)"] --> P["Principal decides"] --> TL["Transition ledger<br/>(Applied History)"]
  P -- "grants AU-33 to AD-7.2<br/>(separate Transition)" --> AD72
  RR -. "research contribution per unit consumed<br/>incl. rejected screens (Evaluation, DERIVED)" .-> EVA["Agent Design Evaluation<br/>under ES-1"]
  EVA -. "cited by" .-> P
  RUN["Strategy Runner (AU-04)<br/>keeps running SV-40.1 after AD-7.1 retires"]
  TL -- "standing of SV-40.1" --> RUN
```

### 4.3 Research selection, with AIE as a replaceable policy

```mermaid
flowchart TB
  SEL1["Selection lineage SEL-1<br/>Agent Design, method: AIE<br/>(value of information)"]
  SEL2["Selection lineage SEL-2<br/>Agent Design, method: other"]
  DISC["Discovery scope<br/>(Research Authorization: feeds, units<br/>no policy directs, follow-up caps)"]
  SR["SELECTION Research Records<br/>question, alternatives, value and cost<br/>estimates with declared basis, horizon, stop rule"]
  TRT["Theme / experiment proposals<br/>with selection basis"]
  CK["Checker"]
  P["Principal or admitted policy (D-11)<br/>the only authority to fund"]
  TL["Transition ledger (Applied History)<br/>Theme standing, research grants"]
  SCR["SCREEN records<br/>(what was rejected, and why)"]
  RRB["Research Records<br/>(what the work found, including negatives)"]
  EV["Selection Evaluation (DERIVED)<br/>did resolved experiments change a decision?<br/>estimate error; misses among rejected screens"]

  SEL1 --> SR --> TRT --> CK --> P --> TL
  SEL2 -. "successor or competitor,<br/>matched budgets, new questions" .-> SR
  DISC -- "screens feed items" --> SCR
  SCR -- "CANDIDATE" --> TRT
  TL --> RRB
  RRB -. "resolved outcomes" .-> EV
  SCR -. "later-funded rejections" .-> EV
  EV -. "cited by the Principal to replace<br/>SEL-1 with SEL-2 (Authorization act, 0/0/0)" .-> P
```

### 4.4 The governed boundary between research and paper trading

```mermaid
flowchart LR
  subgraph Research["Research side (proposes; never writes the Paper Book)"]
    RA["Research Agents<br/>(Research Authorizations: Theme and discovery scopes)"]
    OBS["Observation function<br/>(Observation Authorization: numerical, document, feed sources; hop rule)"]
    EVL["Evidence ledger<br/>Observations, screens, Research Records,<br/>Predictions, Outcomes, extraction records,<br/>Decisions, reproductions"]
    RA -- "requests retrieval (cites referencing item)" --> OBS -- "commits" --> EVL
    RA -- "commits Research Records, Predictions" --> EVL
  end

  subgraph Gate["The boundary: the Allocation Transition, by purpose"]
    EXP["EXPLORATORY<br/>from the exploratory pool; purpose and expiry;<br/>no performance Evaluation needed; labelled"]
    QUAL["QUALIFIED<br/>cites an Evaluation under the Standard in force;<br/>grounding series: forward decision-implied record"]
  end

  subgraph Paper["Paper side (executes; never writes research)"]
    TL["Transition ledger (Applied History)<br/>allocation, purpose, limits, pool"]
    RUN["Strategy Runner<br/>(Runner Authorization)<br/>commits Decisions at every standing"]
    EXE["Execution function<br/>(Execution Authorization)"]
    PB["Paper Book<br/>orders, replaces, cancels, fills, refusals"]
    TL -- "standing, allocation" --> RUN
    RUN -- "Decisions" --> EVL
    EVL -- "Decisions" --> EXE
    TL -- "allocation, limits" --> EXE
    EXE -- "sole committer" --> PB
  end

  EVL -. "Evaluation (DERIVED)" .-> QUAL
  EXP -- "Apply" --> TL
  QUAL -- "Apply" --> TL
  PB -. "executed record, labelled by purpose (DERIVED)" .-> EVL
```

## 5. Proposed changes to the client discussion draft

Target: the draft of 17 October 2026, filed as
[reference](../reference/new_speedway_discussion_draft_20261017.md).
Revision 2 corrects the object presentation as the Principal directed:
durable authoritative records are distinguished from the derived
Population State, and the Applied History is not presented as an owner
beside the Transition ledger.

### 5.1 Opening

Keep the first three paragraphs and the three ideas. Replace the two
paragraphs after the three ideas with:

> The trading stays quantitative: prices, volume, flows and risk. What
> changes is where the ideas come from and how fast the research process
> can change itself. An agent can screen the day's new filings, notice a
> product that will create mechanical flows, ask what those flows will do
> to the close, write two competing hypotheses, commit daily predictions
> before the close, write a strategy that trades the prediction, and
> incubate that strategy on paper at zero allocation until its own forward
> record earns capital. None of that needs a backtest, and none of it
> needs a human at every step. What it needs is a record that no agent can
> rewrite.
>
> Strategies are disposable. The record, the research process and its
> ability to replace itself are the assets.

### 5.2 Section 3, "The nine durable objects"

Replace the heading with **"The ten objects, and which ones are
authoritative"** and the lead paragraph with:

> The first four evolve. Three ledgers preserve what happened:
> Transitions, Evidence and the Paper Book. Each ledger is the only
> authority for its facts, and nothing else can overrule it. Authorization
> and the Constitution govern what may happen next. Population State is
> the tenth object, and it is a view: it is rebuilt from the Transition
> ledger and has no authority of its own. An agent run is an actor, not
> state. Predictions, experiments, observations and strategy decisions are
> records within Evidence.

Replace the `Transition` and `Population state` rows and add `Paper Book`:

| Object | Required content | Admission or mutation rule |
| --- | --- | --- |
| Transition | The proposal, its base state, the checks, the decision, and the rule versions it was decided under. Applied Transitions form the system's history. | The ledger of Transitions is authoritative for membership, standing, allocation, limits and what is current. Append-only; one commit boundary; rejections and stops are kept. |
| Population state | Membership, lifecycle, budgets, paper allocations and exposure at a point in the history. | A derived, replayable view of the applied Transitions. No authority of its own; can always be rebuilt and never serves as a fallback. |
| Paper Book | Paper orders, replacements, cancels, fills and execution refusals, each bound to the allocation and the strategy decision that caused it. | Authoritative for execution facts only. Never owns targets; a gap between target and position is reported, never reconciled away. |

Amend three existing rows:

- `Theme`: add "why it was selected: what is uncertain, what decision it
  could change, what the experiment would cost"; mutation rule: "May be
  speculative; a change of scope is a successor Theme that cites its
  predecessor."
- `Hypothesis`: add "the sources that will resolve it, declared before any
  prediction, kept separate from the documents and research that motivated
  it."
- `Evidence`: add "screens of new information, document receipts,
  strategy decisions and reproduction checks".

### 5.3 Section 4, relationships table

Add one row:

| Relationship | Precise meaning |
| --- | --- |
| consumes | A strategy reads a committed prediction or observation as an input to a decision. It does not inherit the prediction's standing. |

### 5.4 Section 6, worked example

Add after "What happens when the explanation changes":

> If S2 keeps making money while H1 fails, S2 keeps its allocation on its
> own record and is labelled as unexplained; its explanation is retired,
> not rewritten, and its risk limits follow the evidence.

### 5.5 Section 7, "Choose the next experiment"

Replace the last sentence of the Pfizer paragraph with:

> The policy for choosing research is itself a research method: it
> proposes, it never funds, its choices are recorded with their reasoning,
> and it is judged afterwards by whether the experiments it chose changed a
> decision at the cost it estimated. A part of the research budget is
> always reserved for screening new information no policy chose.

### 5.6 Section 8, operator views

Add one row:

| Operator view | What it must answer | Available action |
| --- | --- | --- |
| Observation health | Which sources and feeds were retrieved on schedule, which returned nothing, which failed? Which predictions lost forward standing because of it? | Request a retrieval, add a source or slot, or declare a source unreliable. |

### 5.7 Section 9, paper trading

Add one sentence after "Start on paper to answer two questions":

> Paper activity comes in two kinds and is always labelled: exploratory
> allocations exist to measure fills, turnover and timing, and are never
> evidence of an edge; qualified allocations are earned by a strategy's own
> forward record under rules fixed in advance.

### 5.8 Language

Replace "HIL" with "the operator" or "a person" throughout; replace
"gen-ai coding angle" with "one governed record"; remove "Just like a
code gen harness" if it survives from the earlier draft.

### 5.9 What the draft already gets right

The three ideas; principle 4; the explanatory graph with no standing
transfer; the distinction between composition checks and CPOC; evaluating
research quality separately from simulated performance; measuring trading
activity before sizing execution; the token allowance framing.

## 6. Rules for this plan

- No application code, tests, infrastructure, frameworks, dependencies or
  service selection.
- No revision of the Constitution, PD-001 or PD-002 under this plan;
  Group A becomes PD-003 for the Principal.
- Every change is tested on both the product-P case (audit §4, serially
  admitted) and the momentum case (audit §6) before it is proposed.
- Rejected alternatives stay in the audit with their reason.
- Nothing is admitted by being written here.
