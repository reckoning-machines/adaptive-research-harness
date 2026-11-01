"""The demonstration, end to end, with the awkward interruption points. Demonstration and test code.

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m examples.memo_returns

Brings the project up with one call, imports six memos and a returns
table, then runs the graph in separate processes: killed after the second
metered call, killed inside the fourth call between permission and
receipt, blocked until the host confirms that process is gone, resumed
with the replacement, killed after the join's record and before the node
returned, resumed, paused for review. Then a wrong evaluator fails the
check and the right one passes, a resume before any decision pauses
again, the researcher's own attempt to decide is refused, the Principal's
decision pauses the graph once more until it is applied, and the host is
closed and reopened. Prints every step and returns a report. Generated
data, labelled synthetic; no forward standing.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'client')); sys.path.insert(0, str(ROOT))
from arh_client import api, dev
from arh_client.host import HostControl
from examples.memo_returns.provider import calls_file
from examples.memo_returns.evaluator import recompute

RUNS = ROOT / 'artifacts' / 'development' / 'memo_returns'
GROUPS = {'research': ('research.py', 'tools.py', 'provider.py', 'evaluator.py', 'graph.py'), 'configuration': ('project.json',), 'process': ('job.py',), 'demonstration': ('__main__.py', 'make_data.py')}


def fmt(m): return f"{m['numerator']}/{m['denominator']}" if isinstance(m, dict) else str(m)


def line_counts():
    def count(p): return len(p.read_text().splitlines())
    files = {p.name: count(p) for p in HERE.iterdir() if p.suffix in ('.py', '.json') and p.name not in ('setup.json', 'designs_and_methods.json', 'experiment.json', '__init__.py')}
    client = {p.name: count(p) for p in (ROOT / 'client' / 'arh_client').glob('*.py')}
    return {'files': files, 'groups': {g: sum(files.get(f, 0) for f in fs) for g, fs in GROUPS.items()}, 'client': {k: client[k] for k in ('api.py', 'langgraph_nodes.py', 'analysis.py', 'operations.py', 'project.py', 'dev.py', 'refusals.py')}}


class Demo:
    def __init__(self, name=None, quiet=False):
        self.name = name or time.strftime('%Y%m%d-%H%M%S') + '-memo-returns'; self.quiet = quiet; self.run_dir = RUNS / self.name
        self.report = {'lines': [], 'checks': {}, 'timings': {}, 'name': self.name}
    def say(self, *parts):
        line = ' '.join(str(p) for p in parts); self.report['lines'].append(line)
        if not self.quiet: print(line, flush=True)
    def expect(self, name, condition, detail=''):
        self.report['checks'][name] = bool(condition); self.say(('  ok  ' if condition else '  FAIL') + ' ' + name + ((': ' + str(detail)) if detail else '')); return bool(condition)
    def job(self, crash=None, provider_crash=None):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(ROOT / 'client'), MEMO_PROVIDER_DIR=str(self.run_dir / 'researcher' / 'provider'))
        if provider_crash: env['MEMO_PROVIDER_CRASH'] = str(provider_crash)
        args = [sys.executable, '-m', 'examples.memo_returns.job', '--run', str(self.run_dir)] + (['--crash', crash] if crash else [])
        proc = subprocess.Popen(args, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True); out, err = proc.communicate()
        if proc.returncode == 137: return {'crashed': True, 'pid': proc.pid}
        if proc.returncode == 3: return dict(json.loads(out), pid=proc.pid)
        if proc.returncode != 0: raise RuntimeError(err.strip()[-2000:])
        return json.loads(out)
    def calls(self): return json.loads(calls_file().read_text())['calls'] if calls_file().exists() else 0

    def run(self):
        os.environ['MEMO_PROVIDER_DIR'] = str(self.run_dir / 'researcher' / 'provider'); t0 = time.monotonic()
        host, project, fresh = dev.start(HERE, self.run_dir, charter='# Charter\nDo positive-tone analyst memos precede positive next-day returns, and does a placebo column show nothing?\n')
        self.report['timings']['up_s'] = round(time.monotonic() - t0, 1)
        try:
            importer = api.connect(HERE, 'observer', self.run_dir); research = api.connect(HERE, 'researcher', self.run_dir); c = research.c
            owner = api.connect(HERE, 'principal', self.run_dir); owner.advance_to('2026-10-31')
            self.expect('project up with one call, startup signed', fresh and c.state()['N'] == 5, f"N={c.state()['N']} in {self.report['timings']['up_s']} s; connection {host.connection_path.name}")
            for p in sorted((HERE / 'data' / 'memos').glob('*.md')): importer.import_file('SRC-MEMO-SYN', p, '2026-10-30', 'examples/memo_returns/data/memos', note='generated, labelled synthetic')
            importer.import_file('SRC-RET-SYN', HERE / 'data' / 'returns.csv', '2026-10-31', 'examples/memo_returns/data', note='generated, labelled synthetic')
            docs = research.documents(); self.expect('two sources imported', len([d for d in docs if d['source'] == 'SRC-MEMO-SYN']) == 6 and len([d for d in docs if d['source'] == 'SRC-RET-SYN']) == 1, f"{len(docs)} documents, {sum(1 for d in docs if d['class'] == 'synthetic')} labelled synthetic")
            # 1. killed after the second metered call; the journal, not the checkpoint, holds the two calls
            j1 = self.job(crash='after_call_2'); ops = [e for e in research.ops.list() if e['kind'] == 'call']
            self.expect('killed after two calls: both journaled before the node returned', j1.get('crashed') and self.calls() == 2 and len(ops) == 2 and all(e['status'] == 'recorded' for e in ops), f'provider calls {self.calls()}, journal entries {[e["operation"] for e in ops]}')
            # 2. killed inside the fourth call, after the provider counted it and before any receipt
            j2 = self.job(provider_crash=4)
            self.expect('killed inside the fourth call: the first two calls were not repeated', j2.get('crashed') and self.calls() == 4, f'provider calls {self.calls()}')
            # 3. resumed: the fourth call is uncertain; its replacement is refused until the host confirms the dead process is gone
            j3 = self.job(); pending = c.obligations()['pending_attempts']; entry = research.ops.get('score/m04.md')
            self.expect('uncertain call settled at the maximum; replacement refused without proof of quiescence', 'error' in j3 and 'WORKER_NOT_QUIESCENT' in j3['error'] and entry['status'] == 'uncertain' and pending == [], f"{j3.get('error', '')[:120]}")
            control = HostControl.from_file(host.connection_path); control.quiesce(control.generation(j2['pid']))
            # 4. resumed again: replacement admitted with the next dispatch index, remaining calls made, then killed after the join's record before the node returned
            j4 = self.job(crash='join:after_record'); attempts = [e for e in c.history('E') if e['kind'] == 'ATTEMPT' and e['body']['input']['tool_id'] == 'TONE-CALL-1']
            self.expect('replacement admitted after quiescence; six memos, seven calls, one authorized repeat', j4.get('crashed') and self.calls() == 7 and len(attempts) == 7 and sorted(a['body']['dispatch_index'] for a in attempts) == [0, 0, 0, 0, 0, 0, 1], f'calls {self.calls()}, attempts {len(attempts)}' + (f"; job: {j4.get('error')}" if j4.get('error') else ''))
            join_attempts = lambda: [e for e in c.history('E') if e['kind'] == 'ATTEMPT' and e['body']['input']['tool_id'] == 'TONE-JOIN-1']
            self.expect('join killed after its record, before the node returned: the record is on the ledger and in the journal', research.ops.get('join') is not None and 'record' in (research.ops.get('join') or {}).get('stages', {}) and len(join_attempts()) >= 1, f"join stages {sorted((research.ops.get('join') or {}).get('stages', {}))}, join attempts {len(join_attempts())}")
            # 5. resumed: join and placebo recover their own attempts; the selection proposes; the graph pauses for review
            j5 = self.job(); arh = j5.get('arh', {}); join = arh.get('join', {}); placebo = arh.get('placebo', {}); nxt = arh.get('next', {})
            self.expect('parallel branches resumed, one attempt each, nothing run twice', j5.get('paused') and join.get('status') == 'recorded' and placebo.get('status') == 'recorded' and len(join_attempts()) == 2 and self.calls() == 7,
                        f"join {fmt(join.get('conclusion', {}).get('metric'))} {join.get('conclusion', {}).get('state')}; placebo {fmt(placebo.get('conclusion', {}).get('metric'))} {placebo.get('conclusion', {}).get('state')}; join attempts {len(join_attempts())}")
            self.report['results'] = {'join': join.get('conclusion'), 'placebo': placebo.get('conclusion'), 'links': join.get('links')}
            tr = nxt.get('transition'); self.expect('own next question recorded and proposed; graph paused waiting for review', nxt.get('status') == 'waiting_for_review' and bool(tr), f"{tr} {nxt.get('theme')}")
            if not tr: raise RuntimeError('no proposal; the review demonstrations cannot run: ' + json.dumps(j5, default=str)[:800])
            # 6. a wrong evaluator fails the check; the right one passes
            wrong = api.connect(HERE, 'checker', self.run_dir, recompute=lambda inputs, spec, result: False); c1 = wrong.check(tr)
            right = api.connect(HERE, 'checker', self.run_dir, recompute=recompute, kind='tone-return-join'); c2 = right.check(tr)
            self.expect('check fails when the result does not recompute, passes when it does', c1.result == 'FAIL' and c2.result == 'PASS' and research.review(tr).status == 'waiting_for_review', f'first check {c1.result}, second {c2.result}')
            # 7. resuming the graph before any decision pauses it again; the researcher cannot decide
            j6 = self.job(); refused = c.call('decide', {'transition_id': tr, 'check': c2.check_sequence, 'decision': 'ADMITTED', 'reason': 'the graph approves itself'})
            self.expect('resume is not approval; a researcher deciding is refused', j6.get('paused') and (j6.get('pause') or {}).get('review') == 'waiting_for_review' and not refused.ok and refused.reason == 'UNAUTHORIZED', f"resume {j6.get('how')} paused {j6.get('paused')}; decide {refused.reason}")
            # 8. the Principal decides; the graph pauses again until the decision is applied
            d = owner.decide(tr, 'ADMITTED', 'placebo clean; test on the next quarter'); j7 = self.job()
            self.expect('decision recorded; graph pauses again because a decision is not an application', d.ok and j7.get('paused') and (j7.get('pause') or {}).get('review') == 'decided' and (j7.get('pause') or {}).get('decision') == 'ADMITTED', f"review {(j7.get('pause') or {}).get('review')} decision {(j7.get('pause') or {}).get('decision')}")
            a = owner.apply(tr); j8 = self.job()
            self.expect('applied: the graph completes with the accepted direction', a.ok and not j8.get('paused') and j8['arh']['next'].get('review') == 'applied' and c.state()['N'] == 6, f"N={c.state()['N']}, themes {sorted(c.state()['themes'])}")
            self.report['timings']['to_applied_s'] = round(time.monotonic() - t0, 1)
        finally: host.close()
        self.say('Host closed. Reopening the run with the same call.')
        host, project, fresh = dev.start(HERE, self.run_dir)
        try:
            j9 = self.job(); research = api.connect(HERE, 'researcher', self.run_dir)
            self.expect('reopened: the finished graph reports the same state and starts nothing', not fresh and j9.get('how') == 'already_finished' and j9['arh']['next'].get('review') == 'applied' and self.calls() == 7, f"{j9.get('how')}")
            hist = research.history.conclusions(where={'column': 'next_day_bp'}); self.expect('history query by analysis field', len(hist) == 1 and hist[0]['conclusion']['state'] == 'MET', f"{len(hist)} conclusion(s) for next_day_bp")
            self.report['state'] = research.c.state()['N']
        finally: host.close()
        counts = line_counts(); self.report['line_groups'] = counts['groups']; self.report['client_lines'] = counts['client']; self.report['timings']['total_s'] = round(time.monotonic() - t0, 1)
        g = counts['groups']; self.say('Lines:', f"research {g['research']} | configuration {g['configuration']} | process {g['process']} | demonstration {g['demonstration']} | client api+nodes {counts['client']['api.py'] + counts['client']['langgraph_nodes.py']}")
        self.say('Timings:', self.report['timings'])
        self.report['status'] = 'PASS' if all(self.report['checks'].values()) else 'FAIL'; self.say('Result:', self.report['status'], '| generated data labelled synthetic; no forward standing.')
        return self.report


def run(argv=None):
    p = argparse.ArgumentParser(prog='examples.memo_returns'); p.add_argument('--name', default=None); p.add_argument('--quiet', action='store_true'); a = p.parse_args(argv)
    report = Demo(a.name, a.quiet).run()
    if (RUNS / report['name']).exists(): (RUNS / report['name'] / 'report.json').write_text(json.dumps(report, indent=1, default=str))
    return report


if __name__ == '__main__': sys.exit(0 if run().get('status') == 'PASS' else 1)
