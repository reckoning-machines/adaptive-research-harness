# Runbook

Verified steps for operating the Adaptive Research Harness on one machine.
The [README](README.md) says what it is for, the
[architecture](architecture.md) says how it works, and the
[client README](client/README.md) documents each Python operation. Every
command below was run on macOS with Python 3.12.3 on 2026-11-01 against
the current tree. Anything not exercised is marked.

## Prerequisites

| Need | Detail |
| --- | --- |
| Python | 3.12 from a standard distribution. The harness uses only the standard library |
| Operating system | macOS or Linux. No virtual machine, no container |
| Working directory | The repository root for every harness command. The client runs from anywhere |
| Environment | `PYTHONDONTWRITEBYTECODE=1` on each harness command so no bytecode is written next to the covered source. The examples include it |
| For the LangGraph paths | A virtual environment with the client and its `langgraph` extra, as in path C |

Every run is disposable synthetic development. Charges are simulated
units, nothing outside the machine is contacted, and nothing earns forward
standing.

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
and the two tools the harness runs itself. It does not use the client.

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

If the source tree changed since the bundle was frozen, the core refuses to
start with `ARTIFACT_CHANGED` and the run can only be read. Freeze a new
run directory for new work.

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

Run the harness on files you have. Documents keep their provenance and are
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
records the attempt, and the calculator the harness runs does the work.
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
If the source has changed since the run was frozen it opens read-only.

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

## Refusals and errors

A refusal is an `Outcome` with `ok == False`. It is on the ledger and
nothing was spent. An operational error raises `HarnessError`.

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
| `HarnessError ARTIFACT_CHANGED` at host start | The source changed since the bundle was frozen | Read the old run, or freeze a new run directory |
| `HarnessError ACTOR_MISMATCH` | The token does not match the identity | Reconnect with the current `connection.json` |
| `HarnessError` with a socket error | The host is not up or the path moved | Start or reopen the host and use the new connection file |
| `inspect-request` answers `UNKNOWN` | The core never received the command whose reply you lost | Send it again with the same key |

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
