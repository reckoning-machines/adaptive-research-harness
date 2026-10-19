# Principal Decision Record 008 — Research Budget Reservation and Settlement (D-12)

Status: **ADMITTED 2026-10-19 by the Principal (document-phase admission): revision 4, as written, with the declared Constitutional Delta including the narrow `ΔA`.** Applied to the Constitution as revision 8 and re-audited in [osa_reaudit_pd008_20261019.md](../audits/osa_reaudit_pd008_20261019.md). Admission text, as approved:

```text
ADMITTED 2026-10-19 by the Principal (document-phase admission):
PD-008 revision 4, Research Budget Reservation and Settlement, with
Alternative A (the FENCE) and the declared Constitutional Delta,
including the narrow ΔA for a Principal-only funding stop without
prior independent Check.

Clarifications on admission:
(a) The ΔA is an explicit exception for stopping further funding under
    a Research Authorization. It does not bypass the Evidence
    boundary's identity, authorization, validation, serialization or
    accounting requirements: a FENCE is admitted by that boundary like
    every other record, under the Principal's authority, at its own
    sequence, and is accounted for in the five budget states.
(b) The exception cannot grant, widen or resume funding. Existing
    admitted attempts remain accountable and may complete. Any later
    funding requires the ordinary governed authorization process (a
    successor Authorization granted by Transition); nothing can reverse
    or erase a fence.
(c) This is a document-phase admission, not a claim that a
    Constitutional Transition executed before genesis.

Constitutional Delta admitted:
ΔO: +2 Research Record kinds: RESERVATION (grantee, under its Research
    Authorization); FENCE (Principal only).
ΔS: as PD-008 §5: Research Record content for reservations, attempts
    (dispatch-indexed identity, estimated maximum, PENDING/SETTLED),
    settlements with provenance and UNKNOWN, overrun, CLOSED; the
    Evidence commit boundary's rules 1 to 8; the five budget states,
    DERIVED; funding stopped versus revoked; a fence required before
    any revocation or supersession Transition, verified at Check;
    "active, fenced"; Authorization content (units, estimation rule,
    per-grantee cap, guarantee tiers, default expiry); no inherited
    reservation; budgeted proposals name their reservation.
ΔA: +1: the Principal may stop funding under a Research Authorization
    by committing a FENCE, with no Check and no Apply, effective at its
    Evidence sequence and before any Transition; FENCE committable only
    under the Principal's authority. The right stops funding only; it
    is irreversible and attributable; the revocation Transition keeps
    its Check. No agent, Checker or policy gains any right.

Closed by this admission: D-12.
Open items preserved with owners: P8-R1 to P8-R3 (PD-008 audit);
D-10, D-11 (PD-007 proposed); D-17, N-1; U-8 and the paper fill
methodology; every item of the earlier re-audits.
```

Prior content follows.

Date: 2026-10-19 (revisions 1 to 3: same day)

Subject: D-12, concurrent research budgets. Supersedes PD-007.3's
"reservation by derivation", which the Principal rejected: a derived
view of pending proposals is not an atomic reservation, and a Research
Record written after execution cannot prevent money already spent.

Sources: Constitution revision 7 §III.5 (Research Record; the Evidence
clock), §III.6 ("research resource consumption is owned by Research
Records on the Evidence ledger, recorded as the work is done"; capital
consumed at admission), §III.7 (budget ownership: the Authorization
owns the grant, an immutable ceiling; remaining budget `DERIVED`), I-8,
I-13, Part IX principle 4 and 5; PD-002 (witness reads at the Evidence
boundary); the Principal's brief of 2026-10-19; focused audit
[osa_audit_pd008_proposed_20261019.md](../audits/osa_audit_pd008_proposed_20261019.md).

## 1. The requirement

**Research resources must be authorized and reserved before
consequential consumption begins.** Ten agents under one ceiling must
be unable to spend the same unit twice, and no agent may hold any
authority over the ceiling. Resource budgets are not the Constitutional
budget: the grant's size, its units and its estimation rules are
Authorization content set by the Principal; what this record makes
constitutional is the contract by which a grant is reserved, consumed,
settled and released.

## 2. Why existing ownership is insufficient

| Candidate carrier | Why it cannot reserve |
| --- | --- |
| The Authorization | Owns the grant, an immutable ceiling (§III.7). It cannot carry a per-agent, per-experiment claim without being amended by the Principal for every experiment |
| Research Records as drafted | Record consumption after the work (§III.6). They cannot prevent a spend that has already happened, and ten of them can each be lawful alone while their sum exceeds the grant unless something before them held the amount |
| A proposed Transition's declared budget (PD-007.3, derivation) | A proposal is not an entitlement; two proposals checked against the same remainder both pass; nothing at Check holds anything; a derived view is read, not committed, and so is not atomic |
| The Applied History | Owns capital and allocation consumption at Apply (PD-001 direction), deliberately not research consumption, which accrues during execution; routing every reservation through a consequential Transition would put a Checker and a decider in front of every experiment |

What is missing is **an exclusive commit before consumption** on the
ledger that owns research consumption. That is a new kind of Research
Record, declared below as `ΔO` +1.

## 3. The contract

### Facts and owners

| Fact | Carrier and owner | Commit boundary | Class elsewhere |
| --- | --- | --- | --- |
| Grant: amount in **units**; optional per-grantee cap; the unit definition and the **estimation rule** (units per metered quantity of each permitted provider or tool); whether unboundable calls are permitted and with what margin; default reservation expiry | Authorization content (Transition ledger; Principal) | Authorization Transition | Projection `DERIVED` |
| **Reservation**: Authorization; grantee; amount; purpose (an active Theme, a `SearchFamily` in the empirical or discovery scope, or a named pending registration); expiry instant on the Evidence clock; sequence | Research Record of kind **`RESERVATION`** (Evidence ledger) | Evidence commit, by the grantee under its Research Authorization | The agent's plan: `EPHEMERAL` |
| **Attempt**: a Research Record with a reservation reference, a deterministic attempt identity (reservation, step index, input hash), an estimated maximum in units, standing `PENDING`; committed **before** the consequential call or run | Research Record content (existing kind) | Evidence commit, same Authorization | None |
| **Settlement**: the attempt's actual units (or `UNKNOWN`, settling at the estimated maximum), the result, and standing `SETTLED`; or the reservation's **close**, releasing the remainder | Research Record content | Evidence commit | None |
| **Funding stop**: funding under a named Authorization stops at Evidence sequence `F` | Research Record of kind **`FENCE`** (Evidence ledger), naming the `AuthorizationId`; committable only under the Principal's authority; never removed | Evidence commit, by the Principal | Projection "active, fenced" `DERIVED` |
| Authorization standing: active, revoked, superseded | Applied History (the revocation or successor-Authorization Transition) | Apply | Projection `DERIVED` |
| Reserved, committed, consumed, released, available (§3, definitions) | None | None | `DERIVED` from the Authorization and the records above |
| `OVERSPENT` standing of an Authorization | None | None | `DERIVED`: consumed exceeds the grant |

### Five states, all derived, none counted twice

Every unit of a grant is in exactly one of these states at any Evidence
sequence.

| State | Definition | Counts against the grant? |
| --- | --- | --- |
| **Reserved allowance** | The part of an open reservation's amount not yet attempted: amount minus settled minus attempted-unsettled | Yes, until the reservation closes |
| **Attempted, unsettled** | The estimated maxima of `PENDING` attempts, inside open **or closed** reservations. An outstanding liability: a charge may already exist | Yes, until each attempt is settled |
| **Settled consumption** | Actuals of `SETTLED` attempts, overruns included in full | Yes, permanently |
| **Released allowance** | A closed reservation's amount minus its settled consumption minus its attempted-unsettled maxima; returns to the grant and nowhere else. **Closing a reservation releases only what was never attempted** | No |
| **Remaining spendable budget** | Grant minus reserved allowance of open reservations minus attempted-unsettled maxima minus settled consumption, across every reservation open or closed. A new reservation is admitted only against this | — |

A `PENDING` attempt therefore stays counted at its maximum through
expiry, close and revocation until a settlement replaces the maximum
with an actual. When the actual is below the maximum, the difference
is released at settlement; when above, the excess is an overrun. No
expiry, close or revocation can move an unsettled liability into
another agent's spendable budget.

### Rules at the Evidence commit boundary

The Evidence commit boundary already assigns a total order and reads
the Applied History head at commit (PD-002); it owns the clock. It now
reads the Authorization's grant at the head and enforces:

1. **Exclusive reservation.** A `RESERVATION` is admitted only if, at
   its sequence, **no `FENCE` for the Authorization has a lower
   sequence**, available ≥ amount, the per-grantee cap holds, and the
   Authorization is active at the Applied History head the boundary
   reads. Otherwise refused `FENCED`, `BUDGET_EXCEEDED`,
   `CAP_EXCEEDED` or `AUTHORIZATION_INACTIVE`, preserved. Two agents'
   reservations are ordered by sequence; the second sees the first. No
   partial admission.
2. **No consumption without a reservation.** A `PENDING` attempt is
   admitted only if **no `FENCE` for the Authorization has a lower
   sequence**, it names an open reservation of the same grantee with
   remaining allowance ≥ its estimated maximum, and no attempt with the
   same identity exists (`FENCED`, `NO_RESERVATION`,
   `ALLOWANCE_EXCEEDED`, `RESERVATION_EXPIRED`, `DUPLICATE_ATTEMPT`).
   Consumption recorded without an attempt is refused. The fence check
   and the attempt's admission are one act of the same serialized
   boundary that admitted the fence: an attempt is either below the
   fence or refused, with no third possibility.
3. **Settlement is always admitted** for an existing `PENDING` attempt,
   including after expiry or revocation, because it reports a fact and
   grants nothing. It is committed by the grantee under its
   Authorization, or by the Principal under its own, and carries its
   provenance: the provider's record, an invoice recorded as a
   `DOCUMENT` Observation, or `UNKNOWN`. A settlement `UNKNOWN` settles
   at the estimated maximum. An actual above the estimated maximum is
   an **overrun**: settled in full, counted in full, and flagged. **If
   a provider never confirms whether an attempt was charged**, the
   attempt stays `PENDING` at its maximum indefinitely; nothing releases
   it; the lawful resolution is the Principal's settlement `UNKNOWN` at
   the maximum, or at an invoiced actual with the invoice as
   provenance, after which the difference releases or the overrun
   counts.
4. **Expiry by the clock.** At a reservation's expiry instant, read by
   the boundary at any later commit, the reservation is closed: its
   never-attempted allowance is released; every `PENDING` attempt
   remains an outstanding liability at its maximum until settled. No
   process needs to act; a dead agent cannot hold unattempted budget
   past expiry, and cannot make an attempted charge disappear.
5. **Close.** The grantee closes a reservation by a Research Record
   naming it `CLOSED`; remaining allowance is released. Work finished,
   failed, abandoned or cancelled closes the same way; the result is in
   the same record.
6. **Revocation requires a fence.** A Transition that revokes a
   Research Authorization, or supersedes it by a successor Authorization
   with a different grant or scope, is checked for a prior `FENCE`
   naming it (the Checker reads the Evidence ledger) and is refused at
   Apply without one. The Apply records the Authorization's standing;
   funding was already stopped by the fence. Settlements remain
   admissible after both, by the former grantee or the Principal.
8. **The fence.** A `FENCE` naming an Authorization is admitted by the
   Evidence boundary only under the Principal's authority. At its
   sequence it **closes every reservation** under the Authorization:
   never-attempted allowance is released to the grant, which can no
   longer be reserved; `PENDING` attempts remain liabilities at maximum
   until settled; attempts admitted below the fence may dispatch and
   settle; ambiguous external execution is reconciled under §3
   (retries). A reservation committed before the fence cannot authorize
   an attempt committed after it, because the attempt's admission is
   ordered against the fence by rule 2. A fence is never removed
   (I-11); funding under a fenced Authorization resumes only through a
   successor Authorization the Principal grants, with its own grant.
   **A fence without its revocation Transition is an effective funding
   stop**: the Authorization is active in the Applied History and
   fenced on the Evidence ledger, a visible state the Principal
   resolves by Transition when it chooses.
7. **Overspend.** When consumed exceeds the grant (only possible through
   overruns), the Authorization is `OVERSPENT`, derived; the boundary
   refuses every new reservation and attempt under it until the
   Principal acts by Transition. The overrun is a visible fact in the
   lineage's memory and its Agent Design Evaluation.

### Three tiers of guarantee

| Tier | What | Who bounds it | Guarantee |
| --- | --- | --- | --- |
| **Bounded units** | Consumption the system itself meters and can refuse before execution: registrations, candidate submissions, review attention, runs on resources the system allocates at a declared cost per run | The Evidence commit boundary, at the attempt's pre-record | **Hard.** Nothing is attempted past a reservation or reserved past a grant |
| **Capped provider charges** | Calls to a provider that enforces a cap the agent sets at or below the attempt's estimated maximum (a token limit, a spend cap) and that the Authorization's estimation rule names as enforced | The provider's enforcement, external | **Enforceable by the provider**, not by the system; recorded as such on the attempt; an overrun is possible only if the provider fails its own cap |
| **Uncapped provider charges** | Calls whose maximum the provider does not enforce | Nobody | **No ceiling.** What the system supports is **admission against an estimate and full overrun accounting**: the attempt is admitted against its estimated maximum, the actual is settled in full, the excess is an overrun, and the Authorization becomes `OVERSPENT` when the grant is exceeded. A margin is an estimate with headroom and is never described as a ceiling. The Authorization declares per provider whether such calls are permitted |

The Authorization declares the tier of each permitted provider or tool.
Hard metered units and enforceable provider caps support ceilings;
uncapped charges support admission against estimates and full overrun
accounting, and nothing more. The doctrine guarantees that no unit is
reserved or attempted twice, that nothing is attempted without a prior
reservation whose authority was established at the attempt's commit,
that every overrun is settled and counted in full, and that an
`OVERSPENT` Authorization funds nothing further until the Principal
acts. It does not guarantee a vendor invoice, and it does not enforce
revocation at commit time (§3, authority boundary).

### Succession and retry

- A reservation belongs to one Authorization and one grantee. A
  successor Agent Design Version holds no Authorization until the
  Principal grants one (§III.4) and cannot reserve. A predecessor's
  unused allowance is released to the grant; if the Principal grants
  the successor an Authorization on the same grant, it reserves afresh.
  Nothing is inherited.
### Retries and uncertain external effects

When a process dies after dispatching a provider request and before
recording the response, the ledger establishes: that a `PENDING`
attempt exists, with its identity, maximum and reservation; that
authority existed at its pre-record; and nothing else. Whether the
provider received, executed or charged the request is unknown.

- **Every dispatch is its own attempt.** An attempt identity is
  (reservation, step, input hash, dispatch index). A retry is dispatch
  index 1 of the same logical step: it requires its **own `PENDING`
  pre-record with its own estimated maximum**, admitted against the
  reservation's remaining allowance before dispatch. The additional
  potential cost is thereby authorized explicitly; where the allowance
  is insufficient the retry is refused `ALLOWANCE_EXCEEDED` and the
  agent may commit a further reservation for the same purpose. A second
  pre-record of dispatch 0 is refused `DUPLICATE_ATTEMPT`.
- **Reconciliation before retry.** Where the provider supplies a record
  of dispatch 0, the agent obtains it and settles dispatch 0 first.
  Where it does not, dispatch 0 stays `PENDING` at its maximum, dispatch
  1 proceeds under its own pre-record, and both may be charged.
- **Exactly-once is never claimed** unless the provider supplies an
  enforceable idempotency mechanism that the Authorization's estimation
  rule names; then the retry carries the same provider key, and the
  provider's deduplication is external evidence recorded in the
  settlement, not a system guarantee.
- A retry after settlement is a new logical step with its own
  pre-record.

### Funding stop and revocation: two facts, two owners, one ordering

| Fact | Owner | Boundary | Effect |
| --- | --- | --- | --- |
| **Funding under `AU` stops at Evidence sequence `F`** | The Evidence ledger: the `FENCE` record | Evidence commit, by the Principal | Every reservation and attempt is ordered against `F` by the boundary's own sequence. Below `F`: admitted, may dispatch and settle. At or above `F`: refused `FENCED`. Exact, because fence, reservations and attempts share one total order (I-8) |
| **`AU` is revoked or superseded** | The Applied History: the Transition | Apply, after Check | Standing. Requires the fence (rule 6). Enforced against funding only through the fence, never by any ordering of an Apply against an Evidence commit, which the Constitution does not supply |

The Evidence boundary keeps its PD-002 read of the Applied History
head: a reservation or attempt whose read already shows the
Authorization revoked is refused `AUTHORIZATION_INACTIVE` as well. That
read establishes nothing about ordering and is not relied on for it.

Three events, kept apart: the **fence commit** and the **attempt
admission commit**, both at the Evidence boundary, decide precedence
exactly; the **external dispatch** happens after an admitted attempt,
is outside every boundary, and is reconciled under the retry rules
where its effect is uncertain. Nothing in this record claims to order
an external execution against anything.

### Authority analysis

Existing Principal write access does not by itself make this `ΔA`
none, and the record does not claim it. Before this record, the only
way to stop funding under a Research Authorization was a consequential
Transition: proposed, independently checked, decided by the Principal,
applied. After it, the Principal stops funding by an **ordinary Evidence
commit with no Check and no Apply, effective immediately and before any
Transition**. That is a new decision right exercised at an ordinary
boundary, and it is declared as `ΔA` +1 in §5. Its properties: it can
only stop funding, never grant, widen or resume it; it is irreversible;
it is attributable to the Principal by the commit restriction; a
revocation Transition still requires a Check, and that Check now
verifies the fence; and a fence left without its Transition is a
visible, fail-closed state. The commit restriction that only the
Principal may commit a `FENCE` is itself part of the same `ΔA` item, in
the form PD-002 used for its commit restrictions.

### What survives process death

The reservation, every attempt and every settlement are Evidence
records. A fresh process under the same Authorization finds `PENDING`
attempts and settles them from the provider's record where obtainable,
else leaves them `PENDING` until it can, or the Principal settles them
`UNKNOWN`. Until then they count at the maximum; expiry and revocation
do not touch them. No budget fact lives in a process.

## 4. Five cases

Grant `AU-40`: 600 units to ten Agent Design Versions, cap 100 per
lineage, Themes `TH-14`, `TH-15`, empirical scope `SF-9`, default
reservation expiry 7 days. Illustrative. `AD-21.1` is Theme-based
(`TH-14`); `AD-27.1` is empirical (`SF-9`, no Theme).

| Case | Before | Authorized motion | Committed state | Lawful next action |
| --- | --- | --- | --- | --- |
| 1. Ten agents request work against one remaining budget | Consumed 320 under closed reservations; no open reservations; available 280 | Ten `RESERVATION`s of 40 arrive within a second, `AD-21.1`'s for `TH-14`, `AD-27.1`'s for `SF-9` | The boundary admits seven by sequence (280), refuses three `BUDGET_EXCEEDED`, preserved; available 0 | The three may reserve smaller amounts as releases occur, or stop; nobody overspent; the refusals are in lineage memory |
| 2. Two agents reserve the last 10 | Available 10 | `AD-21.1` and `AD-27.1` each commit `RESERVATION` 10 | Sequence 3 101 admitted; 3 102 refused `BUDGET_EXCEEDED`; no partial | `AD-27.1` waits or reserves 0; a Check of any proposal it makes reads available 0 |
| 3. Reserve 10, spend 6, die; expiry during an unsettled call | `AD-21.1` reservation `R-3` 10, expiry +7 d | Attempts A-1 (max 4) and A-2 (max 3) pre-recorded, settled 4 and 2; A-3 pre-recorded max 3 and dispatched; the process dies | Settled 6; attempted-unsettled 3; reserved allowance 1; reservation open | A fresh process settles A-3 from the provider record (say 2): settled 8, 1 released at settlement; `CLOSED` releases the last 1. If no process returns, expiry closes `R-3`: the 1 never attempted is released; **A-3 stays a liability of 3**, counted in `AU-40`'s spendable budget, until the Principal settles it `UNKNOWN` at 3 or at an invoiced actual. No other agent can reserve the 3 |
| 4. Ambiguous retry | `AD-27.1` reservation `R-8` remaining 12; attempt A-7 dispatch 0 `PENDING` max 5; the call was sent, the process died; the provider offers no idempotency key | A fresh process cannot re-record dispatch 0 (`DUPLICATE_ATTEMPT`); it cannot obtain the provider's record; it pre-records **dispatch 1** of A-7 with max 5 against the remaining 7 | Attempted-unsettled 10; remaining allowance 2; both dispatches may be charged, and the ledger says so | Dispatch 1 settles at 5. Dispatch 0 stays `PENDING` at 5 until the provider's statement arrives: settled at 5 (both charged) or 0 (never executed), by the grantee with provenance or by the Principal. Had the remaining allowance been 3, the retry would have been refused `ALLOWANCE_EXCEEDED` and a new reservation needed first. Exactly-once was never claimed |
| 5. Contested revocation | `AU-40` active at head 94; `AD-21.1` reservation `R-11` open; `AD-27.1` reservation `R-8` open with A-9 `PENDING` max 6 | The Principal commits `FENCE(AU-40)` at `E = 3 150`. `AD-21.1`'s attempt A-2 is presented at `E = 3 149`; its attempt A-3 at `E = 3 151` with a read that still shows head 94; `AD-27.1`'s reservation `R-12` at `E = 3 153` | A-2 admitted, below the fence; A-3 refused `FENCED` regardless of its read; `R-12` refused `FENCED`; `R-11` and `R-8` closed at 3 150, unattempted allowance released, A-9 a liability at 6. `TR-630` revoking `AU-40`: Check verifies the fence at 3 150; applied at `R = 95` | A-2 dispatches and settles. A-9 settles later with provenance, by the former grantee or the Principal. Nothing under `AU-40` is reserved or attempted again; the Principal may grant `AU-45` with its own grant; neither lineage inherits anything |
| 6. Fence without its Transition | As case 5 before the fence | The Principal commits `FENCE(AU-40)` at `E = 3 150` and dies, or decides to wait, before proposing `TR-630` | `AU-40` active in the Applied History, fenced on the Evidence ledger: every reservation and attempt refused `FENCED`; liabilities held; settlements admitted. The projection shows "active, fenced" | Funding stays stopped indefinitely with no further act. The Principal proposes `TR-630` when it chooses; the Check finds the fence; Apply records the standing. No agent can reopen funding; only a successor Authorization can |
| 7. Death before attempt commit | `R-11` open; `AD-21.1` has read head 94 (ephemerally) and prepared A-5 | The process dies before presenting A-5 | Nothing on any ledger; nothing dispatched | A fresh process presents A-5; the boundary orders it against any fence at its own sequence and takes its own read; admitted below a fence, refused `FENCED` at or above. Nothing from the dead process survives |

Failures shown: refusal at the ceiling (1, 2), process death and expiry
with a liability outstanding (3), a retry whose first dispatch may have
been charged (4), funding stopped during live work (5), a fence left
without its Transition (6), death before commit (7). Recovery in every
case is a ledger read: no process holds a budget fact, no permission
exists outside a commit, and no liability is released by any event but
a settlement.

## 5. Constitutional Delta

```text
ΔO: +2 Research Record kinds on the Evidence ledger:
    RESERVATION (committed by the grantee under its Research
    Authorization): the exclusive claim before consumption, §2.
    FENCE (committed only under the Principal's authority): the
    effective funding stop, ordered against every reservation and
    attempt by the Evidence boundary's own sequence. Justification: the
    one fact that orders funding against revocation must live on the
    ledger that orders attempts; the Applied History cannot be ordered
    against Evidence commits and no existing record carries it.
ΔS: §III.5 Research Record: reservation reference, attempt identity
    with dispatch index, estimated maximum, standing PENDING or
    SETTLED, settlement actuals and provenance, overrun, CLOSED; the
    Evidence commit boundary's rules 1 to 8, including FENCED refusals
    and the closing of reservations at a fence; the five budget states.
    §III.6 and §III.7: reserved, attempted-unsettled, settled,
    released, spendable and OVERSPENT defined and DERIVED; the grant
    stays the Authorization's immutable ceiling; "funding stopped" and
    "revoked" distinguished, with a fence required before any Transition
    revoking or superseding a Research Authorization and verified at
    Check; the projection state "active, fenced". §III.7 Authorization
    content: units, estimation rule, per-grantee cap, the three tiers
    of guarantee, default reservation expiry. §III.4: a successor
    inherits no reservation. Part V: budgeted proposals name the
    reservation that covers their declared budget; the Check of a
    revocation or supersession verifies the fence. Part VII: the
    derived budget quantities and "active, fenced" classed.
    Withdrawn from revision 3: outstanding read permission, the
    read-to-commit interval, instants beyond PD-002's existing witness
    stamp, the straddler view, the Apply witness read of the Evidence
    head.
ΔA: +1 Principal decision right at an ordinary commit boundary:
    stopping funding under a Research Authorization by committing a
    FENCE, with no Check and no Apply, effective at its Evidence
    sequence and before any Transition; together with the commit
    restriction that FENCE is committable only under the Principal's
    authority. The right can only stop funding, never grant, widen or
    resume it; it is irreversible and attributable; the revocation
    Transition keeps its Check. No agent, Checker or policy gains any
    right. The grantee reserves and attempts only within a grant the
    Principal made; refusals at the boundary are the existing
    invariant; the Evidence boundary's read of the Applied History head
    is the I-13 read PD-002 established.
```

Resource budgets remain outside the Constitution: every number in §4 is
illustrative, and the grant, cap, units, estimation rule, tiers and
expiry are Authorization content.

## 6. Consistency with PD-007 (unchanged)

PD-007 revision 2's policy `P-1` condition (b) requires a `RESERVATION`
"open at Apply". Under this revision a fence closes every reservation
under the Authorization at its sequence, so a fenced reservation is not
open and `P-1` admits nothing under a fenced Authorization, whether or
not its revocation Transition has applied. The Check record's budget
line cites the reservation by sequence; a fence below it is a `NOT MET`.
PD-007 needs no change.

## 7. Decisions for the Principal

| Question | Proposal |
| --- | --- |
| Admit `RESERVATION` as a Research Record kind | Yes |
| Admit `FENCE` as a Research Record kind, committable only by the Principal, as the effective funding stop ordered by the Evidence boundary's sequence | Yes |
| Admit the `ΔA`: the Principal's funding stop at an ordinary commit without Check or Apply, effective before any Transition | Yes; it is what makes the ordering exact, and it can only stop funding |
| A revocation or supersession Transition requires a prior fence, verified at Check | Yes |
| A fence without its Transition remains an effective funding stop indefinitely | Yes |
| Require a `PENDING` attempt before every consequential call or metered run; every dispatch, including a retry, has its own pre-record; exactly-once never claimed without a provider mechanism named in the Authorization | Yes |
| An unconfirmed attempt stays a liability at maximum until settled, by the grantee with provenance or by the Principal `UNKNOWN`; expiry, fence and revocation release only never-attempted allowance | Yes |
| `OVERSPENT` refuses further reservations and attempts until the Principal acts | Yes |
| Guarantee tiers: ceilings for metered units and provider-enforced caps; admission against estimates and full overrun accounting for uncapped charges | Yes, as Authorization content per provider |

## 8. Remaining admission issue

One: the `ΔA`. Every other element of this record is `ΔO` or `ΔS`
under existing authority. The Principal is asked to decide whether a
funding stop may be exercised at an ordinary commit without the
independent Check that every consequential change otherwise requires.
The record's position is that it may, because the act is fail-closed,
irreversible, attributable and reserved to the Principal, and because
no mechanism among the existing boundaries gives exact ordering
otherwise. If the Principal declines, Alternative B of the comparison
is the fallback, with its stated exposure.

## Amended by PD-010 (admitted 2026-10-19; Constitution revision 11)

This record is historical and is not rewritten. The following of its content is superseded or supplemented by [PD-010](principal_decision_010_codex_audit_repairs.md) as admitted; the Constitution's text governs.

- The five-state formula is replaced by the accounting of Constitution §III.5: committed amount `C = S + P` per reservation, committed total, reserved total, headroom, remaining spendable budget and released allowance, with `OVERSPENT` when the committed total exceeds the grant; every attempt must fit the reservation's allowance, the Authorization's headroom and the lineage cap (audit B-3).
- "Settlement always admitted" is restated with validation: a valid, attributable settlement of an attempt still `PENDING` at the commit admits after close, expiry, fence, revocation or exhaustion; duplicates are refused `ALREADY_SETTLED`; malformed submissions `INVALID_SETTLEMENT` (Codex R2-3).
- Rule 4's promise that expiry releases unused allowance at the next read is superseded while a reservation is frozen by an Apply binding (PD-010 choice 4a): unused allowance can remain frozen past expiry until consumption, or invalidation followed by `RELEASE`, with no release promised during an outage.
- `RESERVATION`, attempt and settlement records may be committed under a Checker Authorization for verification purposes (audit B-1); the Principal's funding-stop exception extends to Checker Authorizations (`ΔA`).
