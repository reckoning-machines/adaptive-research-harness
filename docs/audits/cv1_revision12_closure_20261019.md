# Independent Closure Review — Constitution Revision 12

**Ready for Principal CV1 admission and subsequent prospect packaging. F-2 is closed. A-3 is confirmed as faithful propagation.**

Reviewer: Codex. Date: 2026-10-19. This is a bounded document review, read together with the original whole-design audit, the final independent review and the [first revision 12 follow-up](cv1_revision12_bounded_followup_20261019.md). It is not admission, permission to execute genesis or certification of runtime conformance. All existing files were preserved.

## Exact reviewed baseline

The subject is **working-tree Constitution revision 12, second pass**, after commit `f77fe921c3672dd4d415196b1dddd124f4eac05b`. It is not the earlier revision 12 reviewed under digest `64b37414…` and is not the committed revision 11.

**Constitution SHA-256: `c56a9cf50a7e9efadad8f2f2be6605e82c758f18d4096ba07eaaf86a8f8b7a64`.**

I read `AGENTS.md`, the [revised handoff](cv1_followup_handoff_20261019.md), the operative clauses and their immediate context, the admitted PD-010 choice 9, proposed PD-011 and the listed package reconciliations. Exact supporting file digests:

| File | SHA-256 |
| --- | --- |
| `AGENTS.md` | `d96e321ff2d1b12d3753c30e52f5305b548ce6d38ad4482360cf03cb4b3b25c4` |
| `docs/audits/cv1_followup_handoff_20261019.md` | `68bdb5c3594bb0fcc02eb0cb400ee1cd127b8b73e82d51e3a580d8ae27d4d6a6` |
| `docs/audits/cv1_correction_record_f1_f2_20261019.md` | `6c34f3fb388950cb10a06ef41ac6bdfe250a18b8926b0a0010d85fb49a714291` |
| `docs/decisions/principal_decision_009_genesis.md` | `054c0617635b0224669144127261f37332d5dc1b5c99e77f61b5b494bb6850ca` |
| `docs/decisions/principal_decision_010_codex_audit_repairs.md` | `2c58d487fc72a5ec6b4db0f901fb17ff6773b5403abbe369ddbc1f6286d63279` |
| `docs/decisions/principal_decision_011_proposed_confirmations.md` | `0c792df4b8b5a63c88302da5215c4ee32e1ceaa9e5a0b4aacffd92603f19f686` |
| `README.md` | `67985fc5cc06e9eac6d8a2eb78d2be20a9b33331f6acdeb136fe1e6f7063826e` |
| `architecture.md` | `11d9d87a24839794e1d7811853dcf33d789864c087df45e5db475694b6761c79` |
| `docs/package/cv1_review_package_manifest.md` | `44fb711255f27dd09f25abd2d0d6bbf1690faaaa7b1b22f67fa7cb3411a03796` |

The handoff's Constitution digest matches. Its correction-record digest `325dfd9d…` is stale. The complete actual correction record was read and is identified above. This is an evidence-index discrepancy, not a governing-clause defect. The final review and first revision 12 follow-up retain their previously recorded digests `939c6885…` and `0415d6d4…` respectively.

## F-2 gate and independent replay

The [Constitution](../doctrines/new_speedway_constitution.md) §III.10 Admission and Limits clauses, particularly lines 1449–1480, now require **all four predicates at the pre-witness**:

1. The set names an applied Allocation Transition of purpose `REDUCE`, in force at `N_1`.
2. That reduction's execution obligation remains outstanding. The order moves toward its lower target, reduces the distance from the confirmed position and does not pass the target.
3. The order is `REDUCING`.
4. Its full fill leaves every limit usage non-increasing, creating or worsening no breach.

The first predicate is authoritative attribution, not a caller's label. The existing set key identifies the actual applied Allocation Transition. Part V's Allocation row requires an independent Check and the Principal as proposer and decider for `REDUCE`. The Transition lifecycle and Applied History establish that those steps occurred. A proposed, merely checked, unapplied or superseded reduction does not qualify. No new authority is conferred on the Execution function.

| Replay | Deciding records and result |
| --- | --- |
| Limit 5, exposure and target 10, qualifying REDUCE to 6 | The independent Check applies I-10's bounded qualification and Part V criteria (i)–(iv), recording residual breach 1 and no increased usage. The Principal decides. Apply records target 6 and unchanged standing. A sell of 4 in the set keyed to that applied reduction satisfies all four predicates and is admitted despite the residual breach. Its fill remains subject to the reducing bound |
| Death after Apply, before any order | Applied target 6 and confirmed position 10 establish the outstanding obligation. Recovery derives the reducing order and checks the same predicates against current records. Process memory supplies no permission |
| Fill 2, then death and restart | Confirmed position is 8, target remains 6 and the original order has remainder 2. A `REPLACE` names that parent and carries only its unfilled remainder. The same-side calculation excludes the parent's remainder for the replacement. Full fill leaves 6, so all four predicates pass. Repeated `OrderId` is refused `DUPLICATE`. At position 6 the obligation is discharged and the exception supplies no further authority |
| Ordinary Strategy Decision targets 6 under unchanged QUALIFIED allocation | Its set names the original allocation, not an applied `REDUCE`. Predicate (a) fails. The ordinary rule treats the remaining exposure 6 against limit 5 as a breach and refuses `LIMIT`. A restart reaches the same result. The Decision cannot substitute for a Principal reduction act |
| Opening, overshooting or worsened-risk order | Opening fails (c). Passing the REDUCE target fails (b). Increasing any usage fails (d), even if that increase would remain within its own limit. Such an order cannot use the exception. Ordinary rules decide any remaining path, with opening into or within a breach expressly refused |

All four conditions are determinable from the applied allocation, current Paper Book records, set linkage and existing limit calculations at the pre-witness. Unreachable authority does not permit fallback. Ordinary Decision and expiry sets outside the qualifying reduction remain under ordinary limits. The exception waives no Execution Authorization, set, expiry, stale-base, provisional-fill, duplicate or fill-bound requirement. U-8 remains the already-declared moving-limit limitation.

Reduction to zero retains `INCUBATING` standing and a separate execution obligation, provided the reduction worsens no other usage. Applying zero does not claim a flat position before execution. No standing promotion or qualification credit follows from a partial reduction.

**F-2 is closed at the document-contract level.** The previous scope counterexample now refuses, while the admitted partial reduction and its recovery proceed.

## A-3 and retained closures

The current predicate faithfully carries PD-010 choice 9's non-increasing-risk and residual-execution requirements through the existing allocation/set linkage. It restores the ordinary rule outside that admitted scope. It creates no new object, caller, cancellation right or discretionary waiver. Together with the previously verified Principal-authority applicability repair under choice 2 and PD-009, **A-3 is confirmed**. The declared semantic propagation adds no permission beyond the admitted choices.

F-1 remains closed. The unsupported Strategy Version registration example has been removed from the control-act list. Independent Check, class criteria and separately funded Checker work remain required. A-1 retains the exact `HypothesisId` witness scope, with Strategy Decision rules unchanged. A-2 retains explicit binding-interval grant content with no default. No concrete contradiction introduced by this change reopens those findings or the settled accounting, binding, settlement, cutoff and reversal conclusions.

The original whole-design audit's failures remain historical evidence for revision 10. The final revision 11 review and first revision 12 follow-up remain accurate for their bytes. This report closes their remaining F-2 blocker rather than treating an earlier focused review as whole-design clearance. Read together, the reviews support readiness of this exact consolidated document baseline for Principal CV1 admission, within the declared prototype scope.

## Package and outstanding preparation

The listed reconciliations are present. README and architecture identify working-tree revision 12, describe F-1 as repaired and identify F-2 as awaiting this check. The architecture's reduction and recovery rows reflect the corrected rules. The manifest names revision 12 and all six prior independent audits. PD-011 marks the broader A-1 and implicit one-day alternatives superseded, and its decision table matches the Principal's directions. The correction record's A-1 row is corrected. These documents make no implemented, admitted or certified claim.

Their statements that this check is pending accurately describe the submission to this review. After the Principal's decisions, update those status references and list this closure report and the admission records in the manifest. Use the actual supporting-file digests above in the final package record. These are routine packaging updates, not additional policy or design blockers. No optional improvement is made an admission condition.

The declared pre-genesis content remains outstanding, particularly the Principal's numerical binding interval for `AU-RP-1`. Required source declarations, extraction and resolution-grace content, exact design provenance and commitments, and complete grant content must be supplied before their relevant genesis acts. An incomplete grant cannot be applied or used for a binding. Leaving these execution parameters unset in the design package does not prevent CV1 admission. This review chooses none of them. Real-provider acceptance and the later Execution Authorization and fill rule remain their existing separate gates, with neither added to the two initial demonstrations.

The existing Downloads ZIP is stale and remains a draft review copy. After Principal admission, regenerate it from the approved packaging baseline with this report and the admission records, preserving paths and checking links. This review does not build or send the ZIP.

**Ready.** No further design correction is required within this bounded closure. The next action is the Principal's recorded decisions and CV1 admission against the exact Constitution digest above, followed by the package updates and ZIP regeneration. No existing file was amended, no policy was changed, and no admission, commit, push, implementation, genesis execution or runtime certification was performed. The audit's `ΔO/ΔS/ΔA` is `0/0/0`.
