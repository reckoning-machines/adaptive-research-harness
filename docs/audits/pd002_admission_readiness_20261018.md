# PD-002 Admission-Readiness Summary

Status: **SUMMARY — EVIDENCE, NOT DOCTRINE. Authorizes nothing.** Prepared
2026-10-18 for the Principal's final review of
[PD-002 revision 4](../decisions/principal_decision_002_predictions_decisions_observation.md).
It restates nothing the record does not say; it lists what admission would
admit, what would still be open, and what would change.

## 1. Dispositions in revision 4

| Disposition | What it admits |
| --- | --- |
| PD-002.1 Predictions and Strategy Decisions (N-5) | Strategy Decision as a new Evidence kind: one per decision event, committed output of an admitted artifact against a closed set of ledger inputs; stable `DecisionEventId`, one Decision per event, `FAILED` final, infrastructure retry lawful; closure over Evidence, Applied History and Paper Book marks with commit-time witness marks; reproduction by re-execution with the closure alone, standing derived from Checker-committed reproduction records; decision-implied record at a Standard-declared notional and executed record from fills, both `DERIVED`; order sets keyed to Allocation Transition, `StateVersion` and Decision, with `NEW`, `REPLACE`, `CANCEL`; "prediction target" defined as scored observable and sign; frozen models admissible, reproducibility class Checker-found |
| PD-002.2 Independent Market Observation (N-3) | Observation function under a Principal-granted Observation Authorization as the sole committer of Market Observations; Source Declaration with immutable `SourceId` (meaning fields) and pinned `SourceRevision`; results `VALUE`, `ABSENT`, `RETRIEVAL_FAILED`; claimed source time informs, witnessed receipt is fact; availability as a derived interval; prospective class only when commitment precedes the lower bound; refusal otherwise |
| PD-002.3 Genesis (N-1) | Recorded as a foundational bootstrap issue; must close before any replay or recovery conformance claim; candidate sequence-0 design not decided |
| PD-002.4 Strategy Runner (U-9) | Runner function under a Runner Authorization: runs admitted Strategy Versions on declared triggers, commits all Decisions, may not propose, admit, change versions, alter Standards or touch capital; runs by Applied History standing and survives the proposing agent's retirement; never certifies reproduction. Execution function consumes Decisions and alone commits paper execution facts. Roles distinct in authority, not necessarily in process |
| PD-002.5 Source Declarations | Remain Observation Authorization content; no new governed object |
| PD-002.6 Training cutoff | Carried into D-14 as a provenance requirement of Agent Design registration; never evidence of freedom from leakage |

## 2. Constitutional Delta of revision 4

```text
ΔO: +1 Evidence kind (Strategy Decision). Nothing else.
ΔS: Strategy (prediction target; declared inputs, trigger, reproducibility
    class; forward record = Decision series; frozen model admissible).
    Evidence (Decision fields and rules; Observation result, times,
    SourceId/SourceRevision; Prediction resolution rule and set; Outcome
    over a bound set, UNRESOLVABLE; Evaluation closure; availability
    interval; I-2 to the lower bound; derived reproduction standing).
    Paper Book (set key; order types; remainder from fills; limit refusal).
    Authorization (Observation and Runner content; Source Declaration
    identity rule; base-state rule for source checks).
    Agent Design (training cutoff as provenance).
    Evidence commit boundary (witness-read duty; refuse when a head is
    unreachable).
ΔA: +2 Authorization classes (Observation, Runner), +2 function roles.
    Commit restrictions: Market Observation -> Observation function;
    Strategy Decision -> Runner; reproduction record -> Checker
    Authorization; execution facts -> Execution function.
    Execution function: rights unchanged, duties added.
    No Research, Checker or Observation Authorization gains or loses a
    right it held before PD-002. No admission authority moves.
    Pending U-10 (Outcome committer): no change declared.
```

## 3. Unresolved constitutional blockers

None blocks admitting PD-002 itself. Each blocks something named.

| Blocker | Blocks | Who decides, when |
| --- | --- | --- |
| U-10 Outcome committer | The complete Part V commit table; operating the Hypothesis loop without a per-instance human act | Principal, with D-10 |
| D-10 Checker independence (U-3, A-9) | Any `REPRODUCED` standing in practice, so any capital competition on Decisions | Principal, plan step 5 |
| N-1 genesis (PD-002.3) | Any replay or recovery conformance claim; CPOC certification | Principal, plan step 4 or 8 |
| `ES-1` content (U-6) | Any Evaluation; any allocation citing one | Principal, Constitutional Transition after admission |
| U-1 non-reproducible grounding | Capital for `NON-REPRODUCIBLE` versions only; the `STOPPED` path exists | Principal, if wanted |
| D-17 (U-5) | The Decide-to-Apply recovery witness | Principal, plan step 4 |
| U-2 cross-ledger simultaneity | Nothing now; revisit at plan step 9 | Principal |
| U-4, U-7, U-8 | Narrow availability reading; genesis; limits at a moving head | Carried |

PD-003 (proposed separately) depends on PD-002 and adds no blocker to it.

## 4. Constitution sections that will change on admission

Part II Roles (Observation function, Strategy Runner, Execution function
named); §III.2 (resolution rule and set); §III.3 (prediction target,
declared inputs, trigger, reproducibility, forward record, frozen model);
§III.4 (training cutoff, direction); §III.5 (Decision row and rules,
`DecisionEventId`, closure and witness marks, Observation result and
times, Prediction and Outcome changes, Evaluation closure, reproduction
records, availability interval, witness-read duty, citation renames
PD-002 → PD-001.2 and PD-003 → PD-001.3); §III.7 (Observation and Runner
Authorizations, Source Declaration identity, base-state rule, Checker
reproduction commit); §III.10 (set key, order types, remainder, cancel,
re-execution, limit refusal, Execution function consumes Decisions); Part
IV (I-2 lower bound; I-12 Decision binding; I-13 witness read; closure
precedes commitment; one Decision per event); Part V (Evidence commit split
four ways; registration Check additions; Order row); Part VI (T-A, T-B,
T-D revised; T-F and T-G added on the unified timeline); Part VII (new
rows); Part VIII (three non-agent writers); `ES-1` (U-6, after admission);
audits and plan (N-5, N-3, U-9 closed; N-1 bootstrap; U-1 to U-8, U-10
registered; challenge 9 reworded).

## 5. Verification of this summary against revision 4 (2026-10-18)

Checked line by line against the record:

| Claim in this summary | Where revision 4 states it |
| --- | --- |
| Outcome committer deferred as U-10, no change declared | PD-002.4 commit-restrictions table ("Outcome: as drafted (any authorized) ... the committer question is U-10"); F-2 closing paragraph; remaining-defects table U-10; OSA fact table ("Evidence commit (committer U-10)"); Constitutional Delta ("Pending U-10: Outcome committer; no change declared"); readiness table in the record |
| Runner and Execution distinct in authority, not necessarily in process | PD-002.4 role table ("distinct in authority from the Execution function and the Observation function ... may share a process or service; each commit is attributed to exactly one Authorization"); "Commits: Strategy Decisions ... Nothing else"; "May not ... commit any Paper Book fact"; Execution function restated ("Alone commits paper execution facts ... May not run a Strategy Version, commit a Decision"); ANF check ("three functions, three Authorizations, three commit scopes") |
| `ΔO +1`, two Authorization classes, two function roles, four commit restrictions | Precise Constitutional Delta block, revision 4 |

No discrepancy found. PD-003 revision 2 depends on PD-002 and changes
nothing in it.

## 6. Readiness

Ready for admission as a design, with clarifications the Principal may
wish to state on U-10 (recommendation: decide with D-10) and on whether
the Principal prefers to keep the Runner and Execution function in
separate processes as an operating rule rather than leaving it open.
