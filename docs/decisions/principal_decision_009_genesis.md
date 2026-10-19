# Principal Decision Record 009 — Genesis (N-1), Decide-to-Apply Continuation (D-17), and D-06

Status: **ADMITTED 2026-10-19 by the Principal (document-phase admission): revision 2, the enumerated choices below and no other.** Applied to the Constitution as revision 10 and re-audited in [osa_reaudit_pd009_20261019.md](../audits/osa_reaudit_pd009_20261019.md). Genesis is not executed and `ConstitutionVersion 1` is not certified. Admission text, as approved:

```text
ADMITTED 2026-10-19 by the Principal (document-phase admission): PD-009
revision 2, these choices only:
- the exact three-item sequence-zero bootstrap and its narrowly
  bounded one-time waiver;
- full Checker independence criteria, with provider diversity
  supplementary;
- a second Checker lineage for checks concerning the first;
- the shared 600-unit research pool and 100-unit per-lineage caps as
  initial prototype settings, with the stated accounting table;
- synthetic-provider and metered-tool funding demonstrations, with
  real-provider cap assumptions unresolved until separately accepted;
- the carried-forward recovery rules (D-17), evidence labels,
  fill-rule restrictions and infrastructure-reuse constraint;
- removal of D-06's continuity claim and its references, preserving
  predecessor records and lineage access: inherited performance credit
  is removed, historical visibility is not.
These approvals cover the enumerated choices, not any additional
decision absent from the report. Genesis is not executed;
ConstitutionVersion 1 is not certified.
Constitutional Delta admitted: ΔO none; ΔS the Part V genesis
paragraph, the D-17 continuation rule, resume versus admit for
attempts, removal of the continuity-claim sentence and its two
references; ΔA +1, one-time, the Check waiver for sequence 0's
enumerated content, never reusable.
Closed: N-1 (as content), D-17, D-06.
```

Prior content follows. Proposes
the content of the first Apply sequences, the sequence-zero bootstrap
and its one-time waiver, the initial actors and their Authorizations,
the D-17 continuation rule, the fill rule and method commitments for
the first Checks, and the resolution of D-06. Depends on Constitution
revision 9 (PD-001 to PD-008 applied). Admits nothing, certifies
nothing, authorizes no code; genesis executes only after
`ConstitutionVersion 1` is admitted following the independent
whole-design audit ([checklist](../audits/cv1_whole_design_audit_checklist_20261019.md)).
Revision 2 (2026-10-19): removes the second-human dependency; applies
the full admitted independence criteria; clarifies the research grant
and what a unit measures; separates demonstrated controls from provider
assumptions; presents D-06.

Date: 2026-10-19 (revision 1: same day)

Sources: Constitution revision 9 (§III.4, §III.6, §III.7, §III.8
Independence and Check record, Part V, Part IX principle 10, Part X §3);
PD-002.3; PD-006 §PD-006.3; PD-007 §PD-007.6; PD-008; the Principal's
directions of 2026-10-19.

Numbers below are **illustrative and provisional**; each is
Authorization or limit content set at genesis, never Constitution text.

## 1. The sequence-zero bootstrap and its one-time waiver

**Content of sequence 0**, exactly three things: (i) the text of
`ConstitutionVersion 1`; (ii) the registration of the initial
independent Checker, Agent Design Version `AD-CK-1.0`, method class
`CHECKER`, with its provider, model version and training cutoff
declared as provenance; (iii) one Checker Authorization `AU-CK-A` to
`AD-CK-1.0`, narrowly scoped (§3). The Principal proposes, decides and
applies this exact bootstrap under the waiver. Everything after
sequence 0 is checked by `AD-CK-1.0` or a Checker it checked into
existence.

**Check against the admitted rules.**

| Rule | Finding |
| --- | --- |
| §III.8 Independence (PD-007): separate authority, protected standards, immutable evidence | Satisfied for every sequence ≥ 1: the proposer is the Principal; `AD-CK-1.0` is not the Principal, acts under its own Authorization, and is in no proposer's lineage; it checks under `ConstitutionVersion 1` as pinned; it reads committed records only. No admitted decision requires a human Checker; PD-007 and Part II define a Checker as "human or an Agent Design Version of method class `CHECKER`" |
| Part V: Constitutional Transition mutates "Constitution, Evaluation Standards" | **Deviation.** Sequence 0 also records a membership (the registration) and an Authorization grant. Carrying them inside a Constitutional Transition is not in the class table; it requires an explicit clause (below), not a silent reading |
| Part V: every consequential Transition requires a Check | **Deviation.** No Checker exists before sequence 0. The one-time waiver is an authority exception and is declared as such (§8) |
| §III.4: a successor runs under no Authorization until the Principal grants one | Satisfied: `AU-CK-A` is granted by the Principal inside the bootstrap; nothing is inherited |
| I-14: a Transition needing an identity, meaning or authority the Constitution does not supply is `STOPPED` | Satisfied once the clause exists; without it sequence 0 would itself be `STOPPED` |

**The exact clause**, proposed as the last paragraph of Part V:

> **Genesis.** Apply sequence 0 is a Constitutional Transition proposed,
> decided and applied by the Principal whose content is exactly: the
> text of `ConstitutionVersion 1`; the registration of one Agent Design
> Version of method class `CHECKER`; and one Checker Authorization to
> it. For sequence 0 alone, and for that enumerated content alone, the
> Check requirement is waived. The waiver applies to no other sequence,
> class, content, version, replay, re-genesis or migration; a
> Transition at any other sequence that invokes it is `STOPPED`. The
> registration and the grant carried by sequence 0 are ordinary
> membership and Authorization facts thereafter, amended or revoked only
> by checked Transitions.

Why it is not a reusable bypass: one sequence number, one class, three
enumerated items; it creates the Checker so that nothing after it is
unchecked; the clause is itself Constitution text changeable only by a
checked Constitutional Transition; and the Checker it creates can be
revoked only by a checked Transition, which `AD-CK-1.0` cannot check for
itself and a second Checker (sequence 13 below) can.

**Delta of the clause**: `ΔS` +1 (the Part V genesis paragraph); `ΔA`
+1, one-time: the Check requirement waived for sequence 0's enumerated
content, and the Principal's decision of one registration and one grant
without independent Check, never again.

## 2. The initialization sequence, ordered

| Apply | Transition | Proposer | Checker | Decider | Content |
| --- | --- | --- | --- | --- | --- |
| 0 | Constitutional (genesis clause) | Principal | waived (§1) | Principal | `ConstitutionVersion 1` with `ES-1.0` as Part X; `AD-CK-1.0` registered; `AU-CK-A` granted |
| 1 | Authorization grant | Principal | `AD-CK-1.0` | Principal | `AU-OBS-1` to the Observation function: Source Declarations (§4), feed sources with enumeration contracts, hop rule depth 2, slot plan, the synthetic development feed for Proof 2, the bounded synthetic provider as a declared tool (§5) |
| 2 | Limits | Principal | `AD-CK-1.0` | Principal | Exploratory pool 0; portfolio limits nominal; no allocation possible until a later limits Transition |
| 3 to 12 | Agent Design registration ×10 | Principal | `AD-CK-1.0` | Principal | `AD-R1.0` to `AD-R10.0`, method class `RESEARCH`, provider and cutoff declared, each with its initial method commitment (§6) |
| 13 | Agent Design registration | Principal | `AD-CK-1.0` | Principal | `AD-CK-2.0`, a second `CHECKER` lineage, so that `AD-CK-1.0`'s successor, revocation or amendment can be checked by a Checker outside its lineage; granted `AU-CK-B` at 14 |
| 14 | Authorization grant | Principal | `AD-CK-1.0` | Principal | `AU-CK-B` to `AD-CK-2.0` |
| 15 | Authorization grant | Principal | `AD-CK-1.0` | Principal | `AU-RP-1`, the pooled Research Authorization of §3 |
| 16 | Theme registration | Principal | `AD-CK-1.0` | Principal | `TH-G1`, the Proof 1 Theme, with motivation closure and selection basis |
| 17 | Constitutional (admitted policy) | Principal | `AD-CK-2.0` | Principal | `P-1`'s admitting Transition naming `AU-RP-1` |
| 18 onward | Ordinary operation | Agents, `P-1`, Principal | `AD-CK-1.0`, `AD-CK-2.0` | `P-1` or Principal | Reservations, attempts, Research Records, Hypothesis registrations under `P-1` |

No Runner or Execution Authorization is granted at genesis: Proofs 1
and 2 run no Decisions and no Paper Book. Each is a later checked
Transition, carrying the fill rule of §6 when the Execution
Authorization is granted.

## 3. Initial actors, permissions, scopes, units, tiers, caps, expiry

| Actor | Authorization | Permissions | Scope and independence content | Units | Guarantee tiers | Cap | Expiry |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Principal | none needed | Everything reserved in Part V; `FENCE`; `P-1` suspension; genesis | all | — | — | — | — |
| `AD-CK-1.0` (`CHECKER`) | `AU-CK-A` (seq 0) | Check every class; reproduction records; expected-but-missing Outcomes; propose nothing but its own successor | **Full §III.8 criteria apply**: separate authority (no Research Authorization, never a proposer's lineage), protected standards (criteria pinned at base), immutable evidence (committed records only). **Supplement**: provider different from any proposer it checks, as Authorization content; this adds to the three conditions and replaces none | 60 units from its own grant for its calls | provider calls: see §5 | 60 | 2027-04-30 |
| `AD-CK-2.0` (`CHECKER`) | `AU-CK-B` (seq 14) | As `AU-CK-A`; the Checker for anything concerning `AD-CK-1.0` | As above | 30 | see §5 | 30 | 2027-04-30 |
| Observation function | `AU-OBS-1` (seq 1) | Retrieve declared sources and feeds; hop retrievals on request; commit Market Observations | `SRC-E` (daily equity closes; structural bound session end), `SRC-SYN` (synthetic development feed; enumeration contract: complete daily listing; labelled synthetic); hop domains: the synthetic corpus only | — | — | — | 2027-04-30 |
| `AD-R1.0` to `AD-R5.0` (`RESEARCH`, Theme path) | `AU-RP-1` (seq 15) | Reserve, attempt, settle; Research Records of every kind; Predictions; propose registrations and successors | Theme `TH-G1`; discovery scope: `SRC-SYN`, fixed grant 60 units of the pool, cadence daily, hop depth 2 | **one shared pool of 600 units** (§3a) | tier 1 for metered runs; provider calls per §5 | **aggregate 100 units per lineage** across the pool, not an allocation of 100 | reservations 7 days; Authorization 2027-04-30 |
| `AD-R6.0` to `AD-R10.0` (`RESEARCH`, empirical path) | `AU-RP-1` (seq 15) | As above | `SearchFamily SF-G1` over `SRC-E`, no Theme; same discovery scope | same pool | same | same | same |
| Strategy Runner, Execution function | not granted at genesis | — | — | — | — | — | — |

### 3a. What a unit measures

A **unit** is the Authorization's common measure of metered work. The
grant of `AU-RP-1` is 600 units, shared by ten lineages; the cap of 100
is the most any one lineage may have reserved plus settled at any time;
ten lineages can together consume at most 600 however it is divided.
Heterogeneous operations consume units through the **estimation rule**,
Authorization content, provisional:

| Operation | Units | Basis (provisional) |
| --- | --- | --- |
| Provider model call | 1 per 10,000 tokens, input plus declared maximum output | Tokens are what the provider meters; the maximum is computable before dispatch when the output cap is set (§5) |
| Backtester run on system-allocated compute | 1 per run up to a declared dataset size; 2 above it | A run is refused before it starts if no allowance; its charge is a declared constant |
| Hop retrieval or feed screen | 0.1 per retrieval; 0.05 per screened item | Declared constants for metered local work |
| Checker calls | Charged to the Checker's own grant, never to a proposer's | Separate authority |
| Review attention of the Principal | Not metered | Outside the grant |

Every attempt pre-records its estimated maximum in these units;
settlement records the actual in the same units from the provider's or
tool's record.

## 4. Evidence at genesis, labelled

- Proof 1 runs backtests on `SRC-E` history. Every such Research Record
  is **Historical Reconstruction**, carries dataset snapshot identity
  and hash, source cutoff, parameters, backtester version and hash, and
  a reproducibility binding (PD-006), and is checked with the finding
  "authored knowing the period". It can reject a candidate and motivate
  succession; it earns nothing.
- Proof 2 runs on `SRC-SYN`, a **synthetic** development. Every
  Observation from it is labelled synthetic in its Source Declaration;
  no Prediction over it is Contemporaneous Forward Record; its
  "resolution" tests the machinery and is reported as such.
- No genuine prospective market evidence exists at genesis, and the
  record says so on every Evaluation.

## 5. Demonstrated controls versus provider assumptions

| Control | Mechanism | Standing |
| --- | --- | --- |
| Metered runs, screens and retrievals (tier 1) | The attempt's pre-record is refused before execution when allowance is short; the charge is a declared constant; nothing external | **Demonstrated by the system** once the boundary exists; a ceiling |
| Provider output cap (tier 2) | The provider's request parameter limiting output tokens, with input tokens counted before dispatch; the maximum charge is computable before dispatch **if** the provider enforces the parameter and bills by tokens at a declared price | **Unresolved**: enforcement is a provider property the system has not established. Until the Principal records a decision on a named provider, no real provider call is tier 2 |
| Bounded synthetic provider | A declared tool under `AU-OBS-1` that enforces an output cap by construction and bills in units | **Demonstrates the funding protocol** (reserve, attempt, settle, overrun, fence) end to end. It is **not evidence** of any real provider's spending guarantee |
| Uncapped calls (tier 3) | None | **Prohibited** at genesis, as proposed in PD-008 and unchanged here; relaxing it is a Principal decision |

Consequence for the demonstrations: Proof 1 and Proof 2 run their
funding protocol against the bounded synthetic provider and metered
local tools. A real provider enters only when the Principal records,
per provider, the cap parameter, the billing basis and the acceptance
of the enforcement assumption as a **provider assumption**, labelled so
on every attempt that relies on it. The research agents' reasoning
itself may run on a real provider only under that decision.

## 6. The fill rule and the method commitments for the first Checks

**Method commitments** (Part X §3), fixed in each registration before
any window:

| Subject | Commitment |
| --- | --- |
| Each `AD-R` lineage | Contribution measure: forward-resolved research per unit, questions closed including negative, screening coverage; estimate error for any `SELECTION` record |
| Each Hypothesis registered in the proofs | Scoring rule: hit rate against the registered tolerance; `N_eff` method: cluster Outcomes by shared shock within the horizon; predictive-check method: coverage of the committed interval at a declared level; all versioned with hashes |
| Any Strategy Version registered in Proof 2 (incubating, zero capital) | `N_eff` and multiplicity methods as above; cost model: declared spread, impact and fee assumptions per instrument class with basis; cost-sensitivity: two conservative scenarios; predictive check and thresholds; stress set `SS-1.0` calibrated from the instrument class |

**Fill rule `FR-0` (provisional; plan step 7 content).** Granted with
the first Execution Authorization, not at genesis: a simulated fill at
the first `VALUE` Observation of the instrument witnessed after the
order's admission, at that value plus a declared slippage per instrument
class, for a quantity no greater than a declared participation fraction
of the Observation's volume, the remainder staying open. It is a method
of the Execution function under PD-004.15; its fills are provisional
until confirmed and are never cost evidence (PD-005). Replaceable by a
successor commitment.

## 7. D-17: continuation after death between Decide and Apply

Starting rule, as the Principal set it:

1. **Unchanged base.** A decided, unapplied Transition found by a fresh
   process may be applied only if **every current admission condition
   still holds at Apply**: the base is still the head; for a delegated
   class, every `P-1` condition; for every class, the Authorization
   active, the cited `RESERVATION` open and below any `FENCE`, no
   `OVERSPENT`, no suspension of the deciding policy, no expiry passed.
   An unchanged head is necessary, never sufficient.
2. **Changed base.** Re-check under the rules applicable at the new
   base; the Check record names the new base; the decision is re-made
   by the applicable decider (`P-1` on a `PASS`, else the Principal).
3. **No bypass by restart.** A funding fence, a reservation expiry, an
   exhausted allowance, or a suspended delegation refuses the Apply or
   the attempt whatever the head says; restart re-reads the ledgers and
   finds them.
4. **Resuming versus admitting.** Resuming an **already-admitted
   external attempt** (a `PENDING` record exists) means settling it, or
   dispatching it if it was never dispatched, under the permission its
   commit consumed; no new admission is needed and none is made.
   Admitting a **new attempt** (including any retry) is a fresh commit,
   ordered against any fence and checked against the reservation at its
   own sequence. A fresh process never treats an intention it finds in
   memory as an admitted attempt.
5. **Death between Check and Decide** leaves a checked, undecided
   Transition; the decider decides it under rule 1 or 2. **Death after
   Apply** leaves an applied Transition; nothing is re-done.

## 8. Execution infrastructure

Genesis names no runtime, scheduler, queue, database or framework.
Every actor above is defined by its Authorization and the ledgers it
reads and writes; the substrate that runs the agents, the Checkers and
the Observation function is chosen later by evaluating existing agent
runtimes and workflow engines against one concrete sequence (reserve,
attempt, interruption, fence, retry, settlement, evidence admission), as
the Principal directed; a custom component is justified only by naming
the contract no existing one satisfies (Part IX principle 10).

## 9. D-06: the continuity claim

**The clause as it stands** (§III.5, "Evidence does not transfer"):

> A Transition may *claim* evidentiary continuity for a Strategy Version
> with `Proposition delta: NONE`; the claim is checked independently and
> recorded as a claim, and reporting always shows the per-version
> record. **TENTATIVE**; see audit D-06.

**The choice in plain English.** When a new Strategy Version keeps the
same economic proposition and changes only implementation (a lookback,
a rebalance frequency), may the registration say "this is a
continuation of the predecessor's track record"? Two readings. Keep the
claim: a checked, recorded assertion that informs a reader and grounds
nothing, since every Evaluation already uses the version's own forward
record (Part X R-2) and shows the family (R-4). Remove the claim: a
successor begins at zero with no continuity assertion at all; the
predecessor's record is visible as family history and nowhere else.

**What the claim would do if kept.** Nothing that any rule uses: it
cannot enter a grounding series, cannot change a floor, cannot move
capital. It would exist to be read, and a reader who sees "continuity
claimed" beside a per-version record of two events will weigh it,
which is exactly the inherited confidence the adopted doctrine forbids
("not partially, not proportionally, not with adjustment").

**Recommended resolution, the smallest suitable for the paper
prototype: remove the claim.** Delete the sentence and the TENTATIVE
marker; in Part V's Strategy Version registration Check, delete
"continuity claim"; in T-B, replace "Continuity claim: yes" with "No
continuity claim; the family is shown under Part X R-4". `ΔS`: one
sentence removed; `ΔO` and `ΔA` none. D-06 closes, and the Constitution
carries no TENTATIVE marker.

## 10. Constitutional Delta of this record

```text
ΔO: NONE.
ΔS: the Part V genesis paragraph (§1); the D-17 continuation rule
    (§III.8 lifecycle); "resume" versus "admit" for attempts (§III.5);
    removal of the D-06 continuity-claim sentence and its two
    references (§9).
ΔA: +1, one-time: the Check requirement waived for Apply sequence 0's
    enumerated content (text, one CHECKER registration, one Checker
    Authorization), decided by the Principal without independent
    Check, never reusable. No other right is created or moved; the
    first Authorizations are granted by their ordinary classes under
    Check from sequence 1.
```

## 11. Decisions for the Principal

| Question | Proposal |
| --- | --- |
| The bootstrap of §1 with an agent Checker, the Part V genesis clause, and the one-time `ΔA` | Yes |
| A second `CHECKER` lineage at sequences 13 and 14 so the first can itself be checked | Yes |
| The shared 600-unit pool with a 100-unit aggregate cap per lineage, and the unit table of §3a | Yes, provisional |
| Provider output caps labelled unresolved; demonstrations on the bounded synthetic provider; real providers only by a recorded per-provider decision; uncapped calls prohibited | Yes |
| D-17 rule as in §7 | Yes |
| `FR-0` as the provisional fill rule, granted later | Yes |
| D-06: remove the continuity claim | Yes |
| Proceed to the independent whole-design audit before any admission of `ConstitutionVersion 1` | Yes |
