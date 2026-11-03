"""A project: one experiment directory described by project.json, its identities, analyses, sources and budgets by name.

The description is administrative. Amounts in it become authoritative only
when the Principal signs the grants at startup. Nothing here holds
authority.
"""
from __future__ import annotations
from pathlib import Path
import json
from .protocol import require
from .setup import write_setup, identities, FILES

FILE = 'project.json'
ROLES = {'researcher': 'researcher', 'checker': 'checker', 'principal': 'Principal', 'observer': 'Observation function'}


class Project:
    def __init__(self, directory, data):
        self.directory = Path(directory).resolve(); self.data = data; self.ids = identities(data)
    @classmethod
    def load(cls, directory):
        directory = Path(directory); p = directory / FILE; require(p.is_file(), 'NO_PROJECT', f'{FILE} not found in {directory}')
        return cls(directory, json.loads(p.read_bytes()))
    @property
    def name(self): return self.data.get('project', self.data['experiment_id'].lower())
    @property
    def sources(self): return self.data['sources']
    @property
    def analyses(self): return self.data['analyses']
    @property
    def theme(self): return self.ids['theme']
    def setup_exists(self): return all((self.directory / f).is_file() for f in FILES)
    def write_setup(self): return write_setup(self.directory, self.data)

    def analysis(self, what):
        """The analysis entry for a tool id, an analysis kind, or a function carrying .kind from host_tool."""
        kind = getattr(what, 'kind', None) or what
        for a in self.analyses:
            if a['id'] == kind or a.get('kind') == kind: return a
        raise_ = require(False, 'ANALYSIS_NOT_DECLARED', f'{kind} is not an analysis in {FILE}')
    def tool_id(self, what): return self.analysis(what)['id']

    def budget(self, name=None):
        """The purpose a named budget funds, defaulting to the umbrella Theme."""
        default = {'kind': 'Theme', 'id': self.theme}
        if name is None: return {'name': None, 'purpose': default}
        budgets = self.data.get('budgets', {}); require(name in budgets, 'BUDGET_NOT_DECLARED', f'{name} is not a budget in {FILE}')
        entry = budgets[name] if isinstance(budgets[name], dict) else {}
        return {'name': name, 'purpose': entry.get('purpose', default), 'proposal_budget': entry.get('proposal_budget', '1.00')}

    def actor(self, role):
        require(role in ROLES, 'INVALID_ROLE', role)
        return {'researcher': self.ids['researcher'], 'checker': self.ids['checker']}.get(role, ROLES[role])

    @staticmethod
    def connection_file(run):
        run = Path(run); return run if run.is_file() else run / 'state' / 'connection.json'
    def connect(self, role, run):
        from .connection import connect
        return connect(self.connection_file(run), self.actor(role))
