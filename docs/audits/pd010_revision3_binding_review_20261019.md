# Independent review of PD-010 revision 3 — terminal binding and reservation continuation

Status: **AUDIT — EVIDENCE, NOT DOCTRINE. Choices 4a–4d are ready
subject to corrections R3-1 and R3-2 below; revision 3 is not ready for
approval as written. No admission or implementation authority.**

Date: 2026-10-19. Reviewer: Codex, independently reviewing Claude's
proposal at the Principal's request.

## Reviewed subject and limits

Exact subject: [PD-010, revision 3](../decisions/principal_decision_010_codex_audit_repairs.md),
dated 2026-10-19, marked **PROPOSED FOR ADMISSION**, 655 lines. SHA-256
of the complete reviewed file:

```text
54cb6c14d87ab00d5c2c126d04c56b6573a4facc0ff9f5c022169b70080a0942
```

Branch `main`; HEAD `895f953aca14e440c1593db8f0f7088da0556cb2`.
The proposal is uncommitted. Line references below identify these exact
bytes, not a future revision at the same path.

Read `AGENTS.md`, the proposal, the
[revision 2 review](pd010_revision2_binding_review_20261019.md), and the
relevant governing clauses: Constitution revision 10 §III.5 (clock,
reservation, attempts and settlement), §III.7 (budget ownership and
authority), §III.8 (lifecycle and continuation), I-12/I-13, Part V
(`P-1`) and Part VII; PD-008 §3 and its admitted delta; PD-009 §3a,
§7 and its admission. For authority classification, also consulted the
adoption record's engineering operating contract and Constitutional
Coherence doctrine at fin123-core commit
`8175d504998bf682170847119a866d7f5e7df8fd`.

This review covers §2's binding and settlement contracts, their §6
interactions and §7 decision rows. It independently orders the events
and applies the predicates below; the proposal's own replay outcomes
are claims under review, not proof. Existing modifications to
`AGENTS.md` and the document-first plan, both prior audits and PD-010
are preserved. Only this audit is added.

**Disposition.** Rules 4–7 close revision 2's delayed-Apply/release
race at the stated document-contract level. The settlement predicate
closes R2-3. Two corrections remain: the Evidence-side definition of a
live binding contradicts successful consumption, and the authority
delta omits the boundary's new terminal-invalidation right while
claiming existing ledger ownership supplies it. Neither requires a
new object, completion acknowledgement or infrastructure choice.

## Terminal exclusivity and safe release

For one exact binding `E_b`, rule 6 serializes Apply and invalidation
on the same Transition boundary. If Apply commits first, rule 5 refuses
invalidation because the Transition is already applied. If invalidation
commits first, rule 4 refuses every subsequent Apply citing `E_b`.
Those checks belong to the committing boundary, so a process paused
after an earlier witness cannot evade them. A fresh binding has a
different `E_b` and does not erase the old invalidation.

This establishes **at most one terminal disposition, and exactly one
once either terminal operation succeeds**. It does not establish that
every binding eventually receives a disposition. Rule 9 explicitly
allows an unresolved binding to remain frozen without a running
process. The sentence “Exactly one terminal disposition exists per
binding” (lines 231–234) should describe that exclusivity contract,
not assert completion at BIND or promise eventual recovery.

Rule 7 requires a positive durable invalidation of the exact binding,
read by Evidence at the release commit. A negative observation of
Apply, a timeout, a lost response or an earlier clock witness is
insufficient. After that positive invalidation, no concurrent or
delayed Apply of that binding can become legal. Duplicate recovery
requests produce one invalidation and one RELEASE; the others refuse.
An unreachable Transition ledger refuses RELEASE
`LEDGER_UNREACHABLE`. Rule 10 also stops recovery when Evidence is
unreachable. No fallback to a remembered disposition is permitted.

There is an express **fence exception to the literal proposition that
unused allowance can be released only after invalidation**. Rule 3 and
PD-008 close R and release its never-attempted allowance at FENCE while
Apply may still succeed. This is safe for the stated policy because
the grant is irreversibly fenced: neither that allowance nor settlement
underruns can finance another attempt or reservation under it. A
successor grant is separately authorized. Thus the defensible invariant
is: release of the binding for reuse requires invalidation; a fence
may close the reservation without invalidating registration eligibility,
but creates no reusable spending permission. Do not describe the
fence's accounting release as `RELEASE(E_b, n_i)`.

## R3-1 — High: successful consumption has contradictory freeze semantics

**Exact clauses.** §2 “Records and identity,” lines 231–234; rule 1,
lines 243–244; rule 2, lines 248–254; rule 4, lines 275–276; rule 6,
lines 294–295; rule 7, lines 305–309; rules 9–10, lines 326–338;
the allowance check, lines 363–370; §6 freeze interaction, line 593.
Governing comparators: Constitution §III.5 ordinary closure and
attempt rules; PD-008 §3 Evidence rules 2–5 and 8; PD-009 §7.5.

The proposal says that a binding remains live on Evidence until
RELEASE. A consumed binding can never receive RELEASE. It also says
that frozen allowance is freed by RELEASE “and by nothing else.” Yet
rule 4 says Apply unfreezes R, rule 9 ends the freeze on consumption,
and the allowance check and §6 say Apply is an alternative to RELEASE.
There is no declared distinction between an unreleased historical BIND
and a binding that still freezes R. Keeping the same immutable Evidence
record is correct; making its unreleased presence the continuing live
predicate is not.

**Smallest counterexample.** R has amount 10, no attempts, no fence,
an active grant and expiry at time 20. BIND at time 0; Apply succeeds
at time 1; the process dies before any further Evidence write. At
time 2 the original grantee requests a maximum-1 attempt for the
registered subject. Rule 4 permits ordinary admission, but the
Evidence definition still finds a live binding, and rule 2 refuses
`RESERVATION_BOUND`. A grantee CLOSED request is similarly allowed by
the intended ordinary lifecycle and forbidden by the continuing freeze.
At time 21, one reading closes R on expiry; the other continues to
suppress expiry reads. Recovery cannot satisfy the latter reading:
invalidation refuses `ALREADY_APPLIED`, RELEASE refuses
`NO_INVALIDATION`, and rule 10 says nothing further is required.
Unused allowance can therefore be stranded under a literal reading.

This is a contradiction, not evidence that Apply needs an Evidence
completion record. Apply already supplies the sole durable consumption
fact. Nor may a reviewer silently choose the favorable sentence over
the conflicting definition.

**Minimum repair.** Define reservation freeze standing from both
existing ledgers, with these exhaustive cases:

| Binding facts | Freeze and ordinary lifecycle |
| --- | --- |
| BIND exists; no terminal disposition | R remains frozen; no new attempt or grantee close; the proposed expiry deferral applies |
| Invalidation exists; no RELEASE | R remains frozen pending authorized RELEASE; Apply of this binding is permanently forbidden |
| Apply cites this BIND | Consumption is terminal and the freeze ends from that Apply alone; no RELEASE or completion record is required or permitted |
| Invalidation and RELEASE exist | The freeze ends; R returns to ordinary closure, expiry and attempt rules |

A fence closes R in every case and never loses its effect. Define
“live” consistently with these cases, or use it only for a separately
defined unreleased record and stop using it to decide the freeze. Remove
the rule 7 “and by nothing else” conflict. Preserve the prohibition on
rebinding/reapplying an already-applied Transition.

For the next attempt, close or budget/expiry computation, the Evidence
boundary must derive consumption and purpose from the exact committed
Apply, using an authoritative read under I-13. If that fact cannot be
established, refuse the dependent operation; an acknowledgement, cache
or process memory has no deciding role. A stale pre-Apply read may
conservatively leave the operation frozen; it cannot authorize spending.
Once Apply is read, ordinary lifecycle checks apply without a second
completion step. The read does not acquire a new decision right.

Make “unfreezes for the subject's attempts” conditional on those ordinary
checks. Apply changes purpose and removes the binding freeze; it grants
no new caller, amount, expiry or Authorization. The original grantee
retains its reservation; a registered successor does not inherit it.
At a read after expiry, close before admitting a new attempt. A fence
still refuses `FENCED`; grant/cap exhaustion still refuses new attempts.
Ordinary CLOSED or expiry releases only unused allowance; PENDING
maxima remain liabilities. This is the narrow correction needed for
choices 4a and 4d's reservation lifecycle, already intended by rule 4.

## R3-2 — High: terminal invalidation's authority is not fully declared

**Exact clauses.** §2 rules 4–5, lines 266–290; “Who commits what,”
lines 342–347, especially “Its own ledger; no new right”; Group 2 delta,
lines 407–423; §7 choices 4b and 4d, lines 616 and 618. Comparators:
Constitution §III.7 authority, §III.8 lifecycle and Part V `P-1`;
PD-008 §3 “Authority analysis”; the adopted Authority Normal Form and
mandatory Authority Delta.

**Smallest counterexample to the zero-authority claim.** A decided
Transition has a binding and its Apply fails a current condition. The
pre-existing boundary may refuse that Apply. Revision 3 additionally
lets it commit a durable event that permanently prevents every later
Apply of this exact binding and enables Evidence to unfreeze its
reservation. That terminal consequence is a new governed fact and
decision right, even when its predicate is completely mechanical.
Owning the Transition ledger does not itself authorize it. The elapsed
interval request right likewise does not, by itself, declare who may
adjudicate and commit the terminal result.

**Minimum repair.** Explicitly include in the proposed Authority Delta
the Transition boundary's exclusive right and duty to establish
terminal invalidation under **both** grounds: atomically with its own
Apply-side refusal, or on a verified elapsed-interval request from an
attributable process acting for the Apply boundary under D-17. It has
no power to cancel for any other reason. Retain the separate narrow
Evidence caller extension for BIND/RELEASE. Reconcile the authority
table and choices 4b/4d with that declaration. The count may remain two
if the second item explicitly bundles terminal adjudication with its
request right; the complete rights, not an arbitrary count, matter.

State the durable evidence of each ground: the exact failed condition
and cited authority with the atomic refusal, or the requesting role,
verified clock pair `(t, E)`, exact BIND and applicable Authorization
interval on the invalidation event. The latter must preserve the
otherwise ephemeral clock answer for historical attribution. A caller
asserting “elapsed” or a locally measured timeout is insufficient.
“Any process” in replay rows 4 and 6 must mean a process acting within
the declared boundary role, not a new public write permission.

Complete the representation declaration: BIND and RELEASE are
`AUTHORITATIVE` for their exact Evidence-side acts; Apply and
invalidation are `AUTHORITATIVE` for terminal disposition; consumed,
frozen and remaining-budget views are `DERIVED`; a recorded clock
answer is `RECEIPT` for the clock's answer. These are classifications
of existing proposed carriers, not additional objects or writers.

The declared `ΔO +1` BINDING kind is otherwise adequate; invalidation
is an appended lifecycle event on an existing Transition, not a new
independently identified object. The declared `ΔS` names the terminal
event, freeze, interval, recovery and changed funding eligibility, but
must incorporate R3-1's consistent successful-consumption rule and
explicitly supersede PD-008's automatic expiry release for the frozen
interval. Settlement retains the existing callers and single pending
liability lifecycle; its clarification remains `0/0/0`.

## Policy choices, distinct from the contradictions

**Eligibility versus spending.** Choice 4a is now an express policy
change. BIND establishes registration eligibility at `E_b`; it does
not establish current spending permission at a later Apply. A later
fence closes R immediately under PD-008, while registration may still
apply if the Authorization remains active and all other Apply-side
conditions hold. Revocation at the head, suspension of the applicable
policy or STOP refuses Apply and invokes the proposed invalidation.
Existing `P-1` conditions and D-17 re-check/re-decision requirements
remain; rule 4's short list must not repeal unrelated criteria.

Deferring expiry reads while frozen deliberately changes PD-008 §3
rule 4's promise that a dead agent cannot retain unused allowance past
expiry. It can retain it beyond expiry until consumption or invalidation
followed by RELEASE; no maximum hold is promised. This is a Principal
choice, not an inherent contradiction once explicitly admitted. It
must replace the corresponding D-17 funding clauses, including the
blanket “no bypass” wording, only for registration eligibility. It must
not change new-attempt admission or the original expiry instant.

A post-BIND overrun does not invalidate registration. New spending
still obeys current allowance, grant headroom and lineage cap. An
overrun does not necessarily make the grant OVERSPENT: with grant 100
and reservations 50/50, actual 60 in the first leaves headroom 40;
after consumption/unfreeze, a maximum-40 attempt under the second can
pass, while maximum 50 refuses `GRANT_EXHAUSTED`. If committed total
exceeds 100, new reservations and attempts refuse OVERSPENT as stated.
No binding protects headroom from other liabilities.

The phrases “nothing can be spent” and “the subject may attempt” need
these distinctions when propagated. PD-008 and PD-009 still permit
an already-admitted PENDING attempt to complete/dispatch under its
consumed permission, and to settle after fence or expiry. Binding
consumption is not permission to retry: a retry needs a fresh admitted
attempt. There is no basis here to widen a grant or revive fenced or
expired permission.

**Invalidation and interval.** Both proposed grounds are objective when
enforced as written: a failed Apply-side condition at the serialized
commit, or a verified Evidence-clock read with `t - t_b > interval`.
Exactly at the interval is not “greater than.” Requesting invalidation
after that threshold is a bounded recovery choice; there is no right
to cancel an otherwise eligible binding before it. A proposer or
Checker's preference is not a third ground. This mechanical rule still
requires the authority admission in R3-2.

An earlier `t < threshold` witness cannot defeat a later invalidation.
An old post-threshold witness proves passage at its recorded instant,
not current terminal standing or a release right: the boundary must
still serialize against Apply and verify the exact binding. No process
may substitute a cached clock answer when it cannot obtain the read
required by Constitution §III.5. Unreachable authority gives no positive
ground for inventing a failed policy condition.

Choice 4c correctly makes the interval permission to request
invalidation, not a guaranteed release or strict Apply deadline. An
Apply arriving after it can win the race lawfully. An invalidation can
win even though a competing Apply would otherwise pass. That is the
explicit policy choice; it is not discretionary cancellation outside
the two grounds.

## Independent event replays

Assumptions for these paper traces: `BIND(TR-x,R)` at `E_b=101`,
`t_b=0`, interval 10, a valid decided Transition and otherwise valid
Apply conditions. Evidence sequences and Transition lifecycle sequences
are distinct orders; neither number orders events on the other ledger.
Where R3-1 prevents a unique answer, the table records that failure
instead of adopting the proposal's favorable replay.

| Case | Authoritative deciding record and independent result | Lawful continuation and exact refusal |
| --- | --- | --- |
| 1. BIND → fence → Apply | FENCE at E=102 closes R and stops funding. Apply citing 101 can then commit under the proposed eligibility policy if AU is still active. Apply owns consumption; FENCE still owns closure. | No new attempt/reservation under AU: `FENCED`. Previously admitted liabilities remain accountable. If revocation wins before Apply, the inactive-Authorization condition refuses Apply and atomically invalidates 101 on `APPLY_REFUSED`. No unfencing follows from consumption. |
| 2. Early witness → pause → invalidation → RELEASE → delayed Apply | A's t=9 witness establishes no terminal right. B obtains t=11; the boundary commits invalidation of 101 at n_i=12. Evidence then reads that positive record and admits RELEASE at E=130. | A's delayed Apply of 101 refuses `BINDING_INVALIDATED`, even if it passed every earlier read. Re-check/re-decision as required and a fresh eligible BIND may continue. A negative Apply read without n_i would instead make RELEASE refuse `NO_INVALIDATION`. |
| 3. Apply wins against invalidation | The Apply record citing 101 commits first. Rule 5 then finds TR-x APPLIED, irrespective of the interval witness. | Invalidation refuses `ALREADY_APPLIED`; RELEASE refuses `NO_INVALIDATION`; repeat Apply refuses `ALREADY_APPLIED`. Consumption is reconstructable. Ordinary reservation continuation is R3-1, not established by the absence of a RELEASE. |
| 4. Invalidation wins against Apply | The exact invalidation of 101 commits first at the same serialized boundary. | Every Apply of 101 refuses `BINDING_INVALIDATED`. An authorized recovery process can RELEASE after reading n_i; until then the binding freeze persists, subject to fence closure. Another invalidation while still unapplied refuses `DUPLICATE`; another RELEASE refuses `ALREADY_RELEASED`. |
| 5. Death immediately after Apply | Apply citing 101 survives without a later Evidence write. It is the sole consumption authority; death and interval passage do not change it. | Do not reapply (`ALREADY_APPLIED`), invalidate (`ALREADY_APPLIED`) or RELEASE (`NO_INVALIDATION`). The subsequent attempt/CLOSED/expiry trace below exposes R3-1. The proposal's unconditional “subject may attempt” is not a complete admission result. |
| 6. Death after invalidation, before RELEASE | n_i permanently excludes Apply of 101; loss of the process does not erase it. | Authorized recovery reads n_i and releases once. With Transition unreachable: `LEDGER_UNREACHABLE`, no release; with Evidence unreachable: no Evidence commit. Concurrent recoveries cannot release twice. No running recovery means no promised completion; a fence can still close R. |
| 7. Old invalidated binding, fresh binding, old operation resumes | Invalidation of 101 and RELEASE at 130 permit fresh BIND 131 if R is still eligible. Each terminal decision names its own binding. | Apply(101): `BINDING_INVALIDATED`; repeat RELEASE(101): `ALREADY_RELEASED`; RELEASE(131) without its invalidation: `NO_INVALIDATION`. Apply(131) can win once. Re-invalidating 101 before Apply(131) refuses `DUPLICATE`; after Apply(131), rule 5's already-applied guard can instead return `ALREADY_APPLIED`. Neither affects 131. |
| 8. Settlement after revocation; duplicate and malformed requests | X is PENDING at maximum 10. FENCE and revocation remove no liability. A valid former-grantee settlement at 7 commits at E=140; P falls by 10 and S rises by 7 once. | Retry after lost response or another valid concurrent submission: `ALREADY_SETTLED`, no effect. Negative/non-finite/wrong-unit amount, missing provenance, wrong binding or unrelated caller: `INVALID_SETTLEMENT`, no effect. Invalid submissions while X is still PENDING leave 10 outstanding; invalid submissions after E=140 leave the settled 7, not a resurrected maximum. |

For case 8, predicate failure order can affect which diagnostic is
reported for a submission that is both malformed and already settled;
it cannot affect accounting. Revision 3 supplies the intended named
refusals. `UNKNOWN` must settle at the exact admitted maximum. An
unknown attempt cannot create a liability to release. Valid settlements
continue after close, expiry, revocation, grant exhaustion and cap
exhaustion; an actual above the maximum is recorded in full. A later
conflicting invoice is not a second settlement of a PENDING attempt;
this review creates no correction lifecycle.

### Extended case 5: subsequent use and closure

Start with R=10, no liabilities, expiry 20; BIND at 0, Apply at 1,
then process death. A fresh Evidence consumer reads the Apply at time 2.
Under the minimum correction, consumption removes the freeze without
an Evidence acknowledgement. The original grantee may admit an attempt
of maximum 3 if the current grant, cap, purpose and caller checks pass.
An independently attempted duplicate identity refuses
`DUPLICATE_ATTEMPT`. A later grantee CLOSED record releases 7, retaining
the pending 3. Settlement at actual 2 moves that liability to actual
consumption once, freeing the remaining 1 under the accounting repair.

Alternatively, with no attempt and the first read at time 21, Evidence
closes R for expiry and releases 10; a new attempt refuses
`RESERVATION_EXPIRED`. With a pending maximum 3 it releases only 7.
If a fence preceded the read, closure already follows from FENCE and
a new attempt refuses `FENCED`. If an overrun elsewhere exhausted
headroom, the attempt refuses `GRANT_EXHAUSTED` (or OVERSPENT when
applicable), but ordinary close and valid settlement remain possible.
None of these operations needs or permits binding RELEASE after Apply.

As written, the still-live-until-RELEASE definition can instead keep
refusing `RESERVATION_BOUND` and suppress those closure paths. This
is the failed continuation witness for R3-1. Repairing it resolves
indefinite retention caused by the contract; it does not promise that
reads or recovery occur while every process or authority is unavailable.

## Approval recommendation and retained findings

| Choice | Focused recommendation |
| --- | --- |
| 4a — eligibility at BIND | Ready as an explicit Principal policy choice, subject to R3-1's lifecycle correction. Accepting deferred expiry means accepting the loss of PD-008's automatic release while frozen; it confers no extended spending permission. |
| 4b — terminal invalidation and release | The mutual-exclusion and safe-release mechanism is adequate at document level. Ready subject to R3-2's complete authority and attribution declaration. |
| 4c — interval meaning | Ready for Principal acceptance as stated: permission to request invalidation, no automatic completion and no Apply deadline. |
| 4d — binding and its delta | Ready subject to both named corrections and matching decision-brief/delta text. Existing write access cannot stand in for the terminal right. |

Keep the prior review's recommendations on choices **3, 5, 7, 8 and
9**: accounting/headroom/cap with validation, source-specific cutoff
and canonical Outcome, effective reduction before a reversal's opening
leg, removal of `FLATTEN_ON_QUOTA`, and Principal-only REDUCE without
promotion. The binding correction changes neither their arithmetic nor
their evidence or execution criteria. No concrete interaction defect
found here warrants reopening those recommendations.

This focused review does not close the independent whole-design audit,
approve the other decision-brief choices, amend doctrine, admit PD-010
or ConstitutionVersion 1, execute genesis, or establish CPOC/runtime
conformance or certification. These are paper replays, not executed
witnesses. The next step is the two narrow proposal corrections and
Principal acceptance of the explicitly identified policy and authority
changes; no implementation or commit was performed.
