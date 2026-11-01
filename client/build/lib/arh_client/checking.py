"""Checking toolkit for an evaluator registered as a Checker design.

evaluate() computes the common criteria and the class criteria from a
committed closure and the bundle profile. The one experiment-specific
criterion, HYPOTHESIS recomputation, is supplied by the team as a function.
A Checker that uses this module remains a separately registered design
under its own grant: the core enforces that separation; this module only
helps compute findings. Nothing here imports the core.
"""
from __future__ import annotations
from dataclasses import dataclass
from .protocol import digest, units, instant, HarnessError, time_text, require
from .results import Outcome, Ref
from .research import invocation, event_ref

Refusal = HarnessError

COMMON = ('authority', 'current_base', 'independence', 'funding', 'closure', 'registration_difference')
CLASS_CRITERIA = {
    'AUTHORIZATION': ('grant_content', 'prior_fence', 'source_declarations', 'tool_permissions'),
    'LIMITS': ('complete_limits', 'composition'),
    'AGENT_DESIGN': ('design_content', 'method_commitment', 'provenance', 'no_inherited_authority'),
    'THEME': ('motivation', 'typed_claims', 'selection'),
    'HYPOTHESIS': ('testability', 'resolution', 'sources', 'disjoint', 'selection', 'methods', 'recomputation', 'restatement'),
    'SUSPEND_POLICY': ('policy', 'scope', 'no_other_mutation'),
}
SELECTION_FIELDS = ('uncertainty', 'decision_it_could_change', 'experiment', 'value_estimate', 'value_basis', 'cost_estimate_units', 'time_estimate_ms', 'horizon', 'stopping_rule', 'origin')


def evaluate(snapshot, transition_id, actor, checker_grant, attempt, profile, recompute=None):
    """Criterion findings for one proposal. recompute(context) -> bool verifies the research arithmetic a HYPOTHESIS rests on."""
    events = snapshot['transitions']; evidence = snapshot['evidence']
    proposals = {}; designs = {}; grants = {}; active = set(); themes = {}; registered = []
    for event in events:
        b = event['body']
        if event['kind'] == 'PROPOSED': proposals[event['transition_id']] = event
        if event['kind'] != 'APPLIED' or b['n'] > snapshot['N']: continue
        if 'genesis' in b:
            g = b['genesis']; designs[g['design']['AgentDesignVersionId']] = g['design']
            grants[g['grant']['AuthorizationId']] = g['grant']; active.add(g['grant']['AuthorizationId'])
        else:
            p = proposals[event['transition_id']]['body']; c = p['content']; typ = p['class']
            if typ == 'AUTHORIZATION':
                active.discard(c['predecessor']); grants[c['grant']['AuthorizationId']] = c['grant']
                if c['action'] != 'REVOKE': active.add(c['grant']['AuthorizationId'])
            elif typ == 'AGENT_DESIGN': designs[c['AgentDesignVersionId']] = c
            elif typ == 'THEME': themes[c['ThemeId']] = c
            if typ in ('AGENT_DESIGN', 'THEME', 'HYPOTHESIS'): registered.append((typ, c))
    if transition_id not in proposals: raise Refusal('NO_PROPOSAL')
    pe = proposals[transition_id]; p = pe['body']; c = p['content']; typ = p['class']; now = snapshot['time_ms']
    if typ not in CLASS_CRITERIA: raise Refusal('CAPABILITY_UNSUPPORTED')
    proposer = pe['actor']; cg = grants.get(checker_grant, {}); pg = grants.get(p.get('grant'), {})
    ev = {e['seq']: e for e in evidence}; fenced = {e['body']['grant'] for e in evidence if e['kind'] == 'FENCE'}
    def ref(e, ledger): return {'ledger': ledger, 'sequence': e['seq'], 'sha256': e['sha256']}
    refs = [ref(pe, 'T')] + [ref(e, 'T') for e in events if e['kind'] == 'APPLIED']
    refs += [ref(e, 'E') for e in evidence if e['kind'] in ('RESERVATION', 'ATTEMPT', 'FENCE', 'OBSERVATION', 'RESEARCH_RECORD')]
    checks = {}
    def record(name, value, reason): checks[name] = {'status': 'MET' if value else 'NOT MET', 'reason': reason, 'refs': refs}
    def active_grant(g, who):
        try: return g['AuthorizationId'] in active and who in g['grantee'] and now < instant(g['expiry'])
        except (KeyError, TypeError, ValueError): return False
    direct = proposer == 'Principal' and p.get('grant') is None and p.get('budget') == '0.00' and p.get('funding_ref') is None
    record('authority', direct or active_grant(pg, proposer), 'Direct Principal control or active exact proposer grant at closure')
    record('current_base', snapshot['N'] == max((x['body']['n'] for x in events if x['kind'] == 'APPLIED'), default=None), 'Checked base is the authoritative head')
    own = designs.get(actor, {}).get('AgentDesignLineageId'); other = designs.get(proposer, {}).get('AgentDesignLineageId')
    independent = active_grant(cg, actor) and cg.get('class') == 'Checker' and actor != proposer and (other is None or other != own)
    independent &= not any(g.get('class') == 'Research' and k in active and actor in g['grantee'] for k, g in grants.items())
    if typ == 'AGENT_DESIGN': independent &= c.get('AgentDesignLineageId') != own
    if typ == 'AUTHORIZATION': independent &= actor not in (c.get('grant') or {}).get('grantee', []) and c.get('predecessor') != checker_grant
    prov = designs.get(actor, {}).get('provenance', {})
    # The synthetic-only exception (A1): a Checker that invokes no provider. A grant claiming provider diversity is outside this toolkit.
    independent &= all(prov.get(k) is None for k in ('provider', 'model', 'model_version', 'training_cutoff'))
    record('independence', independent, 'Separate eligible CHECKER lineage/grant; protected CV1; A1 no-model provenance; own-subject restrictions')
    covered = direct
    if not direct:
        r = ev.get(p.get('funding_ref'), {}); rb = r.get('body', {})
        try:
            covered = r.get('kind') == 'RESERVATION' and rb['actor'] == proposer and rb['grant'] == p['grant'] and rb['purpose'] == {'kind': 'Transition', 'id': transition_id}
            covered &= units(rb['amount']) >= units(p['budget']) and rb['expiry_ms'] > now and rb['grant'] not in fenced
            covered &= not any(e['kind'] == 'CLOSED' and e['body']['reservation'] == r['seq'] for e in evidence)
        except (KeyError, TypeError, ValueError): covered = False
    record('funding', covered, 'N/A for Principal; otherwise literal named open/unfenced reservation, amount and purpose; Checker cost separate')
    closure_ok = True
    for e in evidence: closure_ok &= e['seq'] <= snapshot['E'] and digest(e['body']) == e['sha256']
    record('closure', closure_ok and snapshot['F'] == 'N/A — no Paper Book', 'Exact committed closure; authored knowing the period; synthetic history earns no forward standing')
    different = True
    if typ == 'AGENT_DESIGN':
        different = c.get('AgentDesignVersionId') not in designs
        for old in designs.values():
            if (c.get('instructions'), c.get('research_question'), c.get('tool_specs')) == (old.get('instructions'), old.get('research_question'), old.get('tool_specs')): different = False
    if typ == 'THEME': different = not any(t == typ and old.get('statement') == c.get('statement') for t, old in registered)
    record('registration_difference', different, 'Concrete instruction/question/tool difference; IDs alone do not supply a difference')
    def selection(x):
        q = x.get('selection_basis') or {}; return all(q.get(k) is not None for k in SELECTION_FIELDS)
    template = profile['artifacts'].get('hypothesis_template', {}).get('content', {})
    try:
        if typ == 'AUTHORIZATION':
            g = c.get('grant') or {}; kind = g.get('class')
            complete = all(g.get(k) is not None for k in ('AuthorizationId', 'grantor', 'grantee', 'class', 'may_propose', 'may_check', 'may_commit_evidence', 'expiry', 'constitutional_budget', 'tools'))
            complete &= g.get('grantor') == 'Principal' and g.get('constitutional_budget') == {'delta_O': 0, 'delta_S': 0, 'delta_A': 0}
            complete &= not g.get('capital_permission', True) and not g.get('provider_calls_permitted', True) and not g.get('uncapped_calls_permitted', True)
            complete &= all(x in designs if kind != 'Observation' else x == 'Observation function' for x in g.get('grantee', []))
            if kind in ('Research', 'Checker'):
                complete &= units(g['research_budget_units']) >= 0 and units(g['per_lineage_cap_units']) >= 0 and g['default_reservation_duration_ms'] == 604800000
                if kind == 'Research': complete &= type(g.get('binding_interval_ms')) is int and g['binding_interval_ms'] > 0
                else: complete &= g.get('binding_interval_ms') is None and bool(g.get('forbidden_subjects')) and bool(g.get('provider_diversity'))
            elif kind != 'Observation': complete = False
            complete &= bool(g.get('grantee')) and instant(g['expiry']) > now
            if kind == 'Observation': complete &= g['may_propose'] == [] and g['may_check'] == [] and g['tools'] == []
            if kind == 'Checker':
                complete &= all(designs[x]['method_class'] == 'CHECKER' for x in g['grantee'])
                complete &= all('Research' not in x and 'grant' not in x.lower() for x in g['may_propose'])
                complete &= 'no provider diversity claimed' in g['provider_diversity'].lower()
                complete &= all(any(s['kind'] == 'check' and t['id'] in s['tools'] for s in profile['experiment']['steps']) for t in g['tools'])
            if kind == 'Research':
                complete &= all(designs[x]['method_class'] == 'RESEARCH' for x in g['grantee']) and g['may_check'] == []
                complete &= units(g['per_lineage_cap_units']) <= units(g['research_budget_units'])
                complete &= units(g['discovery_scope']['fixed_subgrant_units']) <= units(g['research_budget_units'])
                complete &= set(g['scope_by_grantee']) == set(g['grantee'])
                complete &= not any(any(s['kind'] == 'check' and t['id'] in s['tools'] for s in profile['experiment']['steps']) for t in g['tools'])
            record('grant_content', complete, 'All grant fields, registered grantees, synthetic scope and applicable funding fields evaluated')
            predecessor = c.get('predecessor')
            record('prior_fence', not predecessor or (predecessor in active and (grants[predecessor]['class'] == 'Observation' or predecessor in fenced)), 'Exact predecessor and prior Principal fence for Research/Checker supersession/revocation')
            source_ok = True
            if kind == 'Observation':
                source_ok = bool(g.get('source_declarations')) and 'observation_plan' in g
                for src in g.get('source_declarations', []):
                    sc = src['content']; source_ok &= digest(sc) == src['SourceRevision'] and all(sc.get(k) is not None for k in ('SourceId', 'provider', 'dataset', 'field', 'unit', 'print_rule', 'claimed_time_field', 'resolution_grace_ms', 'endpoint', 'access_method', 'parsing', 'extraction_rule'))
                    source_ok &= type(sc.get('resolution_grace_ms')) is int and sc['resolution_grace_ms'] > 0 and type(sc.get('synthetic')) is bool
                    if sc.get('synthetic'): source_ok &= bool(sc.get('enumeration_contract'))
            record('source_declarations', source_ok, 'Source meanings, revisions, grace, extraction and feed completeness; synthetic sources declare enumeration')
            known = profile['artifacts']['tools']; tool_ok = True
            for t in g.get('tools', []): tool_ok &= t.get('id') in known and t.get('tier') == 1 and t.get('spec_sha256') == known.get(t.get('id'), {}).get('content_sha256')
            record('tool_permissions', tool_ok, 'Own declared capped synthetic tools only, no foreign-grant tool consumption')
        elif typ == 'LIMITS':
            values = [x for k, x in c.items() if k.endswith('_units')]
            exact_limits = set(c) == set(profile['setup']['initial_limits'])
            record('complete_limits', exact_limits and bool(values) and all(units(x) == 0 for x in values) and c.get('strategy_versions') == [], 'Explicit zero research-only capital/risk limits')
            record('composition', not any(e['kind'] == 'APPLIED' and proposals.get(e['transition_id'], {}).get('body', {}).get('class') in ('STRATEGY', 'ALLOCATION') for e in events), 'Replayed empty allocation set: every usage zero, no silent breach')
        elif typ == 'AGENT_DESIGN':
            record('design_content', all(c.get(k) is not None for k in ('AgentDesignVersionId', 'AgentDesignLineageId', 'method_class', 'instructions', 'tool_specs', 'evaluation_inputs', 'proposable_outputs')) and c['method_class'] in ('RESEARCH', 'CHECKER'), 'Immutable method content and declared lineage/output/tool contract')
            method = c.get('initial_method') or {}; known = profile['artifacts']['methods'].get(method.get('id'), {})
            record('method_commitment', method.get('sha256') == known.get('content_sha256') and bool(known), 'Versioned contribution method hash verified')
            pv = c.get('provenance') or {}
            record('provenance', pv.get('execution_kind') == 'deterministic synthetic program' and c.get('executable_closure_sha256') == digest({'code': profile['inventory']['code_closure'], 'configuration': {k: v for k, v in c.items() if k != 'executable_closure_sha256'}}) and bool(c.get('executable_closure_sha256')) and all(pv.get(k) is None for k in ('provider', 'model', 'model_version', 'training_cutoff')), 'Actual frozen executable closure, truthful no-model provenance')
            record('no_inherited_authority', not c.get('authorization_request') and (not c.get('predecessor') or c['predecessor'] in designs), 'Registration carries no grant; predecessor references remain visible')
        elif typ == 'THEME':
            closure = c.get('motivation_closure'); valid = isinstance(closure, dict) and bool(closure.get('refs'))
            if valid: valid = closure.get('N', snapshot['N']) <= snapshot['N'] and all(r['ledger'] == 'E' and r['sequence'] in ev and ev[r['sequence']]['sha256'] == r['sha256'] for r in closure['refs'])
            record('motivation', valid, 'Formation closure exists before Theme proposal and is within direct Principal scope')
            record('typed_claims', bool(c.get('typed_claims')) and all(x.get('kind') in ('QUESTION', 'ASSUMPTION', 'REPORTED', 'INTERPRETATION') for x in c.get('typed_claims', [])), 'Typed claims disclose synthetic assumptions and questions')
            record('selection', selection(c), 'Every selection-basis field present, including time and origin')
        elif typ == 'SUSPEND_POLICY':
            record('policy', c.get('policy') == 'P-1' and c.get('action') == 'SUSPEND', 'Existing CV1 suspension control, no new policy')
            record('scope', c.get('scope') in grants and proposer == 'Principal', 'Exact named grant and direct Principal authority')
            record('no_other_mutation', set(c) == {'policy', 'scope', 'action', 'reason'}, 'Suspension content contains no unrelated mutations')
        elif typ == 'HYPOTHESIS':
            if c.get('template_id') != template.get('template_id'): raise Refusal('CAPABILITY_UNSUPPORTED')
            record('testability', all(c.get(k) is not None for k in ('observable', 'statement', 'falsifier', 'horizon', 'stopping_rule')) and c.get('tolerance') == '0' and all(c.get(k) == template.get(k) for k in ('observable', 'statement', 'falsifier', 'horizon', 'stopping_rule')), 'Fixed binary observable, falsifier, horizon and zero tolerance')
            rule = c.get('resolution_rule'); members = c.get('resolution_set') or []
            resolution = bool(rule) and rule == template['resolution_rule'] and digest(rule) == c.get('resolution_rule_sha256') and len(members) == 1 and members[0].get('SourceId') == template.get('resolution_source') == c.get('resolution_source') and members[0].get('period') == c.get('resolution_period') and members[0].get('print') == c.get('print') == template.get('print')
            record('resolution', resolution, 'Exact deterministic rule hash, declared period/print/member; no later replacement')
            sources = [s for k, g in grants.items() if k in active and g['class'] == 'Observation' and now < instant(g['expiry']) for s in g['source_declarations']]
            src = next((s['content'] for s in sources if s['content']['SourceId'] == c.get('resolution_source')), None)
            record('sources', src is not None and bool(src.get('extraction_rule')) and bool(src.get('resolution_grace_ms')) and src.get('synthetic') is True, 'Source active at base; deterministic extraction, declared grace, synthetic classification')
            mc = c.get('motivation_closure'); form = []
            if isinstance(mc, dict):
                form = [ev.get(r['sequence']) for r in mc.get('refs', []) if r.get('ledger') == 'E']
                if any(r.get('ledger') != 'E' or r['sequence'] not in ev or ev[r['sequence']]['sha256'] != r['sha256'] for r in mc.get('refs', [])): form = []
            docs = [e for e in form if e and e['kind'] == 'OBSERVATION' and e['body']['form'] == 'DOCUMENT']
            period = c.get('resolution_period') or {}
            disjoint = bool(docs) and all(d['body']['document']['period_end'] <= period.get('start', '') for d in docs) and instant(period['end']) > now
            record('disjoint', disjoint, 'Formation items precede a distinct future member with declared structural availability bound')
            record('selection', selection(c), 'Complete cost/time/value uncertainty and declared origin')
            method = c.get('initial_method') or {}; expected = profile['artifacts']['methods'].get(method.get('id'), {})
            record('methods', bool(expected) and method.get('sha256') == expected.get('content_sha256'), 'Scoring, effective observations and predictive check fixed by exact method artifact')
            rr = [e for e in form if e and e['kind'] == 'RESEARCH_RECORD']
            recomputed = False
            if recompute is not None and docs and rr:
                try: recomputed = bool(recompute({'documents': docs, 'records': rr, 'content': c, 'proposer': proposer, 'profile': profile, 'evidence': ev, 'now': now}))
                except (Refusal, KeyError, TypeError, ValueError, IndexError): recomputed = False
            record('recomputation', recomputed, 'Independent recomputation of the committed research result from committed inputs; verifies arithmetic and join, not provider labels' if recompute else 'No recomputation validator supplied: missing capability is never PASS')
            keys = ('observable', 'resolution_source', 'print', 'tolerance', 'resolution_rule_sha256', 'initial_method', 'falsifier')
            record('restatement', not any(t == 'HYPOTHESIS' and all(old.get(k) == c.get(k) for k in keys) for t, old in registered), 'Compared registered scientific tuple; a new date/ID alone is not a difference')
    except Refusal as exc:
        if exc.code == 'CAPABILITY_UNSUPPORTED': raise
        for name in CLASS_CRITERIA[typ]:
            if name not in checks: record(name, False, 'Invalid declared content: ' + exc.code)
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        for name in CLASS_CRITERIA[typ]:
            if name not in checks: record(name, False, 'Incomplete/invalid declared content: ' + type(exc).__name__)
    for name in COMMON + CLASS_CRITERIA[typ]:
        if name not in checks: record(name, False, 'Missing criterion input')
    return {'transition_id': transition_id, 'base': snapshot['N'], 'grant': checker_grant, 'attempt': attempt,
            'closure': {k: snapshot[k] for k in ('E', 'N', 'F', 'time_ms')}, 'criteria': checks,
            'result': 'PASS' if all(x['status'] == 'MET' for x in checks.values()) else 'FAIL',
            'es': 'ES-1.0', 'constitution': 1, 'provenance': designs.get(actor, {}).get('provenance', {}),
            'context': {'class': typ, 'subject': p['subject'], 'proposal': {'ledger': 'T', 'sequence': pe['seq'], 'sha256': pe['sha256']},
                        'proposer': {'identity': proposer, 'authority': 'Principal' if proposer == 'Principal' else p['grant'], 'provenance': designs.get(proposer, {}).get('provenance')},
                        'checker': {'identity': actor, 'design': actor, 'grant': checker_grant, 'provenance': designs.get(actor, {}).get('provenance')},
                        'funding': {'proposer': 'N/A' if proposer == 'Principal' else p['funding_ref'], 'checker_attempt': attempt, 'separate': True},
                        'classification': 'Synthetic Historical Reconstruction; authored knowing the period', 'provider_exception': 'A1 synthetic-only; no provider provenance claimed'}}


def checker_context(connection):
    """This actor's Checker grant, Check tool and check step, from the ledger and the profile."""
    actor = connection.actor; profile = connection.profile(); s = connection.state()
    design = next(d['content'] for d in profile['artifacts']['designs'] if d['content']['AgentDesignVersionId'] == actor)
    require(design['method_class'] == 'CHECKER', 'NOT_CHECKER', actor)
    grant = next((k for k in s['active'] if s['grants'][k]['class'] == 'Checker' and actor in s['grants'][k]['grantee']), None)
    require(grant is not None, 'AUTHORIZATION_INACTIVE', 'no active Checker grant names ' + actor)
    steps = [st for st in profile['experiment']['steps'] if st['kind'] == 'check' and any(t in design['tool_specs'] for t in st['tools'])]
    require(len(steps) == 1, 'CAPABILITY_UNSUPPORTED', 'one check step expected')
    tool = next(t for t in steps[0]['tools'] if t in design['tool_specs'])
    return {'grant': grant, 'tool': tool, 'step': steps[0]['name'], 'maximum': steps[0]['maximum']}


@dataclass
class CheckResult:
    """One completed Check: result is 'PASS', 'FAIL' or None when no judgment could be computed."""
    transition_id: str
    result: str | None
    criteria: dict | None
    check: Outcome | None
    attempt: Ref
    settlement: Outcome
    negative_record: Outcome | None = None
    @property
    def check_sequence(self) -> int | None: return self.check.sequence if self.check and self.check.ok else None


def run_check(connection, transition_id, evaluate_fn, hook=lambda point: None) -> CheckResult:
    """Fund, attempt, claim, compute, register, commit (or preserve a negative record), settle and close one Check."""
    ctx = checker_context(connection); grant, tool, maximum = ctx['grant'], ctx['tool'], ctx['maximum']; profile = connection.profile()
    snapshot = connection.closure(); p = next(x for x in snapshot['transitions'] if x['kind'] == 'PROPOSED' and x['transition_id'] == transition_id)
    r = connection.call_or_raise('reserve', {'grant': grant, 'amount': maximum, 'purpose': {'kind': 'Check', 'id': transition_id}}).ref
    data = invocation(profile, tool, ctx['step'], [event_ref(p, 'T')], {'transition_id': transition_id})
    a = connection.call_or_raise('attempt', {'reservation': r.sequence, 'step': ctx['step'], 'input': data, 'dispatch_index': 0, 'maximum': maximum, 'tier': 1}).ref
    permission = connection.query('tool-run', {'attempt': a.sequence})
    require(permission.get('status') == 'PERMISSION_CONSUMED', 'CHECK_DISPATCH_UNCERTAIN')
    error = None; candidate = None
    try:
        snapshot = connection.closure(); hook('checker_during_computation')
        candidate = evaluate_fn(snapshot, transition_id, connection.actor, grant, a.sequence, profile)
    except (HarnessError, KeyError, ValueError, TypeError) as exc: error = str(exc)
    receipt = {'attempt': a.sequence, 'input_hash': digest(data), 'tool_id': tool, 'actual': maximum, 'synthetic': True, 'result': candidate, 'error': error}
    hook('checker_after_result')
    connection.query('tool-finish', {'attempt': a.sequence, 'receipt': receipt})
    check = negative_record = None
    if candidate: check = connection.call('check-commit', candidate)
    else:
        snapshot = connection.closure()
        negative = {'grant': grant, 'attempt': a.sequence, 'question': 'Verify ' + transition_id, 'result': {'failure': error}, 'failure': error,
                    'closure': {'E': snapshot['E'], 'N': snapshot['N'], 'refs': [event_ref(p, 'T')]},
                    'claims': [{'kind': 'ASSUMPTION', 'text': 'Computation interrupted or outside supported capability; no Check judgment'}],
                    'kind': 'plain', 'snapshot': {'identity': transition_id, 'sha256': p['sha256']}, 'source_cutoff': time_text(snapshot['time_ms']),
                    'parameters': data['parameters'], 'tool': {'id': tool, 'spec_sha256': data['tool_spec_hash'], 'executable_hash': data['executable_hash']},
                    'reproducibility': {'input_refs': data['input_refs'], 'invocation_hash': digest(data), 'result_hash': None}, 'synthetic': True}
        negative_record = connection.call('research-commit', negative)
    settlement = connection.call_or_raise('settle', {'attempt': a.sequence, 'actual': receipt['actual'], 'unit': 'simulated_research_units', 'provenance': {'kind': 'TOOL_RECEIPT', 'receipt': receipt}})
    connection.call('close', {'reservation': r.sequence})
    return CheckResult(transition_id, candidate['result'] if candidate else None, {k: v['status'] for k, v in candidate['criteria'].items()} if candidate else None, check, a, settlement, negative_record)


class Checker:
    """An evaluator process under a Checker identity. check() runs one independent Check."""
    def __init__(self, connection, evaluate_fn=None, recompute=None):
        self.c = connection
        self.evaluate_fn = evaluate_fn or (lambda snapshot, tr, actor, grant, attempt, profile: evaluate(snapshot, tr, actor, grant, attempt, profile, recompute=recompute))
    def check(self, transition_id: str) -> CheckResult:
        """Fund, compute and commit one Check of a proposed Transition under this Checker's own grant."""
        return run_check(self.c, transition_id, self.evaluate_fn)
