# Adaptive Research Harness client

ARH is Adaptive Research Harness.

A small Python client for running your own research agents under the
harness. You supply a researcher and an experiment. ARH holds the
budget, records every attempt, requires an independent check before
anything is admitted, and keeps every refusal. Nothing you write needs to
read the constitution; the core refuses what it does not allow and tells
you why.

Standard library only. LangGraph is an optional extra for the graph adapter.

## Install

The client installs anywhere. The host that runs the core is started from a
checkout of ARH repository.

```sh
# client, in any environment
pip install /path/to/speedway/client
# with the LangGraph adapter
pip install '/path/to/speedway/client[langgraph]'
```

## Start a host

From the checkout, against an experiment directory (the headline example
here). The command freezes the experiment into a bundle, starts the core and
any core-run tool workers as processes, and prints the connection file.

```sh
cd /path/to/speedway
python3 -m adaptive_research_harness.local_host --setup examples/langgraph_headlines --run /tmp/arh-run
```

It prints `connection /tmp/arh-run/state/connection.json`. That file holds
the socket path, the control socket and one token per actor. Whoever reads
it can act as any actor. Treat it like a credential. Ctrl-C stops the host;
the run directory keeps every record and can be restarted with the same
command.

## Getting started

Each identity gets its own connection. The researcher does research; the
Checker checks; the Principal decides. The core refuses a connection that
tries to do another identity's work.

```python
from arh_client import connect, Researcher, Execution, ReceiptStore, Connection, event_ref

conn = connect('/tmp/arh-run/state/connection.json', 'AD-RH1.0')
r = Researcher(conn)

# Keys make every command safe to repeat. Persist them before use.
keys = {name: Connection.new_key() for name in ('reserve', 'attempt', 'settle', 'record', 'close')}

doc = r.formation('SRC-NEWS-SYN')                      # the committed input document
reservation = r.reserve('0.50', {'kind': 'Theme', 'id': 'TH-H1'}, keys['reserve'])
if not reservation.ok:
    print('refused', reservation.reason, reservation.detail); raise SystemExit(1)

attempt = r.attempt(reservation.sequence, 'classify-headlines', 'FAKE-LLM-1',
                    [event_ref(doc)], {'lexicon': 'LEX-1', 'labels': ['bullish', 'bearish']}, '0.48', keys['attempt'])
attempt.raise_for_refusal()

ex = Execution(r, attempt.sequence, attempt.input_hash, 'FAKE-LLM-1', '0.48')
outcome = ex.run(lambda claim: my_provider(doc['body']['document'], claim), ReceiptStore('/tmp/my-receipts'))
if outcome['status'] == 'uncertain':
    ex.settle_unknown(keys['settle'])                   # liability kept at the maximum; nothing is called again
else:
    receipt = outcome['receipt']
    body = r.record_body(attempt.sequence, 'What does the provider label?', receipt['result'], None, [event_ref(doc)])
    r.research_commit(body, keys['record']); ex.settle(receipt, keys['settle']); r.close(reservation.sequence, keys['close'])
```

`my_provider(document, claim)` is your code. It returns `(result, actual)`
where `actual` is the charge as a two-decimal string. It receives the claim
so it can key its own records by it.

## What the core enforces, and what you supply

| You supply | The core enforces |
| --- | --- |
| An experiment directory: `setup.json` (grants, limits, theme), `designs_and_methods.json` (your researcher and Checker designs, tools, methods, hypothesis template, formation document), `experiment.json` (steps, tariffs, sources) | Only declared steps, tools and parameters are admitted; the estimate must match the tariff; sources follow their declared period and item rules |
| A researcher program, LangGraph or not, under the researcher token | Reserve before attempt, attempt before execution, one fresh permission per attempt, settlement at actual or at the maximum, every refusal preserved |
| A provider or tool your researcher calls | Your receipt is accounting. The core binds it to the attempt and refuses a second different receipt. It cannot stop your process spending at a provider it can reach; a tool the host runs (`execution: core`) is the stronger arrangement |
| An evaluator under the Checker token | A Check must come from a Checker grant, a different lineage, with its own funded attempt; its content must equal the registered receipt; the proposer cannot check, decide or apply |
| Principal decisions, or policy `P-1` for routine registrations | Decision requires a passing Check at the current base; Apply requires the decision and, for a researcher's proposal, bound funding |

## Public API

Stable, documented here. Everything else in the package is an internal
helper and may change.

### Results and errors

- `Outcome`: the core's answer to a command. `status` is `COMMITTED` or
  `REFUSED`; `ok` is the boolean; `reason` and `detail` explain a refusal;
  `refs` are the records written, including the preserved refusal;
  `sequence` is the first record's sequence; `raise_for_refusal()` turns
  a refusal into `RefusedError`.
- `Ref`: a ledger record, `ledger` (`E` evidence or `T` transition),
  `sequence`, `sha256`.
- `HarnessError`: an operational failure, transport or host. Retry is
  safe only with the same key, which returns the original outcome.
- `RefusedError`: raised by `*_or_raise` and `raise_for_refusal()`;
  carries `outcome`.

### `connect(connection_file, actor) -> Connection`

Reads: `profile()` (the frozen bundle, including `experiment`),
`state()` (head `N`, grants, designs, hypotheses), `budget(grant)`,
`obligations()`, `get(ref)`, `history(ledger)`, `closure()`.
Commands: `call(op, payload, key)` returns an `Outcome`; `outcome(key)`
tells you what became of a command whose reply you lost: `COMMITTED`,
`REFUSED`, `PARTIAL` or `UNKNOWN`. `Connection.new_key()` makes a key.

Retry rule for every command: send the same key and payload again and you
get the original outcome. A different payload under the same key is
refused `REQUEST_KEY_CONFLICT`.

### `Researcher(connection)`

| Operation | Purpose | Returns | Refusals you will see |
| --- | --- | --- | --- |
| `formation(source, item_id=None)` | The earliest committed document of a source | record dict | `FORMATION_MISSING` (HarnessError) |
| `reserve(amount, purpose, key)` | Hold budget for a purpose in scope | `Outcome` | `BUDGET_EXCEEDED`, `CAP_EXCEEDED`, `FENCED`, `PURPOSE_OUT_OF_SCOPE` |
| `attempt(reservation, step, tool, input_refs, parameters, maximum, key)` | Record an attempt before any work; `maximum` must equal the tariff | `Outcome` with `input_hash` | `ALLOWANCE_EXCEEDED`, `GRANT_EXHAUSTED`, `INVALID_ESTIMATE`, `TOOL_NOT_PERMITTED`, `INVALID_STEP`, `CAPABILITY_UNSUPPORTED` (parameters) |
| `record_body(attempt, question, result, failure, input_refs, ...)` | Build a research record in the admitted shape. `attempt=None` with `tool=` for an `EXPERIMENT DESIGN` or `SELECTION` that meters no work; `revises=` names an earlier record of yours; the class follows the cited documents | dict | |
| `research_commit(body, key)` | Commit the record | `Outcome` | `UNAUTHORIZED`, `INVALID_CLOSURE` |
| `close(reservation, key)` | Release unused allowance; liabilities stay | `Outcome` | `RESERVATION_BOUND` |
| `propose_hypothesis(content, budget, propose_key, fund_key)` | Propose and fund a hypothesis from the template | `Outcome` with `transition_id`; `raw['funded']` | `SCOPE_VIOLATION`, `STALE_BASE`, `WRONG_RESERVATION` |
| `propose_theme(content, budget, propose_key, fund_key)` | Propose and fund a Theme, the next investigation. Admission needs a check and a Principal decision | `Outcome` with `transition_id` | `SCOPE_VIOLATION`, `UNAUTHORIZED` |
| `retry(previous_attempt, key)` | A new attempt for the same work | `Outcome` | `PENDING_PREDECESSOR`, `WORKER_NOT_QUIESCENT` |

### `Execution(researcher, attempt, input_hash, tool, maximum)`

The explicit part. `claim()` asks the core for permission; the reply
`PERMISSION_CONSUMED` is given exactly once for an attempt and is never
cached. `run(call, store, lookup=None)` does the whole sequence and
returns `{'status': ..., 'receipt': ...}`:

| status | Meaning | What happened |
| --- | --- | --- |
| `executed` | fresh permission, your provider ran once, receipt stored durably then registered | normal path |
| `registered` | the core already held a receipt | nothing ran |
| `resumed` | your durable receipt existed, the core had not been told | registered it, nothing ran |
| `recovered` | your provider's own record for this attempt was found by `lookup(attempt, input_hash)` | receipt rebuilt, nothing ran |
| `uncertain` | permission was consumed and no receipt exists anywhere | nothing ran; settle with `settle_unknown(key)` at the maximum |

For a tool the host runs (`execution: core`) call `run()` with no
arguments: the core dispatches to its worker and the status is
`registered`, or `recovered` when the reply was lost and the worker still
held the receipt.

`settle(receipt, key)` settles at the actual charge; `settle_unknown(key)`
at the maximum. Settling at the maximum is accounting. It does not cancel
work at your provider. A `retry` of an uncertain attempt is admitted only
after the host records that your process is gone and, for a provider
declared `may_outlive_caller`, that the provider completed or cancelled
the earlier operation. `ReceiptStore(directory)` is the durable receipt
file per attempt the sequence relies on.

### `Checker(connection, recompute=None, validate_motivation=None)`

`check(transition_id) -> CheckResult` funds, computes, registers and
commits one independent Check under the Checker's own grant. `result` is
`PASS`, `FAIL` or `None` when no judgment could be computed; `criteria`
maps each criterion to `MET` or `NOT MET`; `check_sequence` is what a
decision cites. `recompute(context)` is your experiment's validator for a
hypothesis: it receives the committed documents, research records and
proposal content and returns true when the arithmetic recomputes. Without
it a hypothesis fails `recomputation`; missing capability never passes.
`validate_motivation(context)` does the same for a Theme: it receives the
documents and research records the Theme cites and returns true when the
analysis they describe recomputes; otherwise `motivation` is not met.

### `Principal(connection)`

`decide(transition_id, check, decision, reason)`,
`policy_decide(transition_id, check)`, `apply(transition_id, decision)`,
`fence(grant, reason)`, `recover(transition_id)`, each returning an
`Outcome`. Refusals: `CHECK_NOT_PASS`, `STALE_CHECK`, `NOT_DECIDED`,
`STALE_DECISION`, `BINDING_INVALIDATED`, `ALREADY_FENCED`.

### `Observer(connection)` and `startup(...)`

`observe(source, content, date)` commits a source document with its listing
and extraction. `import_file(source, path, date, origin, note=...)` and
`import_bytes(...)` commit a local file as a historical document: name,
content hash, size, media type, your declared origin and receipt time, and
its text or rows. The source must be declared historical in the profile.
`historical_document(raw, name, origin)` builds that body for you. `startup(principal, observer, check, tick)` runs genesis and
the control transitions a setup declares, each checked by your `check`
callable, and returns the applied head.

### `HostControl.from_file(connection_file)`

`tick(ms)` advances the synthetic clock. `quiesce(generation,
provider_dispositions)` records that a caller process is gone and, per
attempt, what the provider did with its operation. `status()`, `stop()`.

### `arh_client.langgraph_adapter`

`ExperimentSpec` names your step, tool, parameters, purpose, reservation
amount, source, provider, optional provider lookup, record builder and
optional derive and proposal builders. `build_research_graph(researcher,
spec, store, checkpointer)` returns a compiled graph: prepare, reserve,
attempt, execute, report. `build_proposal_graph(...)` returns derive,
propose. Keys are made in `prepare` and checkpointed before use, so a node
re-run after a crash re-sends the same key. Permission is obtained inside
`execute` and never stored in state.

## How failures and retries work

- A refusal is an `Outcome` with `ok == False`. The requested operation
  was refused and the refusal is on the ledger. Earlier spending and
  unresolved liabilities remain.
- A lost reply: call `connection.outcome(key)`. `COMMITTED` or `REFUSED`
  is the outcome you missed. `UNKNOWN` means no committed outcome was
  found for that key; send the same payload with the same key again, and
  if the core had received it the original outcome comes back.
- A crash after `attempt` and before `execute` finished: re-run. `claim()`
  answers `IN_PROGRESS_OR_UNCERTAIN`; `Execution.run` resumes from your
  receipt store, then from your provider's lookup, and otherwise reports
  `uncertain`. It never calls the provider a second time for that attempt.
- Uncertain means the work may have run or may still be running. Settle at
  the maximum so the liability is counted. To do the work again, open a
  retry; the host must first record your dead process and the provider's
  completion or cancellation of the earlier operation.
- Checks, decisions and Apply are separate processes under separate
  tokens. A researcher connection that calls them is refused and the
  refusal is kept.

## Trust model

One host process generates every token and writes them to one file. There
is no OS isolation; identity is a shared secret plus a self-reported pid.
For a tool your process executes, the receipt is your statement: the core
binds it and counts it, which is accounting, not enforcement over what your
process spends. A tool the host runs as its own worker is the stronger
arrangement: the core hands it the admitted input and takes its receipt.
Everything in the shipped examples is synthetic and earns no forward
standing.

## The complete LangGraph example

`examples/langgraph_headlines/` in the checkout is a whole experiment:
setup, profile, a deterministic fake provider, a LangGraph researcher with
a SQLite checkpointer, an evaluator and a runner. Run it from the checkout:

```sh
python3 -m venv .venv && .venv/bin/pip install -e './client[langgraph]'
.venv/bin/python -m examples.langgraph_headlines
```

Or copy the directory anywhere, install the client there, and run
`python -m langgraph_headlines --harness /path/to/speedway`. It prints the
research result and thirteen control decisions: startup, a recorded and
settled classification, returns committed a period later, an overstated
count failing its Check, the researcher refused when it tries to approve,
the honest proposal admitted, over-budget work refused before the provider
runs, three interruption cases, the replayed claim, and the replacement
rule.
