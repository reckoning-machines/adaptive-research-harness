# Final Independent Design and Package Review — Constitution Revision 11

Status: **BLOCKED for Principal CV1 admission and final packaging. Audit evidence only.**

Date: 2026-10-19. Reviewer: Codex, reviewing Claude's consolidated design independently. No subordinate agents were used. These are document replays, not executed demonstrations or certification. This review authorizes no change to governing text.

## 1. Disposition and exact scope

Two operative conflicts remain. **F-1** leaves Principal-proposed Agent Design registration and interrupted Principal control acts without a consistent authority predicate. **F-2** admits residual-breach reductions in Part V while retaining unconditional composition and execution limit gates. Both need a narrowly scoped corrective decision and propagation before CV1 admission.

The core accounting, binding, settlement, cutoff and reversal repairs survive independent replay. The qualification-floor defect in the original reduction case is repaired. F-2 concerns the interaction of its additional residual-breach branch with other operative clauses. It does not withdraw the recommendation to permit independently checked, Principal-decided reduction without a qualification floor.

The prospect package at the reviewed commit also contained inaccurate ledger routes, overstated control descriptions and an unsupported commitment to build a simulator. During this review the Principal separately requested more natural, concise README and architecture prose, no semicolons, and a plain explanation of document-first work. Those two explanatory files were revised under that instruction. Their corrections are distinguished below from the unchanged governing design. A reviewer-authored explanation is not evidence that the underlying design has been repaired.

The repository's `AGENTS.md`, the [final handoff including §7](cv1_final_handoff_20261019.md), the operative Constitution, relevant admitted decisions, the original audit and both demonstration paths were examined. Prior focused reviews and the author's propagation and architecture checks were treated as supporting records, not closure. The scope includes the [whole-design checklist](cv1_whole_design_audit_checklist_20261019.md). Historical checklist references do not supersede later admitted rules.

| Baseline | Exact identity |
| --- | --- |
| Reviewed commit | `f77fe921c3672dd4d415196b1dddd124f4eac05b` |
| Constitution | Revision 11, draft, not admitted as `ConstitutionVersion 1` |
| Working tree at entry | Clean |
| Governing design | Unchanged by this review |
| Additional authorized work | README and architecture editorial and explanatory corrections only |

SHA-256 identifies the complete file bytes, not a rendering.

| File at f77fe92 | SHA-256 |
| --- | --- |
| `docs/doctrines/new_speedway_constitution.md` | `869601bfbba427536d179aa7a0f795645fd8a169251de5a0e12306753e943a72` |
| `docs/decisions/principal_decision_010_codex_audit_repairs.md` | `2c58d487fc72a5ec6b4db0f901fb17ff6773b5403abbe369ddbc1f6286d63279` |
| `architecture.md` | `ae63c0f22684a9cc70037af7736f2b448ca8f8fa884c92127528b667e0c0227e` |
| `README.md` | `e7f3ac772abd01aa7575e8d3eba02185b9fa5418d4d1daef3bca95c0ba9c06bc` |
| `docs/package/cv1_review_package_manifest.md` | `99c92496b7640f577c591522e544c27ec3cb3735d01c674fa94bf0b1a3f9e175` |
| `docs/reference/new_speedway_design_proposal_20261019.docx` | `15faec2112251b49564144df03558502c5d8792b85bb04b9bd9f6834c713a77b` |

The final explanatory files reviewed after the requested edits have these hashes:

| Working-tree file | SHA-256 |
| --- | --- |
| `README.md` | `bd1f1395852079faccf7b682d379abdc5a2a43fc38fa35baef598db30f82d098` |
| `architecture.md` | `7d486af05cfa58d333919850fe8f07212e26f04c4c5e57de6a657d0d7149a19c` |

References below use **C** for the [Constitution](../doctrines/new_speedway_constitution.md). Line numbers refer to the unchanged f77fe92 governing text. Audit and explanatory edits carry `ΔO/ΔS/ΔA = 0/0/0`. They grant no new authority.

## 2. Unresolved design findings

### F-1 — High, admission blocker: Principal authority is not carried consistently through Check and continuation

**Exact clauses.** C §III.8 Check record item 4, lines 1094–1107, permits direct Principal authority for an enumerated group of control acts. That list includes grants, limits, Constitutional Transitions, Theme registration and Allocation. It omits Agent Design registration. Part V's Agent Design Version registration row, line 1566, expressly permits the Principal to propose it. PD-009 §2 requires Principal-proposed registrations at sequences 3–12 and 13. PD-009 §3 requires no Research Authorization for the Principal.

C §III.8 Continuation, lines 1175–1195, separately requires, “for every class, the Authorization active” and no expiry of that Authorization. Unlike the repaired Check item, this continuation predicate has no direct-Principal-authority branch. The proposal need not have a funding Authorization at all.

**Smallest counterexamples.** First, after valid Applies 0–2, the Principal proposes the first research Agent Design at sequence 3. Part V permits the proposal, but the Check's closed enumeration does not permit direct authority for that class. A Checker cannot both demand a scoped Authorization and record that none is required. Second, the Checker passes the Principal's `AU-OBS-1` grant and the Principal decides it. The process dies immediately before Apply 1, with the head still at 0. Recovery must establish an active, unexpired Authorization that this control act does not have. An unchanged head cannot satisfy the missing predicate.

**Consequence and refusal.** The first independent Check is funded correctly, but the complete genesis and recovery paths are not coherent. The lawful response is to stop at the conflicting authority criterion. The documents do not specify a dedicated refusal code for this conflict. Inventing a Principal self-grant or silently treating the gate as inapplicable would supply an unadmitted rule.

**Minimum repair.** Make the authority predicate applicable to the actor and class at Check, Decide, Apply and continuation. Express direct Principal authority for every class Part V permits the Principal to propose, including Agent Design registration. Express which Authorization and budget tests are inapplicable to unmetered Principal acts. Preserve independent checking, the Checker's separate funding, and every applicable gate for funded or delegated proposals. No additional unchecked genesis act is needed.

**Decision boundary.** The underlying Principal rights are already stated in Part V and PD-009. This is a contradiction in their application, not a request to invent a new role. Under handoff §6, the correction still requires a new decision record, declared delta, Principal admission and propagation. This audit does not choose wording that changes rights.

### F-2 — High, admission blocker: residual-breach reduction conflicts with composition and execution gates

**Exact clauses.** C Part V Allocation, line 1562, permits `REDUCE` where every limit usage is non-increasing and there is no new instrument exposure. It expressly admits a smaller or equal residual breach when the existing breach cannot be eliminated in one step. The row also requires composition legality. C I-10, lines 1496–1500, unconditionally requires the resulting projection to satisfy every limit and invariant. C §III.10 Admission, lines 1374–1377, admits a Decision-set `REDUCING` order when the allocation is in force and “limits hold.” Its Limits clause, lines 1426–1432, refuses an order that would breach a limit. The reduction's required re-execution and visible residual are at lines 1419–1421.

**Smallest counterexample.** Take the existing-breach state that the new Allocation row expressly contemplates. A limit is 5, current exposure and target are 10, and a proposed reduction to 6 decreases every affected usage and adds no instrument. Part V admits the residual breach of 1. I-10 rejects the resulting projection. Even if the specific admitted REDUCE exception is taken to control at Apply, a sell of 4 leaves 6 against the same unchanged limit of 5. The ordinary Paper Book “limits hold” gate still cannot be satisfied. This example needs neither a moving limit nor a clock race and is distinct from U-8.

**Consequence and refusal.** An operator cannot determine one consistent admission result from all cited clauses. The unconditional reading refuses composition at Check or Apply and refuses the resulting order as `LIMIT`. A general exemption for reducing orders would be too broad, since a version-level reduction can increase portfolio net risk. A visible residual obligation records failure to execute but does not itself authorize the missing continuation.

**Minimum repair.** Reconcile the stated residual-breach policy with I-10 and the applicable Paper Book gates. Specify the bounded treatment of an existing breach without allowing a new or worsened risk. Alternatively, the Principal can expressly narrow or defer the residual-breach branch. Preserve the fill-level reducing bound, independent Check, Principal decision, stale-base refusal and ordinary expiry obligations. Replay both a partial reduction with a residual breach and reduction to zero.

**Decision boundary.** The original removal of the qualification floor remains justified. Choosing how the accepted residual-breach branch interacts with execution limits is a Principal policy clarification. The contradictory unconditional gates are a document defect. This finding does not authorize a new execution service, limit waiver or expanded prototype.

## 3. Original findings against the operative text

| Finding | Independent result at revision 11 |
| --- | --- |
| B-1, Checker funding | Resolved. C §III.5, §III.7 and Part V expressly cover Checker reservations, attempts and settlements. PD-009's amended initial grant names usable tools, tiers, estimation, cap, expiry and verification purposes |
| B-2, first Check | Partially resolved. Direct Principal authority and the `N/A` proposer budget line make Check 1 possible. F-1 prevents whole-chain closure |
| B-3, accounting | Resolved. `C = S + P`, open usage `max(A,C)`, closed usage `C`, grant headroom and lineage headroom prevent offsetting overruns or forgetting closed pending liabilities |
| B-4, final funding admission | Resolved at the document-contract level. C §III.5 and §III.8 serialize terminal disposition, require positive invalidation before release, and end the freeze on successful Apply without another completion record |
| B-5, cutoff and Outcome | Resolved. Observation receipt by each pinned cutoff controls inclusion, computation time does not. At most one canonical Outcome is admitted. Resolution grace belongs to each Source Declaration |
| B-6, method commitment | Resolved for the original cross-ledger failure. The registration commitment governs until a successor commitment precedes the event in Evidence order. Prediction admission witnesses registration. The propagation scope item below needs explicit attribution |
| B-7, cost route | Resolved. Part X §3 requires committed Market Observations before the Check. A vendor page or provenance attached only to a Check cannot qualify a cost model |
| B-8, reversal | Resolved in the operative §III.10 rules. Reducing fills are bounded at admission and the beyond-zero opening leg is derived only after zero. T-H remains an inconsistent illustration, addressed below |
| B-9, quota expiry | Resolved. Quota exhaustion refuses opening permission and does not create an expiry instant. `FLATTEN_ON_QUOTA` is removed |
| B-10, reduction floor | Original counterexample resolved. An allocation qualified with 20 effective Decisions can be reduced after the floor becomes 40. The residual-breach extension remains blocked by F-2 |
| C-1, stale summaries and examples | Substantially reconciled. Research accounting, T-A, T-B, T-C, T-F/T-G and continuity wording were corrected. T-H still describes deriving both reversal legs together, contrary to operative B-8 repair. This illustration needs reconciliation before packaging |
| C-2, sequences and rechecks | Resolved. Projection 0 is after genesis. Rechecks and redecisions preserve the original proposal and identify the effective base. Empty-ledger coordinates distinguish absent Paper Book from unreachable ledger |
| C-3, constants | Resolved. Hop depth remains explicit provisional grant content, decay count refers to ES-1 §6, and the checklist distinguishes policy constants from identities and example numbers |
| C-4, refusals and Checker proposals | Resolved. Known failed gates are `NOT MET`, constitutional indeterminacy is distinct, and Checker criterion-change proposals route to Principal constitutional decisions |
| C-5, classification and dispatch | Resolved. `CLASS PENDING` is not forward credit. Classification waits for the binding Outcome where needed. No response does not prove no dispatch, and an uncertain retry needs a fresh funded attempt |
| C-6, provider and storage | Resolved for the prototype. The registered provider/model binding is fixed. Hosting a ledger confers no independent decision right. D-14 remains open beyond that constraint |
| C-7, first Checker's own subject | Resolved as grant content. `AU-CK-A` excludes its own design and grant, with the second lineage routed to those subjects. F-1 still affects registering that second lineage |

**Accounting replay.** A 10-unit reservation with an actual of 20 has committed amount and usage 20, not 10. In a 100-unit grant it leaves 80 available once no other usage exists. A pending maximum of 10 settled at 6 returns 4 to an open reservation, or to grant headroom after closure. Two reservations of 50, followed by an actual of 60 in one, leave only 40 of grant headroom. A new attempt of 50 in the other is refused even though its local allowance is 50. An admitted maximum of 40 later settling at 45 produces total commitment 105 and `OVERSPENT`. Pending amounts under closed reservations continue to count against the lineage cap. No settled overrun is netted against another reservation's unused allowance.

**Cutoff and method replay.** With cutoff day 12, a qualifying observation received day 11 still resolves the Prediction if computation waits until day 20. A value first received day 13 cannot qualify even if no Outcome has yet been committed. A duplicate Outcome is refused. With registration at Apply 200 and Evidence head 20, an eligible event at Evidence 21 uses the registration commitment. The numbers 200 and 21 are never compared as one sequence. A successor Evidence commitment must precede its scored event in Evidence order. Synthetic observations and historical reconstructions do not acquire forward standing from timely computation.

## 4. Binding, settlement and recovery interactions

The following replay uses the operative clauses, not the proposal's case table as proof. `b` names one exact binding. Apply and invalidation compete at the same serialized Transition boundary. A freeze may persist during an outage, so terminal exclusivity does not imply guaranteed eventual completion.

| Case | Authoritative record, lawful continuation and refusal |
| --- | --- |
| BIND, then fence, then Apply | `b` establishes registration eligibility. FENCE closes the reservation and stops spending. Apply may consume `b` while the grant remains active and other Apply gates hold. Later attempts refuse `FENCED`. If revocation wins first, the inactive grant causes Apply refusal and atomic invalidation with ground `APPLY_REFUSED` |
| Early witness, pause, invalidation, release, delayed Apply | The durable invalidation of `b` decides. An earlier time read grants no terminal right. Evidence may release on the positive invalidation record. The delayed Apply refuses `BINDING_INVALIDATED` |
| Apply wins | The successful Apply citing `b` is consumption authority. Invalidation and repeat Apply refuse `ALREADY_APPLIED`. Release refuses `NO_INVALIDATION` |
| Invalidation wins | Every Apply using `b` refuses `BINDING_INVALIDATED`. Recovery may release once. Duplicate invalidation refuses `DUPLICATE` while the Transition remains unapplied, and duplicate release refuses `ALREADY_RELEASED` |
| Death immediately after successful Apply | The Apply record alone ends the freeze. No second Evidence completion or release is required. Recovery reads that record and does not repeat Apply |
| Death after invalidation and before release | The invalidation permanently excludes Apply. An authorized continuation caller can finish release. An unreachable required ledger yields `LEDGER_UNREACHABLE` or prevents the commit. Concurrent recoveries cannot release twice. No recovery process means no promised release time |
| Old binding resumes after a fresh binding | Old invalidation and release concern only the old identity. Old Apply refuses `BINDING_INVALIDATED`. A release of the fresh binding without its own invalidation refuses `NO_INVALIDATION`. The fresh eligible binding may independently win Apply once |
| Settlement after revocation, malformed and duplicate requests | Only a permitted caller's valid submission for the exact attempt still `PENDING` at commit changes accounting. A maximum of 10 settled at 7 replaces the pending 10 with actual 7 once. A duplicate refuses `ALREADY_SETTLED`. Wrong identity, units, amount, provenance or caller refuses `INVALID_SETTLEMENT` and changes nothing |

**Subsequent use after successful Apply.** The reservation's purpose becomes the admitted subject. The original grantee can use remaining allowance only if ordinary reservation, grant, cap, headroom, expiry and fence predicates pass. An unfenced, unexpired reservation can continue or close through the ordinary lifecycle. If expiry passed during the freeze, the next applicable commit reads it and closes the reservation. A prior fence leaves it closed. An overrun still prevents new attempts. Pending liabilities settle after any of these stops. Successful consumption does not create a successor grant, revive spending permission or require a duplicate completion authority.

**Invalidation authority.** `APPLY_REFUSED` carries the violated Apply condition and deciding evidence. `INTERVAL_ELAPSED` requires the continuation role, binding, declared interval and Evidence-clock receipt, checked by the boundary. The interval permits a request. It neither cancels automatically nor imposes an Apply deadline. A still-uninvalidated binding can win after the interval. No discretionary cancellation right follows from ledger write access. These rights are explicit in the operative text and declared delta.

## 5. Genesis and both demonstrations

### Genesis replay

| Stage | Result |
| --- | --- |
| Empty ledgers and Apply 0 | The bounded exception admits the exact CV1 text, initial Checker design with provenance and method commitment, and `AU-CK-A`. It does not waive future Checks |
| First independent Check | Principal first proposes `TR-1`. Checker reserves under its own 60-unit grant, records an attempt, performs the Check with proposer budget `N/A`, its own cost in item 5, and closure `(E, 0, N/A — no Paper Book)`. This is now fundable without an Observation tool grant |
| Decide and Apply 1 | The ordinary uninterrupted grant path is express. Death after Decide exposes F-1. Checker settlement remains independently valid after completion or interruption |
| Observation and limits | Apply 1 activates declared source permissions. Apply 2 sets limits. The Observation function alone commits source results. An absent Paper Book must not be confused with an unreachable one |
| Registrations 3–12 and second Checker 13–14 | F-1 affects the Principal's registration authority predicate. Conditional on correction, each design requires its own checked registration. The second lineage is established before own-subject changes to the first |
| Research grant 15 and Theme 16 | The 600-unit pool and 100-unit lineage cap include closed pending liabilities. A grant naming a pending Theme does not authorize Theme-bound reservations before that Theme is active |
| Ordinary operation from 17 | The redundant second admission of `P-1` is deleted. CV1 already contains the policy. No Runner or Execution Authorization is granted by this sequence |

Initial source declarations, immutable hashes and grant parameters still need their specified content before execution. This is ordinary genesis preparation, not permission to infer values or run genesis now. A provider's cap remains an accepted assumption only after the required provider-specific decision. The two demonstrations use the bounded synthetic provider and metered local tools.

### Proof 1 — evolutionary research

Conditional on correcting F-1, ten registered agents reserve from one serialized pool. Each backtest has a funded attempt and a Research Record identifying the exact dataset, cutoff, parameters, tool version and reproducibility binding. Failed and abandoned candidates remain visible. They do not become forward contradictions merely because a historical test failed.

A proposed Hypothesis registration identifies scope, resolution sources, selection basis, method commitment and purpose-matched reservation. The Checker can fail a restatement. A passing registration under `P-1` must still meet current base, policy and binding conditions. If another Transition wins the base, the loser is rechecked and redecided. A cached PASS cannot admit it.

A successor Agent Design can be registered without authority. Running it requires a Principal grant. A replacement grant requires the prior fence where prescribed and does not inherit its predecessor's budget or liabilities. A retirement of an admitted Hypothesis is a checked standing act, not an agent's abandonment note. At the lineage ceiling, new spending refuses. After a crash, liabilities remain. An uncertain dispatch needs a fresh attempt, and a valid settlement survives the funding stop. The demonstration establishes research control behavior, not alpha or forward fitness.

### Proof 2 — development, Theme and competing Hypotheses

Conditional on correcting F-1, the Observation function commits a declared feed and retrieved documents. A partial feed response proves no absence. Research records separate reported claims, interpretations and assumptions, citing exact committed bytes. Hops remain within the grant's domains, depth and budget. A new Theme requires its motivation closure, selection basis, Check and Principal decision.

The initial grant's Theme scope cannot silently expand to the new Theme. The Principal must supply an appropriate grant or checked amendment with the required fence before dependent research. Competing Hypotheses share a prior experiment design where required and keep motivation disjoint from resolution. Different IDs do not manufacture independent trials. Source extraction and resolution-grace declarations must exist before the relevant Predictions.

The proposed Strategy Version must be executable and reproducibly bound, with registration at zero capital. Its registration does not run a Strategy Runner or permit execution. Selection of the next research question is recorded under the applicable research scope with candidates, estimates or `UNESTIMATED`, and reasons. Synthetic Outcomes test the machinery without becoming market evidence. Neither demonstration needs an extra execution prototype, live venue, streaming feed or custom backtesting framework.

## 6. Propagation and delta attribution

The PD-010 rev4 proposal body is preserved. Reconstructing its original proposed-status header produces the reviewed SHA-256 `a47dad4069d06bbb469c300ef27361952b82193357edd1244d2edeecd2f723d2`. The admitted file has a new admission/status header. The handoff's claim that its digest differs by a prepended block alone is imprecise, but no proposal-body change was found. The four prior independent audits are unchanged between the propagation baseline and f77fe92.

The declared `ΔO +1` covers `BINDING`. The four authority additions cover Checker reservation, attempt and settlement rights, the funding-stop extension to Checker grants, the Apply caller extension on Evidence, and terminal invalidation with its bounded continuation request right. Reservation consumption, release, freezing and ordinary lifecycle resumption are explicit semantic changes. Existing write access is not used as a substitute for those declarations. Part VII keeps binding copies and clock receipts from becoming fallback authority.

Two propagation details need attribution before the final freeze:

- C §III.5's Prediction row, line 540, extends the registration witness refusal to `StrategyVersionId` as well as `HypothesisId`. PD-010 §3 B-6's exact replacement names `HypothesisId`, although decision choice 6 more broadly approves the Prediction witness read. The extension is consistent with requiring admitted subjects, but its broader scope should be confirmed in the corrective decision or brought back to the exact admitted scope. This is not an inferred new caller right.
- PD-009's amendment supplies a provisional one-day binding interval for `AU-RP-1`. The reviewed PD-010 requires an interval declaration but selects no value. Identify the one day as proposed future grant content or obtain its explicit Principal acceptance. It must not acquire admitted standing solely by appearing in a propagation note.

These are narrow attribution questions, distinct from the two operational contradictions. Neither calls for a new object or a broader redesign.

## 7. Architecture, reuse and package

### Explanatory corrections made under the subsequent user instruction

At f77fe92, architecture §4 sent `FENCE` and reproduction records to the Transition ledger. C §III.5 places both on Evidence. Its table also said the whole Transition ledger was written only by Apply, although proposals, Checks, decisions, refusals and invalidations precede or differ from successful Apply. The revised explanation distinguishes the ledger from its applied subsequence and corrects the routes.

The original controls table also described reduction as the Principal's decision “alone,” blurred BIND-time eligibility with funding at Apply, and implied expiry prevents residual exposure. The revised text retains the independent Check, distinguishes registration from spending permission, and explains persistent liquidation obligations without promising completion during an outage. It acknowledges the genesis exception and the unresolved F-1/F-2 conflicts rather than implying those paths already work.

The original D-14 discussion implied every provider update retires every agent. The prototype instead fixes the registered binding and stops unsupported substitution. A pinned model remaining available is not automatically retired by a vendor update. The original U-8 advice to change limits when no orders are in flight was not an admitted solution. It has been removed as a purported control. The runtime checkpoint explanation now states the actual rule: recovery must consult authoritative ledgers.

The original reuse table said “Nothing external” and “Build, minimal, deferred” for paper execution. PD-004's internal simulator rules exclude reliance on an external paper account but do not prove reusable fill computation unsuitable. PD-006 §PD-006.1 expressly includes paper fills among replaceable tools and permits custom infrastructure only against an unmet OSA requirement. The revised table leaves computation and technology choice open while retaining Speedway's responsibility for the governed Paper Book boundary. Its acceptance criteria are testable against the existing contracts. No product is selected and no product-capability claim is made.

The README and architecture now explain the design in concise investment-management language, with no semicolons. The reason for document-first work is stated directly: lower cost, faster iteration and debugging before implementation. Their status refers to this blocked review. No implementation, executed witness, certification or CV1 admission is claimed. The governing documents and prior author's checks remain unchanged.

### Package verification

The manifest's baseline inclusion resolves to 50 tracked files, comprising 49 Markdown files and the DOCX. The only excluded tracked file is the agent router. The governing documents, all decisions and cited admission texts, prior audits, plans, adoption record and reference materials are present. The adopted source provenance remains identified in the adoption record. This package is a document record, not a vendored implementation environment.

An independent check of the f77fe92 package found **220 relative Markdown links, no missing targets, no missing heading anchors and no targets outside the package**. Heading links were checked as well as file existence, excluding fenced examples. This verifies the historical package, not a promise about a later ZIP. New and changed files require a fresh check at the eventual packaging baseline.

After the requested explanatory edits, the same check over the proposed package plus this review found **212 relative links and no errors**. README and architecture contain no semicolons. A byte comparison against f77fe92 confirmed that every other tracked file, including all governing documents and prior audits, remains unchanged. Whitespace checks passed.

The DOCX archive passes its integrity check and contains three embedded figure files. Its visible cover and the text reference both name **Reckoning Machines**, **Brett and David**, and the discussion date **17 October 2026**. The different repository filing dates do not change those parties. The DOCX's creator is Reckoning Machines and its last-modified-by metadata is Vanessa Avery. That metadata does not establish a different Principal, recipient or admitted design author. The proposal remains reference material with historical research and pricing claims, not a current verified product recommendation.

The manifest correctly requires adding this final review. It also needs the subsequent corrective decision, follow-up review and CV1 admission when those exist. Its current “four independent audits” description is historical, not the complete count after this review. A final package cannot be labelled ready merely because the baseline links resolve.

### Nonblocking reconciliation and optional improvements

C Part VI T-H still derives sell 40 reducing and sell 30 opening together, while the operative rule derives the opening leg only after confirmed zero. Reconcile that illustration in the corrective propagation. The author's propagation check claims this example was updated, but it was not. Preserve that earlier check as historical evidence and record the correction separately. This does not reopen the sound fill-admission repair.

Other illustration polish, including making the later SV-5.4 allocation in Part VIII explicitly a later hypothetical state, can improve reading without blocking the two research demonstrations. A shorter glossary or additional diagrams are optional. None is a reason to expand prototype scope. D-14, U-1, U-8, real-provider cap acceptance and the later fill-rule grant remain the already-declared constraints, not newly demanded prototype features.

## 8. Exact actions before building the ZIP

1. Propose a narrow corrective decision for F-1 and F-2 with its own declared delta. Include an explicit disposition of the two propagation-attribution items. The Principal must accept any policy choice and admit the repair before governing text changes.
2. Propagate the admitted correction, including the stale T-H illustration. Preserve prior decisions and audits. Recheck the two failed traces, interrupted genesis, both research walks and the touched interactions against the new exact Constitution digest.
3. Obtain a readiness determination on that corrected baseline and the Principal's separate admission of `ConstitutionVersion 1`. This review is blocked and cannot serve as that admission or as certification.
4. Update the manifest and current explanatory status to include this review, corrective records, follow-up review and admission. Establish the approved committed packaging baseline under separate authorization. The manifest requires byte-for-byte committed content.
5. Recheck all relative file and heading links on that baseline, verify the DOCX and figures, and archive only the manifest's paths with the repository directory structure preserved.

No ZIP was built. No governing file or prior audit was modified. No implementation, genesis execution, certification, technology selection, commit or push was performed.
