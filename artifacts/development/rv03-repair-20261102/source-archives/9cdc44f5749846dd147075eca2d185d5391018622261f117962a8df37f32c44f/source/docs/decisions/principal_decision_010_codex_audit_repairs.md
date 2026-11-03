# Principal Decision Record 010 — Repairs Proposed for the Independent Pre-implementation Audit

Status: **ADMITTED 2026-10-19 by the Principal (document-phase admission): revision 4, the consolidated §8 choices 1 to 3, 4a to 4d and 5 to 14, taking the recommended alternatives, binding over earmarking.** Applied to the Constitution as revision 11; the author's propagation consistency check is [pd010_propagation_check_20261019.md](../audits/pd010_propagation_check_20261019.md) and the final handoff to Codex is [cv1_final_handoff_20261019.md](../audits/cv1_final_handoff_20261019.md). Genesis is not executed; nothing is certified. Approval, as given, recorded against the independently reviewed digest:

```text
ADMITTED 2026-10-19 by the Principal (document-phase admission):
PD-010 revision 4, consolidated §8 choices 1–3, 4a–4d and 5–14,
taking the recommended alternatives, including binding over
earmarking. This is document-phase admission and authorization to
propagate those exact repairs.
Reviewed revision: SHA-256
a47dad4069d06bbb469c300ef27361952b82193357edd1244d2edeecd2f723d2
(verified identical before this block was recorded; the bounded
check of Codex, docs/audits/pd010_revision4_bounded_check_20261019.md,
reviewed the same digest at HEAD 895f953).
The acceptance explicitly includes:
- registration eligibility established at BIND surviving the
  specified later funding events, while new spending remains subject
  to current permission;
- deferred expiry release while frozen, with no guaranteed maximum
  hold or recovery during an outage;
- successful Apply ending the freeze through its own durable record;
- the declared Checker funding rights, funding-stop extension,
  binding caller rights and narrow terminal-invalidation authority.
Constitutional Delta admitted: ΔO +1 (BINDING); ΔS as each group
states, including the lifecycle event BINDING_INVALIDATED on an
existing object; ΔA +4 as §8 states. No application code, runtime
selection, genesis execution, CPOC claim or certification is
authorized. This is a document-phase admission, not a claim that a
Constitutional Transition executed before genesis.
```

Proposal history follows unchanged (the digest above is of the text
below this block as it stood at review). Prior status: **PROPOSED FOR
ADMISSION, revision 4.** Author: Claude. Subject: the blocking findings B-1
to B-10 and clarifications C-1 to C-7 of
[the independent audit](../audits/independent_preimplementation_design_audit_20261019.md)
(Codex, 2026-10-19, OSA FAIL at revision 10), and findings R2-1 to R2-3
of the
[focused review of revision 2](../audits/pd010_revision2_binding_review_20261019.md)
(Codex, 2026-10-19) and findings R3-1 and R3-2 of the
[review of revision 3](../audits/pd010_revision3_binding_review_20261019.md)
(Codex, 2026-10-19), all three preserved unchanged and treated as
evidence, not doctrine. Revision 2 (2026-10-19) corrected revision 1 on five
points the Principal named (B-4 ordering, B-3 closure after overrun,
B-5 cutoff, B-10 `REDUCE`, classification) and the genesis replay.
**Revision 3 (2026-10-19)** replaces the Apply binding protocol of §2
under the Principal's policy direction: eligibility is established at
`BIND`; successful Apply and release-as-unused are mutually exclusive by
a terminal disposition serialized on the Transition ledger; the binding
interval permits invalidation and promises nothing else; recovery uses
existing records; settlement validation is stated in the review's
words. The accounting (B-3), cutoff (B-5) and reduction (B-8 to B-10)
repairs that survived the focused review are kept unchanged. **Revision
4 (2026-10-19)** addresses R3-1 and R3-2 only: reservation freeze
standing is defined exhaustively from both ledgers so that a committed
Apply ends the freeze by itself, "live until `RELEASE`" and "by nothing
else" are removed, and the Transition boundary's terminal-invalidation
authority is declared completely with its evidence and carrier classes.
Nothing else changes. No review is treated as approval of any other
choice. Revision 4 goes to Codex for a bounded correction check, then
to the Principal for admission, then to the final whole-design review.

Date: 2026-10-19 (revisions 1 to 3: same day)

Baseline: Constitution revision 10 at commit `2f24eb2`; handoff at
`895f953`. **C** below means the Constitution. Earlier audit grades are
not evidence; every finding was reconciled against the governing text.

## 0. Reconciliation of the findings against the governing text

| Finding | Reconciled against | Confirmed? | Why the cited rules do not already resolve it |
| --- | --- | --- | --- |
| B-1 Checker funding | C §III.5 reservation block ("committed by the grantee under its Research Authorization"; purposes: Theme, family, pending registration); §III.7 ("A Research Authorization's grant is stated in units"; fence before revoking "a Research Authorization"); Part V `RESERVATION` row; PD-009 §2 row 1, §3 | **Confirmed** | Every reservation rule names Research Authorizations; a `CHECKER` lineage holds none (§III.8). `AU-CK-A`'s 60 units have no lawful consumer, purpose, fence or revocation contract, and its first tool is declared in the Transition it must first check |
| B-2 Check form at initialization | C §III.8 Check record items 3 and 4 | **Confirmed** | The budget line is unconditional; a Principal control act declares no research consumption and the Principal holds no Authorization to reserve under; `F` has no value before any Execution Authorization and the form gives no `N/A` |
| B-3 Five-state arithmetic | C §III.5 five states; PD-008 §3; PD-009 §3a | **Confirmed** | The literal formula goes negative on an overrun and offsets it; underrun prose and formula disagree; the cap omits pending maxima of closed reservations; and, as the Principal's replay shows, no predicate stops an attempt under one reservation from consuming capacity an overrun elsewhere has already used |
| B-4 At-Apply funding conditions | C Part V `P-1` (b) ("open at Apply"); §III.8 Continuation; PD-008 §3 | **Confirmed** | "Open at Apply" is an Evidence fact; the Apply is on another ledger; the design states no ordering for that pair. Revision 1 wrongly called at-Apply enforcement impossible; §2 below gives the contract |
| B-5 Outcome deadline and uniqueness | C §III.5 Outcome row ("by the Standard's deadline"); Part X §6 | **Confirmed** | No deadline exists; "exactly one Prediction" per Outcome does not bound Outcomes per Prediction; no duplicate refusal; and nothing separates when a member is missing from when someone computes |
| B-6 Method commitment sequences | C Part X §3 | **Confirmed** | The comparison is across ledgers with no binding stated |
| B-7 Cost evidence route | C Part X §3 (b) versus §III.8 Independence | **Confirmed** | The two clauses contradict; Part V makes the Observation function the only Market Observation committer |
| B-8 Reducing fill after expiry | C §III.10 ("A fill of a `REDUCING` order is `EFFECTIVE` at commit") | **Confirmed** | The counterexample is admitted by the text and crosses zero after expiry |
| B-9 `FLATTEN_ON_QUOTA` | C §III.10 Expiry; Admission rules; §III.7 triggers | **Confirmed** | The derived set's orders fail `NOT_YET_DUE`; the obligation predicate names only `T` |
| B-10 Reducing qualified exposure | C Part V Allocation row; Standing Transition "after expiry"; Part X R-8 | **Confirmed** | No purpose lowers an amount without qualification evidence; the zero path exists only after expiry |

C-1 to C-7 are reconciled in §5. The focused review's findings:

| Finding | Reconciled against | Confirmed? | Treatment in revision 3 |
| --- | --- | --- | --- |
| R2-1 Pre-fence binding survival was a policy change, not a preservation of "open at Apply" | Revision 2 §2 steps 1 to 3 and its comparison table | **Confirmed** | §2 states the policy as the Principal directed and withdraws every claim that funding eligibility is preserved at the Apply instant; the effects of a later fence, expiry and overrun are stated one by one |
| R2-2 Release on timeout could race an in-progress Apply; "not applied" read on another ledger is no exclusion; interval meaning undecided | Revision 2 §2 steps 6 and 7 | **Confirmed** | §2 gives each binding one terminal disposition decided on the Transition ledger, serialized against Apply; `RELEASE` requires a durable invalidation; the interval permits invalidation only |
| R2-3 "Settlement always admitted" must not override caller, identity, units, amount and provenance validation or admit a second accounting effect | Revision 2 §2 settlement predicate; C §III.5 Settlement | **Confirmed** | §2's settlement predicate is the review's replacement text, with the duplicate and malformed replays of §2 |
| R3-1 A consumed binding stayed "live until `RELEASE`" while a `RELEASE` could never follow, so rule 2's freeze contradicted rule 4's unfreeze on Apply and could strand unused allowance | Revision 3 §2 records table, rules 1, 2, 4, 6, 7, 9, 10, allowance check, §6 | **Confirmed** | §2 defines freeze standing from both ledgers in four exhaustive cases; Apply alone ends the freeze; "live" and "by nothing else" are removed; a fence's accounting release is distinguished from binding `RELEASE`; the dependent operation refuses when the Apply fact cannot be established |
| R3-2 The Transition boundary's right to commit a terminal invalidation was claimed from ledger ownership ("its own ledger; no new right") and not declared as authority; the evidence of each ground and the carrier classes were incomplete | Revision 3 §2 rules 4, 5, "Who commits what", delta, §7 choices 4b and 4d | **Confirmed** | §2 declares the boundary's exclusive, narrowly bounded terminal-invalidation authority under both grounds as `ΔA`, states the durable evidence of each ground, classifies every carrier, and reconciles the table, the delta and the decision brief |

## 1. Group 1 — Bootstrap and Check applicability (B-1, B-2)

### Three kinds of consumption, distinguished

| Kind | Who | Funded by | Reservation purpose | Lifecycle |
| --- | --- | --- | --- | --- |
| **Principal control act**: Authorization grant, amendment, revocation; limits; Constitutional Transition; `FENCE`; Theme registration or Allocation proposed by the Principal | Principal | The Principal's own authority, cited directly | None; the Principal's attention is outside every grant | Not metered |
| **Proposer research consumption** | A `RESEARCH` or `SELECTION` grantee | Its Research Authorization | An active Theme; a `SearchFamily` in scope; a named pending registration | Bound into the proposal's admission lifecycle only through the Apply binding of §2 |
| **Checker's own cost** | A `CHECKER` grantee | Its Checker Authorization | A **verification purpose**: the Check of a named, already-proposed Transition; reproduction of named Decisions; Outcome completion for a named subject; a declared verification cadence | Ordinary reservation lifecycle; **never bound to the proposal's admission**; cited in Check record item 5 only |

### Affected clauses and replacement text

| Clause | Current | Replacement |
| --- | --- | --- |
| C §III.5 `RESERVATION` bullet, first sentence | "committed by the grantee under its Research Authorization; names … a purpose (an active Theme, a `SearchFamily` in the Authorization's empirical or discovery scope, or a named pending registration) and an expiry instant" | "committed by the grantee under its **Research or Checker** Authorization; names the Authorization, the grantee, an amount in units, a purpose and an expiry instant. Under a Research Authorization the purpose is an active Theme, a `SearchFamily` in the Authorization's empirical or discovery scope, or a named pending registration (a Transition already proposed). Under a Checker Authorization the purpose is a **verification purpose**: the Check of a named Transition already proposed, reproduction of named Decisions, Outcome completion for a named subject, or a verification cadence the Authorization declares. A Checker's cost is never charged to a proposer's grant, nor a proposer's to a Checker's" |
| C §III.5 `FENCE` bullet | "names an Authorization" | "names a **Research or Checker** Authorization" (revocation sentence likewise) |
| C §III.7 Content | "A Research Authorization's grant is stated in **units** … and a default reservation expiry (PD-008)." | "A **Research or Checker** Authorization's grant is stated in **units**, with the estimation rule converting each permitted provider's or tool's metered quantity into units, **the tools and providers it may consume with the guarantee tier of each**, whether uncapped calls are permitted, an optional per-grantee cap, a default reservation expiry, a **binding interval** (§2), and, for a Checker Authorization, its verification purposes and the subjects it may not check (C-7). A grant names its own tools; no Authorization consumes a tool declared only in another's" |
| C §III.7 Budget ownership | "A Transition revoking a Research Authorization …" | "A Transition revoking a Research **or Checker** Authorization, or superseding it with a different grant or scope, requires a prior `FENCE` naming it" |
| C Part V `RESERVATION` and attempt row, proposer | "The grantee under its Research Authorization" | "The grantee under its Research or Checker Authorization" |
| C §III.8 Check record item 3 | "the closure read `(E, N, F)` with its instant" | "the closure read `(E, N, F)` with its instant, where `F` is `N/A — no Paper Book` while no Execution Authorization has ever been applied (a determinable finding derived from the Applied History), and `LEDGER_UNREACHABLE` whenever a ledger that exists cannot be read, which stops the Check and never falls back" |
| C §III.8 Check record item 4 | "for every class, within the proposer's Authorization and base state current, and the **budget line**: …" | "for every class, the proposer's authority: a cited Authorization in scope, or, for a **Principal control act**, the Principal's own authority cited directly; base state current; and the **budget line**, which applies to proposals declaring metered research consumption: the declared budget is covered by the cited `RESERVATION` (open, below any `FENCE` at the Check's closure, amount sufficient, purpose this Transition), with remaining spendable budget recorded for attribution and never a second requirement. For a Principal control act the budget line reads `N/A — no metered consumption`. The Checker's own cost is its own reservation under a verification purpose, cited in item 5, never substituted for the proposer's" |
| PD-009 §2 row 1 (`AU-OBS-1`) | "… the bounded synthetic provider as a declared tool (§5)" | delete the tool clause; `AU-OBS-1` declares sources and feeds only |
| PD-009 §3 `AU-CK-A` row | "60 units from its own grant for its calls; provider calls: see §5" | "60 units; estimation rule as §3a; tools: the bounded synthetic provider (tier 2 by construction) and metered local compute (tier 1); uncapped calls forbidden; cap 60; reservation expiry 7 days; binding interval not applicable (Checker grants bind nothing); verification purposes: every class except Transitions concerning `AD-CK-1.0` or `AU-CK-A` (C-7)"; `AU-CK-B` and `AU-RP-1` likewise name their own tools |

### Smallest repair and delta

```text
ΔO: NONE.
ΔS: the clauses above; Check record applicability (control acts; N/A
    for F); PD-009 content.
ΔA: +1 permitted-caller extension, declared as PD-002 declared commit
    restrictions: holders of a Checker Authorization may commit
    RESERVATION, attempt and settlement records under their own grant.
    +1 scope extension of the Principal's funding-stop exception
    (PD-008 ΔA) to Checker Authorizations. No decision right moves; the
    sequence-zero waiver keeps its three items; independent Check is
    waived nowhere else.
```

### Replay of the audit's failed transition, corrected ordering

1. State 0 applied: `CV1` text; `AD-CK-1.0`; `AU-CK-A` with 60 units,
   tools and verification purposes.
2. The Principal **proposes `TR-1`** (`AU-OBS-1`): the proposal content
   is now immutable on the Transition ledger.
3. `AD-CK-1.0` commits `RESERVATION` 4 under `AU-CK-A`, purpose "Check of
   `TR-1`", which now names an existing proposal (Evidence boundary:
   Checker Authorization active at head 0; no fence; headroom 60 ≥ 4):
   **admitted**.
4. It pre-records an attempt (reservation, "check", hash of `TR-1`'s
   content, dispatch 0), max 3, on the bounded synthetic provider named
   in `AU-CK-A`: **admitted** (allowance 4 ≥ 3; headroom 60 ≥ 3).
5. The Check record: proposer authority = the Principal's own, cited;
   budget line `N/A — no metered consumption`; closure
   `(E = 3, N = 0, F = N/A — no Paper Book)`; Authorization-row
   criteria met; item 5 cites the Checker's own attempt; `PASS`.
6. The Principal decides; Apply 1 (a control act: no Apply binding).
7. The Checker settles its attempt at 2 units; its reservation closes
   when it chooses or at expiry.

Interruption: the Checker's process dies after step 4. On restart it
finds the `PENDING` attempt, settles or resumes it under PD-009 §7, and
either completes the Check or returns the reservation to expiry. `TR-1`
waits checked or unchecked; nothing about the proposal was consumed.

### Interactions

Group 2's predicates apply to Checker reservations identically; the
Apply binding never touches a Checker reservation. Group 3's Outcome
completion is a verification purpose. Genesis: the three-item
bootstrap is unchanged; `AU-CK-A`'s content is now stated in full.

## 2. Group 2 — Budget accounting and final admission (B-3, B-4)

### Accounting (B-3)

For each reservation `R` with amount `A`, settled actuals `S` (overruns
included), pending maxima `P`, committed `C = S + P`:

| Quantity | Definition |
| --- | --- |
| Remaining allowance of `R` (open only) | `max(A − C, 0)`; never negative |
| Overrun of `R` | `max(C − A, 0)`; counted in full, never offset |
| Usage of `R` | open: `max(A, C)`; closed: `C` |
| **Committed total** of an Authorization | `Σ C` over every reservation, open or closed: actual consumption plus pending liabilities |
| **Reserved total** | `Σ usage(R)`: committed total plus unused allowance of open reservations |
| **Headroom** | `max(grant − Σ C, 0)`: capacity not yet consumed or owed |
| Remaining spendable budget | `max(grant − Σ usage(R), 0)`: capacity neither consumed, owed nor reserved |
| Released allowance | at close of `R`: `max(A − C, 0)`, a historical figure on the `CLOSED` record, not a balance |
| `OVERSPENT` | `Σ C > grant` |

Lineage quantities are the same sums over the lineage's reservations
against the cap.

**Admission predicates.**

- A new `RESERVATION` of amount `a`: admitted iff `a ≤ remaining
  spendable budget` and `a ≤ cap − Σ usage_lineage`, and no fence, and
  the Authorization not `OVERSPENT`.
- A new `PENDING` attempt of maximum `m` under `R`: admitted iff
  `m ≤ remaining allowance(R)` **and `m ≤ headroom`** **and
  `m ≤ cap − Σ C_lineage`**, and no fence, and not `OVERSPENT`. The
  reservation's own allowance is necessary and never sufficient: an
  overrun elsewhere has consumed grant capacity that every open
  reservation's unused allowance was counting on, and the headroom test
  is what refuses it.
- Settlement (R2-3): a valid settlement by a permitted caller (the
  grantee under the grant the attempt was admitted under, including a
  former grantee after close, expiry, fence or revocation, or the
  Principal) for an exact attempt **still `PENDING` at this Evidence
  commit** is admitted notwithstanding close, expiry, fence, revocation
  or budget or cap exhaustion. Identity (reservation, step, input hash,
  dispatch index), attribution, units, amount and provenance remain
  validated as §III.5 requires; `UNKNOWN` settles at the maximum. The
  pending-to-settled effect occurs once: a second submission for the
  same attempt, whether a retry after a lost response or a concurrent
  duplicate, is refused `ALREADY_SETTLED` and changes nothing; a
  malformed submission (negative, non-finite or wrong-unit amount,
  missing required provenance, wrong reservation or Authorization,
  unknown attempt, unrelated caller) is refused `INVALID_SETTLEMENT`,
  preserved, and the liability remains at its maximum until a valid
  settlement. A later invoice conflicting with a final settlement is not
  a settlement of a `PENDING` attempt; no correction lifecycle is
  proposed here. This states the existing boundary's obligations and
  grants no caller right: `0/0/0`.

**Underrun disposition** (kept from revision 1, Principal choice): in an
open reservation the difference returns to that reservation's remaining
allowance; in a closed reservation it leaves `C` and so returns to
headroom and spendable budget.

**Replay of the Principal's case.** Grant 100; `R1` 50, `R2` 50
(reserved total 100, spendable 0, headroom 100). `R1`'s sole attempt,
max 50, settles at 60: `C1 = 60`, overrun 10, usage(`R1`) 60; committed
total 60; reserved total 110; headroom 40; spendable 0; `OVERSPENT`
false. `R2`'s attempt of 50: allowance 50 ≥ 50, but headroom 40 < 50 →
**refused `GRANT_EXHAUSTED`**. An attempt of 40 under `R2`: admitted;
committed total 100; headroom 0; every further attempt under any
reservation refused `GRANT_EXHAUSTED`; `R2`'s remaining allowance 10 is
unfundable, visible, released at close. That attempt settles at 45:
committed 105 > 100 → `OVERSPENT`; reservations and attempts refused;
valid settlements of existing liabilities still admitted. Lineage cap 100
with a reservation closed holding 100 pending: `Σ C_lineage = 100`;
the next attempt refused `CAP_EXHAUSTED` until settlement lowers it.

**Replay of B-3's originals.** Grant 100, `R` 10, attempt max 10 settled
at 20: allowance 0, overrun 10, usage 20, headroom 80, spendable 80.
Settled at 6 while open: allowance 4, usage 10, headroom 94, spendable
90; at close released 4, spendable 94.

### Final admission: eligibility at `BIND`, one terminal disposition (B-4)

Revision 1 said at-Apply enforcement was impossible. Revision 2 claimed
the binding preserved "open at Apply" exactly and let a release on
timeout race an in-progress Apply (R2-1, R2-2). Both are withdrawn.
Revision 3 states the policy as the Principal directed, using the two
existing ledgers and their commit boundaries, no acknowledgement, no
service and no runtime.

**Policy.** Funding eligibility for a budgeted registration is
established at `BIND`, not at Apply. A binding admitted before a
funding fence may complete its one named registration, subject to the
binding's terminal disposition and the remaining Apply-side conditions.
The fence still forbids new attempts. This record does not claim that
the reservation is open, unfenced, unexpired or funded at the Apply
instant; it claims only that it was so at `E_b`, and that nothing
admitted after `E_b` withdraws the eligibility.

**Records and identity.**

| Record | Ledger | Identity | Meaning |
| --- | --- | --- | --- |
| `BIND(TR-x, R)` | Evidence; Research Record kind `BINDING`, form `BIND` | Its Evidence sequence `E_b`; carries the clock receipt `(t_b, E_b)` taken in the commit | Eligibility of `TR-x`'s one registration against `R`; the start of `R`'s binding freeze |
| Apply of `TR-x` citing `E_b` | Transition ledger, `TR-x`'s lifecycle (`APPLIED`) | The Apply record | Terminal disposition **CONSUMED**. The sole durable consumption fact; no Evidence completion record or acknowledgement exists, is required or is permitted |
| `BINDING_INVALIDATED(E_b, ground, evidence)` | Transition ledger, `TR-x`'s lifecycle, an appended event on a `DECIDED` Transition | The event's Transition-ledger sequence `n_i` | Terminal disposition **INVALIDATED**: every later Apply citing `E_b` is refused |
| `RELEASE(E_b, n_i)` | Evidence; form `RELEASE` | Cites `E_b` and `n_i` | Ends the binding freeze of `R` after invalidation; lawful only citing a durable invalidation |

**Terminal exclusivity.** At most one terminal disposition exists per
binding; one is established when a terminal operation, an Apply or an
invalidation, succeeds; each is decided on the Transition ledger. No
rule promises that a binding eventually receives one. Each binding has
its own identity, and a disposition of `E_b` says nothing about any
other binding.

**Freeze standing of a reservation**, derived from both ledgers, the
exhaustive cases:

| Binding facts for `R` | `R`'s standing |
| --- | --- |
| A `BIND` naming `R` exists; no terminal disposition | **Frozen.** No new attempt, no grantee `CLOSED`; the expiry deferral of rule 2 applies |
| Invalidation exists; no `RELEASE` cites it | **Frozen pending release.** Apply of this binding is forbidden permanently; `R` stays frozen until an authorized `RELEASE` |
| An Apply cites the `BIND` | **Consumed; the freeze ends from that Apply alone.** No `RELEASE` and no completion record is required or permitted; `R` returns to its ordinary lifecycle with its purpose the registered subject |
| Invalidation and `RELEASE` both exist | **The freeze ends.** `R` returns to its ordinary closure, expiry and attempt rules |

A `FENCE` closes `R` in every case and never loses its effect. The
fence's release of never-attempted allowance is an **accounting
release** into a grant that can no longer be reserved; it is not a
binding `RELEASE`, it is never written as one, and it creates no
reusable spending permission under the fenced grant. The word "live" is
not used; the `BIND` record is immutable and its unreleased presence
decides nothing by itself.

**Admission rules.**

1. **`BIND`.** The Evidence boundary admits `BIND(TR-x, R)` at `E_b` iff
   `R` is open; no `FENCE` for `R`'s Authorization has sequence below
   `E_b`; `R`'s expiry instant is after `t_b`; the Authorization is not
   `OVERSPENT`; `TR-x` is `DECIDED ADMITTED` and not `APPLIED` at the
   Applied History head the boundary witnesses; `R` is not frozen; and
   no binding of `TR-x` is without a terminal disposition or awaiting
   release. Otherwise refused `FENCED`, `RESERVATION_CLOSED`,
   `RESERVATION_EXPIRED`, `OVERSPENT`, `NOT_DECIDED`, `ALREADY_APPLIED`
   or `ALREADY_BOUND`, preserved, and the Apply is refused with that
   reason recorded on `TR-x`.
2. **Freeze.** While `R` is frozen: `R` admits no attempt
   (`RESERVATION_BOUND`); the grantee may not commit `CLOSED` for `R`;
   `R`'s expiry instant is **not read** against it. An instant that
   passes while frozen closes `R` at the first read after the freeze
   ends, and nothing revives it. A `FENCE` still closes `R` at its own
   sequence. Valid settlements of `PENDING` attempts under `R` are
   admitted as always. **Declared tradeoff:** unused allowance can
   remain frozen beyond `R`'s expiry instant until consumption, or
   invalidation followed by `RELEASE`; this supersedes, for the frozen
   interval only, PD-008's rule that expiry releases unused allowance
   at the next read; it extends neither spending permission nor the
   original expiry instant, and promises no release during an outage.
3. **Effects of later events on eligibility.** None withdraws it.
   A `FENCE` above `E_b` closes `R`, releases its never-attempted
   allowance into a grant that can no longer be reserved (accounting
   release), and refuses every later attempt `FENCED`; the registration
   may still apply and the registered subject holds a closed
   reservation. An expiry instant passing after `E_b` has no effect
   while frozen (rule 2); after consumption, `R` expires at the next
   read, releasing only unused allowance, and a new attempt refuses
   `RESERVATION_EXPIRED`. An overrun elsewhere after `E_b` withdraws
   nothing; new spending obeys current allowance, headroom and cap, and
   if the committed total exceeds the grant every new reservation and
   attempt refuses `OVERSPENT` until the Principal acts. An
   already-admitted `PENDING` attempt completes, dispatches or settles
   under its consumed permission in every case; consumption of a
   binding is never permission to retry.
4. **Apply.** The Transition commit boundary admits the Apply of `TR-x`
   citing `E_b` iff `TR-x` is not `APPLIED`; `E_b` is a `BIND` of
   `TR-x`; no `BINDING_INVALIDATED(E_b)` is on `TR-x`'s lifecycle; and
   every Apply-side condition holds at the commit: the base current or
   re-checked with `PASS`, every `P-1` condition for a delegated class,
   the Authorization active at the head, `P-1` not suspended for it, no
   `STOP`, and every other D-17 condition that is not the Evidence-side
   funding clause this section replaces. A refusal on an Apply-side
   condition is committed together with `BINDING_INVALIDATED(E_b,
   APPLY_REFUSED, …)` as one Transition-ledger commit (rule 5). An
   Apply citing an invalidated binding is refused `BINDING_INVALIDATED`
   whenever it is presented. **Effect on `R`:** the Apply changes `R`'s
   purpose to the registered subject and ends the binding freeze. It
   grants no caller, amount, expiry or Authorization: the original
   grantee keeps `R` with its original expiry instant; a registered
   successor inherits no reservation and no permission; every later
   attempt, `CLOSED`, expiry read and budget view is governed by the
   ordinary caller, purpose, expiry, fence, allowance, headroom and cap
   checks; `PENDING` liabilities survive ordinary closure.
5. **Invalidation.** The Transition commit boundary, and it alone,
   appends `BINDING_INVALIDATED(E_b, ground, evidence)` iff `TR-x` is
   not `APPLIED` (`ALREADY_APPLIED` otherwise), `E_b` is a `BIND` of
   `TR-x`, and no invalidation of `E_b` exists (`DUPLICATE` otherwise).
   Two grounds exist and no other, each with its durable evidence on
   the event:
   - **`APPLY_REFUSED`**: atomically with the boundary's own refusal of
     an Apply citing `E_b`; the event records the exact failed
     condition and the authority cited for it (the Authorization,
     policy, base or `STOP` record by sequence).
   - **`INTERVAL_ELAPSED`**: on an attributable request from a process
     acting in the Apply-boundary continuation role under D-17; the
     event records the exact `BIND` `E_b`, the applicable binding
     interval read from the Authorization, the requesting role, and
     the verified Evidence-clock receipt `(t, E)` with
     `t − t_b > interval` (equal is not greater). The boundary verifies
     the receipt against the cited `BIND`; a caller's assertion, a
     local timeout or a remembered clock answer is not a receipt.
   No party holds a discretionary right to cancel a binding, and no
   other ground exists. The Principal acts on a binding only through
   existing acts, suspension of `P-1`, revocation of the Authorization
   at the head, or a `STOP`, each of which makes the next Apply refuse
   under rule 4; the proposer and the Checker hold no route.
6. **Mutual exclusion.** Apply and invalidation of the same `E_b` are
   appended to the same Transition's lifecycle by one serialized
   boundary, and each refuses when the other has committed (rules 4 and
   5). If Apply succeeds, the binding is consumed and no invalidation or
   `RELEASE` can follow. If invalidation succeeds, every later Apply
   citing `E_b` refuses. A read elsewhere showing "not applied" decides
   nothing.
7. **Release.** The Evidence boundary admits `RELEASE(E_b, n_i)` iff a
   `BIND` at `E_b` exists with no `RELEASE` citing it, and
   `BINDING_INVALIDATED(E_b)` at `n_i` is durably on the Transition
   ledger, which the boundary reads at the commit (an I-13 read).
   Refused `NO_INVALIDATION` without it, `ALREADY_RELEASED` for a
   second release, and `LEDGER_UNREACHABLE` when the Transition ledger
   cannot be read, which never falls back. `RELEASE` ends the binding
   freeze; `R` is then read under its ordinary rules: closed if a fence
   closed it, expired if its instant has passed, otherwise open. It
   reopens no fenced grant and revives no expired reservation.
8. **Deriving consumption at the Evidence boundary.** Before admitting
   an attempt, a `CLOSED`, an expiry close or a budget view for a
   reservation with a `BIND` that no `RELEASE` cites, the Evidence
   boundary establishes the binding's standing by an authoritative read
   of the Transition ledger (I-13): an Apply citing the `BIND` means
   consumed and the ordinary checks of rule 4 govern; an invalidation
   without `RELEASE` means frozen; neither means frozen. If the
   Transition ledger cannot be read, the dependent operation is refused
   `LEDGER_UNREACHABLE`; an acknowledgement, cache or process memory
   has no deciding role, and a stale pre-Apply read can leave `R`
   frozen but can never authorize spending. The read acquires no
   decision right.
9. **Fresh binding.** A new `BIND` for `TR-x` is admitted only when
   `TR-x` is not `APPLIED` and no prior binding of `TR-x` is without a
   disposition or awaiting release. An Apply cites exactly one `E_b`.
   Invalidating `E_b` touches no other binding; a delayed Apply carrying
   `E_b` is refused regardless of what fresh binding exists. A process
   that presents an Apply citing a fresh, valid binding of the same
   decided Transition performs that Transition's single lawful Apply,
   whatever process requested the binding, because the boundary
   verifies every condition at the commit and a second Apply is refused
   `ALREADY_APPLIED`; old and fresh are properties of bindings, not of
   processes.
10. **Interval meaning.** The Authorization's **binding interval**
    permits a request for invalidation on ground `INTERVAL_ELAPSED`. It
    is not an automatic release, not a guaranteed maximum freeze (no
    process need be running), and not a deadline for the Apply commit:
    an Apply after the interval is lawful until an invalidation
    commits. After the interval an Apply and an invalidation may race;
    rule 6 decides, and either result is lawful. A reservation frozen
    by a binding with no disposition, or by an unreleased invalidation,
    stays frozen until a terminal operation succeeds and, for
    invalidation, a `RELEASE` follows; nothing promises either.
11. **Recovery (D-17), from existing records only.** A process acting
    in the Apply-boundary continuation role reads `TR-x`'s lifecycle
    and the Evidence ledger. `APPLIED` citing `E_b`: consumed; nothing
    to do, and the interval is irrelevant. `BINDING_INVALIDATED(E_b)`
    present and no `RELEASE`: commit `RELEASE`, then re-check and a
    fresh `BIND` under D-17. `BIND` with no disposition: within the
    interval, present the Apply when the Apply-side conditions hold,
    otherwise its refusal invalidates; after the interval, present the
    Apply or request invalidation with a clock receipt, and the
    serialized result decides. If the Transition ledger or the Evidence
    ledger is unreachable, the process does nothing, and in particular
    releases nothing.

**Authority to commit each act.** Ownership of a ledger is not an
authority grant; every right below is declared.

| Act | Committer | Authority declared |
| --- | --- | --- |
| `BIND`, `RELEASE` | The Apply boundary as a caller of the Evidence commit boundary, for these two forms only, for Transitions it is applying; the Evidence boundary verifies every condition and the caller decides nothing | **`ΔA` item 1**: the Evidence caller extension (as revision 2) |
| `BINDING_INVALIDATED(…, APPLY_REFUSED, …)` | The Transition commit boundary, atomically with its own Apply-side refusal, recording the failed condition and the cited authority | **`ΔA` item 2**: the Transition commit boundary's exclusive, narrowly bounded authority to establish terminal invalidation under the two grounds of rule 5 and no other; it includes the right to adjudicate and commit the terminal result on an attributable `INTERVAL_ELAPSED` request. Pre-existing ownership of the Transition ledger does not supply this right |
| `BINDING_INVALIDATED(…, INTERVAL_ELAPSED, …)` | The Transition commit boundary, on the attributable request of a process acting in the Apply-boundary continuation role under D-17, recording the exact `BIND`, the applicable interval, the requesting role and the verified clock receipt | **`ΔA` item 2** (the same bundled right); the requesting role may request on this ground only and decides nothing |
| Reading the Transition ledger to admit `RELEASE`, an attempt, a `CLOSED`, an expiry close or a budget view (rules 7 and 8) | The Evidence boundary | An I-13 read; `ΔA` 0 |

**Carrier classification** (Part VII classes; classifications of the
proposed carriers, no new object or writer):

| Carrier | Class |
| --- | --- |
| `BIND`, `RELEASE` records | `AUTHORITATIVE` for their exact Evidence-side acts (eligibility established; freeze ended after invalidation) |
| The Apply record; the `BINDING_INVALIDATED` event | `AUTHORITATIVE` for the terminal disposition of the binding they cite |
| Consumed, frozen, pending-release and remaining-budget standing of a reservation | `DERIVED` from the records above and the reservation records; no vote |
| The recorded clock answer on a `BIND` (`t_b`, `E_b`) or on an `INTERVAL_ELAPSED` event (`t`, `E`) | `RECEIPT` of the Evidence clock's answer at that read, preserved for attribution |

**Replays, as the Principal specified.** Interval 10 on the Evidence
clock; `BIND` at `E_b = 101`, `t_b = 0`; `TR-x` decided `ADMITTED`.

| # | Case | Sequence of commits | Durable deciding record | Refusal or continuation |
| --- | --- | --- | --- | --- |
| 1 | `BIND` → fence → Apply | `BIND` 101; `FENCE(AU)` 102 closes `R` (accounting release of never-attempted allowance into the fenced grant), attempts `FENCED`; Apply of `TR-x` citing 101 at `N = 11`, Apply-side conditions holding | `BIND` 101 (eligibility); the Apply (consumption); the `FENCE` (closure) | **Applies.** The freeze ends on the Apply; `R` is closed by the fence and stays closed; every new attempt or reservation under `AU` is `FENCED`; admitted `PENDING` liabilities remain accountable and settle; the subject can spend only under a successor grant, which inherits nothing. Consumption unfences nothing. A revocation applied before the Apply instead refuses it and invalidates 101 atomically (`APPLY_REFUSED`, condition: Authorization inactive, citing the revocation's Apply) |
| 2 | Pre-expiry witness → pause → invalidation → release → delayed Apply | Process A reads `t = 9`, pauses; process B, in the continuation role, obtains receipt `(t = 11, E = 120)` and requests `BINDING_INVALIDATED(101, INTERVAL_ELAPSED, {101, 10, role, (11, 120)})`, appended at `n_i = 12`; B commits `RELEASE(101, 12)` at `E = 130`; A resumes and presents Apply citing 101 | The invalidation at `n_i = 12` | A's Apply **refused `BINDING_INVALIDATED`**. A's earlier witness established no right; `TR-x` awaits re-check and a fresh `BIND` |
| 3 | Apply wins against invalidation | A commits Apply citing 101 at `N = 11`; B's invalidation request arrives after | The Apply at `N = 11` | B's request **refused `ALREADY_APPLIED`**; B's `RELEASE` cannot be formed (`NO_INVALIDATION`); binding consumed; the freeze ended at `N = 11`; B reconstructs consumption from the Apply and does nothing |
| 4 | Invalidation wins against Apply | B's invalidation appended at `n_i = 12`; A's Apply citing 101 presented after | The invalidation at `n_i = 12` | A's Apply **refused `BINDING_INVALIDATED`**; `R` is frozen pending release until a process in the continuation role commits `RELEASE(101, 12)`; a second invalidation refuses `DUPLICATE`; a fence may close `R` meanwhile |
| 5 | Death after Apply, before any further Evidence write | Apply citing 101 at `N = 11`; the process dies | The Apply at `N = 11` | A fresh process finds `TR-x` `APPLIED` citing 101: consumed; it does not re-apply (`ALREADY_APPLIED`), cannot invalidate (`ALREADY_APPLIED`) and cannot release (`NO_INVALIDATION`). The freeze ended at `N = 11` with no Evidence record. `R`'s purpose is the subject; the original grantee's later attempt is admitted iff the ordinary checks pass (continuation trace below) |
| 6 | Death after invalidation, before release | `BINDING_INVALIDATED(101)` at `n_i = 12`; the process dies before `RELEASE` | The invalidation at `n_i = 12` | Every Apply citing 101 refuses from `n_i` on. `R` is frozen pending release (no attempt, no grantee close, expiry unread) until a process in the continuation role commits `RELEASE(101, 12)` once; concurrent releases cannot commit twice; no promise of release exists while no such process runs; a fence can still close `R`. After `RELEASE`, `R` is read: fenced, expired or open |
| 7 | Old binding invalidated, fresh binding created, old operation resumes | Invalidation of 101 at `n_i = 12`; `RELEASE(101, 12)` at 130; fresh `BIND(TR-x, R)` at 131 (`R` not frozen, open, unfenced, unexpired; no binding of `TR-x` undisposed or unreleased); the old operation presents Apply citing 101 | The invalidation of 101; the fresh `BIND` 131 | Old Apply **refused `BINDING_INVALIDATED`** (identity 101). A second `RELEASE(101)` refused `ALREADY_RELEASED`; `RELEASE(131)` refused `NO_INVALIDATION`. The fresh process applies citing 131: consumed. Re-invalidating 101 is refused `DUPLICATE` before Apply(131) and `ALREADY_APPLIED` after; neither touches 131 |
| 8 | Duplicate and malformed settlement after revocation | Attempt `X` `PENDING` (max 10) under `R`; `FENCE` then revocation applied; former grantee settles `X` at 7 with the provider's record: admitted at `E = 140`; the same settlement resubmitted after a lost response; a settlement of `X` at −3; a settlement of `X` by an unrelated caller; a settlement naming a reservation `X` does not belong to | The first valid settlement at `E = 140` | Resubmission **refused `ALREADY_SETTLED`**, no accounting change; the −3, the unrelated caller and the wrong reservation **refused `INVALID_SETTLEMENT`**, preserved; invalid submissions before `E = 140` leave 10 outstanding, after it leave the settled 7; `C` moved from 10 to 7 exactly once |

**Re-run under revision 4.**

| Trace | Sequence | Result under the freeze standing table |
| --- | --- | --- |
| Successful-Apply continuation (case 5 extended) | `R` amount 10, no attempts, expiry 20; `BIND` at `t = 0`; Apply at `t = 1`; death. At `t = 2` the original grantee requests an attempt of maximum 3 for the registered subject | The Evidence boundary reads the Transition ledger (rule 8), finds the Apply citing 101: consumed, not frozen. Caller is the grantee, purpose the subject, expiry 20 unpassed, no fence, allowance 10 ≥ 3, headroom and cap holding: **admitted**. A duplicate identity refuses `DUPLICATE_ATTEMPT`. A later grantee `CLOSED` releases 7 and keeps the pending 3 as a liability; settlement at 2 moves it to actual consumption once. Alternatively, with no attempt and the first read at `t = 21`: `R` closes on expiry, releasing 10; a new attempt refuses `RESERVATION_EXPIRED`. With a pending 3 it releases 7 only. A prior fence: closure already stands, attempts `FENCED`. Headroom exhausted by an overrun elsewhere: `GRANT_EXHAUSTED`, or `OVERSPENT` if the committed total exceeds the grant; close and valid settlement remain possible. Transition ledger unreachable at `t = 2`: the attempt refuses `LEDGER_UNREACHABLE`; nothing is spent and nothing is released. No path needs or permits a `RELEASE` after Apply |
| Delayed-Apply race (cases 2 and 4) | A witnesses `t = 9`; B requests invalidation with receipt `(11, 120)`; A's Apply and B's request reach the Transition boundary in either order | Whichever commits first excludes the other: Apply first → B refused `ALREADY_APPLIED`, consumed, freeze ended; invalidation first → A refused `BINDING_INVALIDATED`, `R` frozen pending release until `RELEASE(101, 12)`. An old post-threshold receipt proves passage at its instant only; the boundary still serializes against Apply and verifies the exact binding. Allowance is freed to reuse only by `RELEASE`, which requires the invalidation that excludes A |
| Fence interaction (case 1) | `BIND` 101; `FENCE` 102; Apply 11 | The fence closes `R` and makes its accounting release into a grant nothing can reserve; the registration applies on the eligibility of 101; the freeze ends at the Apply; `R` remains closed; no attempt or reservation under `AU` admits; liabilities settle; a successor grant is separately authorized and inherits nothing. The fence's accounting release is never written as `RELEASE(E_b, n_i)` |

**Allowance check across the failure paths.** Allowance frozen by a
binding leaves the freeze by the Apply citing the binding (into the
ordinary checks of rule 4, with the original grantee, purpose changed,
expiry unchanged) or by `RELEASE` after a durable invalidation that
refuses every later Apply citing that binding. A fence's accounting
release goes only into a grant nothing can reserve. Expiry is unread
while frozen. So no path frees allowance to any other consumer while an
Apply citing the old binding remains possible, and no consumed binding
strands allowance.

**`P-1` condition (b), replacement.** "the funding Authorization is
active at the head, and the declared research budget is covered by a
`RESERVATION` the proposer committed before the Check, named in the
proposal, with purpose this Transition; the Apply cites a `BIND` of
this Transition to that reservation that is not invalidated, and
eligibility is the one established at that `BIND` (§III.5, §III.8);
the reservation binds to the registered subject on Apply".

**D-17, replacement of the Evidence-side clause.** "for a proposal
declaring metered consumption, an Apply citing a `BIND` of this
Transition that is not invalidated, or a fresh `BIND` after every prior
one has a terminal disposition and, if invalidated, a `RELEASE`; a
binding is never released without its durable invalidation, and an
applied binding is consumed whether or not any later record exists.
Registration eligibility established at a `BIND` survives a later
fence, expiry instant or overrun with the effects §III.5 states, and a
reservation frozen by a binding is not read for expiry until the freeze
ends; the 'bypasses no fence, expiry, exhausted allowance or suspended
delegation' rule is unchanged for every attempt, reservation and
continuation other than this registration eligibility".

**§III.8 Lifecycle, addition.** "A `DECIDED ADMITTED` Transition that
declares metered consumption carries zero or more appended
`BINDING_INVALIDATED` events and at most one Apply; an Apply and an
invalidation of the same binding exclude each other at this boundary,
which alone establishes terminal invalidation, under the two grounds
§III.5 names and no other."

**Comparison with earmarking**, corrected from revision 2:

| | Apply binding (recommended) | Earmark at reservation |
| --- | --- | --- |
| Funding eligibility decided | At `BIND`, immediately before the Apply attempt, against fences, closes, expiry and overrun by Evidence sequence | At the reservation's own commit |
| Fence after the eligibility point | Registration may still apply; no attempt after the fence | Same |
| Expiry after the eligibility point | Unread while frozen; read after the freeze ends | Suspended while earmarked |
| Overrun elsewhere after the eligibility point | Registration may still apply; new spending obeys headroom and cap | Same |
| What a false funding fact at the eligibility point does | Refuses `BIND`, hence the Apply | Refuses the reservation only; an Apply days later rests on a reservation that may have been fenced or overspent since |
| Apply versus release ordering | Serialized on the Transition ledger by the terminal disposition | No release exists; nothing to order |
| New records and rights | `BINDING` kind; one lifecycle event; the Evidence caller extension; the terminal-invalidation authority | None |
| Recommendation | **Adopt.** Eligibility is current to the Apply attempt and the release path is exact | Acceptable if the Principal prefers no new kind and accepts eligibility aged by the whole Check interval |

### Delta of Group 2

```text
ΔO: +1 Research Record kind BINDING, forms BIND and RELEASE (Evidence
    ledger). BINDING_INVALIDATED is an appended lifecycle event on an
    existing Transition, not a new object.
ΔS: the accounting table; the admission predicates with headroom; the
    settlement clarification (R2-3, meaning preserved); underrun
    disposition; the binding policy (eligibility at BIND; effects of
    later fence, expiry and overrun); the freeze standing table with
    the consumed case ending the freeze from the Apply alone; the
    deferral of expiry reads while frozen, superseding PD-008's
    automatic expiry release for the frozen interval only; the
    terminal disposition with the lifecycle event BINDING_INVALIDATED,
    its two grounds and their recorded evidence; the release rule; the
    Evidence boundary's derivation rule (refuse when unreachable); the
    interval meaning; the recovery rule; binding interval as
    Authorization content; carrier classes; P-1 (b); D-17; §III.8
    lifecycle.
ΔA: item 1. Evidence caller extension: the Apply boundary commits BIND
    and RELEASE on the Evidence ledger for Transitions it is applying,
    nothing else, deciding nothing.
    item 2. Terminal-invalidation authority: the Transition commit
    boundary's exclusive, narrowly bounded right and duty to establish
    BINDING_INVALIDATED under two grounds only: (a) atomically with its
    own Apply-side refusal, recording the failed condition and cited
    authority; (b) on an attributable request from a process acting in
    the Apply-boundary continuation role under D-17 after the binding
    interval, recording the exact BIND, the applicable interval, the
    requesting role and the verified Evidence-clock receipt. The
    requesting role holds the request right on ground (b) only. No
    discretionary cancellation ground exists for any party. Existing
    ownership of the Transition ledger is not this grant.
```

### Decisions for the Principal

| Question | Recommendation |
| --- | --- |
| Headroom and cap predicates on every attempt (Codex recommends approval) | Yes; the only predicates that close admission after an overrun |
| Underrun disposition | To the open reservation; to headroom once closed |
| Settlement clarification in the review's words | Retain; `0/0/0` |
| Eligibility established at `BIND`, surviving a later fence, expiry and overrun with the effects of rule 3; expiry unread while frozen, accepting that unused allowance can stay frozen past expiry with no release promised during an outage | Yes; the policy the Principal directed, with the tradeoff explicit |
| Terminal disposition on the Transition ledger; the boundary's exclusive terminal-invalidation authority under the two grounds with their recorded evidence (`ΔA` item 2); `RELEASE` only after a durable invalidation | Yes; the only exact closure of Apply against release using existing ledgers |
| Interval as permission to request invalidation, nothing more | Yes |
| Apply binding (`ΔO` +1, `ΔA` +2) versus earmarking | Binding |

## 3. Group 3 — Evidence completion and binding (B-5, B-6, B-7)

### B-5: observation cutoff, canonical Outcome, grace

| Clause | Replacement |
| --- | --- |
| C §III.7 Source Declaration | add to meaning fields: "**resolution grace**: for a source used in resolution sets, the duration on the Evidence clock after a member's period end within which the source's declared print is expected; pinned by the `SourceRevision` at each Prediction's commitment. A declaration without one cannot be a resolution source, as with the deterministic extraction rule; the Checker refuses the registration" |
| C Part X §6, new row **Observation cutoff rule** | "A member's **cutoff** is its period end plus its source's resolution grace, fixed at the Prediction's commitment. The Prediction's cutoff is the latest member cutoff. A member is **observed** iff a `VALUE` Observation of its declared print has witnessed receipt at or before its cutoff; its bound Observation is the one the print rule selects among those. Missingness is a function of the ledger and the pinned cutoffs alone" |
| C §III.5 Outcome row | replace "`UNRESOLVABLE`, with the missing member named, when a member has no `VALUE` by the Standard's deadline" with: "The Outcome is a deterministic function of the resolution set, the pinned cutoffs and the Evidence ledger: resolved when every member is observed, `UNRESOLVABLE` naming each member not observed. **When it is computed changes nothing**: a Prediction whose members were all observed before their cutoffs resolves identically whether the Outcome is committed before or after the cutoff; a `VALUE` witnessed after a member's cutoff is a Market Observation that never qualifies, whether or not any Outcome has yet been committed. An Outcome may be committed before the Prediction's cutoff only when every member is already observed. **At most one Outcome per `PredictionId`**: the Evidence boundary refuses a second (`DUPLICATE_OUTCOME`), preserved; the first committed is canonical. The Checker's duty to commit expected-but-missing Outcomes falls due at the Prediction's cutoff" |

Resolver scheduling cannot change the result: two resolvers computing at
different times after the cutoff bind the same qualifying Observations;
one computing before the cutoff can only commit a fully observed
result, which is the same result. The universal five-session default of
revision 1 is **withdrawn**: a grace is a fact about a source's
publication lag, declared per source by the Principal in the
Observation Authorization, not a Standard constant.

Adversarial trace: member `M` period ends day 10, grace 2 days, cutoff
day 12. (a) `VALUE` witnessed day 11; the Outcome is computed day 20:
resolved; day 20 is irrelevant. (b) No `VALUE` by day 12; `VALUE`
witnessed day 13, nobody has committed an Outcome yet: `M` is not
observed; the canonical Outcome, whenever committed, is `UNRESOLVABLE`
naming `M`; the day-13 value is a Market Observation and nothing more.
(c) Two Checkers commit on day 12 and day 14: identical content; the
second refused `DUPLICATE_OUTCOME`. Interruption: a Checker dies
mid-computation; nothing is committed; the next computes the same
function.

Identity effect, declared: the Outcome's identity is tightened to "the
Outcome of Prediction `P`". Delta: `ΔS` (Source Declaration field; the
cutoff rule; the Outcome row); `ΔO` 0; `ΔA` 0.

### B-6: method commitment binding by ledger and identity

Replacement for Part X §3's selection rule: "The commitment in force for
a scored event is the subject's **registration commitment** unless a
successor `EXPERIMENT DESIGN` commitment for the subject has Evidence
sequence below the event's. The registration commitment precedes every
eligible event by construction on the existing ledgers: a Strategy
Decision's closure `N` is at or above the registration's Apply sequence,
because the Runner runs admitted versions by standing; a Hypothesis's
relevant event is the **Prediction's commitment**, and the Evidence
commit boundary refuses a Prediction whose `HypothesisId` is not
admitted at the Applied History head it witnesses at commit (the witness
read of §III.5, extended from Decisions to Predictions). Successor
commitments and events are compared within the Evidence sequence only."

Trace: registration at Apply 200, Evidence at 20, first Decision at
`E = 21` with closure `N = 200`: the registration commitment governs. A
Prediction for an unadmitted Hypothesis: refused at commit. Delta: `ΔS`;
`ΔA` 0 (an I-13 read of the kind PD-002 established).

### B-7: cost evidence through the Observation route

Replacement for Part X §3 cost verification (b): delete "or recorded in
the Check with their provenance"; "checks the model against **market
evidence committed as Market Observations** under declared sources for
spreads, volume, depth and fees, by sequence and before the Check; the
Check cites them. Evidence not so committed cannot be cited (§III.8).
Where no declared source exists for an instrument class, the cost model
is unverified and `Qualify` is withheld under (f)." Trace: a Checker
reading a vendor page during a Check cannot cite it; the cost line is
`NOT MET` or, with no Observation at all, `NOT DETERMINABLE` on the cost
criterion, which withholds `Qualify` rather than stopping the Check.
Delta: `ΔS` (removal of a route admitted by PD-005; see §5); `ΔA` 0.

## 4. Group 4 — Safe exposure reduction (B-8, B-9, B-10)

### B-8: a fill must still reduce at its admission

| Clause | Replacement |
| --- | --- |
| C §III.10, "A fill of a `REDUCING` order is `EFFECTIVE` at commit" | "A fill of a `REDUCING` order is admitted only up to the **reducing bound at the head**: the confirmed position of the version in the instrument, plus same-side `PROVISIONAL` fills, toward zero and not through it. The admitted quantity is `EFFECTIVE` at commit; any excess is refused `REDUCING_BOUND` and preserved; the order's unfilled remainder stays open. No fill inherits reduction from its order's class" |
| C §III.10 Intent class, split sentence | append: "The beyond-zero leg of a reversal is **derived only when the to-zero leg's fills are `EFFECTIVE` and the position is zero**; until then it does not exist, and after expiry it is never derived" |

Trace: +40; sell 40 `REDUCING`; sell 30 not derived. Fill 40 before
`T`: position 0; sell 30 may be derived with a read `t < T`. After `T`
no set is derived. If sell 40 filled only 10 (+30) and `T` passed, a
later fill of sell 40 is bounded to 30. Interruption: the Execution
function dies between the to-zero fill and deriving the beyond-zero leg;
on restart the position is zero and `T` has passed: nothing is derived.

### B-9: remove `FLATTEN_ON_QUOTA`

Delete "optionally `FLATTEN_ON_QUOTA`" (§III.10 Expiry) and "and, where
declared, quota exhaustion of applied allocations" (§III.7 triggers).
Quota exhaustion refuses opening and does not expire. Trace: quota
exhausted Monday, `T` Friday: no set Monday; opening refused all week;
Friday's read derives the set; a Wednesday restart finds no obligation.
Delta: `ΔS` removal of an option PD-004 admitted; `ΔA` 0 (trigger set
narrows). **This is a new policy choice**, not transcription (§5).

### B-10: `REDUCE` without standing promotion

| Clause | Replacement |
| --- | --- |
| C Part V Allocation row, Content | add: "`REDUCE`: a new amount lower than the amount in force, including zero, for an allocation of any purpose; cites the Evaluation or limit finding that motivates it, which need not meet any qualification floor" |
| C Part V Allocation row, Check for `REDUCE` | "(i) composition at the lower amount; (ii) the **standing recorded is never higher than before**: `QUALIFIED` stays `QUALIFIED` at the lower amount, `EXPLORATORY` stays `EXPLORATORY` with its `expiry_time`, quota and instruction unchanged, and zero is `INCUBATING`; a `REDUCE` never promotes and never qualifies; (iii) **risk effect**: every limit usage is non-increasing and no new instrument exposure is created; where an existing breach cannot be eliminated in one step, the Check records the **residual breach** (the same limit, smaller or equal after) as distinct from a **new or worsened risk** (any limit usage that increases, or a breach that appears), and admits only the former; (iv) the **residual execution obligation**: the Execution function re-executes to the lower target under the new key (§III.10), an incomplete reduction remaining a visible obligation; the Apply changes the target and liquidates nothing. No forward-event floor, cost verification or stress qualification is required to withdraw exposure" |
| C Part V Allocation row, Proposer and Decider for `REDUCE` | "Principal; never a policy" |
| C Part V "Standing Transition after expiry" row | rename "Standing Transition after expiry or `REDUCE` to zero" |
| C §III.6 | append: "**Withdrawing allocation** is an Apply that changes the target; **flattening positions** is the Execution function's re-execution duty toward the new target (§III.10). They are distinct facts; neither an allocation change nor a standing label flattens anything" |
| C Part V, new row **Limits** | "Limits Transition: Applied History limits (exploratory pool, caps, portfolio limits); proposer the Principal; Checker (composition at the head under the new limits; no breach created silently); decider the Principal; `0/0/0`" (transcription of PD-004 §III.6 and §PD-004.11) |

Trace: a version `QUALIFIED` at 10; a limit breach under stress; the
Principal proposes `REDUCE` to 6 (zero would breach a portfolio net
limit through the short leg of a hedge, a worsened risk); the Checker
records the residual breach at 6, no new risk; Apply: allocation 6,
standing unchanged; the Execution function derives `REDUCING` orders to
the 6 target, each fill bounded (B-8). A second `REDUCE` to 0 follows
when the hedge is unwound. An `EXPLORATORY` allocation reduced to 0:
`INCUBATING`; its expiry obligation is superseded by the new target,
which the re-execution duty carries (PD-004: "the successor's rules
carry the residual"). Interruption: death after Apply and before any
order: restart derives the obligation from allocation versus confirmed
position, as T-D does.

Delta of Group 4: `ΔO` 0; `ΔS` the clauses above; `ΔA` 0 (`REDUCE` is
the Principal's, who decides every Allocation). Decision: whether any
policy may ever decide `REDUCE`. Recommendation: no.

## 5. Reconciliation of C-1 to C-7, and the classification of every item

Two classes: **A** applies an already-admitted decision to text or
examples (no new choice); **B** chooses new policy, semantics or
authority (Principal decision).

| Ref | Item | Class | Treatment |
| --- | --- | --- | --- |
| C-1 | Part IX principle 4 wording; I-4 continuity sentence; T-A dates; T-B transfer to a zero-record successor; T-C merged acts; T-F/T-G annotation | A | Principle 4: "Capital and allocation budgets are consumed at Apply; research budgets are reserved before and settled after the work". I-4: "The predecessor's record remains visible and transfers nothing". T-A: commitment moved to 2026-10-15 15:50. T-B: `TR-310` becomes an `EXPLORATORY` allocation with purpose, `expiry_time`, `FLATTEN`; `SV-5.3` retired by a standing act. T-C: registration, fence, grant, revocation as four acts. T-F/T-G annotated historical where PD-004 to PD-008 differ |
| C-2 | Sequence-zero projection; re-check binding; genesis coordinates | A | §III.6: Population State at 0 is the projection after Apply 0; "first `N`" counts 0 as first. §III.8: a re-check appends a Check naming the base it checked; decision and Apply cite it; the proposal is never rewritten. PD-009: first clock instant and empty coordinates `E = 0`, `N = −`, `F = N/A` |
| C-3 | Hop depth literal; R-8 "two consecutive"; checklist item 11 | A | "(default 2, a provisional Authorization default admitted by PD-003)"; cross-reference; checklist reworded |
| C-4 | Checker proposals; refusal vocabulary | A | "proposes nothing but its own successor and, as any agent may, a Constitutional Transition `STOPPED` until the Principal decides" (Part V already allows the latter). Known failed gate → `NOT MET` → `FAIL`; `NOT DETERMINABLE` → `STOP` only for constitutional indeterminacy; PD-007's example corrected |
| C-5 | Classification timing | **B** | `CLASS PENDING` as a reported state until the Outcome binds, finalized then and never changed, is a new lifecycle label for an existing fact and a Principal choice. Dispatch ambiguity: A, transcription of PD-008's unknown-effect rule |
| C-6 | Provider binding; storage | provider: **B**; storage: A | "For this prototype the registered provider and model version are fixed to the Agent Design Version; substitution is `STOPPED` until a rule is admitted (D-14)" is a new explicit limit. "A replaceable store may host the logical ledgers; hosting confers no decision right" transcribes principle 10 |
| C-7 | Own-subject routing in `AU-CK-A` | A | PD-009's admitted routing as Authorization content |
| B-7 | Remove the Check-recorded cost route | **B** | PD-005 admitted the alternative; removing it reconciles a contradiction but changes an admitted rule |
| B-9 | Remove `FLATTEN_ON_QUOTA` | **B** | PD-004 admitted the option |
| B-5 | One Outcome per Prediction; cutoff rule; grace per source | **B** | New cardinality, new rule, new Source Declaration field |
| B-2 | `F = N/A`; budget line `N/A` for control acts | **B** | New applicability rules |
| B-6 | Prediction witness read | **B** | A new refusal at the Evidence boundary |
| Limits row | Part V row | A | Transcription of PD-004 |
| Sequence 17 | Delete, or make `P-1` applicability Authorization content | **B** | Changes PD-009's approved sequence |

Revision 1 wrongly listed B-9, the Outcome cardinality, `F = N/A` and
`CLASS PENDING` as reconcilable under existing approvals; they are
choices.

## 6. Interactions across the groups

| Interaction | Finding |
| --- | --- |
| Apply binding (G2) and fence (G1) | Same ledger; exact at `E_b`. A fence above `E_b` closes the bound reservation and forbids attempts; the registration may still apply (rule 3). A fence on a Checker Authorization never meets a `BIND`, because Checker reservations are never bound |
| Apply binding and the Checker's reservation (G1) | Disjoint: the Check's reservation has a verification purpose and ordinary lifecycle; the `BIND` names the proposer's reservation only |
| Headroom predicate (G2) and Checker grants (G1) | Applies per Authorization; a Checker's overrun exhausts only its own grant |
| `BIND` freeze and attempts under `R` | While frozen `R` admits no attempt and its expiry is unread; the freeze ends from the Apply alone, or from `RELEASE` after invalidation, with no guaranteed maximum (rule 10). New failure checked: an expiry instant passing while frozen frees nothing and revives nothing; a consumed binding strands nothing, because the Evidence boundary derives consumption from the Apply (rule 8) |
| Terminal disposition (G2) and D-17 | A continuation process never releases from a negative read; it reads the Transition lifecycle for the disposition and acts only from it; an unreachable ledger stops it and refuses the dependent operation |
| `REDUCE` (G4) and the expiry obligation (PD-004) | A `REDUCE` to zero of an `EXPLORATORY` allocation supersedes the expiry obligation with the re-execution obligation; both derive from allocation versus confirmed position; no double flatten, because sets are keyed and duplicates refused |
| Reducing bound (B-8) and `REDUCE` re-execution | Re-execution to a lower target derives `REDUCING` orders whose fills are bounded; a worsened position between derivation and fill is refused at the bound, not executed |
| Cutoff rule (B-5) and `CLASS PENDING` (C-5) | A Prediction is `CLASS PENDING` until its Outcome binds; the cutoff rule fixes when that must happen; R-3 counts finalized Outcomes only |
| Prediction witness read (B-6) and `P-1` | A Hypothesis admitted under `P-1` at Apply `N` can have Predictions from the first Evidence commit witnessing `N`; none before |
| Genesis replay (G1) and Apply binding (G2) | Control acts bind nothing; the first budgeted Apply in the sequence is a Hypothesis registration under `P-1` in ordinary operation, which binds the proposer's reservation; `AU-RP-1` must declare its binding interval |
| Restart | Every new fact (`BIND`, `BINDING_INVALIDATED`, `RELEASE`, cutoff, reducing bound, `REDUCE` target) is a ledger or clock fact; D-17 reads them |

## 7. Decision brief

**Applies existing decisions (class A):** C-1, C-2, C-3, C-4, C-7, the
dispatch-ambiguity transcription, the storage sentence, the Part V
Limits row.

**Choices for the Principal (class B):**

| # | Choice | Recommendation |
| --- | --- | --- |
| 1 | Group 1's two `ΔA` items (Checker grantees reserve and attempt; funding-stop exception covers Checker Authorizations) | Yes |
| 2 | Budget line `N/A` for Principal control acts; `F = N/A — no Paper Book` | Yes |
| 3 | Headroom and cap predicates on every attempt; underrun to the open reservation, to headroom once closed; settlement validation as §2 states it | Yes (Codex: recommend approval, with validation retained) |
| 4a | Eligibility established at `BIND`; a later fence, expiry or overrun has the effects of §2 rule 3 and withdraws nothing; expiry is unread while frozen, so unused allowance can stay frozen past expiry until consumption or invalidation plus `RELEASE`, with no release promised during an outage (Codex: ready, subject to R3-1, now addressed) | Yes |
| 4b | At most one terminal disposition per binding, on the Transition ledger; the Transition boundary's exclusive terminal-invalidation authority under the two grounds with their recorded evidence (`ΔA` item 2); `RELEASE` only after a durable invalidation (Codex: ready, subject to R3-2, now addressed) | Yes |
| 4c | The binding interval permits a request for invalidation and is neither a release, a maximum freeze nor an Apply deadline (Codex: ready) | Yes |
| 4d | Apply binding (`ΔO` +1 `BINDING`; `ΔA` +2 as the Group 2 delta states; one lifecycle event; carrier classes declared) rather than earmarking (Codex: ready, subject to both corrections) | **Binding** |
| 5 | Resolution grace as Source Declaration content, no universal default; observation cutoff rule; at most one Outcome per Prediction | Yes (Codex: recommend approval for the late-observation cases) |
| 6 | Prediction witness read at the Evidence boundary | Yes |
| 7 | Reducing bound at fill admission; beyond-zero leg derived only at zero | Yes (Codex: recommend approval for the reversal failure) |
| 8 | Remove `FLATTEN_ON_QUOTA` | Yes (Codex: recommend approval) |
| 9 | `REDUCE` as an Allocation purpose, Principal-only, never promoting, with residual-breach versus new-risk verification | Yes (Codex: recommend approval for withdrawal of exposure) |
| 10 | Remove the Check-recorded cost route | Yes |
| 11 | `CLASS PENDING` until the Outcome binds | Yes |
| 12 | Provider and model version fixed to the Agent Design Version for the prototype | Yes |
| 13 | Delete genesis sequence 17 | Yes |
| 14 | T-A, T-B, T-C reworked; T-F/T-G annotated | Yes |

Codex's recommendations on choices 3, 4a to 4d, 5, 7, 8 and 9 are
review evidence; they admit nothing, and neither review passed on
choices 1, 2, 6 and 10 to 14.

**Order of application after decision**, then one re-audit on paper of
the audit's failed transitions, the eight binding replays of §2 and the
genesis walk, then a handoff to Codex at a new commit: Group 1 with C-7
and the Limits row; Group 2 with C-2; Group 3 with C-5 and B-7; Group 4
with the PD-004 cases re-run; C-1, C-3, C-4, C-6 and the PD-009
sequence change.

**Bounded correction check for Codex (revision 4).** Scope: §2 from
"Records and identity" to the Group 2 decisions, the §6 rows citing
them, and §8; the rest is unchanged from revision 3. Questions: whether
the freeze standing table and rules 2, 4, 7 and 8 are consistent for
every reference to frozen, consumed, released and expired; whether the
successful-Apply continuation trace admits the ordinary attempt, close
and expiry paths without any `RELEASE`; whether `ΔA` item 2 declares
the terminal-invalidation authority completely, with the evidence of
each ground, and adds no discretionary ground; and whether the carrier
classes are correct. After the check: Principal admission under §8's
approval block, propagation in the stated order, then the final
whole-design review.

## 8. Revision 4 closure map, final authority delta and approval block

**How the revised clauses close R3-1 and R3-2.**

| Finding | Point raised | Closing clause in §2 |
| --- | --- | --- |
| R3-1 | A binding "live until `RELEASE`" contradicted the freeze ending on Apply | "Freeze standing of a reservation" table: four exhaustive cases; the consumed case ends the freeze from the Apply alone; the word "live" is removed; rules 1 and 9 use "frozen" and "without a disposition or awaiting release" |
| R3-1 | "Freed by `RELEASE` and by nothing else" | Removed from rule 7; the allowance check names the two exits, Apply and `RELEASE` after invalidation |
| R3-1 | The fence's accounting release was conflated with binding `RELEASE` | The paragraph after the table and replay row 1: a fence closes `R` in every case; its accounting release is never written as `RELEASE(E_b, n_i)` and creates no reusable permission |
| R3-1 | Evidence must derive consumption from the Apply and refuse when it cannot | Rule 8: authoritative I-13 read of the Transition ledger before any dependent operation; `LEDGER_UNREACHABLE` refuses; a stale read can only leave `R` frozen |
| R3-1 | After consumption, ordinary checks; original grantee and expiry; successor inherits nothing; liabilities survive closure | Rule 4 "Effect on `R`"; rule 3's overrun and `PENDING` sentences; the successful-Apply continuation trace |
| R3-1 | Exclusivity must not assert completion or promise recovery | "Terminal exclusivity" paragraph: at most one disposition, one established when a terminal operation succeeds, no promise; rule 10 |
| R3-2 | Terminal invalidation claimed from ledger ownership | "Authority to commit each act" table and `ΔA` item 2: exclusive, narrowly bounded, under both grounds; ownership is not the grant |
| R3-2 | Durable evidence of each ground | Rule 5: failed condition and cited authority for `APPLY_REFUSED`; exact `BIND`, interval, requesting role and verified clock receipt `(t, E)` for `INTERVAL_ELAPSED`; "any process" replaced by the continuation role in replay rows 4 and 6 |
| R3-2 | Carrier classes | "Carrier classification" table: `BIND`/`RELEASE` and Apply/invalidation `AUTHORITATIVE` for their acts; consumed, frozen and budget views `DERIVED`; the clock answer `RECEIPT` |
| R3-2 | Reconcile the delta and the decision brief | Group 2 delta restated with two `ΔA` items; §7 rows 4a to 4d and the Group 2 decisions table restated |

**Final constitutional delta of PD-010, all groups.**

```text
ΔO: +1  Research Record kind BINDING (BIND, RELEASE), Group 2.
ΔS:     Groups 1 to 4 and §5 as each section states; the new
        Transition lifecycle event BINDING_INVALIDATED is ΔS on an
        existing object.
ΔA: +4  Group 1: (1) holders of a Checker Authorization may commit
        RESERVATION, attempt and settlement records under their own
        grant; (2) the Principal's funding-stop exception extends to
        Checker Authorizations.
        Group 2: (3) the Apply boundary as caller of the Evidence
        boundary for BIND and RELEASE only; (4) the Transition commit
        boundary's exclusive terminal-invalidation authority under the
        two grounds, bundling the continuation role's request right on
        ground INTERVAL_ELAPSED.
        Groups 3 and 4: none.
```

**Consolidated approval block.** Every remaining Principal choice, in
the form an admission would cite. Nothing below is admitted by this
record.

```text
PD-010 revision 4, choices for admission (document-phase):
 1. Group 1 ΔA items (1) and (2).                       [recommend YES]
 2. Budget line N/A for Principal control acts;
    F = N/A — no Paper Book.                             [recommend YES]
 3. Headroom and cap predicates on every attempt;
    underrun to the open reservation, to headroom once
    closed; settlement validation as §2 states (0/0/0).  [recommend YES]
 4a. Eligibility at BIND; later fence, expiry, overrun
    withdraw nothing; expiry unread while frozen, with
    the declared tradeoff (no release promised).         [recommend YES]
 4b. At most one terminal disposition per binding on
    the Transition ledger; ΔA item (4); RELEASE only
    after durable invalidation.                          [recommend YES]
 4c. Binding interval = permission to request
    invalidation only.                                   [recommend YES]
 4d. Apply binding (ΔO +1; ΔA items (3), (4)) rather
    than earmarking.                                     [recommend BINDING]
 5. Resolution grace per Source Declaration, no
    universal default; observation cutoff rule; one
    Outcome per Prediction.                              [recommend YES]
 6. Prediction witness read at the Evidence boundary.    [recommend YES]
 7. Reducing bound at fill admission; beyond-zero leg
    derived only at zero.                                [recommend YES]
 8. Remove FLATTEN_ON_QUOTA.                             [recommend YES]
 9. REDUCE: Principal-only, never promoting, residual
    breach versus new risk.                              [recommend YES]
10. Remove the Check-recorded cost route.                [recommend YES]
11. CLASS PENDING until the Outcome binds.               [recommend YES]
12. Provider and model version fixed to the Agent
    Design Version for the prototype.                    [recommend YES]
13. Delete genesis sequence 17.                          [recommend YES]
14. T-A, T-B, T-C reworked; T-F/T-G annotated.           [recommend YES]
Class A items (C-1, C-2, C-3, C-4, C-7, dispatch-ambiguity
transcription, storage sentence, Limits row) apply on admission
without a separate choice.
```

Sequence after this record: Codex's bounded correction check of
revision 4; the Principal's admission of the choices above, in whole or
by number; propagation into the Constitution in §7's order with one
paper re-audit; the final whole-design review by Codex before
`ConstitutionVersion 1`.

Nothing in this record applies any repair, admits any decision,
certifies anything, executes genesis, selects a runtime or authorizes
code.
