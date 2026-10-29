# First-cycle build audit: fixes and executed evidence

Status: **PRIVATE DISPOSABLE DEVELOPMENT — APPLICATION TESTS PASS; OS ISOLATION UNVERIFIED.**

This reconciles [Claude's build audit](adversarial_first_cycle_build_audit_20261029.md)
under the Principal's superseding development authorization. No new approval
packet or constitutional amendment is proposed. CV1 bytes are unchanged.

Evidence:

- [Full cooperative suite](../../artifacts/development/final-audit/75269ddd9d5a4cab880e66bbcef9fa67/summary.json): **77 scenario executions passed**, including 20 death schedules, two forced terminal orders and X01–X05 audit regressions. Inventory `e34ce45e3460fc0da6d2f7989eb3ae32c3eb4897b4f120470d8836075e7bcd0d`.
- [Finished example](../../artifacts/development/finished-example/47d0103061cd4f0983b011f50af3590d/E01.json) and [46 passing unit/component tests](../../artifacts/development/finished-example/47d0103061cd4f0983b011f50af3590d/unit-results.json): inventory `cbb9715806dd670c4603cd7ed413c86cfda18e814b6af38ab7989076142d3509`. The harness's complete application-code hash map is identical to the full-suite build. Subsequent changes affect evidence utilities and an expanded X03 test recipe, separately rerun below.
- [Expanded final X03/X05 regressions](../../artifacts/development/final-regressions/00cc9326c1e74b3591044f144efb6e40/summary.json) and [46 current unit/component tests](../../artifacts/development/final-regressions/00cc9326c1e74b3591044f144efb6e40/unit-results.json) pass under `da7c09d770fe6b62e0b829a529f784387d28bba5070ceeb042912254de4523d2`. X03 additionally verifies that a scientifically passing marked test candidate cannot be admitted by P-1 or the Principal.
- [Retained full-suite database/state index](../../artifacts/development/final-audit/75269ddd9d5a4cab880e66bbcef9fa67/retained-state-index.json): all 77 states copied with file hashes; original test reports were left unchanged.
- [Before-fix integration regressions](../../artifacts/development/audit-before/992335ea6d374c06b51297d8b61c625c/summary.json): X02, X03, X04 failed on archived pre-fix code. [Before-fix unit replay](../../artifacts/development/audit-before/unit-regressions-before.json): F6, F7 and F16 failed against that archived source; executable/test bytes were unchanged in the replay. The earlier F1 wrong-binding probe is retained under `artifacts/development/regression-before/`; it predates complete source archiving and is not retroactively presented as reproducible source evidence.
- [Traceability regression](../../artifacts/development/finished-example/47d0103061cd4f0983b011f50af3590d/traceability-regression.json): old report lacks a source snapshot; current report supplies its exact inventory, file list and snapshot. Earlier evidence is retained, not silently updated to describe new code.

These are executed application tests, not certification of CV1 or the Linux host.

| Finding | Disposition and exact resolution |
| --- | --- |
| F1 | **Accepted, fixed.** `engine._commit` invalidates only the binding of the Transition and decision actually undergoing Apply, excluding pre-admission request failures. X01 presents another Transition's binding, gets one refusal, retains FROZEN, then correctly applies that other Transition. B03/B06 retain atomic legitimate refusal/invalidation. |
| F2 | **Accepted; remedy modified.** CV1 §III.8, “Apply binding, terminal disposition and invalidation,” permits only the Apply continuation and explicitly gives proposers no discretionary cancellation route. `engine.command` and `service.core_handler` therefore restrict continuation triggers to the Principal-operated internal continuation. They do **not** grant the proposer generic invalidation/release/recovery privileges. Ordinary proposer Apply remains. Committed events contain real `requester` and `acting_role=@Apply`. X02 rejects other researchers **and the proposer**, then verifies lawful attribution. Unauthorized domain requests remain preserved refusals rather than being erased as suggested by the audit's no-event remedy. |
| F3 | **Accepted, fixed.** Both actor entrypoints reject generic adversarial `propose`/`research-commit`. `actors.propose_mutated` derives its base from the actor's own committed Research Record, applies explicit test mutations, and permanently marks adversarial origin. Such candidates cannot be admitted. C05/R14/S05/S08 use this route. X03 rejects the original driver-proposal bypass; the independent reader validates real or marked origin. |
| F4 | **Accepted; no grant-byte rewrite.** `rules.independence` reads the existing exact exclusion declarations and their successor chains. Reservation and attempt admission enforce them before work. X04 preserves zero additional reserved/committed cost; R12/S06 now expect the earlier refusal. The proposed general structured exclusion language is unnecessary for these two approved synthetic declarations. Unknown declaration syntax remains unsupported. |
| F5 | **Accepted; workflow remedy superseded.** No manual digest approval or replacement packet. Every run generates a unique bundle, exact file hashes and complete source snapshot. Reports are unique and retained. X05 checks archived bytes and actual candidate-byte alteration; source changes during a run fail verification. The generic build command also uses a fresh destination. Older reports remain explicitly weaker historical records. |
| F6 | **Accepted; relaxing emptiness rejected.** Rejected pre-genesis requests are durable operational command receipts, outside both governed ledgers. Corrected genesis requires a fresh request key and literally empty governed ledgers. No exception ignores refusal-only governed histories. Focused unit test verifies refusal lookup, both empty ledgers, then exact Apply 0. |
| F7 | **Accepted, fixed.** `acceptance.reader` independently reconstructs supported authority, funding, allowance/cap, Check/decision/Apply, binding, invalidation and release relationships from history, without core predicates. Evidence admission witnesses pin E/N. Six corrupted-history mutants are rejected; genuine histories pass. Legacy histories without witnesses are explicitly reported weaker. The reader runs in a fresh process. |
| F8 | **Accepted coverage limitation.** B10 is explicitly **SUBSTITUTED** by whole-core outage, not a ledger-specific failure. Constitutional NOT DETERMINABLE/STOP is **UNREACHABLE** in this bounded Checker language. Neither is claimed as a completed original witness. |
| F9 | **Per-grant reset remedy rejected.** CV1 §III.5, accounting paragraph, defines lineage sums over the lineage's reservations, including pending maxima of closed reservations; I-5 retains consumed research budget. A successor is not a cap reset. `test_cross_grant_lineage` retains this conservative interpretation. No future grant semantics are invented. |
| F10 | **Accepted, fixed in scoped domain routes.** Early Apply authorization/no-proposal refusals and NOT_INITIALIZED requests are preserved; pre-initialization receipts stay operational. Pre-genesis unauthorized calls are also preserved without poisoning ledgers. Malformed wire input and unavailable transport remain operational errors, not fabricated constitutional events. |
| F11 | **Accepted, fixed.** Worker `describe` occurs outside the write lock/transaction; claim eligibility is rechecked inside. The actual worker rejects a handoff naming another generation. Concurrency/claim and paused-worker cases pass. |
| F12 | **Historical gate objection superseded.** Both private-development permission paths perform automatic traceability, not a separate human approval. Linux entrypoints retain UID checks and runtime grants. The suggested platform/UID prohibition would obstruct authorized disposable testing and is not adopted. |
| F13 | **Partly accepted, partly improved.** Final record reading is now a separate process; candidate integrity testing changes actual copied source bytes. Local actor attribution remains cooperative and local quiescence covers only owned, killed-and-joined fixture processes. No UID, credential or cgroup security is inferred. |
| F14 | **Accepted limitation.** Tariffs, dates and thresholds implement the exact synthetic profile; there is no claim to interpret arbitrary future grants. Generalizing configuration is outside the agreed first cycle. |
| F15 | **Accepted test gap, addressed by integration.** Real startup/cycle/death tests now execute all the listed admission predicates against SQLite and actor processes. Focused regressions supplement the unit suite; they do not duplicate each implementation branch with a mirror test. |
| F16 | **Accepted, fixed.** `host.still_alive` treats only positive OS evidence of absence as dead. Permission/read/generation failures become WORKER_NOT_QUIESCENT. The regression failed before the fix and passes afterward. Actual Linux hidepid/UID behavior is unverified. |
| F17 | **Accepted limits, no new host project.** Source/interpreter hashes and Python/SQLite/build-platform versions are recorded; this is not a complete native-library or OS measurement. No target Linux fingerprint exists. Attempt generation data is historical operational provenance, never part of the reservation/step/input/index identity or authorization. |
| F18 | **Accepted current-scope behavior.** A1 is deliberately synthetic-only and truthful no-provider provenance is required. Real-provider grant generalization is excluded by the Principal. |

## Remaining coverage and practical result

No suitable local Linux VM is registered (`limactl list --json` reports none).
T06 is **UNEXECUTED**. R01/R12/R13/T07 exercise cooperative application behavior;
their OS-attribution/security portions remain **UNVERIFIED**. B10 and STOP limits
are stated above and recorded in the machine-readable reports. The independent
reader checks the supported synthetic contracts, not every possible CV1 judgment.

The example asks whether larger synthetic shocks warrant a narrower selling
hypothesis. Actual counts are n=12, k=8, n_large=2, k_large=2. A and B cost
2.00 simulated units total; registration checking costs 0.25, separate from
4.00 startup Checker cost. An independently computed Check, P-1 decision and
Apply produce N=17, no pending liabilities, and no forward/economic standing.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m acceptance.local --example
```

No real provider/spending, trading, production changes, public release or license
selection occurred. No known confirmed audit blocker remains in the exercised
synthetic cycle; the unverified and unreachable coverage is not hidden as a pass.
