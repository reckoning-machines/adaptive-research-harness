"""Generate the three setup files through the client's generator. Administrative defaults only; the evaluator is evaluator.py."""
from pathlib import Path
import csv
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'client'))
from arh_client.setup import write_setup


def main():
    charter = {'class': 'synthetic', 'synthetic': True, 'file': {'name': 'charter.md', 'sha256': '0' * 64, 'bytes': 0, 'media_type': 'text/markdown'},
               'provenance': {'origin': 'the Principal', 'received_at': '2026-10-29T00:00:00.000Z', 'note': 'placeholder; the run supplies the real charter'}, 'text': 'Charter placeholder.',
               'item_id': 'signals-2026-10-28-0000000000000000', 'period_start': '2026-10-28T00:00:00.000Z', 'period_end': '2026-10-29T00:00:00.000Z', 'claimed_publication_time': '2026-10-29T00:00:00.000Z'}
    ids = write_setup(HERE, experiment_id='SIGNAL-GROUPS-1', short='S', question='Does the momentum signal in the table separate forward returns?',
                      source_id='SRC-SIG-SYN', item_prefix='signals-', source_class='synthetic', source_description='Generated signal and forward-return tables, examples/signal_groups/data/*.csv',
                      tool_id='SIGNAL-GROUPS-1', tool_module='tool.py', tool_callable='calculate',
                      tool_description='Wrap signal_groups.analyze unchanged: sort rows by the design\'s signal, split into equal groups, report each group\'s count, mean outcome and hit rate as exact ratios, and the spread between the top and bottom group means.',
                      tool_cost='0.10 units per document, charged on the number of admitted documents; 50 documents maximum.',
                      step_name='analyze-signal', step_parameters={'analysis_from': 'design'}, tariff={'measure': 'documents', 'limit': 50, 'per_unit': '0.10'},
                      input_shapes=[{'kind': 'OBSERVATION', 'form': 'DOCUMENT', 'min': 1, 'max': 50}, {'kind': 'RESEARCH_RECORD', 'record_kind': 'EXPERIMENT DESIGN', 'min': 1, 'max': 1}],
                      researcher_program='researcher.py', researcher_entrypoint='examples.signal_groups.researcher:SignalResearcher', evaluator_module='evaluator.py', evaluator_entrypoint='examples.signal_groups.evaluator:evaluate',
                      evaluator_description='For a Theme, re-run signal_groups.analyze on the committed rows and design and compare the result, verify the conclusion against the recorded expectation, the order of design before attempt, the settlement, and that the selection\'s candidate set follows the declared rule over the history it cites. Reproducibility and record integrity only.',
                      formation_content=charter, theme_statement='Investigations of signals in the Principal\'s tables under this run\'s charter.')
    print('wrote setup for', ids)


if __name__ == '__main__': main()
