"""Headless demonstration: three cohorts, an interrupted run resumed, a read-only copy.

Prints what happened. Returns 0 when every expectation holds.
"""
from pathlib import Path
import json
import shutil
import time
from adaptive_research_harness.encoding import Refusal
from .session import Session, open_run, RUNS, list_runs
from . import records


def complete(run):
    n=0
    while run.view()['next'] is not None:run.step();n+=1
    return n


def run_demo():
    stamp=time.strftime('%Y%m%d-%H%M%S');ok=True;report=[]
    def say(*a):print(*a,flush=True);report.append(' '.join(str(x) for x in a))
    outcomes={}
    for cohort in ('original','independent-shocks'):
        s=Session.create(cohort,name=f'demo-{stamp}-{cohort}')
        try:
            steps=complete(s);v=s.view();c=next(x for x in v['stages'] if x['key']=='control')
            outcomes[cohort]=v;say(f"{cohort}: {steps} steps, {v['status']}, N={v['state']['N']}, path={c['analysis']}, control='{c['text']}'");say('   ',c['nature'])
            say('    budgets',{g:b['committed'] for g,b in v['controls']['budgets'].items() if b.get('committed') not in (None,'0.00')},'reader',s.reader()['status'])
        finally:s.close()
    name=f'demo-{stamp}-control-survives-interrupted'
    s=Session.create('control-survives',name=name)
    try:
        s.step();s.step();v=s.view();say(f"control-survives: stopped after the diagnostic; next permitted = {v['next']['op']}; E={v['counts']['E']}")
    finally:s.close()
    es1,ts1,_=records.load_readonly(RUNS/name/'state'/'harness.sqlite')
    r=open_run(RUNS/name);say(f"reopened {name} as {r.mode}; next permitted = {r.view()['next']['op']}")
    steps=complete(r);v=r.view();es2,ts2,_=records.load_readonly(RUNS/name/'state'/'harness.sqlite')
    attempts=[e for e in es2 if e['kind']=='ATTEMPT' and e['actor']=='AD-R1.0']
    say(f"continued with {steps} steps to {v['status']}, N={v['state']['N']}; researcher attempts={len(attempts)}; AU-RP-1 committed={v['controls']['budgets']['AU-RP-1']['committed']}; earlier records unchanged={es2[:len(es1)]==es1 and ts2[:len(ts1)]==ts1}")
    ok&=len(attempts)==2 and v['controls']['budgets']['AU-RP-1']['committed']=='2.00' and es2[:len(es1)]==es1
    r.close()
    for cohort,v in outcomes.items():
        r=open_run(RUNS/f'demo-{stamp}-{cohort}');say(f"reopened completed {cohort}: {r.mode}, status {r.view()['status']}, next={r.view()['next']}");ok&=r.view()['next'] is None;r.close()
    old=RUNS/f'demo-{stamp}-old-build';shutil.copytree(RUNS/name,old,ignore=shutil.ignore_patterns('*.sock','fixture.json'))
    inv=json.loads((old/'bundle/inventory.json').read_bytes());inv['files'][0]['sha256']='0'*64;(old/'bundle/inventory.json').write_bytes(json.dumps(inv,sort_keys=True,separators=(',',':')).encode()+b'\n')
    ro=open_run(old);say(f"copy with a differing build: {ro.mode} ({ro.reason}); reader {ro.reader()['status']}")
    try:ro.step();ok=False
    except Refusal as exc:say('   step refused:',exc.code)
    say('runs listed:',[(x['run'],x['progress'],'live-eligible' if x['live_eligible'] else 'read-only') for x in list_runs() if stamp in x['run']])
    say('DEMO','PASS' if ok else 'FAIL')
    return 0 if ok else 1
