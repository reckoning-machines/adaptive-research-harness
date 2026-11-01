"""TONE-CALL-1: a deterministic stand-in for a model call that scores one memo's tone.

Executed by the researcher process, one attempt per memo, through
research.langgraph.call. It counts every call durably so a test can show
that a resumed node repeats none. Research code only; nothing here holds
authority.
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import os
import re

POSITIVE = ('beat', 'expanded', 'raised', 'buyback', 'grew', 'improved', 'record', 'strong', 'increased')
NEGATIVE = ('missed', 'weak', 'cut', 'warned', 'contracted', 'lowered')
PER_MEMO = '0.05'


def calls_file(): return Path(os.environ.get('MEMO_PROVIDER_DIR', '.')) / 'calls.json'


def calls():
    p = calls_file(); return json.loads(p.read_text())['calls'] if p.exists() else 0


def score(inputs, spec, claim):
    """(result, actual) for one memo. Counted before anything else, like a request that reached a provider."""
    p = calls_file(); p.parent.mkdir(parents=True, exist_ok=True); tmp = p.with_suffix('.new')
    tmp.write_text(json.dumps({'calls': calls() + 1})); os.replace(tmp, p)
    if os.environ.get('MEMO_PROVIDER_CRASH') == str(calls()): os._exit(137)   # demonstration: the process dies after the provider counted the call and before any receipt
    name, text = inputs.texts[0]; words = re.findall(r'[a-z]+', text.lower())
    pos = [w for w in words if w in POSITIVE]; neg = [w for w in words if w in NEGATIVE]
    result = {'memo': name, 'memo_id': Path(name).stem, 'tone': len(pos) - len(neg), 'positive_terms': pos, 'negative_terms': neg, 'lexicon': spec.get('lexicon'),
              'n': 1, 'input_sha256': hashlib.sha256(text.encode()).hexdigest(), 'synthetic': True}
    return result, PER_MEMO


score.kind = 'tone-call'
