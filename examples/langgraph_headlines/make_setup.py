"""Generate setup.json, designs_and_methods.json and experiment.json for the headline experiment.

Run once from this directory's parent or anywhere: python3 -m examples.langgraph_headlines.make_setup
Hashes are computed here so that the declared artifacts are exact.
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
CV1 = 'c56a9cf50a7e9efadad8f2f2be6605e82c758f18d4096ba07eaaf86a8f8b7a64'
EXPIRY = '2027-04-30T00:00:00.000Z'
BULLISH = ['beats', 'raises', 'record', 'upgrade', 'surge', 'wins', 'approval', 'expands', 'buyback']


def canonical(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
def digest(v): return hashlib.sha256(canonical(v)).hexdigest()
def write(name, value): (HERE / name).write_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=1).encode() + b'\n')


HEADLINES = [
    ('h01', 'Acme beats estimates and raises full-year guidance', 180), ('h02', 'Borealis posts record quarterly revenue', 95),
    ('h03', 'Cobalt Mining wins supply contract with carmaker', 60), ('h04', 'Delta Pharma receives regulatory approval for new drug', 240),
    ('h05', 'Evergreen expands into two new markets', 40), ('h06', 'Falcon Air announces share buyback', 70),
    ('h07', 'Granite Bank upgrade from regional broker', -35), ('h08', 'Helios Solar output surge on new plant', 110),
    ('h09', 'Indigo Retail beats on margins, raises dividend', 85), ('h10', 'Juniper Software wins government tender', -20),
    ('h11', 'Kestrel Energy record output in the quarter', 55), ('h12', 'Lumen Media approval for merger clears', -15),
    ('h13', 'Meridian cuts outlook on weak demand', -140), ('h14', 'Nimbus Cloud misses revenue estimates', -90),
    ('h15', 'Orion Steel warns of plant closure', -60), ('h16', 'Pinnacle Foods recalls product line', -30),
    ('h17', 'Quartz Semis delays chip launch', 25), ('h18', 'Redwood Timber suspends dividend', -75),
    ('h19', 'Sable Shipping reports loss on fuel costs', -45), ('h20', 'Tundra Telecom loses key customer', 10),
    ('h21', 'Umber Chemicals faces lawsuit over spill', -55), ('h22', 'Vega Motors recalls vehicles', 30),
    ('h23', 'Willow Health downgrades growth forecast', -20), ('h24', 'Xenon Labs halts trial after side effects', 50),
]


def main():
    headline_rows = [{'row_id': r, 'headline': h} for r, h, _ in HEADLINES]
    return_rows = [{'row_id': r, 'next_day_return_bp': bp} for r, _, bp in HEADLINES]
    formation = {'item_id': 'headlines-2026-10-28', 'period_start': '2026-10-28T00:00:00.000Z', 'period_end': '2026-10-29T00:00:00.000Z',
                 'claimed_publication_time': '2026-10-29T00:00:00.000Z', 'synthetic': True, 'rows': headline_rows}
    returns = {'item_id': 'returns-2026-10-29', 'period_start': '2026-10-29T00:00:00.000Z', 'period_end': '2026-10-30T00:00:00.000Z',
               'claimed_publication_time': '2026-10-30T00:00:00.000Z', 'synthetic': True, 'rows': return_rows}
    news_source = {'SourceId': 'SRC-NEWS-SYN', 'provider': 'Local deterministic headline fixture in this example; not a news vendor', 'dataset': 'Daily synthetic headline cohort documents',
                   'field': 'well_formed_rows', 'field_definition': 'Rows with a unique string row_id and a string headline over all listed rows.', 'unit': 'dimensionless exact numerator/denominator pair',
                   'print_rule': 'FIRST_RELEASE', 'claimed_time_field': 'claimed_publication_time', 'resolution_grace_ms': 600000, 'endpoint': 'synthetic://SRC-NEWS-SYN/headlines/{period_date}',
                   'access_method': 'Local fixture lookup; no network', 'parsing': 'Strict JSON; rows with row_id and headline; unique row_id; exact period and item binding.',
                   'extraction_rule': 'Count well-formed rows over listed rows; malformed bytes => NOT_EXTRACTABLE. Headlines carry no outcome.', 'source_kind': 'DOCUMENT_FEED',
                   'structural_availability_bound': 'Released no earlier than period_end within the simulated source contract.', 'synthetic': True,
                   'enumeration_contract': {'complete_set': 'Exactly the headline item for each declared period_date whose period_end <= current synthetic time.', 'completeness': 'COMPLETE requires a successful full listing.',
                                            'item_identity': 'headlines-YYYY-MM-DD, one FIRST_RELEASE document per period; differing bytes are a new Observation.', 'window': 'One UTC daily period per retrieval; 2026-10-28 through 2027-04-29.'}}
    ret_source = {'SourceId': 'SRC-RET-SYN', 'provider': 'Local deterministic return fixture in this example; not a market', 'dataset': 'Next-day synthetic returns in basis points per headline row',
                  'field': 'positive_return_fraction', 'field_definition': 'Rows with next_day_return_bp > 0 over all listed rows.', 'unit': 'dimensionless exact numerator/denominator pair',
                  'print_rule': 'FIRST_RELEASE', 'claimed_time_field': 'claimed_publication_time', 'resolution_grace_ms': 600000, 'endpoint': 'synthetic://SRC-RET-SYN/returns/{period_date}',
                  'access_method': 'Local fixture lookup; no network', 'parsing': 'Strict JSON; rows with row_id and integer next_day_return_bp; unique row_id.',
                  'extraction_rule': 'Count rows with next_day_return_bp > 0 over listed rows; malformed bytes => NOT_EXTRACTABLE. Published one period after the headlines it scores.', 'source_kind': 'DOCUMENT_FEED',
                  'structural_availability_bound': 'Released no earlier than period_end within the simulated source contract; never before the headline period it scores has ended.', 'synthetic': True,
                  'enumeration_contract': {'complete_set': 'Exactly the returns item for each declared period_date whose period_end <= current synthetic time.', 'completeness': 'COMPLETE requires a successful full listing.',
                                           'item_identity': 'returns-YYYY-MM-DD, one FIRST_RELEASE document per period.', 'window': 'One UTC daily period per retrieval; 2026-10-29 through 2027-04-30.'}}
    tools = {
        'FAKE-LLM-1': {'content': {'kind': 'deterministic synthetic classifier standing in for a model provider', 'version': 1,
                                   'algorithm': 'Label each headline bullish when it contains a word from the fixed lexicon ' + ', '.join(BULLISH) + ', otherwise bearish. Return labels, counts, input SHA-256 and synthetic=true. Receives headlines only; never sees returns.',
                                   'cost': '0.02 units per row, charged on the row count of the admitted input; 500 rows maximum.',
                                   'inputs': 'Exact canonical headline DOCUMENT bytes from committed closure.', 'failure': 'Invalid shape returns failure with diagnostic and the same charge.',
                                   'provider_work': 'Declared as able to outlive its caller, as a remote provider would; keeps its own record per claim, answers lookup, honours cancellation.'}},
        'CHECK-H-1': {'content': {'kind': 'deterministic Checker', 'version': 1, 'algorithm': 'Common and class criteria through the client checking toolkit; HYPOTHESIS recomputation joins the recorded labels to the committed returns and recounts. Verifies arithmetic and join, not labels.',
                                  'cost': '0.25 units per full Check attempt including a failing or incomplete Check; zero external billing.', 'input_limit_bytes': 33554432}},
    }
    for t in tools.values(): t['content_sha256'] = digest(t['content'])
    methods = {
        'MC-RESEARCH-H1': {'content': {'version': 1, 'meaning': 'Contribution report only; no standing or grant.', 'forward_contribution': 'Count distinct registrations with their own finalized forward Outcomes; synthetic count is zero. Divide by settled actual research units; zero denominator NOT_ESTIMABLE.', 'limits': 'No profitability credit; no statistical claim from synthetic counts.'}},
        'MC-CHECKER-H1': {'content': {'version': 1, 'meaning': 'Verification contribution, not permission.', 'measure': 'Defects later established in passed subjects and refusals later shown unwarranted, with exact references, divided by settled Checker units.', 'limits': 'Absence of a later defect finding is not proof of correctness.'}},
        'MC-HYPOTHESIS-H1': {'content': {'version': 1, 'scoring': 'Binary target; hit = 1 when prediction equals resolved target; tolerance 0.', 'effective_observations': 'One headline row is one raw observation; rows sharing a row_id prefix letter are clustered; N_eff is the number of clusters.',
                                         'falsifier': 'Registered success probability p>=3/5 is contradicted only if the exact one-sided Binomial(n,3/5) lower-tail probability of observed successes is <=0.05 after the family adjustment.', 'multiplicity': 'Compare the nominal one-sided p-value to 0.05/T_total over every recorded trial.',
                                         'predictive_check': 'Before each scoring window commit Bernoulli(p=3/5) as the working predictive model; central 0.95 interval.', 'stopping_rule': 'Review after 12 effective finalized forward Outcomes; no standing conclusion before the CV1 floor or from synthetic records.', 'limits': 'Illustrative scientific choices, not constitutional constants.'}},
    }
    for m in methods.values(): m['content_sha256'] = digest(m['content'])
    resolution_rule = {'version': 1, 'algorithm': 'For the resolution period, take the committed headline document of the preceding period and the committed returns document of the resolution period; label headlines with FAKE-LLM-1 under the registered lexicon; join labels to returns by row_id; target is 1 iff 5*k_bullish_up >= 3*n_bullish with n_bullish>0, otherwise 0. A missing member cannot be substituted.',
                       'input_fields': ['n_bullish', 'k_bullish_up'], 'missing_member': 'Unresolved; no alternative print, imputation or substitution.'}
    template = {'template_id': 'HEAD-H1', 'HypothesisId': 'HY-HEAD-1.0', 'HypothesisLineageId': 'HY-HEAD-1', 'SearchFamily': 'SF-HEAD', 'predecessor': None,
                'observable': 'Binary predicate over the fraction of bullish-labelled headlines followed by a positive next-day return',
                'statement': 'In the next synthetic daily headline cohort, at least three in five headlines labelled bullish by FAKE-LLM-1 are followed by a positive next-day return.',
                'falsifier': methods['MC-HYPOTHESIS-H1']['content']['falsifier'], 'horizon': 'One UTC day per target; first resolution member fixed below. No predictions are executed in this milestone.',
                'stopping_rule': methods['MC-HYPOTHESIS-H1']['content']['stopping_rule'], 'tolerance': '0', 'print': 'FIRST_RELEASE',
                'resolution_source': 'SRC-RET-SYN', 'resolution_period': {'start': '2026-10-30T00:00:00.000Z', 'end': '2026-10-31T00:00:00.000Z'},
                'resolution_set': [{'SourceId': 'SRC-RET-SYN', 'period': {'start': '2026-10-30T00:00:00.000Z', 'end': '2026-10-31T00:00:00.000Z'}, 'print': 'FIRST_RELEASE'}],
                'resolution_rule': resolution_rule, 'resolution_rule_sha256': digest(resolution_rule),
                'initial_method': {'id': 'MC-HYPOTHESIS-H1', 'sha256': methods['MC-HYPOTHESIS-H1']['content_sha256']},
                'motivated_by': ['TH-H1', 'the exact committed joined research record'], 'motivation_closure': 'Headline document, returns document, label record and joined record supplied from completed commits.',
                'selection_basis': {'uncertainty': 'Whether lexicon-labelled sentiment carries over to the next synthetic day.', 'decision_it_could_change': 'Which labelling experiment receives the next authorized attempt.',
                                    'experiment': 'Classify the next headline cohort, join to the next returns document, compare to three in five.', 'value_estimate': 'UNESTIMATED', 'value_basis': 'No investment-economic inference from synthetic data.',
                                    'cost_estimate_units': '0.30', 'time_estimate_ms': 600000, 'horizon': 'One synthetic day for the declared resolution member.', 'stopping_rule': 'Abandon as research if source or method requirements cannot be satisfied.', 'origin': 'theme TH-H1'}}
    provenance = {'execution_kind': 'deterministic synthetic program', 'provider': None, 'model': None, 'model_version': None, 'training_cutoff': None, 'spec_version': 'headline-design-v1',
                  'not_applicable_reason': 'FAKE-LLM-1 is a deterministic lexicon stand-in; no trained model or model provider is invoked; no diversity claim.'}
    designs = [
        {'content': {'AgentDesignVersionId': 'AD-RH1.0', 'AgentDesignLineageId': 'AD-RH1', 'method_class': 'RESEARCH', 'predecessor': None, 'program': 'researcher.py',
                     'entrypoint': 'examples.langgraph_headlines.researcher:main', 'ordinary_cycle_enabled': True, 'scope_profile': 'TH-H1',
                     'instructions': 'Read only committed closure. Reserve, pre-record each attempt, obtain one fresh permission, send headlines and nothing else to FAKE-LLM-1, keep the receipt durably before telling the core, settle, record labels and counts. After the returns document is committed, join recorded labels to committed returns and record the counts. Propose the pinned hypothesis template when research motivates it. Never check, decide, grant, fence, change a profile or claim forward standing. Preserve failures.',
                     'research_question': {'target': 'bullish label then positive next-day return', 'predicate': 'label=bullish', 'scope': 'TH-H1', 'difference_basis': 'Fixed lexicon labelling; no claim of model capability.'},
                     'tool_specs': {'FAKE-LLM-1': tools['FAKE-LLM-1']['content_sha256']}, 'initial_method': {'id': 'MC-RESEARCH-H1', 'sha256': methods['MC-RESEARCH-H1']['content_sha256']},
                     'evaluation_inputs': ['own Research Records', 'active grant and population', 'declared source observations'], 'evidence_outputs': ['plain Research Record', 'SELECTION'],
                     'proposable_outputs': ['Hypothesis registration', 'Agent Design successor registration without grant request'], 'provenance': provenance}},
        {'content': {'AgentDesignVersionId': 'AD-CK-H1.0', 'AgentDesignLineageId': 'AD-CK-H1', 'method_class': 'CHECKER', 'predecessor': None, 'program': 'evaluator.py',
                     'entrypoint': 'examples.langgraph_headlines.check:main',
                     'instructions': 'Execute every common and class criterion on a committed closure under the base-pinned CV1 and ES-1.0 through the client checking toolkit. Recompute the join of recorded labels to committed returns independently. Fund verification from own Checker grant. Never propose research, grant authority, decide a proposal or waive a criterion. Missing capability never becomes PASS.',
                     'tool_specs': {'CHECK-H-1': tools['CHECK-H-1']['content_sha256']}, 'initial_method': {'id': 'MC-CHECKER-H1', 'sha256': methods['MC-CHECKER-H1']['content_sha256']},
                     'evaluation_inputs': ['exact proposal', 'Transition lifecycle and Applied History', 'Evidence closure', 'pinned CV1 and ES-1.0', 'own grant', 'referenced artifacts'],
                     'evidence_outputs': ['verification Research Record', 'own reservation/attempt/settlement/close'], 'proposable_outputs': ['own Agent Design successor'], 'provenance': provenance}},
    ]
    for d in designs: d['content_sha256'] = digest(d['content'])
    artifacts = {'designs': designs, 'tools': tools, 'methods': methods, 'hypothesis_template': {'content': template, 'content_sha256': digest(template)},
                 'formation_cohort': {'source': 'SRC-NEWS-SYN', 'content': formation, 'content_sha256': digest(formation)},
                 'returns_cohort': {'source': 'SRC-RET-SYN', 'content': returns, 'content_sha256': digest(returns)},
                 'future_cohort_rule': {'content': {'version': 1, 'meaning': 'Deterministic synthetic daily headline and returns cohorts, not an observed market.', 'algorithm': 'For period date d reuse the formation rows with item_id headlines-d and returns-(d+1); released no earlier than period_end.'}},
                 'status': 'BUILT_PRIVATE_NOT_INITIALIZED'}
    artifacts['future_cohort_rule']['content_sha256'] = digest(artifacts['future_cohort_rule']['content'])
    common = {'grantor': 'Principal', 'expiry': EXPIRY, 'constitutional_budget': {'delta_O': 0, 'delta_S': 0, 'delta_A': 0}, 'capital_permission': False, 'provider_calls_permitted': False, 'uncapped_calls_permitted': False}
    grants = [
        {'content': {**common, 'AuthorizationId': 'AU-CK-H', 'class': 'Checker', 'grantee': ['AD-CK-H1.0'], 'tools': [{'id': 'CHECK-H-1', 'tier': 1, 'spec_sha256': tools['CHECK-H-1']['content_sha256']}],
                     'may_propose': ['own Agent Design successor', 'Constitutional proposal STOPPED until Principal decides'], 'may_check': ['every supported Transition class except own subjects'],
                     'may_commit_evidence': ['Research Record for verification', 'RESERVATION', 'attempt', 'settlement', 'CLOSED'], 'research_budget_units': '20.00', 'per_lineage_cap_units': '20.00',
                     'default_reservation_duration_ms': 604800000, 'binding_interval_ms': None, 'forbidden_subjects': ['AD-CK-H1 lineage and every successor', 'AU-CK-H and its successor chain'],
                     'provider_diversity': 'No provider diversity claimed: deterministic program under the A1 synthetic-only exception.'}},
        {'content': {**common, 'AuthorizationId': 'AU-OBS-H', 'class': 'Observation', 'grantee': ['Observation function'], 'tools': [], 'may_propose': [], 'may_check': [],
                     'may_commit_evidence': ['DOCUMENT Observation', 'feed retrieval COMPLETE/PARTIAL/RETRIEVAL_FAILED', 'Market Observation VALUE/ABSENT/NOT_EXTRACTABLE/RETRIEVAL_FAILED'],
                     'source_declarations': [{'SourceId': s['SourceId'], 'SourceRevision': digest(s), 'content': s} for s in (news_source, ret_source)],
                     'observation_plan': {'SRC-NEWS-SYN': {'retrieval_slot': 'period_end plus 1000 milliseconds', 'period_dates_inclusive': ['2026-10-28', '2027-04-29'], 'stop_rule': 'No slot at or after grant expiry.'},
                                          'SRC-RET-SYN': {'retrieval_slot': 'period_end plus 1000 milliseconds', 'period_dates_inclusive': ['2026-10-29', '2027-04-30'], 'stop_rule': 'No slot at or after grant expiry.'}}}},
        {'content': {**common, 'AuthorizationId': 'AU-RH-1', 'class': 'Research', 'grantee': ['AD-RH1.0'], 'tools': [{'id': 'FAKE-LLM-1', 'tier': 1, 'spec_sha256': tools['FAKE-LLM-1']['content_sha256']}],
                     'may_propose': ['Hypothesis registration', 'Agent Design successor registration without grant request', 'Theme registration', 'Constitutional proposal STOPPED until Principal decides'], 'may_check': [],
                     'may_commit_evidence': ['plain Research Record', 'SELECTION', 'RESERVATION', 'attempt', 'settlement', 'CLOSED'], 'research_budget_units': '3.00', 'per_lineage_cap_units': '3.00',
                     'default_reservation_duration_ms': 604800000, 'binding_interval_ms': 300000, 'scope_by_grantee': {'AD-RH1.0': {'themes': ['TH-H1'], 'empirical_search_families': []}},
                     'discovery_scope': {'SearchFamily': 'SF-HEAD-DISCOVERY', 'fixed_subgrant_units': '1.00', 'feed_sources': ['SRC-NEWS-SYN'], 'included_in_pool': True, 'shared_across_grantees': True, 'max_hop_depth': 1, 'followup_count': 0,
                                         'expected_screening_cadence': 'One classification per available headline item; inactivity leaves visible missing screens.'}}},
    ]
    theme = {'ThemeId': 'TH-H1', 'predecessor': None, 'statement': 'Lexicon-labelled headline sentiment may carry over to the next synthetic day.',
             'motivation_closure': 'The exact SRC-NEWS-SYN formation DOCUMENT committed after Apply 1; its sequence is resolved from that commit.',
             'typed_claims': [{'kind': 'QUESTION', 'text': 'Do bullish-labelled headlines precede positive next-day returns in the synthetic cohort?'},
                              {'kind': 'ASSUMPTION', 'text': 'Headlines and returns are synthetic fixtures; nothing here is market evidence.'}],
             'selection_basis': {'uncertainty': 'Whether a fixed lexicon label has any relation to the next synthetic return.', 'decision_it_could_change': 'Which labelling attempt to fund next.',
                                 'experiment': 'Classify the admitted headline cohort with FAKE-LLM-1, join to the returns document, propose the pinned template.', 'value_estimate': 'UNESTIMATED',
                                 'value_basis': 'Synthetic figures carry no economic meaning.', 'cost_estimate_units': '1.00', 'time_estimate_ms': 600000, 'horizon': 'One simulated daily period.',
                                 'stopping_rule': 'Stop after one accepted or refused registration.', 'origin': 'discovery-scope initiative'}}
    limits = {'portfolio_capital_units': '0.00', 'exploratory_pool_units': '0.00', 'per_strategy_allocation_cap_units': '0.00', 'per_strategy_lifetime_exploratory_cap_units': '0.00',
              'portfolio_gross_exposure_units': '0.00', 'portfolio_absolute_net_exposure_units': '0.00', 'per_instrument_exposure_units': '0.00', 'factor_exposure_units': '0.00',
              'portfolio_drawdown_loss_units': '0.00', 'strategy_versions': [], 'interpretation': 'Research-only zero-capital state.'}
    setup = {'profile': 'headline-sentiment-persistence-1', 'constitution': {'version': 1, 'sha256': CV1, 'evaluation_standard': 'ES-1.0'},
             'clock': {'epoch': '2026-10-29T00:00:00.000Z', 'initial_tick': 0, 'tick_unit': 'millisecond', 'maximum_tick': 15897600000, 'maximum_instant': '2027-05-01T00:00:00.000Z', 'binding_interval_ms': 300000, 'advance': 'explicit host advance only'},
             'grants': grants, 'initial_limits': limits, 'theme': {'content': theme, 'content_sha256': digest(theme)}, 'ordinary_researcher': 'AD-RH1.0',
             'startup': {'apply_0': ['CV1', 'AD-CK-H1.0', 'AU-CK-H'], 'then': ['AU-OBS-H', 'formation observation', 'initial_limits', 'AD-RH1.0', 'AU-RH-1', 'TH-H1'], 'ordinary_operation_from': 6},
             'status': 'BUILD_APPROVED_RUNTIME_NOT_INITIALIZED'}
    experiment = {'ExperimentId': 'HEADLINE-SENT-1', 'version': 1, 'description': 'Lexicon labels on synthetic headlines, joined to next-day synthetic returns committed one period later.',
                  'genesis': {'design': 'AD-CK-H1.0', 'grant': 'AU-CK-H'},
                  'steps': [{'name': 'classify-headlines', 'kind': 'research', 'tools': ['FAKE-LLM-1'], 'inputs': {'count': 1, 'kind': 'OBSERVATION', 'form': 'DOCUMENT'},
                             'parameters': {'lexicon': 'LEX-1', 'labels': ['bullish', 'bearish']}, 'input_limit_bytes': 1048576,
                             'tariff': {'measure': 'rows', 'limit': 500, 'per_unit': '0.02'}},
                            {'name': 'check-transition', 'kind': 'check', 'tools': ['CHECK-H-1'], 'maximum': '0.25'}],
                  'tools': {'FAKE-LLM-1': {'execution': 'caller', 'module': 'provider.py', 'callable': 'classify', 'label': 'fake-llm', 'provider_work': 'may_outlive_caller'},
                            'CHECK-H-1': {'execution': 'caller', 'module': 'evaluator.py', 'callable': 'evaluate', 'label': 'check-h', 'provider_work': 'ends_with_caller'}},
                  'sources': {'SRC-NEWS-SYN': {'period_ms': 86400000, 'item_id': {'prefix': 'headlines-'}, 'window': {'start': '2026-10-28T00:00:00.000Z', 'end': '2027-04-30T00:00:00.000Z'},
                                               'document': {'synthetic': True, 'max_bytes': 1048576},
                                               'extraction': {'validator': 'row-ratio', 'row_fields': {'row_id': 'str', 'headline': 'str'}, 'unique': 'row_id', 'denominator': [], 'numerator': []}},
                              'SRC-RET-SYN': {'period_ms': 86400000, 'item_id': {'prefix': 'returns-'}, 'window': {'start': '2026-10-29T00:00:00.000Z', 'end': '2027-05-01T00:00:00.000Z'},
                                              'document': {'synthetic': True, 'max_bytes': 1048576},
                                              'extraction': {'validator': 'row-ratio', 'row_fields': {'row_id': 'str', 'next_day_return_bp': 'int'}, 'unique': 'row_id', 'denominator': [], 'numerator': [{'field': 'next_day_return_bp', 'greater_than': 0}]}}}}
    write('setup.json', setup); write('designs_and_methods.json', artifacts); write('experiment.json', experiment)
    print('wrote setup.json designs_and_methods.json experiment.json')


if __name__ == '__main__': main()
