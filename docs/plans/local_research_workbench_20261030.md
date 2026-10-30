# Local Research Workbench - Implementation Plan

Status: **ADMITTED 2026-10-30 by the [workbench authorization](../decisions/workbench_authorization_20261030.md), with the two adjustments recorded there and folded in below.**

Date: 2026-10-30. This plan answers the
[workbench readiness audit](../audits/workbench_readiness_audit_20261030.md)
and proposes the smallest build that satisfies the Principal's brief
reproduced there. It becomes authorized only when a decision in
`docs/decisions/` admits it.

Governing baseline: [CV1, revision 12](../doctrines/new_speedway_constitution.md),
as [admitted](../decisions/cv1_admission_20261019.md). The
[first research-cycle plan](first_research_cycle_implementation_20261029.md)
and the
[build approval addendum](../decisions/first_research_cycle_build_approval_addendum_20261029.md)
define the cycle this workbench sits on. CV1 governs if this plan conflicts
with it. Constitutional budget for every step below: 0/0/0.

## 1. Exact milestone

One local page, served by one Python process from the standard library,
that can do the following against the built harness and nothing else.

1. Start a research run on a chosen synthetic cohort. Three cohorts ship:
   the original, one with independent large shocks, one where the broad
   claim survives its control.
2. Show the run as the sequence question, experiment, result, diagnostic,
   revised question, Check, admission, each stage linked to the ledger
   record that is its evidence.
3. Show the rows, the computed counts, the candidates the researcher
   considered, the one it chose, the ones it rejected and the stated reason.
4. Show budget reserved, spent and remaining per grant, every accepted or
   refused action with its reason, and open obligations.
5. List retained runs. Reopen one live when the current source matches its
   inventory, otherwise read-only from its database, and say which. From a
   live reopened run, offer only the next steps the actor programs permit.
   An unfinished run, closed after the diagnostic, continues from the next
   permitted step without repeating any computation, charge or admission.
6. Carry a permanent banner: deterministic researcher, synthetic data,
   disposable store, OS isolation unverified.

The demo that closes the milestone is in section 8. The milestone is not a
product, a deployment or a framework adapter. It produces no forward
standing and changes no admitted record.

## 2. Decisions required before code

Admitted on 2026-10-30 in the
[workbench authorization](../decisions/workbench_authorization_20261030.md).
The four items are kept here as the scope they fixed.

- **W1.** Authorize building and testing the workbench described here as
  disposable synthetic development under the addendum's workflow paragraph,
  lifting the first-cycle plan's "broad UI work" exclusion for this scope
  only.
- **W2.** Confirm that variant cohorts are declared synthetic Observations
  from the existing source `SRC-SYN`, each with its own `item_id`, carried
  into the run bundle as build artifacts. No new source declaration, grant,
  object kind or Transition class is created.
- **W3.** Confirm the standard library only, loopback only, no accounts, no
  cloud, no graph editor, no new dependency. A framework choice, if ever
  wanted, is a separate decision.
- **W4.** Confirm that the uploaded historical dataset and the LLM proposer
  named in the brief are out of scope for this plan and will each get their
  own plan. The first needs a new source declaration, which is an
  Authorization change.

If implementation finds that a variant needs a new identity rule, a new
evidentiary class or any non-zero delta, work stops and the exact provision
returns to the Principal.

## 3. Shape of the build

Three pieces under a new `workbench/` package. Nothing under
`adaptive_research_harness/` changes except the three actor functions in
section 4. Nothing under `docs/plans/research_cycle_admission_20261029/`
changes.

| Piece | File | What it is |
| --- | --- | --- |
| Session | `workbench/session.py` | A long-lived subclass of `acceptance.local.LocalRuntime`. Keeps core and tools alive between requests. Exposes the existing agent operations one at a time instead of running a scripted case. Knows which steps are permitted from the current state. |
| API | `workbench/api.py` | `http.server` on `127.0.0.1`, JSON in and out. Every read is a core query. Every write is an existing agent operation or Principal command. No direct SQLite write. |
| Page | `workbench/index.html` | One file, no build step, no external script. Five panes described in section 5. |

Retained runs stay where the fixture already puts them, under
`artifacts/development/<output>/<run_id>/`, with the output name set to
`workbench`. A run's page state is derived from the ledgers on every
request, so the page holds nothing authoritative.

### API

| Method and path | Does | Reads or invokes |
| --- | --- | --- |
| `GET /runs` | Lists retained runs with inventory digest, cohort, status, and whether live reopen is possible | Retained `E01.json`-style reports and `DISPOSABLE.json` |
| `POST /runs` | Freezes a bundle, starts core and tools, runs startup, observes the chosen cohort | `LocalRuntime.startup()` then `observe` |
| `GET /runs/{id}` | Status header: `N`, `E`, clock, inventory, cohort, labels | `state`, `clock`, `profile` |
| `GET /runs/{id}/sequence` | The seven stages with record references | `history` on both ledgers |
| `GET /runs/{id}/record/{ledger}/{seq}` | One record, full body | `get` |
| `GET /runs/{id}/controls` | Budget per grant, reservations, attempts, settlements, refusals, obligations | `budget`, `history`, `obligations` |
| `GET /runs/{id}/next` | The permitted next operations, each with the actor that would perform it | `state`, `obligations`, session rules |
| `POST /runs/{id}/step` | Performs one permitted operation | One of `research`, `choose-next-experiment`, `run-next-experiment`, `propose-hypothesis`, `check`, `policy-decide`, `apply`, `close-reservation` |
| `POST /runs/{id}/reopen` | Starts core and tools against a copy of the retained state when the inventory matches; otherwise loads read-only | `host('restart')` pattern, or `Store.events()` plus `reader.audit()` |
| `GET /runs/{id}/reader` | The independent reader's reconstruction | `acceptance.reader.read()` or `audit()` |
| `POST /runs/{id}/close` | Stops processes, retains state | `LocalRuntime.close()` |

The step endpoint refuses any operation not in the permitted list and
records nothing of its own. A refusal from the core is returned as the
core's own receipt, with its reason, and shown in the controls pane.

## 4. Harness changes

Smallest set, all inside the actor programs and the freeze step.

1. **Cohort catalog.** A new file `workbench/cohorts.json` holding the three
   cohorts as complete synthetic documents in the existing row schema
   (`event_id`, `exposure_id`, `shock_id`, `size_units`, `spike`,
   `selling`), each with a distinct `item_id` and date. `freeze.py`
   materializes it into the bundle as `artifacts.variant_cohorts` with a
   content digest per cohort, so each run's inventory names exactly which
   data it used.
2. **`actors.observe(client, date, form, cohort=None)`.** When `cohort` is
   given, the document is that cohort's content rather than a copy of the
   formation cohort. Everything else, including the listing, document and
   extraction commits, is unchanged.
3. **`actors.formation(client, profile, cohort=None)`.** Finds the
   observation whose document digest matches the named cohort's digest, or
   the formation cohort when none is named.
4. **`actors.research(client, tool, stop_after, cohort=None)`** passes the
   cohort to `formation`. **`actors.run_next_experiment()`** reads the cohort
   from the prior record's closure document instead of assuming the
   formation cohort, so the control runs on the same rows the first
   experiment used.

`next_experiment()`, the two tools, both Checkers, Rules, the engine and the
schema are untouched. Case `E01` is untouched and must still pass.

### The three cohorts

| Cohort | Construction | Researcher path | Expected outcome |
| --- | --- | --- | --- |
| `original` | The admitted 12-row cohort. Both large events share shock `s01`. | `complement-control` | 6 of 10 non-large rows show selling, below two-thirds. Broad claim not adopted. Narrow question registered. |
| `independent-shocks` | Same rows, except the second large event carries its own `shock_id`. | `independent-reproduction` | Tool B reproduces the counts exactly. The next action is to seek a new independent cohort. Registration proceeds. |
| `control-survives` | Original shock structure, with selling true on enough non-large rows that `3k >= 2n`. | `complement-control` | The broad claim survives its within-cohort control. Research failure is null. Registration proceeds with a different next action. |

The second and third paths exist in `actors.py` today and have no
end-to-end coverage. Section 6 adds it.

## 5. The page

One screen, five panes, no routing.

- **Run.** Cohort selector, Start, and the list of retained runs with Reopen
  on each. The banner from section 1 sits above everything and cannot be
  dismissed.
- **Sequence.** Seven boxes left to right. Each shows its stage name, one
  line of plain content and the record reference it rests on. Grey until the
  record exists. Clicking opens the record in the Evidence pane. The next
  permitted step appears as a button on the first grey box.
- **Evidence.** The selected record. For an observation, the rows as a
  table. For a research record, the counts and the question. For a selection
  record, the candidates with cost estimates, the chosen one, the rejected
  ones and the reason, in the researcher's own recorded words. For a Check,
  each criterion with its status and references. Where tool B reproduces
  counts on the same rows, the page says so in those words: an independent
  calculation, not independent evidence. Thresholds such as two-thirds are
  shown as the diagnostic the researcher applied, not as statistical proof.
- **Controls.** One row per grant: committed, reserved, headroom. Below it,
  every reservation, attempt and settlement in order, then every refusal
  with its reason, then open obligations.
- **Reader.** The independent reader's result for the run: reconstructed or
  not, `N`, `E`, pending attempts, binding states, preserved refusals.

No chart is needed for the milestone. Numbers are shown as counts beside
the rows they were computed from.

## 6. Order of work

Each step has an exit criterion and is complete only when it holds. The
motion is the repository's `Audit -> Plan -> Implement -> Verify`.

| Step | Work | Exit |
| --- | --- | --- |
| S1 | Cohort catalog and the four actor changes | `E01` passes unchanged. New component tests drive all three cohorts through `research`, `choose-next-experiment` and `run-next-experiment` in the fixture and assert the path and counts in section 4. The reader reconstructs each. |
| S2 | Session | A test starts a session, performs the eight steps one at a time on the original cohort, and reaches the same `N`, budgets and records as `E01`. A refused step out of order returns the core's refusal and leaves `N` unchanged. |
| S3 | API | Every endpoint in section 3 has a test. No endpoint writes to SQLite directly. Bound to loopback only. |
| S4 | Page | Loads from the API with no external resource. The sequence pane renders all seven stages for a completed original run. The banner is present on every state. |
| S5 | Reopen | A run closed in one process is listed, reopened live in a new process under the same inventory, and offers only the permitted next step. The same run under a changed inventory loads read-only, labelled so, with the reader result. |
| S6 | Demo script | The demo in section 8 runs end to end from a shell command as an acceptance case named `W01`, with its report retained like `E01.json`. |
| S7 | Records | `BUILD.md` gains a workbench section with the same honesty about limits. An independent reviewer audits S1 to S6 against this plan and the audit's findings. The README's "What exists" section is updated only after that audit. |

Order matters. S1 is harness work and can be verified without any page.
Nothing in S2 to S5 starts until S1's tests pass.

## 7. Trust and limits, stated up front

- The workbench process is the fixture driver. It holds every actor token
  and plays every role. This is the acceptance fixture's trust model and
  carries no OS isolation claim. The page never sees tokens or paths.
- The server binds to `127.0.0.1` and has no authentication because it has
  no users other than the person who started it. Binding elsewhere is out
  of scope.
- Live reopen requires the current source to match the run's inventory.
  Runs from older inventories are read-only. The page says so.
- The researcher is a fixed policy with two candidates and one method id.
  Nothing here makes it an LLM, and the banner says so.
- Each run adds a bundle directory and, when the digest is new, a source
  snapshot under `artifacts/development/`. These are disposable evidence.

## 8. The demo that closes the milestone

Observable facts, each checkable from the page and from the retained
records.

1. Start a run on `original`. The sequence fills to the diagnostic. The
   Evidence pane shows both large rows carrying shock `s01` and the
   researcher's recorded reason that one shock is not independent
   repetition. The control runs, shows 6 of 10, and the broad claim is not
   adopted. Check passes, P-1 decides, Apply consumes the binding. Controls
   show 2.00 committed on `AU-RP-1` and 4.25 on `AU-CK-A`.
2. Start a run on `independent-shocks`. The diagnostic chooses
   `independent-reproduction`. Tool B reproduces the counts. The next action
   is to seek a new independent cohort. Registration proceeds.
3. Start a third run on any cohort and stop after the diagnostic. Close the
   server. Start it again. All three runs are listed. The unfinished one
   reopens live, offers only the control experiment as its next step, and
   completes with the same attempt count and charges as an uninterrupted
   run. The two completed runs open live with no permitted mutating step.
   The Reader pane shows `RECONSTRUCTED` for all with zero pending attempts.
4. Modify one covered source file in a scratch copy and start the server
   from it. Both runs are listed read-only and labelled so.

## 9. Exclusions

Accounts, cloud or remote deployment, a graph or workflow editor,
infrastructure beyond one process, any dependency outside the standard
library, an LLM proposer, uploaded or real data, a new source declaration,
framework adapters, charts, changes to Checkers, tools, Rules, engine or
schema, and any edit to admitted records or the admission packet. The
presentation under `docs/presentations/demo/` is not reused.

## 10. What follows, separately

One real research question on an uploaded historical dataset. That needs a
declared non-synthetic source, which is an Authorization change and a
Principal decision, and a statement of what evidentiary class the upload
carries. It gets its own audit and plan after S7. An LLM proposer comes after
that, when there is a bounded task for it and a Checker that can recompute
what it proposes.
