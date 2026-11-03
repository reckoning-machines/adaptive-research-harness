"""Checker B: independent set/index reconstruction, not Checker A or tool code."""
from ..encoding import digest, units, instant, Refusal
from ..contracts import COMMON, CLASS_CRITERIA


def evaluate(s, transition_id, actor, checker_grant, attempt, profile):
    ts=s['transitions'];es=s['evidence'];now=s['time_ms']
    proposals={x['transition_id']:x for x in ts if x['kind']=='PROPOSED'}
    if transition_id not in proposals:raise Refusal('NO_PROPOSAL')
    pe=proposals[transition_id];p=pe['body'];c=p['content'];typ=p['class'];proposer=pe['actor']
    if typ not in CLASS_CRITERIA:raise Refusal('CAPABILITY_UNSUPPORTED')
    applied=sorted((x for x in ts if x['kind']=='APPLIED' and x['body']['n']<=s['N']),key=lambda x:x['body']['n'])
    initial=next((x['body']['genesis'] for x in applied if 'genesis' in x['body']),None)
    if initial is None:raise Refusal('NOT_INITIALIZED')
    acts=[proposals[x['transition_id']]['body'] for x in applied if 'genesis' not in x['body']]
    auth=[x['content'] for x in acts if x['class']=='AUTHORIZATION']
    grants={x['grant']['AuthorizationId']:x['grant'] for x in auth}
    grants[initial['grant']['AuthorizationId']]=initial['grant']
    disabled={x['predecessor'] for x in auth if x['predecessor']}|{x['grant']['AuthorizationId'] for x in auth if x['action']=='REVOKE'}
    active=set(grants)-disabled
    designs={x['content']['AgentDesignVersionId']:x['content'] for x in acts if x['class']=='AGENT_DESIGN'}
    designs[initial['design']['AgentDesignVersionId']]=initial['design']
    eidx={e['seq']:e for e in es};fences={e['body']['grant'] for e in es if e['kind']=='FENCE'}
    closed={e['body']['reservation'] for e in es if e['kind']=='CLOSED'}
    citations=[{'ledger':'T','sequence':x['seq'],'sha256':x['sha256']} for x in [pe]+applied]
    citations += [{'ledger':'E','sequence':x['seq'],'sha256':x['sha256']} for x in es if x['kind'] in ('OBSERVATION','RESEARCH_RECORD','ATTEMPT','RESERVATION','FENCE')]
    verdict={}
    def put(k,ok,reason):verdict[k]={'status':'MET' if ok else 'NOT MET','reason':reason,'refs':citations}
    def eligible(g,who):
        try:return g['AuthorizationId'] in active and who in g['grantee'] and instant(g['expiry'])>now
        except (ValueError,KeyError,TypeError):return False
    principal=proposer=='Principal' and p.get('grant') is None and p.get('budget')=='0.00' and p.get('funding_ref') is None
    put('authority',principal or eligible(grants.get(p.get('grant'),{}),proposer),'Direct authority or active grantee set at this closure')
    put('current_base',s['N']==max((x['body']['n'] for x in applied),default=None),'Reconstructed Apply head equals checked base; immutable original base is not rewritten')
    cg=grants.get(checker_grant,{})
    lineage=designs.get(actor,{}).get('AgentDesignLineageId')
    forbidden=(actor==proposer or (proposer in designs and designs[proposer]['AgentDesignLineageId']==lineage))
    forbidden |= any(g['class']=='Research' and actor in g['grantee'] for k,g in grants.items() if k in active)
    if typ=='AGENT_DESIGN':forbidden |= c.get('AgentDesignLineageId')==lineage
    if typ=='AUTHORIZATION':forbidden |= c.get('predecessor')==checker_grant or actor in (c.get('grant') or {}).get('grantee',[])
    provenance=designs.get(actor,{}).get('provenance',{})
    put('independence',eligible(cg,actor) and cg.get('class')=='Checker' and not forbidden and
        all(provenance.get(k) is None for k in ['provider','model','model_version','training_cutoff']),
        'Disjoint proposer/Checker authority and lineage, own-subject exclusion, synthetic exception, immutable evidence')
    cover=principal
    if not cover:
        entry=eidx.get(p.get('funding_ref'),{});r=entry.get('body',{})
        try:cover=entry.get('kind')=='RESERVATION' and r['actor']==proposer and r['grant']==p['grant'] and r['purpose']=={'kind':'Transition','id':transition_id} and units(r['amount'])>=units(p['budget']) and r['expiry_ms']>now and r['grant'] not in fences and entry['seq'] not in closed
        except (ValueError,TypeError,KeyError):cover=False
    put('funding',cover,'Exact reservation-sequence membership and coverage, not purpose-only selection; Principal N/A')
    put('closure',s['F']=='N/A — no Paper Book' and all(e['seq']<=s['E'] and digest(e['body'])==e['sha256'] for e in es),'Immutable closure hashes; authored knowing the period; synthetic outcomes earn no forward standing')
    previous=[x['content'] for x in acts if x['class']==typ]
    different=True
    if typ=='AGENT_DESIGN':
        signatures={digest([x.get('instructions'),x.get('research_question'),x.get('tool_specs')]) for x in designs.values()}
        different=c.get('AgentDesignVersionId') not in designs and digest([c.get('instructions'),c.get('research_question'),c.get('tool_specs')]) not in signatures
    if typ=='THEME':different=c.get('statement') not in {x.get('statement') for x in previous}
    put('registration_difference',different,'Set comparison of declared scientific/instruction differences, not renamed IDs')
    try:
        if typ=='AUTHORIZATION':
            g=c.get('grant') or {};kind=g.get('class')
            required={'AuthorizationId','grantor','grantee','class','may_propose','may_check','may_commit_evidence','expiry','constitutional_budget','tools'}
            good=required<=g.keys() and not any(g[k] is None for k in required)
            good &= g.get('grantor')=='Principal' and g.get('constitutional_budget')=={'delta_O':0,'delta_S':0,'delta_A':0}
            good &= g.get('capital_permission') is False and g.get('provider_calls_permitted') is False and g.get('uncapped_calls_permitted') is False
            good &= set(g.get('grantee',[])) <= (set(designs) if kind!='Observation' else {'Observation function'})
            if kind in {'Research','Checker'}:
                good &= units(g['research_budget_units'])>=0 and units(g['per_lineage_cap_units'])>=0 and g.get('default_reservation_duration_ms')==604800000
                good &= (type(g.get('binding_interval_ms')) is int and g['binding_interval_ms']>0) if kind=='Research' else (g.get('binding_interval_ms') is None and bool(g.get('forbidden_subjects')) and bool(g.get('provider_diversity')))
            else:good &= kind=='Observation'
            good &= len(g.get('grantee',[]))>0 and now<instant(g['expiry'])
            if kind=='Observation':good &= not g['may_propose'] and not g['may_check'] and not g['tools']
            elif kind=='Research':
                good &= {designs[x]['method_class'] for x in g['grantee']}=={'RESEARCH'} and not g['may_check']
                good &= max(units(g['per_lineage_cap_units']),units(g['discovery_scope']['fixed_subgrant_units']))<=units(g['research_budget_units'])
                good &= set(g['grantee'])==set(g['scope_by_grantee']) and not any(t['id'].startswith('CHECK') for t in g['tools'])
            elif kind=='Checker':
                good &= {designs[x]['method_class'] for x in g['grantee']}=={'CHECKER'}
                good &= not any('Research' in x or 'grant' in x.lower() for x in g['may_propose'])
                good &= 'no provider diversity claimed' in g['provider_diversity'].lower() and all(t['id'].startswith('CHECK') for t in g['tools'])
            put('grant_content',good,'Complete grant, class-correct actors, zero capital/constitutional delta, explicit cost and expiry fields')
            old=c.get('predecessor')
            put('prior_fence',not old or (old in active and (grants[old]['class']=='Observation' or old in fences)),'Predecessor active, prior fence for funding grants')
            good=True
            if kind=='Observation':
                sources=g.get('source_declarations',[]);good=bool(sources) and 'observation_plan' in g
                required={'SourceId','provider','dataset','field','unit','print_rule','claimed_time_field','resolution_grace_ms','endpoint','access_method','parsing','extraction_rule'}
                for decl in sources:
                    x=decl['content'];good &= required<=x.keys() and all(x[k] is not None for k in required) and digest(x)==decl['SourceRevision']
                    good &= type(x.get('resolution_grace_ms')) is int and x['resolution_grace_ms']>0
                    if x.get('SourceId')=='SRC-SYN':good &= bool(x.get('enumeration_contract')) and x.get('synthetic') is True
                    if x.get('SourceId')=='SRC-E':good &= x.get('synthetic') is False
            put('source_declarations',good,'Full source meanings and deterministic extraction/enumeration with pinned grace')
            specs=profile['artifacts']['tools'];valid={(k,v['content_sha256'],1) for k,v in specs.items()}
            put('tool_permissions',all((t.get('id'),t.get('spec_sha256'),t.get('tier')) in valid for t in g.get('tools',[])),'Each tool belongs to the explicit synthetic specification/tier set')
        elif typ=='LIMITS':
            limits={k:units(v) for k,v in c.items() if k.endswith('_units')}
            put('complete_limits',set(c)==set(profile['setup']['initial_limits']) and len(limits)==9 and set(limits.values())=={0} and c.get('strategy_versions')==[],'All nine zero limits are explicit')
            put('composition',not {'STRATEGY','ALLOCATION'} & {x['class'] for x in acts},'Empty strategy/allocation set yields zero usage for every declared limit')
        elif typ=='AGENT_DESIGN':
            needed={'AgentDesignVersionId','AgentDesignLineageId','method_class','instructions','tool_specs','evaluation_inputs','proposable_outputs'}
            put('design_content',needed<=c.keys() and all(c[k] is not None for k in needed) and c['method_class'] in {'RESEARCH','CHECKER'},'Immutable method and explicit inputs/outputs/tools')
            method=c.get('initial_method') or {};versions={(k,v['content_sha256']) for k,v in profile['artifacts']['methods'].items()}
            put('method_commitment',(method.get('id'),method.get('sha256')) in versions,'Initial contribution method has exact version/hash')
            pv=c.get('provenance') or {}
            put('provenance',pv.get('execution_kind')=='deterministic synthetic program' and bool(c.get('executable_closure_sha256')) and c['executable_closure_sha256']==digest(dict(configuration=dict((k,v) for k,v in c.items() if k!='executable_closure_sha256'),code=profile['inventory']['code_closure'])) and all(pv.get(k) is None for k in ('provider','model','model_version','training_cutoff')),'Actual pinned code closure and explicit absence of trained-model provenance')
            put('no_inherited_authority',not c.get('authorization_request') and (not c.get('predecessor') or c['predecessor'] in designs),'Predecessor exists where cited; no grant is carried by registration')
        elif typ=='THEME':
            closure=c.get('motivation_closure') or {};rs=closure.get('refs',[]) if isinstance(closure,dict) else []
            put('motivation',bool(rs) and all(r.get('ledger')=='E' and r['sequence'] in eidx and eidx[r['sequence']]['sha256']==r['sha256'] for r in rs),'Formation membership established before Theme registration')
            put('typed_claims',bool(c.get('typed_claims')) and {x.get('kind') for x in c['typed_claims']} <= {'QUESTION','ASSUMPTION','REPORTED','INTERPRETATION'},'Synthetic motivation represented as typed statements')
            sb=c.get('selection_basis') or {};keys={'uncertainty','decision_it_could_change','experiment','value_estimate','value_basis','cost_estimate_units','time_estimate_ms','horizon','stopping_rule','origin'}
            put('selection',keys<=sb.keys() and all(sb[k] is not None for k in keys),'All selection fields, including uncertainty/time/origin')
        elif typ=='SUSPEND_POLICY':
            put('policy',(c.get('policy'),c.get('action'))==('P-1','SUSPEND'),'Only the existing bounded suspension act')
            put('scope',c.get('scope') in grants and proposer=='Principal','Named grant with direct Principal authority')
            put('no_other_mutation',set(c)=={'policy','scope','action','reason'},'No grant, method, constitution or unrelated state change')
        elif typ=='HYPOTHESIS':
            template=profile['artifacts']['hypothesis_template']['content']
            if c.get('template_id')!=template['template_id']:raise Refusal('CAPABILITY_UNSUPPORTED')
            put('testability',all(c.get(k) is not None for k in ('observable','statement','falsifier','horizon','stopping_rule')) and c.get('tolerance')=='0' and {k:c.get(k) for k in ('observable','statement','falsifier','horizon','stopping_rule')}=={k:template.get(k) for k in ('observable','statement','falsifier','horizon','stopping_rule')},'Registered binary target and explicit falsification/horizon')
            members=c.get('resolution_set') or [];rule=c.get('resolution_rule')
            put('resolution',bool(rule) and rule==template['resolution_rule'] and digest(rule)==c.get('resolution_rule_sha256') and len(members)==1 and members[0].get('SourceId')=='SRC-SYN' and members[0].get('period')==c.get('resolution_period') and members[0].get('print')==c.get('print')==template.get('print'),'Known deterministic template rule, exact hash and single member')
            sources={x['content']['SourceId']:x['content'] for gid,g in grants.items() if gid in active and g['class']=='Observation' and instant(g['expiry'])>now for x in g['source_declarations']}
            source=sources.get(c.get('resolution_source'),{})
            put('sources',bool(source.get('extraction_rule')) and bool(source.get('resolution_grace_ms')) and source.get('synthetic') is True,'Active synthetic source with deterministic field extraction and grace')
            closure=c.get('motivation_closure');rrs=closure.get('refs',[]) if isinstance(closure,dict) else []
            formation=[eidx[r['sequence']] for r in rrs if r.get('ledger')=='E' and r['sequence'] in eidx and eidx[r['sequence']]['sha256']==r['sha256']]
            if len(formation)!=len(rrs):formation=[]
            documents=[e['body']['document'] for e in formation if e['kind']=='OBSERVATION' and e['body']['form']=='DOCUMENT']
            period=c.get('resolution_period') or {}
            put('disjoint',bool(documents) and all(d['period_end']<=period.get('start','') for d in documents) and instant(period['end'])>now,'Distinct future resolution period, not a formation member')
            sb=c.get('selection_basis') or {};keys={'uncertainty','decision_it_could_change','experiment','value_estimate','value_basis','cost_estimate_units','time_estimate_ms','horizon','stopping_rule','origin'}
            put('selection',keys<=sb.keys() and all(sb[k] is not None for k in keys),'Complete disclosed value uncertainty and intended next experiment')
            method=c.get('initial_method') or {};methods={(k,x['content_sha256']) for k,x in profile['artifacts']['methods'].items()}
            put('methods',(method.get('id'),method.get('sha256')) in methods,'Exact methods and constants, no synthetic forward standing')
            counts=None
            if len(documents)==1:
                rows=documents[0]['rows'];ids=[r['event_id'] for r in rows]
                if len(ids)==len(set(ids)) and all(type(r['spike']) is bool and type(r['selling']) is bool and type(r['size_units']) is int and 0<=r['size_units']<=10 for r in rows):
                    spikes={r['event_id'] for r in rows if r['spike']};selling={r['event_id'] for r in rows if r['selling']};large={r['event_id'] for r in rows if r['size_units']>=2}
                    counts={'n':len(spikes),'k':len(spikes&selling),'n_large':len(spikes&large),'k_large':len(spikes&large&selling)}
            research=sorted((e for e in formation if e['kind']=='RESEARCH_RECORD'),key=lambda e:e['seq'])
            control_valid=True
            if research and research[-1]['body']['result'].get('adaptation',{}).get('id')=='complement-control' and counts is not None:
                analysis=research[-1]['body']['result']['adaptation'];nonlarge=spikes-large
                observed=(len(nonlarge),len(nonlarge&selling))
                control_valid=(analysis['comparison_n'],analysis['comparison_k'])==observed and analysis['passes']==(observed[0]>0 and 3*observed[1]>=2*observed[0])
                sel=eidx.get(analysis['selection_ref']['sequence'],{})
                control_valid &= sel.get('sha256')==analysis['selection_ref']['sha256'] and sel.get('actor')==proposer and sel.get('body',{}).get('kind')=='SELECTION'
                control_valid &= len(set(row['shock_id'] for row in documents[0]['rows'] if row['event_id'] in spikes&large))==1
            put('recomputation',control_valid and counts is not None and counts['n_large']>0 and bool(research) and research[-1]['actor']==proposer and research[-1]['body']['reproducibility']['result_hash']==digest(research[-1]['body']['result']) and research[-1]['body']['result']['input_sha256']==digest(documents[0]) and all(research[-1]['body']['result'].get(k)==v for k,v in counts.items()),'Independent set cardinalities equal committed research values; authored knowing the period')
            keys=('observable','resolution_source','print','tolerance','resolution_rule_sha256','initial_method','falsifier')
            signatures={digest([x.get(k) for k in keys]) for x in previous}
            put('restatement',digest([c.get(k) for k in keys]) not in signatures,'Full admitted family scientific tuple comparison; date/ID are not sufficient differences')
    except Refusal as exc:
        if exc.code=='CAPABILITY_UNSUPPORTED':raise
        for k in CLASS_CRITERIA[typ]:
            if k not in verdict:put(k,False,'Invalid declared content: '+exc.code)
    except (ValueError,KeyError,TypeError,IndexError) as exc:
        for k in CLASS_CRITERIA[typ]:
            if k not in verdict:put(k,False,'Missing/malformed criterion input: '+type(exc).__name__)
    for k in COMMON+CLASS_CRITERIA[typ]:
        if k not in verdict:put(k,False,'Missing criterion')
    return {'transition_id':transition_id,'base':s['N'],'grant':checker_grant,'attempt':attempt,
            'closure':{k:s[k] for k in ('E','N','F','time_ms')},'criteria':verdict,
            'result':'FAIL' if any(x['status']!='MET' for x in verdict.values()) else 'PASS',
            'constitution':1,'es':'ES-1.0','provenance':provenance,'context':{'class':typ,'subject':p['subject'],'proposal':{'ledger':'T','sequence':pe['seq'],'sha256':pe['sha256']},
              'proposer':{'identity':proposer,'authority':'Principal' if proposer=='Principal' else p['grant'],'provenance':designs.get(proposer,{}).get('provenance')},
              'checker':{'identity':actor,'design':actor,'grant':checker_grant,'provenance':designs.get(actor,{}).get('provenance')},
              'funding':{'proposer':'N/A' if proposer=='Principal' else p['funding_ref'],'checker_attempt':attempt,'separate':True},
              'classification':'Synthetic Historical Reconstruction; authored knowing the period','provider_exception':'A1 synthetic-only; no provider provenance claimed'}}
