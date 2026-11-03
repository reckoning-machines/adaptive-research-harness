"""Actual process-death schedules. Never called by the build-only test suite."""
from .runtime import expect,key
from .cases import pending,C06,require_refusal


def run(r,point):
    if point=='clock_unavailable':C06(r);return
    if point=='all_components_restart':
        r.research();before=r.history('E');r.host('restart');r.ready();assert r.history('E')==before;return
    if point.startswith('tool_'):
        a=pending(r);r.arm(a,'PAUSE_AT_BOUNDARY','after_tool_execution' if point=='tool_after_execution_before_reply' else None)
        r.pool.submit(r.agent,'r01','complete-research',{'attempt':a});r.barrier()
        r.host('restart');r.ready();expect(r.settle(a))
        if point=='tool_before_execution':assert r.read('budget',{'grant':'AU-RP-1'})['committed']=='1.00'
        return
    if point.startswith('checker_'):
        candidate=r.candidate();r.host('pause-actor',actor='ck1',point=point)
        r.pool.submit(r.check,candidate['transition_id']);r.barrier(point)
        obligations=r.read('obligations')['pending_attempts'];assert obligations
        r.host('restart');r.ready()
        for a in obligations:expect(r.agent('ck1','settle-pending',{'attempt':a}))
        assert not any(x['kind']=='CHECK' and x['transition_id']==candidate['transition_id'] for x in r.history('T'))
        return
    op=point.removeprefix('before_').removeprefix('after_').removesuffix('_commit')
    if point=='principal_control_continuation':op='decide';point='after_decide_commit'
    candidate=None;body=None;bind=None
    if op=='reserve':
        k=key();r.arm(k,'PAUSE_AT_BOUNDARY',point);future=r.pool.submit(r.reserve,'r01','1.00',k)
    elif op=='attempt':
        r.arm('@op:attempt','PAUSE_AT_BOUNDARY',point);future=r.pool.submit(r.research,'SYN-A-1',True)
    elif op in ('dispatch_claim','research-commit','settle'):
        a=pending(r);target='@op:tool-run' if op=='dispatch_claim' else '@op:'+op
        r.arm(target,'PAUSE_AT_BOUNDARY',point);future=r.pool.submit(r.agent,'r01','complete-research',{'attempt':a})
    elif op=='check-commit':
        candidate=r.candidate();r.arm('@op:check-commit','PAUSE_AT_BOUNDARY',point)
        future=r.pool.submit(r.check,candidate['transition_id'])
    elif op=='decide':
        candidate=r.candidate();check=r.check(candidate['transition_id']);r.arm('@op:decide','PAUSE_AT_BOUNDARY',point)
        future=r.pool.submit(r.decision,candidate['transition_id'],check)
    elif op in ('bind','apply'):
        candidate,body=r.decided();r.arm('@op:apply','PAUSE_AT_BOUNDARY',point);future=r.pool.submit(r.call,'apply',body)
    elif op=='invalidate-request':
        candidate,body,bind=r.bound();r.tick(301001);r.arm('@op:invalidate-request','PAUSE_AT_BOUNDARY',point)
        future=r.pool.submit(r.call,'invalidate-request',{'bind':bind['seq']})
    else:raise AssertionError('Unmapped death point '+point)
    r.barrier(point)
    # Before-commit hooks hold the owning transaction; don't query through a
    # blocked writer to fabricate a snapshot. Kill and reconstruct afterward.
    proof=r.host('restart')['proof'];assert proof['terminated_generations'];r.ready()
    if op=='reserve':
        result=expect(r.reserve('r01','1.00',k))
        repeats=[e for e in r.history('E') if e['kind']=='RESERVATION' and e['actor']=='AD-R1.0']
        assert len(repeats)==1;return
    if op=='attempt':
        attempts=[e for e in r.history('E') if e['kind']=='ATTEMPT' and e['actor']=='AD-R1.0']
        assert len(attempts)==(0 if point.startswith('before') else 1)
    for a in r.read('obligations')['pending_attempts']:
        e=next(x for x in r.history('E') if x['seq']==a);actor='ck1' if e['actor']=='AD-CK-1.0' else 'r01'
        expect(r.agent(actor,'settle-pending',{'attempt':a}))
    if candidate and op in ('bind','apply','decide','invalidate-request'):
        result=r.call('recover',{'continue':True,'transition_id':candidate['transition_id']})
        assert result['status'] in ('COMMITTED','ALREADY_APPLIED'),result
    if point=='after_research-commit_commit':assert any(e['kind']=='RESEARCH_RECORD' and e['actor']=='AD-R1.0' for e in r.history('E'))
    if point=='after_check-commit_commit':assert any(e['kind']=='CHECK' and e['transition_id']==candidate['transition_id'] for e in r.history('T'))


def terminal_order(r,winner):
    p,body,bind=r.bound();r.tick(301001)
    if winner=='apply':
        expect(r.call('apply',body));require_refusal(r.call('invalidate-request',{'bind':bind['seq']}),'BINDING_TERMINAL')
    else:
        expect(r.call('invalidate-request',{'bind':bind['seq']}));require_refusal(r.call('apply',body),'BINDING_INVALIDATED')
        expect(r.call('release',{'bind':bind['seq']}))
