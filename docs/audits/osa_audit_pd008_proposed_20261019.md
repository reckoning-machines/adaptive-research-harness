# OSA Audit of PD-008 as Proposed (D-12), revision 4

Status: **AUDIT — EVIDENCE, NOT DOCTRINE. Authorizes nothing. Certifies
nothing.**

As-of: 2026-10-19. Subject:
[PD-008, proposed](../decisions/principal_decision_008_research_budget_reservation.md).
Reconciliation standard: Constitution revision 7 (§III.5, §III.6,
§III.7, I-6, I-8, I-11, I-13, Part IX 4 and 5); PD-001's direction that
research consumption is an Evidence fact recorded as work is done;
PD-002's witness reads; ANF and the seven authority invariants; CPOC's
negative invariants. The Principal's tests: an atomic reservation, not
a derived view; nothing spent before it is reserved; hard limits
distinguished from estimated charges; no hidden process-local budget
authority.

## Executive disposition

**B+ — BOUNDED. `ΔO` +2 (`RESERVATION`, `FENCE`), both justified; `ΔA`
+1, declared: the Principal's funding stop at an ordinary commit
without Check or Apply; no contradiction with revision 7; exact
ordering of funding against revocation on one ledger; ceilings claimed
only for metered units and provider-enforced caps; no permission exists
outside a commit. Ready for the Principal's decision, which turns on
the one `ΔA`; PD-007 depends on it and needs no change.**

## 1. Authority check

| Question | Finding |
| --- | --- |
| Who owns a reservation? | The Evidence ledger, as a Research Record kind; committed by the grantee under its Research Authorization at Evidence commit. One owner, one boundary |
| Is the reservation atomic? | YES. The Evidence boundary assigns a total order (I-8) and admits a `RESERVATION` only against available at that sequence; the second of two concurrent reservations sees the first. Nothing is derived from pending proposals |
| Does the grantee gain authority? | NO. It reserves within a grant the Principal made; it cannot widen the grant, the cap or an expiry; refusals at the boundary are the existing invariant |
| Does the Evidence boundary gain a right? | NO. It gains a read of the Authorization's grant at the head, the same kind of I-13 read PD-002 gave it for witness marks |
| Does revocation remain the Principal's? | YES, in two acts: the `FENCE` (Evidence commit, Principal only) stops funding exactly at its sequence; the Transition (Check, Apply) records standing and requires the fence. Nothing an agent does can keep a reservation alive past the fence |
| What is the authoritative funding-stop fact, its owner, its boundary? | "Funding under `AU` stops at Evidence sequence `F`": owned by the Evidence ledger as the `FENCE` record; enforced by the Evidence commit boundary, which orders every reservation and attempt against `F` by its own sequence (I-8). Not the Applied History, which cannot be ordered against Evidence commits |
| Is a new decision right introduced? | YES, and declared: before, funding stopped only by a checked, applied Transition; now the Principal stops it by an ordinary commit with no Check and no Apply, effective before any Transition. Fail-closed, irreversible, attributable, Principal-only. `ΔA` +1 |
| Can an agent, Checker or policy commit a fence or lift one? | NO. Commit restriction to the Principal; a fence is never removed; funding resumes only by a successor Authorization the Principal grants |
| Is any budget fact process-local? | NO. Reservation, attempts and settlements are ledger records; expiry is a clock fact read at commit; a dead agent holds nothing past expiry |
| Is the vendor ceiling claimed? | NO. §3 says the guarantee is on units at commit; unboundable calls are forbidden or margined by Authorization content; overruns are recorded and can only ever be a visible fact |
| Why `ΔO` and not `ΔS`? | A reservation is a new kind of entry with its own admission rule, not new content of a consumption record; declaring it as a kind keeps the Research Record's existing meaning (what was learned) intact |
| Stop conditions | The kind, its rules and the derived quantities are proposed for the Principal's decision; none is established by the record |

## 2. Findings

| Ref | Mode | Finding | Disposition |
| --- | --- | --- | --- |
| P8-1 | Ontology | Is a new kind truly needed? | YES, by §2 of the record: the Authorization is immutable, consumption records are after the fact, proposals entitle nothing, and the Applied History deliberately does not own research consumption |
| P8-2 | Semantics | The five budget states are defined so that no unit is counted twice | Checked after R-1: every unit is in exactly one state; remaining spendable = grant − reserved allowance − attempted-unsettled − settled, across open and closed reservations; released is only what was never attempted |
| P8-3 | Semantics | Consumption accrues per settled attempt; long experiments are many attempts | Interim totals derived; nothing is consumed without a prior `PENDING` |
| P8-4 | Semantics | Unused allowance on finish, failure, cancellation, retirement, expiry or revocation | Released to the grant in every case; never to another Authorization or a successor |
| P8-5 | Semantics | Successor and predecessor allowance | A successor cannot reserve without an Authorization; nothing is inherited (§III.4 unchanged) |
| P8-6 | Idempotency | Retry | After R-2: every dispatch has its own pre-record and maximum (identity includes a dispatch index); `DUPLICATE_ATTEMPT` refuses a second pre-record of the same dispatch; reconciliation precedes retry where the provider allows; exactly-once never claimed without a named provider mechanism |
| P8-7 | Honesty | Overrun above the reservation | Settled in full and counted in full; the reservation goes negative, the grant absorbs it, `OVERSPENT` refuses further work until the Principal acts. The record does not pretend the overrun was prevented |
| P8-8 | Authority | Settlement after revocation | Admitted, because it reports and entitles nothing; consistent with "nothing is deleted" (I-11) |
| P8-9 | Two paths | Theme-based and empirical agents | Reservation purpose is a Theme or a `SearchFamily` in scope; the five cases alternate between `AD-21.1` and `AD-27.1`; no rule differs |
| P8-10 | Dependency | PD-007's `P-1` condition (b) | Must read a committed `RESERVATION` named by the proposal, not a derived remainder; PD-007 revision 2 makes that change |
| P8-11 | CPOC | Process death before settlement; two processes settling one attempt | The first settlement wins by sequence; the second is refused as a settlement of a `SETTLED` attempt and preserved; a fresh process reconstructs every open obligation from the ledger |
| P8-13 | Ordering | Can a reservation committed before the fence authorize an attempt after it? | NO. Rule 2 orders the attempt's admission against the fence at the attempt's own sequence; the reservation's sequence is irrelevant to that check; the fence closed it |
| P8-14 | Ordering | Is the fence check made through the same serialized mechanism that inserted the fence? | YES. One Evidence commit boundary, one sequence; the check and the admission are one act; no read of another ledger decides it |
| P8-15 | Crash | Fence committed, Principal dies before the Transition | "Active, fenced": funding stopped, liabilities held, settlements admitted; resolved by Transition whenever the Principal acts; indefinitely safe |
| P8-16 | Crash | Agent dies before attempt commit | Nothing survives; a fresh commit is ordered against the fence at its own sequence |
| P8-17 | Scope | Were revision 3's additions removed in full? | YES: outstanding permission, read-to-commit interval, instants beyond PD-002's stamp, straddler view, Apply witness read; only the withdrawal sentences remain |
| P8-12 | Scope | Queues, databases, providers | None named; the contract is facts and boundary rules only |

## 3. ANF check

| Invariant | Finding |
| --- | --- |
| Singular decision authority | Grant: Authorization. Reservation, attempt, settlement: Evidence ledger. Derived quantities and `OVERSPENT`: none |
| Classified representation closure | Every quantity classed `DERIVED`; the agent's plan `EPHEMERAL`; the provider's invoice is external evidence recorded in a settlement, never authority |
| Exclusive governed commit boundary | Unchanged: Evidence commit under the Research Authorization; the new kind has its own admission rule at the same boundary |
| Temporal and binding closure | Reservations bound to an Authorization, a purpose and an expiry on the Evidence clock; attempts bound to a reservation and a deterministic identity; settlements to an attempt |
| Owner-resolved consumption | Research consumption on the Evidence ledger, now before and after the work; capital consumption at Apply unchanged |
| Legacy isolation | Not implicated |
| Constitutional failure closure | New refusals preserved: `BUDGET_EXCEEDED`, `CAP_EXCEEDED`, `AUTHORIZATION_INACTIVE`, `NO_RESERVATION`, `ALLOWANCE_EXCEEDED`, `RESERVATION_EXPIRED`, `DUPLICATE_ATTEMPT`, settlement of a settled attempt; `OVERSPENT` as a derived refusal standing |

## 4. Residuals and open items, with owners

| Item | Standing | Owner |
| --- | --- | --- |
| P8-R1 Vendor charges are estimated; the units ceiling is hard, the invoice is not | Stated; Authorization content decides margins and whether unboundable calls are allowed | Principal, per grant |
| P8-R2 A reservation held open by a live but idle agent until expiry | Visible; expiry bounds it; the default expiry is Authorization content | Principal |
| P8-R3 Pre-recording every call has an operating cost | Accepted; it is the price of "reserved before consumption"; granularity (per call or per batch) is the agent's choice within a reservation | Plan step 9 |
| P7-R2 (PD-007) stale derived reservations | Closed by this record: there are no derived reservations | — |

## 5. Revision 2 adversarial review (Principal's four tests)

| Test | Revision 1 | Defect | Repair in revision 2 |
| --- | --- | --- | --- |
| Outstanding obligations at expiry or revocation | Released = amount − settled; rule 4 released "the remainder" | **R-1.** A closed reservation's `PENDING` attempt could be released into another agent's spendable budget: a liability counted twice or not at all | Five states; released = amount − settled − attempted-unsettled; expiry and revocation release only never-attempted allowance; an unconfirmed attempt stays a liability at maximum until settled by the grantee with provenance or by the Principal `UNKNOWN` |
| Retries and uncertain external effects | Retry under the same identity; both charges settled together | **R-2.** The retry's additional potential cost was never authorized before dispatch; the reservation could be overrun by construction | Dispatch index in the attempt identity; a retry is its own pre-record against remaining allowance, refused if insufficient; reconciliation before retry where possible; exactly-once never claimed without a provider mechanism named in the Authorization |
| Authorization revocation race | The reservation's commit read the head; nothing said when a reservation may fund work | **R-3.** Unstated authority boundary across two ledgers with no shared transaction | The attempt's commit is the boundary: admitted only with the Authorization active at the head read there; active at both reads means active throughout (append-only, revocation never undone); a reservation whose authority cannot be established funds nothing; a revocation after the pre-record does not reach the in-flight charge, which settles |
| Hard versus soft guarantees | "Forbid or require a declared margin" beside the units ceiling | **R-4.** A margin on an uncapped charge read as a ceiling | Three tiers: bounded units (hard, system-enforced); capped provider charges (enforced by the provider, recorded as such); uncapped charges (soft; a margin is an estimate, never a ceiling); full overrun settlement and `OVERSPENT` preserved |

Five runs under revision 2: ten agents against one remaining budget
(seven admitted by sequence, three refused); simultaneous last-unit
reservation (second refused, no partial); expiry during an unsettled
call (unattempted 1 released, A-3's 3 held as a liability until
settlement); ambiguous retry (dispatch 1 pre-recorded against remaining
allowance, dispatch 0 held at maximum, exactly-once not claimed);
concurrent revocation (attempt refused at the head, reservation funded
nothing, in-flight A-9 settles). All five are in the record's §4.

**Answers.** (1) The existing Research Record and Evidence commit
boundary suffice once the `RESERVATION` kind is added; no further
object, ledger or boundary. (2) The repairs are `ΔS` only: the five
states, the dispatch index and settlement provenance, the authority
boundary and the tiers; `ΔO` stays +1, `ΔA` stays 0. (3) Genuinely
enforceable: no unit reserved or attempted twice; nothing attempted
without a reservation whose authority is established at the attempt;
nothing attempted past a reservation; nothing reserved past a grant;
every overrun settled and counted; `OVERSPENT` funds nothing further;
no liability released except by settlement. (4) Dependent on providers:
whether a capped call is actually capped; whether an uncapped call's
charge exceeds its estimate; whether a dispatch after process death was
executed or charged; whether a provider deduplicates a retry. (5) PD-008
revision 2 is ready for the Principal's admission.

## 6. Revision 3: the revocation-ordering challenge

**The interleaving.** Read at `H` active; revocation applied at `H+1`;
attempt committed on the basis of `H`; dispatch.

**Finding under revision 2: admitted.** The boundary's read showed
active at `H`; the commit recorded `N_w = H`; nothing refused it.
Revision 2's "active at both reads means active throughout" established
activity up to the instant of the second read and said nothing about
the commit instant; as a claim about the commit it was an overclaim,
since no existing boundary orders an Evidence commit against an Apply.
"Read the current head" cannot refuse step 3; neither can "check again",
because any check is itself a read with the same gap after it.

**Repair (revision 3).** Precedence is *defined*, not observed: an
attempt with witness `N_w < R` precedes the revocation at `R`; one with
`N_w ≥ R` is refused. The read confers an **outstanding permission**
scoped to one commit by the reading boundary within its own
read-to-commit interval, consumed by that commit, extinguished by any
later read; an attempt admitted under it is lawful, dispatches, settles,
and is counted. Revocation is enforced at the next read. The three
events, authorization read, attempt admission commit, external dispatch,
are distinguished; the commit decides precedence; the dispatch decides
nothing. The window is made visible (`t_r`, `t_c` stamped by the clock
the Evidence boundary owns) and boundable (a declared maximum interval
as Authorization content); straddlers are made derivable by a witness
read of the Evidence head at the revocation's Apply.

**Mechanism check.** Does the repair use existing owners and boundaries?
The Evidence commit boundary already reads the Applied History head
inside its commits and stamps instants (PD-002); the Applied History's
Apply sequence already exists; the Transition record already carries
Apply content. The one addition is the Apply boundary's witness read of
the Evidence head, a ledger read of the kind I-13 admits and PD-002
classed as `ΔS`. The record reports it for classification rather than
assuming.

**Delta after revision 3.** `ΔO` +1 unchanged. `ΔS` extended: defined
precedence, outstanding permission, `t_r` and `t_c`, the interval
constant, the straddler view, the Apply witness read. `ΔA`: none claimed;
the Apply witness read reported, `ΔS` recommended by precedent, `ΔA` +1
read right if the Principal so classifies.

**Guarantees, qualified as directed.** Hard metered units and
enforceable provider caps support ceilings. Uncapped charges support
admission against estimates and full overrun accounting, and no
ceiling. Revocation supports refusal at the next read and visibility of
every straddler, and no commit-time enforcement.

**Residual P8-R4.** The straddle window is bounded in time by the
declared interval and in size by the attempt rate, never zero. Owner:
Principal, as Authorization content; the view makes every instance
visible.

## 7. Revision 4: Alternative A adopted

At the Principal's direction (2026-10-19) the record adopts the fence
of the [comparison](pd008_revocation_ordering_comparison_20261019.md).
The ordering the Principal required holds: every reservation and attempt
is checked against the fence by the same serialized commit that
inserted it; a reservation below the fence cannot authorize an attempt
above it; attempts below it settle; ambiguous external execution stays
under the retry rules. "Funding stopped" (Evidence ledger, fence) and
"revoked" (Applied History, Transition) are distinct, and a fence
without its Transition is an effective stop.

**Authority, corrected.** The record no longer claims `ΔA` none on the
ground that the Principal may already commit Evidence. The authoritative
funding-stop fact is on the Evidence ledger, enforced at its boundary,
and making it effective before Apply gives the Principal a decision
right at an ordinary boundary without the Check every consequential
change otherwise requires. Declared `ΔA` +1 with its commit
restriction.

**Delta of revision 4.** `ΔO` +2 (`RESERVATION`, `FENCE`). `ΔS` as
listed in the record, with revision 3's additions withdrawn. `ΔA` +1.
The Apply witness read is not needed under A and nothing remains to
classify.

**Remaining admission issue.** The `ΔA`. The Principal decides whether
a fail-closed, irreversible, Principal-only funding stop may be
exercised without independent Check. The audit finds the trade honest:
the alternative is inexact enforcement with stated exposure.

## 8. Admission recommendation

PD-008 revision 4 satisfies the governing requirement with one new kind on the
ledger that already owns research consumption, one declared authority change, hard enforcement in units, honest
treatment of external charges, exact ordering of funding against
revocation, and recovery from the ledger alone. Recommend the Principal
decide it before PD-007, whose policy `P-1` reads the reservation it
defines and needs no change.

## 9. What this audit does not establish

That any provider cap will hold, that an estimation rule will be
accurate, or that agents will size reservations sensibly. It
establishes that no two agents can reserve the same unit, nothing is
consumed without a prior reservation and attempt, every overrun is a
recorded fact, and no budget authority lives in a process.
