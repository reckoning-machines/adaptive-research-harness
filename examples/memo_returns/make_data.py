"""Write data/memos/*.md and data/returns.csv. Synthetic: six short memos with tone words, and a returns row per memo."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEMOS = {
    'm01.md': 'Q3 review. Revenue beat guidance and margins expanded. Management raised the outlook and announced a buyback.',
    'm02.md': 'Q3 review. Revenue missed guidance on weak demand. Management cut the outlook and warned on margins.',
    'm03.md': 'Q3 review. Revenue in line. Management reiterated the outlook. Backlog grew and pricing improved.',
    'm04.md': 'Q3 review. Revenue in line but margins contracted. Management lowered guidance for the fourth quarter.',
    'm05.md': 'Q3 review. Record revenue on strong demand. Management raised the full-year outlook and increased the dividend.',
    'm06.md': 'Q3 review. Revenue flat. Management reiterated guidance. No change to the outlook.',
}
RETURNS = 'memo_id,next_day_bp,prior_day_bp\nm01,120,15\nm02,-90,40\nm03,35,-20\nm04,-40,60\nm05,80,-10\nm06,5,30\n'


def main():
    (HERE / 'data' / 'memos').mkdir(parents=True, exist_ok=True)
    for name, text in MEMOS.items(): (HERE / 'data' / 'memos' / name).write_text(text + '\n')
    (HERE / 'data' / 'returns.csv').write_text(RETURNS); print(len(MEMOS), 'memos and returns.csv written')


if __name__ == '__main__': main()
