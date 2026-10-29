"""Pure admission calculations. Only Engine can commit their effects.

Offline component tests may supply fabricated views; that is not initialization.
Checker programs do not import this module.
"""
from __future__ import annotations
from .encoding import require, Refusal, units, amount, digest, fields, instant, canonical
from .contracts import COMMON, CLASS_CRITERIA, STEPS


def independence(v, checker, grant, p):
    require(checker in v.designs and v.designs[checker]['method_class'] == 'CHECKER', 'NOT_CHECKER')
    require(checker != p['actor'], 'NOT_INDEPENDENT')
    own = v.lineage(checker)
    if p['actor'] in v.designs:
        require(v.lineage(p['actor']) != own, 'NOT_INDEPENDENT')
    require(not any(checker in g['grantee'] and g['class'] == 'Research'
                    for ident, g in v.grants.items() if ident in v.active), 'NOT_INDEPENDENT')
    c = p['body']['content']
    if p['body']['class'] == 'AGENT_DESIGN':
        require(c.get('AgentDesignLineageId') != own, 'OWN_SUBJECT')
    if p['body']['class'] == 'AUTHORIZATION':
        require(checker not in (c.get('grant') or {}).get('grantee', []) and
                c.get('predecessor') != grant['AuthorizationId'], 'OWN_SUBJECT')


def proposal_authority(v, actor, p, now):
    if actor == 'Principal':
        require(p['grant'] is None and units(p['budget']) == 0 and p['funding_ref'] is None,
                'INVALID_PRINCIPAL_CONTROL')
        return None
    g = v.grant(p['grant'], actor, now, ('Research', 'Checker'))
    if g['class'] == 'Checker':
        raise Refusal('CAPABILITY_UNSUPPORTED', 'Checker-authored successors require a separately supported funding path; Principal control supported')
    v.proposal_scope(g, actor, p)
    require(type(p['funding_ref']) is int and p['funding_ref'] > 0, 'INVALID_FUNDING_REFERENCE')
    return g


def funding(v, proposal, now, bound=False):
    p = proposal['body']; actor = proposal['actor']
    if actor == 'Principal': return
    r = v.reservation(p['funding_ref'], now)
    b = r['record']['body']
    require(b['grant'] == p['grant'] and b['actor'] == actor and
            b['purpose'] == {'kind':'Transition','id':p['transition_id']}, 'WRONG_RESERVATION')
    require(units(p['budget']) <= r['amount'], 'BUDGET_UNCOVERED')
    if not bound:
        require(b['grant'] not in v.fences, 'FENCED')
        require(not r['closed'], 'RESERVATION_CLOSED')


def check_for(v, transition, seq):
    c = v.checks.get(seq)
    require(c is not None and c['transition_id'] == transition, 'NO_CHECK')
    require(c['body']['result'] == 'PASS', 'CHECK_NOT_PASS')
    require(c['body']['base'] == v.n, 'STALE_CHECK')
    return c


def policy_conditions(v, p, now, bound=False):
    b = p['body']; require(b['class'] in ('HYPOTHESIS','AGENT_DESIGN'), 'P1_CLASS')
    require(b['grant'] not in v.suspended and '*' not in v.suspended, 'POLICY_SUSPENDED')
    require(p['actor'] != 'Principal', 'P1_SCOPE')
    if b['class'] == 'AGENT_DESIGN': require(b['content'].get('predecessor') == p['actor'], 'P1_SCOPE')
    proposal_authority(v, p['actor'], b, now)
    funding(v, p, now, bound)
    require(not any(e['kind'] == 'CHECK' and e['transition_id'] == b['transition_id']
                    and e['body']['result'] == 'STOP' for e in v.transitions), 'STOP_PENDING')


def effect(ledger, kind, actor, body, now=None, tr=None):
    return dict(ledger=ledger, kind=kind, actor=actor, body=body, time_ms=now, transition_id=tr)


class Rules:
    def __init__(self, profile): self.profile = profile

    def execute(self, v, actor, op, b, now):
        fn = getattr(self, 'do_' + op.replace('-', '_'), None)
        require(fn is not None, 'CAPABILITY_UNSUPPORTED', op)
        return fn(v, actor, b, now)

    def do_reserve(self, v, actor, b, now):
        g = v.grant(b['grant'], actor, now, ('Research','Checker'))
        require('RESERVATION' in g['may_commit_evidence'],'UNAUTHORIZED')
        require(b['grant'] not in v.fences, 'FENCED')
        if 'expected_sequence' in b:
            require(b['expected_sequence'] == (v.E or 0)+1, 'FUNDING_REFERENCE_TAKEN')
        if b['purpose'].get('kind') == 'Transition':
            p = v.proposals.get(b['purpose']['id']); require(p is not None, 'NO_PROPOSAL')
            require(p['body']['funding_ref'] == (v.E or 0)+1 and b.get('expected_sequence') == (v.E or 0)+1,
                    'WRONG_RESERVATION')
        v.scope(g, actor, b['purpose'])
        a = units(b['amount']); committed, usage = v.totals(b['grant'], now)
        cap = units(g['research_budget_units'])
        require(committed <= cap, 'OVERSPENT')
        require(a <= max(cap-usage,0), 'BUDGET_EXCEEDED')
        lineage = v.lineage(actor)
        _, lu = v.totals(b['grant'], now, lineage)
        require(a+lu <= units(g['per_lineage_cap_units']), 'CAP_EXCEEDED')
        if b['purpose']['kind'] == 'Discovery':
            _, du = v.totals(b['grant'], now, discovery=True)
            require(a+du <= units(g['discovery_scope']['fixed_subgrant_units']), 'DISCOVERY_CAP')
        duration = g['default_reservation_duration_ms']
        expiry = b.get('expiry_ms', now+duration)
        require(type(expiry) is int and now < expiry <= now+duration, 'INVALID_EXPIRY')
        data = dict(grant=b['grant'], actor=actor, lineage=lineage, amount=b['amount'],
                    purpose=b['purpose'], expiry_ms=expiry)
        return [effect('E','RESERVATION',actor,data,now)]

    def do_attempt(self, v, actor, b, now):
        r = v.reservation(b['reservation'], now); rb = r['record']['body']
        require(actor == rb['actor'], 'UNAUTHORIZED')
        g = v.grant(rb['grant'], actor, now, ('Research','Checker'))
        require('attempt' in g['may_commit_evidence'],'UNAUTHORIZED')
        require(rb['grant'] not in v.fences, 'FENCED')
        require(not r['frozen'], 'RESERVATION_BOUND')
        require(now < rb['expiry_ms'], 'RESERVATION_EXPIRED')
        require(not r['closed'], 'RESERVATION_CLOSED')
        maximum = units(b['maximum']); committed, _ = v.totals(rb['grant'], now)
        require(committed <= units(g['research_budget_units']), 'OVERSPENT')
        require(maximum <= r['allowance'], 'ALLOWANCE_EXCEEDED')
        require(maximum <= max(units(g['research_budget_units'])-committed,0), 'GRANT_EXHAUSTED')
        lc, _ = v.totals(rb['grant'], now, rb['lineage'])
        require(lc+maximum <= units(g['per_lineage_cap_units']), 'CAP_EXHAUSTED')
        require(b['step'] in STEPS and b['input']['step'] == b['step'], 'INVALID_STEP')
        fields(b['input'], {'schema_version','tool_id','tool_spec_hash','executable_hash','step','parameters','input_refs'})
        require(b['input']['schema_version']==1, 'INVALID_INPUT')
        for ref in b['input']['input_refs']:
            raw=v.exact(ref)['body']
            require(ref.get('raw_sha256')==digest(raw.get('document',raw)), 'INVALID_INPUT_HASH')
        tool = next((t for t in g['tools'] if t['id'] == b['input']['tool_id']), None)
        require(tool is not None and b['tier'] == tool['tier'] == 1, 'TOOL_NOT_PERMITTED')
        require(tool['spec_sha256'] == b['input']['tool_spec_hash'], 'TOOL_VERSION_MISMATCH')
        require(v.designs[actor]['tool_specs'].get(tool['id']) == tool['spec_sha256'], 'TOOL_NOT_PERMITTED')
        expected_code = self.profile.inventory['tool_executables'][tool['id']]
        require(b['input']['executable_hash'] == expected_code, 'TOOL_VERSION_MISMATCH')
        if tool['id'].startswith('CHECK'):
            require(b['step'] == 'check-transition' and rb['purpose']['kind'] == 'Check', 'PURPOSE_OUT_OF_SCOPE')
            require(b['input']['parameters']['transition_id'] == rb['purpose']['id'], 'PURPOSE_OUT_OF_SCOPE')
            require(maximum == 25, 'INVALID_ESTIMATE')
        else:
            require(b['step'] in ('research-counts','replacement-counts'), 'INVALID_STEP')
            docs = [v.exact(ref) for ref in b['input']['input_refs']]
            require(len(docs) == 1 and docs[0]['kind'] == 'OBSERVATION' and docs[0]['body']['form'] == 'DOCUMENT', 'INVALID_INPUT')
            require(len(canonical(docs[0]['body']['document']))<=16*1024*1024, 'INPUT_TOO_LARGE')
            require(b['input']['parameters']=={'threshold':2}, 'CAPABILITY_UNSUPPORTED')
            count = len(docs[0]['body']['document'].get('rows', []))
            require(count <= 4096 and maximum == (100 if count <= 1024 else 200), 'INVALID_ESTIMATE')
        ih = digest(b['input']); index = b['dispatch_index']
        require(type(index) is int and index >= 0, 'INVALID_DISPATCH_INDEX')
        previous = [e for e in v.attempts.values() if e['body']['reservation'] == b['reservation'] and
                    e['body']['step'] == b['step'] and e['body']['input_hash'] == ih]
        require(not any(e['body']['dispatch_index'] == index for e in previous), 'DUPLICATE_ATTEMPT')
        require(index == max((e['body']['dispatch_index'] for e in previous), default=-1)+1, 'INVALID_DISPATCH_INDEX')
        data = dict(b, input_hash=ih, actor=actor, grant=rb['grant'], lineage=rb['lineage'], status='PENDING')
        return [effect('E','ATTEMPT',actor,data,now)]

    def do_settle(self, v, actor, b, now):
        a = v.attempts.get(b['attempt']); require(a is not None, 'INVALID_SETTLEMENT')
        require(actor in ('Principal', a['actor']), 'INVALID_SETTLEMENT')
        require(b['unit'] == 'simulated_research_units', 'INVALID_SETTLEMENT')
        try: actual = units(b['actual'])
        except Refusal as exc: raise Refusal('INVALID_SETTLEMENT') from exc
        require(isinstance(b['provenance'], dict) and b['provenance'].get('kind') in ('TOOL_RECEIPT','UNKNOWN'), 'INVALID_SETTLEMENT')
        if b['provenance']['kind'] == 'UNKNOWN':
            require(actual == units(a['body']['maximum']), 'INVALID_SETTLEMENT')
        else:
            receipt = b['provenance'].get('receipt', {})
            require(receipt.get('attempt') == b['attempt'] and receipt.get('input_hash') == a['body']['input_hash']
                    and receipt.get('actual') == b['actual'] and receipt.get('synthetic') is True, 'INVALID_SETTLEMENT')
        require(b['attempt'] not in v.settlements, 'ALREADY_SETTLED')
        return [effect('E','SETTLEMENT',actor,dict(b, reservation=a['body']['reservation'],grant=a['body']['grant']))]

    def do_close(self, v, actor, b, now):
        r = v.reservation(b['reservation'], now)
        require(r['record']['actor'] == actor, 'UNAUTHORIZED')
        v.grant(r['record']['body']['grant'],actor,now,('Research','Checker'))
        require(not r['frozen'], 'RESERVATION_BOUND')
        require(b['reservation'] not in v.closed, 'ALREADY_CLOSED')
        return [effect('E','CLOSED',actor,dict(b,released_allowance=amount(r['allowance'])),now)]

    def do_fence(self, v, actor, b, now):
        require(actor == 'Principal', 'UNAUTHORIZED')
        require(b['grant'] in v.grants and v.grants[b['grant']]['class'] in ('Research','Checker'), 'NO_AUTHORIZATION')
        require(b['grant'] not in v.fences, 'ALREADY_FENCED')
        return [effect('E','FENCE',actor,b)]

    def do_propose(self, v, actor, b, now):
        require(b['class'] in CLASS_CRITERIA, 'CAPABILITY_UNSUPPORTED')
        require(b['transition_id'] not in v.proposals, 'DUPLICATE_TRANSITION')
        require(b['base'] == v.n and v.n is not None, 'STALE_BASE')
        require(b['delta'] == {'O':0,'S':0,'A':0}, 'CONSTITUTIONAL_STOP')
        proposal_authority(v,actor,b,now)
        if b['class'] in ('AUTHORIZATION','LIMITS','SUSPEND_POLICY'): require(actor == 'Principal', 'UNAUTHORIZED')
        if b['class']=='LIMITS':
            for key,value in b['content'].items():
                if key.endswith('_units') and value is not None:units(value)
        if b['class'] == 'AUTHORIZATION':
            fields(b['content'], {'action','grant','predecessor'})
            require(b['content']['action'] in ('GRANT','SUPERSEDE','REVOKE'), 'CAPABILITY_UNSUPPORTED')
        return [effect('T','PROPOSED',actor,b,now,b['transition_id'])]

    def do_check_commit(self, v, actor, b, now):
        p = v.proposals.get(b['transition_id']); require(p is not None, 'NO_PROPOSAL')
        g = v.grant(b['grant'],actor,now,('Checker',)); require(bool(g['may_check']),'UNAUTHORIZED'); independence(v,actor,g,p)
        require(b['base'] == v.n, 'STALE_CHECK')
        require(b['context']['subject']==p['body']['subject'] and b['context']['class']==p['body']['class'] and b['context']['proposer']['identity']==p['actor'] and b['context']['checker']['identity']==actor,'INVALID_CHECK')
        require(b['constitution'] == 1 and b['es'] == 'ES-1.0', 'WRONG_STANDARD')
        closure = b['closure']
        require(closure['N'] == v.n and closure['F'] == 'N/A — no Paper Book' and
                type(closure['E']) is int and closure['E'] <= (v.E or 0), 'INVALID_CLOSURE')
        require(type(closure['time_ms']) is int and closure['time_ms'] <= now, 'INVALID_CLOSURE')
        a = v.attempts.get(b['attempt']); require(a is not None and a['actor'] == actor and
             a['body']['grant'] == b['grant'] and a['body']['step'] == 'check-transition', 'UNFUNDED_CHECK')
        r = v.reservations[a['body']['reservation']]
        require(r['body']['purpose'] == {'kind':'Check','id':b['transition_id']}, 'UNFUNDED_CHECK')
        require(a['seq'] <= closure['E'], 'INVALID_CLOSURE')
        expected = set(COMMON + CLASS_CRITERIA[p['body']['class']])
        require(set(b['criteria']) == expected, 'INCOMPLETE_CHECK')
        outcomes = []
        for observation in b['criteria'].values():
            fields(observation, {'status','reason','refs'})
            require(observation['status'] in ('MET','NOT MET','NOT DETERMINABLE'), 'INVALID_CHECK')
            for ref in observation['refs']:
                e = v.exact(ref)
                if ref['ledger'] == 'E': require(e['seq'] <= closure['E'], 'OUTSIDE_CLOSURE')
            outcomes.append(observation['status'])
        result = 'STOP' if 'NOT DETERMINABLE' in outcomes else ('FAIL' if 'NOT MET' in outcomes else 'PASS')
        require(b['result'] == result, 'INVALID_CHECK_RESULT')
        require(b['provenance'] == v.designs[actor]['provenance'], 'PROVENANCE_MISMATCH')
        return [effect('T','CHECK',actor,b,now,b['transition_id'])]

    def do_decide(self, v, actor, b, now):
        require(actor == 'Principal', 'UNAUTHORIZED')
        p = v.proposals.get(b['transition_id']); require(p is not None, 'NO_PROPOSAL')
        require(b['decision'] in ('ADMITTED','REJECTED','STOPPED'), 'INVALID_DECISION')
        c = v.checks.get(b['check']); require(c is not None and c['transition_id'] == b['transition_id'], 'NO_CHECK')
        require(c['body']['base'] == v.n, 'STALE_CHECK')
        if b['decision'] == 'ADMITTED':
            check_for(v,b['transition_id'],b['check']); proposal_authority(v,p['actor'],p['body'],now)
        return [effect('T','DECISION',actor,dict(b,base=v.n,decider='Principal'),now,b['transition_id'])]

    def do_policy_decide(self, v, actor, b, now):
        require(actor == '@Apply', 'UNAUTHORIZED')
        p = v.proposals.get(b['transition_id']); require(p is not None, 'NO_PROPOSAL')
        check_for(v,b['transition_id'],b['check']); policy_conditions(v,p,now)
        return [effect('T','DECISION',actor,dict(b,base=v.n,decision='ADMITTED',decider='P-1 (TR-0)'),now,b['transition_id'])]

    def do_bind(self, v, actor, b, now):
        require(actor == '@Apply', 'UNAUTHORIZED')
        tr = b['transition_id']; p = v.proposals[tr]; pb = p['body']
        d = v.decisions.get(b['decision']); require(d is not None and d['transition_id'] == tr and
              d['body']['decision'] == 'ADMITTED', 'NOT_DECIDED')
        require(tr not in v.applies, 'ALREADY_APPLIED')
        require(p['actor'] != 'Principal', 'BIND_NOT_APPLICABLE')
        require(not any(x['body']['transition_id'] == tr and v.binding_state(k) in ('FROZEN','PENDING_RELEASE')
                        for k,x in v.binds.items()), 'ALREADY_BOUND')
        funding(v,p,now)
        r = v.reservation(pb['funding_ref'],now); g = v.grants[pb['grant']]
        require(not r['frozen'], 'ALREADY_BOUND')
        require(g['class'] == 'Research', 'BIND_NOT_APPLICABLE')
        require(now < r['record']['body']['expiry_ms'], 'RESERVATION_EXPIRED')
        require(v.totals(pb['grant'],now)[0] <= units(g['research_budget_units']), 'OVERSPENT')
        return [effect('E','BIND',actor,dict(transition_id=tr,reservation=pb['funding_ref'],
                    decision=b['decision'],interval_ms=g['binding_interval_ms'],time_ms=now),now)]

    def do_apply(self, v, actor, b, now):
        require(actor == '@Apply', 'UNAUTHORIZED')
        tr = b['transition_id']; p = v.proposals.get(tr); require(p is not None, 'NO_PROPOSAL')
        require(tr not in v.applies, 'ALREADY_APPLIED')
        d = v.decisions.get(b['decision']); require(d is not None and d['transition_id'] == tr and d['body']['decision'] == 'ADMITTED','NOT_DECIDED')
        check_for(v,tr,d['body']['check'])
        require(d['body']['base'] == v.n, 'STALE_DECISION')
        proposal_authority(v,p['actor'],p['body'],now)
        if p['actor'] != 'Principal':
            bind = v.binds.get(b.get('bind')); require(bind is not None and bind['body']['transition_id'] == tr and
                     bind['body']['decision'] == b['decision'], 'WRONG_BINDING')
            require(v.binding_state(bind['seq']) == 'FROZEN', 'BINDING_INVALIDATED')
            funding(v,p,now,bound=True)
        else: require(b.get('bind') is None, 'BIND_NOT_APPLICABLE')
        if d['body']['decider'].startswith('P-1'): policy_conditions(v,p,now,bound=True)
        c, cls = p['body']['content'], p['body']['class']
        if cls == 'AUTHORIZATION':
            require(c['grant']['AuthorizationId'] not in v.grants, 'DUPLICATE_AUTHORIZATION')
            if c['predecessor']:
                require(c['predecessor'] in v.active, 'AUTHORIZATION_INACTIVE')
                if v.grants[c['predecessor']]['class'] in ('Research','Checker'):
                    require(c['predecessor'] in v.fences, 'FENCE_REQUIRED')
        if cls == 'AGENT_DESIGN': require(c['AgentDesignVersionId'] not in v.designs, 'DUPLICATE_SUBJECT')
        if cls == 'HYPOTHESIS': require(c['HypothesisId'] not in v.hypotheses, 'DUPLICATE_SUBJECT')
        if cls == 'THEME': require(c['ThemeId'] not in v.themes, 'DUPLICATE_SUBJECT')
        return [effect('T','APPLIED',actor,dict(n=v.n+1,check=d['body']['check'],decision=b['decision'],
                       bind=b.get('bind'),constitution=1,es='ES-1.0'),now,tr)]

    def do_invalidate_request(self, v, actor, b, now):
        require(actor == '@Apply', 'UNAUTHORIZED')
        bind = v.binds.get(b['bind']); require(bind is not None, 'NO_BINDING')
        require(v.binding_state(b['bind']) == 'FROZEN', 'BINDING_TERMINAL')
        require(now-bind['body']['time_ms'] > bind['body']['interval_ms'], 'INTERVAL_NOT_ELAPSED')
        return [effect('T','BINDING_INVALIDATED',actor,dict(bind=b['bind'],ground='INTERVAL_ELAPSED',
                  interval_ms=bind['body']['interval_ms'],clock={'t':now,'E':v.E},requester='@Apply'),now,bind['body']['transition_id'])]

    def do_release(self, v, actor, b, now):
        require(actor == '@Apply', 'UNAUTHORIZED')
        require(b['bind'] in v.binds, 'NO_BINDING')
        require(b['bind'] not in v.releases, 'ALREADY_RELEASED')
        require(b['bind'] in v.invalidations, 'NO_INVALIDATION')
        return [effect('E','RELEASE',actor,dict(bind=b['bind'],invalidation=v.invalidations[b['bind']]['seq']),now)]

    def do_research_commit(self, v, actor, b, now):
        g=v.grant(b['grant'],actor,now,('Research','Checker'))
        right='Research Record for verification' if g['class']=='Checker' else ('plain Research Record' if b['kind']=='plain' else b['kind'])
        require(right in g['may_commit_evidence'],'UNAUTHORIZED')
        a = v.attempts.get(b['attempt']); require(a is not None and a['actor'] == actor and a['body']['grant'] == b['grant'], 'UNAUTHORIZED')
        require(b['synthetic'] is True and b['kind'] in ('plain','SCREEN','EXPERIMENT DESIGN','SELECTION'), 'CAPABILITY_UNSUPPORTED')
        require(b['closure']['N'] <= v.n and b['closure']['E'] <= v.E, 'INVALID_CLOSURE')
        for ref in b['closure']['refs']:
            e = v.exact(ref)
            if ref['ledger'] == 'E': require(e['seq'] <= b['closure']['E'], 'OUTSIDE_CLOSURE')
        require(b['snapshot'] and b['source_cutoff'] and b['tool'] and b['reproducibility'], 'INCOMPLETE_RESEARCH_RECORD')
        return [effect('E','RESEARCH_RECORD',actor,b,now)]

    def do_observation_commit(self, v, actor, b, now):
        require(actor == 'Observation function', 'UNAUTHORIZED')
        g = v.grant(b['grant'],actor,now,('Observation',))
        right='DOCUMENT Observation' if b['form']=='DOCUMENT' else ('feed retrieval COMPLETE/PARTIAL/RETRIEVAL_FAILED' if b['form'] in ('COMPLETE','PARTIAL') else 'Market Observation VALUE/ABSENT/NOT_EXTRACTABLE/RETRIEVAL_FAILED')
        require(right in g['may_commit_evidence'],'UNAUTHORIZED')
        src = next((s for s in g['source_declarations'] if s['content']['SourceId']==b['source']),None)
        require(src is not None and src['SourceRevision'] == b['revision'], 'SOURCE_NOT_ACTIVE')
        require(b['source'] == 'SRC-SYN', 'CAPABILITY_UNSUPPORTED')
        require(b['slot']==now, 'STALE_OBSERVATION_SLOT')
        start,end=instant(b['period']['start']),instant(b['period']['end'])
        require(end-start==86400000 and start%86400000==0 and
                instant('2026-10-28T00:00:00.000Z')<=start<instant('2027-04-30T00:00:00.000Z'),'INVALID_PERIOD')
        require(b['item_id']=='cohort-'+b['period']['start'][:10],'INVALID_ITEM')
        require(b['form'] in ('DOCUMENT','VALUE','NOT_EXTRACTABLE','RETRIEVAL_FAILED','COMPLETE','PARTIAL'),'CAPABILITY_UNSUPPORTED')
        if b['form']=='DOCUMENT':
            d=b['document']
            require(d.get('synthetic') is True and b['item_id']==d['item_id'] and
                    d['period_start']==b['period']['start'] and d['period_end']==b['period']['end'],'INVALID_DOCUMENT')
            require(end<=now,'SOURCE_NOT_YET_AVAILABLE')
            require(len(canonical(d))<=16*1024*1024,'INPUT_TOO_LARGE')
        elif b['form'] in ('VALUE','NOT_EXTRACTABLE'):
            document=v.exact(b['document_ref']);db=document['body']
            require(document['kind']=='OBSERVATION' and db['form']=='DOCUMENT' and
                    db['source']==b['source'] and db['revision']==b['revision'] and
                    db['period']==b['period'] and db['item_id']==b['item_id'],'INVALID_EXTRACTION_BINDING')
            try:
                rows=db['document']['rows'];seen=set();n=k=0
                for row in rows:
                    require(isinstance(row['event_id'],str) and row['event_id'] not in seen and type(row['size_units']) is int and
                            type(row['spike']) is bool and type(row['selling']) is bool,'NOT_EXTRACTABLE')
                    seen.add(row['event_id'])
                    if row['spike'] and row['size_units']>=2:n+=1;k+=int(row['selling'])
                extractable=n>0
            except (Refusal,KeyError,TypeError):extractable=False
            if b['form']=='VALUE':require(extractable and b.get('value')=={'numerator':k,'denominator':n},'INVALID_EXTRACTION')
            else:require(not extractable and bool(b.get('error')),'INVALID_EXTRACTION')
        elif b['form']=='COMPLETE':
            require(b.get('window')==b['period'] and b.get('items')==([b['item_id']] if end<=now else []),'INCOMPLETE_LISTING')
        else:require(bool(b.get('error')),'MISSING_RETRIEVAL_FAILURE')
        return [effect('E','OBSERVATION',actor,dict(b,synthetic=True),now)]
