# Implementation Report - Experiment Profile, Client, Host and the LangGraph Example

Status: **IMPLEMENTATION RECORD OF DISPOSABLE SYNTHETIC DEVELOPMENT. CV1 UNCHANGED. CONSTITUTIONAL DELTA 0/0/0. NOTHING HERE IS CERTIFICATION, ADMISSION OR PRODUCTION GENESIS.**

Date: 2026-11-01. Implements the
[integration plan](../plans/langgraph_integration_20261101.md) as revised
with the Principal's corrections, answering the
[integration readiness audit](../audits/langgraph_integration_readiness_audit_20261101.md).
Working tree at HEAD `212ac40` plus the changes listed in section 7.

## 1. What works

- **The synthetic experiment is a profile, not code.** Its steps, tools,
  tariffs, Check cost, source rules, extraction validator and genesis pair
  are in `experiments/synthetic_flow/experiment.json`, frozen into every
  bundle. `rules.do_attempt`, `rules.do_observation_commit`, `dispatch`,
  `tool_worker`, `engine.genesis`, the service wiring and `freeze` read
  the profile. Refusal codes are unchanged. The original example and every
  acceptance case run as before.
- **Caller-executed tools are a declared kind.** `tool-run` gives one fresh
  `PERMISSION_CONSUMED` per attempt against a durable claim; `tool-finish`
  registers one receipt and refuses a different one; settlement is at the
  receipt or at the maximum. Replacement after a receipt-less claim needs
  proof the caller generation is gone and, for a provider declared
  `may_outlive_caller`, a recorded `COMPLETED` or `CANCELLED` disposition
  of the earlier operation. Deduplication recovers the original claim only.
- **A host command.** `python3 -m adaptive_research_harness.local_host
  --setup DIR --run DIR` freezes a setup directory into a bundle, starts
  the core and core-run tool workers, writes a connection file and serves a
  control socket (`tick`, `quiesce`, `status`, `stop`). The acceptance
  fixture and the workbench now use the same module.
- **An installable client.** `client/` installs `arh_client` from its own
  directory with no dependencies. Public surface: `connect`, `Connection`,
  `Outcome`, `Ref`, `HarnessError`, `RefusedError`, `Researcher`,
  `Execution`, `ReceiptStore`, `Checker`, `CheckResult`, `Principal`,
  `Observer`, `startup`, `HostControl` and the optional
  `langgraph_adapter`. Governed refusals are structured `Outcome` values
  with reason, detail and record references; operational failures raise
  `HarnessError`. `client/README.md` documents every public operation with
  purpose, arguments, return, refusals and retry behaviour, a getting
  started example and the trust model, and marks internal helpers.
- **A complete external experiment.** `examples/langgraph_headlines/`
  supplies its own setup, profile, deterministic fake provider, LangGraph
  researcher with a SQLite checkpointer, evaluator and runner. The core
  imports none of it. Headlines go to the classifier; next-day returns are
  a second source committed one period later; the evaluator joins recorded
  labels to committed returns and states that it verifies the join and the
  arithmetic, not the labels.

## 2. How to run it

```sh
python3 -m venv .venv && .venv/bin/pip install -e './client[langgraph]'
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m examples.langgraph_headlines
```

From outside the checkout: copy `examples/langgraph_headlines` anywhere,
install the client there, run `python -m langgraph_headlines --harness
/path/to/speedway`. The original synthetic example is unchanged:
`python3 -m acceptance.local --example`.

The retained run `artifacts/development/langgraph/20261101-064151/`
printed, in order:

| Demonstration | Result |
| --- | --- |
| Startup through checked controls | N=5, five Checks PASS by AD-CK-H1.0 |
| Classification recorded and settled | 12 bullish / 12 bearish of 24, cost 0.48, one provider call |
| Returns committed one period later | the classifier never saw them |
| Overstated count proposed | Check FAIL on recomputation, `policy-decide` refused `CHECK_NOT_PASS`, N unchanged, proposal preserved outside the Applied History |
| Researcher tries to approve or change rules | apply before decision `NOT_DECIDED`, check-commit `UNVERIFIED_CHECK`, decide, policy-decide, fence, propose LIMITS and propose AUTHORIZATION `UNAUTHORIZED`; seven refusals preserved |
| Honest proposal | 9/12 bullish labels followed by a positive return, Check PASS, P-1 ADMITTED, Apply, N=6 |
| Over-budget work | reserve 5.00 `BUDGET_EXCEEDED`; reserve 0.20 then attempt 0.48 `ALLOWANCE_EXCEEDED`; provider calls unchanged |
| Killed after the durable receipt | resumed from the checkpoint, no second call |
| Exact successful claim request replayed | `RECEIPT`, no permission, no call |
| Killed after the provider completed, before the receipt | recovered by provider lookup under the original claim, no second call |
| Killed with no record anywhere | reconciled `UNKNOWN` at 0.48, liability counted, pending attempts empty, no second call |
| Replacement | refused `WORKER_NOT_QUIESCENT` with no proof and again with only the dead caller; admitted after the provider's `CANCELLED` disposition; executed once and settled |
| Budgets | AU-RH-1 committed 2.40 of 3.00; AU-CK-H 1.75; five provider calls in all |

## 3. What was tested

| Suite | Command | Result |
| --- | --- | --- |
| Unit, component, workbench, integration | `python3 -m unittest discover -s tests -t .` | 74 tests, OK, 87 s (61 before this work, 13 added) |
| Component, profile boundary | `tests/component/test_experiment.py`: profile loading and eleven malformed profiles refused, tariff bands and per-unit maxima, `row-ratio` reproducing the `SRC-SYN` extraction, attempt and observation admission reading the profile, caller-tool replacement rules including the `may_outlive_caller` dispositions, receipt binding through a real engine | 10 tests, OK |
| Integration, real processes | `tests/integration/test_langgraph_example.py`: every demonstration above as assertions; the example run from a copy outside the checkout; generic startup on the synthetic bundle reproducing the sixteen transitions `TR-1` to `TR-16` with the same subjects and `AU-CK-A` committed 4.00 | 3 tests, OK |
| Cooperative acceptance with death schedules | `python3 -m acceptance.local --jobs 4` | 77 cases PASS, no failures, 2 min 7 s with 4 jobs; summary under `artifacts/development/latest/bceebe2e663e493692250034ea9adab3/`, inventory `bd7167a9...`, `os_isolation: UNVERIFIED` as before |
| Original example | `python3 -m acceptance.local --example` | `E01 PASS`, N=17, same printed result as before |
| Clean environment | a fresh venv outside the checkout, `pip install '<checkout>/client[langgraph]'`, the README getting-started snippet run verbatim apart from the provider against a host started from the checkout | startup N=5; record, settlement and close `COMMITTED`; same key again returns the same outcome; lost-reply lookup `COMMITTED`; `decide` as researcher `REFUSED UNAUTHORIZED` |

Adapted fixtures: `tests/component/fabricated.py` freezes a disposable
bundle from the current tree instead of loading the historical one.
`acceptance/local.py`, `workbench/session.py` and `acceptance/runtime.py`
read the core tool labels from the profile. No acceptance case assertion
was changed.

## 4. Claims verified against the code, from the adversarial inputs

Section 6 of the audit records each. Of note during implementation:

- The feasibility audit's LangGraph claim held in 1.2.19: a node killed
  mid-way re-executes from its beginning on resume. The adapter therefore
  keeps permission inside the execute node and never in state, and the
  replay test shows a re-sent claim request grants nothing.
- F14 (tariffs and bounds in code) is closed by the profile. F18 (A1
  no-provider assumption in the Checkers) is unchanged and is noted in the
  client toolkit's independence criterion.
- `check-commit` from the researcher is refused `UNVERIFIED_CHECK` before
  the grant class is examined, because no claim receipt exists for it. Both
  refusals are correct; the printed reason is the first one the core meets.

## 5. Decisions made during implementation

- Tool modules may be installed package modules or files relative to the
  experiment directory; file modules are copied into the bundle under
  `tools/` and both forms are hashed into `tool_executables`. The
  enforcement process reads only the hashes.
- The synthetic bundle now orders design roles by method class in file
  order; the result equals the historical role map.
- `Profile` refuses a bundle without `experiment.json` as
  `BUNDLE_INCOMPLETE`; the workbench opens such retained runs read-only by
  reading the artifacts directly. The historical bundle under `docs/builds`
  is untouched.
- The profile query now carries `experiment` so a client can compute the
  tariff it must declare.
- `contracts.STEPS` was removed; nothing read it after the profile.
- The example runner expects N=5 after startup, not 6 as the plan's text
  implied: genesis consumes the Checker design and grant.

## 6. Remaining limitations

- Cooperative tokens in one host process and one file; no OS isolation;
  Linux templates still unexecuted.
- For `caller` tools the receipt is the caller's statement. The core binds
  and counts it. It cannot stop a process spending at a provider it can
  reach. The controlled arrangement is a tool the host runs, as A and B are.
- Quiescence proofs rest on pids no longer running, which is fixture
  evidence. Provider dispositions are recorded by the host on the
  Principal's token from what the provider reported; the core verifies
  their shape and binding to the claim, not their truth.
- The independent reader reconstructs the synthetic experiment only. The
  headline experiment's arithmetic is verified by its registered evaluator.
- The host runs from the checkout; the client runs anywhere. The example
  copied outside the checkout still starts the host inside it.
- LangGraph is pinned to the 1.x line and langgraph-checkpoint-sqlite to
  2.x or 3.x; tested with langgraph 1.2.19, langgraph-checkpoint 4.3.1 and
  langgraph-checkpoint-sqlite 3.1.3 on Python 3.12.3.
- Everything is synthetic and earns no forward standing. Real documents
  need the small extension the plan's section 9 describes, decided first.
- `build_support/verify.py` fails on a stale `/private/tmp` snapshot as it
  did before this work.

## 7. Files

Changed: `.gitignore`, `BUILD.md`, `README.md`, `architecture.md`,
`runbook.md`, `acceptance/local.py`, `adaptive_research_harness/__main__.py`,
`contracts.py`, `dispatch.py`, `engine.py`, `host.py`, `profile.py`,
`rules.py`, `service.py`, `tool_worker.py`, `build_support/freeze.py`,
`tests/component/fabricated.py`, `workbench/session.py`.

New: `adaptive_research_harness/experiment.py`,
`adaptive_research_harness/local_host.py`,
`experiments/synthetic_flow/experiment.json`, `client/` (package, README,
`pyproject.toml`), `examples/langgraph_headlines/`,
`tests/component/test_experiment.py`, `tests/integration/`, this report,
the audit and the plan.

Untouched: every admitted document, the admission packet, the historical
build record, `actors.py`, both Checkers, both synthetic tools, and the
acceptance case assertions.
