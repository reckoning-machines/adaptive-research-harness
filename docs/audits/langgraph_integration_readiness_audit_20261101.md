# Integration Readiness Audit - External Researcher, Profile Separation and a LangGraph Client

Status: **AUDIT EVIDENCE - READ-ONLY INSPECTION OF THE BUILT CYCLE AGAINST THE INTEGRATION BRIEF. AUTHORIZES NOTHING. THE COMPANION PLAN PROPOSES THE WORK.**

Date: 2026-11-01. Reviewer: Claude (Fable 5.1), at the Principal's
direction. Subject: the Principal's brief to make the harness usable by a
data science team connecting an existing LangGraph swarm, read against the
implementation at HEAD `212ac40` (inventory of the current tree
`109c4e0a93e44896f4eeabe4b73e93c19e1e7b3a7518b47ababbaf0d240bf34d`),
[BUILD.md](../../BUILD.md), the
[architecture](../../architecture.md), the
[build approval addendum](../decisions/first_research_cycle_build_approval_addendum_20261029.md)
with its workflow-supersession paragraph, and the
[workbench authorization](../decisions/workbench_authorization_20261030.md)
with its working rule.

Adversarial input. The brief names "the adversarial review" as input. Two
adversarial documents exist in this checkout and both were used:

- the [public-library feasibility audit](feasibility_coherence_public_library_20261029.md),
  sections 5 and 6, which proposed the library boundary, the trust
  statement an embedding contract must make, and the LangGraph adapter
  shape (reserve before metered work, look up the governed attempt on
  node re-entry, carry ledger references in graph state, separate proposer
  and Checker contexts, treat replay as workflow behaviour);
- the [adversarial first-cycle build audit](adversarial_first_cycle_build_audit_20261029.md),
  whose findings F3, F4, F6, F7, F10, F11, F14 and F18 bear on an
  integration.

Each claim taken from them was checked against the code and is marked
below as holding, superseded or still open.

Method. Source reading of every module under `adaptive_research_harness/`,
`acceptance/`, `workbench/`, `build_support/` and `tests/`, the frozen
bundle under `docs/builds/first_cycle_20261029/run_bundle/`, and the two
adversarial documents. Commands run, all non-mutating or disposable under
the addendum:

| Command | Outcome |
| --- | --- |
| `python3 -m unittest discover -s tests -t .` | 61 tests, OK, 58 s |
| `python3 -m acceptance.local --example` | `E01 PASS`, N=17, inventory `109c4e0a...` |
| `python3 build_support/verify.py` | `AssertionError` at line 25, before any change in this work. It compares the tree to a stale `/private/tmp/arh-build-before.json` snapshot. Pre-existing, outside this brief |
| `pip install langgraph` into a scratch venv | LangGraph 1.2.19, langgraph-checkpoint 4.3.1, langgraph-checkpoint-sqlite imports; Python 3.12.3 |

No governed record, admitted document, test or implementation file was
modified by this audit.

## 1. Disposition

**The core already enforces, generically, everything the brief wants
preserved. What blocks an external team is that the one synthetic
experiment is written into the enforcement code, and that no installable
caller exists outside the repository.** Authority, funding, evidence,
checking and admission are enforced in `rules.py`, `engine.py`,
`model.py`, `storage.py` and `dispatch.py` without reference to the
experiment's content, with the exceptions listed in section 2. The
caller-executed tool path the integration needs already exists for Check
tools and is selected by a string prefix. The retry rule after a lost
receipt is stricter than the caller-executed case warrants. No new
governed identity, evidentiary class, Transition class, Authorization or
Evaluation Standard is needed to close the gap. Expected Constitutional
Delta for the companion plan: 0/0/0.

## 2. What is experiment-specific inside enforcement code

Each row is a literal of the spike-and-selling experiment inside a module
that also enforces a general control. The brief asks to move these into
an explicit profile without weakening the controls around them.

| Where | Literal | General control it sits inside |
| --- | --- | --- |
| `adaptive_research_harness/contracts.py:29` | `STEPS` names four steps | Attempt admission |
| `rules.py:158` | `b['step'] in STEPS` | Attempt admission |
| `rules.py:170-173` | Check tools identified by `tool['id'].startswith('CHECK')`, Check cost `maximum == 25` | Checker funding |
| `rules.py:175-181` | Research steps named; exactly one `OBSERVATION` of form `DOCUMENT`; `parameters == {'threshold': 2}`; row limit 4096; tariff 1.00 up to 1024 rows and 2.00 above | Estimate admission before dispatch |
| `rules.py:366-371` | Source must be `SRC-SYN`; 24-hour periods aligned to midnight; window 2026-10-28 to 2027-04-30; `item_id` is `cohort-` plus the date | Observation route |
| `rules.py:384-393` | `VALUE` extraction recomputes spike and selling counts in code | Observation extraction binding |
| `dispatch.py:14-17` | `work_key` maps the two research step names to one key | Duplicate-work detection |
| `dispatch.py:41, 59, 84` | Caller-executed path selected by `tool.startswith('CHECK')` | Dispatch claim before handoff |
| `dispatch.py:54` | Core tools receive `input_refs[0]`'s document only | Handoff content |
| `dispatch.py:94` | `receipt['actual'] == '0.25'` for a finished Check | Receipt binding |
| `tool_worker.py:13` | Tool id to module map for A and B | Worker identity |
| `service.py:104`, `__main__.py:17-19, 40` | Tool sockets and UIDs for A and B | Service wiring (Linux path, untouched by the local fixture) |
| `engine.py:194-195` | Genesis expects `AD-CK-1.0` and `AU-CK-A` from the bundle | Apply 0 exactness |
| `build_support/freeze.py:53, 62-64, 107` | `step_catalog`, role UIDs for ten researchers and two Checkers, `tool_executables` for four modules | Build identity |
| `actors.py` entire | The researcher program: grant `AU-RP-1`, amounts, Theme `TH-G1`, steps, hypothesis template, Checker to grant map, imports of `checkers.a` and `checkers.b` | None. This is the synthetic researcher, not a control. It is wired in by `service.run_agent` and `acceptance/local.py:109-130` |
| `checkers/a.py:132-177`, `checkers/b.py` | `HYPOTHESIS` criteria compare against `hypothesis_template` and recompute spike and selling counts from rows | None. These are the two registered Checker designs for this experiment |
| `acceptance/reader.py:226-240` | Research recomputation assumes `n_large` in results | The independent reader is experiment-specific |

Everything else that admits or refuses is generic and needs no change for
a different experiment: request-key deduplication and receipt lookup
(`engine.py:79-82, 108-121`), grant activity, grantee, expiry and class
(`model.py:69-75`), reservation scope and caps (`rules.py:107-139`),
attempt allowance and lineage cap (`rules.py:142-157`), settlement at
actual or `UNKNOWN` maximum (`rules.py:190-204`), proposal authority and
scope (`rules.py:49-59`, `model.py:139-152`), Check structure, criteria
set, closure and receipt binding (`rules.py:235-263`, `engine.py:136-138`),
decision and `P-1` (`rules.py:265-281`), binding, Apply and invalidation
(`rules.py:283-343`, `engine.py:85-109, 145-156`), research-record
admission (`rules.py:345-356`), fence (`rules.py:214-218`), the clock and
the immutable carrier.

## 3. What an external caller has today

| Need | Exists | Gap |
| --- | --- | --- |
| A wire protocol | Length-framed canonical JSON over a Unix socket (`transport.py:28-41`, `encoding.py:36-70`). The local fixture adds `token` and `pid` to each request (`acceptance/local.py:49-53, 90-94`) | Not packaged. The only clients are `adaptive_research_harness.client.Client`, which needs Linux peer credentials, and `acceptance.local.LocalClient`, which lives in fixture code |
| Idempotent commands | Every command carries a request key; a repeat returns the original receipt; a conflicting payload under the same key is refused (`engine.py:79-82, 111-112`, `storage.py:78-100`). `inspect-request` answers whether a lost call committed (`engine.py:55-59`) | Keys must be version-4 UUIDs, so a caller cannot derive them from a job name. The caller must persist keys before use, which maps directly onto a checkpointed graph state |
| Reserve, attempt, dispatch, settle | All present (`rules.do_reserve`, `do_attempt`, `dispatch.run`, `do_settle`) | The sequence is composed only inside `actors.py` |
| A caller that executes its own metered work | The Check path does exactly this: `tool-run` returns `PERMISSION_CONSUMED` against a durable claim, the caller computes, `check-finish` registers the receipt once and refuses a different one (`dispatch.py:59, 90-98`), `check-commit` must equal that receipt, settlement cites it | Selected by the `CHECK` prefix and bound to the 0.25 cost. Not available to a research tool |
| A host that starts the core | `acceptance.local.LocalRuntime` and `workbench.session.Session` start core and tool workers as processes, hold tokens, write a quiescence proof on restart | Both are fixtures that also drive the synthetic case. No command starts a host against an arbitrary bundle and hands a connection file to another process |
| Startup | `acceptance/runtime.py:55-75` runs the 16-step startup with ids written in | The order is derivable from `setup.json` (genesis, Observation grant, formation, limits, designs in file order, remaining grants in file order, theme). A generic startup can reproduce the same transition ids |

## 4. Execution lifecycle and recovery, as built

The brief's lifecycle requirements are compared with the code.

| Requirement | As built | Finding |
| --- | --- | --- |
| Reserve before potentially billable dispatch | `do_attempt` requires an open, unfenced, unexpired reservation with allowance for the maximum (`rules.py:142-157`). `dispatch.run` refuses without an admitted attempt (`dispatch.py:36`) | Holds |
| Durable identity per attempt | The `ATTEMPT` Evidence sequence; a durable `dispatch_claims` row before handoff (`dispatch.py:50-52`); `dispatch_index` per retry with `DUPLICATE_ATTEMPT` and ordering checks (`rules.py:182-187`) | Holds |
| Settle the recorded outcome | `TOOL_RECEIPT` settlement must equal the claim's receipt; `UNKNOWN` settles at the admitted maximum (`engine.py:133-135`, `rules.py:197-202`) | Holds |
| Preserve unresolved liability | Pending attempts count at maximum in every total (`model.py:96-101`); `obligations` lists them; nothing erases a claim | Holds |
| Retries and resume must not dispatch the same attempt again | A second `tool-run` on a claimed attempt returns `IN_PROGRESS_OR_UNCERTAIN` or the receipt, never a second handoff (`dispatch.py:38, 48`). A new attempt for the same work key requires the predecessor settled and a quiescence proof (`dispatch.py:19-29`) | Holds for core-dispatched tools. For a caller-executed tool the proof demanded names the old core generation (`dispatch.py:27-28`) although the core handed nothing to anyone. The generation that could still act is the caller's. A LangGraph process that died after a lost receipt could not lawfully open a replacement attempt while the same core runs. A refinement, not a new rule |
| Completing a graph node must not admit output | Admission needs `check-commit` from a Checker grant and either a Principal `decide` or `P-1` inside `@Apply`, then `apply` (`rules.py:235-329`). No command lets a research actor do any of these | Holds |

The LangGraph claim in the feasibility audit, that an interrupted node
restarts from its beginning so preceding code runs again, holds for
LangGraph 1.2.19: state is checkpointed after a node completes, so a
process killed mid-node re-executes that node on resume. The integration
must therefore split "obtain permission" from "execute" only if each half
is idempotent against the core, which the claim and receipt mechanism
already supplies.

## 5. Trust model, as built

Facts the integration guide must state, each verified in code:

- In the local arrangement one host process generates every actor token
  and writes them to a file (`acceptance/local.py:141-144`). A caller's
  identity is a shared secret plus a self-reported pid. There is no OS
  isolation; `BUILD.md` already says so and the Linux templates remain
  unexecuted.
- For a caller-executed tool, the executable hash in the attempt is
  supplied by the caller and compared with the bundle inventory
  (`rules.py:167-168`). The inventory pins the bytes on disk when the
  host starts (`profile.py:32-34`). Nothing proves the caller ran those
  bytes. The receipt is the caller's own statement. This is accounting.
- For a core-dispatched tool, the core hands the admitted input to a
  worker it started, with the input hash in the claim, and accepts a
  receipt only from that worker's generation (`dispatch.py:60-63`,
  `tool_worker.py:27-28`). A provider credential held only by such a
  worker would be spending the researcher cannot reach. The synthetic
  tools A and B are the built instance of this path.
- A Checker is a separate registered design under a Checker grant.
  Independence is lineage, grant and provider based (`rules.py:11-47`).
  A researcher cannot register a Checker that could check it: a successor
  design must share its lineage (`model.py:148-149`), and only the
  Principal can propose an Authorization (`rules.py:226`).
- Tool B recomputing counts from the same rows is an independent
  calculation, not independent evidence. The workbench already labels it
  so. The same applies to a Checker recomputing an aggregate from labels
  a provider produced: it verifies the arithmetic, not the labels.

## 6. Adversarial findings checked against the current code

| Finding | Status now | Evidence |
| --- | --- | --- |
| F3 driver-built proposals under the researcher's identity | Superseded | `adversarial-command` refuses `propose` and `research-commit` (`service.py:159`, `acceptance/local.py:127`); `propose-mutated` writes `adversarial_case` into content (`actors.py:234`); decide, policy-decide and apply refuse marked content (`rules.py:273, 280, 306`) |
| F4 own-subject Checker funding admitted | Superseded | `do_reserve` evaluates independence for Check purposes before charging (`rules.py:111-117`); case X04 |
| F6 refused genesis poisons the store | Superseded | Pre-initialization refusals stay in the receipt table only (`engine.py:189-194`) |
| F7 reader cannot expose admission defects | Superseded for the synthetic experiment | `acceptance/reader.py:86-107` reconstructs Check, decision, bind and funding links; still experiment-specific for recomputation |
| F10 some refusals not preserved | Partly superseded | `apply` refusals now commit through `_commit(failure=...)` (`engine.py:93-94`); `NOT_INITIALIZED` remains a receipt-only refusal by design |
| F11 write transaction held across tool IPC | Superseded | `describe` runs before the transaction (`dispatch.py:33-44`) |
| F14 tariffs and bounds duplicated in code | Open | Section 2 lists them. This is the profile work |
| F18 Checker independence hardcodes the A1 exception | Open | `checkers/a.py:46-47`. Unchanged by this brief; a profile-driven Checker toolkit should read `provider_diversity` from the grant rather than assume no provider |
| Feasibility section 5, trust assumptions must be stated | Open | Nothing outside `BUILD.md` states them for an embedding caller |
| Feasibility section 6, LangGraph hooks | Open | No adapter exists; the hooks it lists map onto existing operations as section 3 shows |

## 7. Routine decisions the plan makes

These are implementation choices within the admitted design. None creates
a governed identity, owner, class, Authorization, budget or Standard.

1. The profile is a data file, `experiment.json`, frozen into the bundle
   and covered by the inventory, read by `rules`, `dispatch`,
   `tool_worker`, `freeze` and the Checkers. It declares steps, tools,
   tariffs, Check cost, source rules and the genesis pair. Validation it
   needs is selected by name from a closed registry inside the core and
   parametrised; the profile cannot name code.
2. Each tool declares `execution`, either `core`, handed to a worker the
   host starts, or `caller`, executed by the actor that holds the attempt
   and reported through `tool-finish`. The Check tools become the first
   `caller` tools and keep their fixed cost.
3. For a `caller` tool, replacement after a settled receipt-less claim
   requires proof that the caller's recorded generation is gone, not the
   core's. Core-dispatched tools keep the existing rule.
4. The installable client is standard-library Python speaking the existing
   framed protocol with the token ingress. LangGraph is an optional extra.
5. The host that starts core and workers moves from fixture code into the
   package so a team can run it without the acceptance driver. The
   acceptance fixture and the workbench keep using it.
6. The example experiment classifies synthetic headlines with a
   deterministic fake provider and asks whether bullish labels precede
   positive next-day returns. It lives under `examples/`, with its own
   setup, profile, provider, LangGraph researcher and evaluator, none of
   which the core imports.
7. The historical bundle under `docs/builds/first_cycle_20261029/` is not
   regenerated. Component tests that need a bundle freeze a disposable
   one. The historical bundle stays what it is, a record of an older
   tree.

## 8. Items for the Principal, none blocking

- The new example's grants, designs, source and theme are a second
  disposable synthetic setup, authorized as development under the
  addendum's workflow paragraph. They are not an admitted packet and
  produce no production genesis.
- The independent reader in `acceptance/reader.py` reconstructs the
  synthetic experiment only. The new experiment's reconstruction is
  performed by its registered evaluator, which is a registered design and
  not an independent reader. A general reader is later work.
- The pre-existing `build_support/verify.py` failure is left as found.

`dO/dS/dA` of this audit: **`0/0/0`**. It adds evidence only.
