# Independent review of PD-010 revision 2 — binding, release and settlement

Status: **AUDIT — EVIDENCE, NOT DOCTRINE. Revision 2's binding protocol
is not ready for approval as written. No admission or implementation
authorization is made here.**

Date: 2026-10-19. Reviewer: Codex.

## Subject and disposition

Read the full [PD-010 revision 2](../decisions/principal_decision_010_codex_audit_repairs.md),
including its interactions and decision brief, against Constitution
revision 10, PD-008's funding and settlement rules, and PD-009's
continuation rule. This is the focused follow-up requested by the
Principal, not a second general readiness audit.

Branch `main`, HEAD `895f953aca14e440c1593db8f0f7088da0556cb2`.
PD-010 is an uncommitted proposal, not an admitted change. Exact reviewed
file SHA-256:

```text
bbb4b1b0b6a7e96613890eff7d9ab63e663c662e8ed158f45b1d9645ea88704d
```

The pre-existing modifications to `AGENTS.md` and the document-first
plan, the proposed PD-010, and the original independent audit are
preserved. Only this review is added.

**Recommendation:** approve the accounting, observation-cutoff and
reduction choices identified below, subject to retaining existing
validation requirements. Hold decision-brief choice 4, the binding
protocol, for a narrow correction. Its text explicitly permits a
pre-fence binding to authorize a later registration; that policy can be
coherent, but it is a change from requiring funding eligibility at the
later Apply commit. The expiry/release rules do not yet establish that
an old in-progress Apply cannot succeed after its binding is released.

The Apply record itself can establish consumption after process death.
A missing Evidence-side completion acknowledgement is not, by itself,
a defect: revision 2 does not require such an acknowledgement. What is
missing is a rule that makes successful Apply and release mutually
exclusive, including delayed operations and recovery.

“Approve” here is a recommendation to the Principal on specific choices.
The reviewer admits no policy, changes no governing text and does not
close the whole-design audit.

## 1. BIND → fence → Apply

**Clauses:** PD-010 §2, binding steps 1–3, 6–8; “The at-Apply condition,
as now defined”; comparison table; counterexample replay; proposed
`P-1` condition (b).

| Event | Facts and consequence under revision 2 |
| --- | --- |
| `BIND(TR-x,R)` commits at E=101, time `t_b` | R is open, unfenced and unexpired; the grant is not `OVERSPENT`. Binding eligibility has been established at this Evidence sequence |
| Principal commits `FENCE(AU)` at E=102 | New attempts under AU are forbidden. The original fence rule closes reservations; step 2 preserves this binding's registration eligibility despite the later fence |
| Apply commits within the binding interval, with base current, Authorization still active and policy unsuspended | **Yes: registration applies.** Revision 2's own replay expressly says so. It cannot then fund a new post-fence attempt |

This answer changes if the Principal also completes revocation or
suspends the policy before Apply: those are Apply-side conditions, and
step 3 still checks them. A funding fence alone is deliberately different
from an applied revocation.

**Finding R2-1 — High, policy clarification required:** the binding is
an eligibility decision at `E_b` that survives certain later events.
It does not prove that R is unfenced, unexpired or funded at the later
Apply commit. Step 2 similarly protects against a later reservation
expiry or overrun, including one that exhausts funding elsewhere in the
grant. Freezing new attempts under R does not freeze settlements of
existing liabilities elsewhere, nor should it prevent their recording.

The comparison table's assertion that a fence “between reservation and
Apply” refuses Apply is true only when the fence precedes BIND. Its
assertion that a prior false funding fact never admits registration
needs the same qualification: prior to BIND, not necessarily prior to
the Apply commit. Calling `E_b` “immediately before Apply” does not
exclude an intervening fence or a process interruption.

**Smallest repair:** expressly present for Principal decision:

> A binding admitted before a funding fence retains eligibility for
> its one named registration, subject to the binding's terminal
> disposition and the remaining Apply-side conditions. The later
> fence still forbids new attempts. Reservation expiry and later
> overruns have the specifically stated effects on that eligibility;
> they are not silently ignored by calling it “open at Apply.”

Reconcile the fence's reservation-close rule with the binding's freeze
and release rules. Releasing a binding must not reopen a fenced grant
or revive an expired reservation. The binding may protect eligibility
without pretending the underlying funding fact remains unchanged.

**Decision / OSA:** Principal semantic and permission decision required.
The new kind/caller declarations do not, alone, admit this survival
policy. It is not an inherently incoherent choice, but choice 4 must not
be approved on the claim that the original at-Apply condition is
preserved exactly.

## 2. BIND → interval expires → delayed Apply

**Clauses:** PD-010 §2, binding steps 3–7, particularly the interval
tested “at the Apply's witness read”; D-17 replacement.

Let the declared binding interval end at Evidence-clock time 10. The
numbers are illustrative; no interval length is recommended.

| Order | Process A: delayed Apply | Process B: recovery | Durable state |
| --- | --- | --- | --- |
| 1 | Commits BIND at time 0; base N=10 | — | BIND exists, no Apply or RELEASE |
| 2 | Reads the Evidence clock at time 9 and finds the binding valid; then pauses before committing Apply | — | Witness satisfied the stated interval test; N remains 10 |
| 3 | Still paused | At time 11 reads no Apply, finds the binding stale, commits `RELEASE(E_b)` under steps 6–7 | RELEASE exists; R returns to ordinary lifecycle, potentially reusable or closable |
| 4 | Resumes; base remains 10, Authorization active, policy unsuspended; presents Apply citing the old binding and witness | — | No stated terminal Apply-boundary rule excludes this previously in-progress operation |

**Finding R2-2 — Blocking:** the old pre-expiry witness does not prove
that the later Apply commits within the interval. Nor does RELEASE on
the other ledger, by itself, prevent an already-running operation from
committing. “A stale BIND is cited nowhere” states the desired result,
but the following recovery rule does not establish it.

Adding a last read of Evidence is insufficient: pause A immediately
after that last read, let B release, then resume A. A process timeout
or a belief that A died is not a durable exclusion of its queued or
in-progress operation. The original ordering gap has moved to
RELEASE/expiry versus Apply.

The same issue appears without a long delay if one recovery process
observes no Apply while another is completing it. Serializing the two
Apply commits prevents duplicate Apply, but does not automatically
serialize an Apply commit with an Evidence-side release.

**Smallest repair obligation:** for the exact binding identified by
`E_b`, establish one durable terminal choice: either Apply consumes it,
or a disposition makes every later Apply citing it inadmissible.
RELEASE may unlock the reservation only after the latter is established.
This disposition must be enforced by the boundary that admits Apply,
not only by the process asking that boundary to act. It must also
distinguish an old binding from any fresh binding after recheck.

One way to state that obligation using the existing ledgers is to require
a binding-specific terminal refusal/invalidation on the Transition side
before releasing on Evidence, serialized there against Apply. If Apply
wins, recovery cannot release that binding as unused. If invalidation
wins, the delayed Apply is refused. This is a proposed narrow repair
direction, not an admitted lifecycle rule or a request for a new object,
service or storage technology.

The Principal must also choose what the interval bounds. If it is a
strict deadline for the Apply commit, a pre-commit clock witness alone
does not establish it. If expiry instead permits recovery to seek the
terminal invalidation, say so: an operation that wins the terminal race
has a different contract. Do not claim both meanings at once.

“A dead Apply freezes R for at most the interval” also does not follow
from a rule requiring a recovery process to release it. No release is
guaranteed at the deadline while every relevant process is unavailable.
State eligibility for recovery at expiry, separately from promptness.

**Decision / OSA:** a Principal decision is needed on terminal ownership,
ordering and interval meaning (`ΔS`, and `ΔA` if the boundary's admitted
rights change). No additional object or runtime selection is required by
this finding. Until this obligation is written, choice 4 is not ready
for approval.

## 3. BIND → Apply commits → death before Evidence completion

**Clauses:** PD-010 §2 binding steps 3, 5 and 7; Constitution §III.8
Continuation (“an applied one is never re-done”).

| Event | Lawful conclusion |
| --- | --- |
| BIND at E=101 | One exact reservation-to-Transition binding exists |
| Apply at N=11 durably cites E=101 | The registration is applied; step 3 says the binding is consumed by derivation |
| Process dies without another Evidence record | Consumption still follows from the committed Apply. No additional completion record is specified or needed to create that fact |
| Fresh process reads the exact Transition and its Apply | Reconstruct the binding as consumed, do not re-Apply, and do not release it as an unused binding, even if its interval has since elapsed |

**Positive result:** this recovery path has an authoritative carrier.
Do not add a completion record merely to duplicate the Applied History's
answer. If an acknowledgement is ever used operationally, its absence
cannot overrule the Apply record.

**Remaining problem, consolidated into R2-2:** the blanket stale-binding
release instruction in step 6 must be subordinate to the consumed-state
test. If recovery cannot reach the authoritative Transition/Apply state,
it cannot establish that the binding is unused and must not release it.
If recovery reads “not applied” and an Apply commits immediately after
that read, a subsequent RELEASE still needs the terminal exclusion
described in case 2. Negative observation of the current head is not
proof that no in-progress Apply can commit later.

The text's “no live BIND” predicate also needs the terminal distinction:
consumed does not mean available for rebinding the same applied
Transition. The existing never-redo rule forbids a second Apply; make
that terminal standing part of the BIND/RELEASE validation rather than
claiming duplicate safety solely from “no live binding.” Releasing any
otherwise unused allowance after legitimate work is a separate ordinary
reservation operation, not erasure of this binding's consumption.

The required invariant is compact:

```text
For each exact binding E_b:
  successful Apply and release-as-unused are mutually exclusive;
  release-as-unused excludes every later Apply using E_b;
  successful Apply remains consumed across restart and interval expiry.
```

This uses the existing exact binding reference. It does not require a
new generation identity.

## 4. “Settlements always admit” retains validation and single consumption

**Clauses:** PD-010 §2 Admission predicates, settlement bullet;
Constitution §III.5 Settlement; PD-008 §3 rules 2–3 and funding-stop
clarifications.

The defensible reading is **a valid, attributable settlement of a
currently PENDING attempt is not refused merely because its funding
permission has ended or its actual cost exceeds the budget**. Existing
requirements still name the grantee or Principal and require provenance;
`UNKNOWN` settles at the admitted maximum. Revision 2 does not expressly
repeal those requirements. It should not use “always” to override them.

| Settlement case | Required result |
| --- | --- |
| Valid actual after reservation close, expiry, fence or Authorization revocation | Admit by the permitted former grantee or Principal; replace the pending maximum with the actual exactly once |
| Valid actual exceeds maximum, headroom, grant or cap | Admit and count in full; flag overrun/overspend as applicable. These are admission gates for new consumption, not reasons to hide an incurred charge |
| Two concurrent settlements for the same pending attempt | The Evidence boundary atomically checks current pending standing and appends the first valid settlement; the second cannot change S or P again |
| Retry after the settlement response was lost | Resolve to the prior settlement or preserve a duplicate refusal; never append a second accounting effect |
| Unknown attempt, wrong reservation/Authorization binding, or unrelated caller | Refuse and preserve the refusal; do not change the liability |
| Malformed units/amount, negative or non-finite consumption, missing required provenance, or invalid `UNKNOWN` amount | Refuse; the pending liability remains at its maximum. A later valid attributable settlement remains possible |

**Finding R2-3 — Medium, clarification before propagation:** “existing
PENDING attempt” must mean current derived standing at the serialized
settlement commit, not merely that an immutable PENDING pre-record once
existed. Otherwise retries could subtract the same liability twice or
count duplicate actuals. Attribution uses the original grant binding;
revocation does not transform the settlement exception into a right for
any caller to write any amount.

**Smallest replacement:**

> A valid settlement by a permitted caller for an exact attempt still
> PENDING at this Evidence commit is admitted notwithstanding close,
> expiry, fence, revocation or budget/cap exhaustion. Identity,
> attribution, units, amount and provenance remain validated. The
> pending-to-settled effect occurs once; duplicates and invalid
> submissions are refused without releasing or recounting the liability.

This spells out the existing ordinary-boundary obligations. If a later
invoice conflicts with an already-final settlement, it is not a second
settlement of a PENDING attempt; this review does not invent an accounting
correction lifecycle to handle it.

**Decision / OSA:** this clarification grants no new caller rights or
settlement lifecycle and needs no new object. It is intended to preserve
the admitted meaning (`0/0/0`), not introduce a policy choice. The
Principal should retain it when admitting and propagating PD-010; any
proposal to permit duplicate effects or waive attribution would instead
require an explicit semantic/authority decision.

## 5. Choices that survive the requested review

These are recommendations on the named choices, not approval of every
clause in the 14-item decision brief or a fresh whole-design grade.

| Decision-brief choice | Result for the reviewed failure cases |
| --- | --- |
| 3 — Headroom/cap predicates and underrun disposition | **Recommend approval**, with R2-3 and the pre-existing caller, identity, expiry and Authorization checks retained. The new predicates supplement those checks; they do not replace them |
| 4 — BIND/RELEASE and binding interval | **Hold.** Explicitly decide pre-fence-binding survival (R2-1) and close terminal Apply/release ordering (R2-2). Do not approve the claim that the old at-Apply condition is preserved exactly |
| 5 — Per-source grace, observation cutoff, one canonical Outcome | **Recommend approval for the missing/late-observation cases.** The deciding time is the member's witnessed receipt relative to its pinned cutoff, not the resolver's execution time. Canonical commitment still requires a valid deterministic result and duplicate refusal |
| 7 — Fill-time reducing bound and sequential reversal legs | **Recommend approval for the reversal failure.** Only effective confirmed reduction establishes zero before deriving the beyond-zero leg; provisional fills cannot establish a reduction or a new opening entitlement. Existing conservative provisional-fill rules remain in force |
| 8 — Remove `FLATTEN_ON_QUOTA` | **Recommend approval.** Quota refuses opening; calendar expiry supplies the flatten obligation. This is an explicit policy narrowing, not a claim that the old branch worked |
| 9 — Principal-only REDUCE, no promotion, residual-breach check | **Recommend approval for withdrawal of exposure.** It separates withdrawal from qualification, preserves or lowers standing, and allows only residual rather than new/worsened limit risk. Apply changes the target; the Execution function still owes the residual reduction |

Accounting replay: grant 100, reservations 50 and 50, first actual 60.
Committed total is 60, headroom 40, reserved total 110 and spendable zero.
A new maximum-50 attempt under the second reservation fails despite its
local allowance; maximum 40 passes. If that settles at 45, committed total
becomes 105 and further consumption is refused, while valid settlements
continue. Pending liabilities of closed reservations also remain in the
lineage cap. These formulas close the audited arithmetic failures without
claiming to prevent uncapped vendor overruns.

Cutoff replay: a member due by day 12 and observed on day 11 resolves
the same way when computed on day 20. A value first witnessed on day 13
does not qualify even if no Outcome was previously committed. A failed
resolver creates no permission to change the cutoff or use the late
value. This addresses the reported scheduling dependence.

Reduction replay: +40 first reduces effectively to zero; only then may
the −30 opening leg be derived, with the opening and expiry conditions
still required. A process restarting after T cannot derive that opening
leg. REDUCE from a qualified amount 10 to 6 needs no new qualification
floor, cannot promote an exploratory allocation, and records any
permitted residual breach separately from execution still owed. These
are adequate repairs for the cited reduction failures, subject to their
faithful propagation and later implementation conformance.

## Final disposition

The accounting, cutoff and reduction choices above survive this focused
review. **The binding protocol does not yet close B-4.** It makes the
funding decision at BIND and intentionally preserves it across a later
funding fence, but its release-on-timeout path can race an old Apply.
Consumption after a committed Apply is reconstructable without another
Evidence record; release must respect that fact and must exclude every
still-possible competing Apply.

Request only the narrow policy and terminal-ordering correction plus the
settlement clarification, then replay these same three cases. No broader
design expansion is recommended. Nothing here establishes runtime
conformance, executes genesis or demonstrates investment efficacy.
