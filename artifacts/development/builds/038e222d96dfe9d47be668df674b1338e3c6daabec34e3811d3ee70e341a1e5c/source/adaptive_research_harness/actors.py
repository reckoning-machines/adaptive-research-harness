"""Pinned actor programs. Fixture drivers select actions, never compose successful research."""
from copy import deepcopy
from datetime import datetime,timedelta
import uuid
from .encoding import digest, require, Refusal, time_text, instant


def invocation(profile,tool,step,refs,parameters):
    return {'schema_version':1,'tool_id':tool,'tool_spec_hash':profile['artifacts']['tools'][tool]['content_sha256'],
            'executable_hash':profile['inventory']['tool_executables'][tool],
            'step':step,'parameters':parameters,'input_refs':refs}


def event_ref(e,ledger='E'):
    return {'ledger':ledger,'sequence':e['seq'],'sha256':e['sha256'],
            'raw_sha256':digest(e['body'].get('document',e['body']))}


def settle(client,attempt,receipt):
    return client.committed('settle',{'attempt':attempt,'actual':receipt['actual'],
        'unit':'simulated_research_units','provenance':{'kind':'TOOL_RECEIPT','receipt':receipt}})


def formation(client,profile):
    closure=client.query('closure')
    expected=profile['artifacts']['formation_cohort']['content_sha256']
    docs=[e for e in closure['evidence'] if e['kind']=='OBSERVATION' and e['body']['form']=='DOCUMENT'
          and digest(e['body']['document'])==expected]
    require(bool(docs),'FORMATION_MISSING')
    return min(docs,key=lambda e:e['seq'])


def research(client,tool='SYN-A-1',stop_after=None):
    profile=client.query('profile');design=next(d['content'] for d in profile['artifacts']['designs'] if d['content']['AgentDesignVersionId']==client.actor)
    require(design['ordinary_cycle_enabled'] is True,'CAPABILITY_UNSUPPORTED','Dormant profile has no ordinary research loop')
    require(tool in design['tool_specs'],'TOOL_NOT_PERMITTED')
    doc=formation(client,profile);ref=event_ref(doc)
    reservation=client.committed('reserve',{'grant':'AU-RP-1','amount':'3.00' if tool=='SYN-A-1' else '1.00','purpose':{'kind':'Theme','id':'TH-G1'}})['refs'][0]
    step='research-counts' if tool=='SYN-A-1' else 'replacement-counts'
    data=invocation(profile,tool,step,[ref],{'threshold':2})
    attempt=client.committed('attempt',{'reservation':reservation['sequence'],'step':step,'input':data,
                        'dispatch_index':0,'maximum':'1.00','tier':1})['refs'][0]
    if stop_after=='attempt':return {'reservation':reservation,'attempt':attempt,'input':data}
    return complete_research(client,attempt['sequence'])


def complete_research(client,attempt_seq):
    profile=client.query('profile');closure=client.query('closure')
    a=next(e for e in closure['evidence'] if e['seq']==attempt_seq and e['kind']=='ATTEMPT')
    require(a['actor']==client.actor,'UNAUTHORIZED')
    dispatch=client.query('tool-run',{'attempt':attempt_seq})
    if dispatch.get('status')!='RECEIPT':return dispatch
    receipt=dispatch['receipt'];inp=a['body']['input'];ref=inp['input_refs'][0]
    doc=client.query('get',{'ref':ref})
    value=receipt['result'];error=receipt['error']
    if not error:
        try:
            require(value['input_sha256']==digest(doc['body']['document']) and value['synthetic'] is True,'INVALID_TOOL_RECEIPT')
            require(all(type(value[k]) is int for k in ('n','k','n_large','k_large')),'INVALID_TOOL_RECEIPT')
        except (Refusal,KeyError,TypeError):error='INVALID_TOOL_RECEIPT'
    closure=client.query('closure')
    record={'grant':a['body']['grant'],'attempt':attempt_seq,'question':'Do large synthetic volatility events warrant a narrower selling hypothesis?',
        'result':value if value is not None else {'failure':error},'failure':error,
        'closure':{'E':closure['E'],'N':closure['N'],'refs':[ref]},'claims':[
            {'kind':'REPORTED','document':ref,'location':'/rows','text':'Declared synthetic cohort rows'},
            {'kind':'INTERPRETATION','reported':[0],'text':'Calculated synthetic counts; no economic or forward standing'}],
        'kind':'plain','snapshot':{'identity':doc['body']['item_id'],'sha256':digest(doc['body']['document'])},
        'source_cutoff':doc['body']['document']['period_end'],'parameters':inp['parameters'],
        'tool':{'id':inp['tool_id'],'spec_sha256':inp['tool_spec_hash'],'executable_hash':inp['executable_hash']},
        'reproducibility':{'input_refs':inp['input_refs'],'invocation_hash':a['body']['input_hash'],
                           'result_hash':digest(value) if value is not None else None,'classification':'Historical Reconstruction'},'synthetic':True}
    result=client.call('research-commit',record)
    settlement=settle(client,attempt_seq,receipt)
    close=client.call('close',{'reservation':a['body']['reservation']})
    return {'record':result,'settlement':settlement,'close':close,'failure':error}


def propose_hypothesis(client,research_ref,previous=None):
    profile=client.query('profile');rr=client.query('get',{'ref':research_ref})
    require(rr['kind']=='RESEARCH_RECORD' and rr['actor']==client.actor and not rr['body'].get('failure'),'NO_POSITIVE_RESEARCH')
    result=rr['body']['result'];require(result['synthetic'] is True and result['n_large']>0,'NO_TESTABLE_CANDIDATE')
    c=deepcopy(profile['artifacts']['hypothesis_template']['content'])
    document_refs=rr['body']['closure']['refs']
    c['motivated_by']=['TH-G1',research_ref]
    c['motivation_closure']={'N':rr['body']['closure']['N'],'refs':document_refs+[research_ref]}
    state=client.query('state');clock=client.query('clock');future=(clock['E'] or 0)+1
    adaptation=result.get('adaptation')
    tr=adaptation['proposing_transition'] if adaptation else 'TR-RESEARCH-'+uuid.uuid4().hex
    if adaptation:c['selection_basis']['origin']={'selection_record':adaptation['selection_ref'],'research_record':research_ref}
    p={'transition_id':tr,'base':state['N'],'class':'HYPOTHESIS','subject':c['HypothesisId'],'content':c,
       'budget':'2.00','grant':'AU-RP-1','funding_ref':future,'delta':{'O':0,'S':0,'A':0}}
    if previous:p['predecessor_transition']=previous
    proposal=client.committed('propose',p)
    funding=client.call('reserve',{'grant':'AU-RP-1','amount':'2.00','purpose':{'kind':'Transition','id':tr},'expected_sequence':future})
    return {'transition_id':tr,'proposal':proposal,'funding':funding,'funding_ref':future}


def check(client,transition_id,hook=lambda point:None):
    profile=client.query('profile');grant={'AD-CK-1.0':'AU-CK-A','AD-CK-2.0':'AU-CK-B'}[client.actor]
    tool={'AD-CK-1.0':'CHECK-A-1','AD-CK-2.0':'CHECK-B-1'}[client.actor]
    snapshot=client.query('closure');p=next(x for x in snapshot['transitions'] if x['kind']=='PROPOSED' and x['transition_id']==transition_id)
    r=client.committed('reserve',{'grant':grant,'amount':'0.25','purpose':{'kind':'Check','id':transition_id}})['refs'][0]
    data=invocation(profile,tool,'check-transition',[event_ref(p,'T')],{'transition_id':transition_id})
    a=client.committed('attempt',{'reservation':r['sequence'],'step':'check-transition','input':data,'dispatch_index':0,'maximum':'0.25','tier':1})['refs'][0]
    permission=client.query('tool-run',{'attempt':a['sequence']})
    require(permission.get('status')=='PERMISSION_CONSUMED','CHECK_DISPATCH_UNCERTAIN')
    error=None;candidate=None
    try:
        snapshot=client.query('closure')
        hook('checker_during_computation')
        if client.actor=='AD-CK-1.0':
            from .checkers.a import evaluate
        else:
            from .checkers.b import evaluate
        candidate=evaluate(snapshot,transition_id,client.actor,grant,a['sequence'],profile)
    except (Refusal,KeyError,ValueError,TypeError) as exc:error=str(exc)
    receipt={'attempt':a['sequence'],'input_hash':digest(data),'tool_id':tool,'actual':'0.25',
             'synthetic':True,'result':candidate,'error':error}
    hook('checker_after_result')
    client.query('check-finish',{'attempt':a['sequence'],'receipt':receipt})
    if candidate:
        result=client.call('check-commit',candidate)
    else:
        snapshot=client.query('closure')
        negative={'grant':grant,'attempt':a['sequence'],'question':'Verify '+transition_id,
          'result':{'failure':error},'failure':error,'closure':{'E':snapshot['E'],'N':snapshot['N'],'refs':[event_ref(p,'T')]},
          'claims':[{'kind':'ASSUMPTION','text':'Computation interrupted or outside supported capability; no Check judgment'}],
          'kind':'plain','snapshot':{'identity':transition_id,'sha256':p['sha256']},
          'source_cutoff':time_text(snapshot['time_ms']),'parameters':data['parameters'],
          'tool':{'id':tool,'spec_sha256':data['tool_spec_hash'],'executable_hash':data['executable_hash']},
          'reproducibility':{'input_refs':data['input_refs'],'invocation_hash':digest(data),'result_hash':None},'synthetic':True}
        result={'status':'CAPABILITY_UNSUPPORTED','reason':error,'negative_record':client.call('research-commit',negative)}
    settlement=settle(client,a['sequence'],receipt)
    client.call('close',{'reservation':r['sequence']})
    return {'check':result,'settlement':settlement,'computed_result':candidate['result'] if candidate else None,'attempt':a}


def observe(client,date='2026-10-28',form='DOCUMENT'):
    require(client.actor=='Observation function','UNAUTHORIZED')
    profile=client.query('profile');source=next(s for g in profile['setup']['grants'] if g['content']['AuthorizationId']=='AU-OBS-1'
        for s in g['content']['source_declarations'] if s['content']['SourceId']=='SRC-SYN')
    doc=deepcopy(profile['artifacts']['formation_cohort']['content'])
    start=datetime.strptime(date,'%Y-%m-%d');end=start+timedelta(days=1)
    doc.update(item_id='cohort-'+date,period_start=start.strftime('%Y-%m-%dT00:00:00.000Z'),
               period_end=end.strftime('%Y-%m-%dT00:00:00.000Z'),claimed_publication_time=end.strftime('%Y-%m-%dT00:00:00.000Z'))
    clock=client.query('clock')
    payload={'grant':'AU-OBS-1','source':'SRC-SYN','revision':source['SourceRevision'],'form':form,
             'period':{'start':doc['period_start'],'end':doc['period_end']},'item_id':doc['item_id'],
             'document':doc if form=='DOCUMENT' else None,'slot':clock['t']}
    if form=='DOCUMENT':
        listing=dict(payload,form='COMPLETE',document=None,items=[doc['item_id']],window=payload['period'])
        client.committed('observation-commit',listing)
        result=client.committed('observation-commit',payload)
        rows=doc['rows'];n=sum(1 for row in rows if row['spike'] and row['size_units']>=2)
        k=sum(1 for row in rows if row['spike'] and row['size_units']>=2 and row['selling'])
        extraction=dict(payload,form='VALUE' if n else 'NOT_EXTRACTABLE',document=None,document_ref=result['refs'][0])
        if n:extraction['value']={'numerator':k,'denominator':n}
        else:extraction['error']='No large spike rows'
        client.committed('observation-commit',extraction)
        return result
    if form in ('ABSENT','COMPLETE'):
        payload.update(form='COMPLETE',items=[doc['item_id']] if clock['t']>=instant(doc['period_end']) else [],window=payload['period'])
    elif form in ('RETRIEVAL_FAILED','PARTIAL'):payload['error']='Explicit synthetic retrieval fault'
    return client.committed('observation-commit',payload)


def recover_settlement(client,attempt_seq):
    page=client.query('history',{'ledger':'E','after':attempt_seq-1,'limit':1})
    a=next(x for x in page['records'] if x['kind']=='ATTEMPT' and x['seq']==attempt_seq)
    require(client.actor in (a['actor'],'Principal'),'UNAUTHORIZED')
    receipt=client.query('tool-receipt',{'attempt':attempt_seq})
    if receipt.get('receipt') is not None:return settle(client,attempt_seq,receipt['receipt'])
    return client.committed('settle',{'attempt':attempt_seq,'actual':a['body']['maximum'],'unit':'simulated_research_units','provenance':{'kind':'UNKNOWN'}})


def retry_research(client,attempt_seq):
    page=client.query('history',{'ledger':'E','after':attempt_seq-1,'limit':1})
    a=page['records'][0];require(a['kind']=='ATTEMPT' and a['actor']==client.actor,'UNAUTHORIZED')
    b=a['body'];closure=client.query('closure')
    indexes=[x['body']['dispatch_index'] for x in closure['evidence'] if x['kind']=='ATTEMPT' and x['body']['reservation']==b['reservation'] and x['body']['step']==b['step'] and x['body']['input_hash']==b['input_hash']]
    payload={k:b[k] for k in ('reservation','step','input','maximum','tier')};payload['dispatch_index']=max(indexes)+1
    new=client.call('attempt',payload)
    if new.get('status')!='COMMITTED':return new
    return {'attempt':new['refs'][0],'result':complete_research(client,new['refs'][0]['sequence'])}


def propose_successor(client,case,ordinal):
    require(case in ('S04','R11') and type(ordinal) is int and ordinal>=1,'CAPABILITY_UNSUPPORTED')
    profile=client.query('profile');state=client.query('state');current=deepcopy(state['designs'][client.actor])
    require(current['method_class']=='RESEARCH','CAPABILITY_UNSUPPORTED')
    current['predecessor']=client.actor;current['AgentDesignVersionId']=client.actor+'-'+case+'-'+str(ordinal)
    current['instructions']+=' Retain negative evidence in deterministic sorted question order.'
    current.pop('executable_closure_sha256')
    current['executable_closure_sha256']=digest({'code':profile['inventory']['code_closure'],'configuration':deepcopy(current)})
    prospective=(client.query('clock')['E'] or 0)+1;tr=f'TR-{case}-{ordinal}'
    proposal={'transition_id':tr,'base':state['N'],'class':'AGENT_DESIGN','subject':current['AgentDesignVersionId'],
      'content':current,'grant':'AU-RP-1','budget':'2.00','funding_ref':prospective,'delta':{'O':0,'S':0,'A':0}}
    p=client.committed('propose',proposal)
    r=client.call('reserve',{'grant':'AU-RP-1','amount':'2.00','purpose':{'kind':'Transition','id':tr},'expected_sequence':prospective})
    return {'transition_id':tr,'proposal':p,'funding':r,'successor':current['AgentDesignVersionId']}


def propose_mutated(client,research_ref,case,ordinal,mutations=None,transition_id=None,funding_ref=None):
    """Explicit negative-test program: derive own candidate, then retain mutations."""
    require(case in ('R14','C05','S05','S08') and type(ordinal) is int,'INVALID_CASE')
    # Derive candidate through the genuine program without submitting an
    # unmarked driver-supplied proposal. Mutations can only affect its content.
    profile=client.query('profile');rr=client.query('get',{'ref':research_ref})
    require(rr['kind']=='RESEARCH_RECORD' and rr['actor']==client.actor and not rr['body'].get('failure'),'NO_POSITIVE_RESEARCH')
    c=deepcopy(profile['artifacts']['hypothesis_template']['content'])
    c['motivated_by']=['TH-G1',research_ref]
    c['motivation_closure']={'N':rr['body']['closure']['N'],'refs':rr['body']['closure']['refs']+[research_ref]}
    for change in mutations or []:
        path=change['path'];require(bool(path) and path[0] in c,'INVALID_CASE');target=c
        for field in path[:-1]:target=target[field]
        if change.get('remove'):target.pop(path[-1],None)
        else:target[path[-1]]=deepcopy(change['value'])
    c['adversarial_case']={'case':case,'derived_from':research_ref,'mutations':mutations or []}
    tr=transition_id or f'TR-{case}-{ordinal}'
    future=funding_ref or (client.query('clock')['E'] or 0)+1
    body={'transition_id':tr,'base':client.query('state')['N'],'class':'HYPOTHESIS','subject':c['HypothesisId'],'content':c,
      'budget':'2.00','grant':'AU-RP-1','funding_ref':future,'delta':{'O':0,'S':0,'A':0}}
    proposal=client.committed('propose',body)
    return {'transition_id':tr,'proposal':proposal,'funding_ref':future,'adversarial':True}


def next_experiment(counts,document):
    """A research heuristic, not an Evaluation Standard or standing judgment."""
    large=[r for r in document['rows'] if r['spike'] and r['size_units']>=2]
    require(len(large)==counts['n_large'] and counts['n_large']>0,'NO_TESTABLE_CANDIDATE')
    groups={r['shock_id'] for r in large}
    if len(groups)==1:
        return {'id':'complement-control','question':'Does selling still reach two-thirds after excluding the large-event group?',
          'reason':f"The {counts['k_large']}/{counts['n_large']} large-event result comes from one shock, so it is not independent repetition.",
          'initial_failure':'The large-event result alone cannot justify a claim across shock sizes.',
          'large_shocks':len(groups)}
    return {'id':'independent-reproduction','question':'Does an independent implementation reproduce the multi-shock result?',
      'reason':f"The large events span {len(groups)} shocks; first check calculation reproducibility.",
      'initial_failure':None,'large_shocks':len(groups)}


def _derived_research(client,source,question,result,refs,kind='plain',parameters=None):
    body=deepcopy(source['body']);body.pop('witness',None)
    closure=client.query('closure')
    body.update(question=question,result=result,kind=kind,failure=None,
      closure={'E':closure['E'],'N':closure['N'],'refs':refs})
    if parameters:body['parameters']=parameters
    body['reproducibility']['result_hash']=digest(result)
    body['reproducibility']['input_refs']=refs
    body['reproducibility']['analysis_parameters']=body['parameters']
    body['claims'].append({'kind':'INTERPRETATION','reported':[0],
      'text':question+' '+result['adaptation']['reason']})
    return client.committed('research-commit',body)['refs'][0]


def choose_next_experiment(client,research_ref):
    prior=client.query('get',{'ref':research_ref})
    require(prior['kind']=='RESEARCH_RECORD' and prior['actor']==client.actor and not prior['body'].get('failure'),'NO_POSITIVE_RESEARCH')
    doc_ref=prior['body']['closure']['refs'][0];doc=client.query('get',{'ref':doc_ref})['body']['document']
    choice=next_experiment(prior['body']['result'],doc)
    transition='TR-RESEARCH-'+uuid.uuid4().hex
    result=dict(prior['body']['result'],adaptation={**choice,
      'original_claim':'The observed selling pattern may generalize beyond the largest shocks.',
      'prior_research':research_ref,'method':'shock-concentration-control-v1',
      'candidates':[{'id':'complement-control','cost_estimate_units':'1.00'},
                    {'id':'independent-reproduction','cost_estimate_units':'1.00'}],
      'chosen_subset':[choice['id']],
      'rejections':[{'id':other,'reason':'Does not address the next uncertainty selected by the observed shock concentration.'} for other in ('complement-control','independent-reproduction') if other!=choice['id']],
      'proposing_transitions':[transition],
      'revisit_rule':'Revisit generalization only with a new independent cohort; no economic standing from this synthetic sample.'})
    ref=_derived_research(client,prior,'Which next experiment addresses the limitation in the first result?',result,
      [doc_ref,research_ref],kind='SELECTION',parameters={'threshold':2,'method':'shock-concentration-control-v1','planned_transition':transition})
    return {'selection_ref':ref,'choice':choice}


def run_next_experiment(client,selection_ref):
    selection=client.query('get',{'ref':selection_ref})
    require(selection['kind']=='RESEARCH_RECORD' and selection['actor']==client.actor and selection['body']['kind']=='SELECTION','INVALID_SELECTION')
    plan=selection['body']['result']['adaptation'];prior_ref=plan['prior_research']
    prior=client.query('get',{'ref':prior_ref});doc_ref=prior['body']['closure']['refs'][0]
    doc=client.query('get',{'ref':doc_ref})['body']['document']
    require(next_experiment(prior['body']['result'],doc)['id']==plan['id'],'INVALID_SELECTION')
    # The authorized tool returns the sufficient count statistics. The researcher
    # performs the selected complement contrast; it does not alter source bytes.
    work=research(client,'SYN-B-1');require(not work['failure'],'NO_POSITIVE_RESEARCH')
    measured_ref=work['record']['refs'][0];measured=client.query('get',{'ref':measured_ref})
    counts=measured['body']['result'];n=counts['n']-counts['n_large'];k=counts['k']-counts['k_large']
    contrast=plan['id']=='complement-control'
    passes=n>0 and 3*k>=2*n if contrast else counts==prior['body']['result']
    result=dict(counts,adaptation={'id':plan['id'],'selection_ref':selection_ref,'prior_research':prior_ref,
      'proposing_transition':plan['proposing_transitions'][0],
      'comparison_n':n if contrast else counts['n'],'comparison_k':k if contrast else counts['k'],
      'rule':'3*k >= 2*n on non-large spikes' if contrast else 'exact count reproduction',
      'passes':passes,'reason':f"{k} of {n} non-large spike rows show selling; {'meets' if passes else 'falls below'} the two-thirds comparison." if contrast else 'Independent count reproduction completed.',
      'research_failure':'The broad claim fails this within-cohort control.' if contrast and not passes else None,
      'next_action':'Keep only the narrower large-event question as an unproven hypothesis; seek new independent shocks before generalizing.' if contrast and not passes else 'Seek a new independent cohort before any stronger conclusion.'})
    ref=_derived_research(client,measured,plan['question'],result,[doc_ref,prior_ref,selection_ref,measured_ref],
      parameters={'threshold':2,'analysis':plan['id'],'comparison_ratio':[2,3]})
    return {'research_ref':ref,'measurement_ref':measured_ref,'settlement':work['settlement'],'analysis':result['adaptation']}
