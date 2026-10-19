# Principal Decision Record 003 — Discovery, Formation Evidence, Document Resolution, Research Selection and Capital Standings

Status: **ADMITTED 2026-10-18 by the Principal, dispositions PD-003.1 to PD-003.5 only.** Admission text, as approved:

```text
ADMITTED 2026-10-18 by the Principal, after PD-002 and against the
Constitution as revised for it: PD-003 revision 4, dispositions
PD-003.1 to PD-003.5, as written, including the Principal's directions
of 2026-10-18 (hop depth 2; deterministic extraction only; discovery
units as a fixed grant; D-01 closed by Theme succession without
re-parenting).

Clarifications on admission:
(a) PD-003.6 (capital standings and exploratory expiry) is NOT admitted.
    It is PD-004, proposed, with its own ΔA. Until PD-004 is decided, a
    registered Strategy Version has allocation zero until an Allocation
    Transition applies, and no exploratory allocation class exists.
    FR-12 remains open.
(b) Checker extraction is not admitted. It is a future proposal
    dependent on D-10.
(c) ES-1 is not changed. Forward-event minimums, the decision-implied
    notional, treatment of UNESTIMATED values and search-family trial
    counts are Standard content for a later Constitutional Transition.
(d) FR-6 and FR-8 (Group B) are not admitted.

Constitutional Delta admitted:
ΔO: NONE.
ΔS: §III.1 Theme (selection basis; successor without re-parenting).
    §III.2 Hypothesis (motivated_by set; motivation closure; selection
    basis; document-sourced resolution members under six conditions).
    §III.3 Strategy (selection basis with search family; cited mechanism
    as reference). §III.4 Agent Design (method class). §III.5 Evidence
    (DOCUMENT form; feed items; feed retrieval records COMPLETE, PARTIAL,
    RETRIEVAL_FAILED; absence witness; hop chain; Research Record
    closure, typed claims, kinds SCREEN, EXPERIMENT DESIGN, SELECTION,
    SearchFamily label; NOT_EXTRACTABLE; Outcome pins SourceRevision).
    §III.7 Authorization (feed sources with enumeration contract; hop
    rule, depth default 2; discovery scope with fixed grant and cadence;
    deterministic extraction rules). Part V (Observation function feed
    retrieval; Checker verification of selection basis and search
    family). I-5 read set-valued.
ΔA: Observation Authorization: feed sources; hop rule. Research
    Authorization: discovery scope. No commit right, no time authority,
    no admission authority is created or moved.

Closed by this admission: FR-1, FR-3, FR-5, FR-7, FR-10, FR-11, FR-13,
D-01.
Open items preserved with owners: FR-12 (PD-004); UD-4 (Checker
extraction, with D-10); UD-10 (exploratory lifetime cap, a limit, with
PD-004); UD-11 and UD-12 (ES-1); UD-14 (Paper Book clock, Principal,
later); FR-4, FR-6, FR-8, FR-9 (Group B and C of the forward research
plan).
```

PD-003.6 is excluded; [PD-004](principal_decision_004_exploratory_capital_standings.md) remains proposed and unadmitted; FR-12 remains open. The Constitution as a whole remains a draft. Applied to the Constitution in revision 4 of 2026-10-18; re-audited in [osa_reaudit_pd003_20261018.md](../audits/osa_reaudit_pd003_20261018.md).

Prior status: proposed for admission, revision 4.

Date: 2026-10-18 (revisions 1 to 4)

## Separation of PD-003.6

The Principal's expiry clarification of 2026-10-18 and the OSA defect
found afterwards (an event quota does not establish calendar expiry or
guarantee flattening when the Runner dies; a reversal is new exposure)
concern capital standings and exploratory expiry only. That disposition is
now [PD-004](principal_decision_004_exploratory_capital_standings.md).
Where the examples below name a capital standing (`INCUBATING`,
`EXPLORATORY`, `QUALIFIED`), the name is PD-004's proposal; under this
record alone a registered Strategy Version simply has allocation zero
until an Allocation Transition applies.

## Principal's directions applied in revision 2

| Direction | Applied in |
| --- | --- |
| Hop depth default 2, under existing domain, count and resource limits | PD-003.1 |
| Documentary resolution: deterministic extraction only in the initial Constitution; Checker extraction a future proposal dependent on D-10 | PD-003.3 |
| Exploratory purpose stated per Allocation Transition | PD-004 (formerly PD-003.6) |
| Discovery units: fixed grant per Research Authorization | PD-003.1 |
| D-01: Theme succession without re-parenting existing Hypotheses | PD-003.4 |

Subjects: forward research audit defects FR-1, FR-3, FR-5, FR-7, FR-10,
FR-11, FR-12, FR-13; the Principal's directions on availability-
conditioned documentary resolution, deterministic extraction and
non-retrospective extraction rules, complete selection history, and the
exploratory/qualified distinction; the repair directions on expiry, feed
completeness and empirical selection history.

Sources: [forward research OSA audit, revision 2](../audits/forward_research_osa_audit_20261018.md)
(where this record and the audit's §3.1 or §4.4 differ, this record
supersedes); [forward research design plan](../plans/forward_research_design_plan.md);
[PD-001](principal_decision_001_identity_and_evidence.md) (admitted);
[PD-002 revision 4](principal_decision_002_predictions_decisions_observation.md);
[Constitution revision 2](../doctrines/new_speedway_constitution.md);
fin123-core at `8175d504`: forward evidentiary doctrine §5, §9, §11,
Constitutional Coherence doctrine (ANF). Focused audit:
[osa_audit_pd003_proposed_20261018.md](../audits/osa_audit_pd003_proposed_20261018.md).

Kept without change: the ten-object ontology; every admitted PD-001 rule
(Transition ledger authority with the Applied History as its applied
subsequence, Population State derived, pinning, the five Economic
Proposition boundaries, the evidence clock); every PD-002 disposition.

---

## PD-003.1. Autonomous feed-based Theme discovery and bounded follow-up (FR-10, FR-1)

### Feed sources and the enumeration contract

The Observation Authorization may declare **feed sources**: a `SourceId`
whose retrieval at a slot yields the items the source enumerates. A feed's
Source Declaration carries, as meaning fields, the **enumeration
contract**: what the feed enumerates completely (for example, every
filing of named form types accepted by the index), the window a retrieval
covers (since the previous slot, or a fixed look-back), the item identity
rule, and how completeness is established at retrieval (the source's own
count, an end-of-list marker, exhaustive pagination). Endpoint and parsing
are revision content.

Each item is committed by the Observation function as a Market
Observation of form `DOCUMENT` (PD-003.2) carrying the feed `SourceId`
and `SourceRevision`, the slot, the locator, the content hash, the claimed
publication time and the witnessed receipt.

### Retrieval completeness and absence witnesses

Each feed retrieval commits one **feed retrieval record** (a Market
Observation of the feed itself) with a result:

| Result | Meaning | Establishes |
| --- | --- | --- |
| `COMPLETE` | The retrieval satisfied the enumeration contract's completeness condition for its window | An **absence witness**, at the witnessed receipt time, for every item within the contract and window that the retrieval did not contain |
| `PARTIAL` | The source was reached but the completeness condition was not met (truncated list, pagination stopped, count mismatch) | Nothing about absence. Items it did return are ordinary `DOCUMENT` Observations |
| `RETRIEVAL_FAILED` | The source was not reached or could not be parsed | Nothing |

Rules:

1. A feed slot establishes absence only through a `COMPLETE` retrieval,
   and only for items the enumeration contract covers. An item of a form
   type or period the feed does not enumerate has no absence witness from
   that feed.
2. A delayed `COMPLETE` retrieval establishes absence at its actual
   witnessed time, never at the slot time it missed.
3. Absence from the declared source is what is established. It says
   nothing about availability through other channels; PD-002's narrow
   reading (N-4) stands. The only other lower bound is a structural bound
   the Checker accepted at registration.
4. An item that later appears with a claimed publication time earlier
   than a `COMPLETE` retrieval that did not contain it is recorded as
   such: the claimed time informs, the witness bounds.

### Discovery scope

A Research Authorization may carry a **discovery scope**:

| Field | Content |
| --- | --- |
| Feeds | The feed `SourceId`s the holder may screen |
| Units | A **fixed grant** of research units consumable on Research Records attributed to no Theme (screens, follow-ups, formation records before a Theme exists). Consumption by Research Records as work is done; remaining `DERIVED` |
| Follow-up caps | Maximum hop retrievals per period; maximum hop depth, **default 2**, under the Observation Authorization's domain list and the scope's unit grant |
| Screening cadence | The expected screening cadence per feed: within how many slots of an item's first receipt a screen is expected. Expected screens are derivable from the feed Observations; a missing screen is a visible gap counted in the lineage's evaluation. A gap does not invalidate any other lawful act of the lineage; it is contribution evidence, not a refusal |
| Expiry | As for every Authorization |

### Screening records

Under a discovery scope the holder commits Research Records of kind
`SCREEN`: the item's Evidence sequence, typed claims (PD-003.2), and a
disposition `CANDIDATE`, `DEFERRED` or `REJECTED` with a stated reason;
declared unit consumption. A `DERIVED` view over screens keyed by item
content hash shows every lineage's disposition of every item; a later
screen of the same item may differ and must state the difference.
Rejected candidates are preserved and are inputs to the evaluation of
selection (PD-003.5).

### The hop rule, replacing open retrieval

An on-request retrieval must cite the `DOCUMENT` Observation in whose
bytes the requested locator appears, and the chain from a feed item to the
cited Observation must be no longer than the scope's depth. The
Observation function verifies the locator is present in the cited bytes
before fetching; commits the result with the feed `SourceId` and a hop
marker carrying the chain; and refuses, with the refusal preserved by the
Evidence commit boundary, a request outside the requester's feeds, beyond
its depth, count or units, outside the Observation Authorization's
permitted domains, or whose locator is not in the cited bytes.
`SRC-ADHOC` does not exist. A source an agent cannot reach lawfully is
reason to propose a successor Observation Authorization, decided by the
Principal.

### Constitutional Delta

```text
ΔO: NONE.
ΔS: Source Declaration gains the enumeration contract (meaning fields).
    Market Observation gains feed retrieval records with results
    COMPLETE, PARTIAL, RETRIEVAL_FAILED; feed items; hop provenance with
    chain. Research Record gains kind SCREEN with dispositions and may
    cite no Theme under a discovery scope. Absence witness defined.
ΔA: Observation Authorization gains feed sources and the hop rule
    (depth, count, domains). Research Authorization gains a discovery
    scope (feeds, fixed unit grant, caps, cadence). The Observation
    function remains the only committer of Observations. No agent gains
    a commit right.
```

---

## PD-003.2. Document provenance (FR-5)

### `DOCUMENT` form of Market Observation

| Field | Assigned by |
| --- | --- |
| `SourceId`, `SourceRevision` (declared document source, feed, or feed with hop chain) | Observation Authorization; Observation function |
| Locator; content hash of the exact bytes; stored bytes addressed by hash (`RECEIPT`) | Observation function |
| Claimed publication time (`RECEIPT` content; informs, establishes nothing) | The document or index |
| Witnessed receipt time and sequence | Evidence commit boundary |
| Requesting Authorization and hop chain (hops only) | Observation function |

A later retrieval of the same locator with a different hash is a new
Observation; the earlier stands. Availability of a feed item is bounded
below by its absence witness (a prior `COMPLETE` retrieval within
contract) and above by first receipt. A hop retrieval has only the upper
bound unless the Checker accepted a structural bound for its source at
registration.

### Research Record closure and typed claims

Every Research Record records a **closure**: the Evidence sequences of
the Observations and Research Records it read, and the `StateVersion` it
read. Every claim carries one type:

| Type | Must cite |
| --- | --- |
| `REPORTED` (a statement the document makes) | A `DOCUMENT` Observation and a location in it |
| `INTERPRETATION` (the agent's reading) | The `REPORTED` claims it rests on |
| `ASSUMPTION` (a premise without a source) | Nothing; declared as such |
| `QUESTION` | The claims that motivate it |
| `PREDICTION_REF` | A committed Prediction's sequence |

A claim citing bytes outside the closure is unsupported on its face. The
agent reads from the ledger copy; anything read elsewhere is `EPHEMERAL`
and cannot be cited. Research Record kinds `EXPERIMENT DESIGN` (names a
resolution set and must precede every Prediction over it) and `SELECTION`
(PD-003.5) are added. A Research Record may carry a declared
`SearchFamily` label (PD-003.5).

```text
ΔO: NONE.
ΔS: Market Observation gains the DOCUMENT form. Research Record gains a
    closure, typed claims, kinds EXPERIMENT DESIGN and SELECTION, and
    an optional SearchFamily label.
ΔA: NONE.
```

---

## PD-003.3. Formation versus resolution evidence; documentary resolution (FR-11)

### The line

A Hypothesis registration declares a **motivation closure**: the Research
Records and Observations that formed it. No member of a Prediction's
Hypothesis's motivation closure may be a member of that Prediction's
resolution set. Formation evidence never tests. Standing is built only
from Outcomes.

### When a document may resolve

A resolution-set member may be a **document-sourced field** only when all
of the following were fixed in the Prediction's resolution rule at
commitment and hold at resolution:

| Condition | Rule |
| --- | --- |
| Source identity | A declared document source or feed `SourceId` under an Observation Authorization active at commitment; never a hop retrieval |
| Period or event | The period the document must report, or the event it must announce |
| Field meaning | The quantity, unit and definition as the source defines it. Field meaning is a meaning field of the `SourceId`: a change is a new `SourceId` |
| Print rule | First posting or a named amendment |
| Extraction rule | A **deterministic** rule carried in the `SourceRevision` pinned at commitment (below). A source with no deterministic extraction rule cannot be a resolution source; its documents are formation evidence only |
| **Independently established availability** | The resolving Observation's availability interval has a lower bound: for a feed item, a prior `COMPLETE` retrieval within the enumeration contract that did not contain it; for a directly retrieved document source, an `ABSENT` result at a declared absence slot; or a structural bound the Checker accepted at registration. The Prediction's commitment precedes that bound. A later Evidence sequence alone is not sufficient. A `PARTIAL`, failed or delayed retrieval establishes nothing. Where no lower bound exists, prospective classification is refused as for any value (PD-002); the Outcome is still committed, as Historical Reconstruction with the reason recorded |

### Extraction: deterministic only

The Source Declaration carries an extraction rule (a tagged data element,
a named table cell, a fixed parser with content hash). The Observation
function applies it at retrieval and commits a `VALUE` result bound to
the `DOCUMENT` Observation; the value is then an ordinary Market
Observation and resolves like a price. If the rule yields no value from
the bytes, the function commits `NOT_EXTRACTABLE` bound to the document,
and the Outcome over that member is `UNRESOLVABLE`.

**No retrospective change to an extraction rule.** The rule is content of
the `SourceRevision` pinned by the Prediction at commitment. A changed
rule is a new `SourceRevision` that applies only to Predictions committed
after it; the Outcome pins the revision it used; a Prediction whose pinned
revision can no longer be applied resolves `UNRESOLVABLE`, never under a
newer rule.

**Checker extraction is not part of this record.** Adjudicated
extraction for sources without a deterministic rule is a future proposal
dependent on D-10 (Checker independence). Revision 1's draft of its
authority is preserved in the audit as a rejected-for-now alternative.

```text
ΔO: NONE.
ΔS: Hypothesis registration gains a motivation closure. Resolution-set
    members may be document-sourced fields under the six conditions.
    Source Declaration gains deterministic extraction rules. Observation
    results gain NOT_EXTRACTABLE. Outcome pins SourceRevision.
ΔA: NONE. (Revision 1's Checker extraction-record commit right is
    withdrawn.)
```

---

## PD-003.4. The explanatory graph, selection basis, and Theme succession (FR-3, FR-7, D-01)

- A Hypothesis's `motivated_by` is a **set** of Themes and Research
  Records recorded in its registration proposal. Funding is exactly one
  Authorization. §III.1's "belongs to at most one Theme" is removed.
  Lineage memory (I-5) is read set-valued and is unchanged in kind.
- **D-01, as directed:** a Theme's scope change is a successor Theme
  citing its predecessor. Existing Hypotheses are not re-parented; their
  `motivated_by` sets stand, and a Hypothesis registered under the
  successor cites the successor. The predecessor's standing becomes
  retired by the same Transition. Lineage memory for the successor
  includes the predecessor's by the predecessor reference.
- Theme and Hypothesis registration carry a **selection basis** (fields
  in PD-003.5).
- Cited Hypotheses and `motivated_by` references transfer no standing.
  Explanatory standing of a Strategy's declared mechanism is `DERIVED`
  from the standing of the Hypotheses it cites; whether the mechanism
  field is immutable as declared (FR-6) is Group B and not admitted here.

```text
ΔO: NONE.
ΔS: Hypothesis relationship to Themes; Theme succession without
    re-parenting (D-01 closed); selection basis as registration content.
ΔA: NONE.
```

---

## PD-003.5. Research selection history on both discovery paths; AIE optional and replaceable (FR-7, FR-9)

### The selection basis, on every registration that spends research or capital attention

Theme registration, Hypothesis registration and **Strategy Version
registration** each carry a selection basis:

| Field | Content | Note |
| --- | --- | --- |
| Question or purpose | What the registration proposes to find out or capture | |
| Alternatives actually considered | The candidates compared: for a Theme, the screens or records it was chosen over; for a Strategy Version, the search family's other trials (signals, parameters, universes), each by Research Record sequence | The empirical path records parameter and universe trials here; no Theme or Hypothesis is required |
| Unsuccessful trials | Research Records with negative or inconclusive results in the same search family, by sequence | Historical Reconstruction trials included; never grounding |
| Reason for proposing | Why this candidate, in the proposer's words, typed as `INTERPRETATION` or `ASSUMPTION` | |
| Budget consumed to date | `DERIVED` from Research Records under the search family and Authorization; the proposal states the figure it read and its `StateVersion` | |
| Value estimate | A figure with its declared basis (fin123-core §11), **or `UNESTIMATED` with the reason** (no defensible basis; no comparable history; the question is exploratory) | No precision is invented. `ES-1` may treat `UNESTIMATED` as it sees fit; nothing here penalizes it |
| Cost and time estimate | Units and calendar time, or `UNESTIMATED` with reason | |
| Horizon and stopping rule | When the question is considered answered or abandoned | |
| Origin | The `SELECTION` record that chose it; or "discovery-scope initiative"; or "empirical search family `SearchFamily` X" | |

### Search families

A Research Record may declare a `SearchFamily` label naming the family of
trials it belongs to (a Theme's experiments; a lineage's parameter search
over one signal idea). It is content, not an object; a `DERIVED` view
groups Research Records, Predictions and Strategy Versions by it. The
Evaluation Standard counts trials across a family (FR-8, Group B). A
Strategy Version registration names its family; the Checker verifies the
alternatives and unsuccessful trials cited are in it.

### The selection method, when one is used

A research-selection method is an **Agent Design lineage** whose
registration declares method class `SELECTION`. It holds an ordinary
Research Authorization and, where the Principal wishes, a discovery
scope. It proposes; it admits and funds nothing. Applied Information
Economics is one such method, **optional**: a lineage may select by any
declared method or by none, in which case registrations cite their origin
directly. Replacing a method is an Authorization act (`0/0/0`).

### The selection record

Every `SELECTION` Research Record carries: method (`AgentDesignVersionId`,
Authorization); closure; the full candidate set with each candidate's
value estimate or `UNESTIMATED`, cost estimate, horizon, stopping rule and
the screens or records it came from; the chosen subset linked to the
proposing Transitions; every rejected candidate with reason; and a revisit
rule.

### What makes the history complete, on both paths

| Fact | Where it lives |
| --- | --- |
| What was chosen and rejected, and why | `SELECTION` records where a method was used; otherwise the registration's selection basis (alternatives and reason) |
| Unsuccessful trials | Research Records in the search family |
| What the chosen work cost | Research Records' consumption under the family and Authorization; `DERIVED` sum |
| How long it took | Registration Apply to the standing Transition that closed the question; `DERIVED` |
| What it found | Outcomes, Decisions and Evaluations |
| Whether it changed a decision | Transitions citing those Evaluations; `DERIVED` |
| What rejected candidates became | Later screens, `SELECTION` records and registrations citing them; `DERIVED` join on item hash or question hash |
| Estimate error, or that there was no estimate | `SELECTION OUTCOME`, a `DERIVED` Evaluation under `ES-1` |

```text
ΔO: NONE.
ΔS: Selection basis as content of Theme, Hypothesis and Strategy Version
    registration, with UNESTIMATED permitted. SearchFamily label on
    Research Records. Agent Design method class. SELECTION record fields.
ΔA: NONE. A selection lineage holds an ordinary Research Authorization.
```

---

## PD-003.6 — removed to PD-004

Capital standings, the exploratory pool, the `EXPLORATORY` label, expiry
and the opening-exposure rule are proposed in
[PD-004](principal_decision_004_exploratory_capital_standings.md) and are
not part of this record. FR-12 stays open until PD-004 is decided.

Note, 2026-10-19: PD-004 was admitted (revision 3 with the
internal-simulator clarification) and FR-12 closed. The exploratory rows
of the two-case test below (momentum "Exploratory" row; forward steps
8e, 9b, 9d) describe the superseded decision-count mechanism and are
kept as the record of what this revision proposed; the admitted worked
text is PD-004 §PD-004.9 and Constitution T-H.

---

## Two-case test against PD-003 revision 4 (dispositions 1 to 5)

### Traditional momentum (`SV-8.1`, lineage `SL-8`)

| Step | Act | PD-003 rule exercised |
| --- | --- | --- |
| Discovery | None. `AD-3.3` under `AU-27` studies `SRC-E` closes | Discovery scope, feeds, screens unused |
| Formation and trials | Research Records `RR-300` to `RR-312` in `SearchFamily SF-8`: twelve lookback and rebalance variants, nine negative or inconclusive, constants declared with periods used; class Historical Reconstruction | PD-003.2 closure and typed claims; PD-003.5 search family |
| Registration | `SV-8.1`, mechanism `none claimed`, motivated_by {`RR-300`}; **selection basis**: alternatives `RR-301` to `RR-312`; unsuccessful trials listed; reason (`INTERPRETATION`); budget consumed 31 units (derived, at `StateVersion` 47); value estimate **`UNESTIMATED`** (reason: no forward history of this family); cost estimate 20 units over 12 weeks; stopping rule 20 forward events; origin "empirical search family SF-8" | PD-003.5 on the empirical path, with no Theme, no Hypothesis, no selection method |
| Check | Alternatives and trials verified in `SF-8`; `UNESTIMATED` accepted as stated | |
| Incubation | `INCUBATING`; Runner Decisions; decision-implied record | PD-003.6 |
| Exploratory | `TR-355`: `EXPLORATORY` 1 unit, purpose "measure fills and Friday clustering", `expiry_events = 8`, instruction `FLATTEN`. The ninth Friday Decision: the Paper Book boundary establishes index 9 > 8 at admission and refuses opening orders; the Execution function cancels open opening orders and derives the flattening set keyed `TR-355:N:EXPIRY`; `TR-356` (scheduled standing Transition) records allocation 0. Had the Runner died after the eighth Decision, no opening order could be admitted and the eighth position would stand as a visible fact | PD-003.6 expiry |
| Qualification | `QUALIFIED` on forward events only; exploratory record shown, labelled, excluded from grounding | PD-003.6 rule 3 |

The empirical path now carries a complete selection history without a
Theme or an explanatory Hypothesis, and states no estimate it cannot
defend.

### Forward product-rebalancing (`TH-14`, `HY-140`/`141`/`142`, `SV-40.1`)

Sequence as in the audit §4.1 (serially admitted, `N` 54 → 67), with
revision 2 and 3 differences:

| Step | Revision 2 rule |
| --- | --- |
| 0a | `AU-02c` declares `SRC-EDGAR-NEW` with an enumeration contract (all filings of named form types accepted by the index; window since previous slot; completeness by the index's count); hop depth 2; permitted domains: the two feeds and the issuer |
| 0b | `AU-31`: discovery scope with a fixed grant of 40 units, cadence "screen within two slots of receipt" |
| 1a | 12-01 19:00 retrieval `COMPLETE` (count matched) and did not contain `DO-1`; 12-02 07:01 retrieval `COMPLETE` contains it. `DO-1`'s availability from the declared source: (12-01 19:00, 12-02 07:01]. Its claimed time 17:40 informs only. Had the 19:00 retrieval been `PARTIAL`, no lower bound |
| 1b | `RR-390` screens all 41 within cadence; the view shows no gap |
| 1c | Hop 1 to the prospectus exhibit `DO-2` (permitted). Hop 2 to the issuer's product page linked in the exhibit: depth 2 permitted, domain permitted, units available → `DO-3` committed. Hop 2 to a third-party commentary article: depth permitted, **domain refused**; refusal preserved |
| 2 | `TR-400` selection basis: value estimate `UNESTIMATED` (reason: no precedent for this product class on this underlying); cost 60 units over 8 weeks; origin "discovery-scope initiative" |
| 4b | `HY-142`'s resolution member: `SRC-P`, period 2026-12-31, field "net assets, USD", first posting, deterministic `R-P1` under the pinned `SourceRevision`. Had `SRC-P` carried no deterministic rule, `HY-142` could not have been registered with that member |
| 6a | `PR-642` forward: `SRC-P`'s 17:45 `ABSENT` on 12-31 (a direct retrieval of the specific locator, complete by construction) is the lower bound; commitment on 12-05 precedes it |
| 8e | `TR-415`: `EXPLORATORY` 1 unit, purpose "measure fill quality and timing sensitivity of 15:30 entries", `expiry_events = 10`, instruction `FLATTEN` |
| 9a | `DO-9` retrieved; `R-P1` applied by the function; `VALUE` committed; `OC-642` binds the set and pins the revision. Counterfactual: layout change on 12-20 → `NOT_EXTRACTABLE` → `UNRESOLVABLE`; no newer rule applied |
| 9b | Eleventh decision event `SD-4011` (`E=2 836`): the Paper Book boundary establishes index 11 > 10 from the Evidence ledger and the allocation's content, and refuses the opening order; the Execution function records its refusal, cancels open opening orders of sets under `TR-415`, and derives the flattening set `TR-415:63:EXPIRY` from positions at the Paper Book head (for this 30-minute Strategy the tenth set already flattened at 16:00, so the flatten set is empty and recorded as such); a fill of a pre-expiry order that races a cancel is recorded under the label. `TR-416` (scheduled standing Transition, Principal or policy; `CK-H1` verifies count, refusals, cancels, flatten) applies at 63 → 64: allocation 0, `INCUBATING` |
| 9d | `EV-200` shows the exploratory record, including refusals, cancels and the empty flatten set, labelled and excluded from grounding |
| 13 | `AD-7.1`'s evaluation counts the 39 rejected screens, the screening coverage (no gaps), and `TR-400`'s `UNESTIMATED` value against the realized 70 units and 7 weeks |

Both paths run under one set of rules. Each exercises the selection
basis, capital standings and expiry; only the forward path exercises
feeds, hops and document resolution.

---

## Aggregate Constitutional Delta of PD-003 revision 4 (dispositions 1 to 5)

```text
ΔO: NONE. No governed object, ledger or Evidence kind is added.
    DOCUMENT is a form of Market Observation; feed retrieval records are
    Market Observations of the feed; SCREEN, EXPERIMENT DESIGN and
    SELECTION are Research Record kinds; SearchFamily is a Research
    Record label.

ΔS: §III.1 Theme (selection basis; successor without re-parenting,
    D-01 closed).
    §III.2 Hypothesis (motivated_by set; motivation closure; selection
    basis; document-sourced resolution members under six conditions).
    §III.3 Strategy (selection basis with search family; cited
    mechanism as reference).
    §III.4 Agent Design (method class).
    §III.5 Evidence (DOCUMENT form, feed items, feed retrieval records
    with COMPLETE/PARTIAL/RETRIEVAL_FAILED, absence witness definition,
    hop chain; Research Record closure, typed claims, kinds, SearchFamily;
    NOT_EXTRACTABLE; Outcome pins SourceRevision).
    §III.7 Authorization (feed sources with enumeration contract, hop
    rule with depth default 2, discovery scope with fixed grant and
    cadence; deterministic extraction rules in Source Declarations).
    Part V (Observation function feed retrieval; Checker verification
    of selection basis and search family).
    I-5 read set-valued.

ΔA: Observation Authorization: feed sources; hop rule (depth, count,
    domains). Research Authorization: discovery scope (feeds, fixed
    grant, caps, cadence). No commit right and no time authority is
    created for any agent or function.
    No admission authority moves. (Revision 1's Checker extraction-record
    right is withdrawn.)
```

## Blockers and dependencies

| Item | Standing |
| --- | --- |
| PD-002 admission | Required first: Observation function, Runner, closures, resolution sets, `SourceId`/`SourceRevision`, availability interval |
| Checker extraction | Not in this record; future proposal dependent on D-10 |
| `ES-1` | Not changed; forward-event minimum, notional, `UNESTIMATED` treatment, search-family counting are Standard content (Group B) |
| FR-6, FR-8 | Group B, not admitted here |
| FR-12 (capital standings, expiry) | PD-004, proposed; carries a declared `ΔA` |
| D-10, D-11, D-12, D-14, D-17, N-1 | Untouched |

No constitutional blocker to admitting PD-003 remains once PD-002 is
admitted.

## What happens on admission

1. Constitution revision 3 in the sections listed, reconciled against
   ANF and fin123-core §5, §9, §11; the product-P sequence enters Part VI
   as T-H; the momentum selection basis joins T-B.
2. Re-audit for duplicate ownership among feed items, feed retrieval
   records, screens and formation records; for expiry-time authority; for
   exploratory leakage into qualification; for selection-history
   completeness on both paths.
3. FR-1, FR-3, FR-5, FR-7, FR-10, FR-11, FR-13 and D-01 closed by
   reference; FR-12 stays open for PD-004.
4. Next: `ES-1` drafting with FR-6 and FR-8, then D-10 with D-11, which
   also carries the Checker-extraction proposal and PD-002's U-10.
