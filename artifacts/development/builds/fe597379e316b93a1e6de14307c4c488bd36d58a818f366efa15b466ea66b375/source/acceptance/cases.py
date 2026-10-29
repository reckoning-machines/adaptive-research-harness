"""Executable adversarial schedules through the real protected boundaries only."""
from copy import deepcopy
from pathlib import Path
import time
from adaptive_research_harness.encoding import digest,instant
from .runtime import expect,key


def seq(response):return response['refs'][0]['sequence']
def settlement(a,actual='1.00'):
    return {'attempt':a,'actual':actual,'unit':'simulated_research_units','provenance':{'kind':'UNKNOWN'}}
def pending(r):return r.research(stop=True)['attempt']['sequence']
def require_refusal(response,reason=None):
    assert response.get('status') in ('REFUSED','ERROR'),response
    if reason:assert response.get('reason')==reason,response
    return response

def advance_head(r):
    r.fence('AU-CK-B');r.revoke('AU-CK-B',action='SUPERSEDE')

def mutable_candidate(r):
    candidate=r.candidate();p=r.read('get',{'ref':candidate['proposal']['refs'][0]})['body'];return deepcopy(p)

def negative_proposal(r,p,mutate):
    r.ordinal+=1;original=deepcopy(p['content']);changed=deepcopy(original);mutate(changed)
    changes=[]
    def diff(before,after,path):
        if isinstance(before,dict) and isinstance(after,dict):
            for k in before.keys()|after.keys():
                if k not in after:changes.append({'path':path+[k],'remove':True})
                elif k not in before:changes.append({'path':path+[k],'value':after[k]})
                else:diff(before[k],after[k],path+[k])
        elif before!=after:changes.append({'path':path,'value':after})
    diff(original,changed,[])
    rr=next(ref for ref in original['motivated_by'] if isinstance(ref,dict))
    candidate=r.agent('r01','propose-mutated',{'research_ref':rr,'case':r.case,'ordinal':r.ordinal,'mutations':changes})
    expect(candidate['proposal']);tr=candidate['transition_id']
    expect(r.adversarial('r01','reserve',{'grant':'AU-RP-1','amount':'2.00','purpose':{'kind':'Transition','id':tr},'expected_sequence':candidate['funding_ref']}))
    return tr


def R01(r):
    require_refusal(r.adversarial('r01','fence',{'grant':'AU-RP-1','reason':'unauthorized'}),'UNAUTHORIZED')
    require_refusal(r.adversarial('r01','bind',{}))
    require_refusal(r.adversarial('r01','genesis',{}))
    assert r.read('state')['N']==16

def R02(r):
    for i in range(1,7):expect(r.reserve(f'r{i:02d}','90.00'))
    futures=[r.pool.submit(r.reserve,x,'40.00') for x in ('r07','r08')]
    values=[f.result() for f in futures]
    assert sorted(v['status'] for v in values)==['COMMITTED','REFUSED'],values
    require_refusal(next(v for v in values if v['status']=='REFUSED'),'BUDGET_EXCEEDED')
    assert r.read('budget',{'grant':'AU-RP-1'})['reserved']=='580.00'

def R03(r):
    a=pending(r);p=settlement(a);k=key();r.arm(k,'DROP_COMMAND_REPLY','after_settle_commit')
    first=r.adversarial('r01','settle',p,k);require_refusal(first)
    repeat=expect(r.adversarial('r01','settle',p,k));assert seq(repeat)>a
    require_refusal(r.adversarial('r01','settle',p),'ALREADY_SETTLED')
    assert len([e for e in r.history('E') if e['kind']=='SETTLEMENT' and e['body']['attempt']==a])==1

def R04(r):
    a=pending(r);r.fence();r.revoke();expect(r.settle(a));require_refusal(r.reserve(),'AUTHORIZATION_INACTIVE')
    assert r.read('budget',{'grant':'AU-RP-1'})['committed']=='1.00'

def R05(r):
    a=pending(r);base=settlement(a)
    for change in [{'unit':'USD'},{'actual':'-1.00'},{'actual':'NaN'},{'provenance':{}},{'attempt':999999}]:
        require_refusal(r.adversarial('r01','settle',dict(base,**change)),'INVALID_SETTLEMENT')
    require_refusal(r.adversarial('r02','settle',base),'INVALID_SETTLEMENT')
    assert a in r.read('obligations')['pending_attempts']

def R06(r):
    a=pending(r);r.arm(a,'AFTER_START_FAILURE');out=r.agent('r01','complete-research',{'attempt':a})
    expect(out['record']);expect(out['settlement']);assert out['failure']=='AFTER_START_FAILURE'
    record=r.read('get',{'ref':out['record']['refs'][0]});assert record['body']['failure']
    require_refusal(r.agent('r01','propose-hypothesis',{'research_ref':out['record']['refs'][0]}),'NO_POSITIVE_RESEARCH')

def R07(r):
    a=pending(r);r.host('restart');r.ready()
    require_refusal(r.agent('r01','complete-research',{'attempt':a}),'UNCERTAIN_OLD_ATTEMPT')
    expect(r.settle(a));retry=r.agent('r01','retry-research',{'attempt':a});assert 'attempt' in retry,retry
    assert retry['attempt']['sequence']!=a

def R08(r):
    a=pending(r);r.fence();out=r.agent('r01','complete-research',{'attempt':a});expect(out['settlement'])
    require_refusal(r.agent('r01','retry-research',{'attempt':a}),'FENCED')

def R09(r):
    a=pending(r);r.arm(a,'OVERRUN_601');out=r.agent('r01','complete-research',{'attempt':a});expect(out['settlement'])
    assert r.read('budget',{'grant':'AU-RP-1'})['committed']=='601.00'
    require_refusal(r.reserve(),'OVERSPENT')

def R10(r):
    start=r.research(stop=True);a=start['attempt']['sequence'];expect(r.adversarial('r01','close',{'reservation':start['reservation']['sequence']}))
    assert r.read('budget',{'grant':'AU-RP-1'})['reserved']=='1.00';expect(r.settle(a))

def R11(r):
    p,body=r.decided();advance_head(r)
    refusal=r.call('apply',body);require_refusal(refusal,'STALE_CHECK')
    bindings=[e for e in r.history('E') if e['kind']=='BIND' and e['body']['transition_id']==p['transition_id']]
    if bindings:expect(r.call('release',{'bind':bindings[-1]['seq']}))
    check=r.check(p['transition_id']);decision=r.decision(p['transition_id'],check,True)
    expect(r.call('apply',{'transition_id':p['transition_id'],'decision':decision}))

def R12(r):
    p=r.candidate();require_refusal(r.agent('r01','check',{'transition_id':p['transition_id']}))
    g=deepcopy(r.read('state')['grants']['AU-CK-A']);g['AuthorizationId']='AU-CK-A-R12-1'
    tr,response=r.propose_control('AUTHORIZATION',g['AuthorizationId'],{'action':'SUPERSEDE','predecessor':'AU-CK-A','grant':g});expect(response)
    own=r.check(tr,passed=False);require_refusal(own,'PURPOSE_OUT_OF_SCOPE')

def R13(r):
    require_refusal(r.adversarial('r01','standing',{'subject':'H-SYN-1','standing':'SUPPORTED'}),'CAPABILITY_UNSUPPORTED')
    require_refusal(r.adversarial('r01','observation-commit',{'grant':'AU-OBS-1','source':'SRC-SYN','revision':'wrong','form':'DOCUMENT','period':{},'item_id':'forged','document':{},'slot':0}),'UNAUTHORIZED')

def R14(r):
    p=mutable_candidate(r)
    mutations=[lambda c:c.update(resolution_source=None),lambda c:c['selection_basis'].update(time_estimate_ms=None),lambda c:c['initial_method'].update(sha256='0'*64),lambda c:c['resolution_period'].update(start='2026-10-28T00:00:00.000Z')]
    for mutate in mutations:
        tr=negative_proposal(r,p,mutate)
        for actor in ('ck1','ck2'):
            result=r.check(tr,actor,False);expect(result['check']);assert result['computed_result']=='FAIL',result

def R15(r):
    p=r.candidate();ref=p['proposal']['refs'][0];before=r.read('get',{'ref':ref});r.host('restart');r.ready()
    assert r.read('get',{'ref':ref})==before
    assert r.read('state',{'N':0})['active']==['AU-CK-A']

def R16(r):
    p=r.profile;design=next(x['content'] for x in p['artifacts']['designs'] if x['content']['AgentDesignVersionId']=='AD-CK-1.0');grant=next(x['content'] for x in p['setup']['grants'] if x['content']['AuthorizationId']=='AU-CK-A')
    require_refusal(r.call('genesis',{'constitution_sha256':p['setup']['constitution']['sha256'],'design':design,'grant':grant}),'GENESIS_SCOPE')
    require_refusal(r.call('genesis',{'constitution_sha256':p['setup']['constitution']['sha256'],'design':design,'grant':grant,'extra_grant':{}}))
    assert r.read('state')['N']==16

def B01(r):
    p,body,bind=r.bound();expect(r.call('recover',{'continue':True,'transition_id':p['transition_id']}))
    assert r.read('obligations')['bindings'][str(bind['seq'])]=='CONSUMED'

def B02(r):
    p,body,bind=r.bound();r.fence();expect(r.call('apply',body));require_refusal(r.reserve(),'FENCED')

def B03(r):
    p,body,bind=r.bound();r.fence();r.revoke();ref=require_refusal(r.call('apply',body))
    assert len(ref['refs'])==2;expect(r.call('release',{'bind':bind['seq']}))

def B04(r):
    p,body,bind=r.bound();tick=bind['body']['time_ms']-instant(r.profile['setup']['clock']['epoch'])+300000
    r.tick(tick);require_refusal(r.call('invalidate-request',{'bind':bind['seq']}),'INTERVAL_NOT_ELAPSED')
    r.tick(tick+1);expect(r.call('invalidate-request',{'bind':bind['seq']}));expect(r.call('release',{'bind':bind['seq']}))

def B05(r):
    p,body,bind=r.bound();r.tick(301001)
    # Concurrent calls; the separate D-terminal schedules below force both orders.
    fs=[r.pool.submit(r.call,'apply',body),r.pool.submit(r.call,'invalidate-request',{'bind':bind['seq']})]
    results=[f.result() for f in fs];assert sum(x['status']=='COMMITTED' for x in results)==1,results
    terminal=r.read('obligations')['bindings'][str(bind['seq'])];assert terminal in ('CONSUMED','PENDING_RELEASE')
    if terminal=='PENDING_RELEASE':expect(r.call('release',{'bind':bind['seq']}))

def B06(r):
    p,body,bind=r.bound();advance_head(r);k=key();r.arm(k,'PAUSE_AT_BOUNDARY','before_apply_commit')
    r.pool.submit(r.call,'apply',body,k);r.barrier('before_apply_commit');r.host('restart');r.ready()
    assert r.read('obligations')['bindings'][str(bind['seq'])]=='FROZEN'
    result=require_refusal(r.call('apply',body));assert len(result['refs'])==2
    expect(r.call('release',{'bind':bind['seq']}))

def B07(r):
    p,body,bind=r.bound();r.tick(301001);expect(r.call('invalidate-request',{'bind':bind['seq']}));r.host('restart');r.ready()
    assert r.read('obligations')['bindings'][str(bind['seq'])]=='PENDING_RELEASE'
    expect(r.call('recover',{'continue':True,'transition_id':p['transition_id']}))

def B08(r):
    p,body,bind=r.bound();expect(r.call('apply',body));require_refusal(r.call('apply',body),'ALREADY_APPLIED')
    require_refusal(r.call('release',{'bind':bind['seq']}),'NO_INVALIDATION');require_refusal(r.call('invalidate-request',{'bind':bind['seq']}),'BINDING_TERMINAL')

def B09(r):
    p,body,bind=r.bound();r.tick(301001);expect(r.call('invalidate-request',{'bind':bind['seq']}));expect(r.call('release',{'bind':bind['seq']}))
    c=r.check(p['transition_id']);d=r.decision(p['transition_id'],c,True)
    expect(r.call('apply',{'transition_id':p['transition_id'],'decision':d}));require_refusal(r.call('apply',body),'ALREADY_APPLIED')
    require_refusal(r.call('release',{'bind':bind['seq']}),'ALREADY_RELEASED')

def B10(r):
    p,body,bind=r.bound();r.host('stop',unit='harness-core.service')
    try:r.call('release',{'bind':bind['seq']})
    except (OSError,EOFError):pass
    else:raise AssertionError('Unavailable owner supplied a result')
    r.host('start',unit='harness-core.service');r.ready();assert r.read('obligations')['bindings'][str(bind['seq'])]=='FROZEN'

def B11(r):
    p,body,bind=r.bound();r.tick(604801001)
    require_refusal(r.adversarial('r01','close',{'reservation':p['funding_ref']}),'RESERVATION_BOUND')
    expect(r.call('invalidate-request',{'bind':bind['seq']}));expect(r.call('release',{'bind':bind['seq']}))
    require_refusal(r.call('apply',{'transition_id':p['transition_id'],'decision':body['decision']}),'RESERVATION_CLOSED')

def B12(r):
    p,body,bind=r.bound()
    r.control('SUSPEND_POLICY','P-1',{'policy':'P-1','scope':'AU-RP-1','action':'SUSPEND','reason':'B12 authorized existing control'},checker='ck2')
    result=require_refusal(r.call('apply',body));assert len(result['refs'])==2
    expect(r.call('release',{'bind':bind['seq']}));c=r.check(p['transition_id'])
    require_refusal(r.call('policy-decide',{'transition_id':p['transition_id'],'check':c}),'POLICY_SUSPENDED')

def C01(r):
    k=key();r.arm(k,'PAUSE_AT_BOUNDARY','before_reserve_commit');future=r.pool.submit(r.reserve,'r01','1.00',k)
    barrier=r.barrier('before_reserve_commit')
    result=r.host('competing-core');assert result['returncode']==0 and 'INSTANCE_ALREADY_RUNNING' in result['stdout'],result
    r.host('release-barrier',path=barrier['path']);expect(future.result())
    C02(r)

def C02(r):
    k=key();fs=[r.pool.submit(r.reserve,'r01','1.00',k) for _ in range(2)];a,b=[f.result() for f in fs]
    expect(a);assert a==b;require_refusal(r.reserve('r01','2.00',k),'REQUEST_KEY_CONFLICT')
    r.host('restart');r.ready();assert r.reserve('r01','1.00',k)==a

def C03(r):
    a=pending(r);fs=[r.pool.submit(r.agent,'r01','complete-research',{'attempt':a}) for _ in range(2)]
    for f in fs:f.result()
    claims=r.read('dispatch-status')['claims'];assert len([x for x in claims if x['attempt']==a])==1
    assert len([e for e in r.history('E') if e['kind']=='SETTLEMENT' and e['body']['attempt']==a])==1

def C04(r):
    a=pending(r);r.arm(a,'PAUSE_AT_BOUNDARY');r.pool.submit(r.agent,'r01','complete-research',{'attempt':a});r.barrier()
    r.host('kill',unit='harness-core.service');r.host('start',unit='harness-core.service');r.ready();expect(r.settle(a))
    require_refusal(r.agent('r01','retry-research',{'attempt':a}),'WORKER_NOT_QUIESCENT')
    proof=r.host('restart')['proof'];assert proof['old_channels_closed'] and proof['terminated_generations'];r.ready()
    result=r.agent('r01','retry-research',{'attempt':a});assert 'attempt' in result,result

def C05(r):
    base=mutable_candidate(r);prospective=(r.read('clock')['E'] or 0)+1
    proposals=[]
    for i in (1,2):
        p=deepcopy(base);p.update(transition_id=f'TR-C05-{i}',funding_ref=prospective)
        rr=next(ref for ref in p['content']['motivated_by'] if isinstance(ref,dict))
        candidate=r.agent('r01','propose-mutated',{'research_ref':rr,'case':'C05','ordinal':i,'transition_id':p['transition_id'],'funding_ref':prospective})
        expect(candidate['proposal']);proposals.append(p)
    def reserve_for(p,k=None):return r.adversarial('r01','reserve',{'grant':'AU-RP-1','amount':'2.00','purpose':{'kind':'Transition','id':p['transition_id']},'expected_sequence':p['funding_ref']},k)
    fs=[r.pool.submit(reserve_for,p) for p in proposals];out=[f.result() for f in fs]
    assert sum(x['status']=='COMMITTED' for x in out)==1,out
    loser=proposals[next(i for i,x in enumerate(out) if x['status']!='COMMITTED')]
    c=r.check(loser['transition_id'],passed=False);assert c['computed_result']=='FAIL'
    check=r.read('get',{'ref':c['check']['refs'][0]});assert check['body']['criteria']['funding']['status']=='NOT MET'
    p=deepcopy(base);p.update(transition_id='TR-C05-3',funding_ref=(r.read('clock')['E'] or 0)+1)
    rr=next(ref for ref in p['content']['motivated_by'] if isinstance(ref,dict))
    expect(r.agent('r01','propose-mutated',{'research_ref':rr,'case':'C05','ordinal':3,'transition_id':p['transition_id'],'funding_ref':p['funding_ref']})['proposal']);expect(r.agent('observe','observe'))
    require_refusal(reserve_for(p),'FUNDING_REFERENCE_TAKEN')
    p=deepcopy(base);p.update(transition_id='TR-C05-4',funding_ref=(r.read('clock')['E'] or 0)+1)
    expect(r.agent('r01','propose-mutated',{'research_ref':rr,'case':'C05','ordinal':4,'transition_id':p['transition_id'],'funding_ref':p['funding_ref']})['proposal']);k=key();r.arm(k,'DROP_COMMAND_REPLY','after_reserve_commit')
    require_refusal(reserve_for(p,k));lookup=r.agent('r01','inspect-request',{'request_id':k});expect(lookup)
    assert seq(lookup)==p['funding_ref'];assert reserve_for(p,k)==lookup


def C06(r):
    a=pending(r);r.host('stop',unit='harness-clock.service');expect(r.settle(a));require_refusal(r.reserve(),'CLOCK_UNAVAILABLE')
    r.host('start',unit='harness-clock.service');r.ready()
    r.tick(2000);r.host('rollback-clock');require_refusal(r.reserve(),'CLOCK_ROLLBACK')
    r.host('restore-clock');r.ready()
    now=r.read('clock')['t'];require_refusal(r.adversarial('r01','reserve',{'grant':'AU-RP-1','amount':'1.00','purpose':{'kind':'Theme','id':'TH-G1'},'expiry_ms':now+604800001}),'INVALID_EXPIRY')

def C07(r):
    p=mutable_candidate(r);p['transition_id']='TR-C07-1'
    require_refusal(r.call('propose',dict(p,acting_as='AD-R1.0')))
    require_refusal(r.call('recover',{'acting_as':'AD-R1.0','continue':True,'transition_id':p['transition_id']}))
    RR=[x for x in r.history('E') if x['kind']=='RESEARCH_RECORD' and x['actor']=='AD-R1.0'];assert RR
    assert RR[-1]['body']['tool']['executable_hash']==r.profile['inventory']['tool_executables']['SYN-A-1']

def S01(r):r.assert_startup()
def S02(r):
    originals={x['content']['AuthorizationId']:x['content'] for x in r.profile['setup']['grants']}
    for ident,path in [('AU-RP-1',('binding_interval_ms',)),('AU-RP-1',('tools',0,'tier')),('AU-OBS-1',('source_declarations',1,'content','resolution_grace_ms')),('AU-OBS-1',('source_declarations',1,'content','enumeration_contract'))]:
        c=deepcopy(originals[ident]);target=c
        for k in path[:-1]:target=target[k]
        target[path[-1]]=None;tr,pr=r.propose_control('AUTHORIZATION',ident,{'action':'GRANT','predecessor':None,'grant':c});expect(pr)
        for actor in ('ck1','ck2'):
            result=r.check(tr,actor,False);assert result['computed_result']=='FAIL',result

def S03(r):
    limits=deepcopy(r.profile['setup']['initial_limits']);limits['portfolio_capital_units']='-1.00'
    _,p=r.propose_control('LIMITS','negative',limits);require_refusal(p)
    limits['portfolio_capital_units']=None;tr,p=r.propose_control('LIMITS','missing',limits);expect(p)
    assert r.check(tr,passed=False)['computed_result']=='FAIL'

def S04(r):
    original=next(x['content'] for x in r.profile['artifacts']['designs'] if x['content']['AgentDesignVersionId']=='AD-R1.0')
    for change in [{'initial_method':None},{'instructions':'changed bytes under admitted id'},{'authorization_request':'AU-RP-1'},{}]:
        c=dict(deepcopy(original),**change);tr,p=r.propose_control('AGENT_DESIGN',c['AgentDesignVersionId'],c);expect(p)
        assert r.check(tr,passed=False)['computed_result']=='FAIL'

    successor=r.agent('r01','propose-successor',{'case':'S04','ordinal':r.ordinal+1})
    expect(successor['proposal']);expect(successor['funding']);c=r.check(successor['transition_id']);d=r.decision(successor['transition_id'],c,True)
    expect(r.call('apply',{'transition_id':successor['transition_id'],'decision':d}))
    state=r.read('state');assert successor['successor'] in state['designs']
    assert not any(successor['successor'] in g['grantee'] for k,g in state['grants'].items() if k in state['active'])

def S05(r):R14(r)
def S06(r):
    g=deepcopy(r.read('state')['grants']['AU-CK-A']);g['AuthorizationId']='AU-CK-A-S06-1'
    tr,p=r.propose_control('AUTHORIZATION',g['AuthorizationId'],{'action':'SUPERSEDE','predecessor':'AU-CK-A','grant':g});expect(p)
    own=r.check(tr,passed=False);require_refusal(own,'PURPOSE_OUT_OF_SCOPE')
    r.fence('AU-CK-A');c=r.check(tr,'ck2');d=r.decision(tr,c);expect(r.call('apply',{'transition_id':tr,'decision':d}))

def S07(r):
    p=r.candidate();r.host('pause-actor',actor='ck1',point='checker_during_computation');r.pool.submit(r.check,p['transition_id']);r.barrier('checker_during_computation')
    pending_before=r.read('obligations')['pending_attempts'];assert pending_before
    r.host('restart');r.ready()
    for a in pending_before:
        result=r.agent('ck1','settle-pending',{'attempt':a});expect(result)
    assert not any(x['kind']=='CHECK' and x['transition_id']==p['transition_id'] for x in r.history('T'))

def S08(r):
    probe=r.host('artifact-probe');assert probe['status']=='CANDIDATE_REFUSED' and probe['reason']=='ARTIFACT_CHANGED',probe
    p=mutable_candidate(r);tr=negative_proposal(r,p,lambda c:c.update(template_id='UNKNOWN-SCIENCE'))
    result=r.check(tr,passed=False);assert result['check']['status']=='CAPABILITY_UNSUPPORTED',result
    assert not any(x['kind']=='CHECK' and x['transition_id']==tr for x in r.history('T'))
    r.verify_artifacts()

def T01(r):
    a=r.research('SYN-A-1');b=r.research('SYN-B-1')
    x=r.read('get',{'ref':a['record']['refs'][0]});y=r.read('get',{'ref':b['record']['refs'][0]})
    assert x['body']['result']==y['body']['result'];assert x['body']['tool']['executable_hash']!=y['body']['tool']['executable_hash']
    assert r.read('budget',{'grant':'AU-RP-1'})['committed']=='2.00'

def T02(r):
    r.fence();before=len(r.read('dispatch-status')['claims'])
    for tool in ('SYN-A-1','SYN-B-1'):require_refusal(r.agent('r01','research',{'tool':tool}),'FENCED')
    assert len(r.read('dispatch-status')['claims'])==before

def T03(r):
    start=r.research('SYN-B-1',True);a=start['attempt']['sequence'];r.arm(a,'FOREIGN_AUTHORITY_OUTPUT');out=r.agent('r01','complete-research',{'attempt':a});expect(out['record'])
    result=r.read('get',{'ref':out['record']['refs'][0]})['body']['result'];assert result['approval']=='ADMITTED'
    assert r.read('state')['N']==16 and 'FORGED-NO-AUTHORITY' not in r.read('state')['grants']

def T04(r):
    p,body,bind=r.bound();a=pending(r)
    require_refusal(r.adversarial('r02','settle',settlement(a)),'INVALID_SETTLEMENT')
    attempt=next(e['body'] for e in r.history('E') if e['kind']=='ATTEMPT' and e['seq']==a)
    change={k:attempt[k] for k in ('step','input','dispatch_index','maximum','tier')};change['reservation']=p['funding_ref']
    require_refusal(r.adversarial('r01','attempt',change),'RESERVATION_BOUND')
    assert a in r.read('obligations')['pending_attempts'];assert r.read('obligations')['bindings'][str(bind['seq'])]=='FROZEN'

def T05(r):
    a=pending(r);body=next(e['body'] for e in r.history('E') if e['kind']=='ATTEMPT' and e['seq']==a)
    p={k:deepcopy(body[k]) for k in ('reservation','step','input','dispatch_index','maximum','tier')};p['input']['tool_id']='UNDECLARED'
    result=r.adversarial('r01','attempt',p);require_refusal(result)
    assert not any(x['claim']['tool_id']=='UNDECLARED' for x in r.read('dispatch-status')['claims'])

def T06(r):
    result=r.host('probe-isolation');assert len(result['probes'])==9 and all(x['denied'] for x in result['probes']),result

def T07(r):
    # Actor-field injection is submitted by a real researcher process, not by
    # a Principal socket claiming to emulate it. Dedicated actor probe below.
    result=r.agent('r01','peer-impersonation',{'actor':'Principal'})
    require_refusal(result,'ACTOR_MISMATCH')

def E01(r):
    research=r.research('SYN-A-1');rr=research['record']['refs'][0]
    candidate=r.agent('r01','propose-hypothesis',{'research_ref':rr});expect(candidate['proposal']);expect(candidate['funding'])
    check=r.check(candidate['transition_id']);decision=r.decision(candidate['transition_id'],check,True)
    applied=expect(r.call('apply',{'transition_id':candidate['transition_id'],'decision':decision}))
    expect(r.agent('r01','close-reservation',{'reservation':candidate['funding_ref']}))
    replacement=r.research('SYN-B-1')
    first=r.read('get',{'ref':rr});second=r.read('get',{'ref':replacement['record']['refs'][0]})
    assert first['body']['result']==second['body']['result']
    assert r.read('budget',{'grant':'AU-RP-1'})['committed']=='2.00'
    assert r.read('budget',{'grant':'AU-CK-A'})['committed']=='4.25'
    assert r.read('state')['N']==17
    r.trace.append({'worked_example':{'question':first['body']['question'],'counts':first['body']['result'],
      'research_cost':'2.00 simulated units across A and B','checker_cost':'0.25 for registration plus 4.00 startup',
      'evidence':rr,'applied':applied['refs'][0],'classification':'Synthetic Historical Reconstruction; no forward or economic standing',
      'next_permitted_action':'Inspect exact admitted hypothesis and spendable budgets; propose another bounded experiment only under current grant. Prediction/standing execution is outside this build.'}})


def X01(r):
    first,body=r.decided();second,other,binding=r.bound()
    body['bind']=binding['seq']
    result=require_refusal(r.call('apply',body),'WRONG_BINDING')
    assert len(result['refs'])==1,result
    assert r.read('obligations')['bindings'][str(binding['seq'])]=='FROZEN'
    expect(r.call('apply',other))

def X02(r):
    p,body,bind=r.bound();r.tick(301001)
    for op,payload in [('invalidate-request',{'bind':bind['seq']}),('release',{'bind':bind['seq']}),('policy-decide',{'transition_id':p['transition_id'],'check':1})]:
        require_refusal(r.adversarial('r02',op,payload),'UNAUTHORIZED')
    require_refusal(r.adversarial('r01','invalidate-request',{'bind':bind['seq']}),'UNAUTHORIZED')
    require_refusal(r.adversarial('r02','recover',{'transition_id':p['transition_id'],'continue':True}),'UNAUTHORIZED')
    invalid=expect(r.call('invalidate-request',{'bind':bind['seq']}))
    event=r.read('get',{'ref':invalid['refs'][0]});assert event['body']['requester']=='Principal' and event['body']['acting_role']=='@Apply'
    expect(r.call('release',{'bind':bind['seq']}))

def X03(r):
    p=mutable_candidate(r);p['transition_id']='TR-R14-driver';p['funding_ref']=(r.read('clock')['E'] or 0)+1
    require_refusal(r.adversarial('r01','propose',p),'INVALID_CASE')

def X04(r):
    g=deepcopy(r.read('state')['grants']['AU-CK-A']);g['AuthorizationId']='AU-CK-A-R12-1'
    tr,response=r.propose_control('AUTHORIZATION',g['AuthorizationId'],{'action':'SUPERSEDE','predecessor':'AU-CK-A','grant':g});expect(response)
    before=r.read('budget',{'grant':'AU-CK-A'})
    require_refusal(r.agent('ck1','reserve',{'grant':'AU-CK-A','amount':'0.25','purpose':{'kind':'Check','id':tr}}),'PURPOSE_OUT_OF_SCOPE')
    after=r.read('budget',{'grant':'AU-CK-A'});assert (before['committed'],before['reserved'])==(after['committed'],after['reserved'])


def X05(r):
    from adaptive_research_harness.encoding import raw_digest
    profile=r.read('profile');h=profile['inventory_sha256']
    root=__import__('pathlib').Path(__file__).resolve().parents[1]
    archive=root/'artifacts/development/builds'/h
    assert raw_digest((archive/'inventory.json').read_bytes())==h
    for item in profile['inventory']['files']:
        assert raw_digest((archive/'source'/item['path']).read_bytes())==item['sha256']
    result=r.host('artifact-probe');assert result['reason']=='ARTIFACT_CHANGED' and result['actual_candidate_bytes_changed']
