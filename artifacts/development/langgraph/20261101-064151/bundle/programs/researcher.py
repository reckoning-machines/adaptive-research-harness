"""AD-RH1.0: the team's researcher as a LangGraph graph with a SQLite checkpointer.

Two jobs. classify: reserve, attempt, obtain one fresh permission, call
FAKE-LLM-1 with the headline document only, keep the receipt durably, tell
the core, record labels and counts, settle, close. join: after the returns
document is committed, join recorded labels to committed returns, record the
counts, propose the pinned hypothesis and fund the proposal.

python3 -m <package>.researcher --connection PATH --run-dir DIR --job NAME --mode classify|join [options]
Re-running the same job resumes from its checkpoint.
"""
from __future__ import annotations
from copy import deepcopy
import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path
from arh_client import connect, Researcher, ReceiptStore, event_ref
from arh_client.protocol import digest
from arh_client.langgraph_adapter import ExperimentSpec, build_research_graph, build_proposal_graph
from .provider import FakeProvider

STEP = 'classify-headlines'; TOOL = 'FAKE-LLM-1'; PARAMETERS = {'lexicon': 'LEX-1', 'labels': ['bullish', 'bearish']}
QUESTION = 'Which synthetic headlines does the fixed lexicon label bullish?'
JOIN_QUESTION = 'How many bullish-labelled headlines were followed by a positive next-day synthetic return?'


def build_record(researcher, state, receipt):
    result = receipt['result']; failure = receipt.get('error')
    return researcher.record_body(state['attempt'], QUESTION, result if not failure else None, failure, [state['formation']],
                                  claims=[{'kind': 'REPORTED', 'document': state['formation'], 'location': '/rows', 'text': 'Declared synthetic headline rows'},
                                          {'kind': 'INTERPRETATION', 'reported': [0], 'text': 'Lexicon labels from FAKE-LLM-1; no economic or forward standing; returns were not an input'}])


def derive(researcher, state):
    """Join the recorded labels to the committed returns document. Reads committed closure only."""
    o = state.get('options') or {}
    labels_rec = researcher.c.get(o['labels_record']); lab = labels_rec['body']['result']
    headline_ref = labels_rec['body']['closure']['refs'][0]
    returns_doc = researcher.formation('SRC-RET-SYN', o.get('returns_item')); returns_ref = event_ref(returns_doc)
    rows = {r['row_id']: r['next_day_return_bp'] for r in returns_doc['body']['document']['rows']}
    bull = [x['row_id'] for x in lab['labels'] if x['label'] == 'bullish']; bear = [x['row_id'] for x in lab['labels'] if x['label'] == 'bearish']
    k_up = sum(1 for i in bull if i in rows and rows[i] > 0)
    parameters = dict(PARAMETERS, analysis='label-return-join', comparison_ratio=[3, 5])
    if o.get('exaggerate'):
        k_up += 2; parameters['demonstration'] = 'inflated-count: the researcher overstates k_bullish_up by two to show the independent Check'
    result = {'n_bullish': len(bull), 'k_bullish_up': k_up, 'n_bearish': len(bear), 'k_bearish_down': sum(1 for i in bear if i in rows and rows[i] < 0),
              'passes': len(bull) > 0 and 5 * k_up >= 3 * len(bull), 'rule': '5*k_bullish_up >= 3*n_bullish, a descriptive diagnostic, not a statistical test',
              'labels_record': {'sequence': labels_rec['seq'], 'sha256': labels_rec['sha256']}, 'input_sha256': digest(researcher.c.get(headline_ref)['body']['document']), 'synthetic': True}
    labels_ref = {'ledger': 'E', 'sequence': labels_rec['seq'], 'sha256': labels_rec['sha256'], 'raw_sha256': digest(labels_rec['body'])}
    body = researcher.record_body(labels_rec['body']['attempt'], JOIN_QUESTION, result, None, [headline_ref, returns_ref, labels_ref], parameters=parameters,
                                  claims=[{'kind': 'REPORTED', 'document': headline_ref, 'location': '/rows', 'text': 'Headline rows'},
                                          {'kind': 'REPORTED', 'document': returns_ref, 'location': '/rows', 'text': 'Next-day synthetic returns, committed one period later'},
                                          {'kind': 'INTERPRETATION', 'reported': [0, 1], 'text': 'Join of recorded labels to committed returns; synthetic; no forward standing'}],
                                  source_cutoff=returns_doc['body']['document']['period_end'])
    return body


def build_proposal(researcher, state):
    o = state.get('options') or {}
    template = deepcopy(researcher.profile()['artifacts']['hypothesis_template']['content'])
    derived = state['derived']; labels_rec = researcher.c.get(o['labels_record']); rec = researcher.c.get(derived)
    refs = [r for r in rec['body']['closure']['refs']]
    template['motivated_by'] = ['TH-H1', derived]
    template['motivation_closure'] = {'N': rec['body']['closure']['N'], 'refs': refs + [derived]}
    template['selection_basis']['origin'] = {'research_record': derived, 'labels_record': o['labels_record']}
    return template


def make_spec(provider, crash):
    def hook(point):
        if crash == point: os._exit(137)
    return ExperimentSpec(step=STEP, tool=TOOL, parameters=PARAMETERS, purpose={'kind': 'Theme', 'id': 'TH-H1'}, reserve_amount='0.50', source='SRC-NEWS-SYN',
                          provider=provider, provider_lookup=provider.lookup, build_record=build_record, question=QUESTION,
                          derive=derive, build_proposal=build_proposal, proposal_budget='0.30', hook=hook)


def run_job(connection_path, run_dir, job, mode, options=None, crash=None, actor='AD-RH1.0'):
    from langgraph.checkpoint.sqlite import SqliteSaver
    run_dir = Path(run_dir); conn = connect(connection_path, actor); researcher = Researcher(conn)
    provider = FakeProvider(run_dir / 'provider', crash=crash); spec = make_spec(provider, crash)
    store = ReceiptStore(run_dir / 'researcher' / 'receipts')
    db = sqlite3.connect(str(run_dir / 'researcher' / 'checkpoints.sqlite'), check_same_thread=False); saver = SqliteSaver(db)
    graph = build_research_graph(researcher, spec, store, saver) if mode == 'classify' else build_proposal_graph(researcher, spec, saver)
    config = {'configurable': {'thread_id': job}}
    existing = graph.get_state(config)
    if existing.values: out = graph.invoke(None, config); resumed = True
    else: out = graph.invoke({'job': job, 'options': options or {}, 'log': []}, config); resumed = False
    out = dict(out); out['resumed'] = resumed; out['provider_calls'] = provider.calls(); db.close(); return out


def main(argv=None):
    p = argparse.ArgumentParser(); p.add_argument('--connection', required=True); p.add_argument('--run-dir', required=True); p.add_argument('--job', required=True)
    p.add_argument('--mode', choices=['classify', 'join'], default='classify'); p.add_argument('--options', default='{}'); p.add_argument('--crash', default=None)
    a = p.parse_args(argv)
    out = run_job(a.connection, a.run_dir, a.job, a.mode, json.loads(a.options), a.crash)
    print(json.dumps(out, sort_keys=True, default=str)); return 0


if __name__ == '__main__': sys.exit(main())
