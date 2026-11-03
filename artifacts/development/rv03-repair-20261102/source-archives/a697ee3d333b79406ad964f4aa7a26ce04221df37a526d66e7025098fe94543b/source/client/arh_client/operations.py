"""A durable journal of operations the caller is running against ARH, outside any graph checkpoint.

An operation is one piece of governed work with an identity the research
code gives it. Its request keys are made once and written with fsync
before the first call that uses them; every ledger reference the core
returns is written after the reply. A process that dies between a call
and the journal write leaves a key with no recorded reply, and the next
process resolves it by asking the core what became of that key before it
sends anything. The same identity resumes; a new identity is new work.
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import os
import re
import time
from .connection import Connection
from .protocol import require

KEY_NAMES = {'analysis': ('design', 'reserve', 'attempt', 'record', 'settle', 'close'),
             'call': ('reserve', 'attempt', 'record', 'settle', 'close'),
             'selection': ('select', 'propose', 'fund'),
             'retry': ('attempt', 'record', 'settle', 'close')}


def _durable(path, value):
    path = Path(path); tmp = path.with_suffix(path.suffix + '.new')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as f: f.write(json.dumps(value, sort_keys=True)); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)
    d = os.open(path.parent, os.O_RDONLY)
    try: os.fsync(d)
    finally: os.close(d)


class OperationStore:
    """One file per operation identity under a directory the caller owns."""
    def __init__(self, directory):
        self.directory = Path(directory); self.directory.mkdir(parents=True, exist_ok=True)
    def path(self, operation):
        slug = re.sub(r'[^A-Za-z0-9_.-]+', '_', operation)[:80]; return self.directory / f'{slug}-{hashlib.sha256(operation.encode()).hexdigest()[:12]}.json'
    def get(self, operation):
        p = self.path(operation); return json.loads(p.read_text()) if p.exists() else None
    def begin(self, operation, kind, **fields):
        """The journal entry for an operation, created with fresh keys if it does not exist. Existing entries are returned unchanged."""
        require(isinstance(operation, str) and operation, 'INVALID_OPERATION', 'an operation needs an identity')
        require(kind in KEY_NAMES, 'INVALID_OPERATION', kind)
        existing = self.get(operation)
        if existing is not None:
            require(existing['kind'] == kind, 'OPERATION_KIND_MISMATCH', f'{operation} is a {existing["kind"]}')
            return existing
        entry = {'operation': operation, 'kind': kind, 'keys': {k: Connection.new_key() for k in KEY_NAMES[kind]}, 'stages': {}, 'status': 'begun',
                 'created_ms': int(time.time() * 1000), **fields}
        _durable(self.path(operation), entry); return entry
    def update(self, operation, **fields):
        entry = self.get(operation); require(entry is not None, 'NO_OPERATION', operation)
        entry.update(fields); entry['updated_ms'] = int(time.time() * 1000); _durable(self.path(operation), entry); return entry
    def stage(self, operation, name, reply):
        """Record the core's reply for one stage of an operation."""
        entry = self.get(operation); require(entry is not None, 'NO_OPERATION', operation)
        entry['stages'][name] = reply; entry['updated_ms'] = int(time.time() * 1000); _durable(self.path(operation), entry); return entry
    def list(self):
        return [json.loads(p.read_text()) for p in sorted(self.directory.glob('*.json'))]


def resolve_stage(connection, entry, name, send, store=None):
    """The reply for one stage: the journal's if recorded, else the core's if the key was used, else a fresh send.

    send(key) performs the call and returns an Outcome. The reply is journaled before it is returned.
    """
    from .results import Outcome
    stages = entry.get('stages', {}); key = entry['keys'][name]
    if name in stages: return Outcome.from_reply(stages[name])
    prior = connection.outcome(key)
    if prior.get('status') in ('COMMITTED', 'REFUSED'): r = Outcome.from_reply(prior)
    else: r = send(key)
    if store is not None: store.stage(entry['operation'], name, r.raw)
    else: stages[name] = r.raw
    return r
