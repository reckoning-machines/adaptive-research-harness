# Implementation Report - Research on the Principal's Own Documents

Status: **IMPLEMENTATION RECORD OF DISPOSABLE DEVELOPMENT ON REAL LOCAL FILES. CV1 UNCHANGED. CONSTITUTIONAL DELTA 0/0/0. NOTHING HERE IS CERTIFICATION, ADMISSION OR PRODUCTION GENESIS.**

Date: 2026-11-01. Implements the direction in the
[local documents record](../decisions/local_documents_research_20261101.md).
Builds on the [integration report](langgraph_integration_20261101.md).

## 1. What works

One research workflow on your own files, through the workbench page at
`/local` or through `workbench.local_session.LocalRun` in code.

| You do | What is recorded | Who verifies or permits |
| --- | --- | --- |
| Write a charter and start | The charter as the first historical document; startup to N=5 with the umbrella direction `TH-L0` citing it | Each startup control checked by the evaluator, decided and applied by the Principal |
| Import files | One `OBSERVATION` per file with name, content hash, size, media type, your origin and receipt time, text or rows, class `historical` | The core refuses a synthetic label on this source, missing provenance, and an item id that does not carry the content hash |
| State a question, an expectation and an analysis | An `EXPERIMENT DESIGN` record with no attempt, citing the documents, naming the planned tool, optionally revising an earlier design | The core admits it under the research grant; it costs nothing |
| Run | A reservation, an attempt citing the documents and the design as exact inputs, the host-run calculator's receipt, a result record with the conclusion MET, NOT_MET or INCONCLUSIVE, a settlement | The core pins inputs and the estimate; the calculator runs in a worker the host started and sees only admitted inputs |
| Choose the next step | A `SELECTION` with the candidates the conclusion produced, your choice, your reason and the rejections | The candidate set is the researcher program's declared rule over the conclusion state; the choice is yours and is recorded |
| Propose the direction | A Theme proposal citing documents, design, result and selection, funded | The evaluator recomputes the analysis with its own code and verifies conclusion, order, settlement and selection; the Principal admits or rejects after a passing check |
| Stop and reopen | Everything under `artifacts/development/workbench/<run>/`; reopen on the same records with the same next actions, or read-only under a differing build | Nothing is re-executed on reopen |

A retained run, `artifacts/development/workbench/demo-20261101-072344-local-memos/`,
holds three memos and a trade table, a met expectation admitted as
direction `TH-L1` at N=6, and a second investigation, a revision concluded
NOT_MET, stopped at its selection step. It reopens live on the page with
the candidates waiting for a choice.

The next action responds to the evidence: a met expectation offers extend,
sharpen or alternative explanation; a failed one offers revise the
expectation, change the analysis or reject; too few documents offers add
documents or relax the minimum. What the researcher proposes and what the
harness verifies and permits are separate records: the design and the
selection are proposals, the check is the verification, the decision and
apply are permission.

## 2. The extension, exactly

| Change | Where | Meaning |
| --- | --- | --- |
| Document class | `experiment.py` source rule, `rules.do_observation_commit` | A source is `synthetic` or `historical`. A historical document must carry file identity and provenance and is stamped `class: historical, synthetic: false`. A synthetic label on a historical source is refused, and the reverse |
| Record class inheritance | `rules.do_research_commit` | A research record declares its class; one citing a historical input must be historical |
| Records without an attempt | `rules.do_research_commit` | `EXPERIMENT DESIGN` and `SELECTION` may carry `attempt: null` under a Research grant |
| Revisions | `rules.do_research_commit` | `revises` names an earlier record by the same actor; both stay |
| Input shapes and measures | `experiment.py`, `rules.do_attempt`, `dispatch.run`, `tool_worker` | A step declares shapes of inputs with bounds; a tariff may count rows, documents or kilobytes; a host-run tool with `interface: inputs` receives every admitted input |
| Many items per period | `experiment.py`, `rules.do_observation_commit` | Item id is prefix, date and the first sixteen hex of the content hash; no listing form for such a source |
| No extraction | `experiment.py` | A source may declare validator `none`; VALUE forms are then unsupported |
| Optional record fields | `contracts.py` | `class`, `revises`, `design`, `expectation`, `analysis`, `conclusion` |

Nothing changed in authority: who may reserve, attempt, check, decide or
apply, the criteria set, the receipt binding or the replacement rule. The
synthetic cycle and the headline example run unchanged.

## 3. What was tested

| Suite | Result |
| --- | --- |
| Component, `tests/component/test_experiment.py` | 14 tests OK, including historical document rules, class inheritance, design records without an attempt, revisions, input shapes and the per-document tariff |
| Integration, `tests/integration/test_local_documents.py` | 3 tests OK, under five seconds. The session path: charter, three memos, a term-count design concluded MET, candidates, selection, Theme checked PASS and admitted to N=6, a CSV import, a revised table-stat design concluded NOT_MET, reject chosen, Theme checked PASS and rejected by the Principal, a forged conclusion failing its check on `motivation` and refused at decision, close, reopen with identical records, a copy under a differing build read-only. The HTTP path: the page, every route in order, a decide before any check refused `NO_CHECK`, the synthetic step route refused, close and reopen |
| Unit, component, workbench, integration | 81 tests OK, 92 s |
| Cooperative acceptance | 77 cases PASS, no failures, 2 min 6 s with 4 jobs; summary under `artifacts/development/latest/e510aff473dd4b01ac7d2528bf9d4867/`, `os_isolation: UNVERIFIED` as before |
| Headline example and synthetic example | unchanged, within the suites above |

## 4. An LLM researcher: what it would need, not built

The workflow above uses a deterministic calculator the host runs. Replacing
or supplementing it with a model provider needs the following, each a
Principal decision or a declared arrangement, none made here.

| Need | Why | Where it would land |
| --- | --- | --- |
| A provider identity rule, D-14 | The registered design pins provider, model and version; substitution needs an admitted rule | Grant and design content |
| A cap and billing decision for the provider | Real calls are not capped by the harness; the tariff admits an estimate and settlement counts the actual | A recorded Principal acceptance per provider, then `provider_calls_permitted` on the grant and a real settlement unit |
| Credential placement | A credential held by the researcher process gives accounting only; held by a worker the host runs it gives controlled access | A core-run tool whose worker holds the credential, with `provider_work: may_outlive_caller` and provider-side lookup and cancellation |
| Provenance on the design | The Checkers require no-provider provenance under the A1 exception; a design that invokes a model declares provider, model, version and cutoff | Design content and the evaluator's independence criterion |
| Checking what a model produced | The evaluator can recompute arithmetic over recorded labels, not the labels | The same split as the headline example: recorded outputs are evidence, recomputation covers the join |

## 5. Limitations

- The synthetic clock is advanced to the day after each import. Your
  declared receipt time is provenance the ledger keeps, not a system
  witness.
- Text, markdown, CSV, TSV and JSON rows only. PDFs are not read.
- Two analyses, `term-count` and `table-stat`. Another needs a calculator
  implementation and a matching recount in the evaluator.
- Funding is under the umbrella direction `TH-L0`; admitted directions
  record where the research goes and do not change the grant's scope.
- The workbench process holds every token; no OS isolation. The evaluator
  runs in that process under its own token.
- The independent reader covers the synthetic experiment only.
- Historical reconstruction earns no forward standing. Forward predictions
  on these documents are not built.

## 6. Files

New: `experiments/local_documents/` (setup generator and JSON, calculator,
evaluator, researcher), `workbench/local_session.py`, `workbench/local.html`,
`tests/integration/test_local_documents.py`, the decision record and this
report.

Changed: `adaptive_research_harness/experiment.py`, `rules.py`,
`contracts.py`, `dispatch.py`, `tool_worker.py`, `client/arh_client/`
(`research.py`, `principal.py`, `checking.py`, `__init__.py`, README),
`workbench/session.py`, `workbench/api.py`, `workbench/__main__.py`,
`tests/component/test_experiment.py`, `BUILD.md`, `runbook.md`,
`architecture.md`.
