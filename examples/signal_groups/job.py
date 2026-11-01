"""Run one design in its own process, with persisted keys and an optional crash point, so an interruption can be resumed.

python3 -m examples.signal_groups.job --connection PATH --work DIR --design SEQ [--crash after_attempt|after_execution]
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path
from arh_client import connect, Connection
from examples.signal_groups.researcher import SignalResearcher


def main(argv=None):
    p = argparse.ArgumentParser(); p.add_argument('--connection', required=True); p.add_argument('--work', required=True); p.add_argument('--design', type=int, required=True); p.add_argument('--crash', default=None); p.add_argument('--actor', default='AD-S1.0')
    a = p.parse_args(argv); work = Path(a.work); work.mkdir(parents=True, exist_ok=True); keyfile = work / f'design-{a.design}.keys.json'
    keys = json.loads(keyfile.read_text()) if keyfile.exists() else {k: Connection.new_key() for k in ('reserve', 'attempt', 'record', 'settle', 'close')}
    if not keyfile.exists(): keyfile.write_text(json.dumps(keys))   # persisted before use: a re-run sends the same keys
    r = SignalResearcher(connect(a.connection, a.actor)); design = r.c.record('E', a.design)
    def hook(point):
        if a.crash == point: os._exit(137)
    out = r.run({'ledger': 'E', 'sequence': design['seq'], 'sha256': design['sha256']}, keys, hook)
    print(json.dumps({k: (v.raw if hasattr(v, 'raw') else v) for k, v in out.items()}, default=str)); return 0


if __name__ == '__main__': sys.exit(main())
