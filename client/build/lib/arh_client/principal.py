"""Principal and Observation-function helpers, and a generic startup derived from the setup."""
from __future__ import annotations
from copy import deepcopy
from datetime import datetime, timedelta
from .protocol import digest, instant, HarnessError, require
from .results import Outcome, Ref
from .research import event_ref

Refusal = HarnessError


class Principal:
    """The owner's decisions. Every method returns an Outcome."""
    def __init__(self, connection): require(connection.actor == 'Principal', 'UNAUTHORIZED'); self.c = connection
    def genesis(self, design: dict, grant: dict, key: str | None = None) -> Outcome:
        p = self.c.profile()
        return self.c.call_or_raise('genesis', {'constitution_sha256': p['setup']['constitution']['sha256'], 'design': design, 'grant': grant}, key)
    def propose_control(self, cls: str, subject: str, content: dict, transition_id: str, key: str | None = None) -> Outcome:
        """Propose a control Transition on direct Principal authority: AUTHORIZATION, LIMITS, AGENT_DESIGN, THEME or SUSPEND_POLICY."""
        payload = {'transition_id': transition_id, 'base': self.c.state()['N'], 'class': cls, 'subject': subject, 'content': content,
                   'grant': None, 'budget': '0.00', 'funding_ref': None, 'delta': {'O': 0, 'S': 0, 'A': 0}}
        return self.c.call('propose', payload, key)
    def decide(self, transition_id: str, check: int, decision: str = 'ADMITTED', reason: str = 'Principal decision', key: str | None = None) -> Outcome:
        """Decide a checked proposal: ADMITTED, REJECTED or STOPPED. Refusals: NO_CHECK, CHECK_NOT_PASS, STALE_CHECK."""
        return self.c.call('decide', {'transition_id': transition_id, 'check': check, 'decision': decision, 'reason': reason}, key)
    def policy_decide(self, transition_id: str, check: int, key: str | None = None) -> Outcome:
        """Let policy P-1 decide a routine Hypothesis or successor-design registration. Refusals: CHECK_NOT_PASS, P1_CLASS, POLICY_SUSPENDED."""
        return self.c.call('policy-decide', {'transition_id': transition_id, 'check': check}, key)
    def apply(self, transition_id: str, decision: int, bind: int | None = None, key: str | None = None) -> Outcome:
        """Apply an admitted decision; for a researcher's proposal the core binds its funding first. Refusals: NOT_DECIDED, STALE_DECISION, BINDING_INVALIDATED, FENCED."""
        p = {'transition_id': transition_id, 'decision': decision}
        if bind is not None: p['bind'] = bind
        return self.c.call('apply', p, key)
    def fence(self, grant: str, reason: str, key: str | None = None) -> Outcome:
        """Stop new spending under a grant. Existing liabilities remain. Refusals: ALREADY_FENCED, NO_AUTHORIZATION."""
        return self.c.call('fence', {'grant': grant, 'reason': reason}, key)
    def recover(self, transition_id: str | None = None, key: str | None = None) -> Outcome | dict:
        """Continue an interrupted admission from the ledgers, or list obligations when no transition is named."""
        p = {'continue': True, 'transition_id': transition_id} if transition_id else {}
        return self.c.call('recover', p, key) if transition_id else self.c.query('recover', p)
    def dispatch_status(self) -> dict: return self.c.query('dispatch-status')


def row_ratio(spec, document):
    """The client's copy of the core's row-ratio extraction, so an observer can state the value the core will verify."""
    def holds(row, conditions):
        for c in conditions:
            v = row[c['field']]
            if 'equals' in c:
                if v != c['equals']: return False
            else:
                name = next(k for k in ('at_least', 'at_most', 'greater_than', 'less_than') if k in c); b = c[name]
                if type(v) is not int: raise Refusal('NOT_EXTRACTABLE')
                if name == 'at_least' and not v >= b: return False
                if name == 'at_most' and not v <= b: return False
                if name == 'greater_than' and not v > b: return False
                if name == 'less_than' and not v < b: return False
        return True
    try:
        seen = set(); n = k = 0
        for row in document['rows']:
            for name, kind in spec['row_fields'].items():
                v = row[name]
                if kind == 'str': require(isinstance(v, str), 'NOT_EXTRACTABLE')
                else: require(type(v) is {'int': int, 'bool': bool}[kind], 'NOT_EXTRACTABLE')
            require(row[spec['unique']] not in seen, 'NOT_EXTRACTABLE'); seen.add(row[spec['unique']])
            if holds(row, spec['denominator']):
                n += 1
                if holds(row, spec['numerator']): k += 1
    except (Refusal, KeyError, TypeError): return False, None
    return n > 0, ({'numerator': k, 'denominator': n} if n > 0 else None)


class Observer:
    """The Observation function: the only identity that may commit source documents."""
    def __init__(self, connection): require(connection.actor == 'Observation function', 'UNAUTHORIZED'); self.c = connection
    def grant_for(self, source):
        s = self.c.state()
        for ident in s['active']:
            g = s['grants'][ident]
            if g['class'] == 'Observation' and any(d['content']['SourceId'] == source for d in g['source_declarations']):
                return ident, next(d for d in g['source_declarations'] if d['content']['SourceId'] == source)
        raise Refusal('SOURCE_NOT_ACTIVE', source)
    def observe(self, source, content, date, form='DOCUMENT', extract=True):
        """Commit the COMPLETE listing, the DOCUMENT and its extraction for one source item on one date, as the core's rules require."""
        grant, decl = self.grant_for(source); rule = self.c.experiment()['sources'][source]
        doc = deepcopy(content); start = datetime.strptime(date, '%Y-%m-%d'); end = start + timedelta(milliseconds=rule['period_ms'])
        doc.update(item_id=rule['item_id']['prefix'] + date, period_start=start.strftime('%Y-%m-%dT%H:%M:%S.000Z'), period_end=end.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                   claimed_publication_time=end.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        clock = self.c.clock()
        payload = {'grant': grant, 'source': source, 'revision': decl['SourceRevision'], 'form': form, 'period': {'start': doc['period_start'], 'end': doc['period_end']},
                   'item_id': doc['item_id'], 'document': doc if form == 'DOCUMENT' else None, 'slot': clock['t']}
        if form != 'DOCUMENT':
            if form in ('ABSENT', 'COMPLETE'): payload.update(form='COMPLETE', items=[doc['item_id']] if clock['t'] >= instant(doc['period_end']) else [], window=payload['period'])
            else: payload['error'] = 'Explicit synthetic retrieval fault'
            return self.c.call_or_raise('observation-commit', payload)
        self.c.call_or_raise('observation-commit', dict(payload, form='COMPLETE', document=None, items=[doc['item_id']], window=payload['period']))
        result = self.c.call_or_raise('observation-commit', payload)
        if extract:
            extractable, value = row_ratio(rule['extraction'], doc)
            extraction = dict(payload, form='VALUE' if extractable else 'NOT_EXTRACTABLE', document=None, document_ref=result.ref.as_dict())
            if extractable: extraction['value'] = value
            else: extraction['error'] = 'No rows pass the declared extraction'
            self.c.call_or_raise('observation-commit', extraction)
        result.raw['document'] = doc; return result


def startup(principal, observer, checker, tick=None, formation_date=None, ordinary_designs_first=True):
    """Genesis and the control transitions a setup declares, in the order the admitted synthetic startup used.

    checker(transition_id) runs an independent Check under a Checker identity and returns the PASS Check's sequence.
    tick(ms) advances the synthetic clock before the formation observation. Returns the applied head and formation refs.
    """
    c = principal.c; p = c.profile(); setup = p['setup']; artifacts = p['artifacts']; exp = p['experiment']
    designs = {d['content']['AgentDesignVersionId']: d['content'] for d in artifacts['designs']}
    grants = {g['content']['AuthorizationId']: g['content'] for g in setup['grants']}
    genesis = exp['genesis']; principal.genesis(designs[genesis['design']], grants[genesis['grant']])
    ordinal = 0; log = []
    def control(cls, subject, content):
        nonlocal ordinal
        ordinal += 1; tr = f'TR-{ordinal}'
        principal.propose_control(cls, subject, content, tr).raise_for_refusal()
        check = checker(tr)
        d = principal.decide(tr, check, 'ADMITTED', 'Startup control').raise_for_refusal()
        principal.apply(tr, d.sequence).raise_for_refusal()
        log.append({'transition_id': tr, 'class': cls, 'subject': subject}); return tr
    observation_grants = [g for g in setup['grants'] if g['content']['class'] == 'Observation']
    for g in observation_grants: control('AUTHORIZATION', g['content']['AuthorizationId'], {'action': 'GRANT', 'predecessor': None, 'grant': g['content']})
    if tick: tick(1000)
    formation = {}
    formation_content = artifacts['formation_cohort']['content']
    date = formation_date or formation_content['period_start'][:10]
    for source in exp['sources']:
        if source not in {d['content']['SourceId'] for g in observation_grants for d in g['content']['source_declarations']}: continue
        if source == artifacts['formation_cohort'].get('source', next(iter(exp['sources']))):
            formation[source] = event_ref(c.get(observer.observe(source, formation_content, date).ref))
    control('LIMITS', 'initial_limits', setup['initial_limits'])
    for d in artifacts['designs']:
        ident = d['content']['AgentDesignVersionId']
        if ident == genesis['design']: continue
        control('AGENT_DESIGN', ident, d['content'])
    for g in setup['grants']:
        ident = g['content']['AuthorizationId']
        if ident == genesis['grant'] or g['content']['class'] == 'Observation': continue
        control('AUTHORIZATION', ident, {'action': 'GRANT', 'predecessor': None, 'grant': g['content']})
    theme = deepcopy(setup['theme']['content']); first = next(iter(formation.values()))
    theme['motivation_closure'] = {'N': c.state()['N'], 'refs': [{k: v for k, v in first.items() if k != 'raw_sha256'}]}
    control('THEME', theme['ThemeId'], theme)
    return {'N': c.state()['N'], 'formation': formation, 'transitions': log}
