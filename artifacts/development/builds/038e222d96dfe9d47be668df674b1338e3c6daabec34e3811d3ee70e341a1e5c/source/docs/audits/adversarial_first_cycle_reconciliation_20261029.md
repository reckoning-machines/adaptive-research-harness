# Adversarial First-Cycle Review — Finding-by-Finding Reconciliation

Status: **AUDIT EVIDENCE; NO IMPLEMENTATION, ADMISSION OR CERTIFICATION.**

Date: 2026-10-29. Codex reconciles
[Claude's review](adversarial_first_cycle_plan_review_20261029.md) against
admitted CV1/decisions, the original reviewed plan, and the **later complete
setup packet** present in this checkout. The review is preserved verbatim.
The Principal's subsequent direction retains ten designs and requires proof
that an original worker cannot still dispatch before treating retry as safe.

“Accepted” concerns the supported failure, not automatic acceptance of its
remedy. “Already resolved” identifies an exact existing setup provision;
“corrected” means a document correction, not tested runtime enforcement.
Remaining decisions are only D1–D3 in the
[consolidated packet](../decisions/first_research_cycle_build_decision_proposed_20261029.md).

Evidence abbreviations:

- **C**: [admitted CV1](../doctrines/new_speedway_constitution.md), exact SHA-256
  `c56a9cf50a7e9efadad8f2f2be6605e82c758f18d4096ba07eaaf86a8f8b7a64`.
- **G**: [CV1 admission](../decisions/cv1_admission_20261019.md), especially
  “Outstanding pre-genesis parameters”; **PD9**:
  [genesis record](../decisions/principal_decision_009_genesis.md), including
  its appended PD-010 amendments.
- **P0**: [exact reviewed implementation-plan bytes](../plans/research_cycle_reconciled_20261029/reviewed_inputs/first_research_cycle_implementation_20261029.md.txt);
  line numbers in Claude's table still refer to this version. The current
  [plan](../plans/first_research_cycle_implementation_20261029.md) is revision 2.
- **SC**: existing [setup specification](../plans/research_cycle_admission_20261029/setup_specification.md);
  **CK**: existing [Checker contract](../plans/research_cycle_admission_20261029/checker_contract.md);
  **HP**: existing [host/protocol contract](../plans/research_cycle_admission_20261029/host_and_protocol.md);
  **AM**: existing [proposed amendments](../plans/research_cycle_admission_20261029/amendments.md).
- **RC**: current [exact corrections](../plans/research_cycle_reconciled_20261029/contracts.md),
  incorporated into the revised plan and
  [acceptance specification](../plans/first_research_cycle_acceptance_20261029.md).

All earlier plan/packet/approval bytes have exact `.txt` snapshots under
`reviewed_inputs/`; snapshots are evidence, not current instructions. The
old manifest bound earlier plan bytes and is historical, not the current
approval manifest. No later packet is treated as already admitted merely
because it was written.

## 1. Review scope and startup findings

| Finding | Disposition | Latest-packet status and exact evidence | Correction or remedy disposition |
| --- | --- | --- | --- |
| Checkout statement: no admission packet, only HTML non-Markdown files | Partially accepted | No core/runtime test exists. But the current packet has `setup.json`, `designs_and_methods.json`, CK, HP and a manifest; repository presentations also have other assets. These are specifications, not runtime enforcement | Treat absence-of-packet claim as stale for this reconciliation, not evidence of missing code. Preserve the review rather than rewriting its observations |
| S1 — bootstrap Checker cannot check startup | Accepted | **Already resolved in latest packet:** CK §3 enumerates initial Observation/Research/Checker grants, initial limits, Research/Checker designs, Theme, Hypothesis and revocation; CK §1 charges each computed invocation; SC §4 specifies 16 funded Checks. C Part V rows 1612–1621 require these classes. P0 §5 remained narrower than CK | Propagate full matrix into current plan §5. Retain S01–S08; add only the exact existing P-1 suspension control needed by A10. No canned startup PASS |
| S2 — authorization/artifact-hash circularity | Accepted | **Still open in latest packet:** SC §1 items 1–2 defer executable hashes to a build inventory, but the old approval §3/§4 authorizes startup without a separate approval of those unknown bytes. G explicitly requires exact design content hashes before their genesis acts | **D1:** approve building/offline validation first; after building, separately approve exact run inventory before any Apply 0, including fixtures. Correction is ordering of authority, not merely filling hashes later |
| S3 — reservation identity/order | Partially accepted | **Still open:** P0 §5 says “allocate the reservation identifier” before the immutable proposal. C §III.5 lines 659–665 requires purpose “a Transition already proposed”; P-1(b), lines 1653–1655, requires reservation “named in the proposal” and committed before Check. C's object table identifies Evidence by EvidenceId/commit sequence; it never specifies the proposed client reservation namespace | Accept the unsupported client-ID shortcut. Reject the claim that client ID or purpose-only matching are the only remedies. **D2 recommends prospective numeric Evidence sequence, conditional append and fail-closed collision**, detailed in RC. No slot/budget is reserved before commit; no immutable proposal is edited; exact sequence/actor/grant/purpose is checked. Explicit Principal confirmation is required; this interpretation is not asserted admitted |
| S4 — missing Observation identity | Accepted | **Already resolved:** HP §1 assigns UID 20002 `harness-observe`, mapping it to Observation under AU-OBS-1; tool UIDs have no command access. `setup.json` grant AU-OBS-1 permits Observation forms only. C Part II and Part V make that function the caller | Propagate into plan §4 and C07; no weakening of R13. Core recovery cannot impersonate the Observation UID |
| S5 — Theme formation before source commit | Accepted | **Already resolved:** SC §4 expressly commits formation feed/DOCUMENT after Apply 1 and before TH-G1; `setup.json.theme.content.motivation_closure` names that exact committed DOCUMENT. C §III.1 requires a motivation closure; P0 worked step 1 misleadingly delayed all observations until setup completed | Correct current plan worked step 1. Do not adopt an empty-closure shortcut or invent a placeholder Evidence sequence |
| S6 — synthetic provider diversity | Accepted | **Specified, still awaiting decision:** AM A1 explicitly says deterministic programs do not satisfy PD9 §3's different-provider supplement and proposes an exact scoped exception including Principal controls. C §III.8 lines 1229–1253 defines three independence conditions and allows extra provider conditions as grant content | **D3:** approve that existing narrow supplement exception and A2's local-tool narrowing as future grant specifications. No fake provider provenance; all CV1 independence conditions remain. Runtime grants still require exact-artifact run approval and lawful startup |
| S7 — researcher attribution | Partially accepted | Existing `designs_and_methods.json` supplies ten immutable instruction/profile templates and tool/method bindings; SC §1 requires eventual executable hashes. That is a legitimate specification, not evidence that a process exists. It did not sufficiently exclude a driver composing the positive proposal under researcher credentials. C §III.4 defines exact instructions/tools/inputs/outputs and C §III.7 grants a design or human role, not an arbitrary script using its name | **Corrected:** RC specifies actual pinned researcher programs and AD-R1's derivation from committed input/result into proposal, including negative branches; C07 inspects executable → peer → records. Choose the intended executable research design; do not add a human-role grant or ask a new authority question for an ordinary implementation choice. Exact binaries require D1's later run approval |
| S8 — shared recomputation bug | Partially accepted | **Already resolved:** CK §1 expressly prohibits imports of researcher calculation, core admission predicates, other Checker criterion functions or expected results; `CHECK-A-1`/`CHECK-B-1` specifications independently recompute. P0 did not make that boundary explicit | Propagate prohibition. **Reject the proposed mandatory A-for-B/B-for-A remedy:** it still shares research-tool implementation defects and supplies no startup grant/limit judgment. Keep independent narrow Checker code and source/import inspection; no claim of independent human authorship |

The review's observation that CK-B is not exercised is stale against CK S06,
which routes an actual CK-A/grant-chain change to CK-B; revision-2 acceptance
makes that execution explicit. Registration of an idle Checker alone proves
no working own-subject route.

## 2. Authority, concurrency and recovery findings

| Finding | Disposition | Latest-packet status and exact evidence | Correction or remedy disposition |
| --- | --- | --- | --- |
| A1 — tool inherits core UID | Accepted | **Already resolved:** HP §1 assigns tools UIDs 20101/20102, separate sockets and root-managed units, and says core cannot setuid/spawn Principal/Checker. P0's “service launches” was inconsistent with that concrete arrangement | Correct plan: core contacts fixed tool units. Do not launch tools from the researcher UID either: that could expose researcher credentials/commands. T06 must show OS denial for the actual tool UID |
| A2 — service recovery grants itself caller rights | Accepted | Latest HP command table restricts settlement to original grantee/former grantee or Principal, but its generic recovery and P0 §7 left the mechanism ambiguous. C Part V assigns BIND/RELEASE to Apply boundary; C settlement lines 718–724 grants no service-as-grantee right | **Corrected:** RC limits core recovery to inspection/Apply-owned continuation. Principal uses authenticated Principal client; grantee/Checker/Observation executes its own pinned client. C07 rejects `acting_as` and label-only recovery |
| A3 — caller-selected P-1 decision | Accepted | HP table already says “Principal or internal P-1 only,” but P0 table exposed a “P-1 role” caller. C Part V lines 1646–1666 gives this policy to the Apply boundary, with conditions against the head at Apply | **Corrected:** only Apply/continuation creates a P-1 decision; requests can ask it to evaluate. Recheck every predicate at Apply. No caller-supplied `decider=P-1` authority |
| A4 — host-dependent guarantee split | Partially accepted | **Already substantially resolved:** HP §1 states trusted root/core, separate peer UIDs, no same-UID isolation claim and no arbitrary hostile-code sandbox. The review's classification of all R02–R11 as purely ledger logic overlooks R04's former-grantee authentication | RC/acceptance identify logical and OS portions separately. An ingress-only caller type is useful against accidental misuse, **not** a Python security boundary. Keep both logical and real host witnesses |
| A5 — request-key concurrency | Partially accepted | **Durable part already resolved:** HP §2 says receipt/events commit atomically and binds `(authenticated principal, request_id)` plus bytes. But no precise singleton/old-worker mechanism was given. SQLite commit serialization does not serialize tool execution | Keep durable uniqueness for all mutating commands; add lifetime OS writer exclusion and unique dispatch claims. **Reject** dropping all in-flight coordination or inventing one Research Record per attempt. Domain duplicate predicates complement delivery identity; they do not deduplicate every effect or prevent dual handoff. C01–C03 exercise live concurrency |
| A6 — never-dispatched recovery proof | Partially accepted | **Conservative branch already allowed:** HP §5 says ambiguous fresh handoffs may always use uncertainty; C §III.5 lines 709–717 says missing response is not non-dispatch proof. The proof branch was optional/unspecified, not a demonstrated resume capability | Explicitly unsupported in fresh recovery. **Reject marker absence as proof** while old processes/queued work can act. Retain a claim only as duplicate suppression/uncertainty evidence. Require actual old-generation/channel quiescence before replacement; settle receipt/UNKNOWN, then new funded attempt. C04 holds an old worker alive to test it |
| A7 — settlement during clock outage | Partially accepted | C §III.5 admits valid pending settlement notwithstanding expiry/fence/revocation; its fields require identity/units/provenance, not a fresh expiry eligibility finding. Evidence timestamps apply “where the kind carries one” (§III.5 opening). Neither P0 nor HP enumerated the exact read policy | **Corrected:** RC table makes settlement clock-independent without inferring expiry or releasing a frozen bind. Fresh reserve/attempt/BIND/elapsed invalidation still need clock. Do not infer from the audit that all commits or all settlement-related queries can ignore time. C06 verifies both sides |
| A8 — reservation expiry origin | Accepted | `setup.json` supplies 604800000 ms default, but HP `reserve` accepts expiry without an explicit upper bound. C §III.5 requires an expiry; §III.7 makes the default grant content | **Corrected implementation-profile restriction:** omitted expiry becomes t+7 days; provided expiry must be in (t,t+7 days]. It never extends grant expiry. No new constitutional universal expiry default; C06 supplies an overlong request |
| A9 — monotone clock | Partially accepted | **Already resolved in backend:** `setup.json.clock.advance` is monotonic; HP §5 rejects backward advance, fsyncs tick state and refuses reset after loss. P0 alone was incomplete | Add comparison to greatest durable receipt to detect restoration of an older clock file; C06. This is the declared synthetic clock's contract, not a new evidentiary time authority |
| A10 — P-1 suspension race | Accepted | Missing from the original acceptance; C Part V lines 1670–1673 explicitly allows Principal suspension by Transition; §III.8 Apply predicates preserve it | Add B12 with real checked Principal control, Apply refusal/invalidation, RELEASE and preserved suspension. Include only that bounded existing control in Checker/code scope. Rechecking does not itself unsuspend P-1 or make fresh binding lawful |
| A11 — attempt/input/reproduction fields | Partially accepted | **Partly already resolved:** HP §3 supplies canonical bytes; SC supplies corpus/tool/method hashes; CK §2 requires Historical Reconstruction finding. C §III.5 attempt tuple and Research Record row require fixed input identity and reproducibility content. Exact step catalog/hash scope was still missing | RC supplies step tokens and canonical invocation-byte scope excluding dispatch index/request key, plus exact dataset/cutoff/parameters/reproducibility binding. Plan `research.record` now names all fields; historical finding retained. No new governed identity introduced |

## 3. Complexity recommendations

| Recommendation | Disposition | Evidence and chosen treatment |
| --- | --- | --- |
| Reduce ten Research designs / SRC-E / setup Applies | Partially accepted as a possible future reduction; **not adopted** | PD9 admission header admits enumerated choices only; ten is not in that short list. But the later **admitted G parameter table explicitly names `AD-R1.0` to `AD-R10.0` and SRC-E/SRC-SYN**, and PD-010 choice 13 calls the initialization order an approved sequence. CV1 itself requires only three bootstrap items. Therefore ten is not a universal constitutional cardinality, but deleting it is not an unapproved implementation simplification. The Principal now expressly retains ten |
| Drop request-key in-flight coordination | Partially accepted | Durable unique-key enforcement is required; memory cannot be authority. Yet serialized dispatch and actual worker exclusion still matter. Keep simple in-process queues as ephemeral mechanisms plus the durable/OS protections; do not confuse the two |
| Drop tool receipt storage | Rejected as a required correction | UNKNOWN may equal the ordinary fixed tariff, but an exact retained receipt can recover successful or failed evidence and attribution. It owns no ledger effect. Retain the already specified narrow store; no general provider receipt service or spending authority added |
| Remove role-bearing generic recovery | Accepted | Restrict core to its own continuation; exact correction under A2, C07 |
| Replace six reads by two | Rejected as necessary work for this reconciliation | The current reads distinguish exact records, as-of projections, budgets, obligations and request receipts. Multiple convenience selectors do not create authority. Their shared exact-reference/as-of implementation can be factored during coding; no user decision or interface redesign is needed to fix the reported failures |

**Smallest setup conclusion.** Under the instructions actually in force, the
smallest authorized target remains the seventeen-Apply setup, with one
ordinary researcher active. With a new explicit scope decision, CV1 could
support the review's eight-Apply sequence (one researcher, two Checkers,
synthetic source only). That is not a reduction currently approved. It would
also need to preserve the existing distinct-grantee shared-budget witness;
one grantee under a 100 cap cannot demonstrate independent lineages competing
for the 600 pool. Keep ten and the existing R02 lawful funding schedule.
No setup-reduction decision is put before the Principal in this packet.

## 4. Remaining decisions and verification boundary

D1 separates build from exact-artifact initialization/run; D2 confirms an
explicit reference-ordering construction using existing sequence identity;
D3 approves the existing synthetic grant supplement exception and narrow
initial tools. All other accepted gaps have concrete document corrections or
already exist in the latest setup. Numerical setup/host choices are not sent
back as unanswered questions. These are not runtime fixes: no core exists.

The current plan, acceptance specification and RC replace conflicting older
prose. The previous proposed all-in-one approval is explicitly superseded;
it was never admitted. The current manifest and exact build approval are in
the single remaining decision record. Admitted bytes and historical audits
are preserved. Build permission cannot be read as permission to initialize
unknown future artifacts. After the later exact-artifact run approval, the
coding assignment continues directly to the prescribed acceptance evidence,
not another general architecture review.
