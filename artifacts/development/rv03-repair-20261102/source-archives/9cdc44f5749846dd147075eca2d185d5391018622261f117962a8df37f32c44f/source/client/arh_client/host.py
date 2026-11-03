"""Control of a running local host over its control socket, with the Principal token."""
from __future__ import annotations
from pathlib import Path
from .protocol import request, decode, HarnessError, require


class HostControl:
    def __init__(self, control_path, token, info=None): self.path = str(control_path); self.token = token; self.info = info or {}
    @classmethod
    def from_file(cls, connection_path):
        info = decode(Path(connection_path).read_bytes()); return cls(info['control'], info['tokens']['Principal'], info)
    def call(self, op, **fields):
        r = request(self.path, dict(fields, op=op, token=self.token))
        if r.get('status') == 'ERROR': raise HarnessError(r['reason'], r.get('detail', ''))
        return r
    def tick(self, tick): return self.call('tick', tick=tick)
    def status(self): return self.call('status')
    def quiesce(self, generation, provider_dispositions=None):
        """Record that a caller generation is gone, with any provider dispositions established for its claims."""
        return self.call('quiesce', generation=generation, provider_dispositions=provider_dispositions or {})
    def stop(self): return self.call('stop')
    def generation(self, pid): return {'pid': pid, 'run': self.info['run_id']}
