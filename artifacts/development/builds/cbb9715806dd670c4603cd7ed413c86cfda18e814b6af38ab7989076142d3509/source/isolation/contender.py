"""Runtime C01 probe: the second lifetime lock must fail; never opens storage."""
from adaptive_research_harness.transport import LifetimeLock
from adaptive_research_harness.encoding import Refusal
if __name__=='__main__':
    try:
        with LifetimeLock('/run/adaptive-research-harness/core/writer.lock'):
            raise SystemExit('FAIL: second writer acquired lock')
    except Refusal as exc:
        if exc.code!='INSTANCE_ALREADY_RUNNING':raise
        print('INSTANCE_ALREADY_RUNNING: second process excluded before storage/dispatch')
