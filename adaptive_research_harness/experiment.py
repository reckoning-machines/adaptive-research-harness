"""Experiment profile: the one place an experiment's shape is declared.

The profile is bundle data under the inventory. It names steps, tools,
tariffs, the Check cost, source rules and the genesis pair. Validation it
needs is selected by name from the closed registry below and parametrised;
a profile cannot name code, change who may act, or widen any control.
"""
from __future__ import annotations
import importlib
import importlib.util
from pathlib import Path
import re
from .encoding import fields, require, Refusal, units

EXECUTIONS = ('core', 'caller')
PROVIDER_WORK = ('ends_with_caller', 'may_outlive_caller')
KINDS = ('research', 'check')
FIELD_TYPES = {'str': str, 'int': int, 'bool': bool}
CONDITIONS = ('equals', 'at_least', 'at_most', 'greater_than', 'less_than')
IDENT = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}')


def _ident(value, code):
    require(isinstance(value, str) and IDENT.fullmatch(value) is not None, code, str(value))
    return value


def _conditions(spec):
    require(isinstance(spec, list), 'INVALID_PROFILE', 'conditions')
    for c in spec:
        fields(c, {'field'}, set(CONDITIONS))
        require(len(c) == 2, 'INVALID_PROFILE', 'one condition per clause')
    return spec


def _holds(row, conditions):
    for c in conditions:
        value = row[c['field']]
        if 'equals' in c:
            if value != c['equals']: return False
        else:
            require(type(value) is int, 'NOT_EXTRACTABLE')
            name = next(k for k in CONDITIONS if k in c); bound = c[name]
            require(type(bound) is int, 'INVALID_PROFILE', name)
            if name == 'at_least' and not value >= bound: return False
            if name == 'at_most' and not value <= bound: return False
            if name == 'greater_than' and not value > bound: return False
            if name == 'less_than' and not value < bound: return False
    return True


def row_ratio(spec, document):
    """Count rows passing the denominator filter and, of those, the numerator.

    Returns (extractable, value). Malformed rows make the whole document
    NOT_EXTRACTABLE, never a partial count.
    """
    try:
        rows = document['rows']; seen = set(); n = k = 0
        for row in rows:
            require(isinstance(row, dict), 'NOT_EXTRACTABLE')
            for name, kind in spec['row_fields'].items():
                value = row[name]
                if kind == 'str': require(isinstance(value, str), 'NOT_EXTRACTABLE')
                else: require(type(value) is FIELD_TYPES[kind], 'NOT_EXTRACTABLE')
            key = row[spec['unique']]
            require(key not in seen, 'NOT_EXTRACTABLE'); seen.add(key)
            if _holds(row, spec['denominator']):
                n += 1
                if _holds(row, spec['numerator']): k += 1
    except (Refusal, KeyError, TypeError):
        return False, None
    return n > 0, ({'numerator': k, 'denominator': n} if n > 0 else None)


VALIDATORS = {'row-ratio': row_ratio}


def _validate_extraction(spec):
    fields(spec, {'validator', 'row_fields', 'unique', 'denominator', 'numerator'})
    require(spec['validator'] in VALIDATORS, 'INVALID_PROFILE', 'validator')
    require(isinstance(spec['row_fields'], dict) and spec['row_fields'] and
            all(v in FIELD_TYPES for v in spec['row_fields'].values()), 'INVALID_PROFILE', 'row_fields')
    require(spec['unique'] in spec['row_fields'], 'INVALID_PROFILE', 'unique')
    for part in ('denominator', 'numerator'):
        for c in _conditions(spec[part]):
            require(c['field'] in spec['row_fields'], 'INVALID_PROFILE', part)


class Experiment:
    def __init__(self, data):
        fields(data, {'ExperimentId', 'version', 'genesis', 'steps', 'tools', 'sources'}, {'description'})
        self.data = data
        self.id = _ident(data['ExperimentId'], 'INVALID_PROFILE')
        require(type(data['version']) is int and data['version'] >= 1, 'INVALID_PROFILE', 'version')
        fields(data['genesis'], {'design', 'grant'}); self.genesis = data['genesis']
        self.tools = {}
        require(isinstance(data['tools'], dict) and data['tools'], 'INVALID_PROFILE', 'tools')
        for tool_id, spec in data['tools'].items():
            _ident(tool_id, 'INVALID_PROFILE')
            fields(spec, {'execution', 'module', 'callable', 'label', 'provider_work'}, {'uid'})
            require(spec['execution'] in EXECUTIONS, 'INVALID_PROFILE', tool_id)
            require(spec['provider_work'] in PROVIDER_WORK, 'INVALID_PROFILE', tool_id)
            m = spec['module']
            require(isinstance(m, str) and ((m.endswith('.py') and not m.startswith('/') and '..' not in m.split('/'))
                    or re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)+', m) is not None), 'INVALID_PROFILE', 'module')
            _ident(spec['callable'], 'INVALID_PROFILE'); _ident(spec['label'], 'INVALID_PROFILE')
            if 'uid' in spec: require(type(spec['uid']) is int, 'INVALID_PROFILE', 'uid')
            self.tools[tool_id] = spec
        labels = [s['label'] for s in self.tools.values() if s['execution'] == 'core']
        require(len(labels) == len(set(labels)), 'INVALID_PROFILE', 'duplicate core tool label')
        self.steps = {}; self.order = []
        require(isinstance(data['steps'], list) and data['steps'], 'INVALID_PROFILE', 'steps')
        for spec in data['steps']:
            fields(spec, {'name', 'kind', 'tools'}, {'inputs', 'parameters', 'input_limit_bytes', 'tariff', 'maximum'})
            name = _ident(spec['name'], 'INVALID_PROFILE'); require(name not in self.steps, 'INVALID_PROFILE', 'duplicate step')
            require(spec['kind'] in KINDS, 'INVALID_PROFILE', name)
            require(isinstance(spec['tools'], list) and all(t in self.tools for t in spec['tools']), 'INVALID_PROFILE', name)
            if spec['kind'] == 'check':
                fields(spec, {'name', 'kind', 'tools', 'maximum'}); units(spec['maximum'])
            else:
                fields(spec, {'name', 'kind', 'tools', 'inputs', 'parameters', 'input_limit_bytes', 'tariff'})
                fields(spec['inputs'], {'count', 'kind', 'form'})
                require(spec['inputs']['count'] == 1 and spec['inputs']['kind'] == 'OBSERVATION' and spec['inputs']['form'] == 'DOCUMENT',
                        'INVALID_PROFILE', 'only one DOCUMENT input is supported')
                require(isinstance(spec['parameters'], dict), 'INVALID_PROFILE', 'parameters')
                require(type(spec['input_limit_bytes']) is int and 0 < spec['input_limit_bytes'] <= 16 * 1024 * 1024, 'INVALID_PROFILE', 'input_limit_bytes')
                t = spec['tariff']; fields(t, {'measure', 'limit'}, {'bands', 'per_unit'})
                require(t['measure'] == 'rows' and type(t['limit']) is int and t['limit'] > 0, 'INVALID_PROFILE', 'tariff')
                require(('bands' in t) != ('per_unit' in t), 'INVALID_PROFILE', 'tariff needs bands or per_unit')
                if 'bands' in t:
                    require(isinstance(t['bands'], list) and t['bands'], 'INVALID_PROFILE', 'bands')
                    last = 0
                    for band in t['bands']:
                        fields(band, {'up_to', 'maximum'}); units(band['maximum'])
                        require(type(band['up_to']) is int and band['up_to'] > last, 'INVALID_PROFILE', 'bands must ascend'); last = band['up_to']
                    require(last == t['limit'], 'INVALID_PROFILE', 'last band must end at the limit')
                else: units(t['per_unit'])
            self.steps[name] = spec; self.order.append(name)
        self.sources = {}
        require(isinstance(data['sources'], dict) and data['sources'], 'INVALID_PROFILE', 'sources')
        for source_id, spec in data['sources'].items():
            _ident(source_id, 'INVALID_PROFILE')
            fields(spec, {'period_ms', 'item_id', 'window', 'document', 'extraction'})
            require(type(spec['period_ms']) is int and spec['period_ms'] > 0, 'INVALID_PROFILE', 'period_ms')
            fields(spec['item_id'], {'prefix'}); _ident(spec['item_id']['prefix'], 'INVALID_PROFILE')
            fields(spec['window'], {'start', 'end'})
            fields(spec['document'], {'synthetic', 'max_bytes'})
            require(spec['document']['synthetic'] is True, 'INVALID_PROFILE', 'only synthetic sources are supported')
            require(type(spec['document']['max_bytes']) is int and 0 < spec['document']['max_bytes'] <= 16 * 1024 * 1024, 'INVALID_PROFILE', 'max_bytes')
            _validate_extraction(spec['extraction'])
            self.sources[source_id] = spec

    def step(self, name): return self.steps.get(name)
    def steps_of(self, kind): return [n for n in self.order if self.steps[n]['kind'] == kind]
    def tool(self, tool_id):
        spec = self.tools.get(tool_id); require(spec is not None, 'TOOL_NOT_PERMITTED', str(tool_id)); return spec
    def caller_executed(self, tool_id): return self.tool(tool_id)['execution'] == 'caller'
    def core_tools(self): return {t: s for t, s in self.tools.items() if s['execution'] == 'core'}
    def core_labels(self): return [s['label'] for s in self.core_tools().values()]
    def tool_by_label(self, label):
        for t, s in self.tools.items():
            if s['label'] == label: return t
        raise Refusal('TOOL_NOT_PERMITTED', label)

    def expected_maximum(self, step, row_count):
        """Hundredths the attempt must declare, or a refusal when the input is outside the tariff."""
        t = step['tariff']; require(type(row_count) is int and 0 <= row_count <= t['limit'], 'INVALID_ESTIMATE')
        if 'bands' in t:
            return units(next(b['maximum'] for b in t['bands'] if row_count <= b['up_to']))
        return row_count * units(t['per_unit'])

    def extract(self, source_id, document):
        spec = self.sources[source_id]['extraction']
        return VALIDATORS[spec['validator']](spec, document)

    def may_outlive_caller(self, tool_id): return self.tool(tool_id)['provider_work'] == 'may_outlive_caller'
    def file_module(self, tool_id):
        """Bundle-relative path of a file module, or None for an installed package module."""
        m = self.tool(tool_id)['module']
        return ('tools/' + m) if m.endswith('.py') else None

    def load_callable(self, tool_id, bundle=None):
        """Import a tool's callable. Only a worker or the caller does this; the enforcement process never does."""
        spec = self.tool(tool_id); m = spec['module']
        if m.endswith('.py'):
            require(bundle is not None, 'INVALID_TOOL_REQUEST', 'file module needs the bundle')
            path = Path(bundle)/'tools'/m
            loader = importlib.util.spec_from_file_location('arh_tool_' + re.sub(r'[^A-Za-z0-9_]', '_', tool_id), path)
            module = importlib.util.module_from_spec(loader); loader.loader.exec_module(module)
        else: module = importlib.import_module(m)
        return getattr(module, spec['callable'])
