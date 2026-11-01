"""Compare an outcome across signal groups in a CSV.

    python3 signal_groups.py data/signals.csv --signal mom_20 --outcome fwd_5d_bp --groups 3

Rows are sorted by the signal and split into equal groups, lowest first.
For each group the row count, the mean outcome and the hit rate (outcome
above zero) are reported, and the spread between the top and bottom group
means. Arithmetic is exact: means are integer ratios of basis points, never
floats, so the same rows always give the same bytes.
"""
from __future__ import annotations
import argparse
import csv
import sys


def ratio(numerator, denominator): return {'numerator': numerator, 'denominator': denominator}
def as_bp(r): return r['numerator'] / r['denominator'] if r['denominator'] else float('nan')


def analyze(rows, signal, outcome, groups=3):
    """rows: dicts with integer signal and outcome fields. Returns exact group statistics."""
    usable = [r for r in rows if isinstance(r.get(signal), int) and isinstance(r.get(outcome), int)]
    if groups < 2 or len(usable) < groups: raise ValueError('need at least one row per group and two groups')
    ordered = sorted(usable, key=lambda r: (r[signal], str(r.get('ticker', '')), str(r.get('date', ''))))
    size, extra = divmod(len(ordered), groups); out = []; start = 0
    for g in range(groups):
        n = size + (1 if g < extra else 0); chunk = ordered[start:start + n]; start += n
        total = sum(r[outcome] for r in chunk); hits = sum(1 for r in chunk if r[outcome] > 0)
        out.append({'group': g + 1, 'rows': n, 'signal_min': chunk[0][signal], 'signal_max': chunk[-1][signal], 'mean_bp': ratio(total, n), 'hit_rate': ratio(hits, n)})
    top, bottom = out[-1]['mean_bp'], out[0]['mean_bp']
    spread = ratio(top['numerator'] * bottom['denominator'] - bottom['numerator'] * top['denominator'], top['denominator'] * bottom['denominator'])
    return {'signal': signal, 'outcome': outcome, 'groups': out, 'rows_used': len(ordered), 'rows_skipped': len(rows) - len(ordered), 'spread_top_minus_bottom_bp': spread}


def read_csv(path):
    with open(path, newline='') as f:
        rows = []
        for r in csv.DictReader(f):
            rows.append({k: (int(v) if v.lstrip('-').isdigit() else v) for k, v in r.items()})
    return rows


def main(argv=None):
    p = argparse.ArgumentParser(); p.add_argument('csv'); p.add_argument('--signal', required=True); p.add_argument('--outcome', required=True); p.add_argument('--groups', type=int, default=3)
    a = p.parse_args(argv); result = analyze(read_csv(a.csv), a.signal, a.outcome, a.groups)
    print(f"{a.signal} -> {a.outcome}, {result['rows_used']} rows in {a.groups} groups ({result['rows_skipped']} skipped)")
    print('group  rows  signal range      mean bp   hit rate')
    for g in result['groups']:
        print(f"{g['group']:>5}  {g['rows']:>4}  {g['signal_min']:>6} .. {g['signal_max']:<6}  {as_bp(g['mean_bp']):>8.1f}   {as_bp(g['hit_rate']):>5.2f}")
    print(f"spread top minus bottom: {as_bp(result['spread_top_minus_bottom_bp']):.1f} bp")
    return 0


if __name__ == '__main__': sys.exit(main())
