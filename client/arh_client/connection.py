"""One actor's authenticated connection to the host."""
from __future__ import annotations
from pathlib import Path
import os
import uuid
from .protocol import request, decode, HarnessError, require
from .results import Outcome, Ref


class Connection:
    """An authenticated channel for one actor. Obtain one with connect()."""
    def __init__(self, socket_path, actor: str, token: str, info: dict | None = None):
        self.path = str(socket_path); self.actor = actor; self.token = token; self.info = info or {}; self._profile = None

    @classmethod
    def from_file(cls, connection_path, actor: str) -> 'Connection':
        info = decode(Path(connection_path).read_bytes())
        require(actor in info['tokens'], 'UNKNOWN_ACTOR', f"{actor} is not one of {sorted(info['tokens'])}")
        return cls(info['socket'], actor, info['tokens'][actor], info)

    @staticmethod
    def new_key() -> str:
        """A fresh request key. Persist it before use; re-sending a command with the same key returns the original Outcome."""
        return str(uuid.uuid4())

    # ----- commands -----
    def call(self, op: str, payload: dict | None = None, key: str | None = None) -> Outcome:
        """Send one command. Returns the core's Outcome; raises HarnessError on operational failure."""
        return Outcome.from_reply(self._send(op, payload, key))
    def call_or_raise(self, op: str, payload: dict | None = None, key: str | None = None) -> Outcome:
        return self.call(op, payload, key).raise_for_refusal()
    def outcome(self, key: str) -> dict:
        """What became of a command whose reply was lost: status COMMITTED, REFUSED, PARTIAL or UNKNOWN from the core's durable receipts."""
        return self.query('inspect-request', {'request_id': key})

    # ----- reads -----
    def query(self, op: str, payload: dict | None = None) -> dict:
        reply = self._send(op, payload, None)
        if reply.get('status') == 'ERROR': raise HarnessError(reply['reason'], reply.get('detail', ''))
        return reply
    def profile(self) -> dict:
        """The frozen bundle: setup, artifacts, experiment profile and inventory. Cached; it cannot change while the host runs."""
        if self._profile is None: self._profile = self.query('profile')
        return self._profile
    def experiment(self) -> dict: return self.profile()['experiment']
    def state(self) -> dict:
        """Applied head N, designs, grants, active grants, themes, hypotheses, limits and suspensions."""
        return self.query('state')
    def clock(self) -> dict: return self.query('clock')
    def closure(self) -> dict:
        """Both ledgers in full at the current instant: the committed closure a Checker or researcher reasons from."""
        return self.query('closure')
    def budget(self, grant: str) -> dict:
        """committed, reserved, headroom, spendable and overspent for one grant, as unit strings."""
        return self.query('budget', {'grant': grant})
    def obligations(self) -> dict:
        """Pending attempts, binding states and decided-but-unapplied transitions."""
        return self.query('obligations')
    def get(self, ref: Ref | dict) -> dict:
        """One exact record by reference; refused if the hash does not match."""
        return self.query('get', {'ref': ref.as_dict() if isinstance(ref, Ref) else {k: v for k, v in ref.items() if k != 'raw_sha256'}})
    def history(self, ledger: str) -> list[dict]:
        """Every record of ledger 'E' or 'T', in sequence."""
        out = []; after = 0; through = None
        while True:
            p = {'ledger': ledger, 'after': after, 'limit': 1000}
            if through is not None: p['through'] = through
            page = self.query('history', p); out += page['records']; through = page['through']; after = page['next_after']
            if after >= through or not page['records']: return out
    def record(self, ledger: str, sequence: int) -> dict:
        for e in self.history(ledger):
            if e['seq'] == sequence: return e
        raise HarnessError('NO_RECORD', f'{ledger}{sequence}')

    def _send(self, op, payload, key):
        return request(self.path, {'actor': self.actor, 'op': op, 'payload': payload or {}, 'request_id': key or self.new_key(), 'token': self.token, 'pid': os.getpid()})


def connect(connection_file, actor: str) -> Connection:
    """Open a connection for one actor named in the host's connection file."""
    return Connection.from_file(connection_file, actor)
