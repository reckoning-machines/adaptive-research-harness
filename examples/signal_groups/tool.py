"""SIGNAL-GROUPS-1: the host-run tool. The analysis function, and the one call that connects it."""
from __future__ import annotations
from arh_client.analysis import host_tool
from examples.signal_groups.signal_groups import analyze


def analysis(inputs, spec):
    """The script's calculation, unchanged. The spread between the top and bottom groups is the metric the expectation compares."""
    r = analyze(inputs.rows, spec['signal'], spec['outcome'], int(spec.get('groups', 3)))
    return dict(r, metric=r['spread_top_minus_bottom_bp'], n=r['rows_used'])


calculate = host_tool(analysis, kind='signal-groups')
