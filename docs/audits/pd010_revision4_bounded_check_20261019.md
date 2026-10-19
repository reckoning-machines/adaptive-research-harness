# PD-010 revision 4 — bounded independent correction check

Status: **AUDIT — EVIDENCE, NOT DOCTRINE. R3-1 and R3-2 are resolved
in the reviewed proposal. Choices 4a–4d are ready for Principal
approval. No admission, propagation or certification.**

Date: 2026-10-19. Reviewer: Codex, independently checking Claude's
revision at the Principal's request.

## Exact subject and scope

Reviewed [PD-010 revision 4](../decisions/principal_decision_010_codex_audit_repairs.md),
dated 2026-10-19, marked **PROPOSED FOR ADMISSION**, 852 lines.
SHA-256 of the complete reviewed file:

```text
a47dad4069d06bbb469c300ef27361952b82193357edd1244d2edeecd2f723d2
```

HEAD: `895f953aca14e440c1593db8f0f7088da0556cb2`. PD-010 remains an
uncommitted proposal. Line references identify these exact bytes.

Read the current `AGENTS.md`, checked the operative clauses against
[R3-1/R3-2](pd010_revision3_binding_review_20261019.md), and checked
their Group 2 delta, §6 interactions, §7 decision rows and §8
consolidated declaration. Also checked Group 1's actual replacement
clauses and authority declaration for Checker attempts, reservations
and settlements. Constitution revision 10 and PD-008/PD-009 have the
same digests as the governing texts used in the preceding review;
their closure, liability, continuation and authority rules remain the
comparators. The proposal's closure map and replay claims were not
treated as proof.

This is the requested bounded correction check, not another
whole-design audit. **No concrete defect found within this scope.
No further Claude revision is required by this check.**

## R3-1: resolved in the actual lifecycle clauses

The four-case freeze table (§2, lines 248–256) distinguishes unresolved
BIND, invalidated-but-unreleased, consumed, and invalidated-and-released.
The consumed case ends the freeze from Apply alone. Lines 258–264
explicitly deny deciding force to an unreleased BIND's mere presence
and distinguish fence accounting release from binding RELEASE.

These meanings agree with the operative rules:

- Rule 2 (278–289) freezes only a reservation in frozen standing and
  explicitly declares the temporary exception to PD-008 expiry release.
- Rule 4 (305–323) makes Apply end the freeze, changes purpose, and
  preserves the original grantee, expiry, caller and funding checks.
  It transfers no reservation or permission to a registered successor.
- Rules 6–7 (347–363) forbid RELEASE after consumption and permit it
  only following a durable invalidation. The former “by nothing else”
  conflict is gone.
- Rule 8 (364–375) makes Evidence read the exact Apply before a
  dependent attempt, CLOSED, expiry close or budget view. Unreachable
  authority refuses `LEDGER_UNREACHABLE`; a stale pre-Apply read can
  keep an operation frozen but cannot authorize spending.
- Rules 9–11 (376–408) preserve single Apply, binding-specific
  invalidation and recovery from existing records. The allowance
  check, D-17 replacement and §6 freeze row agree (452–481, 705).

Independent continuation replay: R=10, expiry 20, no pending liability;
BIND at time 0, Apply at time 1, immediate process death. The Apply
is the deciding consumption record. At time 2, Evidence reads it and
may admit the original grantee's maximum-3 attempt if all ordinary
checks hold. CLOSED then releases 7 and retains the pending 3;
settlement at actual 2 replaces that maximum once. No Evidence
completion or binding RELEASE is needed. Repeat Apply and invalidation
refuse `ALREADY_APPLIED`; binding RELEASE refuses `NO_INVALIDATION`.

In the alternative with no attempt and the first read at time 21,
ordinary expiry closes R and releases 10; a new attempt refuses
`RESERVATION_EXPIRED`. With pending maximum 3, only 7 is released.
A fence remains decisive for closure and new spending refuses
`FENCED`. Insufficient headroom refuses `GRANT_EXHAUSTED`; an
OVERSPENT grant refuses new spending. Valid settlement remains possible.
The former consumed-but-permanently-frozen path no longer follows from
the text. Outages still carry no promise of progress or release.

## R3-2: resolved in the authority declaration

Rule 5 (324–346) gives the Transition boundary alone the terminal
invalidation act, with exactly two grounds and durable evidence:

| Ground | Required basis and attribution |
| --- | --- |
| `APPLY_REFUSED` | Atomic with its own refusal of the exact Apply; failed condition and cited authority recorded by sequence |
| `INTERVAL_ELAPSED` | Attributable request in the Apply-boundary continuation role; exact BIND, applicable Authorization interval, requesting role and verified Evidence-clock receipt recorded; `t - t_b > interval` |

The authority table (410–418) and Group 2 delta (522–535) expressly
declare the boundary's exclusive right **and duty** under both grounds.
The elapsed-interval request right is bundled into that terminal
authority item; it does not grant the requester adjudication power.
Both declarations reject ledger ownership as the source of the right.
No discretionary cancellation ground appears.

The carrier table (420–428) classifies the acts and terminal records as
AUTHORITATIVE for their exact facts, standing and budget views as
DERIVED, and clock answers as RECEIPT. The new event remains a
lifecycle event on an existing Transition. The Group 2 delta, §7
choices 4b/4d and §8 total agree: local authority items 1/2 correspond
to consolidated items 3/4. No additional authority is inferred from
the read in rule 8.

Independent ordering check: if Apply wins, invalidation refuses
`ALREADY_APPLIED` and RELEASE lacks its required invalidation. If
invalidation wins, every delayed Apply of that exact BIND refuses
`BINDING_INVALIDATED`; Evidence can RELEASE only after reading that
durable record. A second release refuses `ALREADY_RELEASED`. A fresh
BIND cannot erase the old invalidation. Process death, concurrent
recovery and an earlier clock witness change none of those predicates.
Unreachable authority releases nothing. The interval still permits
invalidation rather than guaranteeing release or imposing an Apply
deadline (rule 10); terminal exclusivity now correctly states “at most
one,” with no eventual-completion promise (241–246).

## Checker authority: attempts expressly included

**Confirmed in the actual proposal, not inferred from reservation or
settlement permission.**

| Clause | Confirmation |
| --- | --- |
| §1 replacement table, line 82 | The Part V **RESERVATION and attempt** caller becomes the grantee under its Research **or Checker** Authorization |
| §1 delta, lines 94–96 | Explicitly permits Checker holders to commit “RESERVATION, attempt and settlement records under their own grant” |
| §8 final delta, lines 790–793 | Repeats all three acts in consolidated authority item (1); item (2) separately extends the Principal's funding-stop exception |
| §8 approval block, line 808 | Incorporates those Group 1 items (1) and (2), including attempt authority |

The declaration is consistent with verification purposes and separate
funding in §1. Checker reservations remain outside the Apply binding
protocol (§1 interactions and §6, lines 131–133 and 702–704).
Group 2's currently-PENDING settlement validation adds no further
caller right; the new Checker caller right is declared in Group 1.
This confirms the requested authority coverage without extending this
check into general approval of every Group 1 bootstrap clause.

## Disposition

**R3-1 and R3-2 are resolved at proposal level. Choices 4a–4d are ready
for Principal approval as written in this revision.** Their policy
tradeoffs remain explicit: registration eligibility survives the named
later events; expiry release is deferred while frozen; no maximum
freeze is promised; ordinary spending permission is never extended.
Only the Principal can admit those choices and authority changes.

The earlier recommendations on accounting, cutoff and reduction
(choices 3, 5, 7, 8 and 9) remain unchanged. This check does not close
the whole-design audit or approve all other choices. No governing text
or proposal was modified; prior audits and unrelated work were
preserved. No implementation, executed witness, genesis, certification
or commit occurred. Following Principal admission, propagation and the
final whole-design review remain separate work.
