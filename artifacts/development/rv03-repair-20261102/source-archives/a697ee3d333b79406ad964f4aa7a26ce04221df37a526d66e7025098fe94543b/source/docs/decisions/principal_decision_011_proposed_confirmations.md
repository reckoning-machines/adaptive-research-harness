# Principal Decision Record 011 — Proposed Confirmations after the Final Independent Review

Status: **ADMITTED 2026-10-19 by the Principal (document-phase admission): A-1 narrow, A-2 explicit at genesis with no default, A-3 confirmed as faithful propagation**, recorded in [the `ConstitutionVersion 1` admission record](cv1_admission_20261019.md) after Codex's [closure review](../audits/cv1_revision12_closure_20261019.md) confirmed A-3. The superseded alternatives below remain superseded and were not admitted. Author: Claude.
Date: 2026-10-19.

**Principal's directions (2026-10-19), recorded, not admitted:**

| # | Direction | Applied in the working tree |
| --- | --- | --- |
| A-1 | Keep PD-010's exact `HypothesisId` scope; do not broaden speculatively. No existing Strategy Version Prediction path needs the extension: a Strategy's scored events are Decisions, and Part X §3 names the Prediction's commitment only for Hypotheses | §III.5 Prediction row reverted to `HypothesisId` |
| A-2 | Set the binding interval explicitly in the genesis grant; no implicit one-day default | PD-009 amendment note: explicit grant content, no default, a grant without it is incomplete; **the value itself is still to be supplied by the Principal before genesis** |
| A-3 | Codex to confirm F-1 and F-2 are faithful propagation, especially that the execution exception remains limited to qualifying reductions | Follow-up handoff scope item 3 states this; nothing is admitted until that confirmation |

Sequence after Codex's confirmation, as the Principal directed: record
these decisions, admit `ConstitutionVersion 1`, commit, regenerate the
prospect ZIP. No broader documentation work is planned.

Subject: the items from the
[final independent review](../audits/cv1_final_independent_review_20261019.md)
that are the Principal's to decide, isolated here as the Principal
directed. The propagation corrections for F-1 and F-2, applied under
PD-010 with their basis recorded in the
[correction record](../audits/cv1_correction_record_f1_f2_20261019.md),
are not choices and are not listed here; they are listed below only
for the Principal's acknowledgement.

## A-1. Scope of the Prediction witness read (review §6, first item)

PD-010 choice 6 admitted "the Prediction witness read at the Evidence
boundary"; its exact replacement text in §3 B-6 named `HypothesisId`.
Revision 11's §III.5 Prediction row refuses a Prediction whose
`HypothesisId` **or `StrategyVersionId`** is not admitted at the head
witnessed at commit. Predictions bound to a `StrategyVersionId` exist
(§III.5 Prediction row), and the broader read requires only that the
subject be admitted, as for a Hypothesis.

| Choice | Effect |
| --- | --- |
| ~~Confirm the broader scope~~ **SUPERSEDED, rejected by the Principal's direction of 2026-10-19; not available for admission** | Would have kept the `StrategyVersionId` extension; withdrawn |
| **Narrow to `HypothesisId` (the Principal's direction; applied)** | The row carries PD-010's exact wording; a Strategy Version's Prediction is not subject to the registration witness read, and Strategy Decisions keep their own admitted-version rules |

## A-2. The binding interval value for `AU-RP-1` (review §6, second item)

PD-010 requires every Research Authorization that funds budgeted
registrations to declare a **binding interval** (§III.7) and selects no
value. An earlier version of PD-009's amendment note stated "one day"
as if it were admitted; it was a proposal. The note now says the value
is grant content for the Principal to set at genesis.

| Choice | Effect |
| --- | --- |
| **Set the value explicitly in the genesis grant, no default (the Principal's direction; applied as the PD-009 note)** | No value is admitted now; the genesis grant for `AU-RP-1` is incomplete until the Principal states it; nothing in the Constitution changes |
| ~~Accept one Evidence-clock day now~~ **SUPERSEDED, rejected by the Principal's direction of 2026-10-19; not available for admission** | Withdrawn |

## A-3. Acknowledgement of the two propagation corrections

Listed for the record, not as choices. If the Principal considers
either a new choice rather than a faithful propagation, say so and the
clause is withdrawn pending a proposed amendment.

| Correction | Basis |
| --- | --- |
| F-1: a Principal control act is any Transition the Principal proposes that declares no metered research consumption, and the Principal's own authority is the predicate at Check, Decide, Apply and continuation | PD-010 §1's definition of a control act by actor and funding, and choice 2's applicability rule; PD-009's admitted sequence; Part V's existing proposer rights |
| F-2: I-10 and the Paper Book limit gates test the change a `REDUCE` and its reducing orders make (no new or worsened breach, no opening exposure), not the resulting state, so a verified partial reduction with a residual breach is admitted and executed | PD-010 choice 9, criteria (iii) and (iv), as admitted; the Principal's direction of 2026-10-19 restating the same bound |

## Delta of this record

```text
ΔO: NONE.  ΔS: NONE beyond PD-010 (A-1 keeps or narrows propagated text;
A-2 is Authorization content).  ΔA: NONE.
```

## Decisions for the Principal

| # | Question | Recommendation |
| --- | --- | --- |
| A-1 | Prediction witness read scope | Narrow to `HypothesisId`, as directed and applied |
| A-2 | Binding interval for `AU-RP-1` | Explicit genesis grant content, no default, as directed; value to be supplied by the Principal |
| A-3 | Acknowledge the F-1 and F-2 corrections as faithful propagation | After Codex confirms; the follow-up closed F-1 and required the F-2 execution exception to be gated on an applied `REDUCE`, now done in the working tree |
