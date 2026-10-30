# Workbench Readiness Audit - Local Research Workbench over the First Cycle

Status: **AUDIT EVIDENCE - READ-ONLY INSPECTION OF THE BUILT CYCLE AGAINST THE WORKBENCH BRIEF. AUTHORIZES NO IMPLEMENTATION, USER INTERFACE, DATASET OR SCOPE CHANGE.**

Date: 2026-10-30. Reviewer: Claude (Fable 5.1), at the Principal's
direction. Subject: the Principal's brief for a small local research
workbench (reproduced in section 7), read against the implementation at
HEAD `19facef`, the retained example run under
`artifacts/development/adaptation-final/3887aa1acdab4e0cbe39be306f13e183/`
(inventory `038e222d96dfe9d47be668df674b1338e3c6daabec34e3811d3ee70e341a1e5c`),
[BUILD.md](../../BUILD.md), the
[first research-cycle plan](../plans/first_research_cycle_implementation_20261029.md)
and the
[build approval addendum](../decisions/first_research_cycle_build_approval_addendum_20261029.md).

Method: source reading only. No process was started, no database was
opened, no test was run and no file under the inventory was modified. The
companion [workbench plan](../plans/local_research_workbench_20261030.md)
proposes the work this audit finds necessary. Neither document authorizes
anything.

## 1. Disposition

**The built cycle already persists almost everything the brief wants to
show. The workbench is a read-and-invoke layer over existing boundaries,
not a new system.** Three things the brief asks for do not exist yet and
require harness changes, not only a page: dataset variants, reopening a
retained run, and a research session that lives longer than one scripted
case. The brief is outside the admitted first-cycle scope, which excluded
"broad UI work", so it needs a Principal decision before code. The expected
Constitutional Delta is 0/0/0 if the variants are declared synthetic
Observations from the existing source and no new object kind is introduced.

## 2. The brief against what exists

| Brief | Exists today | Gap |
| --- | --- | --- |
| Start a research run on the synthetic example | `python3 -m acceptance.local --example` freezes a bundle, starts core and tools as processes, runs startup and case `E01`, writes `E01.json` and retains the state directory | Runs one scripted case to completion and then kills every process. No way to start, pause or step |
| A few dataset variants with different outcomes | One cohort of 12 rows, fixed in the admission packet, pinned by digest in `actors.formation()` and copied verbatim by `actors.observe()` | None. The admission packet is frozen by the approved manifest, so variants must come from somewhere else (F1) |
| Watch the sequence | Every stage is a ledger record with a sequence number and hash. Transitions ledger: `PROPOSED`, `CHECK`, `DECISION`, `APPLIED`, `REFUSAL`. Evidence ledger: `OBSERVATION`, `RESERVATION`, `ATTEMPT`, `RESEARCH_RECORD` (kinds `plain` and `SELECTION`), `SETTLEMENT`, `CLOSED`, `BIND` | None in the records. Needs a view that orders them into the seven stages (F4) |
| Inspect the evidence, rows, counts, why the next action | The observation document carries the rows. Research records carry `n`, `k`, `n_large`, `k_large`. The selection record carries `reason`, `initial_failure`, `candidates` with cost estimates, `chosen_subset`, `rejections` and `revisit_rule`. The control record carries `rule`, `passes`, `reason`, `research_failure` and `next_action` | None. The "why" is already on the ledger (F4) |
| See the controls | `budget` query per grant returns committed, reserved, headroom, spendable and overspent. `obligations` returns pending attempts, binding states and decided-unapplied transitions. Refusals are `REFUSAL` events with reason and detail, and command receipts live in the `requests` table | None in the records (F5) |
| Reopen a run and continue | Retained state keeps `harness.sqlite`, `clock.json`, `DISPOSABLE.json` and logs, with capability tokens removed. The core rebuilds its view from the ledgers on start. `LocalRuntime.host('restart')` already restarts core and tools within a run with a quiescence proof | No command starts a core against a retained state directory. Live reopen also requires the current source to match the run's inventory (F2) |
| Read real records, invoke existing commands | All reads go through ten query operations on the core socket. All mutations go through actor programs in `actors.py` and Principal commands | None. The workbench must use these and nothing else (F6) |
| Thin Python API, single page, local, no accounts | The harness has no dependency outside the standard library | A standard-library HTTP server on loopback satisfies the brief without a new dependency (F8) |
| Label the researcher deterministic and the data synthetic | Records carry `synthetic: true` and a classification string. The researcher is a fixed policy in `actors.next_experiment()` | Labels must be on the screen, not only in records (F9) |

## 3. Records and queries the workbench would read

Reads, all through the core socket as the Principal role, defined in
`contracts.READS`:

| Query | Returns | Workbench use |
| --- | --- | --- |
| `history` | Paged ledger records, `E` or `T` | The sequence view and the evidence list |
| `get` | One record by exact reference and hash | Evidence detail, following `refs` |
| `closure` | Both ledgers at the current instant | The independent reader's input |
| `state` | Current `N`, designs, grants, themes, hypotheses, limits, suspensions | Status header, permitted next steps |
| `budget` | Committed, reserved, headroom, spendable, overspent for one grant | Controls pane, one row per grant |
| `obligations` | Pending attempts, binding states, decided-unapplied | Controls pane and continuation |
| `clock` | Synthetic time and `E` | Status header |
| `profile` | Setup, artifacts, inventory and its digest | Run identity and labels |
| `inspect-request` | Receipt for a request id | Accepted or refused actions and reasons |
| `dispatch-status` | Dispatch claims and receipts | Tool run status |

The independent reader in `acceptance/reader.py` reconstructs and audits a
whole history without importing core admission code. Its `audit()` function
takes the two ledgers as lists, so it can also run over a retained database
read directly with `Store.events()` when no core is live. That is the
read-only reopen path.

## 4. Findings

**F1. Dataset variants are not supported and cannot come from the admission
packet.** `actors.formation()` finds the cohort by matching the document
digest to `profile.artifacts.formation_cohort.content_sha256`.
`actors.observe()` deep-copies that same document and changes only its
dates. The artifacts file is materialized by `build_support/freeze.py` from
`docs/plans/research_cycle_admission_20261029/designs_and_methods.json`,
which the approved specification manifest covers byte for byte, so editing
it fails the freeze. Variants therefore need a separate catalog, carried into
the bundle by the freeze step, and three actor changes: observe a named
variant, research against a named cohort, and let the control step use the
cohort its prior record names. Every variant must be a declared synthetic
Observation from source `SRC-SYN` with its own `item_id`, which keeps the
Constitutional Delta at zero.

**F2. The second research path exists in code but has never run end to
end.** `actors.next_experiment()` returns `independent-reproduction` when the
large events span more than one shock, and `actors.run_next_experiment()`
handles that branch by exact count reproduction through tool B. The only
coverage is a unit test on the choice function in
`tests/component/test_adaptation.py`. The brief's demo depends on this
branch. It must be exercised through the fixture before the demo is relied
on.

**F3. Reopen has no entry point and has an inventory constraint.** Each
`LocalRuntime` creates a fresh temporary state directory and fresh tokens,
and `close()` kills all processes and copies the state to the retained
directory. Nothing starts a core against a retained directory. When it does,
`Profile.development_permission()` verifies every inventory file against the
current tree, so a run retained under an older inventory cannot be reopened
live after any covered source changes. It can still be inspected read-only
from its SQLite file. The workbench must show which of the two it is doing.

**F4. The sequence and the reasons are already recorded.** No new record
kind is needed to show question, experiment, result, diagnostic, revised
question, Check and admission. Each stage maps to existing records: the
research record's `question` and `result`; the reservation and attempt that
preceded it; the selection record's `adaptation.reason` and
`initial_failure`; the chosen candidate's `question`; the `CHECK` transition
with per-criterion statuses and references; the `DECISION` and `APPLIED`
transitions and the consumed `BIND`. The workbench adds a view, not data.

**F5. The controls are already queryable.** Reserved before work is visible
as a `RESERVATION` followed by an `ATTEMPT` with a `maximum`, then a
`SETTLEMENT` with `actual` and provenance. Refused actions are `REFUSAL`
records with `reason` and `detail`. The budget query gives the per-grant
totals the brief asks for. The grants in play are `AU-RP-1` for research,
`AU-CK-A` and `AU-CK-B` for the two Checkers and `AU-OBS-1` for observation.

**F6. The workbench driver holds every role.** The acceptance fixture issues
one token per actor and the driver plays the Principal, the Observation
function, the researcher and both Checkers. The workbench inherits exactly
that trust: a same-user process with no OS isolation claim. It must bind to
loopback only, must not expose the tokens or the state path to the page, and
must not add any write path to SQLite outside the core. The schema's
immutability triggers and the absence of a generic append API in `storage.py`
should remain as they are.

**F7. The brief is a scope expansion that needs a decision.** Section 1 of
the first research-cycle plan excludes "broad UI work". The build approval
addendum authorizes building, fixing and testing "the agreed synthetic first
cycle". A workbench with dataset variants and reopen is agreed nowhere. The
plan proposes the decision text. Until it is admitted, no workbench code is
authorized.

**F8. No dependency is needed.** Every import in the harness, acceptance and
build support is standard library. A standard-library HTTP server serving one
HTML file and JSON on 127.0.0.1 meets "thin Python API and a single-page UI".
Choosing a web framework would be a technology selection and a new
dependency, and should go to the Principal rather than be made in code.

**F9. Labels and the old demo.** The page must state that the researcher is
a deterministic policy, the data are synthetic, the store is disposable and
OS isolation is unverified. The presentation under `docs/presentations/demo/`
is a scripted story that its own README says implements nothing. It must not
be reused as the workbench or linked from it as if it were.

**F10. The example case cannot be reused as the session driver.** `E01` in
`acceptance/cases.py` hard-codes the original dataset's outcomes, including
6 of 10 and `N == 17`, as assertions. A variant breaks it. The workbench needs
step-level invocation of the agent operations, which already exist as
individual operations, and `E01` should stay unchanged as acceptance
evidence.

**F11. Artifacts grow per run.** Each start freezes a bundle under
`artifacts/development/run-bundles/<run_id>/` and copies the covered source
to `artifacts/development/builds/<digest>/` when that digest is new. A
workbench used interactively will create many run directories. They are
disposable, but the plan should say where they go and how they are listed.

## 5. What the built cycle does not need

No new ledger kind, no new query, no new grant class, no new Transition
class and no change to Checkers, tools or Rules. The researcher policy keeps
its method identifier and its two candidates. If any of these turns out to be
necessary during the build, that is a stop condition under AGENTS.md and
returns to the Principal.

## 6. What this audit did not do

It did not run the example, open a retained database, test the reopen path,
prototype a page or measure performance. It did not verify the retained run's
inventory against the current tree. The findings are from reading the code
at one commit.

## 7. The brief, as received

> Build a small local research workbench around the working harness. You
> should be able to run an experiment and see how its result changes the
> next decision without reading JSON or terminal logs.
>
> One screen is enough: start a research run on the existing synthetic
> example with a few dataset variants that produce different outcomes; watch
> the sequence, question, experiment, result, diagnostic, revised question,
> Check, admission; inspect the evidence, the actual rows, computed counts
> and why the researcher chose its next action; see the controls, budget
> reserved and spent, accepted or refused actions and reasons; reopen a run,
> display its saved history and continue from the permitted next step. The
> interface should read the real persisted records and invoke the existing
> commands.
>
> The first useful demo: run the original dataset, see the shared-shock
> problem, then run a variant with independent shocks and see the researcher
> take a different path. Close the app, reopen it, and inspect both
> histories.
>
> Keep it local and simple: a thin Python API and a single-page UI. No
> accounts, cloud deployment, graph editor or infrastructure project. Label
> the researcher as deterministic and the data as synthetic.
>
> Once that works, the next functional addition is one real research
> question using an uploaded historical dataset. An LLM proposer can follow
> when there is a clear task for it. The immediate goal is to make the
> existing research cycle understandable and operable.
