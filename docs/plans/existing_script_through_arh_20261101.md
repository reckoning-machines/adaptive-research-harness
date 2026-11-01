# One Existing Script Through ARH - Plan

Status: **PLAN FOR DISPOSABLE DEVELOPMENT UNDER THE ADDENDUM'S WORKFLOW PARAGRAPH. CV1 UNCHANGED. CONSTITUTIONAL DELTA 0/0/0. TWO ITEMS NEED THE PRINCIPAL'S ANSWER BEFORE WORK ON THEM STARTS, LISTED IN SECTION 2.**

Date: 2026-11-01. This plan turns the
[adoption review](../audits/adoption_review_20261101.md) into an
assignment, with the Principal's four adjustments and two corrections
folded in. It does not restructure the prototype. It produces one
experience and measures what it cost.

## 1. The goal

Take a research script the Principal already uses, run it through ARH,
retain an unsuccessful result, show that history changing the next
investigation, then interrupt the work and resume it without losing the
record. Measure the extra code and the setup time.

Everything else in this plan exists to make that possible with the least
new machinery. R6 of the review is the goal. R1 and R4 are built only as
far as that script needs. R5 is included with the Principal's adjustment.
R3 is fixed in proportion. R2 is deferred.

Success is one report, under `docs/implementation/`, that a reader can
follow from the script as it was to the script under ARH, with the
unsuccessful result on the ledger, the next investigation chosen because
of it, an interruption survived, and two numbers: lines of code added and
minutes of setup.

## 2. What the Principal supplies or decides

- **P1, the script.** Name one Python analysis the Principal uses on
  historical data held on disk. It should be deterministic given its
  inputs, read its data from files, and produce a numeric result or a
  small table. No model provider calls. A script that calls a provider is
  a separate test with the decisions the
  [local documents report](../implementation/local_documents_research_20261101.md)
  lists in section 4.
- **P2, what reopen identity covers.** Answered on 2026-11-01: the
  Principal authorized the reopen change within the scope of section 5,
  with two corrections. Files are included by whether they take part in a
  run or its recovery, not by directory, so the client, the workbench
  session code and the fixture modules the sessions use are in. The
  installed Python and declared package versions are compared on reopen,
  since hashing a declaration does not detect an environment change. It
  is implemented and tested; section 5 records what it covers.

## 3. The experience, step by step

1. **Baseline.** Run the script as it is, from its own directory, and
   record what it reads, what it writes, how long it takes and how many
   lines it is. This is the before measurement.
2. **Connect it.** Make the script a tool in an experiment directory. If
   it is a pure function of files it reads, it runs as a host-run tool
   with `interface: inputs`, receiving the committed documents and the
   design record, as `experiments/local_documents/calc.py` does. If it
   needs its own environment, it runs as a caller-executed tool from the
   researcher process, as `examples/langgraph_headlines/provider.py`
   does. The choice is made once and recorded with the reason.
3. **Supply the setup.** A generator in `arh_client` writes the three
   setup files from a short description: the question, the source kind,
   the tool, the budget and the tariff. It supplies administrative
   defaults only: grants, limits, a theme, methods, provenance, identities
   and the startup sequence. It does not supply the evaluator. The
   evaluator is written for this script by hand, and in its first form it
   re-runs the committed script on the committed inputs under the Checker
   identity and compares the result hash, verifies the design preceded
   the attempt and the attempt settled, and verifies the selection. That
   checks reproducibility and record integrity. It does not independently
   validate the calculation or the research method, and the report says
   so.
4. **Run it and keep what happens.** Import the data, record the
   expectation before running, run, and retain the result whatever it
   is. The expectation is written to be tested, not to fail. If the
   demonstration needs a refused or failed case to show a control, that
   case is labelled as deliberate in its record and in the report.
5. **Let the failure change the next step.** The candidate rule reads the
   history under the current direction. Candidates already tried and
   rejected are shown with the reason they were rejected and a condition
   for reconsideration, and they return to the live set when the condition
   is met, for example when new documents arrive or a different direction
   is admitted. Nothing is excluded forever. The selection record names
   which earlier records changed the candidate set. A test shows that the
   same conclusion with different history produces a different set.
6. **Interrupt and resume.** Kill the researcher between the attempt and
   its record, close the host, reopen the run, and continue. The record
   is intact, the attempt resolves as resumed, recovered or reconciled,
   and nothing runs twice.
7. **Measure.** Two separate figures. Development time: the hours spent
   building the integration, the generator and the evaluator for this
   script. Adoption time: the minutes a subsequent user needs to configure
   and run the finished integration, from first command to the first
   admitted direction, measured by doing it again from a clean run
   directory. Beside them, lines added to the script, lines in the
   experiment directory, and the list of concepts the user had to touch.
   These go in the report with the baseline from step 1.

## 4. Changes to the code, in order

| Step | Change | Where |
| --- | --- | --- |
| 3 | Setup generator with administrative defaults, factored from the two `make_setup.py` scripts; the two examples become callers of it | `client/arh_client/setup.py`, `examples/langgraph_headlines/make_setup.py`, `experiments/local_documents/make_setup.py` |
| 3 | A reproducibility evaluator for a host-run or caller-executed script, written per script on the toolkit's `validate_motivation` hook | the new experiment directory |
| 5 | Candidate rule reads history; rejected candidates carry reason and reconsideration condition; selection records cite the history they used | `experiments/local_documents/researcher.py` and its evaluator, or the new experiment's researcher if the script lives there |
| 6 | Nothing new. The host, the client's `Execution.run` and the workbench session already do this; the step verifies it on this script | `tests/integration/` |
| done | Live reopen decided on the execution identity and the recorded environment; the full inventory kept as the build identity | `build_support/freeze.py`, `adaptive_research_harness/profile.py`, `workbench/session.inventory_matches`, `tests/integration/test_reopen_identity.py` |

Deferred: packaging the host so it runs outside the checkout (R2). The
immediate irritation is unrelated edits preventing reopen, which P2
addresses. A general setup framework is not built; the generator does
only what this script needed.

## 5. The execution identity, as built

A file is in the execution identity when it takes part in a run or in its
recovery, whatever directory it sits in. The list is kept in
`build_support/freeze.py` and recorded in every bundle's inventory as
`execution_files`.

| In | Why |
| --- | --- |
| Everything under `adaptive_research_harness/` | The core, the host, the workers |
| Everything under `client/arh_client/` | The researcher, Checker and Principal processes run on it |
| `workbench/session.py`, `local_session.py`, `records.py`, `api.py`, `__main__.py` | The sessions that drive and reopen runs |
| `acceptance/local.py`, `runtime.py`, `reader.py` | The fixture modules the synthetic session is built on |
| The experiment directory the run was frozen from | Profile, setup, tool modules, evaluator, researcher program |
| The run's bundle | The frozen profile and artifacts the core reads |

| Out | Why |
| --- | --- |
| `tests/`, `isolation/`, `build_support/`, the workbench pages, other experiment directories, every document | They do not run during execution or recovery. They stay in the build identity, which still names the build in every bundle and report |

Beside the inventory, `environment.json` records the installed Python
version and the installed version of each package the experiment directory
declares in `dependencies.json`. On reopen both are compared with what is
installed now. A difference opens the run read-only with
`ENVIRONMENT_CHANGED` and the name of what differs. Bundles frozen before
this existed fall back to the full inventory.

## 6. Two corrections carried into the documents

- A setup generator supplies administrative defaults. It cannot invent a
  meaningful scientific evaluator. Step 3 and the report say which part
  was generated and which part was written.
- The accepted record is protected by refusing the researcher's designated
  identity. In the local arrangement every token sits in one process, so
  "the researcher's process cannot write to it" overstates the protection.
  The adoption review carries a dated correction to that sentence.

## 7. Tests

- The generator produces the three files for both existing examples byte
  for byte, so nothing regresses while it is factored out.
- The candidate rule: same conclusion, different history, different
  candidate set; a rejected candidate returns when its condition is met;
  the evaluator refuses a selection whose candidate set does not match the
  history it cites.
- The interruption in step 6 on the real script, through the workbench
  session, with records compared before and after reopen.
- The existing suites, unchanged in their assertions.

## 8. Limits to state in the report

No model provider. One script, chosen by the Principal, which may not
represent other scripts. The evaluator checks reproducibility and order,
not method. Measurements are from one person on one machine. The host
still runs from the checkout.
