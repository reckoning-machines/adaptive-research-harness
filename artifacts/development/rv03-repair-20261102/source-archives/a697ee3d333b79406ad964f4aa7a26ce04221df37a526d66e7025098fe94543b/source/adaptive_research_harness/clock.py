"""Durable synthetic time. No wall-clock fallback and no grant authority."""
from pathlib import Path
import os
import threading
from .encoding import canonical, decode, require, Refusal, instant


def durable_write(path, value):
    path = Path(path)
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.new')
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'wb') as f:
        f.write(canonical(value)); f.flush(); os.fsync(f.fileno())
    os.replace(temporary, path)
    fd = os.open(path.parent, os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)


class SyntheticClock:
    def __init__(self, path, config):
        self.path, self.config = Path(path), config
        self.lock=threading.RLock()
        self.journal=self.path.with_suffix(".receipts")

    def initialize(self):
        with self.lock:
            require(not self.path.exists() and not self.journal.exists(), 'CLOCK_ALREADY_EXISTS')
            self._persist(0)

    def _persist(self,tick):
        self.path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
        value={'tick':tick,'epoch':self.config['epoch']}
        with open(self.journal,'ab',buffering=0) as f:
            f.write(canonical(value)+b'\n');os.fsync(f.fileno())
        durable_write(self.path,value)

    def read(self):
        with self.lock:
            try:
                value=decode(self.path.read_bytes())
                receipts=[decode(line) for line in self.journal.read_bytes().splitlines()]
                require(bool(receipts) and value==receipts[-1], 'CLOCK_ROLLBACK')
                require(all(r['epoch']==self.config['epoch'] and type(r['tick']) is int for r in receipts),'CLOCK_UNAVAILABLE')
                require(all(a['tick']<=b['tick'] for a,b in zip(receipts,receipts[1:])), 'CLOCK_ROLLBACK')
                require(value['epoch']==self.config['epoch'] and type(value['tick']) is int and
                        0<=value['tick']<=self.config['maximum_tick'],'CLOCK_UNAVAILABLE')
            except Refusal:raise
            except (OSError,ValueError,KeyError,TypeError) as exc:raise Refusal('CLOCK_UNAVAILABLE') from exc
            return instant(value['epoch'])+value['tick']

    def advance(self,tick):
        with self.lock:
            current=self.read()-instant(self.config['epoch'])
            require(type(tick) is int and current<=tick<=self.config['maximum_tick'],'CLOCK_ROLLBACK')
            self._persist(tick)
            return self.read()
