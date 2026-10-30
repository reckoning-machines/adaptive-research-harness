"""Checker A: chronological replay and explicit criterion evaluation."""
from ..encoding import digest, units, instant, Refusal
from ..contracts import COMMON, CLASS_CRITERIA


def evaluate(snapshot, transition_id, actor, checker_grant, attempt, profile):
    events = snapshot['transitions']; evidence = snapshot['evidence']
    proposals = {}; designs = {}; grants = {}; active = set(); themes = {}; registered = []
    for event in events:
        b = event['body']
        if event['kind'] == 'PROPOSED': proposals[event['transition_id']] = event
        if event['kind'] != 'APPLIED' or b['n'] > snapshot['N']: continue
        if 'genesis' in b:
            g=b['genesis'];designs[g['design']['AgentDesignVersionId']]=g['design']
            grants[g['grant']['AuthorizationId']]=g['grant'];active.add(g['grant']['AuthorizationId'])
        else:
            p=proposals[event['transition_id']]['body']; c=p['content']; typ=p['class']
            if typ=='AUTHORIZATION':
                active.discard(c['predecessor']);grants[c['grant']['AuthorizationId']]=c['grant']
                if c['action']!='REVOKE':active.add(c['grant']['AuthorizationId'])
            elif typ=='AGENT_DESIGN':designs[c['AgentDesignVersionId']]=c
            elif typ=='THEME':themes[c['ThemeId']]=c
            if typ in ('AGENT_DESIGN','THEME','HYPOTHESIS'):registered.append((typ,c))
    if transition_id not in proposals:raise Refusal('NO_PROPOSAL')
    pe=proposals[transition_id];p=pe['body'];c=p['content'];typ=p['class'];now=snapshot['time_ms']
    if typ not in CLASS_CRITERIA:raise Refusal('CAPABILITY_UNSUPPORTED')
    proposer=pe['actor'];cg=grants.get(checker_grant,{});pg=grants.get(p.get('grant'),{})
    ev={e['seq']:e for e in evidence};fenced={e['body']['grant'] for e in evidence if e['kind']=='FENCE'}
    def ref(e,ledger):return {'ledger':ledger,'sequence':e['seq'],'sha256':e['sha256']}
    refs=[ref(pe,'T')]+[ref(e,'T') for e in events if e['kind']=='APPLIED']
    refs += [ref(e,'E') for e in evidence if e['kind'] in ('RESERVATION','ATTEMPT','FENCE','OBSERVATION','RESEARCH_RECORD')]
    checks={}
    def record(name, value, reason):checks[name]={'status':'MET' if value else 'NOT MET','reason':reason,'refs':refs}
    def active_grant(g,who):
        try:return g['AuthorizationId'] in active and who in g['grantee'] and now<instant(g['expiry'])
        except (KeyError,TypeError,ValueError):return False
    direct=proposer=='Principal' and p.get('grant') is None and p.get('budget')=='0.00' and p.get('funding_ref') is None
    record('authority',direct or active_grant(pg,proposer),'Direct Principal control or active exact proposer grant at closure')
    record('current_base',snapshot['N']==max((x['body']['n'] for x in events if x['kind']=='APPLIED'),default=None),'Checked base is the authoritative head')
    own=designs.get(actor,{}).get('AgentDesignLineageId');other=designs.get(proposer,{}).get('AgentDesignLineageId')
    independent=active_grant(cg,actor) and cg.get('class')=='Checker' and actor!=proposer and (other is None or other!=own)
    independent &= not any(g.get('class')=='Research' and k in active and actor in g['grantee'] for k,g in grants.items())
    if typ=='AGENT_DESIGN':independent &= c.get('AgentDesignLineageId')!=own
    if typ=='AUTHORIZATION':independent &= actor not in (c.get('grant') or {}).get('grantee',[]) and c.get('predecessor')!=checker_grant
    prov=designs.get(actor,{}).get('provenance',{})
    independent &= all(prov.get(k) is None for k in ('provider','model','model_version','training_cutoff'))
    record('independence',independent,'Separate eligible CHECKER lineage/grant; protected CV1; A1 no-model provenance; own-subject restrictions')
    covered=direct
    if not direct:
        r=ev.get(p.get('funding_ref'),{});rb=r.get('body',{})
        try:
            covered=r.get('kind')=='RESERVATION' and rb['actor']==proposer and rb['grant']==p['grant'] and rb['purpose']=={'kind':'Transition','id':transition_id}
            covered &= units(rb['amount'])>=units(p['budget']) and rb['expiry_ms']>now and rb['grant'] not in fenced
            covered &= not any(e['kind']=='CLOSED' and e['body']['reservation']==r['seq'] for e in evidence)
        except (KeyError,TypeError,ValueError):covered=False
    record('funding',covered,'N/A for Principal; otherwise literal named open/unfenced reservation, amount and purpose; Checker cost separate')
    closure_ok=True
    for e in evidence:
        closure_ok &= e['seq']<=snapshot['E'] and digest(e['body'])==e['sha256']
    record('closure',closure_ok and snapshot['F']=='N/A — no Paper Book','Exact committed closure; authored knowing the period; synthetic history earns no forward standing')
    different=True
    if typ=='AGENT_DESIGN':
        different=c.get('AgentDesignVersionId') not in designs
        for oldtyp,old in [('AGENT_DESIGN',x) for x in designs.values()]:
            if oldtyp==typ and (c.get('instructions'),c.get('research_question'),c.get('tool_specs'))==(old.get('instructions'),old.get('research_question'),old.get('tool_specs')):different=False
    if typ=='THEME':different=not any(t==typ and old.get('statement')==c.get('statement') for t,old in registered)
    record('registration_difference',different,'Concrete instruction/question/tool difference; IDs alone do not supply a difference')
    def selection(x):
        q=x.get('selection_basis') or {}
        return all(q.get(k) is not None for k in ('uncertainty','decision_it_could_change','experiment','value_estimate','value_basis','cost_estimate_units','time_estimate_ms','horizon','stopping_rule','origin'))
    try:
        if typ=='AUTHORIZATION':
            g=c.get('grant') or {};kind=g.get('class')
            complete=all(g.get(k) is not None for k in ('AuthorizationId','grantor','grantee','class','may_propose','may_check','may_commit_evidence','expiry','constitutional_budget','tools'))
            complete &= g.get('grantor')=='Principal' and g.get('constitutional_budget')=={'delta_O':0,'delta_S':0,'delta_A':0}
            complete &= not g.get('capital_permission',True) and not g.get('provider_calls_permitted',True) and not g.get('uncapped_calls_permitted',True)
            complete &= all(x in designs if kind!='Observation' else x=='Observation function' for x in g.get('grantee',[]))
            if kind in ('Research','Checker'):
                complete &= units(g['research_budget_units'])>=0 and units(g['per_lineage_cap_units'])>=0 and g['default_reservation_duration_ms']==604800000
                if kind=='Research':complete &= type(g.get('binding_interval_ms')) is int and g['binding_interval_ms']>0
                else:complete &= g.get('binding_interval_ms') is None and bool(g.get('forbidden_subjects')) and bool(g.get('provider_diversity'))
            elif kind!='Observation':complete=False
            complete &= bool(g.get('grantee')) and instant(g['expiry'])>now
            if kind=='Observation':complete &= g['may_propose']==[] and g['may_check']==[] and g['tools']==[]
            if kind=='Checker':
                complete &= all(designs[x]['method_class']=='CHECKER' for x in g['grantee'])
                complete &= all('Research' not in x and 'grant' not in x.lower() for x in g['may_propose'])
                complete &= 'no provider diversity claimed' in g['provider_diversity'].lower()
                complete &= all(t['id'].startswith('CHECK') for t in g['tools'])
            if kind=='Research':
                complete &= all(designs[x]['method_class']=='RESEARCH' for x in g['grantee']) and g['may_check']==[]
                complete &= units(g['per_lineage_cap_units'])<=units(g['research_budget_units'])
                complete &= units(g['discovery_scope']['fixed_subgrant_units'])<=units(g['research_budget_units'])
                complete &= set(g['scope_by_grantee'])==set(g['grantee'])
                complete &= all(not t['id'].startswith('CHECK') for t in g['tools'])
            record('grant_content',complete,'All grant fields, registered grantees, synthetic scope and applicable funding fields evaluated')
            predecessor=c.get('predecessor')
            record('prior_fence',not predecessor or (predecessor in active and (grants[predecessor]['class']=='Observation' or predecessor in fenced)),'Exact predecessor and prior Principal fence for Research/Checker supersession/revocation')
            source_ok=True
            if kind=='Observation':
                source_ok=bool(g.get('source_declarations')) and 'observation_plan' in g
                for src in g.get('source_declarations',[]):
                    sc=src['content'];source_ok &= digest(sc)==src['SourceRevision'] and all(sc.get(k) is not None for k in ('SourceId','provider','dataset','field','unit','print_rule','claimed_time_field','resolution_grace_ms','endpoint','access_method','parsing','extraction_rule'))
                    source_ok &= type(sc.get('resolution_grace_ms')) is int and sc['resolution_grace_ms']>0
                    if sc.get('SourceId')=='SRC-SYN':source_ok &= bool(sc.get('enumeration_contract')) and sc.get('synthetic') is True
                    if sc.get('SourceId')=='SRC-E':source_ok &= sc.get('synthetic') is False
            record('source_declarations',source_ok,'Source meanings, revisions, grace, extraction and feed completeness; no fictional archive retrieval')
            known=profile['artifacts']['tools'];tool_ok=True
            for t in g.get('tools',[]):tool_ok &= t.get('id') in known and t.get('tier')==1 and t.get('spec_sha256')==known.get(t.get('id'),{}).get('content_sha256')
            record('tool_permissions',tool_ok,'Own declared capped synthetic tools only, no foreign-grant tool consumption')
        elif typ=='LIMITS':
            values=[x for k,x in c.items() if k.endswith('_units')]
            exact_limits=set(c)==set(profile['setup']['initial_limits'])
            record('complete_limits',exact_limits and len(values)==9 and all(units(x)==0 for x in values) and c.get('strategy_versions')==[],'Nine explicit zero research-only capital/risk limits')
            record('composition',not any(e['kind']=='APPLIED' and proposals.get(e['transition_id'],{}).get('body',{}).get('class') in ('STRATEGY','ALLOCATION') for e in events),'Replayed empty allocation set: every usage zero, no silent breach')
        elif typ=='AGENT_DESIGN':
            record('design_content',all(c.get(k) is not None for k in ('AgentDesignVersionId','AgentDesignLineageId','method_class','instructions','tool_specs','evaluation_inputs','proposable_outputs')) and c['method_class'] in ('RESEARCH','CHECKER'),'Immutable method content and declared lineage/output/tool contract')
            method=c.get('initial_method') or {};known=profile['artifacts']['methods'].get(method.get('id'),{})
            record('method_commitment',method.get('sha256')==known.get('content_sha256') and bool(known),'Versioned contribution method hash verified')
            pv=c.get('provenance') or {};record('provenance',pv.get('execution_kind')=='deterministic synthetic program' and c.get('executable_closure_sha256')==digest({'code':profile['inventory']['code_closure'],'configuration':{k:v for k,v in c.items() if k!='executable_closure_sha256'}}) and bool(c.get('executable_closure_sha256')) and all(pv.get(k) is None for k in ('provider','model','model_version','training_cutoff')),'Actual frozen executable closure, truthful no-model provenance')
            record('no_inherited_authority',not c.get('authorization_request') and (not c.get('predecessor') or c['predecessor'] in designs),'Registration carries no grant; predecessor references remain visible')
        elif typ=='THEME':
            closure=c.get('motivation_closure');valid=isinstance(closure,dict) and bool(closure.get('refs'))
            if valid:valid=closure.get('N',snapshot['N'])<=snapshot['N'] and all(r['ledger']=='E' and r['sequence'] in ev and ev[r['sequence']]['sha256']==r['sha256'] for r in closure['refs'])
            record('motivation',valid,'Formation closure exists before Theme proposal and is within direct Principal scope')
            record('typed_claims',bool(c.get('typed_claims')) and all(x.get('kind') in ('QUESTION','ASSUMPTION','REPORTED','INTERPRETATION') for x in c.get('typed_claims',[])),'Typed claims disclose synthetic assumptions and questions')
            record('selection',selection(c),'Every selection-basis field present, including time and origin')
        elif typ=='SUSPEND_POLICY':
            record('policy',c.get('policy')=='P-1' and c.get('action')=='SUSPEND','Existing CV1 suspension control, no new policy')
            record('scope',c.get('scope') in grants and proposer=='Principal','Exact named grant and direct Principal authority')
            record('no_other_mutation',set(c)=={'policy','scope','action','reason'},'Suspension content contains no unrelated mutations')
        elif typ=='HYPOTHESIS':
            template=profile['artifacts']['hypothesis_template']['content']
            if c.get('template_id')!=template['template_id']:raise Refusal('CAPABILITY_UNSUPPORTED')
            record('testability',all(c.get(k) is not None for k in ('observable','statement','falsifier','horizon','stopping_rule')) and c.get('tolerance')=='0' and all(c.get(k)==template.get(k) for k in ('observable','statement','falsifier','horizon','stopping_rule')),'Fixed binary observable, falsifier, horizon and zero tolerance')
            rule=c.get('resolution_rule');members=c.get('resolution_set') or []
            resolution=bool(rule) and rule==template['resolution_rule'] and digest(rule)==c.get('resolution_rule_sha256') and len(members)==1 and members[0].get('SourceId')=='SRC-SYN' and members[0].get('period')==c.get('resolution_period') and members[0].get('print')==c.get('print')==template.get('print')
            record('resolution',resolution,'Exact deterministic rule hash, declared period/print/member; no later replacement')
            sources=[s for k,g in grants.items() if k in active and g['class']=='Observation' and now<instant(g['expiry']) for s in g['source_declarations']]
            src=next((s['content'] for s in sources if s['content']['SourceId']==c.get('resolution_source')),None)
            record('sources',src is not None and bool(src.get('extraction_rule')) and bool(src.get('resolution_grace_ms')) and src.get('synthetic') is True,'Source active at base; deterministic extraction, declared grace, synthetic classification')
            mc=c.get('motivation_closure');form=[]
            if isinstance(mc,dict):
                form=[ev.get(r['sequence']) for r in mc.get('refs',[]) if r.get('ledger')=='E']
                if any(r.get('ledger')!='E' or r['sequence'] not in ev or ev[r['sequence']]['sha256']!=r['sha256'] for r in mc.get('refs',[])):
                    form=[]
            docs=[e['body']['document'] for e in form if e and e['kind']=='OBSERVATION' and e['body']['form']=='DOCUMENT']
            period=c.get('resolution_period') or {}
            disjoint=bool(docs) and all(d['period_end']<=period.get('start','') for d in docs) and instant(period['end'])>now
            record('disjoint',disjoint,'Formation items precede a distinct future member with declared structural availability bound')
            record('selection',selection(c),'Complete cost/time/value uncertainty and declared origin')
            method=c.get('initial_method') or {};expected=profile['artifacts']['methods'].get(method.get('id'),{})
            record('methods',bool(expected) and method.get('sha256')==expected.get('content_sha256'),'Scoring, effective observations and predictive check fixed by exact method artifact')
            recomputed=False
            if len(docs)==1:
                counts={'n':0,'k':0,'n_large':0,'k_large':0};seen=set();good=True
                for row in docs[0]['rows']:
                    good &= row['event_id'] not in seen and type(row['spike']) is bool and type(row['selling']) is bool and type(row['size_units']) is int and 0<=row['size_units']<=10
                    seen.add(row['event_id'])
                    if row['spike']:
                        counts['n']+=1;counts['k']+=int(row['selling'])
                        if row['size_units']>=2:counts['n_large']+=1;counts['k_large']+=int(row['selling'])
                rr=[e for e in form if e and e['kind']=='RESEARCH_RECORD']
                recomputed=good and bool(rr) and counts['n_large']>0 and all(rr[-1]['body']['result'].get(k)==val for k,val in counts.items())
                if rr:recomputed &= rr[-1]['actor']==proposer and rr[-1]['body']['reproducibility']['result_hash']==digest(rr[-1]['body']['result']) and rr[-1]['body']['result']['input_sha256']==digest(docs[0])
            if recomputed and rr[-1]['body']['result'].get('adaptation',{}).get('id')=='complement-control':
                analysis=rr[-1]['body']['result']['adaptation']
                control=[row for row in docs[0]['rows'] if row['spike'] and row['size_units']<2]
                nk=len(control);kk=sum(int(row['selling']) for row in control)
                recomputed &= analysis['comparison_n']==nk and analysis['comparison_k']==kk and analysis['passes']==(nk>0 and 3*kk>=2*nk)
                chosen=ev[analysis['selection_ref']['sequence']]
                recomputed &= chosen['sha256']==analysis['selection_ref']['sha256'] and chosen['body']['kind']=='SELECTION' and chosen['actor']==proposer
                recomputed &= len({row['shock_id'] for row in docs[0]['rows'] if row['spike'] and row['size_units']>=2})==1
            record('recomputation',recomputed,'Independent direct row count matches the exact committed research result; authored knowing the period')
            keys=('observable','resolution_source','print','tolerance','resolution_rule_sha256','initial_method','falsifier')
            record('restatement',not any(t=='HYPOTHESIS' and all(old.get(k)==c.get(k) for k in keys) for t,old in registered),'Compared registered scientific tuple; a new date/ID alone is not a difference')
    except Refusal as exc:
        if exc.code=='CAPABILITY_UNSUPPORTED':raise
        for name in CLASS_CRITERIA[typ]:
            if name not in checks:record(name,False,'Invalid declared content: '+exc.code)
    except (KeyError,TypeError,ValueError,IndexError) as exc:
        for name in CLASS_CRITERIA[typ]:
            if name not in checks:record(name,False,'Incomplete/invalid declared content: '+type(exc).__name__)
    for name in COMMON+CLASS_CRITERIA[typ]:
        if name not in checks:record(name,False,'Missing criterion input')
    return {'transition_id':transition_id,'base':snapshot['N'],'grant':checker_grant,'attempt':attempt,
            'closure':{k:snapshot[k] for k in ('E','N','F','time_ms')},'criteria':checks,
            'result':'PASS' if all(x['status']=='MET' for x in checks.values()) else 'FAIL',
            'es':'ES-1.0','constitution':1,'provenance':designs.get(actor,{}).get('provenance',{}),'context':{'class':typ,'subject':p['subject'],'proposal':{'ledger':'T','sequence':pe['seq'],'sha256':pe['sha256']},
              'proposer':{'identity':proposer,'authority':'Principal' if proposer=='Principal' else p['grant'],'provenance':designs.get(proposer,{}).get('provenance')},
              'checker':{'identity':actor,'design':actor,'grant':checker_grant,'provenance':designs.get(actor,{}).get('provenance')},
              'funding':{'proposer':'N/A' if proposer=='Principal' else p['funding_ref'],'checker_attempt':attempt,'separate':True},
              'classification':'Synthetic Historical Reconstruction; authored knowing the period','provider_exception':'A1 synthetic-only; no provider provenance claimed'}}
