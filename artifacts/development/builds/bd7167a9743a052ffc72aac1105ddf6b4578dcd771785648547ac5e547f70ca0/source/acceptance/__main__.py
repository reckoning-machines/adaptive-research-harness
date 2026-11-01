"""Private, separately gated runtime acceptance runner. --list is build-safe."""
import argparse
import os
from pathlib import Path
import traceback
from adaptive_research_harness.encoding import canonical,require,Refusal
from adaptive_research_harness.profile import Profile
from adaptive_research_harness.clock import durable_write
from .catalog import CASES,DEATH_POINTS


def main():
    p=argparse.ArgumentParser();p.add_argument('--list',action='store_true');p.add_argument('--execute',action='store_true')
    p.add_argument('--case',action='append');p.add_argument('--root',default='/opt/adaptive-research-harness')
    p.add_argument('--permit',default='/etc/adaptive-research-harness/run-approval.json')
    p.add_argument('--report-dir',default='/var/lib/adaptive-research-harness-reports');args=p.parse_args()
    if args.list:
        print(canonical({'cases':CASES,'death_points':DEATH_POINTS,'forced_terminal_orders':['apply','invalidate'],'status':'NOT_EXECUTED'}).decode());return 0
    require(args.execute,'EXPLICIT_EXECUTION_REQUIRED');require(os.getuid()==20001,'PRINCIPAL_FIXTURE_UID_REQUIRED')
    root=Path(args.root);profile=Profile(root/'docs/builds/first_cycle_20261029/run_bundle');permit=profile.approve_run(args.permit,root)
    require(permit.get('runtime_scope')=='all-listed-cases-and-death-points','RUNTIME_SCOPE_REQUIRED')
    from .runtime import Runtime
    from . import cases,death
    selected=args.case or list(CASES)+['D-'+x for x in DEATH_POINTS]+['D-terminal-apply','D-terminal-invalidate']
    allowed=set(CASES)|{'D-'+x for x in DEATH_POINTS}|{'D-terminal-apply','D-terminal-invalidate'}
    require(set(selected)<=allowed,'INVALID_CASE');dest=Path(args.report_dir);dest.mkdir(parents=True,exist_ok=True)
    results=[]
    for case in selected:
        record={'case':case,'inventory_sha256':profile.inventory_hash,'status':'NOT_EXECUTED'};r=None
        try:
            r=Runtime(case).startup()
            if case in CASES:getattr(cases,case)(r)
            elif case.startswith('D-terminal-'):death.terminal_order(r,case.removeprefix('D-terminal-'))
            else:death.run(r,case.removeprefix('D-'))
            record.update(r.finish())
        except Exception as exc:
            record.update(status='FAIL',exception=type(exc).__name__,message=str(exc),traceback=traceback.format_exc(),trace=r.trace if r else [])
        durable_write(dest/(case+'.json'),record);results.append({'case':case,'status':record['status']})
        print(case,record['status'],flush=True)
    durable_write(dest/'summary.json',{'inventory_sha256':profile.inventory_hash,'results':results,'no_public_release':True})
    return 0 if all(x['status']=='PASS' for x in results) else 1

if __name__=='__main__':raise SystemExit(main())
