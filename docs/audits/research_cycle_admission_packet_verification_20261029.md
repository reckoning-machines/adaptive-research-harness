# Research-Cycle Admission Packet — Document Verification

Status: **AUTHOR'S VERIFICATION RECORD; NOT AN INDEPENDENT AUDIT, ADMISSION,
RUNTIME TEST RESULT OR CERTIFICATION.**

Date: 2026-10-29. Subject: the [proposed consolidated approval](../decisions/first_research_cycle_admission_proposed_20261029.md)
and [complete setup packet](../plans/research_cycle_admission_20261029/README.md)
for Adaptive Research Harness. This record concerns documentation only.

## Scope and preservation

This assignment added ten files: the consolidated proposed approval, this
verification record, and eight files in
`docs/plans/research_cycle_admission_20261029/` (README, amendments, setup
specification, setup JSON, designs/methods JSON, Checker contract, host/protocol
contract and manifest). No preexisting file was changed in this turn.

At entry, 92 non-Git files were snapshotted by raw SHA-256, including the
earlier uncommitted rename, plans, presentation successors and `test.py`.
All 92 remain byte-identical. The earlier dirty working tree was preserved;
the whole working tree is not claimed clean. No files were staged or committed.
No runtime code, tests, dependencies, infrastructure or license were added.
No remote or public release action occurred.

CV1's actual bytes still hash to
`c56a9cf50a7e9efadad8f2f2be6605e82c758f18d4096ba07eaaf86a8f8b7a64`.
All existing decisions, admission records, historical audits and retained
historical names remain untouched. Proposed A1/A2 changes are stated in a
new proposed record, not applied to admitted text.

## Checks performed

| Check | Observed result |
| --- | --- |
| Existing-file comparison | All 92 entry-snapshot files unchanged |
| Manifest | All 15 covered file digests and byte lengths match; consolidated approval names the actual manifest digest |
| JSON content | Both data documents parse; 30 embedded content/SourceRevision/resolution-rule digests recompute under declared canonical encoding; no float quantities |
| Transitive artifacts | Setup's artifact-file hash matches; all design method/tool references and grant tool-spec hashes resolve to exact supplied content |
| Designs | Ten Research plus two Checker designs; ten declared research-question differences; one ordinary researcher enabled |
| Synthetic corpus | Independent document calculation yields n=12, k=8, n_large=2, k_large=2; this is a fixture-content check, not a run of either future tool |
| Numeric setup | Seven-day duration, five-minute interval, explicit UTC expiry/clock range, shared 600 and 100 caps, 60/30 Checker budgets and within-pool discovery 60 consistent across prose/data |
| Accounting examples | Six lawful 90-unit reservations leave 60; two competing 40-unit requests cannot both fit. Sixteen 0.25 startup Checks total 4.00; successful ordinary A+B cost 2.00, one further Check gives CK-A 4.25 total |
| Local Markdown references | All local links in the ten added files resolve; no new fragment links need anchor resolution |
| Whitespace | `git diff --check` clean for tracked edits; separate scan of every added file finds no trailing whitespace or whitespace-only lines |

The author also compared the setup with CV1 §III.2/.4/.5/.7/.8, Part V and
Part X, PD-009's appended PD-010 corrections, and the existing plan/acceptance
scope. No claim is made that hashing establishes semantic completeness or
that this author's review substitutes for independent acceptance evidence.

## Substantive conclusions and limits

The proposal fills the formerly open binding interval, grant contents,
sources, initial limits, design/method artifacts, exact serialization,
synthetic clock and host isolation arrangement. Runtime hashes/sequences/PIDs
are future measurements with specified derivation, not invented setup values.

Checker coverage includes funded startup and ordinary registration, criterion
results computed from committed inputs, own-subject routing, failures and
capability refusals. The proposal openly requires approval of the synthetic
exception to PD-009's additional provider-diversity supplement. It also
explicitly narrows initial enabled tools to local tier-1 calculations. Neither
is misrepresented as unchanged grant content or a constitutional amendment.

No core exists and no startup, Check, Apply, process death, isolation or billing
control has been demonstrated by this work. No provider diversity is claimed
for synthetic code. The source chronology creates no forward standing.
The forthcoming acceptance report must execute all original cases plus
S01–S08 and name durable records, actual builds and fresh process identities.

The remaining admission decision is the consolidated Principal approval,
including A1/A2 and bounded coding authority. No additional discretionary
setup value is requested from the Principal. A real implementation conflict
with admitted semantics/authority would still require a stop and a specific
decision; the packet does not waive that rule. Publication and licensing
remain undecided and outside the proposed coding scope.
