"""Write an experiment directory's setup files from a short description, with administrative defaults.

What this supplies: grants, limits, a theme, methods, provenance, identities,
the clock, the genesis pair and the profile. What it cannot supply: the
evaluator, which must be written for the experiment, and the scientific
content of a hypothesis template. The generated files are plain JSON and are
meant to be read and edited.
"""
from __future__ import annotations
from pathlib import Path
import json
from .protocol import digest

CV1 = 'c56a9cf50a7e9efadad8f2f2be6605e82c758f18d4096ba07eaaf86a8f8b7a64'
EXPIRY = '2027-04-30T00:00:00.000Z'
WINDOW = {'start': '2026-10-28T00:00:00.000Z', 'end': '2027-04-30T00:00:00.000Z'}
LIMITS = {'portfolio_capital_units': '0.00', 'exploratory_pool_units': '0.00', 'per_strategy_allocation_cap_units': '0.00', 'per_strategy_lifetime_exploratory_cap_units': '0.00',
          'portfolio_gross_exposure_units': '0.00', 'portfolio_absolute_net_exposure_units': '0.00', 'per_instrument_exposure_units': '0.00', 'factor_exposure_units': '0.00',
          'portfolio_drawdown_loss_units': '0.00', 'strategy_versions': [], 'interpretation': 'Research-only zero-capital state.'}
PROVENANCE = {'execution_kind': 'deterministic synthetic program', 'provider': None, 'model': None, 'model_version': None, 'training_cutoff': None, 'spec_version': 'generated-design-v1',
              'not_applicable_reason': 'Deterministic program; no trained model or model provider is invoked; no diversity claim.'}


def _write(directory, name, value): (Path(directory) / name).write_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=1).encode() + b'\n')


def write_setup(directory, *, experiment_id: str, short: str, question: str, source_id: str, item_prefix: str, source_class: str,
                tool_id: str, tool_module: str, tool_callable: str, tool_description: str, tool_cost: str,
                step_name: str, step_parameters: dict, tariff: dict, input_shapes: list,
                researcher_program: str, researcher_entrypoint: str, evaluator_module: str, evaluator_entrypoint: str, evaluator_description: str,
                formation_content: dict, theme_statement: str, budget: str = '100.00', document_max_bytes: int = 4194304,
                source_description: str = 'Local files the Principal supplies.', tool_execution: str = 'core', tool_interface: str = 'inputs') -> dict:
    """Write setup.json, designs_and_methods.json and experiment.json. Returns the identities it chose."""
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    researcher = f'AD-{short}1.0'; researcher_lineage = f'AD-{short}1'; checker = f'AD-CK-{short}1.0'; checker_lineage = f'AD-CK-{short}1'
    grant_r = f'AU-R{short}-1'; grant_ck = f'AU-CK-{short}'; grant_obs = f'AU-OBS-{short}'; theme = f'TH-{short}0'; check_tool = f'CHECK-{short}-1'
    synthetic = source_class == 'synthetic'
    source = {'SourceId': source_id, 'provider': 'The Principal, supplying files from local storage' if not synthetic else 'A deterministic generator in the experiment directory',
              'dataset': source_description, 'field': 'document', 'field_definition': 'One committed file with its rows or text.', 'unit': 'one file', 'print_rule': 'FIRST_RELEASE',
              'claimed_time_field': 'claimed_publication_time', 'resolution_grace_ms': 600000, 'endpoint': f'file://local/{{sha256}}', 'access_method': 'Read from the local filesystem by the Observation function; no network',
              'parsing': 'UTF-8 text; CSV, TSV and JSON parsed to rows with exact integers.', 'extraction_rule': 'None. Documents are inputs to declared analyses.', 'source_kind': 'DOCUMENT_FEED',
              'structural_availability_bound': 'Available from the declared receipt time.', 'synthetic': synthetic,
              'enumeration_contract': ({'complete_set': 'Every file the generator produced.', 'completeness': 'Not listed; many items per period.', 'item_identity': f'{item_prefix}YYYY-MM-DD-<content hash>', 'window': 'Daily periods in the declared window.'} if synthetic else None)}
    tools = {tool_id: {'content': {'kind': 'deterministic calculator' + (' run by the host' if tool_execution == 'core' else ' run by the researcher'), 'version': 1, 'algorithm': tool_description, 'cost': tool_cost,
                                   'inputs': 'Committed documents and one EXPERIMENT DESIGN record by the same researcher.', 'failure': 'A malformed input returns failure with diagnostic and the same charge.'}},
             check_tool: {'content': {'kind': 'deterministic Checker', 'version': 1, 'algorithm': evaluator_description, 'cost': '0.25 units per full Check attempt including a failing or incomplete Check; zero external billing.', 'input_limit_bytes': 33554432}}}
    for t in tools.values(): t['content_sha256'] = digest(t['content'])
    methods = {f'MC-RESEARCH-{short}1': {'content': {'version': 1, 'meaning': 'Contribution report only; no standing or grant.', 'forward_contribution': 'Admitted investigations that later produced a finalized forward Outcome, divided by settled research units; zero denominator NOT_ESTIMABLE.', 'limits': 'No profitability credit; reconstruction carries no forward standing.'}},
               f'MC-CHECKER-{short}1': {'content': {'version': 1, 'meaning': 'Verification contribution, not permission.', 'measure': 'Defects later established in passed subjects and refusals later shown unwarranted, divided by settled Checker units.', 'limits': 'Absence of a later defect finding is not proof of correctness.'}}}
    for m in methods.values(): m['content_sha256'] = digest(m['content'])
    designs = [
        {'content': {'AgentDesignVersionId': researcher, 'AgentDesignLineageId': researcher_lineage, 'method_class': 'RESEARCH', 'predecessor': None, 'program': researcher_program,
                     'entrypoint': researcher_entrypoint, 'ordinary_cycle_enabled': True, 'scope_profile': theme,
                     'instructions': 'Act only on the Principal\'s stated question, expectation and analysis. Commit the design before any attempt. Reserve, record the attempt citing the documents and the design, let the tool run, record the result with its conclusion against the expectation, settle. Derive next-step candidates from the conclusion and the history by the declared rule and record the Principal\'s selection with its rejections and their reconsideration conditions. Propose the next investigation as a Theme. Never check, decide, apply, fence or change a profile.',
                     'research_question': {'target': question, 'predicate': 'declared per design record', 'scope': theme, 'difference_basis': 'Each design states its own question and expectation.'},
                     'tool_specs': {tool_id: tools[tool_id]['content_sha256']}, 'initial_method': {'id': f'MC-RESEARCH-{short}1', 'sha256': methods[f'MC-RESEARCH-{short}1']['content_sha256']},
                     'evaluation_inputs': ['own Research Records', 'active grant and population', 'declared source observations'], 'evidence_outputs': ['EXPERIMENT DESIGN', 'plain Research Record', 'SELECTION'],
                     'proposable_outputs': ['Theme registration', 'Agent Design successor registration without grant request'], 'provenance': PROVENANCE}},
        {'content': {'AgentDesignVersionId': checker, 'AgentDesignLineageId': checker_lineage, 'method_class': 'CHECKER', 'predecessor': None, 'program': evaluator_module, 'entrypoint': evaluator_entrypoint,
                     'instructions': 'Execute every common and class criterion on a committed closure through the client checking toolkit. ' + evaluator_description + ' Fund verification from own Checker grant. Never propose, decide or waive a criterion. Missing capability never becomes PASS.',
                     'tool_specs': {check_tool: tools[check_tool]['content_sha256']}, 'initial_method': {'id': f'MC-CHECKER-{short}1', 'sha256': methods[f'MC-CHECKER-{short}1']['content_sha256']},
                     'evaluation_inputs': ['exact proposal', 'Transition lifecycle and Applied History', 'Evidence closure', 'pinned CV1 and ES-1.0', 'own grant', 'referenced artifacts'],
                     'evidence_outputs': ['verification Research Record', 'own reservation/attempt/settlement/close'], 'proposable_outputs': ['own Agent Design successor'], 'provenance': PROVENANCE}}]
    for d in designs: d['content_sha256'] = digest(d['content'])
    artifacts = {'designs': designs, 'tools': tools, 'methods': methods, 'formation_cohort': {'source': source_id, 'content': formation_content, 'content_sha256': digest(formation_content)}, 'status': 'BUILT_PRIVATE_NOT_INITIALIZED'}
    common = {'grantor': 'Principal', 'expiry': EXPIRY, 'constitutional_budget': {'delta_O': 0, 'delta_S': 0, 'delta_A': 0}, 'capital_permission': False, 'provider_calls_permitted': False, 'uncapped_calls_permitted': False}
    grants = [
        {'content': {**common, 'AuthorizationId': grant_ck, 'class': 'Checker', 'grantee': [checker], 'tools': [{'id': check_tool, 'tier': 1, 'spec_sha256': tools[check_tool]['content_sha256']}],
                     'may_propose': ['own Agent Design successor', 'Constitutional proposal STOPPED until Principal decides'], 'may_check': ['every supported Transition class except own subjects'],
                     'may_commit_evidence': ['Research Record for verification', 'RESERVATION', 'attempt', 'settlement', 'CLOSED'], 'research_budget_units': budget, 'per_lineage_cap_units': budget,
                     'default_reservation_duration_ms': 604800000, 'binding_interval_ms': None, 'forbidden_subjects': [f'{checker_lineage} lineage and every successor', f'{grant_ck} and its successor chain'],
                     'provider_diversity': 'No provider diversity claimed: deterministic program under the A1 synthetic-only exception.'}},
        {'content': {**common, 'AuthorizationId': grant_obs, 'class': 'Observation', 'grantee': ['Observation function'], 'tools': [], 'may_propose': [], 'may_check': [],
                     'may_commit_evidence': ['DOCUMENT Observation', 'feed retrieval COMPLETE/PARTIAL/RETRIEVAL_FAILED', 'Market Observation VALUE/ABSENT/NOT_EXTRACTABLE/RETRIEVAL_FAILED'],
                     'source_declarations': [{'SourceId': source_id, 'SourceRevision': digest(source), 'content': source}],
                     'observation_plan': {source_id: {'retrieval_slot': 'when the Principal imports a file', 'period_dates_inclusive': ['2026-10-28', '2027-04-29'], 'stop_rule': 'No slot at or after grant expiry.'}}}},
        {'content': {**common, 'AuthorizationId': grant_r, 'class': 'Research', 'grantee': [researcher], 'tools': [{'id': tool_id, 'tier': 1, 'spec_sha256': tools[tool_id]['content_sha256']}],
                     'may_propose': ['Theme registration', 'Agent Design successor registration without grant request', 'Constitutional proposal STOPPED until Principal decides'], 'may_check': [],
                     'may_commit_evidence': ['plain Research Record', 'EXPERIMENT DESIGN', 'SELECTION', 'RESERVATION', 'attempt', 'settlement', 'CLOSED'], 'research_budget_units': budget, 'per_lineage_cap_units': budget,
                     'default_reservation_duration_ms': 604800000, 'binding_interval_ms': 300000, 'scope_by_grantee': {researcher: {'themes': [theme], 'empirical_search_families': []}},
                     'discovery_scope': {'SearchFamily': f'SF-{short}-DISCOVERY', 'fixed_subgrant_units': '20.00', 'feed_sources': [source_id], 'included_in_pool': True, 'shared_across_grantees': True, 'max_hop_depth': 1, 'followup_count': 0,
                                         'expected_screening_cadence': 'One analysis per design the Principal commits; no cadence is imposed.'}}}]
    theme_content = {'ThemeId': theme, 'predecessor': None, 'statement': theme_statement, 'motivation_closure': 'The charter document committed after Apply 1.',
                     'typed_claims': [{'kind': 'QUESTION', 'text': question}, {'kind': 'ASSUMPTION', 'text': 'Analyses are reconstruction of committed inputs and earn no forward standing.'}],
                     'selection_basis': {'uncertainty': question, 'decision_it_could_change': 'Which investigation to design next.', 'experiment': 'Designs with recorded expectations, analysed by the declared tool and checked independently.',
                                         'value_estimate': 'UNESTIMATED', 'value_basis': 'No investment-economic inference from reconstruction alone.', 'cost_estimate_units': '20.00', 'time_estimate_ms': 600000,
                                         'horizon': 'The run.', 'stopping_rule': 'When the Principal records no further investigation.', 'origin': 'discovery-scope initiative'}}
    setup = {'profile': experiment_id.lower(), 'constitution': {'version': 1, 'sha256': CV1, 'evaluation_standard': 'ES-1.0'},
             'clock': {'epoch': '2026-10-29T00:00:00.000Z', 'initial_tick': 0, 'tick_unit': 'millisecond', 'maximum_tick': 15897600000, 'maximum_instant': '2027-05-01T00:00:00.000Z', 'binding_interval_ms': 300000, 'advance': 'explicit host advance only'},
             'grants': grants, 'initial_limits': LIMITS, 'theme': {'content': theme_content, 'content_sha256': digest(theme_content)}, 'ordinary_researcher': researcher,
             'startup': {'apply_0': ['CV1', checker, grant_ck], 'then': [grant_obs, 'charter observation', 'initial_limits', researcher, grant_r, theme], 'ordinary_operation_from': 6},
             'status': 'BUILD_APPROVED_RUNTIME_NOT_INITIALIZED', 'generated_by': 'arh_client.setup.write_setup', 'generated_defaults': 'grants, limits, theme, methods, provenance, identities, clock, genesis; the evaluator is not generated'}
    experiment = {'ExperimentId': experiment_id, 'version': 1, 'description': question, 'genesis': {'design': checker, 'grant': grant_ck},
                  'steps': [{'name': step_name, 'kind': 'research', 'tools': [tool_id], 'inputs': input_shapes, 'parameters': step_parameters, 'input_limit_bytes': 16777216, 'tariff': tariff},
                            {'name': 'check-transition', 'kind': 'check', 'tools': [check_tool], 'maximum': '0.25'}],
                  'tools': {tool_id: {'execution': tool_execution, 'module': tool_module, 'callable': tool_callable, 'label': tool_id.lower(), 'interface': tool_interface, 'provider_work': 'ends_with_caller'},
                            check_tool: {'execution': 'caller', 'module': evaluator_module, 'callable': 'evaluate', 'label': check_tool.lower(), 'provider_work': 'ends_with_caller'}},
                  'sources': {source_id: {'period_ms': 86400000, 'item_id': {'prefix': item_prefix, 'per_period': 'many'}, 'window': WINDOW,
                                          'document': {'class': source_class, 'synthetic': synthetic, 'max_bytes': document_max_bytes}, 'extraction': {'validator': 'none'}}}}
    _write(directory, 'setup.json', setup); _write(directory, 'designs_and_methods.json', artifacts); _write(directory, 'experiment.json', experiment)
    return {'researcher': researcher, 'checker': checker, 'grants': {'research': grant_r, 'checker': grant_ck, 'observation': grant_obs}, 'theme': theme, 'check_tool': check_tool}
