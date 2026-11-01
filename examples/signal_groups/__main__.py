"""Your own CSV through ARH: the expectation recorded first, the analysis run by the host, the next question chosen from the evidence.

    python3 -m examples.signal_groups --csv FILE --signal COL --outcome COL --expect ">= 50" [--groups 3] [--minimum-n 1] [--origin TEXT] [--date YYYY-MM-DD] [--question TEXT] [--statement TEXT] [--name RUN]
    python3 -m examples.signal_groups --run RUN [--csv FILE] --signal COL --outcome COL --expect ">= 50" [--revises SEQ]
    python3 -m examples.signal_groups --run RUN --choose CANDIDATE --reason TEXT --next QUESTION
    python3 -m examples.signal_groups --run RUN --admit TR-... [--reason TEXT]
    python3 -m examples.signal_groups --run RUN --reject TR-... --reason TEXT
    python3 -m examples.signal_groups --run RUN

The first form creates a run whose source is your own files, declared
historical, writes its setup into the run directory, imports the file with
the origin you give (default, its path), records the question and the
expectation as a design, lets the host run the analysis and prints the
result, the conclusion and the candidates for the next investigation. The
later forms continue the same run. Every step is one client operation the
core admits or refuses. Records are under artifacts/development/workbench/RUN
and the run opens on the workbench's local page. The demonstration on
generated data is demo.py.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import re
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'client')); sys.path.insert(0, str(ROOT))
from arh_client.analysis import COMPARATORS
from workbench.local_session import LocalRun, open_local, RUNS
from examples.signal_groups.make_setup import own_setup
from examples.signal_groups.signal_groups import as_bp

PROG = 'python3 -m examples.signal_groups'


def parse_expect(text):
    """'>= 50' or '< 25' or '>= 1/2'. Values are integers or exact ratios."""
    op, _, value = text.strip().partition(' '); value = value.strip()
    if op not in COMPARATORS or not value: raise SystemExit(f'--expect takes a comparator and a value, for example ">= 50"; got {text!r}')
    if '/' in value:
        a, b = value.split('/', 1); return op, {'numerator': int(a), 'denominator': int(b)}
    return op, int(value)


def fmt(m): return f'{as_bp(m):.1f}' if isinstance(m, dict) else str(m)


def current_theme(s):
    themes = s.view()['state']['themes']
    return max(themes, key=lambda t: int(re.search(r'(\d+)$', t).group(1)))


def show(s, out):
    v = s.view(); out('Run', v['run'], '| N =', v['state']['N'], '| direction', current_theme(s), '| documents', len(v['documents']), '| pending attempts', v['pending_attempts'])
    for d in v['documents']: out(f"  E{d['seq']} {d['name']} {d['rows']} rows, class {d['class']}, origin {d['origin']}")
    for i in v['investigations']:
        e = i['expectation']; out(f"  design E{i['design']['seq']} [{i['theme']}] {i['question']} | expect {e['comparator']} {fmt(e['value'])} bp, min n {e.get('minimum_n', 1)}" + (f" | revises E{i['revises']}" if i.get('revises') else ''))
        r = i.get('result')
        if r: out(f"    result E{r['seq']} spread {fmt(r['metric'])} bp over {r['n']} rows, conclusion {r['conclusion']['state'] if r.get('conclusion') else r.get('failure')}, settled {r['settled']}")
        if i.get('selection'): out(f"    selection E{i['selection']['seq']} chose {i['selection']['chosen']}: {i['selection']['reason']} | next: {i['selection']['next_question']}")
        if i.get('proposal'):
            p = i['proposal']; out(f"    proposal {p['transition_id']} {p['theme']} | checks {[c['result'] for c in p['checks']]} | decision {p['decision']['decision'] if p['decision'] else None} | applied {bool(p['applied'])}")
    for n in v['next']: out(f"  next: {n['label']} ({n['op']}, {n['actor']})")
    return v


def main(argv=None):
    p = argparse.ArgumentParser(prog=PROG, description=__doc__.split('\n\n')[1], formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--run', help='continue this run'); p.add_argument('--name', help='name for a new run')
    p.add_argument('--csv', action='append', help='a CSV to import as a historical document; repeatable'); p.add_argument('--origin', help='where the file came from; default, its path'); p.add_argument('--date', help='YYYY-MM-DD the file was received; default, today')
    p.add_argument('--signal'); p.add_argument('--outcome'); p.add_argument('--groups', type=int, default=3); p.add_argument('--expect', help='comparator and value for the top-minus-bottom spread in bp, for example ">= 50"')
    p.add_argument('--minimum-n', type=int, default=1); p.add_argument('--question'); p.add_argument('--statement', help='the expectation in your words'); p.add_argument('--revises', type=int, help='design sequence this one revises')
    p.add_argument('--choose', help='candidate id'); p.add_argument('--reason'); p.add_argument('--next', help='the next question, in your words')
    p.add_argument('--admit', help='transition id'); p.add_argument('--reject', help='transition id'); p.add_argument('--budget', default='100.00', help='research budget units for a new run')
    p.add_argument('--quiet', action='store_true')
    a = p.parse_args(argv); lines = []; report = {}
    def out(*parts):
        line = ' '.join(str(x) for x in parts); lines.append(line)
        if not a.quiet: print(line, flush=True)
    designing = bool(a.signal or a.outcome or a.expect)
    if designing and not (a.signal and a.outcome and a.expect): raise SystemExit('--signal, --outcome and --expect go together')
    t0 = time.monotonic()
    if a.run:
        s = open_local(RUNS / a.run)
        if s.mode != 'live': out('Run', a.run, 'is read-only:', s.reason); report['mode'] = 'read-only'; return dict(report, lines=lines, status='READ_ONLY')
    else:
        if not (a.csv and designing): raise SystemExit(f'a new run needs --csv, --signal, --outcome and --expect; or give --run NAME to continue one. See {PROG} --help')
        name = a.name or time.strftime('%Y%m%d-%H%M%S') + '-signal-own'; question = a.question or f'Does {a.signal} separate {a.outcome} across {a.groups} groups?'
        own_setup(RUNS / name / 'setup', budget=a.budget)
        s = LocalRun.create(f'# Charter\n{question}\n', name, setup=RUNS / name / 'setup')
        out('Created run', name, f'in {time.monotonic() - t0:.1f} s; source declared historical; budget', a.budget, 'units')
    report['run'] = s.run_dir.name
    try:
        for path in a.csv or []:
            path = Path(path); raw = path.read_bytes(); origin = a.origin or str(path.resolve()); date = a.date or time.strftime('%Y-%m-%d', time.gmtime())
            o = s.import_document(path.name, raw, origin, note='imported by the signal-groups command line', date=date)
            if not o.ok: out('Import refused:', o.reason, o.detail); report['import'] = o.reason; return dict(report, lines=lines, status='REFUSED')
            d = s.view()['documents'][-1]; out(f"Imported {d['name']} as E{d['seq']}: {d['rows']} rows, class {d['class']}, sha256 {d['file_sha256'][:16]}, origin {d['origin']}")
        if designing:
            op, value = parse_expect(a.expect); theme = current_theme(s)
            expectation = {'comparator': op, 'value': value, 'minimum_n': a.minimum_n, 'statement': a.statement or f'{a.signal} top group minus bottom group of {a.outcome} {op} {fmt(value)} bp'}
            question = a.question or f'Does {a.signal} separate {a.outcome} across {a.groups} groups?'
            docs = [d['seq'] for d in s.view()['documents']]
            if not docs: out('No documents in the run; give --csv'); return dict(report, lines=lines, status='NO_DOCUMENTS')
            d = s.design(question, expectation, {'kind': 'signal-groups', 'signal': a.signal, 'outcome': a.outcome, 'groups': a.groups}, docs, revises=a.revises, theme=theme)
            if not d.ok: out('Design refused:', d.reason, d.detail); return dict(report, lines=lines, status='REFUSED')
            out(f'Recorded design E{d.sequence} under {theme} before any attempt: {question} Expectation: {expectation["statement"]}, min n {a.minimum_n}')
            r = s.run(d.sequence); report['design'] = d.sequence; report['run_status'] = r['status']
            if r['status'] != 'recorded': out('Run did not record:', r['status'], r.get('reason')); return dict(report, lines=lines, status=r['status'].upper())
            c = r['conclusion']; res = r['record']; rec = s.c.get(res.ref)['body']['result']; report['conclusion'] = c['state']; report['metric'] = c['metric']
            out(f"Host ran the analysis, execution {r['execution']}, settled {r['settlement'].ok}, record E{res.sequence}")
            out('group  rows  signal range      mean bp   hit rate')
            for g in rec['groups']: out(f"{g['group']:>5}  {g['rows']:>4}  {g['signal_min']:>6} .. {g['signal_max']:<6}  {as_bp(g['mean_bp']):>8.1f}   {as_bp(g['hit_rate']):>5.2f}")
            out(f"spread top minus bottom: {fmt(c['metric'])} bp over {c['n']} rows ({rec['rows_skipped']} skipped) | conclusion {c['state']}")
            cands = s.researcher.candidates({'ledger': 'E', 'sequence': res.sequence, 'sha256': s.c.get(res.ref)['sha256']}, theme=theme); report['candidates'] = [x['id'] for x in cands['candidates']]
            out('Candidates for the next investigation, by the declared rule:')
            for x in cands['candidates']: out(f"  {x['id']}: {x['question']} ({x['why']})")
            for x in cands['excluded']: out(f"  held back: {x['id']}, rejected in E{x['rejected_in']}, until {x['condition']}")
            for x in cands['reinstated']: out(f"  back in: {x['id']}, rejected in E{x['rejected_in']}, condition {x['condition']} met")
            out(f'Choose one: {PROG} --run {s.run_dir.name} --choose ID --reason "why" --next "the next question"')
        if a.choose:
            if not (a.reason and a.next): raise SystemExit('--choose needs --reason and --next')
            v = s.view(); open_sel = [n for n in v['next'] if n['op'] == 'select']
            if not open_sel: out('No analysis awaits a selection.'); return dict(report, lines=lines, status='NOTHING_TO_SELECT')
            seq = open_sel[-1]['analysis']; theme = current_theme(s)
            sel = s.researcher.select({'ledger': 'E', 'sequence': seq, 'sha256': s.c.record('E', seq)['sha256']}, a.choose, a.reason, a.next, theme=theme)
            if not sel.ok: out('Selection refused:', sel.reason, sel.detail); return dict(report, lines=lines, status='REFUSED')
            rej = s.c.get(sel.ref)['body']['result']['rejections']; out(f"Recorded selection E{sel.sequence}: {a.choose}; rejected " + ', '.join(f"{x['id']} (until {x['reconsider_when']})" for x in rej))
            pr = s.propose(sel.sequence)
            if not pr.ok: out('Proposal refused:', pr.reason, pr.detail); return dict(report, lines=lines, status='REFUSED')
            c = s.check(pr.transition_id); report['transition'] = pr.transition_id; report['check'] = c.result
            out(f"Proposed {pr.transition_id} as the next direction; independent check {c.result}" + ('' if c.result == 'PASS' else f" not met {[k for k, v in (c.criteria or {}).items() if v != 'MET']}"))
            out(f'Decide: {PROG} --run {s.run_dir.name} --admit {pr.transition_id}   or   --reject {pr.transition_id} --reason "why"')
        if a.admit or a.reject:
            tr = a.admit or a.reject; decision = 'ADMITTED' if a.admit else 'REJECTED'
            d = s.decide(tr, decision, a.reason or 'Principal decision'); report['decision'] = decision if d.ok else d.reason
            if not d.ok: out('Decision refused:', d.reason, d.detail); return dict(report, lines=lines, status='REFUSED')
            if a.admit:
                ap = s.apply(tr); report['applied'] = ap.ok; out(f"{tr} admitted and applied: {ap.ok}; N = {s.view()['state']['N']}; direction now {current_theme(s)}")
            else: out(f'{tr} rejected; the proposal and the check stay on the record')
        v = show(s, out); report['N'] = v['state']['N']; report['documents'] = [{'seq': d['seq'], 'class': d['class'], 'origin': d['origin']} for d in v['documents']]
    finally: s.close()
    out(f'Done in {time.monotonic() - t0:.1f} s. Records: {s.run_dir.relative_to(ROOT)}')
    return dict(report, lines=lines, status='OK', seconds=round(time.monotonic() - t0, 1))


if __name__ == '__main__': sys.exit(0 if main().get('status') == 'OK' else 1)
