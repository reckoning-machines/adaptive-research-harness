# Runbook

Verified steps for operating Adaptive Research Harness, ARH, on one machine.
The [README](README.md) says what it is for, the
[architecture](architecture.md) says how it works, and the
[client README](client/README.md) documents each Python operation. Every
command below was run on macOS with Python 3.12.3 on 2026-11-01 against
the current tree. Anything not exercised is marked.

## Prerequisites

| Need | Detail |
| --- | --- |
| Python | 3.12 from a standard distribution. ARH uses only the standard library |
| Operating system | macOS or Linux. No virtual machine, no container |
| Working directory | The repository root for every harness command. The client runs from anywhere |
| Environment | `PYTHONDONTWRITEBYTECODE=1` on each harness command so no bytecode is written next to the covered source. The examples include it |
| For the LangGraph paths | A virtual environment with the client and its `langgraph` extra, as in path C |

Every run is disposable development. The examples in paths A to E use
synthetic data. Path F uses files you supply, recorded as historical
material. Charges are simulated units, nothing outside the machine is
contacted, and nothing earns forward standing.

## Where run records are stored

| Path | What it is | Who runs |
| --- | --- | --- |
| `artifacts/development/latest/<run>/` | Synthetic example and acceptance reports, one directory per invocation | `acceptance.local` |
| `artifacts/development/workbench/<run>/` | Workbench runs, bundle and state kept in place | `workbench` |
| `artifacts/development/langgraph/<stamp>/` | LangGraph example runs, with `report.json`, the host state, the provider's records and the researcher's checkpoints and receipts | the example runner |
| `artifacts/development/run-bundles/<id>/bundle/` | Disposable bundles frozen by tests and fixtures | tests |
| `artifacts/development/builds/<inventory>/` | One snapshot of the covered source per build identity | every freeze |
| The directory you pass as `--run` | A host you start yourself, with `bundle/` and `state/` | path D |

Inside a host's `state/` are `harness.sqlite`, the two ledgers in one
database, `clock.json`, the synthetic clock, `connection.json` while the
host is up, `supervisor/`, the quiescence proofs, and the process logs.

## A. The synthetic example

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m acceptance.local --example
```

It prints the inventory digest, the run directory, `E01 PASS` and the
worked example, ending with the retained evidence references and the next
planned action, and takes about ten seconds. This path uses the built-in researcher
and the two tools ARH runs itself. It does not use the client.

## B. The workbench

The workbench runs the synthetic cycle on one page. It does not run the
LangGraph example or an external researcher.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m workbench --port 8765
```

Open `http://127.0.0.1:8765/` on the same machine. Choose one of the three
synthetic cohorts and press Start. The page offers one step at a time,
each an existing actor operation or Principal command that the core
admits or refuses. Close run stops the processes and keeps the state.
Opening a listed run continues it when the source still matches its
inventory, and otherwise opens it read-only. Ctrl-C closes every live run.

The same cycle runs headless and prints what happened.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m workbench --demo
```

Expected ending, with your own run names and about thirty seconds.

```
reopened demo-...-control-survives-interrupted as live; next permitted = run-next-experiment
continued with 6 steps to complete, N=17; researcher attempts=2; AU-RP-1 committed=2.00; earlier records unchanged=True
copy with a differing build: read-only (ARTIFACT_CHANGED ...); reader RECONSTRUCTED
DEMO PASS
```

## C. The LangGraph example

Create the environment once, then run the example from the repository root.

```sh
python3 -m venv .venv && .venv/bin/pip install -e './client[langgraph]'
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m examples.langgraph_headlines
```

The run takes about ten seconds and prints the following, with sequence
numbers that differ from run to run.

```
Experiment HEADLINE-SENT-1 on build ... host .../state
Trust: one host holds every token; the researcher reports its own receipts for FAKE-LLM-1 (accounting, not enforcement); no OS isolation.
  ok   startup through checked controls: N=5, 5 checks PASS by AD-CK-H1.0
  ok   classification recorded and settled: E26 labels 12 bullish / 12 bearish of 24, cost 0.48, provider calls 1
  ok   returns document committed one period later: ...
  ok   overstated count fails the independent Check and is not admitted: ...
  ok   researcher cannot approve its own proposal or change its rules: ...
  ok   honest proposal passes Check, P-1 admits, Apply registers: ... N=6
  ok   over-budget work refused before the provider runs: ...
  ok   killed after the durable receipt: resumed, no second provider call: ...
  ok   replaying the successful claim request grants no permission: tool-run again -> RECEIPT
  ok   killed after the provider completed, before the receipt: recovered by lookup under the original claim: ...
  ok   killed with no record anywhere: reconciled at the maximum, liability kept, no second call: ...
  ok   replacement refused until the caller is gone and the provider operation is cancelled: ...
  ok   replacement attempt executed once and settled: ...
Budgets: AU-RH-1 committed 2.40 of 3.00; AU-CK-H committed 1.75 ; pending attempts []
Result: PASS | research is synthetic and earns no forward standing; the Check verified the join and the arithmetic, not the labels.
```

Records land under `artifacts/development/langgraph/<stamp>/`. The runner
starts and stops its own host.

To run it from outside the checkout, copy the example directory anywhere,
install the client in that environment, and point it at the checkout.

```sh
cp -R /path/to/speedway/examples/langgraph_headlines ~/work/langgraph_headlines
cd ~/work && python3 -m venv venv && ./venv/bin/pip install '/path/to/speedway/client[langgraph]'
./venv/bin/python -m langgraph_headlines --harness /path/to/speedway --run ~/work/run
```

The host still runs inside the checkout. The example imports only
`arh_client`.

## D. Your own researcher against a separately started host

Three processes under three identities. The host runs from the checkout.
The others run wherever the client is installed.

**1. Start a host.** From the repository root, against your experiment
directory. The headline example's directory is used here.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m adaptive_research_harness.local_host --setup examples/langgraph_headlines --run /tmp/arh-run
```

Expected output, then the process stays up until Ctrl-C.

```
<inventory digest>
connection /tmp/arh-run/state/connection.json
```

The connection file holds the socket, the host's control socket and one
token per identity. Anyone who can read it can act as any identity, so
treat it as a credential and keep it private.

**2. Install the client** in the environment your researcher uses.

```sh
pip install '/path/to/speedway/client[langgraph]'
```

**3. Run startup once per run directory.** Genesis and the startup
transitions the setup declares, each checked by your evaluator. Run this
from the directory holding a copy of the example package, or adapt the
import to your evaluator.

```python
from arh_client import connect, Principal, Observer, Checker, startup, HostControl
from langgraph_headlines.evaluator import recompute

conn = '/tmp/arh-run/state/connection.json'
checker = Checker(connect(conn, 'AD-CK-H1.0'), recompute=recompute)
def check(tr):
    r = checker.check(tr); assert r.result == 'PASS', r.criteria; return r.check_sequence
result = startup(Principal(connect(conn, 'Principal')), Observer(connect(conn, 'Observation function')), check, tick=HostControl.from_file(conn).tick)
print(result['N'])   # 5 for the headline setup
```

Running it a second time on the same run directory is refused at genesis
with `GENESIS_SCOPE`, because the ledgers are no longer empty. That is the
signal that startup already happened.

**4. Run your researcher** under the researcher identity. The example's
researcher is a complete LangGraph program.

```sh
python -m langgraph_headlines.researcher --connection /tmp/arh-run/state/connection.json --run-dir /tmp/arh-run/work --job job-1 --mode classify
```

It prints the final graph state as JSON, with `status`, `attempt`,
`receipt`, `record`, `settlement` and `provider_calls`. The getting
started section of the [client README](client/README.md) shows the same
sequence written directly against `Researcher` and `Execution`.

**5. Advance the clock, commit later data, join and propose.** The returns
document is available one synthetic day later.

```python
from arh_client import connect, Observer, HostControl
import json
conn = '/tmp/arh-run/state/connection.json'
HostControl.from_file(conn).tick(86400000 + 1000)
content = json.load(open('langgraph_headlines/designs_and_methods.json'))['returns_cohort']['content']
Observer(connect(conn, 'Observation function')).observe('SRC-RET-SYN', content, '2026-10-29')
```

```sh
python -m langgraph_headlines.researcher --connection /tmp/arh-run/state/connection.json --run-dir /tmp/arh-run/work --job job-1-join --mode join --options '{"labels_record": <the record ref printed by job-1>}'
```

**6. Check and decide** under the Checker and Principal identities.

```sh
python -m langgraph_headlines.check --connection /tmp/arh-run/state/connection.json --transition <transition id printed by the join job>
```

```python
from arh_client import connect, Principal
p = Principal(connect('/tmp/arh-run/state/connection.json', 'Principal'))
d = p.policy_decide('<transition id>', <check_sequence from the check output>)
a = p.apply('<transition id>', d.sequence)
print(d, a, p.c.state()['N'])
```

Steps 1 to 4 and the stop and reopen sequence in path E were run from a
copy outside the checkout on 2026-11-01. Steps 5 and 6 are what the
example runner does in process; they were not run by hand as separate
commands.

## E. Stop, reopen and recover a run

Three different situations. Keep them apart so nothing is executed twice.

**Stopping.** Ctrl-C in the host's terminal, or from any client
environment.

```python
from arh_client import HostControl
HostControl.from_file('/tmp/arh-run/state/connection.json').stop()
```

The host kills its workers and removes `connection.json`. Every record
stays in `/tmp/arh-run/state/`. A researcher killed mid-attempt leaves a
pending attempt on the ledger, which `obligations()` lists.

**Reopening, which is only reconnecting.** Start the host again with the
same `--run` directory. It freezes nothing new, rebuilds its views from the
ledgers and writes a new `connection.json` with new tokens. Reconnect every
process with the new file. Reopening does not run anything again.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m adaptive_research_harness.local_host --setup examples/langgraph_headlines --run /tmp/arh-run
```

If a file that takes part in execution or recovery changed since the
bundle was frozen, the core refuses to start with `ARTIFACT_CHANGED` and
names the file; a changed Python or declared package version refuses with
`ENVIRONMENT_CHANGED`. The run can still be read. Freeze a new run
directory for new work. Edits to tests or documents do not affect it.

**Recovering an existing attempt.** Re-run the same researcher job with the
same `--job` name. The graph resumes from its checkpoint and the execute
node asks the core for permission again. The core answers without
permission for an attempt it already claimed, and the client then looks in
the researcher's receipt store, then in the provider's own record, and
reports one of these in the printed `execution` field.

| execution | Meaning | Provider calls |
| --- | --- | --- |
| `resumed` | the receipt was durable before the crash | none |
| `recovered` | the provider had recorded the operation | none |
| `uncertain` | no record anywhere, the work may have run or may still be running | none. The job settles at the maximum and records the loss |

Verified on 2026-11-01 with a job killed before the provider recorded
anything, the host stopped and reopened, and the job re-run. It printed
`status reconciled, execution uncertain, provider_calls 1`, the budget
showed the maximum committed, and `obligations()` showed no pending
attempt afterwards.

**Authorizing new work for the same inputs.** Only after the earlier
attempt is settled. A retry is a new attempt and a new claim, and the core
admits it only with evidence that the earlier work can no longer execute.

```python
from arh_client import connect, Researcher, Principal, HostControl, Connection
conn = '/tmp/arh-run/state/connection.json'
r = Researcher(connect(conn, 'AD-RH1.0')); p = Principal(connect(conn, 'Principal')); control = HostControl.from_file(conn)
claim = [c for c in p.dispatch_status()['claims'] if c['receipt'] is None][-1]   # the attempt that never produced a receipt
attempt, generation = claim['attempt'], claim['claim']['worker']                  # the process that held the permission
print(r.retry(attempt, Connection.new_key()))                                     # REFUSED WORKER_NOT_QUIESCENT
control.quiesce(generation)                                                       # refused unless that process id is gone
print(r.retry(attempt, Connection.new_key()))                                     # still refused, the provider may still be working
disposition = my_provider.cancel(attempt, claim['claim']['input_hash'])           # ask the provider, your code
control.quiesce(generation, {str(attempt): disposition})                          # CANCELLED or COMPLETED, bound to the claim
print(r.retry(attempt, Connection.new_key()))                                     # COMMITTED, a new attempt with the next dispatch index
```

Then execute the new attempt with `Execution.run` as usual. Verified on
2026-11-01 across a host restart. The generation recorded in the claim
belongs to the earlier host incarnation, and the proof is accepted on the
process id being gone.

## F. Your own documents

Run ARH on files you have. Documents keep their provenance and are
classed historical. Nothing in this path predicts anything. It records what
you expected, what the documents showed, and what you decided to do next.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m workbench --port 8765
```

Open `http://127.0.0.1:8765/local`. The page at `/` is the synthetic cycle
and does not run this path.

**1. Start.** Write the question you are investigating and press Start.
That text is committed as the first document and the direction `TH-L0`
cites it. Startup takes a few seconds and ends at N=5.

**2. Import.** Choose files, say where they came from, press Import. Text,
markdown, CSV, TSV and JSON rows work, and PDF files are not read. Each
file is recorded
with its name, content hash, size, type, your stated origin and the time
of receipt. Importing the same bytes twice gives the same item.

**3. Say what you expect, then run.** Fill in the question, the expectation
as a sentence, a comparator with a number or a fraction, the minimum
number of documents, the analysis and the documents, then Commit the
design. This is written down before anything runs and costs nothing.
Then press Run, and the researcher reserves 0.10 units per document,
records the attempt, and the calculator ARH runs does the work.
You get the metric, the count, and MET, NOT_MET or INCONCLUSIVE against
your expectation.

Two analyses exist. `term-count` is the fraction of text documents that
contain any of the terms you list. `table-stat` is a count, ratio, sum or
mean over rows that pass the filters you give.

**4. Pick the next question.** The page lists candidates that follow from
the conclusion. These come from a fixed rule in the researcher program: a
met expectation offers extend, sharpen or alternative explanation; a
failed one offers revise the expectation, change the analysis or reject;
too few documents offers add documents or relax the minimum. Pick one,
say why, and write the next question. Your choice and the ones you
rejected are recorded.

**5. Propose, check, decide.** The chosen question is proposed as a
direction. The evaluator, running under its own identity, recomputes the
analysis from the committed files and design with separate code and
checks the conclusion, the order of design before attempt, the
settlement and the selection. After a passing check you admit or reject.
A rejected direction stays on the record. An admitted one is applied.

**6. Revise.** A new design can name the design it revises and run under
an admitted direction. Both designs and both results stay.

**Stop and reopen.** Close run keeps everything under
`artifacts/development/workbench/<run>/`. Open it from the list to carry
on from the same next step, and nothing that already ran will run again.
It opens read-only when a file that takes part in running or recovering
it has changed since the run was frozen, or when the installed Python or a
declared package version differs. Edits to tests or documents do not
affect it.

After the first cycle you should see N=6, directions `TH-L0, TH-L1`,
`AU-RL-1` committed 0.30 for three documents, no pending attempts. The
retained run `demo-20261101-072344-local-memos` on the page has three
memos and a trade table, one admitted direction, and a second
investigation waiting at step 4.

Verified on 2026-11-01 through the session and the HTTP routes, including
a forged conclusion failing its check and a closed run reopened with
identical records. The page was not driven in a browser.

Not in this path: the receipt time you declare is provenance, not a system
clock. The independent reader covers the synthetic experiment only.

## G. A script through ARH, and your own CSV: the signal-groups example

A new example, not an adopted workflow. A 55-line script,
`examples/signal_groups/signal_groups.py`, compares a forward return across
signal groups in a CSV. It runs on its own and knows nothing about ARH.
Four short files connect it, and the same files take your own table.
`examples/signal_groups/README.md` lists exactly what a second analysis
must supply.

Run the script directly first.

```sh
python3 examples/signal_groups/signal_groups.py examples/signal_groups/data/signals.csv --signal mom_20 --outcome fwd_5d_bp --groups 3
```

### Your own CSV

From the repository root, with the client importable. The columns must
hold integers, basis points for the outcome.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m examples.signal_groups --csv my_table.csv --signal sig --outcome out_bp --expect ">= 30" --minimum-n 10 --origin "exported from my notebook on 2026-10-31"
```

The first line printed is the build identity of the bundle frozen for
the run. Then, on a twelve-row table typed by hand:

```
Created run 20261101-120000-signal-own in 0.6 s; source declared historical; budget 100.00 units
Imported my_table.csv as E22: 12 rows, class historical, sha256 f560f905d4607619, origin exported from my notebook on 2026-10-31
Recorded design E23 under TH-S0 before any attempt: Does sig separate out_bp across 3 groups? Expectation: sig top group minus bottom group of out_bp >= 30 bp, min n 10
Host ran the analysis, execution registered, settled True, record E26
group  rows  signal range      mean bp   hit rate
    1     4     -30 .. -15        -18.8    0.25
    2     4     -10 .. 5            2.5    0.50
    3     4      10 .. 25          32.5    1.00
spread top minus bottom: 51.2 bp over 12 rows (0 skipped) | conclusion MET
Candidates for the next investigation, by the declared rule:
  other-horizon: Does the spread hold for a different outcome horizon? (One horizon is one view of the same signal.)
  finer-groups: Is the spread carried by the extremes or spread across the ranking? (Terciles hide where the relation lives.)
  placebo-signal: Does a signal that should carry nothing show a spread of the same size? (A spread the placebo also shows is not evidence for the signal.)
Choose one: python3 -m examples.signal_groups --run 20261101-120000-signal-own --choose ID --reason "why" --next "the next question"
```

The run's source is declared historical, its setup is written into the
run directory, and the file is recorded with its content hash and the
origin you gave. The expectation is on the record as a design before
any attempt. The host runs the analysis, the charge is settled, and the
candidates come from the researcher's declared rule. Continue on the
same run.

```sh
.venv/bin/python -m examples.signal_groups --run RUN --choose placebo-signal --reason "a spread the placebo shows too would mean nothing" --next "Does a column that should carry nothing show the same spread?"
```

```
Recorded selection E29: placebo-signal; rejected other-horizon (until new_documents), finer-groups (until new_documents)
Proposed TR-... as the next direction; independent check PASS
Decide: python3 -m examples.signal_groups --run RUN --admit TR-...   or   --reject TR-... --reason "why"
```

```sh
.venv/bin/python -m examples.signal_groups --run RUN --admit TR-... --reason "placebo first"
```

```
TR-... admitted and applied: True; N = 6; direction now TH-S1
```

Then another design under the new direction, over every document in
the run, with `--csv` to import more rows first and `--revises SEQ` to
mark a revision, and `--run RUN` alone to show the run.

```sh
.venv/bin/python -m examples.signal_groups --run RUN --signal vol --outcome out_bp --expect "< 10"
.venv/bin/python -m examples.signal_groups --run RUN
```

Each command opens the run, makes its records and closes it. A run that
no longer reopens live, because the execution files or the environment
changed, is reported read-only with the reason. The run is listed on the
workbench page and opens on its local page like any local run. Records
are under `artifacts/development/workbench/RUN/`.

### The demonstration on generated data

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m examples.signal_groups.demo
```

It prints the baseline, then each step: startup, the table imported with
its hash, the expectation recorded before the analysis, the host-run
analysis giving the same spread as the direct run, the candidates the
conclusion produced, the selection with the rejected candidates and the
condition under which each would be reconsidered, the independent check
and the decision, a placebo investigation whose candidate set is shaped by
the first selection, new rows reinstating the held-back candidates, and an
attempt interrupted after the host ran the tool, then resumed after the
run is closed and reopened, without running again. The last lines give
line counts and timings. Expected ending:

```
  ok   interrupted attempt resumed without running again: execution registered, ...
Lines: script 55 | experiment-specific 69 | setup 49 | command line and job 177 | demonstration 157 | client analysis module 275
Timings: {...}
Result: PASS | new example on generated data; the calculation is the script's own; no forward standing.
```

The retained run `demo-20261101-signal-groups` is under the workbench
directory. To run one design in its own process with persisted keys, so
a re-run resumes rather than repeats, use the job the demonstration uses:

```sh
.venv/bin/python -m examples.signal_groups.job --connection <run>/state/connection.json --work <run>/work --design <design sequence>
```

### What is whose

The experiment's decisions are `tool.py` (the analysis function),
`candidates.py` (the table), `researcher.py` (the rule and the analysis
kind) and `evaluator.py` (the recompute function), 69 lines together.
`project.json` is the setup description the generator writes the JSON
from, and `make_setup.py` is the call. `arh_client.analysis` holds the lifecycle, the candidate machinery,
the host-tool wrapper and the evaluator's record checks. The evaluator
checks reproducibility and record integrity, not the research method.

Verified on 2026-11-01 through the demonstration, the command line on a
hand-typed table and the integration test. A person following this path
by hand was not timed.

## H. Research code and LangGraph on the everyday interface: the memo-returns example

A two-source analysis through LangGraph where the scientist wrote the
research and the client handled the lifecycle. Six analyst memos are
scored for tone, one metered call each; the scores are joined to a
returns table in two parallel branches, the real next-day column and a
placebo prior-day column; the scientist's own next question is proposed;
the graph waits for an independent check and the Principal's decision.
Generated data, labelled synthetic. `examples/memo_returns/README.md`
lists what was written and what the client did.

### One command up

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m arh_client.dev up examples/memo_returns --run /tmp/arh-memo
```

It writes the setup files from `project.json` if they are missing,
freezes a bundle into the run directory, starts the host, runs the
startup sequence under the Principal, Observation and Checker
identities and prints the connection file, then stays up until Ctrl-C
or `python3 -m arh_client.dev down /tmp/arh-memo`. Expected output:

```
<inventory digest>
project memo-returns | run started | connection /tmp/arh-memo/state/connection.json
```

Run it again on the same directory and it reopens the run instead,
which only works while the execution identity still matches.

### The graph

Import the documents first, through the observer role, after advancing
the clock through the principal role. The demonstration does both; by
hand, in a Python shell with the client importable:

```python
from arh_client import api
owner = api.connect('examples/memo_returns', 'principal', '/tmp/arh-memo'); owner.advance_to('2026-10-31')
importer = api.connect('examples/memo_returns', 'observer', '/tmp/arh-memo')
for name in ('m01', 'm02', 'm03', 'm04', 'm05', 'm06'): importer.import_file('SRC-MEMO-SYN', f'examples/memo_returns/data/memos/{name}.md', '2026-10-30', 'examples/memo_returns/data/memos')
importer.import_file('SRC-RET-SYN', 'examples/memo_returns/data/returns.csv', '2026-10-31', 'examples/memo_returns/data')
```

Then the job, which runs the graph in its own process to the review
pause.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m examples.memo_returns.job --run /tmp/arh-memo
```

It prints the graph state: six tone calls recorded, the join at 3/3
MET, the placebo at 1/3 MET, the selection proposed as `TH-M1`, and
`paused` with the review status `waiting_for_review`. Kill it at any
point and run it again: every node reads the researcher's operation
journal under `/tmp/arh-memo/researcher/operations/` first and repeats
nothing it already did. A call whose outcome was lost is settled at its
maximum and replaced only after the host confirms the dead process is
gone, which the demonstration does with the host control's `quiesce`.

The check and the decision come from the other identities.

```python
from examples.memo_returns.evaluator import recompute
api.connect('examples/memo_returns', 'checker', '/tmp/arh-memo', recompute=recompute, kind='tone-return-join').check('TR-...')
owner.decide('TR-...', 'ADMITTED', 'placebo clean')
```

Run the job again and it resumes the paused graph, reads `decided`, and
pauses again, because a decision is not an application. After
`owner.apply('TR-...')` the next run reads `applied` and the graph
finishes. Resuming never approves anything; the researcher identity
cannot decide, and the demonstration shows the refusal.

### The demonstration

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m examples.memo_returns
```

One command runs the whole sequence with the awkward interruption
points: killed after two calls, killed inside the fourth call between
permission and receipt, blocked until quiescence is proven, replaced,
killed after the join's record before the node returned, resumed in
parallel, paused for review, a wrong evaluator failing and the right
one passing, a resume before any decision, the researcher refused when
it tries to decide, the decision, the application, and the host closed
and reopened. Expected ending:

```
  ok   history query by analysis field: 1 conclusion(s) for next_day_bp
Lines: research 136 | configuration 33 | process 54 | demonstration 160 | client api+nodes 407
Timings: {...}
Result: PASS | generated data labelled synthetic; no forward standing.
```

Records land under `artifacts/development/memo_returns/<stamp>-memo-returns/`.
The retained run `demo-20261101-memo-returns` is there. Verified on
2026-11-01 through the demonstration and its integration test. The
provider is a deterministic stand-in; its calls are counted by the
example, not by ARH, and calls a node makes outside the client's call
wrapper are invisible to ARH.

## Refusals and errors

A refusal is an `Outcome` with `ok == False`. The requested operation was
refused and the refusal is on the ledger. Earlier spending and unresolved
liabilities remain. An operational error raises `HarnessError`.

| You see | What it means | Next action |
| --- | --- | --- |
| `BUDGET_EXCEEDED`, `CAP_EXCEEDED` | The grant or lineage cannot cover the reservation | Reserve less, close unused reservations, or ask the Principal for a grant |
| `ALLOWANCE_EXCEEDED` | The attempt's maximum exceeds what the reservation still holds | Reserve enough for the tariff before attempting |
| `INVALID_ESTIMATE` | The maximum does not equal the tariff for this input size | Compute it from the profile, which the client does for you |
| `TOOL_NOT_PERMITTED`, `INVALID_STEP`, `CAPABILITY_UNSUPPORTED` on an attempt | Tool, step or parameters are not what the profile and the grant declare | Use the declared step, tool and exact parameters |
| `FENCED` | The Principal stopped new spending under the grant | Nothing to do as a researcher. Existing liabilities still settle |
| `UNAUTHORIZED` | The identity cannot do this operation | Run it under the right identity. A researcher cannot check, decide, apply or fence |
| `CHECK_NOT_PASS`, `NOT_DECIDED`, `STALE_CHECK`, `STALE_BASE` | Admission was attempted out of order or against an old head | Re-check at the current head, decide, then apply |
| `PENDING_PREDECESSOR` | A retry before the earlier attempt was settled | Settle it first, at the receipt or at the maximum |
| `WORKER_NOT_QUIESCENT` | No proof that the earlier work can no longer execute | Path E, authorizing new work |
| `GENESIS_SCOPE` | Startup was already run on this run directory | Reconnect, do not restart |
| `INVALID_CLASS` | A record called itself synthetic while citing historical documents, or the reverse | Let the client set the class from the cited documents |
| `INVALID_DOCUMENT` with `provenance` or `file identity` | A historical document without origin, receipt time or file hash | Import through `Observer.import_file`, which supplies them |
| `NO_CHECK` on decide | The direction has not been checked | Run the check first |
| `REQUEST_KEY_CONFLICT` | A different payload under a key already used | Make a new key for new work |
| `HarnessError ARTIFACT_CHANGED` at host start | A file that takes part in execution or recovery changed since the bundle was frozen | Read the old run, or freeze a new run directory |
| `HarnessError ENVIRONMENT_CHANGED` at host start | The installed Python or a declared package version differs from the one recorded at freeze | Use the recorded environment, or freeze a new run directory |
| `HarnessError ACTOR_MISMATCH` | The token does not match the identity | Reconnect with the current `connection.json` |
| `HarnessError` with a socket error | The host is not up or the path moved | Start or reopen the host and use the new connection file |
| `inspect-request` answers `UNKNOWN` | No committed outcome was found for that key | Send the same payload with the same key again. If the core had received it, the original outcome comes back |

## Tests

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t .
```

Unit, component, workbench and integration tests. The workbench and
integration tests start real processes. The integration tests run the
LangGraph example when `.venv/bin/python` exists and skip it otherwise.
The whole suite takes about ninety seconds. Last result 81 tests, OK.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m acceptance.local --jobs 4
```

Cooperative acceptance cases, including the process-death schedules.
About two minutes with four jobs. Last result 77 cases PASS. Reports under
`artifacts/development/latest/<run>/` carry `os_isolation: UNVERIFIED`,
which is accurate.

## Not exercised

- Linux user, socket and cgroup isolation under `isolation/`.
- Path D steps 5 and 6 as separate hand-run commands.
- Any real provider or network access. Real local files are exercised in path F.
