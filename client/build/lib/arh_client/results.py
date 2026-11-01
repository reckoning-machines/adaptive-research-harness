"""Structured results: a Ref names a ledger record; an Outcome is the core's answer to a command."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .protocol import HarnessError


@dataclass(frozen=True)
class Ref:
    """An exact ledger record: ledger 'E' (Evidence) or 'T' (Transition), its sequence and content hash."""
    ledger: str
    sequence: int
    sha256: str
    raw_sha256: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> 'Ref': return cls(d['ledger'], d['sequence'], d['sha256'], d.get('raw_sha256'))
    def as_dict(self) -> dict:
        d = {'ledger': self.ledger, 'sequence': self.sequence, 'sha256': self.sha256}
        if self.raw_sha256: d['raw_sha256'] = self.raw_sha256
        return d
    def __str__(self): return f'{self.ledger}{self.sequence}'


@dataclass
class Outcome:
    """What the core did with a command.

    status is 'COMMITTED' or 'REFUSED'. A refusal is a governed decision, not an
    error: reason names the rule, detail explains it, and refs name the
    preserved refusal records. A transport or server failure raises
    HarnessError instead and never produces an Outcome.
    """
    status: str
    reason: str | None = None
    detail: str | None = None
    refs: list[Ref] = field(default_factory=list)
    raw: dict = field(default_factory=dict)
    input_hash: str | None = None
    transition_id: str | None = None

    @classmethod
    def from_reply(cls, reply: dict) -> 'Outcome':
        if reply.get('status') == 'ERROR': raise HarnessError(reply.get('reason', 'OPERATIONAL_ERROR'), reply.get('detail', ''))
        return cls(status=reply.get('status', 'UNKNOWN'), reason=reply.get('reason'), detail=reply.get('detail'),
                   refs=[Ref.from_dict(r) for r in reply.get('refs', [])], raw=reply)
    @property
    def ok(self) -> bool: return self.status == 'COMMITTED'
    @property
    def ref(self) -> Ref | None: return self.refs[0] if self.refs else None
    @property
    def sequence(self) -> int | None: return self.refs[0].sequence if self.refs else None
    def raise_for_refusal(self) -> 'Outcome':
        if not self.ok: raise RefusedError(self)
        return self
    def __str__(self): return self.status + (f' {self.reason}' if self.reason else '') + (f' ({self.detail})' if self.detail else '')


class RefusedError(HarnessError):
    """Raised by the *_or_raise conveniences when a governed decision was a refusal. Carries the Outcome."""
    def __init__(self, outcome: Outcome):
        super().__init__(outcome.reason or outcome.status, outcome.detail or ''); self.outcome = outcome
