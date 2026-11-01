"""One command runs the whole demonstration.

    python3 -m examples.langgraph_headlines            (from the checkout)
    python3 -m langgraph_headlines --harness /path/to/checkout   (from a copy outside it)

Starts the local host from the checkout against this directory's setup, runs
startup, one governed research cycle through the LangGraph researcher and the
evaluator, then the control demonstrations. Prints the research result and
every control decision. Returns a report for tests.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import threading
import time
from arh_client import connect, Connection, Principal, Observer, Researcher, HostControl, startup, Execution, ReceiptStore
from .provider import FakeProvider

HERE = Path(__file__).resolve().parent
PACKAGE = __package__
PACKAGE_CWD = HERE.parents[PACKAGE.count('.')]


def harness_root(explicit=None):
    candidate = Path(explicit or os.environ.get('ARH_HARNESS_ROOT') or '').resolve() if (explicit or os.environ.get('ARH_HARNESS_ROOT')) else None
    if candidate is None:
        for p in [HERE] + list(HERE.parents):
            if (p / 'adaptive_research_harness' / 'engine.py').is_file(): candidate = p; break
    if candidate is None or not (candidate / 'adaptive_research_harness' / 'engine.py').is_file():
        raise SystemExit('harness checkout not found; pass --harness or set ARH_HARNESS_ROOT')
    return candidate


class Host:
    """The local host as a subprocess started inside the checkout. The example imports only the client."""
    def __init__(self, root, setup_dir, run_dir):
        self.root = Path(root); self.setup = Path(setup_dir); self.run = Path(run_dir); self.proc = None; self.connection = None
    def start(self):
        self.proc = subprocess.Popen([sys.executable, '-m', 'adaptive_research_harness.local_host', '--setup', str(self.setup), '--run', str(self.run)],
                                     cwd=self.root, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        deadline = time.monotonic() + 120; lines = []
        while time.monotonic() < deadline:
            line = self.proc.stdout.readline()
            if not line:
                if self.proc.poll() is not None: raise RuntimeError('host exited: ' + ''.join(lines))
                continue
            lines.append(line)
            if line.startswith('connection '): self.connection = Path(line.split(' ', 1)[1].strip()); break
        if self.connection is None: raise RuntimeError('host did not report a connection file: ' + ''.join(lines))
        threading.Thread(target=lambda: [None for _ in self.proc.stdout], daemon=True).start()
        return self.connection
    def stop(self):
        if self.proc is None: return
        try: HostControl.from_file(self.connection).stop()
        except Exception: pass
        try: self.proc.wait(timeout=20)
        except subprocess.TimeoutExpired: self.proc.kill()


class Demo:
    def __init__(self, root, run_dir, quiet=False):
        self.root = root; self.run_dir = Path(run_dir); self.quiet = quiet; self.report = {'checks': [], 'demonstrations': {}, 'lines': []}
    def say(self, *parts):
        line = ' '.join(str(p) for p in parts); self.report['lines'].append(line)
        if not self.quiet: print(line, flush=True)
    def expect(self, name, condition, detail=''):
        self.report['demonstrations'][name] = bool(condition)
        self.say(('  ok  ' if condition else '  FAIL') + ' ' + name + ((': ' + str(detail)) if detail else ''))
        return bool(condition)

    # ----- processes under other identities -----
    def check(self, tr):
        out = subprocess.run([sys.executable, '-m', PACKAGE + '.check', '--connection', str(self.connection), '--transition', tr], cwd=PACKAGE_CWD, capture_output=True, text=True)
        if out.returncode != 0: raise RuntimeError(out.stderr)
        result = json.loads(out.stdout); self.report['checks'].append({'transition': tr, 'result': result.get('result'), 'criteria': result.get('criteria')}); return result
    def passing_check(self, tr):
        r = self.check(tr)
        if r.get('result') != 'PASS': raise RuntimeError('startup check failed for ' + tr + ': ' + json.dumps(r.get('criteria')))
        return r['check_sequence']
    def job(self, job, mode='classify', options=None, crash=None):
        args = [sys.executable, '-m', PACKAGE + '.researcher', '--connection', str(self.connection), '--run-dir', str(self.run_dir), '--job', job, '--mode', mode, '--options', json.dumps(options or {})]
        if crash: args += ['--crash', crash]
        proc = subprocess.run(args, cwd=PACKAGE_CWD, capture_output=True, text=True)
        if proc.returncode == 137: return {'crashed': True, 'pid': None, 'returncode': 137, 'stderr': proc.stderr}
        if proc.returncode != 0: raise RuntimeError(proc.stderr)
        return json.loads(proc.stdout)
    def crashing_job(self, job, crash, options=None):
        args = [sys.executable, '-m', PACKAGE + '.researcher', '--connection', str(self.connection), '--run-dir', str(self.run_dir), '--job', job, '--mode', 'classify', '--options', json.dumps(options or {}), '--crash', crash]
        proc = subprocess.Popen(args, cwd=PACKAGE_CWD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True); out, err = proc.communicate(timeout=120)
        return {'pid': proc.pid, 'returncode': proc.returncode, 'stderr': err}

    # ----- the run -----
    def run(self):
        host = Host(self.root, HERE, self.run_dir)
        try:
            self.connection = host.start(); self.report['connection'] = str(self.connection); self.report['run_dir'] = str(self.run_dir)
            principal = Principal(connect(self.connection, 'Principal')); observer = Observer(connect(self.connection, 'Observation function'))
            control = HostControl.from_file(self.connection); researcher_conn = connect(self.connection, 'AD-RH1.0'); researcher = Researcher(researcher_conn)
            c = principal.c; profile = c.profile(); provider = FakeProvider(self.run_dir / 'provider')
            self.say('Experiment', profile['experiment']['ExperimentId'], 'on build', profile['inventory_sha256'][:16], 'host', self.connection.parent)
            self.say('Trust: one host holds every token; the researcher reports its own receipts for FAKE-LLM-1 (accounting, not enforcement); no OS isolation.')

            # 1. startup
            s = startup(principal, observer, self.passing_check, tick=control.tick)
            self.expect('startup through checked controls', s['N'] == 5 and len(self.report['checks']) == 5 and all(x['result'] == 'PASS' for x in self.report['checks']), f"N={s['N']}, {len(self.report['checks'])} checks PASS by AD-CK-H1.0")

            # 2. research cycle
            j1 = self.job('j1-classify')
            rec = c.get(j1['record']['refs'][0]); labels = rec['body']['result']
            self.expect('classification recorded and settled', j1['status'] == 'recorded' and j1['receipt']['actual'] == '0.48' and labels['n_bullish'] == 12,
                        f"E{rec['seq']} labels {labels['n_bullish']} bullish / {labels['n_bearish']} bearish of {labels['n_rows']}, cost {j1['receipt']['actual']}, provider calls {j1['provider_calls']}")
            labels_ref = j1['record']['refs'][0]
            control.tick(86400000 + 1000)
            returns = observer.observe('SRC-RET-SYN', profile['artifacts']['returns_cohort']['content'], '2026-10-29')
            self.expect('returns document committed one period later', returns.ok, f"E{returns.sequence} returns-2026-10-29; the classifier never saw it")

            # 6 (first): an overstated joined record is proposed and fails its Check
            bad = self.job('j2-join-inflated', 'join', {'labels_record': labels_ref, 'exaggerate': True})
            bad_check = self.check(bad['proposal']['transition_id'])
            bad_decision = principal.policy_decide(bad['proposal']['transition_id'], bad_check['check_sequence'])
            n_before = c.state()['N']
            self.expect('overstated count fails the independent Check and is not admitted',
                        bad['status'] == 'proposed' and bad_check['result'] == 'FAIL' and bad_check['criteria']['recomputation'] == 'NOT MET' and bad_decision.reason == 'CHECK_NOT_PASS' and n_before == 5,
                        f"{bad['proposal']['transition_id']} Check FAIL (recomputation NOT MET), policy-decide refused {bad_decision.reason}, N={n_before}; proposal stays on the Transition ledger outside the Applied History")
            researcher.close(bad['proposal']['funding_ref'], Connection.new_key())

            # 2 (continued): the honest join, proposed, checked, admitted
            good = self.job('j2-join', 'join', {'labels_record': labels_ref})
            tr = good['proposal']['transition_id']; derived = c.get(good['derived'])['body']['result']
            # 4. the researcher cannot approve its own proposal or change its rules
            refusals = {}
            refusals['apply before decision'] = researcher_conn.call('apply', {'transition_id': tr, 'decision': 1})
            refusals['check-commit'] = researcher_conn.call('check-commit', {'transition_id': tr, 'base': c.state()['N'], 'grant': 'AU-RH-1', 'attempt': 1, 'closure': {'E': 1, 'N': 0, 'F': 'N/A — no Paper Book', 'time_ms': 0},
                                                                              'criteria': {}, 'result': 'PASS', 'es': 'ES-1.0', 'constitution': 1, 'provenance': {}, 'context': {}})
            refusals['decide'] = researcher_conn.call('decide', {'transition_id': tr, 'check': 1, 'decision': 'ADMITTED', 'reason': 'self-approval'})
            refusals['policy-decide'] = researcher_conn.call('policy-decide', {'transition_id': tr, 'check': 1})
            refusals['fence'] = researcher_conn.call('fence', {'grant': 'AU-RH-1', 'reason': 'self-issued'})
            future = researcher.next_evidence_sequence()
            refusals['propose LIMITS'] = researcher_conn.call('propose', {'transition_id': 'TR-RH-LIMITS', 'base': c.state()['N'], 'class': 'LIMITS', 'subject': 'initial_limits', 'content': dict(profile['setup']['initial_limits'], portfolio_capital_units='1.00'),
                                                                           'budget': '0.00', 'grant': 'AU-RH-1', 'funding_ref': future, 'delta': {'O': 0, 'S': 0, 'A': 0}})
            refusals['propose AUTHORIZATION'] = researcher_conn.call('propose', {'transition_id': 'TR-RH-GRANT', 'base': c.state()['N'], 'class': 'AUTHORIZATION', 'subject': 'AU-RH-2', 'content': {'action': 'GRANT', 'predecessor': None, 'grant': dict(researcher.grant(), AuthorizationId='AU-RH-2', research_budget_units='999.00')},
                                                                                  'budget': '0.00', 'grant': 'AU-RH-1', 'funding_ref': future, 'delta': {'O': 0, 'S': 0, 'A': 0}})
            summary = {k: v.reason for k, v in refusals.items()}
            preserved = sum(1 for e in c.history('E') + c.history('T') if e['kind'] == 'REFUSAL' and e['actor'] == 'AD-RH1.0')
            self.expect('researcher cannot approve its own proposal or change its rules', all(v.status == 'REFUSED' for v in refusals.values()) and preserved >= len(refusals),
                        ', '.join(f'{k} -> {v}' for k, v in summary.items()) + f'; {preserved} refusals preserved on the ledgers')
            self.report['refusals'] = summary
            good_check = self.check(tr); decision = principal.policy_decide(tr, good_check['check_sequence']); applied = principal.apply(tr, decision.sequence)
            state = c.state()
            self.expect('honest proposal passes Check, P-1 admits, Apply registers', good_check['result'] == 'PASS' and decision.ok and applied.ok and state['N'] == 6 and 'HY-HEAD-1.0' in state['hypotheses'],
                        f"{tr}: joined {derived['k_bullish_up']}/{derived['n_bullish']} bullish labels followed by a positive return ({'meets' if derived['passes'] else 'below'} three in five, a diagnostic), Check PASS, P-1 ADMITTED, N={state['N']}")
            researcher.close(good['proposal']['funding_ref'], Connection.new_key())
            self.report['research'] = {'labels': {k: labels[k] for k in ('n_rows', 'n_bullish', 'n_bearish')}, 'joined': {k: derived[k] for k in ('n_bullish', 'k_bullish_up', 'n_bearish', 'k_bearish_down', 'passes')}, 'transition': tr, 'N': state['N']}

            # 3. over budget, before the provider runs
            calls_before = provider.calls()
            over = self.job('j3-over-budget', options={'reserve_amount': '5.00'})
            thin = self.job('j3-thin-reservation', options={'reserve_amount': '0.20'})
            if thin.get('reservation'): researcher.close(thin['reservation'], Connection.new_key())
            self.expect('over-budget work refused before the provider runs', over['status'] == 'refused' and over['reason'] == 'BUDGET_EXCEEDED' and thin['status'] == 'refused' and thin['reason'] == 'ALLOWANCE_EXCEEDED' and provider.calls() == calls_before,
                        f"reserve 5.00 -> {over['reason']}; reserve 0.20 then attempt 0.48 -> {thin['reason']}; provider calls still {provider.calls()}")

            # 5. interruption and loss
            calls_before = provider.calls()
            k1 = self.crashing_job('j4-crash-after-receipt', 'after_receipt'); r1 = self.job('j4-crash-after-receipt')
            replay = Execution.from_record(researcher, r1['attempt']).claim()
            self.expect('killed after the durable receipt: resumed, no second provider call', k1['returncode'] == 137 and r1['resumed'] and r1['execution'] == 'resumed' and r1['status'] == 'recorded' and provider.calls() == calls_before + 1,
                        f"attempt E{r1['attempt']} resumed from checkpoint, provider calls {provider.calls() - calls_before}")
            self.expect('replaying the successful claim request grants no permission', replay.get('status') == 'RECEIPT' and provider.calls() == calls_before + 1, f"tool-run again -> {replay.get('status')}")
            calls_before = provider.calls()
            k2 = self.crashing_job('j5-crash-after-provider', 'after_provider_record'); r2 = self.job('j5-crash-after-provider')
            self.expect('killed after the provider completed, before the receipt: recovered by lookup under the original claim', k2['returncode'] == 137 and r2['execution'] == 'recovered' and r2['status'] == 'recorded' and provider.calls() == calls_before + 1,
                        f"attempt E{r2['attempt']} receipt rebuilt from the provider's own record, provider calls {provider.calls() - calls_before}")
            calls_before = provider.calls()
            k3 = self.crashing_job('j6-crash-before-provider-record', 'before_provider_record', {'reserve_amount': '1.00'}); r3 = self.job('j6-crash-before-provider-record')
            budget = c.budget('AU-RH-1'); obligations = c.obligations()
            self.expect('killed with no record anywhere: reconciled at the maximum, liability kept, no second call', k3['returncode'] == 137 and r3['execution'] == 'uncertain' and r3['status'] == 'reconciled' and r3['settlement'].get('status') == 'COMMITTED' and provider.calls() == calls_before + 1 and not obligations['pending_attempts'],
                        f"attempt E{r3['attempt']} settled UNKNOWN at {r3['maximum']}, AU-RH-1 committed {budget['committed']}, pending attempts {obligations['pending_attempts']}")
            retry1 = researcher.retry(r3['attempt'], Connection.new_key())
            gen = control.generation(k3['pid']); control.quiesce(gen)
            retry2 = researcher.retry(r3['attempt'], Connection.new_key())
            disposition = provider.cancel(r3['attempt'], r3['attempt_input_hash'])
            control.quiesce(gen, {str(r3['attempt']): disposition})
            retry3 = researcher.retry(r3['attempt'], Connection.new_key())
            self.expect('replacement refused until the caller is gone and the provider operation is cancelled', retry1.reason == 'WORKER_NOT_QUIESCENT' and retry2.reason == 'WORKER_NOT_QUIESCENT' and retry3.ok,
                        f"no proof -> {retry1.reason}; caller dead -> {retry2.reason}; provider {disposition['state']} -> retry admitted as attempt E{retry3.sequence}")
            if retry3.ok:
                ex = Execution(researcher, retry3.sequence, retry3.input_hash, 'FAKE-LLM-1', c.get(retry3.ref)['body']['maximum'])
                doc = c.get(c.get(retry3.ref)['body']['input']['input_refs'][0])['body']['document']
                outcome = ex.run(lambda claim: provider(doc, {'lexicon': 'LEX-1'}, claim), ReceiptStore(self.run_dir / 'researcher' / 'receipts'), provider.lookup)
                settled = ex.settle(outcome['receipt'], Connection.new_key())
                self.expect('replacement attempt executed once and settled', outcome['status'] == 'executed' and settled.ok, f"attempt E{ex.attempt} actual {outcome['receipt']['actual']}")
                researcher.close(c.get(retry3.ref)['body']['reservation'], Connection.new_key())

            budget = c.budget('AU-RH-1'); ck = c.budget('AU-CK-H'); obligations = c.obligations()
            self.say('Budgets: AU-RH-1 committed', budget['committed'], 'of 3.00; AU-CK-H committed', ck['committed'], '; pending attempts', obligations['pending_attempts'])
            self.report['budgets'] = {'AU-RH-1': budget['committed'], 'AU-CK-H': ck['committed']}; self.report['N'] = c.state()['N']; self.report['provider_calls'] = provider.calls()
            self.report['status'] = 'PASS' if all(self.report['demonstrations'].values()) else 'FAIL'
            self.say('Result:', self.report['status'], '| research is synthetic and earns no forward standing; the Check verified the join and the arithmetic, not the labels.')
        except Exception as exc:
            import traceback
            self.report['status'] = 'ERROR'; self.report['error'] = str(exc); self.report['traceback'] = traceback.format_exc(); self.say('ERROR', exc)
        finally:
            host.stop()
        return self.report


def run(argv=None):
    p = argparse.ArgumentParser(prog=PACKAGE); p.add_argument('--harness', default=None); p.add_argument('--run', default=None); p.add_argument('--quiet', action='store_true')
    a = p.parse_args(argv); root = harness_root(a.harness)
    run_dir = Path(a.run) if a.run else root / 'artifacts' / 'development' / 'langgraph' / time.strftime('%Y%m%d-%H%M%S')
    run_dir.mkdir(parents=True, exist_ok=True)
    report = Demo(root, run_dir, quiet=a.quiet).run()
    (run_dir / 'report.json').write_text(json.dumps(report, indent=1, sort_keys=True, default=str))
    return report


if __name__ == '__main__': sys.exit(0 if run().get('status') == 'PASS' else 1)
