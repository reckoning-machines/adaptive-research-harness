"""Run one Check as the evaluator under the Checker identity, in its own process.

python3 -m <package>.check --connection PATH --transition TR
"""
from __future__ import annotations
import argparse
import json
import sys
from arh_client import connect, Checker
from .evaluator import recompute


def main(argv=None):
    p = argparse.ArgumentParser(); p.add_argument('--connection', required=True); p.add_argument('--transition', required=True); p.add_argument('--actor', default='AD-CK-H1.0')
    a = p.parse_args(argv)
    checker = Checker(connect(a.connection, a.actor), recompute=recompute)
    r = checker.check(a.transition)
    print(json.dumps({'transition': r.transition_id, 'result': r.result, 'criteria': r.criteria, 'check_sequence': r.check_sequence,
                      'check': r.check.raw if r.check else None, 'attempt': r.attempt.as_dict(), 'settlement': r.settlement.status}, sort_keys=True)); return 0


if __name__ == '__main__': sys.exit(main())
