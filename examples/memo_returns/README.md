# Memo tone and next-day returns

A two-source analysis through LangGraph on the everyday interface. Six
analyst memos are scored for tone, one metered call each, the scores are
joined to a returns table in two parallel branches, the real column and a
placebo column, the scientist's own next question is proposed, and the
graph waits for an independent check and the Principal's decision.
Generated data, labelled synthetic. No forward standing.

## What the scientist wrote

| File | Lines | What it is |
| --- | --- | --- |
| `research.py` | 44 | The expectations, the scoring node with one metered call per memo, the inputs of the join, and the choice of the next question |
| `tools.py` | 16 | The join, and one call that makes it the host-run tool |
| `provider.py` | 42 | The deterministic stand-in for a model call that scores one memo |
| `evaluator.py` | 10 | The recompute function, and one call that makes it the Checker's evaluate |
| `graph.py` | 20 | The graph: five nodes, four of them from the client |
| `project.json` | 33 | The project description the generator writes the setup from |

Together 136 lines of research code and 33 of configuration. The
process entry, `job.py`, is 54 lines and would be the same for any
graph. The demonstration, `__main__.py` and `make_data.py`, is 160 lines
nobody needs to run their own graph.

## What the client did

`arh_client.api` and `arh_client.langgraph_nodes`, 407 lines, written
once. Every reservation, attempt, permission, receipt, record,
settlement and closure. A durable journal per operation, so a node
killed before its first return finds its own attempt on restart and
repeats nothing. An explicit replacement for a call whose outcome was
lost, admitted only after the host confirms the dead process is gone.
Namespaces that merge by operation, so parallel branches never overwrite
each other. A review node that pauses while the proposal is waiting, and
again while it is decided but not applied. Refusals with their meaning
and next action.

## Run it

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m examples.memo_returns
```

Or by hand, three terminals.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m arh_client.dev up examples/memo_returns --run /tmp/arh-memo
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m examples.memo_returns.job --run /tmp/arh-memo
```

The job runs the graph to the review pause. The check and the decision
come from other identities, for example in a Python shell with the
client importable.

```python
from arh_client import api
from examples.memo_returns.evaluator import recompute
api.connect('examples/memo_returns', 'checker', '/tmp/arh-memo', recompute=recompute, kind='tone-return-join').check('TR-...')
api.connect('examples/memo_returns', 'principal', '/tmp/arh-memo').admit('TR-...', 'placebo clean')
```

Then the job again, which resumes the paused graph, reads `applied` and
finishes. Documents are imported through the observer role and the clock
is advanced through the principal role; `__main__.py` shows both calls.

## What the demonstration shows

- Killed after two metered calls, before the node returned: both calls
  are in the journal, and the resumed node repeats neither.
- Killed inside the fourth call, after the provider counted it and
  before any receipt: the call is uncertain, settled at its maximum, and
  its replacement is refused until the host confirms the dead process is
  gone. After that proof the replacement is admitted with the next
  dispatch index. Six memos, seven calls, one authorized repeat.
- Killed after the join's record and before the node returned: the
  record is on the ledger and in the journal, and the resumed branches
  run one attempt each.
- A wrong evaluator fails the check and the right one passes. Resuming
  the graph before any decision pauses it again. The researcher's own
  attempt to decide is refused. The Principal's decision pauses the
  graph once more until it is applied.
- The host closed and reopened with the same call reports the finished
  graph and starts nothing.

## Limits

The provider is a deterministic stand-in and its calls are counted by
the example, not by ARH. Calls a node makes outside the call wrapper are
invisible to ARH, and the receipt a caller reports is its own
accounting. There is no OS isolation. The check is on reproducibility
and record integrity, not on the research.
