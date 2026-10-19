# Principal Decision Record 002 — Predictions, Strategy Decisions, and Independent Market Observation

Status: **ADMITTED 2026-10-18 by the Principal.** Admission text, as approved:

```text
ADMITTED 2026-10-18 by the Principal: PD-002 revision 4, dispositions
PD-002.1 to PD-002.6, as written.

Clarifications on admission:
(a) The Outcome committer remains as drafted (any authorized party, with
    expected Outcomes derivable and values recomputable) pending U-10,
    to be decided with D-10. No change is declared.
(b) The Strategy Runner, the Execution function and the Observation
    function are distinct in authority. Whether they run in separate
    processes is an operating decision outside the Constitution.
(c) Nothing in this admission certifies replay, recovery or any
    implementation. N-1 (genesis) remains a bootstrap issue that must
    close before any conformance claim.

Constitutional Delta admitted:
ΔO: +1 Evidence kind (Strategy Decision). Nothing else.
ΔS: Strategy (prediction target; declared inputs, trigger,
    reproducibility class; forward record as Decision series; frozen
    model admissible). Evidence (Decision fields and rules;
    DecisionEventId; closure and witness marks; Observation result,
    times, SourceId/SourceRevision; Prediction resolution rule and set;
    Outcome over a bound set, UNRESOLVABLE; Evaluation closure;
    availability interval; I-2 to the lower bound; derived reproduction
    standing). Paper Book (set key; order types; remainder from fills;
    limit refusal). Authorization (Observation and Runner content;
    Source Declaration identity rule; base-state rule). Agent Design
    (training cutoff as provenance). Evidence commit boundary (witness-
    read duty; refuse when a head is unreachable).
ΔA: +2 Authorization classes (Observation, Runner); +2 function roles.
    Commit restrictions: Market Observation -> Observation function;
    Strategy Decision -> Runner; reproduction record -> Checker
    Authorization; execution facts -> Execution function. Execution
    function rights unchanged, duties added. No admission authority
    moves. Pending U-10: no change.

Open items preserved with owners: U-1, U-2, U-4, U-5 (D-17), U-6
(ES-1), U-7 (N-1), U-8, U-10; D-10, D-11, D-12, D-14, D-17; N-1, N-2,
N-4, N-6; D-01 (closed by PD-003 if admitted), D-06, D-09.
```

The Constitution as a whole remains a draft. Applied to the Constitution in revision 3 of 2026-10-18; re-audited in [osa_reaudit_pd002_20261018.md](../audits/osa_reaudit_pd002_20261018.md).

Prior status: proposed for admission, revision 4, prepared through revisions 1 to 4 on 2026-10-18.

Date: 2026-10-18 (revisions 1 to 4)

Subjects: re-audit questions N-5 (what a Strategy Version predicts and
where its forward record lives) and N-3 (independence of availability
evidence); N-1 (Constitution genesis) recorded as a bootstrap issue; U-9
(who runs a Strategy Version).

Sources: [PD-001](principal_decision_001_identity_and_evidence.md)
(admitted); [PD-001 re-audit](../audits/osa_reaudit_pd001_20261018.md);
[Constitution revision 2](../doctrines/new_speedway_constitution.md);
fin123-core `docs/top_doctrines/method_forward_evidentiary_doctrine.md`
at `8175d504` §5 (Prediction is an execution artifact, bound to one
revision, written before the answer is known, fixed at commitment), §6
(an Outcome evaluates a committed claim, never the explanation directly;
a declined claim is a claim), §9 (two classes, never merged; the author
of a reconstruction knew how the period ended);
`docs/top_doctrines/iris_constitutional_coherence_doctrine.md` (Authority
Normal Form, the seven invariants).

Numbering note. PD-001 labelled its three dispositions PD-001, PD-002 and
PD-003, and the Constitution cites them that way. This record is decision
record 002 and labels its dispositions PD-002.1 to PD-002.6. The revision
list at the end asks that the earlier citations be renamed PD-001.1 to
PD-001.3.

## Revision history

| Revision | Content |
| --- | --- |
| 1 | PD-002.1 (Decisions), PD-002.2 (Observation), PD-002.3 (genesis), two examples |
| 2 | Five review points: closure over three ledgers; Decisions authorize nothing, failures preserved, reproduction standing derived; Source identity and revisions, absence versus failed retrieval; frozen models, reproducibility class Checker-found; adversarial findings A-1 to A-14, defects U-1 to U-8 |
| 3 | Verification against the Constitution and challenges: commit-time witness marks (V-1); the runner's Authorization missing (V-2, U-9) |
| 4 | PD-002.4 Strategy Runner (U-9 decided direction); PD-002.5 Source stays in Authorization; PD-002.6 training cutoff into D-14 as provenance; final checks F-1 to F-4 (authorization chronology, multi-observation Outcomes, decision-event identity and idempotent commit, witness-read authority and no atomic snapshot); both examples re-run on one timeline; readiness statement |

---

## PD-002.1. Predictions and Strategy Decisions (N-5)

### The distinction, as directed

| Term | Meaning | Where it lives |
| --- | --- | --- |
| Hypothesis | A testable claim about market behavior, with falsifier and declared resolution rule | Membership and standing in the Applied History; content on the Transition ledger |
| Prediction | A committed, measurable claim: target, tolerance, resolution rule over a declared observation set, fixed at a commitment time | Evidence ledger |
| Strategy Version | An executable policy mapping a closed set of admitted inputs into target exposures | Membership, standing and allocation in the Applied History; artifact content on the Transition ledger |
| **Strategy Decision** (new Evidence kind) | The committed output of executing one Strategy Version for one decision event against one input closure | Evidence ledger, committed by the Strategy Runner (PD-002.4) |
| Allocation | Capital granted to an exact Strategy Version, and the limits in force | Applied History |
| Order, Fill | What was sent, replaced, cancelled and done | Paper Book, committed by the Execution function |
| Position | What is held | `DERIVED` from fills |
| Market Observation | A `RECEIPT` of what a declared source returned and when the system held it | Evidence ledger, committed by the Observation function |
| Outcome | Resolution of exactly one Prediction by its resolution rule over exactly one bound observation set | Evidence ledger |
| Reproduction record | An Evaluation-kind record stating whether an independent re-execution of a Decision against its closure reproduced its hash | Evidence ledger, committed under a Checker Authorization |
| Evaluation, P&L, ranking | Assessment under a pinned Evaluation Standard | `DERIVED` |

A Strategy need not produce an explicit forecast to be testable. Its
testable claim is implicit in every Decision: *exposures of this sign on
this scored observable, held over this horizon, earn a positive payoff.*
The Evaluation Standard scores that claim. A Strategy Version may also
commit explicit Predictions where its proposition makes one natural, but
no trade is ever a Prediction.

**A Strategy Decision authorizes nothing.** It is not an allocation, which
only an applied Allocation Transition grants, and not an execution
authorization, which only the Principal's Execution Authorization grants.
It is an input the Execution function reads.

### The Strategy Decision record

One record per decision event, never per order.

| Field | Content | Assigned by |
| --- | --- | --- |
| `StrategyVersionId` | The exact artifact that ran | Runner; verified by reproduction |
| `DecisionEventId` | Stable identity of the event (see Decision events) | Derived from the declaration and the trigger instance; verified by the commit boundary |
| Input closure | Bindings, see below | Runner; checkable against the ledgers |
| Commit-time witness marks | Applied History head and Paper Book head observed by the Evidence commit boundary, each with the Evidence-clock instant of its read | Evidence commit boundary |
| Output | Target exposure vector in fractions of allocated capital; or `DECLINED` with the rule that declined; or `FAILED` with the failure class | The artifact, or the Runner for `FAILED` |
| Content hash | Hash of closure plus output | Evidence commit boundary |
| Commitment time and sequence | When the Decision became a ledger fact | Evidence commit boundary's clock, never the Runner |

Class and reproduction standing are not fields; both are derived.

### Decision events: stable identity and idempotent commitment

A Strategy Version declares its trigger at registration: a schedule
(calendar of slots) or a ledger event (a new `VALUE` Observation of a
named `SourceId`; a new Prediction of a named `HypothesisLineageId`). Each
trigger instance yields exactly one decision event:

```text
DecisionEventId = hash( StrategyVersionId, trigger declaration hash,
                        slot identifier            for a schedule trigger
                        | Evidence sequence of the triggering record
                                                   for a ledger-event trigger )
```

Rules enforced by the Evidence commit boundary:

1. **One Decision per event.** A second Decision commit for the same
   `DecisionEventId` is refused and the refusal preserved by the boundary.
   Two Runner processes racing the same event produce at most one record;
   the loser's refusal is a fact. If the two would have differed, only
   reproduction can show it, which is why reproduction is retained as the
   check on the Runner itself.
2. **`FAILED` is final for its event.** It is an artifact result against
   a fixed closure; a retry against the same closure cannot differ. The
   next event is the next trigger.
3. **Infrastructure failure commits nothing.** A Runner that dies, times
   out or cannot reach a ledger before commit leaves no record; retrying
   the event is lawful until a Decision exists for it. The expected set of
   events is derivable from the declaration and the ledgers, so an event
   with no Decision is visible as missing.
4. **Event identity is independent of the Runner.** Any Runner process,
   under any Runner Authorization, computes the same `DecisionEventId`.

### Input closure

| Ledger | Admissible inputs | Mark recorded | Rule |
| --- | --- | --- | --- |
| Evidence | Market Observations; Predictions; Outcomes; Strategy Decisions of any version; committed Evaluations | Evidence high-water mark `E` | Every Evidence input has sequence ≤ `E`; the Decision's own sequence is > `E`. Enforced by the Evidence commit boundary |
| Applied History | The projection at a `StateVersion`: allocation to this version, limits, standing of cited objects, active Authorizations | `StateVersion` `N` | The artifact reads the projection at exactly `N` |
| Paper Book | Fills, open orders, replaces and cancels up to a Paper Book sequence, from which positions are derived | Paper Book sequence `F` | Positions derived from fills ≤ `F`; no stored position is an input |

Rules:

1. **Bindings, not copies.** The closure names records by ledger and
   sequence and carries a hash of their resolved content. It never carries
   values, so a Decision cannot become a second carrier of any
   Observation, allocation or fill.
2. **Declared kinds only.** Registration declares input kinds and
   `SourceId`s inside the artifact's content hash. "Authorized" input means
   declared at registration and verified at Check. Reading a ledger fact
   needs no Authorization and this record creates no reading right.
3. **No external mutable state.** The market data store (`CACHE`), vendor
   APIs, files, environment, wall-clock time and agent memory are not
   admissible inputs. Backfilled Observations are admissible inputs; their
   late witness affects the class of scoring, not admissibility.
4. **Predictions as inputs are inputs, not standing** (I-1).
5. **Decision-time currentness is witnessed at commit.** See F-4 for the
   exact claim the witness makes and the authority under which it reads.
   The boundary refuses a closure whose `N` or `F` exceeds the witnessed
   head. Staleness, the gap between a claimed mark and its witness, is a
   recorded fact. A future read is impossible; a stale read is lawful and
   visible.

### Reproducibility

Reproduction is re-execution of the artifact against the closure, with the
closure the only thing available, by a party other than the Runner that
committed the Decision, under a Checker Authorization. It must yield the
same content hash.

- **Reproduction records** are Evaluation-kind Evidence commits naming the
  Decision, the reproducing party and Authorization, the obtained hash,
  and match or divergence. Any number may exist. Only Checker
  Authorizations may commit them. Which Checker Authorizations qualify is
  D-10, not decided here. **The Runner never certifies reproduction**
  (PD-002.4).
- **Reproduction standing is derived**: `UNVERIFIED`, `REPRODUCED`,
  `UNREPRODUCED`, `DISPUTED` (decided by the Principal). Nothing is stored
  on the Decision.
- **Reproducibility class of a Strategy Version** is found by the Checker
  at registration by test execution: `REPRODUCIBLE` when two executions
  against one closure with the closure alone available yield one hash;
  otherwise `NON-REPRODUCIBLE`.
- **A frozen model may be part of a Strategy Version**: weights,
  tokenizer, inference configuration and seed are in the artifact and the
  content hash, held by the system. A model reached by external call, or a
  hosted model whose version the system cannot fix and verify, makes the
  artifact `NON-REPRODUCIBLE`.
- **Decisions of a `NON-REPRODUCIBLE` Strategy Version** are committed,
  preserved and scored. They cannot obtain `REPRODUCED` standing, and
  under the current Evaluation Standard no record without it grounds
  capital competition, so an Allocation Transition citing such a record
  is `STOPPED` (I-14). What else might ground it is undecided (U-1). No
  future Standard is proposed.

### Evaluation and the two performance records

| Series | Computed from | Notional | Use |
| --- | --- | --- | --- |
| Decision-implied record | Forward-class Decisions marked with declared-print Observations across the horizon, with the Standard's cost model | A notional the Standard declares, the same for every version; never the proposer's and never the allocation | Exists at zero allocation; comparable across versions; the incubation record |
| Executed record | Paper Book fills marked with the same Observations | The actual allocation | Exists only where capital was allocated and executed |

Shortfall is the reported difference. Proposed Standard content: decision-
implied grounds competition while unallocated, executed once allocated,
both always shown; `UNREPRODUCED` and `UNVERIFIED` shown but not counted
in the grounding series; `FAILED` and missing events counted against.
Every Evaluation records its own closure (`E`, `N`, `F`) and Standard
version.

### Execution trace

The Execution function, under the Execution Authorization, consumes
committed Decisions, the current allocation and limits, and the Paper
Book, and alone commits paper execution facts.

| Element | Rule |
| --- | --- |
| Order set key | `TransitionId:StateVersion:DecisionSeq` (applied Allocation Transition; head read at order time; Decision's Evidence sequence) |
| Order | `OrderId` = key plus index; type `NEW`, `REPLACE` or `CANCEL`; `REPLACE` names its parent and may carry only the parent's unfilled remainder as derived from fills at the Paper Book head |
| Fill | Bound to one `OrderId`; partial fills are several Fill records; positions derive from fills only |
| Retry | A `REPLACE` of the remainder, never a second `NEW`; a `REPLACE` that would overfill is refused and the refusal recorded |
| Supersession | Before a set for a newer Decision of the same version, `CANCEL` for open orders of the older set |
| Re-execution at a new allocation | When the head moves, the standing Decision is re-executed at the new `StateVersion` with a new key; the Decision is unchanged |
| Idempotency | The Paper Book refuses a second set with the same key and a second order with the same `OrderId` |
| Limits | An order that would breach a limit in force at the head is refused; the refusal is a Paper Book fact (U-8; plan step 7) |

### Consistency with the five boundaries (PD-001, D-03)

| Boundary | Meaning under this record | Purely empirical Strategy |
| --- | --- | --- |
| Mechanism | Why the payoff should exist | `none claimed` |
| **Prediction target** | **The scored observable and its sign: what the Standard marks every Decision against, and the direction claimed.** A scoring commitment, not a causal one | Required: "long-short spread return of top versus bottom momentum decile, positive" |
| Market or domain | Instruments, universe, venue | Required |
| Horizon | The band each Decision's score runs over | Required |
| Payoff | What is earned when right; shape of loss when wrong | Required |

Changing the scored observable, its sign or the scoring horizon is
`Proposition delta: NEW`. Changing signal construction, inputs within the
declared kinds, trigger, or a frozen model's weights is implementation,
subject to the Checker's independent equivalence finding, and always a
new `StrategyVersionId` at zero.

---

## PD-002.2. Independent Market Observation (N-3)

### Principle

A proposing agent must not control the evidence used to establish
information availability. Availability is established only by records the
proposer could not have timed.

### The Observation function and its Authorization

| Element | Proposal |
| --- | --- |
| Role | **Observation function**: the retrieval process. Not an Agent Design Version |
| Authorization class | **Observation Authorization**, granted only by the Principal |
| Content | Source Declarations; for each `SourceId`, an observation plan: retrieval slots including absence-witness slots; expiry |
| Permitted | Retrieve each declared source at its slots; commit the result as a Market Observation; nothing else |
| Denied | Proposing any Transition; committing any other Evidence kind; checking; running Strategies; executing |
| Exclusivity | No other Authorization includes the right to commit a Market Observation. A Research Agent reads the market data store (`CACHE`) for research; what it reads there establishes nothing and is not a Decision input |
| Plan change | Only a successor Observation Authorization by the Principal |

**No second owner of Market Observations.** The Evidence ledger owns them
and assigns sequence and witnessed time. The Authorization restricts who
may call that commit boundary for this kind.

### Source Declaration (PD-002.5: stays here; no new governed object)

| Element | Rule |
| --- | --- |
| `SourceId` | Immutable. Names the meaning fields: provider, dataset, field, unit, print rule (first print or named final), claimed-time field, structural availability bound if accepted |
| `SourceRevision` | Content hash of the full declaration including non-meaning fields: endpoint, access method, parsing rule. A successor Authorization may carry a new revision of the same `SourceId` only if every meaning field is identical; a changed meaning field is a new `SourceId` |
| Pinning | Every Market Observation records `SourceId` and `SourceRevision`. Hypotheses and Strategy Versions bind `SourceId` only |
| Owner | The Observation Authorization that carries it, a Principal act on the Transition ledger |
| Check | A Checker refuses a Hypothesis or Strategy Version registration whose `SourceId`s were not under an active Observation Authorization **at the registration's base state**, because no forward record could be established for it. See F-1 |

### Retrieval results, receipt, and established availability

| Result | Meaning | Contributes to availability |
| --- | --- | --- |
| `VALUE` | The source returned a value for the period; claimed source time and witnessed receipt time recorded | Upper bound: earliest `VALUE` receipt |
| `ABSENT` | The source was reached and returned no value for the period | Lower bound: latest `ABSENT` before the first `VALUE`. **A retrieval result: the function could not retrieve the value then. Not a statement that the market event had not occurred or that the value existed nowhere** |
| `RETRIEVAL_FAILED` | The source was not reached or the response could not be parsed | Nothing; preserved |

Claimed source time is `RECEIPT` content and establishes nothing.
Witnessed receipt time, from the Evidence clock at commit, is a fact.
**Independently witnessed receipt is a fact; independently established
availability is a derived interval**, never a single time and never
authoritative:

```text
lower bound = max( latest ABSENT before first VALUE, structural bound if accepted )
upper bound = first VALUE receipt
```

Where no `ABSENT` precedes the first `VALUE` and no structural bound is
accepted, the interval has no lower bound. A publication schedule is never
a bound.

### The authoritative record of the three times

| Fact | Authoritative record |
| --- | --- |
| Source availability of a value | None. Only the interval above, `DERIVED` from Market Observations |
| System receipt | Evidence ledger: witnessed receipt time and sequence |
| Prediction or Decision commitment | Evidence ledger: commitment time and sequence by the Evidence clock |

### The precedence rule (tightens PD-001's I-2 and §III.5)

A Prediction or Decision is Contemporaneous Forward Record only if, for
every value needed to resolve or score it, commitment time precedes the
lower bound of that value's availability interval. Where the interval has
no lower bound, prospective classification is refused: Historical
Reconstruction with the reason recorded; nothing later reclassifies it.
The narrow reading (availability from the declared source) is taken; N-4
stays open.

### Information present in model training data (PD-002.6)

No third class is created. Forward record is structurally immune: committed
before its resolving values exist. Historical Reconstruction authored by an
agent is authored with knowledge of the period (fin123-core §9) and is
already outside the forward record. A model reaching outside the closure
at decision time is caught by reproduction for Strategies and by the
precedence rule for Predictions.

**Disposition PD-002.6.** The declared training cutoff of the provider
model is carried into D-14 as a **provenance requirement** of Agent
Design Version registration: a fact about where the method came from,
recorded so that an Evaluation Standard can describe reconstruction
honestly. It is **not evidence of freedom from leakage**, and no rule in
this record or later may treat a period after the cutoff as leak-free on
that ground alone.

---

## PD-002.3. Constitution genesis (N-1), bootstrap issue

Every applied Transition pins a `ConstitutionVersion`, including the
first. The draft has no Transition that admits `ConstitutionVersion 1` and
none that grants the first Observation, Runner and Execution
Authorizations. Standing proposed: **FOUNDATIONAL BOOTSTRAP ISSUE; must
close before any claim of replay or recovery conformance (plan step 8
exit).** Candidate for later decision: Apply sequence 0 is a Constitutional
Transition proposed and decided by the Principal, with the Checker
requirement waived by an exception in `ConstitutionVersion 1` applicable
only to sequence 0; sequences 1 to 3 are the first Observation, Runner and
Execution Authorizations. Not decided here.

---

## PD-002.4. The Strategy Runner (U-9, Principal direction of 2026-10-18)

### Role

| Element | Disposition |
| --- | --- |
| Role | **Strategy Runner function.** A constitutional role distinct in authority from the Execution function and the Observation function. Not an Agent Design Version. The three functions may share a process or service; each commit is attributed to exactly one Authorization, and a shared process holds each Authorization separately |
| Authorization class | **Runner Authorization**, granted only by the Principal; names the Strategy Versions it runs by standing rule (every Strategy Version admitted in the Applied History, or a named subset); expiry |
| Runs | Admitted, immutable Strategy Versions, on their declared triggers, against closed inputs, producing one Decision per decision event |
| Commits | Strategy Decisions, including `DECLINED` and `FAILED`, to the Evidence ledger. Nothing else |
| May not | Propose or admit Transitions; change a Strategy Version or its declaration; modify an Evaluation Standard; authorize or consume capital; commit Market Observations, Predictions, Outcomes, Research Records, reproduction records or Evaluations; commit any Paper Book fact |
| Independence | Runs by the Strategy Version's standing in the Applied History, not by the proposing agent's Authorization. Retirement of the proposing Agent Design Version and revocation of its Authorization do not stop the Runner. A Strategy Version stops being run only by a retirement or suspension Transition applied to it |
| Reproduction | The Runner does not certify reproduction. Reproduction records remain Checker-only, and reproduction is the check on the Runner itself |
| Stop | A Runner that cannot reach the Applied History, the Evidence ledger or the Paper Book refuses to run; it does not run on a cache |

### The Execution function, restated

Consumes committed Decisions, current allocation and limits, and Paper
Book state. Alone commits paper execution facts (orders, replaces,
cancels, fills, refusals). May not run a Strategy Version, commit a
Decision, or commit any other Evidence kind. Its Authorization is the
existing Execution Authorization, unchanged in rights.

### Commit restrictions after PD-002 (all Evidence and Paper Book kinds)

| Record kind | May be committed only under |
| --- | --- |
| Market Observation | Observation Authorization |
| Strategy Decision | Runner Authorization |
| Reproduction record (Evaluation kind) | Checker Authorization |
| Prediction, Research Record, other Evaluations | Research, Checker or Principal Authorization, as drafted |
| Outcome | As drafted (any authorized), with F-2's reproducibility and expected-set rules; the committer question is U-10 |
| Order, Replace, Cancel, Fill, execution refusal | Execution Authorization |

Research Agents therefore never commit Strategy Decisions or Market
Observations and never touch the Paper Book. The counterfactual in which
an agent's process commits a Decision from an early read is impossible by
construction; the remaining threat is a Runner that reads outside its
closure, caught by reproduction.

### Constitutional Delta of PD-002.4

```text
ΔO: NONE. A function role is not a governed object.
ΔS: Strategy Decision commit is attributed to the Runner Authorization;
    a Runner Authorization names the Strategy Versions it runs by
    standing rule; "runs" in every worked example is now attributed.
ΔA: +1 Authorization class: Runner Authorization (Principal only).
    +1 function role: Strategy Runner.
    Strategy Decision commit restricted to the Runner.
    Execution function: rights unchanged; it consumes Decisions.
    No Research, Checker or Observation Authorization gains or loses a
    right it held before PD-002.
```

---

## PD-002.5. Source Declarations remain Authorization content

Disposition as directed: no new governed object at this stage. `SourceId`
and `SourceRevision` rules as in PD-002.2. `ΔO` for PD-002 stays at +1
(the Strategy Decision kind).

## PD-002.6. Training cutoff into D-14

Disposition as directed; text in PD-002.2 above. `ΔS`: Agent Design
Version registration gains a provenance field. `ΔO`, `ΔA`: none.

---

## Final adversarial checks (revision 4)

### F-1. Dealer-gamma authorization chronology — DEFECT FOUND, REPAIRED

Revision 2 placed `AU-02b` (the Observation Authorization that adds
`SRC-S`) at Apply 47 and `HY-88`'s registration at Apply 42, while the
Check of `HY-88` cited `AU-02b` and `PR-501` consumed `SRC-S` values
committed before 2026-10-18. An Authorization cannot be cited five
Transitions before it exists, and no `VALUE` of `SRC-S` could precede it.
The sequence numbers also collided across the two examples, which share
one Evidence ledger.

Repair: one unified timeline (below). `AU-02b` applies at `N=40` on
2026-10-01; `SRC-S` is observed from that date; `HY-88` registers at
`N=42` on 2026-10-18 and its Check cites `AU-02b` as projected at base 41.
Rule made explicit in PD-002.2: the Checker verifies sources against the
Observation Authorizations active **at the registration's base state**,
never against a later one.

### F-2. Reproducible resolution of a multi-observation target — DEFECT FOUND, REPAIRED

Constitution §III.5 binds an Outcome to "exactly one Market Observation of
the declared print". `PR-501`'s target, realized five-session variance
against implied, needs six closes and one implied print. Either the
Outcome binds one Observation and is unreproducible, or it binds several
and contradicts the text.

Repair, proposed for §III.5:

| Element | Rule |
| --- | --- |
| Resolution rule | Declared in the Prediction at commitment: a deterministic function from a declared **resolution set** of (`SourceId`, period, print) members to the target value, with its content hash. Fixed at commitment (fin123-core §5) |
| Outcome binding | Exactly one bound observation set: for each member, the Evidence sequence of the `VALUE` Observation of that member's declared print. The Outcome records the set, the rule hash, the computed value, and the comparison to the target and tolerance |
| Outcome availability time | The witnessed receipt time of the last member bound |
| Reproducibility | Any reader re-applies the rule to the bound set and must obtain the computed value |
| Missing member | If a member's declared print has no `VALUE` Observation by the Standard's resolution deadline, the Outcome is committed as `UNRESOLVABLE` with the missing member named. It is preserved and the Standard says how it counts. A later `VALUE` does not alter it |
| Restatement | A later Observation of a member is a new Observation; the Outcome stands on the prints the rule named (PD-001) |
| Expected Outcomes | Derivable: a Prediction whose resolution set is fully present on the ledger and has no Outcome is a visible omission, like a missing Decision |

Example 2 step 4 below resolves `PR-501` this way. "Exactly one Market
Observation" becomes "exactly one bound observation set"; a
single-observation target is the set of size one.

Committer: Outcome resolution is deterministic and reproducible, so a
wrong Outcome is detectable by any reader and a missing one is visible.
Whether Outcome commit should be restricted to a function (the Runner on
a "resolution set complete" trigger is the natural candidate, but it
expands the Runner's permitted actions beyond the Principal's list) is
**U-10**, not decided here.

### F-3. Stable decision-event identity and idempotent commit — REPAIRED

Rules in PD-002.1 §Decision events. Concurrent Runners, retries after
infrastructure failure, and `FAILED` finality are each covered; the
Evidence commit boundary enforces one Decision per `DecisionEventId` and
preserves refusals.

### F-4. Authority and claim of the witness reads — VERIFIED, CLAIM NARROWED

Authority. The Evidence commit boundary is the authority for Evidence; it
is not a grantee and holds no Authorization. Reading the Applied History
and the Paper Book is a reader act, which the Constitution grants to any
reader and conditions only by I-13: a reader that cannot reach the
authority refuses. The witness read is therefore covered by existing
doctrine and creates no authority. The one consequence to state: when
either head is unreachable, Decision commits refuse, and the system does
not decide on a cache. The revision list adds this duty to §III.5 and
I-13 explicitly so it is not inferred.

Claim. The witness does not claim an atomic snapshot across three ledgers,
which it cannot establish. It claims exactly this, and it is sound because
both ledgers are append-only and their heads are monotone:

```text
At Evidence-clock instant t_N (before this commit's sequence was
assigned) the Applied History head was N_w; at instant t_F the Paper Book
head was F_w. The closure's claimed N and F were read before this commit,
hence at instants when the heads were ≤ N_w and ≤ F_w. Therefore N ≤ N_w
and F ≤ F_w, or the commit is refused.
```

It makes no claim that `N_w` and `F_w` were simultaneous with each other
or with `E`. Staleness is `N_w − N` and `F_w − F`, recorded. U-2 is
narrowed to simultaneity, which the design does not need.

---

## Two complete examples on one unified timeline

One Evidence ledger (`E`), one Applied History (`N`), one Paper Book
(`F`). `CV-1` and `ES-1` pinned throughout. Function Authorizations
assumed applied early, subject to PD-002.3: Observation `AU-02`
(`SRC-E`, `SRC-X`), Runner `AU-04`, Execution `AU-03`. `AU-02b`
(successor, adds `SRC-S`) at `N=40`, 2026-10-01. Checkers: `CK-A2` under
`AU-20`; `CK-H1` (human) under `AU-21`. Research Agent `AD-3.3` under
`AU-27` (research; capital up to 10; `0/0/0`).

### Timeline

| Date | `N` | `E` | `F` | Event |
| --- | --- | --- | --- | --- |
| 10-01 | 40 | | | `AU-02b` applied: `SRC-S r1` (first print; no structural bound; slots 17:55 absence, 18:30, 19:30), `SRC-X r1` (structural bound session end; 16:30) |
| 10-01 to 10-17 | | 2 100 to 2 300 | | Daily `SRC-E`, `SRC-X`, `SRC-S` Observations |
| 10-18 | 42 | | | `TR-301` registers `HY-88` (base 41) |
| 10-18 16:05 | | 2 311 | | `PR-501` |
| 10-19 16:31 | | 2 400 | | `SRC-E`, `SRC-X` closes for 10-19 |
| 10-23 16:31 | | 2 482 | | Closes for 10-23 (last member of `PR-501`'s set) |
| 10-23 17:10 | | 2 485 | | `OC-501` |
| 10-26 | 48 | | | `TR-350` registers `SV-8.1`, allocation 10 (base 47) |
| 10-27 | 51 | | | `TR-360` registers `SV-14.1`, allocation 5 (base 50) |
| 10-27 17:55 / 18:10 / 18:31 | | 2 493 / 2 495 / 2 496 | | `ABSENT` S; `PR-502`; `VALUE` S |
| 10-28 16:00 | | 2 497 | | `PR-503` |
| 10-28 18:31 / 18:36 / 18:50 | | 2 500 / 2 501 / 2 503 | 931 | `VALUE` S; `SD-9001`; `RP-9001`; set `TR-360:51:2501` |
| 10-30 16:31 / 17:02 / 17:20 | | 2 506 / 2 507 / 2 509 | 940 to 999 | Closes; `SD-7001`; `RP-7001`; set `TR-350:48:2507` |
| 10-30 17:55 / 18:30 / 19:31 / 19:35 | | 2 508 / 2 510 / 2 512 / 2 513 | | `ABSENT` S; `RETRIEVAL_FAILED` S; `VALUE` S; `SD-9002 DECLINED` |
| 11-02 | | 2 520 | 1 003, 1 010 | S restates 10-27; partial fill of `OR-...:2507.7`; `REPLACE` `.7r` |
| 11-03 | | 2 524 | | Backfill of 10-28 closes (witnessed 11-03) |
| 11-06 17:02 | | 2 540 | 1 020 onward | `SD-7002`; `CANCEL` open orders of `:2507`; set `TR-350:48:2540` |
| 11-10 | 52 | | | Unrelated Theme retirement |
| 11-13 17:02 | | 2 560 | | `SD-7003 FAILED` |
| 11-20 17:00 | | | | Runner dies before commit; no record |
| 11-23 | | 2 580 | 1 100 | `EV-120` at `N=52` |
| 11-24 | 53 | | | `TR-371` raises `SV-8.1` to 15 (base 52); set `TR-350:53:2540` |
| 11-25 | 54 | | | `TR-380` registers `SV-14.3` (`NON-REPRODUCIBLE`), allocation 0 (base 53) |
| 11-30 | | 2 600 | | `EV-131` at `N=54` |

### Example 1. Price/volume momentum Strategy with no Hypothesis

| Step | Act | Authoritative record written | Inputs or evidence used | Resulting state |
| --- | --- | --- | --- | --- |
| 1 | `AD-3.3` proposes `TR-350`: register `SV-8.1`, lineage `SL-8`, proposition `EP-27`: mechanism `none claimed`; target: 1-month return of top-decile 12-1 momentum names minus bottom decile, volume-filtered, positive; market US large caps; horizon 1 month; payoff long-short spread. Declared inputs: `SRC-E` Observations; projection (own allocation, limits); own fills. Trigger: schedule, Fridays 17:00 ET. Hash `h81`. Allocation 10. Base 47 | Transition ledger | | `PROPOSED` |
| 2 | `CK-A2`: two test executions with closure only yield one hash, `REPRODUCIBLE`; `SRC-E` under `AU-02` active at base 47; declared inputs are ledger kinds; `ES-1` scores the target; composition within limits; `NEW` | Check event pinned `CV-1`/`ES-1` | Artifact; projection at 47 | `CHECKED PASS` |
| 3 | Principal admits; Apply | **`N=48`**: `SV-8.1` member, allocation 10, consumption 10 under `AU-27` | | Runner `AU-04` now runs it by standing |
| 4 | Observation function commits closes each session (`VALUE`, `SRC-E r1`) | Evidence ledger | | |
| 5 | 10-30 17:00 slot: Runner computes `DecisionEventId` `ev(SV-8.1, slot 2026-10-30)`, runs. Closure: `E` ≤ 2 506, `N`=48, `F` ≤ 930. Witness: `N_w`=51, `F_w`=939 (staleness 3 and 9: the projection at 48 is what the artifact declared it reads). Output: 60 weights, hash `d1` | **`SD-7001` at `E=2 507`**, 17:02, under `AU-04` | Closure | Forward: scoring closes from 11-02 have structural bounds after commitment |
| 6 | `CK-A2` re-executes with closure only; obtains `d1` | **`RP-7001` at `E=2 509`** under `AU-20`, match | | Derived `REPRODUCED` |
| 7 | Execution function reads head 51, `SD-7001`, Paper Book head 939; derives set `TR-350:51:2507`, orders `.1` to `.60`, each checked against limits at 51 | Paper Book `F=940` to 999 | | Note the key uses the head at order time, 51, not the closure's 48 |
| 8 | 11-02: `.7` fills 50 % (`F=1 003`); `REPLACE` `.7r` for the remainder derived from fills at the head (`F=1 010`). A late fill of `.7` arriving after `.7r` would overfill, so the function refuses in that case and records it | Paper Book | | Positions `DERIVED` |
| 9 | 11-06 slot: `SD-7002` (`E=2 540`; closure ≤ 2 539, 51, ≤ 1 015). `CANCEL` open orders of set `:2507`; set `TR-350:51:2540` | Evidence; Paper Book | | |
| 10 | 11-13 slot: artifact raises on a malformed Observation | **`SD-7003 FAILED`** (`E=2 560`), closure recorded, under `AU-04` | | Final for its event; counts against |
| 11 | 11-20 slot: Runner dies before commit | Nothing | | Event `ev(SV-8.1, slot 2026-11-20)` has no Decision; derivable as missing; a retry that day would be lawful |
| 12 | 11-23: `EV-120` at `N=52`, closure (≤ 2 580, 52, ≤ 1 100), `ES-1`: expected events 4, committed 3 (`SD-7001 REPRODUCED`, `SD-7002 UNVERIFIED`, `SD-7003 FAILED`), 1 missing; decision-implied at the Standard's notional; executed from fills; shortfall | `DERIVED` | | |
| 13 | 11-24: `TR-371` raises allocation to 15 citing `EV-120` (base 52); Apply `N=53`. Execution re-executes standing `SD-7002` at 53: set `TR-350:53:2540` | Applied History; Paper Book | `EV-120` under the Standard in force at base 52 | `SD-7002` unchanged |
| 14 | The 11-03 backfill of 10-28 closes (`E=2 524`) | Evidence | | Marks the executed record; above every closure before it; no earlier Decision can be re-run against it under its own identity |

Challenges:

- **Duplicate authority.** Capital (Applied History), weights (Evidence by
  the Runner), orders and fills (Paper Book by the Execution function),
  positions (derived). The Runner and Execution function hold separate
  Authorizations even if one process. The closure binds values by
  sequence and hash. Reproduction standing is derived from `RP-` records.
- **Information leakage.** The Runner is the only committer; a Runner that
  read outside the closure diverges at reproduction. Backfill sequences
  exceed earlier closures.
- **Missing input provenance.** Three marks plus witness marks on every
  Decision; declared kinds in the content hash.
- **Selectively omitted failures.** `SD-7003` is a record; the 11-20 gap
  is derivable from the schedule; neither can be removed; `UNVERIFIED`
  never counts in the grounding series.
- **Cross-ledger currentness.** Step 5 records staleness 3 and 9 without
  claiming simultaneity; step 7 keys on the head at order time. A stale
  `N` changed nothing because output is in weights.
- **Retrospective rewriting, recovery.** As in revision 2: new sequences
  only; swapped artifact fails against `h81`; restated close is a new
  Observation; death after `E=2 507` and before orders reconstructs the
  set from `SD-7001` and the absence of key `TR-350:51:2507`; death before
  commit leaves a derivable gap and a lawful retry.

### Example 2. Dealer-gamma Theme to Hypothesis, Prediction, Strategy, paper trades

| Step | Act | Authoritative record written | Inputs or evidence used | Resulting state |
| --- | --- | --- | --- | --- |
| 1 | 10-18: `AD-3.3` proposes `TR-301` registering `HY-88` under `TH-7` (base 41). Resolution rule declared: realized variance = function of six `SRC-X` closes (10-16 to 10-23 window members), implied = `SRC-X` implied print at 10-16; target: realized exceeds implied by Y; tolerance; falsifier. Resolution set: seven (`SourceId`, period, print) members. `CK-H1`: testable; `SRC-S`, `SRC-X` under `AU-02b` **active at base 41** (applied `N=40`); `SRC-S` has an absence-witness slot | **`N=42`** | | `HY-88` admitted, record empty |
| 2 | 10-18 16:05: `PR-501` (`E=2 311`): window 10-19 to 10-23. Condition inputs (S below X for 10-15, 10-16, 10-17) are `VALUE` Observations with `E` < 2 311, which exist because `AU-02b` has observed `SRC-S` since 10-01 | Evidence | Resolving members: closes 10-19 to 10-23, structural bounds after commitment | Forward |
| 3 | 10-23 17:10: Outcome `OC-501` (`E=2 485`): bound set = the seven member Observations by sequence (last member `E=2 482`); rule hash; computed value; realized exceeded implied by 1.4Y; outcome availability 10-23 16:31 | Evidence | Bound set | Any reader recomputes the same value from the same set |
| 4 | 10-27: `TR-360` registers `SV-14.1` (base 50), proposition `EP-31`: mechanism "dealer hedging flow amplifies realized variance"; target realized minus implied variance over 5 sessions, positive; market index variance; horizon 5 sessions; payoff long variance. Declared inputs: `SRC-S`, `SRC-X` Observations; committed Predictions of lineage `HY-88`; projection; own fills. Rule: long variance for window W when a forward-class `HY-88` Prediction for W exists in the closure and S's latest `VALUE` is below X; `DECLINED` if S's latest slot is not `VALUE`. Frozen classifier `m14` in the artifact. Trigger: new `VALUE` of `SRC-S`. Allocation 5 | **`N=51`** after `CK-H1`: `REPRODUCIBLE` including `m14`; sources under `AU-02b` at base 50; Predictions a declared input conferring nothing; `NEW`; within limits | | |
| 5 | 10-27 18:10: `PR-502` (`E=2 495`): "S's print for 10-27 will be below X" | Evidence | Interval for S 10-27: `ABSENT` 17:55 (`E=2 493`), first `VALUE` 18:31 (`E=2 496`) | **Historical Reconstruction, reason "commitment within (17:55, 18:31]"** |
| 6 | 10-28 16:00: `PR-503` (`E=2 497`) for window 10-29 to 11-04 | Evidence | | Forward |
| 7 | 10-28 18:31: `VALUE` S (`E=2 500`) fires the trigger; event `ev(SV-14.1, E=2 500)`. Runner runs at 18:35. Closure: ≤ 2 500 (includes `PR-503`, S), 51, ≤ 930. Witness 51, 930. Output: long variance, hash `g1` | **`SD-9001` at `E=2 501`**, 18:36, under `AU-04` | Closure | Forward: scoring `SRC-X` values for 10-29 to 11-04 have structural bounds after commitment |
| 8 | Counterfactual: a misconfigured Runner reads S's site at 18:05 and commits for event `ev(SV-14.1, E=2 500)`? It cannot: the event does not exist until `E=2 500` is committed. Second counterfactual: at 18:35 the Runner's artifact environment leaks a vendor feed and outputs long variance with S's 10-28 value above X on the ledger. `CK-H1` re-executes against the closure: `DECLINED`, hash differs | `RP-9001` divergence | | `UNREPRODUCED`; shown, not counted; preserved. A Research Agent cannot commit a Decision at all (PD-002.4) |
| 9 | Execution: set `TR-360:51:2501`, order `.1` (`F=931`); partial fill; `REPLACE` `.1r` | Paper Book | | |
| 10 | 10-30: `ABSENT` 17:55 (`E=2 508`); `RETRIEVAL_FAILED` 18:30 (`E=2 510`); `VALUE` 19:31 (`E=2 512`) fires event `ev(SV-14.1, E=2 512)`; S above X; `SD-9002 DECLINED` (`E=2 513`) | Evidence | | Interval for S 10-30: (17:55, 19:31]; the failed retrieval bounds nothing; a Prediction on S's 10-30 print committed at 18:40 is refused forward |
| 11 | Two Runner processes both see event `ev(SV-14.1, E=2 512)`; both compute `DECLINED`; the second commit is refused by `DecisionEventId` and the refusal preserved | Evidence commit boundary refusal | | One Decision per event |
| 12 | 11-02: S restates 10-27 (`E=2 520`) | Evidence | | `OC-501`, `PR-502`'s class, `SD-9001`'s closure unchanged |
| 13 | 11-25: `TR-380` registers `SV-14.3`, same proposition, rule calls a hosted external model. `CK-H1`: test executions diverge and the call leaves the closure: `NON-REPRODUCIBLE`. Admitted at zero allocation | **`N=54`** | | Runner runs it; its Decisions are preserved and scored; none can be `REPRODUCED`; an Allocation Transition for it is `STOPPED` under `ES-1` (U-1) |
| 14 | `AD-3.3` is retired and `AU-27` revoked (as T-C). `SV-8.1`, `SV-14.1`, `SV-14.3` keep running under `AU-04` by standing | Applied History | | Runner independence (PD-002.4) |
| 15 | 11-30: `EV-131` at `N=54`, closure recorded: `HY-88` calibration from `PR-501`/`OC-501` and later pairs, `PR-502` under Historical only; `SV-14.1` records from `SD-900x`, `SRC-X` marks and fills, the step 8 Decision shown `UNREPRODUCED`; `SV-14.3` all `UNVERIFIED`, no grounding series | `DERIVED` | | Separate competitions (I-1) |

Challenges:

- **Duplicate authority.** `HY-88` standing and `SV-14.1` allocation are
  different Applied History facts fed by different Evidence; `PR-503` as
  an input confers nothing. S's values have one owner and one writer. The
  Outcome's bound set references Observations; it holds no second copy.
- **Information leakage.** `PR-502` refused forward by the interval;
  step 8's leaking Runner caught by reproduction; the training-cutoff
  field (PD-002.6) describes `AD-3.3`'s provenance and proves nothing.
- **Missing input provenance.** Every Decision and every Outcome names
  its inputs by sequence; a missing member yields `UNRESOLVABLE`, never a
  substituted value.
- **Selectively omitted failures.** `SD-9002 DECLINED` is a record; an
  Outcome omitted for a failed Prediction is derivable as missing once
  its set is complete; `UNRESOLVABLE` is committed, not skipped.
- **Cross-ledger currentness.** Witness marks on `SD-9001`; the order
  set keys on the head at order time.
- **Retrospective rewriting, recovery.** Restatement alters nothing; a new
  absence slot interprets only later records; the Observation function
  restarting at 18:50 witnesses 18:51 and widens the interval; a Runner
  dying before commit leaves a lawful retry; two Runners cannot both
  commit (step 11). Death between Decide and Apply of `TR-360` is D-17.

### Two-case consistency

One evidence model serves both cases: Hypotheses through Predictions and
Outcomes over bound observation sets; Strategy Versions through Decisions
over closures, committed by the Runner and checked by reproduction; the
Paper Book feeding the executed record only; the Evidence clock and the
availability interval governing class in both; forward-research
Predictions entering a Strategy only as closure inputs.

---

## Adversarial findings (revisions 2 to 4)

| Ref | Mode | Finding | Disposition |
| --- | --- | --- | --- |
| A-1 | Duplicate authority | Reproduction standing stored on the Decision | REPAIRED (r2): derived from reproduction records |
| A-2 | Duplicate authority | Closure carrying values | REPAIRED (r2): bindings and hash |
| A-3 | Leakage | Reading the data store or an API past a sequence check | REPAIRED (r2): declared kinds; reproduction with closure only |
| A-4 | Leakage | Prediction as Strategy input | NOT A LEAK |
| A-5 | Leakage | Model trained on the scoring period | COVERED; PD-002.6 |
| A-6 | Provenance | No marks for allocation or positions read | REPAIRED (r2): `N`, `F` |
| A-7 | Provenance | Input kinds undeclared | REPAIRED (r2) |
| A-8 | Omitted failures | Skipped bad runs | REPAIRED (r2): triggers, `FAILED`, missing events |
| A-9 | Omitted failures | Not seeking reproduction | REPAIRED in part; duty is D-10 |
| A-10 | Currentness | Evaluations without closure | REPAIRED (r2) |
| A-11 | Currentness | `N`, `F` asserted | REPAIRED (r3) as far as sound: witness marks; residual U-2 |
| A-12 | Currentness | Late fill after `REPLACE` | REPAIRED (r2) |
| A-13 | Duplicate execution | Re-execution after allocation change | REPAIRED (r2) |
| A-14 | Rewriting | Outage tightening a lower bound | REPAIRED (r2): `RETRIEVAL_FAILED` |
| V-1 | Currentness | Decision-time currentness unproven | REPAIRED (r3), narrowed (r4, F-4) |
| V-2 | Authority | Runner's Authorization missing | REPAIRED (r4): PD-002.4 |
| F-1 | Chronology | `AU-02b` cited before it existed; sequence collisions | REPAIRED (r4): unified timeline; base-state rule |
| F-2 | Reproducibility | One-Observation Outcome cannot resolve a multi-observation target | REPAIRED (r4): bound observation set, resolution rule, `UNRESOLVABLE` |
| F-3 | Idempotency | No event identity across Runners and retries | REPAIRED (r4): `DecisionEventId`, one per event, `FAILED` final, infra retry lawful |
| F-4 | Authority, claim | Witness reads and atomic snapshot | VERIFIED; claim narrowed to monotone bounds; duty to be made explicit in §III.5 and I-13 |

### Contradictions with PD-001 or revision 2 of the Constitution

| Ref | Finding | Nature |
| --- | --- | --- |
| C-1 | §III.10 and I-12: one Allocation Transition, at most one order; key `TransitionId:StateVersion` | Contradiction with revision 2 text; §III.10, I-12, T-D, challenge 9 to be revised |
| C-2 | §III.5 and PD-001: "earliest retrieval is evidence of availability" | Tightening forced by PD-001's own refusal rule |
| C-3 | Part V: "Evidence commit: any authorized agent or human" | Contradiction with PD-002.2 and PD-002.4; split four ways |
| C-4 | §III.3 Executability | Consistent, made exact; frozen model admissible |
| C-5 | §III.5 Outcome: "exactly one Market Observation" | Contradiction with any multi-observation target; F-2 |
| C-6 | §III.5 three-times table, outcome availability "when the resolving print was taken" | Becomes the last member's witnessed receipt; consistent in spirit |

No contradiction with the three admitted PD-001 clarifications.

### Remaining defects and undecided questions

| Ref | Subject | Standing |
| --- | --- | --- |
| U-1 | Any standing other than `REPRODUCED` grounding allocation for a `NON-REPRODUCIBLE` version | UNDECIDED; `STOPPED` path exists; no future Standard proposed |
| U-2 | Simultaneity across the three ledger clocks | OPEN by design, narrowed; plan step 9 |
| U-3 | Which Checker Authorizations may commit reproduction records; duty to attempt | DEPENDS ON D-10 |
| U-4 | Knowable through undeclared channels (N-4) | OPEN; narrow reading taken |
| U-5 | Execution against an admitted-but-unapplied Allocation (D-17) | OPEN; direction in PD-001 |
| U-6 | `ES-1` content | UNDRAFTED; constitutional; after admission |
| U-7 | Genesis (N-1) | BOOTSTRAP ISSUE; PD-002.3 |
| U-8 | Limits read at a moving head during an order set | OPEN; plan step 7 |
| U-9 | Who runs a Strategy Version | **DECIDED IN DIRECTION** by the Principal; PD-002.4 |
| U-10 | Who may commit Outcomes, now that resolution is a deterministic function over a bound set | OPEN. Candidates: as drafted (any authorized, with omissions visible and values recomputable); or a function on a "set complete" trigger, which would widen the Runner beyond the Principal's list. Recommendation: decide with D-10, since it is the same question as who reproduces |

---

## OSA impact analysis

### New or changed governed facts

| Fact | Authority | Commit boundary | Other carriers and class |
| --- | --- | --- | --- |
| Strategy Decision, `DecisionEventId`, witness marks | Evidence ledger | Evidence commit, Runner Authorization only | Runner memory before commit `EPHEMERAL`; stored copy `CACHE` |
| Reproduction record | Evidence ledger | Evidence commit, Checker Authorization only | Derived standing `DERIVED` |
| Outcome over a bound set, `UNRESOLVABLE` | Evidence ledger | Evidence commit (committer U-10) | Recomputed value `DERIVED` |
| Source Declaration (`SourceId`, `SourceRevision`), observation plan | The Observation Authorization carrying it | Authorization Transition | Scheduler state `EPHEMERAL` |
| `VALUE`, `ABSENT`, `RETRIEVAL_FAILED`, claimed and witnessed times | Evidence ledger | Evidence commit, Observation function only | Claimed time is `RECEIPT` content |
| Availability interval | None; `DERIVED` | None | |
| Order type, set key, `REPLACE` parent, `CANCEL`, execution refusal | Paper Book | Order commit, Execution Authorization only | |
| Decision-implied and executed records, shortfall, expected-versus-committed events and Outcomes | None; `DERIVED` | None | |
| Declared input kinds, trigger, resolution rule, reproducibility class | Transition ledger (proposal content; class as Check finding) | Registration Transition | |
| Training cutoff (provenance) | Transition ledger, Agent Design registration content | Registration Transition | Proves nothing about leakage |
| Runner Authorization | Principal | Authorization Transition | |

### Authority Normal Form check

| Invariant | Finding |
| --- | --- |
| Singular decision authority | One authority per fact. Three functions, three Authorizations, three commit scopes; a shared process changes nothing |
| Classified representation closure | Every alternative carrier named and classed; no new class |
| Exclusive governed commit boundary | Unchanged boundaries; callers restricted per kind |
| Temporal and binding closure | Closures, bound sets, witness marks and keys all by sequence; classes from recorded times; witness claims only monotone bounds |
| Owner-resolved consumption | Capital consumption unchanged; Decisions and Outcomes consume nothing |
| Legacy isolation | Not implicated |
| Constitutional failure closure | New stops and refusals, each preserved: input above `E`; closure above a witnessed head; second Decision for an event; Market Observation, Decision, reproduction record or execution fact committed outside its Authorization; Outcome with a missing member (`UNRESOLVABLE`); Allocation grounded on a non-reproducible record (`STOPPED`); Runner or Evidence boundary unable to reach a ledger (refuse) |

### Separation and forward-evidentiary reconciliation

Observe, run, execute, reproduce, propose, admit: six acts, no two under
one Authorization, the Principal holding only admission. fin123-core §5
and §6 ground the Decision and `DECLINED`; §9 keeps the two classes apart;
F-2 keeps "fixed at commitment" for the resolution rule.

---

## Precise Constitutional Delta of PD-002 (all dispositions, revision 4)

```text
ΔO: +1 Evidence kind: Strategy Decision.
    Nothing else. Reproduction records are Evaluation-kind Evidence.
    Source Declaration is Authorization content (PD-002.5). Function
    roles are not objects. Order type and set key are Order content.
    Outcome's bound set replaces its single binding; same kind.

ΔS: Strategy: "prediction target" = scored observable and sign;
    registration declares input kinds, SourceIds, trigger; Checker finds
    reproducibility class; forward record = forward-class Decision series
    with derived reproduction standing; frozen model admissible.
    Evidence: Strategy Decision (DecisionEventId, closure E/N/F, witness
    marks, outputs incl. DECLINED and FAILED, one per event, FAILED
    final); Market Observation gains result, claimed time, witnessed
    receipt, SourceId, SourceRevision; Prediction gains a resolution
    rule and resolution set; Outcome binds a bound observation set and
    may be UNRESOLVABLE; Evaluation gains a closure; availability =
    derived interval; I-2 precedence to the lower bound; reproduction
    standing derived.
    Paper Book: set key TransitionId:StateVersion:DecisionSeq; order
    types NEW, REPLACE, CANCEL; remainder from fills; limit refusal.
    Authorization: Observation and Runner Authorization content; Source
    Declaration identity rule; base-state rule for source checks.
    Agent Design: training cutoff as provenance (PD-002.6).
    Evidence commit boundary: witness-read duty and refusal when a head
    is unreachable, stated explicitly.

ΔA: +2 Authorization classes: Observation Authorization, Runner
    Authorization (Principal only).
    +2 function roles: Observation function, Strategy Runner.
    Commit restrictions: Market Observation -> Observation function;
    Strategy Decision -> Runner; reproduction record -> Checker
    Authorization; execution facts -> Execution function (as drafted).
    Execution function: rights unchanged; duties added (cancel on
    supersession, REPLACE-only retries, limit refusal, re-execution at a
    new StateVersion).
    Runner independence: runs by Applied History standing; survives the
    proposing agent's retirement.
    No Research, Checker or Observation Authorization gains or loses a
    right it held before PD-002. No admission authority moves.
    Pending U-10: Outcome committer; no change declared.
```

---

## Constitutional sections requiring revision on admission

| Section | Change |
| --- | --- |
| Part II, Roles | Add Observation function, Strategy Runner, and name the Execution function; state that roles are distinct in authority, not necessarily in process |
| §III.2 Hypothesis | Resolution rule and resolution set declared at registration |
| §III.3 Strategy | Prediction target definition; declared inputs, trigger, reproducibility class; frozen model rule; forward record definition; rename PD-002 citation to PD-001.2 |
| §III.4 Agent Design | Training cutoff as provenance (D-14) |
| §III.5 Evidence | Strategy Decision row and rules; `DecisionEventId` and one-per-event; closure and witness marks; Market Observation result, times, `SourceId`/`SourceRevision`; Prediction resolution rule and set; Outcome bound set and `UNRESOLVABLE`; Evaluation closure; reproduction records; availability interval; precedence to lower bound; the commit boundary's witness-read duty; rename PD-003 citation to PD-001.3 |
| §III.7 Authorization | Observation Authorization; Runner Authorization; Source Declaration identity rule; base-state rule; Checker Authorization gains reproduction-record commit |
| §III.10 Paper Book | Order set key; order types; `REPLACE` remainder; `CANCEL` on supersession; re-execution at new `StateVersion`; limit refusal as a Paper Book fact; Execution function consumes Decisions |
| Part IV | I-2 to the lower bound; I-12 reworded for the Decision binding; I-13 names the witness read; new invariant or I-2 extension: a Decision's closure precedes its commitment and is the only thing that may affect its output; one Decision per event |
| Part V | Split Evidence commit into Market Observation (Observation function), Strategy Decision (Runner), reproduction record (Checker), other Evidence; Strategy Version registration Check gains sources active at base, scoring rule exists, reproducibility class found; Order row names the Execution function consuming Decisions |
| Part VI | T-A Check names `AU-02b` at base 41 and the absence witness; `OC-501` as a bound set; T-B gains a Decision, order set and key; T-D rewritten with the Decision and event identity; Examples 1 and 2 enter as T-F and T-G on the unified timeline |
| Part VII | Rows: Strategy Decision `AUTHORITATIVE`; reproduction record; claimed source time `RECEIPT` content; availability interval `DERIVED`; decision-implied and executed records `DERIVED`; expected events and Outcomes `DERIVED` |
| Part VIII governance diagram | Observation function, Runner and Execution function as the three non-agent writers; Checker as sole writer of reproduction records |
| Evaluation Standard `ES-1` | U-6 |
| Audits and plan | Close N-5, N-3, U-9 by reference; N-1 as bootstrap; U-1 to U-8, U-10 registered; challenge 9's exposure reworded; D-14 provenance direction; plan step 2 exit re-evaluated |

Out of scope and untouched: D-06 removal, D-10, D-11, D-12 mechanism, N-2,
N-4, N-6, D-01, D-09.

---

## Readiness for admission

**PD-002 is ready for admission as a design**, on these terms:

- Every disposition the Principal directed is recorded (PD-002.1 to
  PD-002.6), tested on both cases on one timeline, and has a declared
  delta.
- No contradiction with PD-001's admitted clarifications exists. The
  contradictions with revision 2 text (C-1, C-3, C-5) are the revisions
  this record exists to cause.

**Unresolved constitutional blockers**, stated explicitly. None blocks
admitting PD-002 itself; each blocks something named:

| Blocker | Blocks | Who decides |
| --- | --- | --- |
| U-10 Outcome committer | Full Part V commit table; the Hypothesis forward loop being operable without a per-instance human act | Principal, with D-10 |
| D-10 Checker independence (U-3, A-9) | Any `REPRODUCED` standing in practice; therefore any capital competition grounded on Decisions | Principal, plan step 5 |
| N-1 genesis (PD-002.3) | Any replay or recovery conformance claim; CPOC certification | Principal, plan step 4 or 8 |
| `ES-1` content (U-6) | Any Evaluation; any allocation citing one | Principal, Constitutional Transition after admission |
| U-1 non-reproducible grounding | Capital for `NON-REPRODUCIBLE` versions only; `STOPPED` path exists | Principal, if and when wanted |
| D-17 (U-5) | The Decide-to-Apply recovery witness | Principal, plan step 4 |

## What happens on admission

1. Revise the sections above under the admitted text and clarifications,
   reconciled against fin123-core forward evidentiary doctrine §5, §6, §9
   and Authority Normal Form.
2. Re-audit for duplicate ownership among Decision, allocation, position,
   Outcome bound set and reproduction standing; for leakage through
   closures and resolution sets; for omitted failures and Outcomes; for
   the cross-ledger residual U-2; and for the three-function separation
   under one process.
3. Record N-5, N-3 and U-9 closed, N-1 as bootstrap, U-1 to U-8 and U-10
   in the audit register.
4. Only then propose the next decision: D-10 with D-11 (plan step 5),
   which also carries U-3, U-10 and A-9.
