# Independent Bounded Follow-up — Constitution Revision 12

**Disposition: BLOCKED for Principal CV1 admission and final prospect packaging. F-1's original failures are closed. F-2 is not closed because the execution exception exceeds the admitted REDUCE scope.**

Reviewer: Codex. Date: 2026-10-19. This is document review evidence, not admission, implementation or runtime certification. No subordinate agents were used. All pre-existing working-tree edits were preserved.

## Reviewed subject

The subject is the uncommitted working tree after `f77fe921c3672dd4d415196b1dddd124f4eac05b`, not that commit's revision 11. I read `AGENTS.md`, the [follow-up handoff](cv1_followup_handoff_20261019.md), the changed operative clauses and their immediate context, PD-010's admitted choices, PD-009's genesis requirements and proposed PD-011. The user's request includes readiness and package standing, notwithstanding the handoff's narrower exclusion of readiness.

SHA-256 digests of the exact reviewed files:

| File | Digest |
| --- | --- |
| `AGENTS.md` | `b6533c452f73f25d8471857f088c7ea10124a3c5b3b45b6fa3436a4552799009` |
| `docs/doctrines/new_speedway_constitution.md`, revision 12 | `64b37414b38e687846501e4624bde90e30b839386402964f539eceed7d94a6ad` |
| `docs/decisions/principal_decision_009_genesis.md` | `054c0617635b0224669144127261f37332d5dc1b5c99e77f61b5b494bb6850ca` |
| `docs/decisions/principal_decision_010_codex_audit_repairs.md` | `2c58d487fc72a5ec6b4db0f901fb17ff6773b5403abbe369ddbc1f6286d63279` |
| `docs/decisions/principal_decision_011_proposed_confirmations.md` | `2dadba806b5e3bb0be3ddc6ed6a187724399f343c940c326a3a0966e5477f989` |
| `docs/audits/cv1_followup_handoff_20261019.md` | `80bfb5d4edef8139b594427262aae201f56a7ad3a5d1fe8a56f6301416966458` |
| `docs/audits/cv1_correction_record_f1_f2_20261019.md` | `598de3c9831f7ef21b83132f2b2d71e0621c6da7ce23b8fbf9bc24abff5bcbe7` |
| `docs/audits/cv1_final_independent_review_20261019.md` | `939c688541700a53a7e39757b4d7828aac422987dd4755d456e7bd94a10cdc93` |
| `README.md` | `bd1f1395852079faccf7b682d379abdc5a2a43fc38fa35baef598db30f82d098` |
| `architecture.md` | `7d486af05cfa58d333919850fe8f07212e26f04c4c5e57de6a657d0d7149a19c` |
| `docs/package/cv1_review_package_manifest.md` | `bb360d8e1143bef15b582ef8e041f222110cc7805db6328c3cc9f4bc4563298a` |

Below, C means the [Constitution](../doctrines/new_speedway_constitution.md). Line references identify these revision 12 bytes.

## F-1 — Original counterexamples closed

C §III.8 record form item 1 and Check items 1 and 4, lines 1080–1127, now distinguish direct Principal authority from an agent's Authorization. Continuation, lines 1190–1214, applies the active, unexpired Authorization predicate only to a proposal made under one. Part V's Principal control acts paragraph, lines 1610–1626, expressly carries direct authority through Check, Decide, Apply and restart for classes the Principal may already propose. It makes the inapplicable fields `N/A`, preserves every other class criterion and separately funds the Checker's work.

| Replay | Deciding record and result |
| --- | --- |
| First research Agent Design registration after Apply 2 | Part V already permits the Principal proposer. The Check cites direct Principal authority, the current base and its own funded Checker attempt. With provenance, method commitment and other criteria satisfied, the Principal decides and Apply 3 records membership. No Research Authorization for the Principal is invented |
| Death after deciding `AU-OBS-1`, before Apply 1 | The existing Check and Principal decision remain the deciding records. At head 0, recovery can Apply without a nonexistent proposer Authorization or binding. A changed head still requires recheck and redecision. An already applied grant is not reapplied |
| Interrupted agent registration under `P-1` | The agent cannot invoke the Principal branch. Its active grant, policy conditions and binding remain required. Fence, expiry and consumption retain their previously admitted effects |
| Checker funding unavailable | The Principal's `N/A` line does not fund the Checker. A new Checker attempt must pass its own grant, reservation, cap and fence predicates. Direct Principal authority does not waive independent Check or permit an unfunded attempt |

This is faithful applicability propagation of existing Principal rights, PD-009's genesis chain and PD-010 choice 2. Record form item 7 still uses generic Authorization wording, but the explicit lifecycle-wide direct-authority exception supplies the answer without a self-grant.

One nonblocking textual inconsistency should be removed in the same correction pass. The new Part V paragraph lists **Strategy Version registration** among Principal-proposable classes, while its row at line 1600 names only a Research Agent as proposer. The paragraph's opening restriction to classes Part V already permits prevents treating this list as a new grant. Delete that unsupported example rather than infer a new proposer right. Principal decision authority over registration is not the same as proposer authority. Aligning item 7's wording with its explicit exception would also improve clarity, but is not a further functional blocker.

## F-2 — High severity, still blocked by an overbroad execution exception

**What now works.** I-10, lines 1526–1539, and Part V Allocation criterion (i), line 1601, expressly limit the projection exception to `REDUCE`. A Principal-proposed reduction from 10 to 6 against a limit of 5 can pass an independent Check when every usage is non-increasing, no exposure increases and no new breach appears. The residual breach of 1 is recorded. The Principal decides, Apply changes the target and preserves standing, and a sell of 4 can pass the new Paper Book limit test. Apply itself liquidates nothing.

Death after Apply and before an order leaves the applied lower target and confirmed position as the recovery inputs. Recovery derives the reducing obligation, subject to current admission checks. A partial fill leaves a visible residual. Reduction to zero follows the same route where it worsens no other usage, records `INCUBATING` and does not claim liquidation before execution. If unwinding a hedge increases net usage, criterion (iii) fails even if that increase would remain below its limit. A stale base is still refused.

**Concrete remaining defect.** C §III.10 Admission, lines 1392–1396, directs every Decision-set `REDUCING` order to the Limits bullet. That bullet, lines 1445–1462, says an order whose full fill lowers or leaves unchanged every usage is admitted despite a persistent breach. It contains no requirement that the order execute a qualifying applied `REDUCE`. A citation to PD-010 choice 9 does not supply an enforced allocation-purpose predicate. I-10's restriction on the allocation Transition does not restrict ordinary Paper Book admission under an existing allocation.

**Smallest counterexample.** Keep an existing `QUALIFIED` allocation in force, with confirmed exposure 10 and a limit of 5 after an existing breach has arisen. No `REDUCE` is proposed, checked, decided or applied. A normal committed Strategy Decision targets 6. Its sell of 4 is `REDUCING`, lowers every usage and satisfies the revised generic Limits bullet despite leaving exposure 6. It is admitted without the checked, Principal-decided `REDUCE` required for this exception. A restart can derive the same order from the unchanged allocation and Decision. No moving-limit race or opening order is needed.

**Minimum repair.** Gate the persistent-breach exception at the Paper Book boundary on the order's attribution to a qualifying applied `REDUCE` and its admitted execution obligation. Use the existing allocation/set linkage. Require the stated non-increase and no-new-or-worsened-risk tests for this branch, and preserve ordinary limit rules outside it. Any broader exception for ordinary Decision or unrelated expiry orders would require a separate explicit policy decision and cannot be called faithful propagation. No new object or execution prototype is needed.

The opening prohibition remains explicit, and the fill-level `REDUCING_BOUND`, provisional-fill accounting, expiry obligations and U-8 treatment remain intact. The failure is scope, not the original 10-to-6 arithmetic. **A-3 cannot be confirmed until this scope gate exists.**

## A-1, A-2 and immediate interactions

**A-1 passes.** C §III.5 Prediction row, line 551, now names only `HypothesisId` for PD-010's registration witness refusal. An unadmitted Hypothesis cannot submit an eligible Prediction through that route. Strategy Decisions retain their Runner, admitted-version, closure, witness and per-event rules. The Strategy Decision section is unchanged from f77fe92. The correction creates no new Strategy Version Prediction rule.

**A-2 passes at design-package level.** C §III.7 Content, lines 978–987, requires the interval as grant content. PD-009's amendment at line 320 explicitly removes the one-day standing, requires a Principal-supplied value and identifies an omission as an incomplete grant. A blank `AU-RP-1` therefore cannot pass the grant's completeness requirements at the planned Apply 15 or support a BIND. Earlier bootstrap acts do not cure that missing content. The numerical value may remain unset in this design package, but the genesis sequence cannot be completed with the grant incomplete. This review selects no value.

The interval remains permission to request invalidation after elapsed time, not an Apply deadline or release guarantee. Settlement, terminal exclusivity, invalidation authority and post-Apply consumption are unchanged. Valid liabilities still settle after funding stops. T-H now delays the beyond-zero reversal leg until effective zero, then applies the opening quota gate. These corrections do not reopen the settled accounting, cutoff or binding choices or expand either research demonstration.

## Package standing and required reconciliation

The current blocked status remains accurate, but the documents do not yet describe the current revision and reason consistently:

- README's status and architecture's introduction and §8 still identify revision 11. Architecture's recovery row still describes F-1 as unresolved. Update these to revision 12 and this follow-up's result before packaging, preserving the user's prose.
- The manifest header identifies the working-tree revision 12 review copy, but its Constitution inclusion row still says revision 11. Add this report and the eventual decision and admission records. Its draft/CV1-pending label is accurate today.
- Proposed PD-011's top direction correctly selects narrow A-1, but §A-1's recommended alternative and its final decision table still ask to confirm the broader scope. The correction record's final table also incorrectly says the broader text remains in place. Mark those alternatives superseded or reconcile them to the recorded direction before presenting an admission text. Do not obtain accidental approval of the rejected broader scope.

These are required package and decision-record corrections, not additional investment-policy choices. No certification or selected-technology claim is introduced. The reuse rule and two-demonstration scope remain unchanged. The existing package's 222 relative Markdown links were checked before adding this report, with no missing file or heading targets. Final packaging still needs a check over the final contents.

The Downloads archive `new_speedway_review_copy_PRE-IMPLEMENTATION-DRAFT_CV1-ADMISSION-PENDING_20261019.zip` is **stale**. Its SHA-256 is `bab5fe5bda479b152260a8d21316da5385aaf48fb5e01b048088de7d7b9475a1`. Its embedded Constitution digest is `8462162f28cf0ed2eb11741a6496f4b00c20664c58db9ba45203fee72f044bf6`, different from the reviewed revision 12 digest above. Its label correctly calls it a draft review copy. It must be regenerated after admission from the approved packaging baseline, including this review and subsequent records. It was not modified or sent.

## Relationship to earlier reviews and next action

The original revision 10 whole-design audit and the revision 11 final review remain valid evidence for their reviewed bytes. This bounded report closes F-1's original cases and the A-1/A-2 attribution questions. It does not turn the earlier focused binding checks into whole-design closure. F-2's overbroad execution predicate prevents closing the remaining whole-design blocker. The earlier favorable findings on accounting, settlement, cutoff, reduction without a qualification floor and binding recovery stand.

Optional editorial work beyond the noted inconsistencies is not an admission condition. No new demonstration, technology evaluation or interval selection is requested by this review.

Before admission, limit the execution exception to qualifying `REDUCE` obligations and recheck the allowed 10-to-6 case alongside the ordinary-Decision counterexample. Reconcile the package and decision text, record the resulting digests, and obtain the Principal's decision and CV1 admission. Only then regenerate the prospect ZIP. This review changes no governed fact and declares `ΔO/ΔS/ΔA = 0/0/0`.

**Plain-English verdict: blocked. The Principal authority repair works, but the reduction exception still applies more broadly than the admitted decision allows.**
