"""Exclusive governed boundaries. Construction requires a separately approved run."""
from __future__ import annotations
import sqlite3
import threading
import uuid
from .encoding import canonical, decode, digest, require, Refusal, units, amount
from .contracts import validate, READS
from .model import View
from .rules import Rules, effect
from .profile import CV1

TIMELESS = {'settle','fence'}
INTERNAL = {'bind','release','invalidate-request','policy-decide','apply'}


class Engine:
    def __init__(self, store, profile, clock, run_permission, fault_hook=None):
        require(run_permission is not None and run_permission.get('inventory_sha256') == profile.inventory_hash
                and run_permission.get('allow_apply_zero') is True, 'RUN_APPROVAL_REQUIRED')
        self.store, self.profile, self.clock = store, profile, clock
        self.rules = Rules(profile)
        self.dispatcher = None
        self.generation = None
        self.lock = threading.RLock()
        self.fault_hook = fault_hook or (lambda point: None)

    def view(self): return View(self.store.events('E'), self.store.events('T'))

    def now(self):
        t = self.clock.read()
        h = self.store.high_water()
        require(h is None or t >= h, 'CLOCK_ROLLBACK')
        return t

    def query(self, actor, op, b):
        with self.lock:
            v = self.view()
            if op == 'dispatch-status':
                require(actor=='Principal','UNAUTHORIZED')
                return {'claims':[{'attempt':r['attempt_seq'],'claim':decode(r['body']),'receipt':decode(r['receipt']) if r['receipt'] else None} for r in self.store.db.execute('SELECT * FROM dispatch_claims ORDER BY attempt_seq')], 'classification':'OPERATIONAL_RECEIPT_NOT_AUTHORIZATION'}
            if op == 'profile':
                return {'setup':self.profile.setup,'artifacts':self.profile.artifacts,'experiment':self.profile.experiment.data,
                        'inventory':self.profile.inventory,'inventory_sha256':self.profile.inventory_hash}
            if op == 'clock': return {'t':self.now(),'E':v.E}
            if op == 'closure':
                t = self.now(); result = v.export(); result['time_ms']=t; return result
            if op == 'inspect-request':
                final=self.store.lookup(actor,b['request_id'])
                if final:return final
                partial=self.store.lookup(actor,b['request_id']+'/bind')
                return {'status':'PARTIAL','stage':'BIND','receipt':partial} if partial else {'status':'UNKNOWN'}
            if op == 'get': return v.exact(b['ref'])
            if op == 'history':
                require(b['ledger'] in ('E','T'), 'INVALID_LEDGER')
                limit = b.get('limit',100); require(type(limit) is int and 0 < limit <= 1000,'INVALID_LIMIT')
                items = v.evidence if b['ledger']=='E' else v.transitions
                upper = b.get('through',max((e['seq'] for e in items),default=0))
                page=[e for e in items if b.get('after',0)<e['seq']<=upper][:limit]
                return {'records':page,'through':upper,'next_after':page[-1]['seq'] if page else b.get('after',0)}
            if op == 'state':
                if 'N' in b:
                    require(type(b['N']) is int and v.n is not None and 0 <= b['N']<=v.n,'INVALID_STATE')
                    v=View(v.evidence,v.transitions,at_n=b['N'])
                return {'N':v.n,'designs':v.designs,'grants':v.grants,'active':sorted(v.active),
                        'themes':v.themes,'hypotheses':v.hypotheses,'limits':v.limits,'suspended':sorted(v.suspended)}
            if op == 'budget':
                g=v.grants.get(b['grant']); require(g is not None,'NO_AUTHORIZATION')
                now=self.now(); c,u=v.totals(b['grant'],now); cap=units(g['research_budget_units'])
                return {'grant':b['grant'],'committed':amount(c),'reserved':amount(u),'headroom':amount(max(cap-c,0)),
                        'spendable':amount(max(cap-u,0)),'overspent':c>cap,'E':v.E,'N':v.n,'time_ms':now}
            if op == 'obligations':
                return {'pending_attempts':[k for k in v.attempts if k not in v.settlements],
                        'bindings':{str(k):v.binding_state(k) for k in v.binds},
                        'decided_unapplied':[e['transition_id'] for e in v.decisions.values()
                                            if e['body']['decision']=='ADMITTED' and e['transition_id'] not in v.applies],
                        'E':v.E,'N':v.n,'no_authority_conferred':True}
            raise Refusal('CAPABILITY_UNSUPPORTED',op)

    def command(self, actor, key, op, payload):
        try:parsed=uuid.UUID(key)
        except (ValueError,TypeError,AttributeError) as exc:raise Refusal('INVALID_REQUEST_KEY') from exc
        require(parsed.version==4 and str(parsed)==key,'INVALID_REQUEST_KEY')
        validate(op,payload)
        if op == 'genesis': return self.genesis(actor,key,payload)
        if op == 'apply':
            original_hash=digest({'op':op,'payload':payload})
            with self.lock:
                previous=self.store.lookup(actor,key,original_hash)
                self.store.lookup(actor,key+'/bind',original_hash)
            if previous is not None:return previous
            with self.lock:v=self.view()
            p=v.proposals.get(payload['transition_id'])
            if p is None:return self._commit(actor,key,op,payload,failure='NO_PROPOSAL')
            if actor not in ('Principal',p['actor']):return self._commit(actor,key,op,payload,failure='UNAUTHORIZED')
            bound=payload.get('bind')
            if p['actor']!='Principal' and bound is None:
                br=self._commit(actor,key+'/bind','bind',payload,internal=True,request_hash=original_hash)
                if br['status']!='COMMITTED': return br
                bound=br['refs'][0]['sequence']
                self.fault_hook('after_bind_commit')
            return self._commit(actor,key,'apply',dict(payload,bind=bound),internal=True,request_hash=original_hash)
        if op in ('policy-decide','invalidate-request','release'):
            if actor!='Principal':return self._commit(actor,key,op,payload,failure='UNAUTHORIZED')
            # Ingress requests continuation; the caller never supplies the acting role.
            return self._commit(actor,key,op,payload,internal=True)
        return self._commit(actor,key,op,payload)

    def _commit(self, caller, key, op, payload, internal=False, request_hash=None, failure=None):
        request_hash=request_hash or digest({'op':op,'payload':payload})
        with self.lock, self.store.transaction():
            previous=self.store.lookup(caller,key,request_hash)
            if previous is not None: return previous
            self.store.begin_command(caller,key,request_hash)
            v=self.view(); now=None
            if v.n is None:
                result={'status':'REFUSED','reason':'NOT_INITIALIZED','refs':[],'request':payload}
                self.store.remember(caller,key,request_hash,result);return result
            acting='@Apply' if internal else caller
            try:
                if failure:raise Refusal(failure)
                if internal:
                    if op in ('policy-decide','invalidate-request','release'):require(caller=='Principal','UNAUTHORIZED')
                    else:require(caller=='Principal' or caller in v.designs,'UNAUTHORIZED')
                if op not in TIMELESS: now=self.now()
                if op=='settle' and payload['provenance'].get('kind')=='TOOL_RECEIPT':
                    row=self.store.db.execute('SELECT receipt FROM dispatch_claims WHERE attempt_seq=?',(payload['attempt'],)).fetchone()
                    require(row is not None and row['receipt'] is not None and decode(row['receipt'])==payload['provenance']['receipt'],'INVALID_SETTLEMENT')
                if op=='check-commit':
                    row=self.store.db.execute('SELECT receipt FROM dispatch_claims WHERE attempt_seq=?',(payload['attempt'],)).fetchone()
                    require(row is not None and row['receipt'] is not None and decode(row['receipt']).get('result')==payload, 'UNVERIFIED_CHECK')
                actions=self.rules.execute(v,acting,op,payload,now)
                if internal:
                    for action in actions:action['body'].update(requester=caller,acting_role='@Apply')
                if op=='attempt':
                    if self.dispatcher is not None:self.dispatcher.ensure_retry(v,caller,payload)
                    actions[0]['body']['admission_generation']=self.generation
                result=self._persist(actions)
            except Refusal as exc:
                # Clock/storage unavailability is operational, never a claimed durable domain refusal.
                if exc.code in ('CLOCK_UNAVAILABLE','CLOCK_ROLLBACK','LEDGER_UNREACHABLE'): raise
                ledger='T' if op in ('propose','check-commit','decide','policy-decide','apply','invalidate-request') else 'E'
                tr=payload.get('transition_id','@request:'+key)
                refs=[self.store.append(ledger,'REFUSAL',caller,{'op':op,'request':payload,'reason':exc.code,
                        'detail':exc.detail,'E':v.E,'N':v.n},now,tr if ledger=='T' else None)]
                if (op=='apply' and failure is None and exc.code not in ('WRONG_BINDING','NOT_DECIDED','UNAUTHORIZED','BIND_NOT_APPLICABLE','NO_PROPOSAL') and payload.get('bind') in v.binds
                    and v.binds[payload['bind']]['body']['transition_id']==payload.get('transition_id')
                    and v.binds[payload['bind']]['body']['decision']==payload.get('decision')
                    and v.binding_state(payload['bind'])=='FROZEN'):
                    bind=payload['bind']
                    invalid=self.store.append('T','BINDING_INVALIDATED','@Apply',
                         {'bind':bind,'ground':'APPLY_REFUSED','reason':exc.code,'refusal':refs[0],
                          'authority':{'E':v.E,'N':v.n},'requester':caller,'acting_role':'@Apply'},now,v.binds[bind]['body']['transition_id'])
                    self.store.db.execute('INSERT INTO dispositions VALUES(?,?,?)',(bind,invalid['sequence'],'INVALIDATED'))
                    refs.append(invalid)
                result={'status':'REFUSED','reason':exc.code,'detail':exc.detail,'refs':refs}
            self.fault_hook('before_'+op+'_commit')
            self.store.remember(caller,key,request_hash,result)
            return result

    def _persist(self, actions):
        refs=[]
        for a in actions:
            if a['ledger']=='E':
                a['body'].setdefault('witness',{'E':self.store.db.execute('SELECT MAX(seq) FROM evidence').fetchone()[0], 'N':self.store.db.execute('SELECT MAX(n) FROM applied').fetchone()[0]})
            ref=self.store.append(a['ledger'],a['kind'],a['actor'],a['body'],a['time_ms'],a['transition_id']);refs.append(ref)
            if a['kind']=='APPLIED':
                b=a['body'];self.store.db.execute('INSERT INTO applied VALUES(?,?,?,?)',
                     (b['n'],ref['sequence'],a['transition_id'],b.get('bind')))
                if b.get('bind'):
                    self.store.db.execute('INSERT INTO dispositions VALUES(?,?,?)',(b['bind'],ref['sequence'],'CONSUMED'))
            if a['kind']=='BINDING_INVALIDATED':
                self.store.db.execute('INSERT INTO dispositions VALUES(?,?,?)',(a['body']['bind'],ref['sequence'],'INVALIDATED'))
        return {'status':'COMMITTED','refs':refs}

    def genesis(self, actor, key, b):
        h=digest({'op':'genesis','payload':b})
        with self.lock, self.store.transaction():
            prev=self.store.lookup(actor,key,h)
            if prev is not None:return prev
            self.store.begin_command(actor,key,h)
            v=self.view()
            if actor!='Principal':
                refs=[self.store.append('T','REFUSAL',actor,{'reason':'UNAUTHORIZED','request':b},transition_id='@genesis-refused')] if v.n is not None else []
                result={'status':'REFUSED','reason':'UNAUTHORIZED','refs':refs,'request':b}
                self.store.remember(actor,key,h,result);return result
            pair=self.profile.experiment.genesis
            expected={'constitution_sha256':CV1,'design':self.profile.designs[pair['design']],
                      'grant':self.profile.grants[pair['grant']]}
            if v.evidence or v.transitions or b!=expected:
                # Pre-initialization receipts are operational. Neither governed
                # ledger acquires a record before the exact empty-ledger Apply 0.
                refs=[]
                if v.n is not None:
                    refs=[self.store.append('T','REFUSAL',actor,{'reason':'GENESIS_SCOPE','request':b},transition_id='@genesis-refused')]
                result={'status':'REFUSED','reason':'GENESIS_SCOPE','refs':refs,'request':b}
            else:
                t=self.now()
                p=self.store.append('T','PROPOSED',actor,{'class':'GENESIS','content':b,'transition_id':'TR-0',
                      'base':None,'grant':None,'budget':'0.00','funding_ref':None,'subject':'CV1','delta':{'O':0,'S':0,'A':0}},t,'TR-0')
                d=self.store.append('T','DECISION',actor,{'decision':'ADMITTED','decider':'Principal',
                     'waiver':'CV1 Part V exact sequence-zero only','proposal':p},t,'TR-0')
                a=self.store.append('T','APPLIED',actor,{'n':0,'genesis':b,'decision':d['sequence'],
                    'bind':None,'constitution':1,'es':'ES-1.0'},t,'TR-0')
                self.store.db.execute('INSERT INTO applied VALUES(?,?,?,NULL)',(0,a['sequence'],'TR-0'))
                result={'status':'COMMITTED','refs':[p,d,a]}
            self.store.remember(actor,key,h,result)
            return result
