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
- **P2, what reopen identity covers.** Today a retained run reopens live
  only when every file in its bundle inventory matches the tree, and the
  inventory covers tests, documents and the workbench as well as the core.
  This plan proposes that live eligibility rest on an execution identity:
  the core package, the experiment directory, the bundle, and the declared
  dependencies named in section 5. The full inventory is still recorded
  and still names the build. Because `BUILD.md` states what identity
  covers, the Principal decides this before step 4.

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
   checks reproducibility and order. It makes no judgment about whether
   the method is sound, and the report says so.
4. **Run it and keep a failure.** Import the data, record the expectation,
   run, and let the first expectation fail or a first variant fall short.
   The failed result and its conclusion stay on the ledger.
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
7. **Measure.** Lines added to the script, lines in the experiment
   directory, minutes from first command to the first admitted direction,
   and the list of concepts the Principal had to touch. These go in the
   report beside the baseline from step 1.

## 4. Changes to the code, in order

| Step | Change | Where |
| --- | --- | --- |
| 3 | Setup generator with administrative defaults, factored from the two `make_setup.py` scripts; the two examples become callers of it | `client/arh_client/setup.py`, `examples/langgraph_headlines/make_setup.py`, `experiments/local_documents/make_setup.py` |
| 3 | A reproducibility evaluator for a host-run or caller-executed script, written per script on the toolkit's `validate_motivation` hook | the new experiment directory |
| 5 | Candidate rule reads history; rejected candidates carry reason and reconsideration condition; selection records cite the history they used | `experiments/local_documents/researcher.py` and its evaluator, or the new experiment's researcher if the script lives there |
| 6 | Nothing new. The host, the client's `Execution.run` and the workbench session already do this; the step verifies it on this script | `tests/integration/` |
| after P2 | Live reopen decided on the execution identity; the full inventory kept as the build identity | `workbench/session.inventory_matches`, `build_support/freeze.py`, `BUILD.md` |

Deferred: packaging the host so it runs outside the checkout (R2). The
immediate irritation is unrelated edits preventing reopen, which P2
addresses. A general setup framework is not built; the generator does
only what this script needed.

## 5. The execution identity, proposed for P2

Files whose change should turn an earlier run read-only: everything under
`adaptive_research_harness/`, the experiment directory the run was frozen
from, the run's bundle, and a declared dependency list in the experiment
directory naming the Python version and any package the tool or evaluator
imports with its version. Files whose change should not: `tests/`,
`workbench/`, `acceptance/`, `isolation/`, `build_support/`, `experiments/`
other than the run's own, and every document. The full inventory, with
all of these, remains the build identity recorded in every bundle and
report.

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
