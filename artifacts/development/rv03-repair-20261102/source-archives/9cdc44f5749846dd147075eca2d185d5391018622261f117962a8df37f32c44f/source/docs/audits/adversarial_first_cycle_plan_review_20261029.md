# Adversarial Review — First Research-Cycle Plan and Checkout State

Status: **AUDIT EVIDENCE — DOCS-ONLY CHECKOUT; RUNTIME CORRECTNESS UNTESTED; NOTHING ADMITTED OR CERTIFIED.**

Date: 2026-10-29. Reviewer: Claude (Fable 5.1), at the Principal's
direction. Scope: the proposed
[implementation plan](../plans/first_research_cycle_implementation_20261029.md),
its [acceptance specification](../plans/first_research_cycle_acceptance_20261029.md),
the [feasibility audit](feasibility_coherence_public_library_20261029.md),
the [rename and plan verification](rename_and_research_cycle_plan_verification_20261029.md),
and any implementation present, read against the admitted
[CV1](../doctrines/new_speedway_constitution.md) at SHA-256
`c56a9cf50a7e9efadad8f2f2be6605e82c758f18d4096ba07eaaf86a8f8b7a64`,
[PD-009](../decisions/principal_decision_009_genesis.md) as amended, and the
[CV1 admission record](../decisions/cv1_admission_20261019.md). The brief
asked for concrete ways the proposed system could violate its own
contracts and for complexity that makes a correct implementation harder.

## 1. Checkout state and limits of this review

Working tree at HEAD `75036e0` plus untracked files. `test.py` is zero
bytes. The only non-Markdown files are two HTML presentation demos under
`docs/presentations/demo/`, which their own README labels as not the
system. No package, module, test, database, dependency manifest, admission
packet or execution record exists.

**Runtime correctness is untested.** Every finding below concerns the
proposed design. No witness was run because there is nothing to run. The
presentation was not treated as an implementation, and its absence is
stated here once, not repeated as findings.

Line references are to the files as they stand at this date: "plan" is
the implementation plan, "acceptance" is the acceptance specification,
"CV1" is the Constitution.

## 2. Findings: startup and independence

| ID | Finding | Evidence | Required resolution |
| --- | --- | --- | --- |
| S1 | **The deterministic Checker as specified cannot pass Apply 1; startup halts at sequence 1.** The plan scopes the Checker to "a narrow, explicit synthetic hypothesis template family" and says out-of-capability content produces no `PASS`. The mandated setup needs criterion-level Checks of five other classes: Authorization grant and revocation, Limits, eleven Agent Design registrations and a Theme registration | plan 282–288, 65–73, 35–38; CV1 1612–1621 | Plan edit: the Checker capability and the packet enumerate every class the setup and the in-scope revocation require |
| S2 | **Cut 0 is circular.** It requires exact design and tool hashes and explicit coding authorization before cut 1, but `AD-CK-1.0` is the deterministic Checker that cut 1 builds | plan 453, 115 | Plan edit: plan admission authorizes coding; a separate genesis-packet admission with hashes follows cut 1 and precedes cut 2 |
| S3 | **Proposal-names-reservation ordering is a Principal decision, not a serializer choice.** `P-1(b)` requires the reservation "named in the proposal" and committed before the Check; a reservation's purpose must be "a Transition already proposed"; a `RESERVATION` carries no identity besides its sequence; T-A names the reservation by sequence 2 290 inside the proposal, which cannot be known before the reservation commits. The plan resolves this with a client-allocated reservation identifier. That is a new identity rule on an Evidence record: a stop condition under `AGENTS.md`, and inconsistent with the plan's declared `ΔO=0`. Matching by purpose alone is a materially different implementation | CV1 1653, 663–664, 659–662, 1705; plan 246–249, 512 | **Principal decision**: admit a client-chosen reservation identity, or rule that the proposal names its funding by purpose match only |
| S4 | **The Observation function has no identity in the trust model.** §4 lists Researcher, Checkers and the Principal client only, yet cycle step 1 needs the Observation function to commit the `SRC-SYN` corpus under `AU-OBS-1`. If the service commits it in-process, the R13 witness that a wrong Evidence caller is refused is self-attribution | plan 159–166, 406–409; acceptance R13 | Plan edit: name the Observation function's identity, or state it is a service-internal function committing pinned fixture bytes and exclude R13's caller refusal from the isolation claim |
| S5 | **Theme ordering.** `TH-G1` at Apply 16 carries a motivation closure of committed Observations, but the corpus is committed after setup at cycle step 1 | CV1 273–287; plan 406 | Plan edit: commit the corpus between Apply 1 and the proposal of TR-16, or state that an empty closure with declared origin is lawful for a Principal-registered Theme |
| S6 | **Provider diversity is unsatisfiable honestly in a no-provider milestone.** PD-009's admitted supplement makes "provider different from any proposer it checks" content of `AU-CK-A`. Researcher and Checker are both deterministic code. Honoring it "in the supplied synthetic design provenance" is invented provenance | PD-009 130; plan 189–191; CV1 1251–1253 | **Principal decision**: a recorded choice to omit the supplement from grants to designs that have no provider; it is Authorization content and was an enumerated PD-009 choice |
| S7 | **What `AD-R1.0` is must be stated.** The cycle has the Researcher reserve, run a tool and compose an immutable Hypothesis proposal. If a test driver or a person at the CLI composes it under the researcher credential, the registered artifact is fiction and attribution is a label. The nine never-run designs have the same problem | plan 411–419, 70; CV1 483–485, 957–958 | **Principal decision**: `AD-R1.0` is an executable artifact deriving the proposal from the committed Research Record, or a Research Authorization is granted to a human role |
| S8 | **Checker recomputation can share the bug it checks.** If the Checker's independent recomputation links tool A's code, a shared defect passes | plan 274, 316–318 | Plan edit: the Checker recomputes with the other implementation, B for A's result and A for B's; no third implementation |

Own-subject routing is satisfied for the setup as written: sequences 13
and 14 and the revocation of `AU-RP-1` do not concern `AD-CK-1.0` or
`AU-CK-A`. `AD-CK-2.0` is admitted and never exercised in this milestone.

## 3. Findings: authority, concurrency and recovery

| ID | Finding | Evidence | Required resolution |
| --- | --- | --- | --- |
| A1 | **Tool launch contradicts T06.** The service launches tool executables; a subprocess inherits the service's user and therefore the database file access T06 says the tool must lack | plan 172–173; acceptance 119 | Plan edit: specify a privilege drop, or launch tools from the researcher's client process |
| A2 | **Recovery "under the exact role required" is an internal label path.** CV1 gives the Principal a settlement right and the Apply boundary `BIND`, Apply and `RELEASE`; nothing gives a service process a grantee's rights | plan 389–393; CV1 718–721, 764–767 | Plan edit: `recovery.continue` is limited to inspection, Principal settlement and the Apply boundary's continuation; grantee-owned continuations run in the grantee's own process |
| A3 | **"P-1 role" as a caller of `transition.decide` invites a bypass.** CV1 has the Apply boundary evaluate `P-1` at Apply against the head | plan 232; CV1 1646–1662 | Plan edit: only the Apply boundary or its continuation role produces a `P-1` decision event; no caller names the decider |
| A4 | **Host-dependent guarantees, exactly.** R01, R04 former-grantee authentication, R12 proposer/Checker separation, R13 tool-caller refusal, T06 and T07 hold only in the reference arrangement. R02–R11, R14–R16, B01–B11 and T01–T05 are ledger logic that holds in cooperative mode. An in-process import of `transitions` and `evidence` gets logic guarantees only | plan 152–182; acceptance §2, §3, §5 | Plan edit: state the split; make caller attribution a type only the ingress module can construct |
| A5 | **In-memory request-key serialization does not survive two service instances.** "Wait until the original service process is known dead" has no mechanism. SQLite already serializes every identity-bearing commit and CV1 supplies `DUPLICATE_ATTEMPT`, `ALREADY_SETTLED`, `ALREADY_BOUND`, `ALREADY_APPLIED`, `ALREADY_RELEASED`. Only `research.record`, `observation.commit` and a non-client-fixed `transition.propose` need a key | plan 255–256, 266–270 | Plan edit: a durable unique actor-plus-key constraint on the event row and no in-flight memory; or a semantic identity for those operations, such as one result record per attempt |
| A6 | **The never-dispatched resume branch is unreachable as designed.** The kill matrix permits redispatch only "with proof it was never dispatched"; the plan forbids a dispatch marker; CV1 says no response proves nothing. Every kill after attempt commit therefore costs `UNKNOWN` at maximum plus a fresh funded attempt | acceptance 93; plan 329–330; CV1 709–717 | Plan edit: an immutable pre-dispatch `RECEIPT` appended before exec, whose absence proves no dispatch given write-before-exec ordering; or state the branch is unsupported |
| A7 | **Clock coupling of settlement is unspecified.** Expiry "read at any later commit" taken literally makes every Evidence commit touching a reservation need a clock read. Settlement is admitted notwithstanding expiry and must not need one, or a clock outage blocks the settlements R07 and B10 rely on | CV1 736–737, 718–724; plan 343–353 | Plan edit: list the commits that take a read: reservation, attempt, `BIND`, `CLOSED`, expiry evaluation; settlement takes none |
| A8 | **Reservation expiry origin.** Whether the expiry instant is client-supplied or computed from the grant's default is not stated; a client-supplied far-future instant would defeat the default | CV1 659–662, 985–986; plan 224 | Plan edit: the boundary computes the instant from the default, or validates a supplied one at or below it |
| A9 | **Clock monotonicity is nowhere required.** The supervisor "may advance time"; a read below an earlier durable receipt breaks "a read at `t ≥ T` establishes `T` has passed" | plan 348; CV1 546–547 | Plan edit: non-decreasing reads; refuse a read below the last durably recorded receipt |
| A10 | **Missing schedule.** `BIND`; a Transition suspending `P-1` applies; continuation presents Apply. Expected: `APPLY_REFUSED` with invalidation, `RELEASE`, and a re-check before any fresh `BIND` because the head moved | acceptance §3 | Acceptance edit: add as B12 |
| A11 | **Identity details deferred to the packet.** Attempt "step" is undefined and the input hash's byte scope unspecified; encoding is deferred to the packet, which ties back to S2. Synthetic Research Records must carry the Historical Reconstruction run fields and the Check must record "authored knowing the period"; the plan omits the reproducibility binding and source cutoff | plan 225, 337–341, 226, 282–287; CV1 558, 1126–1127 | Plan edit: list the fields; packet supplies encoding before cut 1's hash tests |

Correct as written: the duplicate-accounting versus exactly-once
distinction (plan 254–264; acceptance 122–127); `BIND`, Apply and
`RELEASE` as separate durable commits with refusal-plus-invalidation
atomic; B01–B09 against §III.5 and §III.8; B05's race outcome.

## 4. Complexity that makes correct implementation harder

| Item | Why it is unnecessary | Recommendation |
| --- | --- | --- |
| Seventeen Applies and sixteen funded Checks before the first research unit | Nine research designs, `SRC-E` with full extraction and grace rules, and the second Checker lineage are exercised nowhere in the milestone. The ten-lineage table is not among PD-009's enumerated admitted choices (PD-009 5–31); a minimal setup is a pre-genesis parameter choice, not a reversal | **Principal decision**: a setup of about eight Applies: genesis; `AU-OBS-1` with `SRC-SYN` only; limits; `AD-R1.0`; `AD-CK-2.0`; `AU-CK-B`; `AU-RP-1` for one lineage; `TH-G1` |
| Request-key layer with in-memory serialization | Reduces to a unique constraint; see A5 | Drop in-flight memory |
| `tool.receipt` and a tool-side receipt store (plan 310–312) | A fixed-charge synthetic tool's `UNKNOWN` settlement equals its actual | Drop for the milestone |
| Role-bearing `recovery` module | See A2 | Inspection plus the Apply boundary's own continuation |
| Six read commands (plan 236–238) | Overlapping selectors | One reference read and one as-of state read |

## 5. Disposition

The plan does not violate CV1 by what it states; it fails to complete
startup (S1), cannot be sequenced as written (S2), and resolves one CV1
ambiguity by an identity rule it is not authorized to create (S3). The
independence and trust-model gaps (S4, S6, S7, A1, A2, A3) would make the
acceptance witnesses label-based unless corrected. The remaining items are
specification gaps that permit materially different implementations.

Decisions for the Principal: S3, S6, S7 and the setup size. Plan or
acceptance edits before the packet is written: S1, S2, S4, S5, S8, A1–A3,
A5–A11.

`ΔO/ΔS/ΔA` of this audit: **`0/0/0`**. It adds evidence only; it admits
nothing, changes no governed meaning, selects no technology and claims no
execution.
