# A Thin Integration Layer for One Analysis - Plan

Status: **PLAN. PROPOSES ORDER AND SCOPE. AUTHORIZES NOTHING. CV1 UNCHANGED. CONSTITUTIONAL DELTA 0/0/0.**

Date: 2026-11-01. Follows the
[signal-groups report](../implementation/signal_groups_20261101.md) and
the Principal's two reviews of it, forwarded the same day. The reviews
are the audit for this plan.

## 1. What the reviews found

The signal-groups example shows the integration works. The calculation
stayed unchanged, recorded history affected later choices, and an
interrupted attempt reused the receipt the host held. It also exposes the
adoption problem. Connecting a 55-line script took 295 hand-written
lines, and a second user should not have to reproduce them. Neither the
automated run time nor the agent's build time says anything about ease
of adoption.

The direction given. A thin integration layer, extending `arh_client`,
no new service or framework. A user supplies their analysis function,
their inputs, a budget and an evaluation function. The client handles
reservations, execution, receipts, settlement and recovery. The
researcher still decides what to investigate. The evaluator still
defines what counts as a valid result. The 295 lines are to be sorted
into those responsibilities, with the repeated plumbing moved into the
client and the experiment-specific decisions kept in the example. Some
lines are demonstration and test code ordinary users never need, and
should be labelled so. Then the runner should accept the Principal's own
CSV, column names and expectation, recording the input as historical,
and the documents should say exactly what a second user must supply.
There is no need to manufacture a negative result.

## 2. The sort

Every hand-written line in `examples/signal_groups/` goes to one of
four places.

| Responsibility | Where it lives after this plan | What it holds |
| --- | --- | --- |
| Plumbing that is the same for every analysis | `client/arh_client/analysis.py`, new | The design record with its expectation; reserve, attempt, execute, receipt, record with conclusion, settle, close; keys persisted so a re-run resumes; the candidate rule machinery over the history; the selection record with rejections; the Theme proposal; the host-tool wrapper; the evaluator's record checks |
| The experiment's decisions | `examples/signal_groups/` | The analysis function; the candidate table; the recompute function that says what a valid result is; the setup description with its budget |
| The command line a user runs | `examples/signal_groups/__main__.py` | Own CSV in, expectation recorded, analysis run, candidates shown; selection, proposal, check; the Principal's decision; the run shown |
| Demonstration and test code | `examples/signal_groups/demo.py`, `job.py`, `make_data.py` | The timed experience, the crash point, the generated data |

The client module reads the step, tool, parameters, source and umbrella
Theme from the frozen profile, so an experiment names none of them in
code.

## 3. Changes, in order

1. `client/arh_client/analysis.py`. `compare` and `conclude` for exact
   expectation comparison. `CandidateRule(table)` with `live_set` and
   `gather_history`. `AnalysisResearcher(connection, rule)` with
   `design`, `run`, `candidates`, `select`, `propose`. `host_tool(analysis)`
   returning the `calculate(inputs)` a host-run tool exports.
   `evaluator(recompute, rule)` returning the Checker's `evaluate`.
   `persisted_keys(path)`. Standard library and the package only.
2. `adaptive_research_harness/local_host.py`. Tool workers get the
   client directory on their import path, so a tool module may import
   `arh_client.analysis`. One line. The core process is unchanged.
3. `workbench/local_session.py`. A run directory may already hold a
   `setup/` directory written for it before the run is created.
4. The example re-sorted as the table says. `tool.py` becomes the
   analysis function and one call. `candidates.py` becomes the table.
   `researcher.py` becomes a subclass naming its rule and analysis
   kind. `evaluator.py` becomes `recompute` and one call. `job.py` keeps
   the process entry with its crash point. `make_setup.py` writes
   either the synthetic setup for the generated data or a historical
   setup for the Principal's own files. `demo.py` takes the
   demonstration. `__main__.py` becomes the command line.
5. The command line. `--csv`, `--signal`, `--outcome`, `--groups`,
   `--expect`, `--minimum-n` create a run on a historical setup written
   into the run directory, import the file with its origin, record the
   expectation, run the analysis and print the result, the conclusion
   and the candidates. `--run NAME` continues a run. `--choose`,
   `--reason` and `--next` record the selection, propose it and run the
   check. `--admit` or `--reject` record the Principal's decision.
   `--run NAME` alone shows the run. Every record is the same client
   operation the demonstration makes.
6. Documents. `examples/signal_groups/README.md` says what a second
   user supplies and what the client supplies. The client README gains
   the module. Runbook path G, BUILD.md and the README bullet follow.
   An implementation report with the sorted line counts and the own-CSV
   run.

## 4. Tests

- The candidate rule through the client, including reinstatement under
  each condition and the always-available choice.
- The demonstration unchanged in what it checks, now from `demo.py`.
- The command line on a CSV end to end: the run created on a historical
  setup, the document recorded historical with its origin, the
  expectation before the attempt, the result equal to the direct run,
  the candidates shown, a selection proposed and checked, the Principal's
  admission applied, the run shown after reopening.
- The client module imports nothing outside the standard library and
  the package.

## 5. Limits to state

The 295 lines are sorted, not removed. Lines that are decisions of the
experiment remain the experiment's. The own-CSV run is the Principal's
to perform with a question they want answered. This plan does not run
it for them and does not time a person.
