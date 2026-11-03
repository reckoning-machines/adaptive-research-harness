"""Generate setup.json, designs_and_methods.json and experiment.json for local-document research."""
from __future__ import annotations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
CV1 = 'c56a9cf50a7e9efadad8f2f2be6605e82c758f18d4096ba07eaaf86a8f8b7a64'
EXPIRY = '2027-04-30T00:00:00.000Z'


def canonical(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
def digest(v): return hashlib.sha256(canonical(v)).hexdigest()
def write(name, value): (HERE / name).write_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=1).encode() + b'\n')


def main():
    source = {'SourceId': 'SRC-LOCAL-DOC', 'provider': 'The Principal, supplying files from local storage', 'dataset': 'Documents the Principal brings for investigation: text, markdown, CSV, TSV or JSON rows',
              'field': 'document', 'field_definition': 'One committed file: name, content hash, size, media type, declared origin and receipt time, and its text or rows.', 'unit': 'one file',
              'print_rule': 'FIRST_RELEASE', 'claimed_time_field': 'claimed_publication_time', 'resolution_grace_ms': 600000, 'endpoint': 'file://local/{sha256}',
              'access_method': 'Read from the local filesystem by the Observation function at the Principal\'s request; no network', 'parsing': 'UTF-8 text; CSV, TSV and JSON parsed to rows with exact integers; everything else kept as text.',
              'extraction_rule': 'None. Documents are inputs to declared analyses; no value is extracted at observation.', 'source_kind': 'DOCUMENT_FEED',
              'structural_availability_bound': 'Available from the receipt time the Principal declares. Historical material: read after the fact, never prospective evidence.', 'synthetic': False, 'enumeration_contract': None}
    tools = {
        'LOCAL-CALC-1': {'content': {'kind': 'deterministic local calculator run by the host', 'version': 1,
                                     'algorithm': 'Read the committed EXPERIMENT DESIGN record among the inputs and run its declared analysis over the committed documents. term-count: case-insensitive occurrences of declared terms per text document. table-stat: count, sum, ratio or mean of a numeric column over rows passing declared filters, as exact integers or integer ratios. Return per-document detail, a summary and the metric the design names.',
                                     'cost': '0.10 units per document, charged on the number of admitted documents; 50 documents maximum.', 'inputs': 'One to fifty committed DOCUMENT observations and exactly one EXPERIMENT DESIGN record by the same researcher.',
                                     'failure': 'An unsupported analysis or malformed document returns failure with diagnostic and the same charge.'}},
        'CHECK-L-1': {'content': {'kind': 'deterministic Checker', 'version': 1, 'algorithm': 'Common and class criteria through the client checking toolkit. For a THEME, the motivation criterion additionally recomputes the cited analysis from the cited documents and design with independent code, verifies the conclusion against the recorded expectation, verifies the design preceded the attempt and the attempt settled, and verifies the selection chose among the candidates the evidence produced.',
                                  'cost': '0.25 units per full Check attempt including a failing or incomplete Check; zero external billing.', 'input_limit_bytes': 33554432}},
    }
    for t in tools.values(): t['content_sha256'] = digest(t['content'])
    methods = {
        'MC-RESEARCH-L1': {'content': {'version': 1, 'meaning': 'Contribution report only; no standing or grant.', 'forward_contribution': 'Count admitted investigations that later produced a finalized forward Outcome; historical analyses count zero. Divide by settled research units; zero denominator NOT_ESTIMABLE.', 'limits': 'No profitability credit; historical reconstruction carries no forward standing.'}},
        'MC-CHECKER-L1': {'content': {'version': 1, 'meaning': 'Verification contribution, not permission.', 'measure': 'Defects later established in passed subjects and refusals later shown unwarranted, with exact references, divided by settled Checker units.', 'limits': 'Absence of a later defect finding is not proof of correctness.'}},
    }
    for m in methods.values(): m['content_sha256'] = digest(m['content'])
    provenance = {'execution_kind': 'deterministic synthetic program', 'provider': None, 'model': None, 'model_version': None, 'training_cutoff': None, 'spec_version': 'local-design-v1',
                  'not_applicable_reason': 'Deterministic programs over local documents; no trained model or model provider is invoked; no diversity claim.'}
    designs = [
        {'content': {'AgentDesignVersionId': 'AD-L1.0', 'AgentDesignLineageId': 'AD-L1', 'method_class': 'RESEARCH', 'predecessor': None, 'program': 'researcher.py',
                     'entrypoint': 'experiments.local_documents.researcher:LocalResearcher', 'ordinary_cycle_enabled': True, 'scope_profile': 'TH-L0',
                     'instructions': 'Act only on the Principal\'s stated question, expectation and analysis. Commit the design before any attempt. Reserve, record the attempt citing the documents and the design, let the host run the calculator, record the result with the conclusion against the expectation, settle. Derive next-step candidates from the conclusion by the declared rule and record the Principal\'s selection with its rejections. Propose the next investigation as a Theme. Never check, decide, apply, fence or change a profile. Preserve revisions and rejected conclusions.',
                     'research_question': {'target': 'the Principal\'s current question', 'predicate': 'declared per design record', 'scope': 'TH-L0', 'difference_basis': 'Each design states its own question and expectation.'},
                     'tool_specs': {'LOCAL-CALC-1': tools['LOCAL-CALC-1']['content_sha256']}, 'initial_method': {'id': 'MC-RESEARCH-L1', 'sha256': methods['MC-RESEARCH-L1']['content_sha256']},
                     'evaluation_inputs': ['own Research Records', 'active grant and population', 'declared source observations'], 'evidence_outputs': ['EXPERIMENT DESIGN', 'plain Research Record', 'SELECTION'],
                     'proposable_outputs': ['Theme registration', 'Agent Design successor registration without grant request'], 'provenance': provenance}},
        {'content': {'AgentDesignVersionId': 'AD-CK-L1.0', 'AgentDesignLineageId': 'AD-CK-L1', 'method_class': 'CHECKER', 'predecessor': None, 'program': 'evaluator.py',
                     'entrypoint': 'experiments.local_documents.evaluator:evaluate',
                     'instructions': 'Execute every common and class criterion on a committed closure through the client checking toolkit. For a Theme, recompute the cited analysis independently and verify the conclusion, the ordering of design before attempt, the settlement and the selection. Fund verification from own Checker grant. Never propose, decide or waive a criterion. Missing capability never becomes PASS.',
                     'tool_specs': {'CHECK-L-1': tools['CHECK-L-1']['content_sha256']}, 'initial_method': {'id': 'MC-CHECKER-L1', 'sha256': methods['MC-CHECKER-L1']['content_sha256']},
                     'evaluation_inputs': ['exact proposal', 'Transition lifecycle and Applied History', 'Evidence closure', 'pinned CV1 and ES-1.0', 'own grant', 'referenced artifacts'],
                     'evidence_outputs': ['verification Research Record', 'own reservation/attempt/settlement/close'], 'proposable_outputs': ['own Agent Design successor'], 'provenance': provenance}},
    ]
    for d in designs: d['content_sha256'] = digest(d['content'])
    charter = {'class': 'historical', 'synthetic': False, 'file': {'name': 'charter.md', 'sha256': '0' * 64, 'bytes': 0, 'media_type': 'text/markdown'},
               'provenance': {'origin': 'the Principal', 'received_at': '2026-10-29T00:00:00.000Z', 'note': 'placeholder; the run supplies the real charter'}, 'text': 'Research charter placeholder.',
               'item_id': 'doc-2026-10-28-0000000000000000', 'period_start': '2026-10-28T00:00:00.000Z', 'period_end': '2026-10-29T00:00:00.000Z', 'claimed_publication_time': '2026-10-29T00:00:00.000Z'}
    artifacts = {'designs': designs, 'tools': tools, 'methods': methods,
                 'formation_cohort': {'source': 'SRC-LOCAL-DOC', 'content': charter, 'content_sha256': digest(charter), 'meaning': 'The charter the Principal writes when a run starts replaces this placeholder.'},
                 'status': 'BUILT_PRIVATE_NOT_INITIALIZED'}
    common = {'grantor': 'Principal', 'expiry': EXPIRY, 'constitutional_budget': {'delta_O': 0, 'delta_S': 0, 'delta_A': 0}, 'capital_permission': False, 'provider_calls_permitted': False, 'uncapped_calls_permitted': False}
    grants = [
        {'content': {**common, 'AuthorizationId': 'AU-CK-L', 'class': 'Checker', 'grantee': ['AD-CK-L1.0'], 'tools': [{'id': 'CHECK-L-1', 'tier': 1, 'spec_sha256': tools['CHECK-L-1']['content_sha256']}],
                     'may_propose': ['own Agent Design successor', 'Constitutional proposal STOPPED until Principal decides'], 'may_check': ['every supported Transition class except own subjects'],
                     'may_commit_evidence': ['Research Record for verification', 'RESERVATION', 'attempt', 'settlement', 'CLOSED'], 'research_budget_units': '100.00', 'per_lineage_cap_units': '100.00',
                     'default_reservation_duration_ms': 604800000, 'binding_interval_ms': None, 'forbidden_subjects': ['AD-CK-L1 lineage and every successor', 'AU-CK-L and its successor chain'],
                     'provider_diversity': 'No provider diversity claimed: deterministic program under the A1 synthetic-only exception.'}},
        {'content': {**common, 'AuthorizationId': 'AU-OBS-L', 'class': 'Observation', 'grantee': ['Observation function'], 'tools': [], 'may_propose': [], 'may_check': [],
                     'may_commit_evidence': ['DOCUMENT Observation', 'feed retrieval COMPLETE/PARTIAL/RETRIEVAL_FAILED', 'Market Observation VALUE/ABSENT/NOT_EXTRACTABLE/RETRIEVAL_FAILED'],
                     'source_declarations': [{'SourceId': source['SourceId'], 'SourceRevision': digest(source), 'content': source}],
                     'observation_plan': {'SRC-LOCAL-DOC': {'retrieval_slot': 'when the Principal imports a file', 'period_dates_inclusive': ['2026-10-28', '2027-04-29'], 'stop_rule': 'No slot at or after grant expiry.'}}}},
        {'content': {**common, 'AuthorizationId': 'AU-RL-1', 'class': 'Research', 'grantee': ['AD-L1.0'], 'tools': [{'id': 'LOCAL-CALC-1', 'tier': 1, 'spec_sha256': tools['LOCAL-CALC-1']['content_sha256']}],
                     'may_propose': ['Theme registration', 'Agent Design successor registration without grant request', 'Constitutional proposal STOPPED until Principal decides'], 'may_check': [],
                     'may_commit_evidence': ['plain Research Record', 'EXPERIMENT DESIGN', 'SELECTION', 'RESERVATION', 'attempt', 'settlement', 'CLOSED'], 'research_budget_units': '100.00', 'per_lineage_cap_units': '100.00',
                     'default_reservation_duration_ms': 604800000, 'binding_interval_ms': 300000, 'scope_by_grantee': {'AD-L1.0': {'themes': ['TH-L0'], 'empirical_search_families': []}},
                     'discovery_scope': {'SearchFamily': 'SF-LOCAL-DISCOVERY', 'fixed_subgrant_units': '20.00', 'feed_sources': ['SRC-LOCAL-DOC'], 'included_in_pool': True, 'shared_across_grantees': True, 'max_hop_depth': 1, 'followup_count': 0,
                                         'expected_screening_cadence': 'One analysis per design the Principal commits; no cadence is imposed.'}}},
    ]
    theme = {'ThemeId': 'TH-L0', 'predecessor': None, 'statement': 'Investigations the Principal conducts on local documents under this run\'s charter.',
             'motivation_closure': 'The charter document committed after Apply 1; its sequence is resolved from that commit.',
             'typed_claims': [{'kind': 'QUESTION', 'text': 'What do the Principal\'s documents show about the question stated in the charter?'},
                              {'kind': 'ASSUMPTION', 'text': 'Documents are real material read after the fact; analyses are historical reconstruction and earn no forward standing.'}],
             'selection_basis': {'uncertainty': 'Stated in the charter.', 'decision_it_could_change': 'Which investigation to design next.', 'experiment': 'Designs with recorded expectations, analysed by the host-run calculator and checked independently.',
                                 'value_estimate': 'UNESTIMATED', 'value_basis': 'No investment-economic inference from historical reconstruction alone.', 'cost_estimate_units': '20.00', 'time_estimate_ms': 600000,
                                 'horizon': 'The run.', 'stopping_rule': 'When the Principal records no further investigation.', 'origin': 'discovery-scope initiative'}}
    limits = {'portfolio_capital_units': '0.00', 'exploratory_pool_units': '0.00', 'per_strategy_allocation_cap_units': '0.00', 'per_strategy_lifetime_exploratory_cap_units': '0.00',
              'portfolio_gross_exposure_units': '0.00', 'portfolio_absolute_net_exposure_units': '0.00', 'per_instrument_exposure_units': '0.00', 'factor_exposure_units': '0.00',
              'portfolio_drawdown_loss_units': '0.00', 'strategy_versions': [], 'interpretation': 'Research-only zero-capital state.'}
    setup = {'profile': 'local-documents-1', 'constitution': {'version': 1, 'sha256': CV1, 'evaluation_standard': 'ES-1.0'},
             'clock': {'epoch': '2026-10-29T00:00:00.000Z', 'initial_tick': 0, 'tick_unit': 'millisecond', 'maximum_tick': 15897600000, 'maximum_instant': '2027-05-01T00:00:00.000Z', 'binding_interval_ms': 300000, 'advance': 'explicit host advance only'},
             'grants': grants, 'initial_limits': limits, 'theme': {'content': theme, 'content_sha256': digest(theme)}, 'ordinary_researcher': 'AD-L1.0',
             'startup': {'apply_0': ['CV1', 'AD-CK-L1.0', 'AU-CK-L'], 'then': ['AU-OBS-L', 'charter observation', 'initial_limits', 'AD-L1.0', 'AU-RL-1', 'TH-L0'], 'ordinary_operation_from': 6},
             'status': 'BUILD_APPROVED_RUNTIME_NOT_INITIALIZED'}
    experiment = {'ExperimentId': 'LOCAL-DOCS-1', 'version': 1, 'description': 'The Principal\'s own documents, analysed by a host-run calculator against a recorded expectation, with the next investigation proposed from the evidence and checked independently.',
                  'genesis': {'design': 'AD-CK-L1.0', 'grant': 'AU-CK-L'},
                  'steps': [{'name': 'analyze-documents', 'kind': 'research', 'tools': ['LOCAL-CALC-1'],
                             'inputs': [{'kind': 'OBSERVATION', 'form': 'DOCUMENT', 'min': 1, 'max': 50}, {'kind': 'RESEARCH_RECORD', 'record_kind': 'EXPERIMENT DESIGN', 'min': 1, 'max': 1}],
                             'parameters': {'analysis_from': 'design'}, 'input_limit_bytes': 16777216,
                             'tariff': {'measure': 'documents', 'limit': 50, 'per_unit': '0.10'}},
                            {'name': 'check-transition', 'kind': 'check', 'tools': ['CHECK-L-1'], 'maximum': '0.25'}],
                  'tools': {'LOCAL-CALC-1': {'execution': 'core', 'module': 'calc.py', 'callable': 'calculate', 'label': 'local-calc', 'interface': 'inputs', 'provider_work': 'ends_with_caller'},
                            'CHECK-L-1': {'execution': 'caller', 'module': 'evaluator.py', 'callable': 'evaluate', 'label': 'check-l', 'provider_work': 'ends_with_caller'}},
                  'sources': {'SRC-LOCAL-DOC': {'period_ms': 86400000, 'item_id': {'prefix': 'doc-', 'per_period': 'many'}, 'window': {'start': '2026-10-28T00:00:00.000Z', 'end': '2027-04-30T00:00:00.000Z'},
                                                'document': {'class': 'historical', 'synthetic': False, 'max_bytes': 4194304}, 'extraction': {'validator': 'none'}}}}
    write('setup.json', setup); write('designs_and_methods.json', artifacts); write('experiment.json', experiment)
    print('wrote setup.json designs_and_methods.json experiment.json')


if __name__ == '__main__': main()
