# Complete Proposed Setup

Status: **PROPOSED — NO GENESIS EXECUTED, NO IMPLEMENTATION AUTHORIZED.**

This packet completes the [implementation plan](../first_research_cycle_implementation_20261029.md)
and [acceptance specification](../first_research_cycle_acceptance_20261029.md).
The original documents remain exact. Their unresolved-setup passages now
route conceptually to this proposal; approval of the consolidated record,
not this file's existence, closes them. CV1 and its admitted corrections
remain authoritative. This is one research cycle, not either complete PD-006
demonstration, a general Checker, or an investment evaluation system.

## 1. Exact content and precedence

`setup.json` supplies the proposed grants, sources, limits, clock values,
startup order and charges. `designs_and_methods.json` supplies the twelve
initial designs, four tool specifications, three method commitments, formation
corpus, future-source rule and ordinary Hypothesis template. Their `content`
objects are immutable proposed content; adjacent hashes cover canonical
content, not pretty-printed files. The [encoding contract](host_and_protocol.md)
defines the distinction. The approval manifest binds exact file bytes too.

The packet's technical specifications refine the older plan's illustrative
values. In particular Checker computation costs **0.25 units**, not its
illustrative one unit. No packet field overrides CV1. The only changed
admitted setup directions are the explicitly proposed [A1 grant supplement
and A2 tool-permission narrowing](amendments.md).
No current authoritative document or admitted byte is edited.

Some values cannot exist until execution: OS process IDs, installed source
hashes, commit sequences, clock receipts and exact evidence references.
They are measurements, not setup choices left to the coder. The following
rules fully determine their binding:

1. Build only the programs specified here. Freeze a build inventory before
   genesis containing every executable source file's raw SHA-256, Python and
   SQLite versions, OS/kernel/filesystem, role map and all packet hashes.
   Independently inspect the installed bytes against it. A program claiming
   a matching spec ID is insufficient. No executable hash is invented now.
2. Include that inventory's exact hash and each program's measured hash in
   the runtime design/provenance artifact and its proposal. Initial design
   specifications transitively pin this packet's Checker/host contracts by
   approval-manifest hash. The fully materialized runtime artifact has its
   own content hash; do not mislabel a specification hash as a binary hash.
3. A template reference such as “the formation DOCUMENT” expands to the
   unique exact successful command result in this store, including sequence,
   content hash and source revision. Missing, ambiguous or failed lookup
   refuses materialization. Resolve before proposing; never mutate a proposal
   after a Check. Store both template hash and materialized-content hash.
4. Runtime request IDs are caller-generated lowercase UUIDv4 strings. Proposed
   governed IDs are the stated strings for startup and the ordinary example;
   test successors use the deterministic suffixes specified below. A hash or
   request key does not replace a CV1 identity. Evidence and Apply sequences
   come solely from their respective commit boundaries.
5. Changes to installed code after genesis require ending that build's run
   with history preserved and starting a separately identified empty test
   store, or a lawful successor design/grant where supported. Reusing the
   same installed-design identity for different code is forbidden. A fresh
   process with the same build may continue the existing store.

This authorizes implementation of a specification after approval, not approval
of nonexistent implementation results. Runtime Check, Decide and Apply still
have to succeed. CPOC results and code review remain completion evidence.

## 2. Values, limits and reasons

| Field | Exact proposed value | Reason and consequence |
| --- | --- | --- |
| Clock epoch | 2026-10-29 00:00:00.000 UTC | A reproducible artificial timeline, explicitly unrelated to elapsed wall time |
| Binding interval | 300,000 milliseconds | Short enough to exercise waiting/recovery; five minutes is grant content, not a new deadline or constitutional default |
| Reservation expiry | Seven days from the boundary's witnessed reservation time | Retains PD-009's duration; never extends the grant |
| Grant expiry | 2027-04-30 00:00:00.000 UTC, exclusive | Supplies the missing time/zone conservatively; tests cover equality and later instants |
| Clock range | Epoch through 2027-05-01 00:00:00.000 UTC inclusive | Allows expiry and post-expiry settlement witnesses without resetting time |
| Research funding | Shared 600.00 units, aggregate per-lineage cap 100.00 | Retains admitted prototype values; no ten independent 100-unit accounts |
| Discovery funding | 60.00 within that 600.00, shared across grantees | Retains the discovery allowance without multiplying it by ten |
| Checker funding | AU-CK-A 60.00; AU-CK-B 30.00 | Separate from research; ample for funded startup and bounded witnesses |
| Simulated tool work | A/B 1.00 units through 1,024 rows, 2.00 through 4,096 | Computable maximum before dispatch; fixed simulated actual including a caught post-start failure |
| Checker computation | 0.25 per invocation, including caught post-start failure | Charges startup and ordinary verification alike; no free Check hidden in setup |
| Capital/limits | Every named capital/exposure limit 0.00; no Strategy Versions | Gives initial composition a determinate empty state; no allocation or Paper Book permitted |
| Worker activation | AD-R1.0 active; AD-R2.0–AD-R10.0 registered, normally idle | Preserves ten registrations without ten research loops; no inherited permissions |

The daily discovery cadence remains visible for every grantee, including
missing screens for idle workers. There is no “inactive therefore screened”
exception. Screens/hops are not executable metered tools in this slice;
retained PD-009 rates do not authorize dispatch. The example uses Theme
research after TH-G1 applies. It makes no claim of satisfying all discovery
coverage. Direct Principal attention and unmetered local fixture delivery
are not charged as model work; every declared metered invocation, including
Checker recomputation, requires its own admitted attempt.

Initial zero limits are evaluated from the empty admitted strategy/allocation
set. They are not a market risk model or an assertion about external holdings.
A later nonempty composition or nonzero capital request is outside capability
and cannot receive an initial-limits Check by this implementation.

## 3. Sources and methods

Both Source Declarations are complete proposed grant content. SourceRevision
hashes cover all declaration meaning fields. `SRC-E` retains daily real-equity
close meaning: the profile narrows the dormant archive to AAPL/XNAS official
unadjusted closes, first archived official print, session-end availability
bound, and 24-hour resolution grace. No archive exists in this packet, no
retrieval is scheduled, and no record claims that a real price was observed.
The explicit empty slot list is deliberate, not a missing setup field.

`SRC-SYN` enumerates one cohort per UTC date. Its exact corpus and generation
rule are committed as documents through the authorized Observation function.
A daily future cohort becomes available at period end; an absence slot is
one millisecond earlier and retrieval is one second later. The grace is ten
minutes. No retrieval at/after grant expiry is authorized. A missed slot is
reported missed; the runtime cannot backdate a clock receipt. Partial listing
and retrieval failure establish no absence. The entire source is synthetic:
even a correct release-time experiment never supplies forward standing.

The formation cohort is dated October 28; the first resolution cohort is
October 29, released October 30. They are different exact period/item members.
Formation bytes have twelve rows, eight selling rows and two large rows,
both selling. No field labels a proposal approved. A and B must calculate
the four counts from those rows, using different algorithms. Malformed input
or forced failure produces no successful count record. The independent
Checker must reproduce the calculation from the committed input, not copy
the tool's counts.

Method content declares research contribution, Checker contribution and the
Hypothesis's scoring, effective-sample, predictive-check, multiplicity,
falsifier and stopping rules. These are illustrative scientific choices
within the existing Standard, not changes to ES-1.0. A shared exposure can
collapse all this corpus to one effective cluster; no twelve-row sample is
reported as twelve independent forward Outcomes. There is no evaluator in
this milestone. Any future standing claim must pass the then-applicable
Standard and the committed methods on eligible evidence.

The ten designs have declared differences: five size thresholds in the Theme
path and five lookbacks in the dormant empirical path. Same-family variants
are not independent discoveries. Only AD-R1's threshold-two question is run
ordinarily. Both Checkers declare no model/provider/training cutoff, with an
explicit not-applicable reason. AD-CK-1 uses direct replay and arithmetic;
AD-CK-2 uses separate set-based reconstruction. Neither imports researcher
calculation or core admission predicate implementations.

## 4. Executable startup, without new waivers

| Apply sequence | Exact content | Funded Check and decision |
| --- | --- | --- |
| 0 | CV1, AD-CK-1.0, AU-CK-A only | Existing one-time waiver; Principal acts directly |
| 1 | AU-OBS-1 | CK-A checks already-proposed TR-1 at N=0; Principal decides |
| 2 | Zero limits | CK-A computes empty composition; Principal decides |
| 3–12 | AD-R1.0 through AD-R10.0, in order | CK-A checks each design, provenance, method and declared difference; Principal decides each |
| 13 | AD-CK-2.0 | CK-A checks separate lineage and implementation; Principal decides |
| 14 | AU-CK-B | CK-A checks grant; Principal decides |
| 15 | AU-RP-1 | CK-A checks all grantees/caps/scopes/tools; Principal decides |
| 16 | TH-G1 | CK-A checks formation closure, claims and selection; Principal decides |
| 17 onward | Ordinary research registration | Independent CK-A or eligible CK-B Check; P-1 only on its actual conditions, otherwise Principal or recorded refusal |

Before Apply 0 both ledgers are empty and the Evidence boundary can read its
clock. The three genesis artifacts are proposal content, not illegally
pre-seeded Evidence. The first Checker reserves 0.25 only after TR-1 exists,
pre-records its attempt, then computes. Its closure is `(E,0,N/A — no Paper
Book)`. Proposer authority is directly Principal and budget `N/A`; Checker
cost is never N/A. Each Check includes its own attempt. Successful startup
uses sixteen Checks costing 4.00 from AU-CK-A; AU-CK-B remains 30.00 unused.
Failure/retry costs are additional, never concealed in that expected total.

After Apply 1, advance the declared clock to 00:00:01 and commit the formation
feed retrieval and DOCUMENT through Observation commands. Their actual
sequences later bind TH-G1. Advancing time appends no Evidence by itself.
AU-RP-1 can name TH-G1 before its registration, as PD-009 orders, but no
Theme research proceeds until Apply 16. CV1 already contains P-1; there is
no extra policy-admission sequence. No other initial permission is seeded.

## 5. Preauthorized test acts and exact variation rules

The consolidated approval may authorize the Principal fixture client to
submit the exact startup content and the following bounded test variations.
It is an operator-controlled execution of those human instructions, not a
Research Agent empowered to decide Principal acts. Each runtime act still
uses the right class, Check, current-base decision and Apply. The fixture
cannot inject a Check result or bypass a failing condition.

Each acceptance scenario uses its own empty store and retained evidence
directory. Within a store there is one genesis. Test request/Transition IDs
are `TR-<case>-<ordinal>` (startup TR-0 through TR-16); successor IDs append
`-<case>-<ordinal>` to the predecessor ID and explicitly cite that predecessor.
Ordinals start at 1. The case is the existing R/B/T identifier or a startup
case S01–S08 below. IDs do not confer authority or erase lineage history.

Permitted positive control variations are: fence any initial Research/Checker
grant; revoke it through a checked successor; supersede it with identical or
narrower permissions/caps, no expiry extension and no new provider; and
register a declared successor of a supplied design with the same tools and
method, an instruction to retain negative evidence in deterministic sorted
question order, and no requested grant. A revoked successor has no active
permissions, retains predecessor attribution, and is never a fresh budget.
Successor design registration alone cannot run it. All tests declaring
metered registration consume the named existing-grantee reservation; Principal
control acts declare no metered proposer consumption. Both forms must be tested.

These controls cover staleness and own-subject checks without inventing a
free-form Principal authorization API for agents. Agent grants, sources,
methods or limits outside these variations require a new Principal direction.
Negative payload mutations may be submitted for rejection tests; this
approval never authorizes their invalid effects.

For R02, lawfully reserve 90 units for each of six distinct research grantees
under the common discovery scope, but **not** its 60-unit subgrant: use each
grantee's declared Theme/empirical scope and no tool dispatch. This leaves
60 pool units. Race a 40-unit reservation from each of AD-R7 and AD-R8 in
SF-G1. Each fits its cap; only one fits the remaining shared pool. Read-only
inspection confirms the winning order. Worker activation for this bounded
witness is authorized; ordinary research still uses only AD-R1. No missing
SRC-E archive is accessed to reserve a budget for an admitted empirical scope.

R09 injects an anomalous tool receipt reporting actual **601.00** against a
1.00 maximum under AU-RP-1. It tests truthful overrun accounting, not the
bounded tool's normal tariff. Preserve the injected-fault provenance; refuse
fresh work under the resulting overspend. Never claim this proves an external
billing cap. R06 failure charges 1.00 after start. R07 UNKNOWN settles exactly
the admitted maximum, not zero. All these use separate stores.

## 6. Ordinary worked cycle and completion

AD-R1 asks whether large synthetic volatility events warrant a narrower
selling hypothesis. Reserve 3.00, admit A's attempt at maximum 1.00, compute
12/8/2/2, commit exact negative-or-positive Research Evidence and settle 1.00.
Close the unused 2.00. Registering the supplied future hypothesis declares
2.00 and gets a separate reservation naming that proposed Transition.
The Checker spends 0.25 of its own grant, recomputes and records every
criterion. P-1 decides only on a lawful PASS. Bind, kill the service, and
recover in a new process; Apply or the required refusal/invalidation follows
the actual head and permissions. Close unused registration allowance only
when lawful. Run B under a new 1.00 reservation/attempt; preserve both results.

Expected successful ordinary research settlement is **2.00 total** (A+B),
not the sum of every reserved amount. Successful startup plus the ordinary
Check settles **4.25** for CK-A. Registration reserve has zero metered actual
unless a separately admitted attempt consumes it. These are expected sums
for verification, never imported balances. A fault branch retains all
charges and refusals. No branch creates supported standing.

Next permitted action is a further funded research request or inspection;
Prediction/Outcome execution, Paper Book and adapters remain excluded.
Completion requires every case in the original acceptance specification plus
S01–S08 in the [Checker contract](checker_contract.md), actual fresh-process
recovery and OS isolation evidence. A successful scripted narrative or
document check does not satisfy completion.
