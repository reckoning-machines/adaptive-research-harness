"""The setup description: identities, the source and its class, the tool, the tariff, the budget and the evaluator entry points.

main() writes the three setup files for this directory, whose data is
generated and labelled synthetic. own_setup() writes a setup whose source
is the Principal's own files, declared historical, into another directory
with the tool, evaluator and researcher modules beside it. Both go through
the client's generator, which supplies administrative defaults only.
"""
from __future__ import annotations
from pathlib import Path
import shutil
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'client'))
from arh_client.setup import write_setup

MODULES = ('tool.py', 'evaluator.py', 'researcher.py')


def write(directory, *, source_class, source_id, dataset, budget='100.00'):
    synthetic = source_class == 'synthetic'
    charter = {'class': source_class, 'synthetic': synthetic, 'file': {'name': 'charter.md', 'sha256': '0' * 64, 'bytes': 0, 'media_type': 'text/markdown'},
               'provenance': {'origin': 'the Principal', 'received_at': '2026-10-29T00:00:00.000Z', 'note': 'placeholder; the run supplies the real charter'}, 'text': 'Charter placeholder.',
               'item_id': 'signals-2026-10-28-0000000000000000', 'period_start': '2026-10-28T00:00:00.000Z', 'period_end': '2026-10-29T00:00:00.000Z', 'claimed_publication_time': '2026-10-29T00:00:00.000Z'}
    return write_setup(directory, experiment_id='SIGNAL-GROUPS-1', short='S', question='Does the momentum signal in the table separate forward returns?',
                       source_id=source_id, item_prefix='signals-', source_class=source_class, source_description=dataset, budget=budget,
                       tool_id='SIGNAL-GROUPS-1', tool_module='tool.py', tool_callable='calculate',
                       tool_description='Wrap signal_groups.analyze unchanged: sort rows by the design\'s signal, split into equal groups, report each group\'s count, mean outcome and hit rate as exact ratios, and the spread between the top and bottom group means.',
                       tool_cost='0.10 units per document, charged on the number of admitted documents; 50 documents maximum.',
                       step_name='analyze-signal', step_parameters={'analysis_from': 'design'}, tariff={'measure': 'documents', 'limit': 50, 'per_unit': '0.10'},
                       input_shapes=[{'kind': 'OBSERVATION', 'form': 'DOCUMENT', 'min': 1, 'max': 50}, {'kind': 'RESEARCH_RECORD', 'record_kind': 'EXPERIMENT DESIGN', 'min': 1, 'max': 1}],
                       researcher_program='researcher.py', researcher_entrypoint='examples.signal_groups.researcher:SignalResearcher', evaluator_module='evaluator.py', evaluator_entrypoint='examples.signal_groups.evaluator:evaluate',
                       evaluator_description='For a Theme, re-run signal_groups.analyze on the committed rows and design and compare the result, verify the conclusion against the recorded expectation, the order of design before attempt, the settlement, and that the selection\'s candidate set follows the declared rule over the history it cites. Reproducibility and record integrity only.',
                       formation_content=charter, theme_statement='Investigations of signals in the Principal\'s tables under this run\'s charter.')


def own_setup(directory, dataset='Tables the Principal supplies from local storage', budget='100.00'):
    """A historical-class setup for the Principal's own files, with the modules it names copied beside it."""
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    for m in MODULES: shutil.copyfile(HERE / m, directory / m)
    return write(directory, source_class='historical', source_id='SRC-SIG-OWN', dataset=dataset, budget=budget)


def main():
    ids = write(HERE, source_class='synthetic', source_id='SRC-SIG-SYN', dataset='Generated signal and forward-return tables, examples/signal_groups/data/*.csv')
    print('wrote setup for', ids)


if __name__ == '__main__': main()
