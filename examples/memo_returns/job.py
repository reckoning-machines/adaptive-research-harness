"""Run the memo-returns graph in its own process, resuming whatever an earlier process left, with an optional crash point for the tests.

python3 -m examples.memo_returns.job --run RUN_DIR [--thread memo-1] [--crash after_call_2|join:after_record|...]

A run that was interrupted resumes from its checkpoint; one that paused
for review resumes with a resume command. Either way every node reads the
researcher's operation journal first and repeats no work it already did.
--crash is a demonstration hook; ordinary use never passes it.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import json
import os
import sqlite3
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'client')); sys.path.insert(0, str(ROOT))
from arh_client import api
from examples.memo_returns.graph import build


def run_graph(run, thread='memo-1', crash=None, pause=True):
    from langgraph.checkpoint.sqlite import SqliteSaver
    from langgraph.types import Command
    run = Path(run); os.environ['MEMO_PROVIDER_DIR'] = str(run / 'researcher' / 'provider')
    research = api.connect(project=HERE, role='researcher', run=run)
    def hook(point):
        if crash == point: os._exit(137)
    db = sqlite3.connect(str(run / 'researcher' / 'checkpoints.sqlite'), check_same_thread=False); saver = SqliteSaver(db)
    graph = build(research, saver, pause=pause, hook=hook); config = {'configurable': {'thread_id': thread}}
    before = graph.get_state(config); interrupted = bool(before.tasks) and any(t.interrupts for t in before.tasks)
    if interrupted: out = graph.invoke(Command(resume=True), config); how = 'resumed_after_review_pause'
    elif before.values and before.next: out = graph.invoke(None, config); how = 'resumed_after_interruption'
    elif before.values: out = before.values; how = 'already_finished'
    else: out = graph.invoke({'arh': {}}, config); how = 'started'
    after = graph.get_state(config); paused = bool(after.tasks) and any(t.interrupts for t in after.tasks)
    pause = next((i.value for t in after.tasks for i in (t.interrupts or [])), None) if paused else None
    db.close()
    return {'arh': out.get('arh', {}), 'how': how, 'paused': paused, 'pause': pause, 'next': list(after.next), 'pid': os.getpid(), 'operations': [e['operation'] for e in research.ops.list()]}


def main(argv=None):
    p = argparse.ArgumentParser(); p.add_argument('--run', required=True); p.add_argument('--thread', default='memo-1'); p.add_argument('--crash', default=None); p.add_argument('--no-pause', action='store_true')
    a = p.parse_args(argv)
    try: print(json.dumps(run_graph(a.run, a.thread, a.crash, not a.no_pause), default=str)); return 0
    except Exception as exc:
        # A node that could not proceed, such as a replacement refused until quiescence is proven. The checkpoint keeps the pending work.
        print(json.dumps({'error': f'{type(exc).__name__}: {exc}', 'pid': os.getpid()})); return 3


if __name__ == '__main__': sys.exit(main())
