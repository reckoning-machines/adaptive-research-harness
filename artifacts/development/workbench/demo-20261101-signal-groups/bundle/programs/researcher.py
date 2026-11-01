"""AD-S1.0: the researcher that runs the signal-groups analysis through ARH on the Principal's behalf.

Its decisions are the candidate table and the analysis kind every design
must name. The lifecycle, design, reserve, attempt, execution, record,
settlement, selection and proposal, is the client's AnalysisResearcher.
The entry point is a function; no subclass is needed.
"""
from arh_client.analysis import AnalysisResearcher
from examples.signal_groups.candidates import RULE


def researcher(connection): return AnalysisResearcher(connection, rule=RULE, analysis_kind='signal-groups')


SignalResearcher = researcher   # the earlier name, kept for the retained runs that cite it
