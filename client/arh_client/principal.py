"""Principal and Observation-function helpers, and a generic startup derived from the setup."""
from __future__ import annotations
from copy import deepcopy
from datetime import datetime, timedelta
from .protocol import digest, instant, HarnessError, require
from .results import Outcome, Ref
from .research import event_ref
import hashlib
import csv
import io
import json as _json
import time as _time
from pathlib import Path as _Path

MEDIA_TYPES = {'.txt': 'text/plain', '.md': 'text/markdown', '.csv': 'text/csv', '.json': 'application/json', '.tsv': 'text/tab-separated-values'}


def _rows_from(text, media_type):
    """Rows for tabular files; integers are kept exact, everything else stays text."""
    def cell(v):
        if isinstance(v, str) and re_int.fullmatch(v.strip()): return int(v.strip())
        return v
    import re as _re; re_int = _re.compile(r'-?(?:0|[1-9][0-9]*)')
    if media_type == 'application/json':
        value = _json.loads(text)
        return [dict((k, cell(v)) for k, v in r.items()) for r in value] if isinstance(value, list) and all(isinstance(r, dict) for r in value) else None
    dialect = csv.excel_tab if media_type == 'text/tab-separated-values' else csv.excel
    return [dict((k, cell(v)) for k, v in r.items()) for r in csv.DictReader(io.StringIO(text), dialect=dialect)]


def historical_document(raw: bytes, name: str, origin: str, received_at: str | None = None, note: str | None = None, media_type: str | None = None) -> dict:
    """A historical document body from file bytes: identity by content hash, declared provenance, text or rows."""
    media_type = media_type or MEDIA_TYPES.get(_Path(name).suffix.lower(), 'text/plain')
    text = raw.decode('utf-8')
    doc = {'class': 'historical', 'synthetic': False, 'file': {'name': name, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw), 'media_type': media_type},
           'provenance': {'origin': origin, 'received_at': received_at or _time.strftime('%Y-%m-%dT%H:%M:%S.000Z', _time.gmtime()), 'note': note or ''}}
    rows = _rows_from(text, media_type) if media_type in ('text/csv', 'text/tab-separated-values', 'application/json') else None
    if rows is not None: doc['rows'] = rows
    else: doc['text'] = text
    return doc

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
        many = rule['item_id'].get('per_period', 'one') == 'many'
        item_id = rule['item_id']['prefix'] + date + ('-' + doc['file']['sha256'][:16] if many else '')
        doc.update(item_id=item_id, period_start=start.strftime('%Y-%m-%dT%H:%M:%S.000Z'), period_end=end.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        doc.setdefault('claimed_publication_time', end.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        if rule['document'].get('class', 'synthetic') == 'synthetic': doc['claimed_publication_time'] = end.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        if rule['extraction'].get('validator') == 'none': extract = False
        clock = self.c.clock()
        payload = {'grant': grant, 'source': source, 'revision': decl['SourceRevision'], 'form': form, 'period': {'start': doc['period_start'], 'end': doc['period_end']},
                   'item_id': doc['item_id'], 'document': doc if form == 'DOCUMENT' else None, 'slot': clock['t']}
        if form != 'DOCUMENT':
            if form in ('ABSENT', 'COMPLETE'): payload.update(form='COMPLETE', items=[doc['item_id']] if clock['t'] >= instant(doc['period_end']) else [], window=payload['period'])
            else: payload['error'] = 'Explicit synthetic retrieval fault'
            return self.c.call_or_raise('observation-commit', payload)
        if not many: self.c.call_or_raise('observation-commit', dict(payload, form='COMPLETE', document=None, items=[doc['item_id']], window=payload['period']))
        result = self.c.call_or_raise('observation-commit', payload)
        if extract:
            extractable, value = row_ratio(rule['extraction'], doc)
            extraction = dict(payload, form='VALUE' if extractable else 'NOT_EXTRACTABLE', document=None, document_ref=result.ref.as_dict())
            if extractable: extraction['value'] = value
            else: extraction['error'] = 'No rows pass the declared extraction'
            self.c.call_or_raise('observation-commit', extraction)
        result.raw['document'] = doc; return result
    def import_file(self, source: str, path, date: str, origin: str, received_at: str | None = None, note: str | None = None, name: str | None = None):
        """Commit a local file as a historical document of a source. Text, markdown, CSV, TSV and JSON rows are supported."""
        raw = _Path(path).read_bytes(); return self.observe(source, historical_document(raw, name or _Path(path).name, origin, received_at, note), date)
    def import_bytes(self, source: str, raw: bytes, name: str, date: str, origin: str, received_at: str | None = None, note: str | None = None):
        return self.observe(source, historical_document(raw, name, origin, received_at, note), date)


def startup(principal, observer, checker, tick=None, formation_date=None, ordinary_designs_first=True, formation_content=None):
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
    formation_content = formation_content or artifacts['formation_cohort']['content']
    date = formation_date or formation_content.get('period_start', '2026-10-28T')[:10]
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
