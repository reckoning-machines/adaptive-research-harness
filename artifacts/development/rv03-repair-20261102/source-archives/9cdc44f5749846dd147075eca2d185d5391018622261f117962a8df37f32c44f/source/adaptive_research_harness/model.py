"""Rebuildable views over immutable records. Never a writable state owner."""
from __future__ import annotations
from copy import deepcopy
from .encoding import units, require, Refusal, instant, digest


class View:
    def __init__(self, evidence=(), transitions=(), at_n=None):
        self.evidence = list(evidence)
        self.transitions = list(transitions)
        self.by_e = {e['seq']: e for e in self.evidence}
        self.by_t = {e['seq']: e for e in self.transitions}
        self.proposals, self.checks, self.decisions = {}, {}, {}
        self.applies, self.invalidations, self.releases = {}, {}, {}
        self.designs, self.grants, self.themes, self.hypotheses = {}, {}, {}, {}
        self.active, self.revoked, self.suspended = set(), set(), set()
        self.limits, self.n, self.constitution = None, None, None
        self.fences = {e['body']['grant']: e['seq'] for e in self.evidence if e['kind'] == 'FENCE'}
        for e in self.transitions:
            b, kind = e['body'], e['kind']
            if kind == 'PROPOSED':
                self.proposals[e['transition_id']] = e
            elif kind == 'CHECK':
                self.checks[e['seq']] = e
            elif kind == 'DECISION':
                self.decisions[e['seq']] = e
            elif kind == 'BINDING_INVALIDATED':
                self.invalidations[b['bind']] = e
            elif kind == 'APPLIED' and (at_n is None or b['n'] <= at_n):
                self.n = b['n']
                self.applies[e['transition_id']] = e
                if 'genesis' in b:
                    g = b['genesis']
                    self.constitution = g['constitution_sha256']
                    self.designs[g['design']['AgentDesignVersionId']] = g['design']
                    self.grants[g['grant']['AuthorizationId']] = g['grant']
                    self.active.add(g['grant']['AuthorizationId'])
                else:
                    p = self.proposals[e['transition_id']]['body']
                    c, cls = p['content'], p['class']
                    if cls == 'AUTHORIZATION':
                        if c['predecessor']:
                            self.active.discard(c['predecessor']); self.revoked.add(c['predecessor'])
                        g = c['grant']; ident = g['AuthorizationId']
                        self.grants[ident] = g
                        if c['action'] != 'REVOKE': self.active.add(ident)
                        else: self.revoked.add(ident)
                    elif cls == 'AGENT_DESIGN': self.designs[c['AgentDesignVersionId']] = c
                    elif cls == 'THEME': self.themes[c['ThemeId']] = c
                    elif cls == 'HYPOTHESIS': self.hypotheses[c['HypothesisId']] = c
                    elif cls == 'LIMITS': self.limits = c
                    elif cls == 'SUSPEND_POLICY': self.suspended.add(c['scope'])
        self.reservations = {e['seq']: e for e in self.evidence if e['kind'] == 'RESERVATION'}
        self.attempts = {e['seq']: e for e in self.evidence if e['kind'] == 'ATTEMPT'}
        self.settlements = {e['body']['attempt']: e for e in self.evidence if e['kind'] == 'SETTLEMENT'}
        self.closed = {e['body']['reservation']: e for e in self.evidence if e['kind'] == 'CLOSED'}
        self.binds = {e['seq']: e for e in self.evidence if e['kind'] == 'BIND'}
        self.releases = {e['body']['bind']: e for e in self.evidence if e['kind'] == 'RELEASE'}

    @property
    def E(self): return max(self.by_e, default=None)

    def exact(self, ref):
        require(ref.get('ledger') in ('E','T'), 'INVALID_REFERENCE')
        e = (self.by_e if ref['ledger'] == 'E' else self.by_t).get(ref['sequence'])
        require(e is not None and e['sha256'] == ref['sha256'], 'INVALID_REFERENCE')
        return e

    def grant(self, ident, actor, now, cls=None):
        g = self.grants.get(ident)
        require(g is not None and ident in self.active, 'AUTHORIZATION_INACTIVE')
        require(actor in g['grantee'], 'UNAUTHORIZED')
        require(now is not None and now < instant(g['expiry']), 'AUTHORIZATION_EXPIRED')
        if cls: require(g['class'] in cls, 'UNAUTHORIZED')
        return g

    def lineage(self, actor):
        require(actor in self.designs, 'UNREGISTERED_DESIGN')
        return self.designs[actor]['AgentDesignLineageId']

    def binding_state(self, bind):
        e = self.binds.get(bind)
        require(e is not None, 'NO_BINDING')
        if any(a['body'].get('bind') == bind for a in self.applies.values()): return 'CONSUMED'
        if bind in self.invalidations:
            return 'RELEASED' if bind in self.releases else 'PENDING_RELEASE'
        return 'FROZEN'

    def reservation(self, seq, now=None):
        e = self.reservations.get(seq); require(e is not None, 'NO_RESERVATION')
        b = e['body']; cap = units(b['amount'])
        frozen = any(x['body']['reservation'] == seq and self.binding_state(k) in
                     ('FROZEN', 'PENDING_RELEASE') for k, x in self.binds.items())
        closed = seq in self.closed or b['grant'] in self.fences or b['grant'] in self.revoked
        if not frozen and now is not None and now >= b['expiry_ms']: closed = True
        actual = pending = 0
        for a, entry in self.attempts.items():
            if entry['body']['reservation'] == seq:
                if a in self.settlements: actual += units(self.settlements[a]['body']['actual'])
                else: pending += units(entry['body']['maximum'])
        committed = actual + pending
        return dict(record=e, amount=cap, actual=actual, pending=pending, committed=committed,
                    frozen=frozen, closed=closed, usage=committed if closed else max(cap, committed),
                    allowance=max(cap-committed, 0))

    def totals(self, grant, now=None, lineage=None, discovery=False):
        rows = []
        for seq, r in self.reservations.items():
            b = r['body']
            if lineage is not None:
                if b['lineage'] != lineage: continue
            elif b['grant'] != grant: continue
            if discovery and b['purpose']['kind'] != 'Discovery': continue
            rows.append(self.reservation(seq, now))
        return sum(r['committed'] for r in rows), sum(r['usage'] for r in rows)

    def scope(self, grant, actor, purpose):
        kind, ident = purpose.get('kind'), purpose.get('id')
        if grant['class'] == 'Checker':
            require(kind == 'Check' and ident in self.proposals, 'PURPOSE_OUT_OF_SCOPE')
            return
        require(grant['class'] == 'Research', 'UNAUTHORIZED')
        scope = grant['scope_by_grantee'].get(actor, {})
        if kind == 'Theme': require(ident in scope.get('themes', []) and ident in self.themes, 'PURPOSE_OUT_OF_SCOPE')
        elif kind == 'SearchFamily': require(ident in scope.get('empirical_search_families', []), 'PURPOSE_OUT_OF_SCOPE')
        elif kind == 'Discovery': require(ident == grant['discovery_scope']['SearchFamily'], 'PURPOSE_OUT_OF_SCOPE')
        elif kind == 'Transition':
            p = self.proposals.get(ident); require(p is not None, 'NO_PROPOSAL')
            require(p['actor'] == actor and p['body']['grant'] == grant['AuthorizationId'], 'PURPOSE_OUT_OF_SCOPE')
            self.proposal_scope(grant, actor, p['body'])
        elif kind == 'Subject':
            applied = [a for a in self.applies.values() if a['body'].get('bind') and
                       self.proposals[a['transition_id']]['body']['subject'] == ident and
                       self.proposals[a['transition_id']]['actor']==actor and
                       self.proposals[a['transition_id']]['body']['grant']==grant['AuthorizationId']]
            require(bool(applied), 'PURPOSE_OUT_OF_SCOPE')
        else: raise Refusal('PURPOSE_OUT_OF_SCOPE')

    def proposal_scope(self, grant, actor, p):
        cls = p['class']; c = p['content']
        right={'HYPOTHESIS':'Hypothesis registration','AGENT_DESIGN':'Agent Design successor registration without grant request','THEME':'Theme registration'}.get(cls)
        require(right in grant.get('may_propose',[]),'UNAUTHORIZED')
        if cls == 'HYPOTHESIS':
            scope = grant.get('scope_by_grantee', {}).get(actor, {})
            themes = [v for v in c.get('motivated_by', []) if isinstance(v, str)]
            require(any(t in self.themes and t in scope.get('themes', []) for t in themes)
                    or c.get('SearchFamily') in scope.get('empirical_search_families', []), 'SCOPE_VIOLATION')
        elif cls == 'AGENT_DESIGN':
            require(c.get('predecessor') == actor and c.get('AgentDesignLineageId') == self.lineage(actor), 'SCOPE_VIOLATION')
        elif cls == 'THEME':
            require(bool(grant.get('discovery_scope')), 'SCOPE_VIOLATION')
        else: raise Refusal('UNAUTHORIZED')

    def export(self):
        return {'E': self.E, 'N': self.n, 'F': 'N/A — no Paper Book',
                'evidence': deepcopy(self.evidence), 'transitions': deepcopy(self.transitions)}
