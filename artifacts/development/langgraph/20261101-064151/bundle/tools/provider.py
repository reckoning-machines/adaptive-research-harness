"""FAKE-LLM-1: a deterministic stand-in for a model provider.

It labels headlines from a fixed lexicon and charges 0.02 units per row. It
behaves like a remote provider in the ways that matter to the harness: it
keeps its own durable record of each operation keyed by the claim it was
given, answers a lookup for a claim it completed, honours a cancellation by
discarding any late completion, and counts every call durably. It never
sees returns. Crash points exist only to demonstrate interruption.
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import os
import time

BULLISH = ('beats', 'raises', 'record', 'upgrade', 'surge', 'wins', 'approval', 'expands', 'buyback')
PER_ROW_HUNDREDTHS = 2


def canonical(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
def digest(v): return hashlib.sha256(canonical(v)).hexdigest()
def amount(h): return f'{h // 100}.{h % 100:02d}'


def _durable(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True); tmp = path.with_suffix(path.suffix + '.new')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'wb') as f: f.write(canonical(value)); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def label(headline): return 'bullish' if any(w in headline.lower() for w in BULLISH) else 'bearish'


def classify(document, parameters, claim=None):
    """Pure labelling. Returns (result, actual_text). The stateful provider wraps this."""
    rows = document.get('rows')
    if not isinstance(rows, list) or len(rows) > 500: raise ValueError('INVALID_INPUT')
    labels = []; seen = set()
    for r in rows:
        if not isinstance(r, dict) or not isinstance(r.get('row_id'), str) or not isinstance(r.get('headline'), str) or r['row_id'] in seen: raise ValueError('INVALID_INPUT')
        seen.add(r['row_id']); labels.append({'row_id': r['row_id'], 'label': label(r['headline'])})
    n_bullish = sum(1 for x in labels if x['label'] == 'bullish')
    result = {'labels': labels, 'n_rows': len(rows), 'n_bullish': n_bullish, 'n_bearish': len(rows) - n_bullish, 'lexicon': parameters.get('lexicon'),
              'input_sha256': digest(document), 'synthetic': True}
    return result, amount(len(rows) * PER_ROW_HUNDREDTHS)


class FakeProvider:
    """The provider's own side: durable per-claim records, a call counter, lookup and cancellation."""
    def __init__(self, directory, crash=None):
        self.dir = Path(directory); self.dir.mkdir(parents=True, exist_ok=True); self.crash = crash
    def _record(self, attempt): return self.dir / f'attempt-{attempt}.json'
    def _cancel(self, attempt): return self.dir / f'attempt-{attempt}.cancelled'
    def calls(self):
        p = self.dir / 'calls.json'; return json.loads(p.read_bytes())['calls'] if p.exists() else 0
    def _count(self): _durable(self.dir / 'calls.json', {'calls': self.calls() + 1, 'at': int(time.time() * 1000)})
    def __call__(self, document, parameters, claim):
        """One execution for one claim. Counted before anything else, like a request that reached a provider."""
        self._count(); attempt = claim['attempt']
        try: result, actual = classify(document, parameters, claim); error = None
        except ValueError as exc: result, actual, error = None, amount(len(document.get('rows', [])) * PER_ROW_HUNDREDTHS), str(exc)
        if self.crash == 'before_provider_record': os._exit(137)
        if self._cancel(attempt).exists(): return None, actual   # cancelled before completion: discard
        _durable(self._record(attempt), {'attempt': attempt, 'input_hash': claim['input_hash'], 'result': result, 'actual': actual, 'error': error})
        if self.crash == 'after_provider_record': os._exit(137)
        if error: raise ValueError(error)
        return result, actual
    def lookup(self, attempt, input_hash):
        """The provider's record of the original operation, or None. A cancelled operation is not returned."""
        p = self._record(attempt)
        if not p.exists() or self._cancel(attempt).exists(): return None
        rec = json.loads(p.read_bytes()); return rec if rec['input_hash'] == input_hash else None
    def cancel(self, attempt, input_hash):
        """Cancel an operation. Completed work cannot be cancelled; the disposition says which."""
        rec = self.lookup(attempt, input_hash)
        if rec is not None: return {'state': 'COMPLETED', 'claim_input_hash': input_hash, 'actual': rec['actual']}
        _durable(self._cancel(attempt), {'attempt': attempt, 'input_hash': input_hash, 'cancelled_at': int(time.time() * 1000)})
        return {'state': 'CANCELLED', 'claim_input_hash': input_hash}
