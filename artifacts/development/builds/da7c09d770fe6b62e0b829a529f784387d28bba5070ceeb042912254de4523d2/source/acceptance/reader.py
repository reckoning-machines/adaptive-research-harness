"""Independent history replay: no core model, Rules or admission functions imported.

This checks the supported synthetic contracts, not arbitrary CV1 interpretations.
Equal timestamps are not cross-ledger ordering; Evidence admission witnesses pin N.
"""
from copy import deepcopy
from adaptive_research_harness.client import Client
from adaptive_research_harness.encoding import digest,units,canonical,instant
from adaptive_research_harness.contracts import COMMON,CLASS_CRITERIA


def _audit(es,ts):
    for rows in (es,ts):
        assert [x['seq'] for x in rows]==list(range(1,len(rows)+1)),'sequence'
        assert all(digest(x['body'])==x['sha256'] for x in rows),'body hash'
    ei={e['seq']:e for e in es};ti={e['seq']:e for e in ts}
    proposals={e['transition_id']:e for e in ts if e['kind']=='PROPOSED'}
    assert len(proposals)==sum(e['kind']=='PROPOSED' for e in ts),'duplicate proposal'
    applied=[x for x in ts if x['kind']=='APPLIED']
    assert [x['body']['n'] for x in applied]==list(range(len(applied))),'Apply order'
    assert len({x['transition_id'] for x in applied})==len(applied),'duplicate Apply'
    assert applied and applied[0]['body']['n']==0,'missing genesis'
    states={};s={'grants':{},'active':set(),'designs':{},'suspended':set(),'themes':set()}
    for e in applied:
        b=e['body'];p=proposals[e['transition_id']]
        if b['n']==0:
            assert p['body']['class']=='GENESIS' and e['transition_id']=='TR-0','genesis scope'
            assert [x['kind'] for x in ts[:3]]==['PROPOSED','DECISION','APPLIED'],'nonempty genesis'
            g=b['genesis'];assert set(g)=={'constitution_sha256','design','grant'},'genesis extras'
            s['grants'][g['grant']['AuthorizationId']]=g['grant'];s['active'].add(g['grant']['AuthorizationId'])
            s['designs'][g['design']['AgentDesignVersionId']]=g['design']
        else:
            c=p['body']['content'];typ=p['body']['class']
            if typ=='AUTHORIZATION':
                if c['predecessor']:s['active'].discard(c['predecessor'])
                s['grants'][c['grant']['AuthorizationId']]=c['grant']
                if c['action']!='REVOKE':s['active'].add(c['grant']['AuthorizationId'])
            elif typ=='AGENT_DESIGN':s['designs'][c['AgentDesignVersionId']]=c
            elif typ=='THEME':s['themes'].add(c['ThemeId'])
            elif typ=='SUSPEND_POLICY':s['suspended'].add(c['scope'])
        states[b['n']]=deepcopy(s)
    bindings={e['seq']:e for e in es if e['kind']=='BIND'}
    invalidations={};consumed={};releases={}
    def exact(ref):
        assert ref['ledger'] in ('E','T'),'reference ledger'
        e=(ei if ref['ledger']=='E' else ti).get(ref['sequence'])
        assert e and e['sha256']==ref['sha256'],'reference hash';return e
    def independent(state,actor,grant,p):
        assert actor in state['designs'] and grant['class']=='Checker','Checker role'
        own=state['designs'][actor]['AgentDesignLineageId'];author=p['actor']
        assert actor!=author and (author not in state['designs'] or state['designs'][author]['AgentDesignLineageId']!=own),'Checker lineage'
        assert not any(g['class']=='Research' and actor in g['grantee'] for k,g in state['grants'].items() if k in state['active']),'Research Checker'
        c=p['body']['content'];typ=p['body']['class']
        if typ=='AGENT_DESIGN':assert c['AgentDesignLineageId']!=own,'own design'
        if typ=='AUTHORIZATION':
            assert actor not in c['grant']['grantee'] and c['predecessor']!=grant['AuthorizationId'],'own grant'
        assert grant['forbidden_subjects'],'Checker exclusion absent'
        for text in grant['forbidden_subjects']:
            if text.endswith(' lineage and every successor') and typ=='AGENT_DESIGN':assert c['AgentDesignLineageId']!=text.removesuffix(' lineage and every successor'),'forbidden lineage'
            if text.endswith(' and its successor chain') and typ=='AUTHORIZATION':
                root=text.removesuffix(' and its successor chain');chain={root}
                for a in applied:
                    if a['body']['n']>p['body']['base']:break
                    old=proposals[a['transition_id']]['body']
                    if old['class']=='AUTHORIZATION' and old['content']['predecessor'] in chain:chain.add(old['content']['grant']['AuthorizationId'])
                assert c['predecessor'] not in chain and c['grant']['AuthorizationId'] not in chain,'forbidden grant chain'
    for e in ts:
        b=e['body'];tr=e['transition_id']
        if e['kind']=='CHECK':
            p=proposals[tr];assert p['seq']<e['seq'],'Check precedes proposal'
            state=states[b['base']];g=state['grants'][b['grant']]
            assert b['grant'] in state['active'] and e['actor'] in g['grantee'] and e['time_ms']<instant(g['expiry']),'Check authorization'
            independent(state,e['actor'],g,p)
            assert set(b['criteria'])==set(COMMON+CLASS_CRITERIA[p['body']['class']]),'Check criteria'
            statuses={c['status'] for c in b['criteria'].values()}
            assert statuses<= {'MET','NOT MET','NOT DETERMINABLE'},'Check status'
            expected='STOP' if 'NOT DETERMINABLE' in statuses else 'FAIL' if 'NOT MET' in statuses else 'PASS'
            assert b['result']==expected,'Check result'
            a=ei[b['attempt']];assert a['kind']=='ATTEMPT' and a['actor']==e['actor'] and a['body']['grant']==b['grant'],'Check attempt'
            r=ei[a['body']['reservation']];assert r['body']['purpose']=={'kind':'Check','id':tr},'separate Checker funding'
            assert b['closure']['N']==b['base'] and a['seq']<=b['closure']['E']<=len(es),'Check closure'
            for c in b['criteria'].values():
                for ref in c['refs']:
                    exact(ref)
                    if ref['ledger']=='E':assert ref['sequence']<=b['closure']['E'],'Check outside closure'
        elif e['kind']=='APPLIED' and b['n']>0:
            p=proposals[tr];d=ti[b['decision']];c=ti[b['check']]
            assert d['kind']=='DECISION' and d['transition_id']==tr and d['body']['decision']=='ADMITTED','Apply decision'
            assert c['kind']=='CHECK' and c['transition_id']==tr and c['body']['result']=='PASS','Apply PASS'
            assert d['body']['check']==c['seq'] and c['body']['base']==d['body']['base']==b['n']-1,'Apply base'
            assert p['seq']<c['seq']<d['seq']<e['seq'],'admission order'
            assert not p['body']['content'].get('adversarial_case'),'admitted adversarial input'
            state=states[b['n']-1]
            if p['actor']=='Principal':
                assert p['body']['grant'] is None and p['body']['funding_ref'] is None and units(p['body']['budget'])==0 and b['bind'] is None,'Principal funding'
                assert d['actor']=='Principal' and d['body']['decider']=='Principal','Principal decision'
            else:
                g=state['grants'][p['body']['grant']]
                assert p['body']['grant'] in state['active'] and p['actor'] in g['grantee'] and e['time_ms']<instant(g['expiry']),'Apply authority'
                bind=bindings[b['bind']];assert bind['body']['transition_id']==tr and bind['body']['decision']==d['seq'],'Apply binding relationship'
                assert bind['body']['reservation']==p['body']['funding_ref'],'Apply funding pointer'
                assert b['bind'] not in consumed and b['bind'] not in invalidations,'binding terminal'
                consumed[b['bind']]=b['n']
                if d['body']['decider'].startswith('P-1'):
                    assert d['actor']=='@Apply' and p['body']['class'] in ('HYPOTHESIS','AGENT_DESIGN'),'P-1 class'
                    assert p['body']['grant'] not in state['suspended'],'P-1 suspension'
                else:assert d['actor']=='Principal','decision authority'
        elif e['kind']=='BINDING_INVALIDATED':
            bind=bindings[b['bind']];assert bind['body']['transition_id']==tr,'cross-Transition invalidation'
            assert b['bind'] not in invalidations and b['bind'] not in consumed,'double disposition'
            if b['ground']=='APPLY_REFUSED':
                refusal=exact(b['refusal']);request=refusal['body']['request']
                assert refusal['kind']=='REFUSAL' and refusal['transition_id']==tr and refusal['body']['op']=='apply','invalidation refusal'
                assert request['bind']==bind['seq'] and request['transition_id']==tr and request['decision']==bind['body']['decision'],'refusal binding relationship'
                assert refusal['body']['reason']==b['reason'],'invalidation reason'
                assert refusal['command']==dict(e['command'],position=refusal['command']['position']) if refusal.get('command') and e.get('command') else True,'atomic receipt'
            else:
                assert b['ground']=='INTERVAL_ELAPSED','invalidation ground'
                assert b['clock']['t']-bind['body']['time_ms']>bind['body']['interval_ms'],'interval'
                assert b['requester']=='Principal' and b['acting_role']=='@Apply','continuation identity'
            invalidations[b['bind']]=e
    attempts={};settled={};reservations={};closed=set();fenced=set();seen_binds={};legacy=0
    def state_at(e):
        nonlocal legacy
        w=e['body'].get('witness')
        if w:
            assert w['E']==e['seq']-1 or (w['E'] is None and e['seq']==1),'Evidence witness'
            return states[w['N']],w['N']
        legacy+=1
        # Legacy histories lack enough cross-ledger ordering evidence. They can
        # be inspected, but are explicitly reported as weaker than current runs.
        return states[max(states)],max(states)
    def amounts(seq,now,n):
        r=reservations[seq]['body'];actual=pending=0
        for a in attempts.values():
            if a['body']['reservation']!=seq:continue
            if a['seq'] in settled:actual+=units(settled[a['seq']]['body']['actual'])
            else:pending+=units(a['body']['maximum'])
        frozen=any(e['body']['reservation']==seq and k not in releases and not (k in consumed and consumed[k]<=n) for k,e in seen_binds.items())
        end=seq in closed or r['grant'] in fenced or r['grant'] not in states[n]['active'] or (not frozen and now is not None and now>=r['expiry_ms'])
        c=actual+pending
        return c,c if end else max(units(r['amount']),c),max(units(r['amount'])-c,0),frozen,end
    def totals(grant,now,n,lineage=None,discovery=False):
        rows=[seq for seq,r in reservations.items() if (r['body']['lineage']==lineage if lineage else r['body']['grant']==grant) and (not discovery or r['body']['purpose']['kind']=='Discovery')]
        values=[amounts(seq,now,n) for seq in rows];return sum(v[0] for v in values),sum(v[1] for v in values)
    for e in es:
        b=e['body'];kind=e['kind'];now=e['time_ms']
        if kind not in ('RESERVATION','ATTEMPT','SETTLEMENT','BIND','RELEASE','CLOSED','FENCE','RESEARCH_RECORD'):continue
        state,n=state_at(e)
        if kind=='RESERVATION':
            g=state['grants'][b['grant']];assert b['grant'] in state['active'] and e['actor']==b['actor'] and e['actor'] in g['grantee'],'reservation authorization'
            assert now<instant(g['expiry']) and b['grant'] not in fenced,'reservation eligibility'
            assert b['lineage']==state['designs'][e['actor']]['AgentDesignLineageId'],'reservation lineage'
            c,u=totals(b['grant'],now,n);a=units(b['amount']);assert c<=units(g['research_budget_units']) and u+a<=units(g['research_budget_units']),'reservation budget'
            assert totals(b['grant'],now,n,b['lineage'])[1]+a<=units(g['per_lineage_cap_units']),'lineage cap'
            assert now<b['expiry_ms']<=now+g['default_reservation_duration_ms'],'expiry duration'
            purpose=b['purpose']
            if g['class']=='Checker':
                assert purpose['kind']=='Check','Checker purpose';p=proposals[purpose['id']];independent(state,e['actor'],g,p)
            elif purpose['kind']=='Transition':
                p=proposals[purpose['id']];assert p['actor']==e['actor'] and p['body']['grant']==b['grant'] and p['body']['funding_ref']==e['seq'],'literal funding reference'
                assert a>=units(p['body']['budget']),'funding amount'
            elif purpose['kind']=='Theme':assert purpose['id'] in state['themes'] and purpose['id'] in g['scope_by_grantee'][e['actor']]['themes'],'Theme scope'
            elif purpose['kind']=='SearchFamily':assert purpose['id'] in g['scope_by_grantee'][e['actor']]['empirical_search_families'],'empirical scope'
            elif purpose['kind']=='Discovery':assert purpose['id']==g['discovery_scope']['SearchFamily'] and totals(b['grant'],now,n,discovery=True)[1]+a<=units(g['discovery_scope']['fixed_subgrant_units']),'discovery scope'
            reservations[e['seq']]=e
        elif kind=='ATTEMPT':
            r=reservations[b['reservation']]['body'];g=state['grants'][r['grant']]
            assert e['actor']==r['actor'] and b['grant']==r['grant'] and b['lineage']==r['lineage'],'attempt attribution'
            assert r['grant'] in state['active'] and now<instant(g['expiry']) and r['grant'] not in fenced,'attempt authorization'
            c,u,allowance,frozen,end=amounts(b['reservation'],now,n);a=units(b['maximum'])
            assert not frozen and not end and a<=allowance,'attempt reservation'
            total=totals(r['grant'],now,n)[0];assert total<=units(g['research_budget_units']) and a<=units(g['research_budget_units'])-total,'attempt headroom'
            assert totals(r['grant'],now,n,r['lineage'])[0]+a<=units(g['per_lineage_cap_units']),'attempt cap'
            inp=b['input'];assert digest(inp)==b['input_hash'],'invocation hash'
            for ref in inp['input_refs']:exact(ref)
            assert any(t['id']==inp['tool_id'] and t['spec_sha256']==inp['tool_spec_hash'] and t['tier']==b['tier'] for t in g['tools']),'tool permission'
            assert state['designs'][e['actor']]['tool_specs'].get(inp['tool_id'])==inp['tool_spec_hash'],'design tool'
            same=[a for a in attempts.values() if (a['body']['reservation'],a['body']['step'],a['body']['input_hash'])==(b['reservation'],b['step'],b['input_hash'])]
            assert b['dispatch_index']==len(same),'attempt index'
            if g['class']=='Checker':independent(state,e['actor'],g,proposals[r['purpose']['id']])
            attempts[e['seq']]=e
        elif kind=='SETTLEMENT':
            a=attempts[b['attempt']];assert b['attempt'] not in settled,'duplicate settlement'
            assert e['actor'] in (a['actor'],'Principal') and b['reservation']==a['body']['reservation'] and b['grant']==a['body']['grant'],'settlement attribution'
            assert b['unit']=='simulated_research_units','settlement unit';actual=units(b['actual'])
            if b['provenance']['kind']=='UNKNOWN':assert actual==units(a['body']['maximum']),'UNKNOWN maximum'
            else:
                receipt=b['provenance']['receipt'];assert receipt['attempt']==a['seq'] and receipt['input_hash']==a['body']['input_hash'] and receipt['actual']==b['actual'],'settlement provenance'
            settled[b['attempt']]=e
        elif kind=='FENCE':assert e['actor']=='Principal','fence authority';fenced.add(b['grant'])
        elif kind=='CLOSED':
            r=reservations[b['reservation']];assert e['actor']==r['actor'] and not amounts(r['seq'],now,n)[3],'close eligibility';closed.add(r['seq'])
        elif kind=='BIND':
            p=proposals[b['transition_id']];r=reservations[b['reservation']];g=state['grants'][r['body']['grant']]
            assert e['actor']=='@Apply' and p['body']['funding_ref']==r['seq'],'bind reference'
            assert r['body']['purpose']=={'kind':'Transition','id':p['transition_id']} and r['actor']==p['actor'] and r['body']['grant']==p['body']['grant'],'bind funding'
            assert units(r['body']['amount'])>=units(p['body']['budget']),'bind amount'
            c,u,allowance,frozen,end=amounts(r['seq'],now,n);assert not frozen and not end and r['body']['grant'] not in fenced,'bind eligibility'
            assert totals(r['body']['grant'],now,n)[0]<=units(g['research_budget_units']),'bind overspent'
            d=ti[b['decision']];assert d['kind']=='DECISION' and d['transition_id']==p['transition_id'] and d['body']['decision']=='ADMITTED','bind decision'
            assert b['interval_ms']==g['binding_interval_ms'],'bind interval';seen_binds[e['seq']]=e
        elif kind=='RELEASE':
            assert e['actor']=='@Apply' and b['bind'] not in releases and b['bind'] not in consumed,'release consumed/duplicate'
            assert b['bind'] in invalidations and b['invalidation']==invalidations[b['bind']]['seq'],'release exact invalidation';releases[b['bind']]=e
        elif kind=='RESEARCH_RECORD':
            a=attempts[b['attempt']];assert a['actor']==e['actor'] and a['body']['grant']==b['grant'],'research attribution'
            if not b.get('failure') and 'n_large' in b['result']:
                docs=[exact(ref) for ref in b['closure']['refs'] if ref['ledger']=='E'];doc=next(x['body']['document'] for x in docs if x['kind']=='OBSERVATION' and x['body']['form']=='DOCUMENT')
                rows=doc['rows'];spikes=[x for x in rows if x['spike']];large=[x for x in spikes if x['size_units']>=2]
                expected={'n':len(spikes),'k':sum(x['selling'] for x in spikes),'n_large':len(large),'k_large':sum(x['selling'] for x in large)}
                assert all(b['result'][k]==v for k,v in expected.items()),'research recomputation'
                assert b['result']['input_sha256']==digest(doc) and b['reproducibility']['result_hash']==digest(b['result']),'research binding'
    for p in proposals.values():
        if p['actor'] not in states[max(states)]['designs']:continue
        c=p['body']['content']
        if c.get('adversarial_case'):
            ref=c['adversarial_case']['derived_from'];r=exact(ref);assert r['kind']=='RESEARCH_RECORD' and r['actor']==p['actor'],'mutation origin'
        elif p['body']['class']=='HYPOTHESIS':
            refs=[ref for ref in c.get('motivated_by',[]) if isinstance(ref,dict)]
            assert any(exact(ref)['kind']=='RESEARCH_RECORD' and exact(ref)['actor']==p['actor'] for ref in refs),'researcher proposal origin'
        elif p['body']['class']=='AGENT_DESIGN':assert c['predecessor']==p['actor'],'successor origin'
    committed={}
    for seq,a in attempts.items():committed[a['body']['grant']]=committed.get(a['body']['grant'],0)+units(settled[seq]['body']['actual'] if seq in settled else a['body']['maximum'])
    status={str(k):'CONSUMED' if k in consumed else 'RELEASED' if k in releases else 'PENDING_RELEASE' if k in invalidations else 'FROZEN' for k in bindings}
    return {'status':'RECONSTRUCTED','N':len(applied)-1,'E':len(es),'pending_attempts':sorted(set(attempts)-set(settled)),
      'binding_states':status,'committed_hundredths':committed,'legacy_records_without_admission_witness':legacy,
      'preserved_refusals':sum(e['kind']=='REFUSAL' for e in es+ts),'synthetic_forward_standing':0,
      'next_operation':'Inspect remaining obligations and current authority; settle pending liabilities before retrying uncertain work.'}


def audit(es,ts):
    try:return _audit(es,ts)
    except (KeyError,TypeError,IndexError) as exc:raise AssertionError('Missing or malformed admission relationship: '+str(exc)) from exc


def read(client=None):
    client=client or Client('/run/adaptive-research-harness/core/commands.sock','Principal');records={}
    for ledger in ('E','T'):
        records[ledger]=[];after=0;through=None
        while True:
            p={'ledger':ledger,'after':after,'limit':1000}
            if through is not None:p['through']=through
            page=client.query('history',p);records[ledger]+=page['records'];after=page['next_after'];through=page['through']
            if after>=through or not page['records']:break
    result=audit(records['E'],records['T'])
    for grant,value in result['committed_hundredths'].items():assert units(client.query('budget',{'grant':grant})['committed'])==value,'budget projection mismatch'
    return result

if __name__=='__main__':print(canonical(read()).decode())
