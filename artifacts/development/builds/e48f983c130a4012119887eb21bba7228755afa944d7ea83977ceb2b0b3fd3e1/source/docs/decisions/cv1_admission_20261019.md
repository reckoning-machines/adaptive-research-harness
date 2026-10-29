# Admission of `ConstitutionVersion 1` — Document-Phase Design Baseline

Status: **ADMITTED 2026-10-19 by the Principal (document-phase admission).** This record is the admission. The admitted text is the exact byte sequence of [`docs/doctrines/new_speedway_constitution.md`](../doctrines/new_speedway_constitution.md) at the digest below, Constitution revision 12, which is preserved unchanged: its own status banner ("DRAFT — NOT ADMITTED") predates this record and is superseded by it, because altering the banner would alter the admitted bytes.

## Admission text, as given

```text
I approve the PD-011 narrow A-1 direction, explicit-at-genesis A-2
requirement and confirmed A-3 propagation corrections. I admit
Constitution revision 12 as ConstitutionVersion 1, the document-phase
design baseline, at reviewed SHA-256:
c56a9cf50a7e9efadad8f2f2be6605e82c758f18d4096ba07eaaf86a8f8b7a64
```

Digest verified identical to the working-tree file before this record
was written, and identical to the digest named in Codex's
[independent closure review](../audits/cv1_revision12_closure_20261019.md),
which found the baseline ready for admission with F-2 closed and A-3
confirmed as faithful propagation.

## What is admitted

| Item | Disposition |
| --- | --- |
| `ConstitutionVersion 1` | The text at the digest above: ten governed objects, the invariants, Part V's Transition classes with policy `P-1`, the genesis clause and the Principal control-act paragraph, Part X `ES-1.0`, and every PD-001 to PD-010 repair as propagated through revision 12 |
| PD-011 A-1 | The Prediction witness read keeps PD-010's exact `HypothesisId` scope; the broader alternative is superseded and not admitted |
| PD-011 A-2 | The binding interval of `AU-RP-1` is explicit genesis grant content with no default of any kind; the value is still to be supplied by the Principal before genesis |
| PD-011 A-3 | The F-1 and F-2 corrections of revision 12 are faithful propagation of PD-010 choices 2 and 9, as Codex confirmed |
| Constitutional Delta of this admission | `0/0/0` relative to revision 12; the cumulative delta of the draft is the Constitution's own closing section |

## What has not occurred

Implementation has not begun. No runtime, store, vendor, backtester or
model provider has been selected. Genesis (Apply sequence 0) has not
executed; every admission to date, this one included, is a
document-phase admission by the Principal that stands in for a
Constitutional Transition until genesis executes. No CPOC witness has
run and nothing is certified. No claim of investment performance is
made.

## Outstanding pre-genesis parameters, explicit

Each must be supplied by the Principal before the genesis act that
depends on it; none is chosen here, and an incomplete grant cannot be
applied or used for a binding.

| Parameter | Where it is required |
| --- | --- |
| The numerical binding interval of `AU-RP-1` | §III.7 Content; PD-009 §3 as amended; PD-011 A-2 |
| Source Declarations for `SRC-E` and `SRC-SYN`: identities, print rules, deterministic extraction rules, resolution grace, structural bounds | §III.7 Source Declaration; PD-009 §3 |
| Exact provenance, content hashes and initial method commitments of `AD-CK-1.0`, `AD-CK-2.0` and `AD-R1.0` to `AD-R10.0` | §III.4; Part X §3; PD-009 §6 |
| Complete grant content of `AU-CK-A`, `AU-CK-B`, `AU-OBS-1` and `AU-RP-1`: tools, tiers, estimation rule, caps, expiries, verification purposes | §III.7 Content; PD-009 §3 as amended |
| Per-provider acceptance of the output-cap and billing assumption before any real provider call is treated as capped | PD-009 §5 |
| The first Execution Authorization and fill rule `FR-0`, granted later, not at genesis | PD-009 §6; §III.7 |
| Standing constraints: D-14 (provider fixed to the registered design), U-1 (no capital route for non-reproducible versions), U-8 (limits between witnesses, plan step 7) | Initial audit; PD-002; PD-004 |

## Sequence that led here

The independent pre-implementation audit failed revision 10 on ten
findings; PD-010 repaired them through four reviewed revisions and was
admitted and propagated as revision 11; the final independent review
of revision 11 found F-1 and F-2; the corrections were propagated as
revision 12 with their basis recorded; a bounded follow-up closed F-1
and required the F-2 execution exception to be gated on an applied
`REDUCE`; the second pass did so; the closure review found the baseline
ready. Every audit, including the failures, is preserved unchanged in
`docs/audits/`.

## Next

An implementation plan with its own declared Constitutional Delta and
its evaluation of existing engines against the reserve, attempt,
interruption, fence, retry, settlement and admission sequence becomes
proposable. It authorizes nothing by itself.
