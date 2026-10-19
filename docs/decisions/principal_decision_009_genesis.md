# Principal Decision Record 009 — Genesis (N-1) and Decide-to-Apply Continuation (D-17)

Status: **PROPOSED FOR ADMISSION. Not admitted.** Proposes the content
of the first Apply sequences, the sequence-zero waiver, the initial
actors and their Authorizations, the D-17 continuation rule, and the
fill rule and method commitments needed for the first Checks. Depends
on Constitution revision 9 (PD-001 to PD-008 applied). Admits nothing,
certifies nothing, authorizes no code; genesis is executed only after
`ConstitutionVersion 1` is admitted following the independent
whole-design audit ([checklist](../audits/cv1_whole_design_audit_checklist_20261019.md)).

Date: 2026-10-19

Sources: Constitution revision 9 (§III.6 pinning and serial admission,
§III.7, §III.8 Check record, Part V, Part X §3, Part IX principle 10);
PD-002.3 (the genesis sketch); PD-006 §PD-006.3 (the two
demonstrations); PD-007 §PD-007.6 (the genesis choices); PD-008 (units,
tiers, caps, expiry); the Principal's direction of 2026-10-19.

Numbers below are **illustrative and provisional**; each is
Authorization or limit content set at genesis, never Constitution text.

## 1. The sequence-zero waiver, bounded

Every applied Transition pins a `ConstitutionVersion`, and every
consequential Transition requires a Check. Before sequence 0 no version
and no Checker exist. The waiver:

> Apply sequence 0 is a Constitutional Transition proposed and decided
> by the Principal whose proposal content is exactly: (i) the text of
> `ConstitutionVersion 1`, and (ii) one Checker Authorization to a named
> **human** who is not the Principal, the Genesis Checker. For this
> Transition alone the Check requirement is waived. The waiver applies
> to Apply sequence 0 only, to that class only, to that enumerated
> content only, and to no later version, sequence, class, content,
> replay, re-genesis or migration. A Transition at any other sequence
> that claims it is `STOPPED`.

Why it is not a reusable bypass: it is bound to one sequence number,
one class and an enumerated content; it creates a Checker so that
nothing after it is unchecked; a later Constitutional Transition is
checked by the then-existing Checkers; and the clause is itself
Constitution text changeable only by a checked Constitutional
Transition.

**Without a second human, genesis cannot proceed lawfully.** A single
person cannot be both the proposer of every genesis Transition and its
independent Checker, and extending the waiver past sequence 0 is what
the Principal forbade. The Genesis Checker's Authorization names the
classes it may check (every class) and its expiry.

## 2. The initialization sequence, ordered

| Apply | Transition | Proposer | Checker | Decider | Content |
| --- | --- | --- | --- | --- | --- |
| 0 | Constitutional | Principal | waived (§1) | Principal | `ConstitutionVersion 1` text; `ES-1.0` as Part X; Checker Authorization `AU-GC` to the Genesis Checker (human) |
| 1 | Agent Design registration | Principal | Genesis Checker | Principal | `AD-CK-1.0`, method class `CHECKER`, provider and cutoff declared; proposes nothing but its successor |
| 2 | Authorization grant | Principal | Genesis Checker | Principal | `AU-CK-A` to `AD-CK-1.0`: Checker Authorization for Hypothesis, Strategy Version and Agent Design registrations and for reproduction and Outcome duties; provider rule: different provider from any proposer it checks |
| 3 | Authorization grant | Principal | Genesis Checker | Principal | `AU-OBS-1` to the Observation function: Source Declarations (§4), feed sources with enumeration contracts, hop rule depth 2, slot plan, the synthetic development feed for Proof 2 |
| 4 | Limits | Principal | Genesis Checker | Principal | Exploratory pool 0; portfolio limits nominal; no allocation is possible until a later limits Transition raises the pool |
| 5 to 14 | Agent Design registration ×10 | Principal | `AD-CK-1.0` or Genesis Checker | Principal | `AD-R1.0` to `AD-R10.0`, method class `RESEARCH`, provider and cutoff declared, each with its initial method commitment (§5) |
| 15 | Authorization grant | Principal | Genesis Checker | Principal | `AU-RP-1`, the pooled Research Authorization of §3 to the ten lineages |
| 16 | Theme registration | Principal | `AD-CK-1.0` | Principal | `TH-G1`, the Proof 1 Theme, with motivation closure and selection basis; five lineages work in it |
| 17 | Constitutional (admitted policy) | Principal | Genesis Checker | Principal | `P-1`'s admitting Transition, naming `AU-RP-1`; `ΔA` already admitted by PD-007, now placed in force for the named Authorization |
| 18 onward | Ordinary operation | Agents, `P-1`, Principal | `AD-CK-1.0` | `P-1` or Principal | Reservations, attempts, Research Records, Hypothesis registrations under `P-1` |

No Runner or Execution Authorization is granted at genesis: Proofs 1
and 2 run no Decisions and no Paper Book. Each is a later Transition
checked in the ordinary way, carrying the fill rule of §5 when the
Execution Authorization is granted.

## 3. Initial actors, permissions, scopes, units, tiers, caps, expiry

| Actor | Authorization | Permissions | Scope | Units and grant | Guarantee tiers | Cap | Expiry |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Principal | none needed | Everything reserved in Part V; `FENCE`; `P-1` suspension | all | — | — | — | — |
| Genesis Checker (human) | `AU-GC` (seq 0) | Check every class; reproduction; Outcomes | all | — | — | — | 2027-04-30, or revocation after `AD-CK-1.0` is in force |
| `AD-CK-1.0` (`CHECKER`) | `AU-CK-A` (seq 2) | Check registrations; reproduction; expected-but-missing Outcomes | all registrations; never a proposer's lineage; provider ≠ proposer's | 60 units for its own calls | tier 2 (provider-capped) | 60 | 2027-04-30 |
| Observation function | `AU-OBS-1` (seq 3) | Retrieve declared sources and feeds; hop retrievals on request; commit Market Observations | `SRC-E` (daily equity closes, structural bound session end), `SRC-SYN` (synthetic development feed, enumeration contract: complete daily listing), hop domains: the synthetic corpus only | — | — | — | 2027-04-30 |
| `AD-R1.0` to `AD-R5.0` (`RESEARCH`, Theme path) | `AU-RP-1` (seq 15) | Reserve, attempt, settle; Research Records of every kind; Predictions; propose registrations and successors | Theme `TH-G1`; discovery scope: `SRC-SYN`, fixed grant 60 units, cadence daily, hop depth 2 | pooled 600 units; 1 unit = 10,000 provider tokens or one backtester run | provider calls tier 2 (max-tokens cap set ≤ estimate); backtester runs tier 1 (metered); uncapped calls forbidden | 100 per lineage | reservations 7 days; Authorization 2027-04-30 |
| `AD-R6.0` to `AD-R10.0` (`RESEARCH`, empirical path) | `AU-RP-1` (seq 15) | As above | `SearchFamily SF-G1` over `SRC-E`, no Theme; same discovery scope | as above | as above | 100 per lineage | as above |
| Strategy Runner, Execution function | not granted at genesis | — | — | — | — | — | — |

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

## 5. The fill rule and the method commitments for the first Checks

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

## 6. D-17: continuation after death between Decide and Apply

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

## 7. Execution infrastructure

Genesis names no runtime, scheduler, queue, database or framework.
Every actor above is defined by its Authorization and the ledgers it
reads and writes; the substrate that runs the ten agents, the Checker
and the Observation function is chosen later by evaluating existing
agent runtimes and workflow engines against one concrete sequence
(reserve, attempt, interruption, fence, retry, settlement, evidence
admission), as the Principal directed; a custom component is justified
only by naming the contract no existing one satisfies (Part IX
principle 10).

## 8. Constitutional Delta

```text
ΔO: NONE.
ΔS: the sequence-zero waiver clause as Constitution text (Part V or the
    admission text of ConstitutionVersion 1); the D-17 continuation rule
    (§III.8 lifecycle); "resume" versus "admit" for attempts (§III.5).
ΔA: NONE beyond what is already admitted. Genesis grants the first
    Authorizations by the ordinary class; the waiver is a one-sequence
    exception to the Check requirement, not a right.
```

## 9. Decisions for the Principal

| Question | Proposal |
| --- | --- |
| The waiver as bounded in §1, and a second human as Genesis Checker | Yes; no genesis without one |
| The sequence of §2 and the actors of §3 | Yes, numbers provisional |
| No Runner or Execution Authorization at genesis | Yes |
| D-17 rule as in §6 | Yes |
| `FR-0` as the provisional fill rule, granted later with the Execution Authorization | Yes |
| Proceed to the independent whole-design audit before any admission of `ConstitutionVersion 1` | Yes |
