# Implementation Report - A Thin Integration Layer for One Analysis

Status: **IMPLEMENTATION RECORD OF DISPOSABLE DEVELOPMENT. CV1 UNCHANGED. CONSTITUTIONAL DELTA 0/0/0. NO REAL PROVIDER OR SPENDING.**

Date: 2026-11-01. Implements the
[integration-layer plan](../plans/analysis_integration_layer_20261101.md),
which followed the Principal's two reviews of the
[signal-groups report](signal_groups_20261101.md).

## 1. What changed

The 295 hand-written lines that connected the 55-line script were sorted
by responsibility. The plumbing that is the same for every analysis
moved into the client as `arh_client.analysis`. The example kept its
decisions. The command line takes a user's own CSV and records it as a
historical document. The demonstration and test code is in files of its
own and labelled.

| Responsibility | Where | Lines |
| --- | --- | --- |
| Plumbing, written once | `client/arh_client/analysis.py` | 275 |
| The experiment's decisions | `tool.py` 13, `candidates.py` 23, `researcher.py` 13, `evaluator.py` 20 | 69 |
| The setup description | `make_setup.py` | 49 |
| The command line and the per-process job | `__main__.py` 149, `job.py` 28 | 177 |
| Demonstration and test code | `demo.py` 127, `make_data.py` 30 | 157 |
| The script | `signal_groups.py`, unchanged | 55 |

What a second analysis writes is the 69 lines of decisions and a setup
description. The analysis function returns a dict with `metric` and `n`.
The candidate table says what to investigate next by conclusion state.
The recompute function says what counts as a valid result. The setup
description names the identities, the source and its class, the tool and
its cost, the tariff and the budget. The command line and the job can
be used as they are. `examples/signal_groups/README.md` lists this.

The client module reads the step, the tool, its parameters, the source
and the umbrella Theme from the frozen profile. The example names none
of them in code. The researcher is a subclass that sets the rule and
the analysis kind. The evaluator is the recompute function and one
call.

Two small changes outside the example and the client. The host puts the
client directory on the tool worker's import path, so a tool module the
host runs may use `host_tool`; the core process is unchanged, three
lines in `adaptive_research_harness/local_host.py`. A run directory may
already hold a `setup/` directory written for it before the run is
created, one line in `workbench/local_session.py`.

## 2. The own-CSV run

```sh
python3 -m examples.signal_groups --csv my_table.csv --signal sig --outcome out_bp --expect ">= 30" --minimum-n 10 --origin "exported from my notebook on 2026-10-31"
```

On a twelve-row table typed by hand. The run was created on a setup
whose source is declared historical, written into the run directory.
The file was recorded with its content hash and the given origin, class
historical. The design with the expectation was recorded before any
attempt. The host ran the analysis, the receipt was registered, the
charge settled, and the spread equalled the direct run. The candidates
came from the declared rule. The selection was recorded with the two
rejected candidates and their reconsideration conditions, proposed as
the next direction and checked, PASS. The Principal's admission was
recorded and applied, N 6, direction TH-S1. A further design under the
new direction ran over the same document. The whole loop is in
`tests/integration/test_signal_groups.py`, which also reopens the run
between commands and confirms the demonstration hook is not on this
path. The run took about one second per command, most of it startup.

The Principal's own question has not been run. That is theirs to do,
with a table of their own. Nothing here manufactures a negative result.

## 3. Verification

| Suite | Result |
| --- | --- |
| Unit, component, workbench and integration tests | 92 tests OK |
| Acceptance | 77 cases PASS, no failures, after a first run that three cases failed with `SOURCE_CHANGED_DURING_RUN` because BUILD.md was edited while it ran |
| The demonstration | PASS, retained as `demo-20261101-signal-groups`, regenerated on the sorted code; the earlier run is in git history at `9f722b2` |
| The command line on a hand-typed table | the output in runbook path G |

The client module imports the standard library and its own package
only, asserted by a test. The regenerated setup files for the example are
byte-identical to the committed ones; only the tool module bytes changed,
which is why the retained run was regenerated.

## 4. Limits

The lines are sorted, not removed. A second analysis still writes its
decisions and a setup description, and the setup description is mostly
prose the generator turns into grants and declarations. The command line
is the example's; a team with its own interface would call
`AnalysisResearcher` directly. The host puts the client on the tool
worker's path by convention; a tool module that imports anything else
must declare it in `dependencies.json`. No person was timed.

## 5. Files

New: `client/arh_client/analysis.py`, `examples/signal_groups/demo.py`,
`examples/signal_groups/README.md`, the plan and this report. Changed:
`examples/signal_groups/` (`__main__.py`, `tool.py`, `candidates.py`,
`researcher.py`, `evaluator.py`, `job.py`, `make_setup.py`),
`adaptive_research_harness/local_host.py`, `workbench/local_session.py`,
`client/arh_client/__init__.py`, `client/README.md`, `runbook.md`,
`BUILD.md`, `README.md`, `tests/integration/test_signal_groups.py`.
