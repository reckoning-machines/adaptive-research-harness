"""RV-03: declared Checker steps through public clients and real host processes.

The fixture has trusted same-user tokens, no OS-isolation claim. No ledger is
read or fabricated. The independent worker recomputes all control criteria.
"""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import uuid

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'client'))
from arh_client import Connection, HarnessError, HostControl, Observer, Principal
from arh_client import digest, event_ref, historical_document, invocation
from arh_client.project import Project


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def key():
    return str(uuid.uuid4())


def worker(request_file, output_file):
    request = read(request_file)
    c = Connection.from_file(request['connection'], request['actor'])
    if request['mode'] == 'prepare':
        # A separate process holding only the Checker connection view.
        from tests.integration.checker_step_tools import evaluate
        p = c.profile()
        step = next(s for s in p['experiment']['steps'] if s['name'] == request['step'])
        proposal = next(e for e in c.history('T') if e['kind'] == 'PROPOSED' and e['transition_id'] == request['transition'])
        amount = step['maximum']
        r = c.call_or_raise('reserve', {'grant': request['grant'], 'amount': amount, 'purpose': {'kind': 'Check', 'id': request['transition']}}, key())
        data = invocation(p, step['tools'][0], step['name'], [event_ref(proposal, 'T')], {'transition_id': request['transition']})
        a = c.call_or_raise('attempt', {'reservation': r.sequence, 'step': step['name'], 'input': data, 'dispatch_index': 0, 'maximum': amount, 'tier': 1}, key())
        assert c.query('tool-run', {'attempt': a.sequence})['status'] == 'PERMISSION_CONSUMED'
        body = evaluate(c.closure(), request.get('check_transition', request['transition']), c.actor, request['grant'], a.sequence, p)
        receipt = {'attempt': a.sequence, 'input_hash': digest(data), 'tool_id': step['tools'][0], 'actual': amount, 'synthetic': True, 'result': body, 'error': None}
        c.query('tool-finish', {'attempt': a.sequence, 'receipt': receipt})
        write(output_file, {'pid': os.getpid(), 'actor': c.actor, 'body': body, 'receipt': receipt, 'attempt': a.ref.as_dict(), 'reservation': r.ref.as_dict(), 'amount': amount})
    else:
        c.call_or_raise(request['op'], request['payload'], request['key'])
        # The core committed, but this caller dies before persisting an ack.
        os._exit(23)


class DeclaredCheckerSteps(unittest.TestCase):
    def setUp(self):
        self.run = Path(tempfile.mkdtemp(prefix='arh-rv03-test-', dir='/private/tmp' if sys.platform == 'darwin' else None))
        self.setup = self.run / 'setup'
        self.setup.mkdir()
        self.output = Path(os.environ.get('ARH_RV03_EVIDENCE', str(ROOT / 'artifacts/development/rv03-repair'))) / (self._testMethodName + '-' + key())
        self.trace = []
        self.boundaries = []
        self.host = None
        self.addCleanup(self.cleanup)
        project = {'experiment_id': 'RV03-CHECKER-STEPS', 'short': 'RV3', 'question': 'Verify declared Checker step enforcement, not an investment claim.',
                   'sources': [{'id': 'SRC-RV3', 'prefix': 'rv3-', 'class': 'synthetic'}],
                   'analyses': [{'id': 'CALC-RV3', 'kind': 'unused-calculation', 'module': 'tools.py', 'callable': 'calculate', 'execution': 'caller', 'provider_work': 'ends_with_caller', 'step': 'research',
                                 'parameters': {}, 'tariff': {'measure': 'documents', 'limit': 1, 'per_unit': '0.50'}, 'inputs': [{'kind': 'OBSERVATION', 'form': 'DOCUMENT', 'min': 1, 'max': 1}], 'description': 'Only step-kind refusal is tested.', 'cost': '0.50 maximum'}],
                   'researcher': {'program': 'tools.py', 'entrypoint': 'tools:researcher'},
                   'evaluator': {'module': 'tools.py', 'entrypoint': 'tools:evaluate', 'description': 'Independent public full-criteria evaluator.'},
                   'budget': '12.00', 'theme': 'Bounded Checker mechanics.', 'formation': {'rows': [{'value': 1}], 'class': 'synthetic', 'synthetic': True}}
        self.project = Project(self.setup, project)
        self.ids = self.project.ids
        self.project.write_setup()
        shutil.copyfile(Path(__file__).with_name('checker_step_tools.py'), self.setup / 'tools.py')
        artifacts = read(self.setup / 'designs_and_methods.json')
        setup = read(self.setup / 'setup.json')
        experiment = read(self.setup / 'experiment.json')
        quarter = self.ids['check_tool']
        half = quarter + '-HALF'
        artifacts['tools'][half] = deepcopy(artifacts['tools'][quarter])
        artifacts['tools'][half]['content']['cost'] = '0.50 units per full Check.'
        artifacts['tools'][half]['content_sha256'] = digest(artifacts['tools'][half]['content'])
        experiment['tools'][half] = dict(experiment['tools'][quarter], label='check-half')
        experiment['steps'].append({'name': 'check-half', 'kind': 'check', 'tools': [half], 'maximum': '0.50'})
        checker = next(x for x in artifacts['designs'] if x['content']['AgentDesignVersionId'] == self.ids['checker'])
        grant = next(x['content'] for x in setup['grants'] if x['content']['class'] == 'Checker')
        # CALC membership permits a real admitted non-check attempt to test the
        # Check-commit kind guard. It grants no Research role or authority.
        for tool in (half, 'CALC-RV3'):
            checker['content']['tool_specs'][tool] = artifacts['tools'][tool]['content_sha256']
            grant['tools'].append({'id': tool, 'tier': 1, 'spec_sha256': artifacts['tools'][tool]['content_sha256']})
        checker['content_sha256'] = digest(checker['content'])
        write(self.setup / 'setup.json', setup)
        write(self.setup / 'designs_and_methods.json', artifacts)
        write(self.setup / 'experiment.json', experiment)
        self.start()
        profile = self.p.profile()
        designs = {x['content']['AgentDesignVersionId']: x['content'] for x in profile['artifacts']['designs']}
        grants = {x['content']['AuthorizationId']: x['content'] for x in profile['setup']['grants']}
        Principal(self.p).genesis(designs[self.ids['checker']], grants[self.ids['grants']['checker']], key()).raise_for_refusal()
        tr = 'BOOT-OBSERVATION'
        obs = grants[self.ids['grants']['observation']]
        Principal(self.p).propose_control('AUTHORIZATION', obs['AuthorizationId'], {'action': 'GRANT', 'grant': obs, 'predecessor': None}, tr, key()).raise_for_refusal()
        prep = self.prepare(tr)
        commit = self.commit(prep)
        self.assertTrue(commit.ok, commit.raw)
        self.finish(prep)
        decision = Principal(self.p).decide(tr, commit.sequence, key=key()).raise_for_refusal()
        Principal(self.p).apply(tr, decision.sequence, key=key()).raise_for_refusal()
        document = historical_document(b'[{"value":1}]', 'seed.json', 'RV-03 deterministic synthetic fixture')
        document.update({'class': 'synthetic', 'synthetic': True})
        self.document = Observer(Connection.from_file(self.run / 'state/connection.json', 'Observation function')).observe('SRC-RV3', document, '2026-10-28').raise_for_refusal()

    def start(self):
        self.log = (self.run / 'host.log').open('ab')
        self.host = subprocess.Popen([sys.executable, '-m', 'adaptive_research_harness.local_host', '--setup', str(self.setup), '--run', str(self.run)], cwd=ROOT,
                                     env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), stdout=self.log, stderr=self.log)
        end = time.monotonic() + 30
        while True:
            try:
                self.p = Connection.from_file(self.run / 'state/connection.json', 'Principal')
                self.p.state()
                break
            except (OSError, HarnessError):
                if self.host.poll() is not None or time.monotonic() > end:
                    raise AssertionError((self.run / 'host.log').read_text()[-4000:])
                time.sleep(.03)
        raw = read(self.run / 'state/connection.json')
        view = {k: v for k, v in raw.items() if k != 'tokens'}
        view['tokens'] = {self.ids['checker']: raw['tokens'][self.ids['checker']]}
        self.checker_file = self.run / 'checker-private.json'
        write(self.checker_file, view)
        os.chmod(self.checker_file, 0o600)
        self.ck = Connection.from_file(self.checker_file, self.ids['checker'])

    def stop(self):
        old = HostControl.from_file(self.run / 'state/connection.json').status()
        HostControl.from_file(self.run / 'state/connection.json').stop()
        self.host.wait(timeout=15)
        self.log.close()
        self.host = None
        return old

    def restart(self):
        old = self.stop()
        self.start()
        new = HostControl.from_file(self.run / 'state/connection.json').status()
        self.boundaries.append({'old': old, 'new': new, 'old_host_waited': True})
        self.assertNotEqual(old['processes'][0]['pid'], new['processes'][0]['pid'])

    def propose(self, name):
        Principal(self.p).propose_control('LIMITS', 'initial_limits', self.p.profile()['setup']['initial_limits'], name, key()).raise_for_refusal()
        return name

    def prepare(self, tr, step='check-transition', check_transition=None):
        request = self.run / ('prepare-' + key() + '.json')
        output = request.with_suffix('.reply.json')
        write(request, {'mode': 'prepare', 'connection': str(self.checker_file), 'actor': self.ck.actor, 'grant': self.ids['grants']['checker'], 'transition': tr, 'step': step, 'check_transition': check_transition or tr})
        proc = subprocess.run([sys.executable, '-m', 'tests.integration.test_checker_steps', '--worker', str(request), str(output)], cwd=ROOT,
                              env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), capture_output=True, text=True, timeout=30)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        prep = read(output)
        self.trace.append({'independent_checker_worker': prep})
        return prep

    def commit(self, prep, actor=None, request_key=None):
        c = self.ck if actor is None else Connection.from_file(self.run / 'state/connection.json', actor)
        result = c.call('check-commit', prep['body'], request_key or key())
        self.trace.append({'command': 'check-commit', 'response': result.raw, 'actor': c.actor})
        return result

    def finish(self, prep):
        amount = prep['amount']
        self.ck.call_or_raise('settle', {'attempt': prep['attempt']['sequence'], 'actual': amount, 'unit': 'simulated_research_units', 'provenance': {'kind': 'TOOL_RECEIPT', 'receipt': prep['receipt']}}, key())
        self.ck.call_or_raise('close', {'reservation': prep['reservation']['sequence']}, key())

    def cleanup(self):
        try:
            self.output.mkdir(parents=True, exist_ok=True)
            write(self.output / 'closure.json', self.p.closure())
            write(self.output / 'budget.json', self.p.budget(self.ids['grants']['checker']))
            write(self.output / 'obligations.json', self.p.obligations())
            write(self.output / 'trace.json', self.trace)
            write(self.output / 'boundaries.json', self.boundaries)
            write(self.output / 'identity.json', {'run': str(self.run), 'test': self.id(), 'ARH_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                  'rules_sha256': hashlib.sha256((ROOT / 'adaptive_research_harness/rules.py').read_bytes()).hexdigest(), 'test_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'inventory': self.p.profile()['inventory'], 'synthetic': True, 'OS_isolation': False})
        finally:
            if self.host is not None:
                self.stop()
            self.checker_file.unlink(missing_ok=True)

    def test_declared_quarter_and_half_steps_complete(self):
        for name, step, amount in [('QUARTER', 'check-transition', '0.25'), ('HALF', 'check-half', '0.50')]:
            with self.subTest(step=step):
                prep = self.prepare(self.propose(name), step)
                self.assertEqual(prep['body']['result'], 'PASS', prep['body'])
                result = self.commit(prep)
                self.finish(prep)  # A refused Check still incurs the real charge.
                self.assertTrue(result.ok, result.raw)
                check = self.p.get(result.ref)
                self.assertEqual(check['kind'], 'CHECK')
                self.assertEqual(check['actor'], self.ids['checker'])
                self.assertEqual(prep['receipt']['actual'], amount)
        self.assertEqual(self.p.budget(self.ids['grants']['checker'])['committed'], '1.00')

    def test_undeclared_steps_and_mismatched_maxima_refuse(self):
        tr = self.propose('BAD-STEP')
        p = self.ck.profile()
        proposal = next(e for e in self.ck.history('T') if e.get('transition_id') == tr and e['kind'] == 'PROPOSED')
        for step, maximum, reason in [('undeclared', '0.50', 'INVALID_STEP'), ('check-half', '0.25', 'INVALID_ESTIMATE')]:
            r = self.ck.call_or_raise('reserve', {'grant': self.ids['grants']['checker'], 'amount': '0.50', 'purpose': {'kind': 'Check', 'id': tr}}, key())
            tool = self.ids['check_tool'] + '-HALF'
            inp = invocation(p, tool, step, [event_ref(proposal, 'T')], {'transition_id': tr})
            result = self.ck.call('attempt', {'reservation': r.sequence, 'step': step, 'input': inp, 'dispatch_index': 0, 'maximum': maximum, 'tier': 1}, key())
            self.assertEqual(result.reason, reason, result.raw)
            self.trace.append({'negative_attempt': result.raw})
            self.ck.call_or_raise('close', {'reservation': r.sequence}, key())

    def test_non_checker_step_cannot_be_committed_as_check(self):
        from tests.integration.checker_step_tools import evaluate
        tr = self.propose('NON-CHECK')
        r = self.ck.call_or_raise('reserve', {'grant': self.ids['grants']['checker'], 'amount': '0.50', 'purpose': {'kind': 'Check', 'id': tr}}, key())
        inp = invocation(self.ck.profile(), 'CALC-RV3', 'research', [event_ref(self.ck.get(self.document.ref))], {})
        a = self.ck.call_or_raise('attempt', {'reservation': r.sequence, 'step': 'research', 'input': inp, 'dispatch_index': 0, 'maximum': '0.50', 'tier': 1}, key())
        self.assertEqual(self.ck.query('tool-run', {'attempt': a.sequence})['status'], 'PERMISSION_CONSUMED')
        body = evaluate(self.ck.closure(), tr, self.ck.actor, self.ids['grants']['checker'], a.sequence, self.ck.profile())
        receipt = {'attempt': a.sequence, 'input_hash': digest(inp), 'tool_id': 'CALC-RV3', 'actual': '0.50', 'synthetic': True, 'result': body, 'error': None}
        self.ck.query('tool-finish', {'attempt': a.sequence, 'receipt': receipt})
        prep = {'body': body, 'receipt': receipt, 'attempt': a.ref.as_dict(), 'reservation': r.ref.as_dict(), 'amount': '0.50'}
        result = self.commit(prep)
        self.assertEqual(result.reason, 'UNFUNDED_CHECK', result.raw)
        self.finish(prep)

    def test_invalid_funding_and_transition_scope_refuse(self):
        a = self.propose('FUNDED-A')
        b = self.propose('OTHER-B')
        prep = self.prepare(a, 'check-half', check_transition=b)
        result = self.commit(prep)
        self.assertEqual(result.reason, 'UNFUNDED_CHECK', result.raw)
        self.finish(prep)
        result = self.ck.call('reserve', {'grant': self.ids['grants']['checker'], 'amount': '0.50', 'purpose': {'kind': 'Theme', 'id': 'NO-THEME'}}, key())
        self.assertEqual(result.reason, 'PURPOSE_OUT_OF_SCOPE', result.raw)
        r = self.ck.call_or_raise('reserve', {'grant': self.ids['grants']['checker'], 'amount': '0.25', 'purpose': {'kind': 'Check', 'id': a}}, key())
        proposal = next(e for e in self.ck.history('T') if e['kind'] == 'PROPOSED' and e['transition_id'] == a)
        inp = invocation(self.ck.profile(), self.ids['check_tool'] + '-HALF', 'check-half', [event_ref(proposal, 'T')], {'transition_id': a})
        result = self.ck.call('attempt', {'reservation': r.sequence, 'step': 'check-half', 'input': inp, 'dispatch_index': 0, 'maximum': '0.50', 'tier': 1}, key())
        self.assertEqual(result.reason, 'ALLOWANCE_EXCEEDED', result.raw)
        self.ck.call_or_raise('close', {'reservation': r.sequence}, key())

    def test_unauthorized_actors_and_receipt_reuse_refuse(self):
        prep = self.prepare(self.propose('ROLES'), 'check-half')
        for actor in ('Principal', self.ids['researcher'], 'Observation function'):
            result = self.commit(prep, actor=actor)
            self.assertEqual(result.reason, 'UNAUTHORIZED', result.raw)
        attempt = prep['attempt']['sequence']
        for mutated, reason in [(dict(prep['receipt'], actual='0.25'), 'INVALID_TOOL_RECEIPT'), (dict(prep['receipt'], error='changed'), 'RECEIPT_CONFLICT')]:
            with self.assertRaises(HarnessError) as exc:
                self.ck.query('tool-finish', {'attempt': attempt, 'receipt': mutated})
            self.assertEqual(exc.exception.code, reason)
        replay = self.ck.query('tool-run', {'attempt': attempt})
        self.assertEqual(replay['status'], 'RECEIPT')
        self.assertEqual(replay['receipt'], prep['receipt'])
        self.assertTrue(self.commit(prep).ok)
        self.finish(prep)

    def test_lost_check_and_settlement_responses_reopen_and_replay_once(self):
        tr = self.propose('LOST-REPLY')
        prep = self.prepare(tr, 'check-half')
        ops = [('check-commit', prep['body']), ('settle', {'attempt': prep['attempt']['sequence'], 'actual': '0.50', 'unit': 'simulated_research_units', 'provenance': {'kind': 'TOOL_RECEIPT', 'receipt': prep['receipt']}})]
        for op, payload in ops:
            original_key = key()
            request = self.run / (op + '.json')
            write(request, {'mode': 'lost-response', 'connection': str(self.checker_file), 'actor': self.ck.actor, 'op': op, 'payload': payload, 'key': original_key})
            proc = subprocess.Popen([sys.executable, '-m', 'tests.integration.test_checker_steps', '--worker', str(request), str(request.with_suffix('.unused'))], cwd=ROOT,
                                    env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate(timeout=30)
            self.assertEqual(proc.returncode, 23, stderr)
            self.restart()
            recorded = self.ck.outcome(original_key)
            self.assertEqual(recorded['status'], 'COMMITTED')
            replay = self.ck.call(op, payload, original_key)
            self.assertEqual(replay.raw, recorded)
            self.trace.append({'lost_response': op, 'caller_pid': proc.pid, 'exit': 23, 'request_key': original_key, 'recorded': recorded, 'replay': replay.raw})
        close_key = key()
        payload = {'reservation': prep['reservation']['sequence']}
        closed = self.ck.call_or_raise('close', payload, close_key)
        self.assertEqual(self.ck.call_or_raise('close', payload, close_key).raw, closed.raw)
        checks = [e for e in self.p.history('T') if e['kind'] == 'CHECK' and e['transition_id'] == tr]
        settlements = [e for e in self.p.history('E') if e['kind'] == 'SETTLEMENT' and e['body']['attempt'] == prep['attempt']['sequence']]
        self.assertEqual(len(checks), 1)
        self.assertEqual(len(settlements), 1)
        self.assertEqual(self.p.budget(self.ids['grants']['checker'])['committed'], '0.75')
        self.assertEqual(self.p.obligations()['pending_attempts'], [])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--worker':
        worker(sys.argv[2], sys.argv[3])
    else:
        unittest.main()
