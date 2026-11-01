# Signal groups through ARH

A 55-line CSV analysis, `signal_groups.py`, connected to ARH. The
calculation is the script's own and was not changed. This is a new
example on generated data, not an adopted workflow. The same files take
your own CSV through the command line, recorded as a historical document
with the origin you give.

## What you supply, for your own analysis

Four things. Everything else is the client's.

| You write | File here | Lines | What it is |
| --- | --- | --- | --- |
| The analysis function | `tool.py` | 13 | `analysis(rows, spec)` returns a dict with `metric`, the value the expectation compares, and `n`, the rows used. One call, `host_tool(analysis, kind=...)`, makes it the `calculate` the host runs |
| The candidate table | `candidates.py` | 23 | What to investigate next, by conclusion state, each with the condition under which a rejected candidate comes back |
| The evaluation function | `evaluator.py` | 20 | `recompute(rows, spec, result)` says whether the recorded result is what the analysis gives on the committed rows. One call, `evaluator(recompute, RULE, kind=...)`, makes the Checker's `evaluate` |
| The setup description | `make_setup.py` | 49 | Identities, the source and its class, the tool and its cost, the tariff, the budget, the entry points. The client's generator writes the three JSON files from it |

The researcher, `researcher.py`, is a subclass naming the rule and the
analysis kind. The inputs are the files you import and the design that
names the columns and the expectation. The budget is in the setup
description.

## What the client supplies

`arh_client.analysis`, 275 lines, written once. The design record with
its expectation. Reservation, attempt, execution, receipt, the record
with its conclusion, settlement and closure. Keys persisted so a killed
run resumes rather than repeats. The candidate rule over the history.
The selection record with its rejections. The Theme proposal. The host
tool wrapper. The record checks an evaluator makes before your
recomputation. The step, tool, parameters, source and umbrella Theme are
read from the frozen profile, so your code names none of them.

## Your own CSV

From the repository root, with the client importable.

```sh
python3 -m examples.signal_groups --csv my_table.csv --signal sig --outcome out_bp --expect ">= 30" --minimum-n 10 --origin "exported from my notebook on 2026-10-31"
```

This creates a run whose source is declared historical, writes its setup
into the run directory, imports the file with its content hash and your
origin, records the question and the expectation as a design before any
attempt, lets the host run the analysis, settles the charge and prints
the result, the conclusion and the candidates for the next
investigation. Then, on the same run,

```sh
python3 -m examples.signal_groups --run RUN --choose placebo-signal --reason "why" --next "the next question"
python3 -m examples.signal_groups --run RUN --admit TR-...        # or --reject TR-... --reason "why"
python3 -m examples.signal_groups --run RUN --signal sig2 --outcome out_bp --expect "< 10"
python3 -m examples.signal_groups --run RUN
```

The first records the selection with the rejected candidates and their
reconsideration conditions, proposes it as the next direction and runs
the independent check. The second records your decision and, on
admission, applies it. The third records another design under the new
direction and runs it, over every document in the run, with `--csv` to
import more first and `--revises SEQ` to mark a revision. The last shows
the run. Each run also opens on the workbench's local page. Records are
under `artifacts/development/workbench/RUN`.

Columns must hold integers, basis points for the outcome. Values in
`--expect` are integers or exact ratios such as `1/2`.

## The demonstration

`python3 -m examples.signal_groups.demo` runs the whole experience on
the generated data and times it. `job.py` runs one design in its own
process with persisted keys and a crash point for the tests. `make_data.py`
generates the data. None of these is needed to run your own table.

## Files

| Group | Files | Lines |
| --- | --- | --- |
| The script | `signal_groups.py` | 55 |
| Your decisions | `tool.py`, `candidates.py`, `researcher.py`, `evaluator.py` | 69 |
| Setup description | `make_setup.py` | 49 |
| Command line and job | `__main__.py`, `job.py` | 177 |
| Demonstration | `demo.py`, `make_data.py` | 157 |
| Generated | `setup.json`, `designs_and_methods.json`, `experiment.json` | |
