"""AD-S1.0: the researcher that runs the signal-groups analysis through ARH on the Principal's behalf.

Its decisions are the candidate table and the analysis kind every design
must name. The lifecycle, design, reserve, attempt, execution, record,
settlement, selection and proposal, is the client's AnalysisResearcher.
"""
from arh_client.analysis import AnalysisResearcher
from examples.signal_groups.candidates import RULE


class SignalResearcher(AnalysisResearcher):
    rule = RULE
    analysis_kind = 'signal-groups'
