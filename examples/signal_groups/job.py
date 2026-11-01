"""Run one design in its own process with persisted keys, so a killed run resumes rather than repeats.

python3 -m examples.signal_groups.job --connection PATH --work DIR --design SEQ [--crash after_attempt|after_execution]

--crash is a demonstration hook used by demo.py and the tests. Ordinary use never passes it.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path
from arh_client import connect
from arh_client.analysis import persisted_keys
from examples.signal_groups.researcher import SignalResearcher


def main(argv=None):
    p = argparse.ArgumentParser(); p.add_argument('--connection', required=True); p.add_argument('--work', required=True); p.add_argument('--design', type=int, required=True); p.add_argument('--crash', default=None); p.add_argument('--actor', default='AD-S1.0')
    a = p.parse_args(argv); keys = persisted_keys(Path(a.work) / f'design-{a.design}.keys.json')
    r = SignalResearcher(connect(a.connection, a.actor)); design = r.c.record('E', a.design)
    def hook(point):
        if a.crash == point: os._exit(137)
    out = r.run({'ledger': 'E', 'sequence': design['seq'], 'sha256': design['sha256']}, keys, hook)
    print(json.dumps({k: (v.raw if hasattr(v, 'raw') else v) for k, v in out.items()}, default=str)); return 0


if __name__ == '__main__': sys.exit(main())
