"""The demonstration, end to end, with timings. Demonstration and test code; ordinary use is __main__.py.

    .venv/bin/python -m examples.signal_groups.demo            (or python3; the client must be importable)

Runs the script directly for a baseline, then through ARH: charter, import,
expectation recorded before the analysis, run, candidates from the evidence,
a recorded selection, an independent check, the Principal's decision, a
second investigation whose candidates are shaped by the first selection,
new rows reinstating a rejected candidate, and an interrupted attempt
resumed after the host is closed and reopened. Prints every step and
returns a report. This is a new example, not an adopted workflow; its data
is generated and labelled synthetic.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'client')); sys.path.insert(0, str(ROOT))
from workbench.local_session import LocalRun, open_local, RUNS
from examples.signal_groups.signal_groups import analyze, read_csv

GROUPS = {'script': ('signal_groups.py',), 'experiment': ('tool.py', 'candidates.py', 'researcher.py', 'evaluator.py'), 'setup': ('make_setup.py',),
          'command_line': ('__main__.py', 'job.py'), 'demonstration': ('demo.py', 'make_data.py')}


def fmt(m): return f"{m['numerator'] / m['denominator']:.1f}" if isinstance(m, dict) else str(m)


def line_counts():
    def count(p): return len(p.read_text().splitlines())
    lines = {p.name: count(p) for p in HERE.glob('*.py') if p.name != '__init__.py'}
    return {'files': lines, 'groups': {g: sum(lines.get(f, 0) for f in fs) for g, fs in GROUPS.items()}, 'client_analysis': count(ROOT / 'client/arh_client/analysis.py')}


class Demo:
    def __init__(self, name=None, quiet=False):
        self.name = name or time.strftime('%Y%m%d-%H%M%S') + '-signal-groups'; self.quiet = quiet; self.report = {'lines': [], 'checks': {}, 'timings': {}}
    def say(self, *parts):
        line = ' '.join(str(p) for p in parts); self.report['lines'].append(line)
        if not self.quiet: print(line, flush=True)
    def expect(self, name, condition, detail=''):
        self.report['checks'][name] = bool(condition); self.say(('  ok  ' if condition else '  FAIL') + ' ' + name + ((': ' + str(detail)) if detail else '')); return bool(condition)
    def job(self, connection, design_seq, crash=None):
        args = [sys.executable, '-m', 'examples.signal_groups.job', '--connection', str(connection), '--work', str(RUNS / self.name / 'work'), '--design', str(design_seq)]
        if crash: args += ['--crash', crash]
        proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(ROOT / 'client')))
        if proc.returncode == 137: return {'crashed': True}
        if proc.returncode != 0: raise RuntimeError(proc.stderr)
        return json.loads(proc.stdout)

    def run(self):
        t0 = time.monotonic()
        base = analyze(read_csv(HERE / 'data' / 'signals.csv'), 'mom_20', 'fwd_5d_bp', 3); self.report['timings']['script_direct_s'] = round(time.monotonic() - t0, 3)
        self.say('Baseline, the script on its own:', f"spread {fmt(base['spread_top_minus_bottom_bp'])} bp over {base['rows_used']} rows, {self.report['timings']['script_direct_s']} s")
        t1 = time.monotonic(); s = LocalRun.create('# Charter\nDoes the momentum signal in my table separate forward returns, and does the relation survive a placebo and more data?\n', self.name, setup=HERE)
        self.report['timings']['startup_s'] = round(time.monotonic() - t1, 1)
        try:
            v = s.view(); self.expect('startup through checked controls', v['state']['N'] == 5, f"N={v['state']['N']} in {self.report['timings']['startup_s']} s")
            imp = s.import_document('signals.csv', (HERE / 'data' / 'signals.csv').read_bytes(), 'examples/signal_groups/data', note='generated, labelled synthetic', date='2026-10-30')
            doc1 = s.view()['documents'][0]; self.expect('table imported with its hash', imp.ok and doc1['rows'] == 240, f"E{doc1['seq']} {doc1['name']} {doc1['rows']} rows sha {doc1['file_sha256'][:12]}")
            # 1. the expectation, recorded before the analysis
            exp1 = {'comparator': '>=', 'value': 50, 'minimum_n': 100, 'statement': 'top tercile beats bottom tercile by at least 50 bp'}
            d1 = s.design('Does mom_20 separate fwd_5d_bp across terciles?', exp1, {'kind': 'signal-groups', 'signal': 'mom_20', 'outcome': 'fwd_5d_bp', 'groups': 3}, [doc1['seq']])
            self.expect('expectation recorded before the analysis', d1.ok, f"design E{d1.sequence}: {exp1['statement']}")
            r1 = s.run(d1.sequence); c1 = r1['conclusion']
            self.expect('analysis run by the host and recorded', r1['status'] == 'recorded' and r1['execution'] == 'registered' and c1['metric'] == base['spread_top_minus_bottom_bp'], f"spread {fmt(c1['metric'])} bp, same as the direct run; conclusion {c1['state']}; settled {r1['settlement'].ok}")
            self.report['timings']['first_result_s'] = round(time.monotonic() - t1, 1)
            inv1 = s.view()['investigations'][0]; cands = s.researcher.candidates({'ledger': 'E', 'sequence': inv1['result']['seq'], 'sha256': inv1['result']['sha256']})
            self.say('Candidates from the evidence:', [c['id'] for c in cands['candidates']], 'excluded', cands['excluded'])
            sel1 = s.researcher.select({'ledger': 'E', 'sequence': inv1['result']['seq'], 'sha256': inv1['result']['sha256']}, 'placebo-signal', 'a spread the placebo also shows would mean nothing', 'Does vol_60, which should carry nothing, show a spread under 25 bp?')
            self.expect('selection recorded with rejections and their reconsideration conditions', sel1.ok, [(r['id'], r['reconsider_when']) for r in s.c.get(sel1.ref)['body']['result']['rejections']])
            pr1 = s.propose(sel1.sequence); c = s.check(pr1.transition_id); d = s.decide(pr1.transition_id, 'ADMITTED', 'placebo first'); a = s.apply(pr1.transition_id)
            self.expect('direction checked, admitted and applied', c.result == 'PASS' and d.ok and a.ok and s.view()['state']['N'] == 6, f"{pr1.transition_id} check {c.result}, N={s.view()['state']['N']}")
            self.report['timings']['first_admitted_direction_s'] = round(time.monotonic() - t1, 1)
            # 2. the placebo under the new direction; its candidates are shaped by the first selection
            exp2 = {'comparator': '<', 'value': 25, 'minimum_n': 100, 'statement': 'placebo spread stays under 25 bp'}
            d2 = s.design('Does vol_60 separate fwd_5d_bp?', exp2, {'kind': 'signal-groups', 'signal': 'vol_60', 'outcome': 'fwd_5d_bp', 'groups': 3}, [doc1['seq']], revises=None, theme='TH-S1')
            r2 = s.run(d2.sequence); c2 = r2['conclusion']; inv2 = s.view()['investigations'][1]
            self.say('Placebo result:', f"spread {fmt(c2['metric'])} bp, conclusion {c2['state']}")
            cands2 = s.researcher.candidates({'ledger': 'E', 'sequence': inv2['result']['seq'], 'sha256': inv2['result']['sha256']}, theme='TH-S1')
            self.say('Candidates now:', [c['id'] for c in cands2['candidates']], 'excluded by the earlier rejection:', [(x['id'], x['condition']) for x in cands2['excluded']])
            self.expect('history shapes the candidate set', bool(cands2['excluded']) and all(x['condition'] == 'new_documents' for x in cands2['excluded']), f"{len(cands2['excluded'])} candidates held back until new documents arrive")
            imp2 = s.import_document('signals_more.csv', (HERE / 'data' / 'signals_more.csv').read_bytes(), 'examples/signal_groups/data', note='generated, labelled synthetic', date='2026-10-31')
            cands3 = s.researcher.candidates({'ledger': 'E', 'sequence': inv2['result']['seq'], 'sha256': inv2['result']['sha256']}, theme='TH-S1')
            self.expect('new rows reinstate the held-back candidates', imp2.ok and not cands3['excluded'] and [x['id'] for x in cands3['reinstated']] == [x['id'] for x in cands2['excluded']], f"reinstated {[x['id'] for x in cands3['reinstated']]}")
            sel2 = s.researcher.select({'ledger': 'E', 'sequence': inv2['result']['seq'], 'sha256': inv2['result']['sha256']}, 'finer-groups', 'the placebo is clean, so look at where the momentum relation lives', 'Is the momentum spread carried by the extremes?', theme='TH-S1')
            pr2 = s.propose(sel2.sequence); c = s.check(pr2.transition_id); d = s.decide(pr2.transition_id, 'ADMITTED', 'next'); a = s.apply(pr2.transition_id)
            self.expect('second direction checked against the history it cites', c.result == 'PASS' and a.ok and s.view()['state']['N'] == 7, f"{pr2.transition_id} check {c.result}, N={s.view()['state']['N']}")
            # 3. interruption: a third design run in its own process, killed after the host ran the tool and before the record
            docs = [x['seq'] for x in s.view()['documents']]
            d3 = s.design('Is the momentum spread carried by the extremes?', {'comparator': '>=', 'value': 50, 'minimum_n': 200, 'statement': 'top quintile beats bottom quintile by at least 50 bp'}, {'kind': 'signal-groups', 'signal': 'mom_20', 'outcome': 'fwd_5d_bp', 'groups': 5}, docs, revises=d1.sequence, theme='TH-S2')
            crashed = self.job(s.host.connection_path, d3.sequence, crash='after_execution')
            pending = s.c.obligations()['pending_attempts']
            self.expect('attempt interrupted after the host ran the tool, before the record', crashed.get('crashed') and len(pending) == 1, f"pending attempt {pending}")
        finally: s.close()
        self.say('Host closed. Reopening the run.')
        r = open_local(RUNS / self.name)
        try:
            v = r.view(); self.expect('run reopened live with its records', r.mode == 'live' and v['state']['N'] == 7 and len(v['investigations']) == 3 and v['next'][0]['op'] == 'run', f"N={v['state']['N']}, next {v['next'][0]['op']} for design E{v['next'][0]['design']}")
            resumed = self.job(r.host.connection_path, d3.sequence)
            attempts = [e for e in r.c.history('E') if e['kind'] == 'ATTEMPT' and e['actor'] == 'AD-S1.0']
            self.expect('interrupted attempt resumed without running again', resumed['status'] == 'recorded' and resumed['execution'] == 'registered' and len(attempts) == 3 and r.c.obligations()['pending_attempts'] == [], f"execution {resumed['execution']}, conclusion {resumed['conclusion']['state']}, spread {fmt(resumed['conclusion']['metric'])} bp, attempts {len(attempts)}")
            v = r.view(); self.report['state'] = {'N': v['state']['N'], 'themes': v['state']['themes'], 'budget': v['budgets']['AU-RS-1']['committed']}
        finally: r.close()
        self.report['timings']['total_s'] = round(time.monotonic() - t1, 1)
        counts = line_counts(); self.report['line_counts'] = counts['files']; self.report['line_groups'] = counts['groups']; self.report['client_analysis_lines'] = counts['client_analysis']; self.report['name'] = self.name
        g = counts['groups']; self.say('Lines:', f"script {g['script']} | experiment-specific {g['experiment']} | setup {g['setup']} | command line and job {g['command_line']} | demonstration {g['demonstration']} | client analysis module {counts['client_analysis']}")
        self.say('Timings:', self.report['timings'])
        self.report['status'] = 'PASS' if all(self.report['checks'].values()) else 'FAIL'; self.say('Result:', self.report['status'], '| new example on generated data; the calculation is the script\'s own; no forward standing.')
        return self.report


def run(argv=None):
    p = argparse.ArgumentParser(prog='examples.signal_groups.demo'); p.add_argument('--name', default=None); p.add_argument('--quiet', action='store_true'); a = p.parse_args(argv)
    report = Demo(a.name, a.quiet).run()
    if (RUNS / report['name']).exists(): (RUNS / report['name'] / 'report.json').write_text(json.dumps(report, indent=1, default=str))
    return report


if __name__ == '__main__': sys.exit(0 if run().get('status') == 'PASS' else 1)
