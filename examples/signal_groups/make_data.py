"""Generate data/signals.csv deterministically. Synthetic: a weak relation between a signal and a forward return, plus noise."""
from pathlib import Path
import csv
import random

HERE = Path(__file__).resolve().parent


def generate(seed, tickers, days, month):
    rng = random.Random(seed); rows = []
    for d in range(days):
        date = f'2026-{month:02d}-{d + 1:02d}'
        for t in range(tickers):
            mom = rng.randint(-300, 300)
            fwd = int(0.12 * mom + rng.gauss(0, 90))
            rows.append({'date': date, 'ticker': f'T{t + 1:02d}', 'mom_20': mom, 'fwd_5d_bp': fwd, 'fwd_20d_bp': int(0.05 * mom + rng.gauss(0, 160)), 'vol_60': rng.randint(80, 320)})
    return rows


def write(name, rows):
    with open(HERE / 'data' / name, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(name, len(rows), 'rows')


def main():
    write('signals.csv', generate(20261101, 12, 20, 9)); write('signals_more.csv', generate(20261102, 12, 20, 10))


if __name__ == '__main__': main()
