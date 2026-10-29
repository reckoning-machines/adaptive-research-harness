# First-Cycle Reconciliation — Exact Implementation Corrections

Status: **PROPOSED; BUILD AND RUN AUTHORIZATION REMAIN SEPARATE.**

These corrections refine the current implementation plan and the previously
supplied setup packet. They replace only the conflicting provisions identified
below. All ten designs, numerical grants, sources, method specifications,
synthetic tariffs, canonical encoding and Linux account assignments remain.
The [decision record](../../decisions/first_research_cycle_build_decision_proposed_20261029.md)
contains only remaining decisions D1–D3. No admitted record is edited.

## Build versus initialize

The earlier packet's automatic materialization-and-run permission is withdrawn.
Build approval authorizes implementing the complete bounded code and preparing
fixtures, packaging, static checks and unit/component tests that do not invoke
genesis or establish governed actors/grants. Fabricated state in a pure function
test is labelled test input and never reported as lawful initialization.
Build approval does not grant a running agent any Authorization.

After building, freeze an exact **run inventory** containing: source-tree
commit and dirty-file digests; every installed Python/executable byte hash;
transitive module/import inventory for both Checkers, researcher and tools;
materialized design content/hashes with actual executable provenance; tools,
methods, CV1/ES-1.0 and grant/source/config hashes; database schema hash and
SQLite/Python/OS/filesystem versions; role map, service units, permissions and
clock state-format hash; command schemas; startup and fault-schedule versions;
intended disposable host/run directories; and the precise acceptance cases.
Resolve no runtime evidence sequences in advance: source and proposal closures
still acquire exact references through lawful commands after run approval.

The Principal separately approves that exact run-inventory digest before the
first Apply 0, **including a disposable acceptance store**. That approval
covers only the frozen build/configuration and enumerated runtime Principal
fixture acts. Later rebuilding any executable changes the inventory and needs
new run approval before initialization/continued use; a fresh process running
unchanged approved bytes needs no new approval. Tests passing cannot authorize
changed artifacts. This is an artifact gate within the coding assignment,
not another general design review. No build or run is authorized now.

## Reservation reference ordering

**Recommended D2 construction, subject to explicit Principal confirmation.**
A reservation remains an Evidence record identified by its committed sequence.
There is no client `ReservationId`, no preallocated authoritative slot and no
purpose-only lookup that can replace the proposal's funding reference.

1. The actual researcher program reads the Evidence head and next-sequence
   convention (first event is 1; an empty head is null). Let the prospective
   numeric reference be `r = current last sequence + 1`, or 1 when empty.
   This read is only a prediction of a reference, grants no rights and locks
   no budget. A signed/granted identity is not created by calculating r.
2. It constructs and commits immutable proposal T naming `(Evidence,r)` as
   funding reference, its grant/actor, declared budget and unchanged subject
   artifact. The proposal can exist unfunded. It never claims r already exists.
3. Acting under its own grant, the same researcher requests a RESERVATION
   with purpose **exactly T**, amount/expiry, and transport precondition
   `expected_sequence=r`. Under the Evidence write transaction, append only
   if r is still the next sequence and ordinary CV1 eligibility holds.
   The prior proposal commit is durable; no combined cross-owner commit is
   invented. A conditional append failure preserves refusal at the available
   boundary and creates no reservation at some substitute sequence.
4. The independent Check reads the exact record at r and verifies its kind,
   actor, grant, purpose T, amount, scope, open/unfenced standing and closure.
   An absent record, another event, another Transition's reservation or a
   correctly purposed reservation at another sequence cannot satisfy T.
5. If another commit takes r, the proposal stays immutable and unusable for
   that funding. Preserve it and the refusal. The researcher may construct
   a **new TransitionId** for the same still-unadmitted candidate with a new
   prospective reference, explicitly citing the abandoned proposal; this is
   not a new admitted subject or permission to reset family/search history.
   No funding amendment, hidden pointer update or restatement credit occurs.
6. On a lost reservation response, inspect the original command key and exact
   r. Same-key retry resolves that command's outcome. No new reservation is
   inferred from an absent receipt or matched by purpose alone. A later grant
   change or fence may independently defeat the pending proposal.

Two concurrent proposals may predict the same r; at most one matching
reservation can commit there. The other fails closed. A crash after proposal
and an intervening Observation can strand it. This intentionally trades
liveness for a literal immutable reference using existing CV1 identity.
There is no reservation-row preallocation and no promise of gap-free progress.

CV1 §III.5 requires an already-proposed Transition; P-1(b) requires a named
reservation committed before Check. Neither explicitly bans a prospective
sequence reference. This construction satisfies both orders while retaining
literal sequence identity; it is the proposed resolution of that ambiguity,
**not a claim that the ambiguity was already decided**. D2 approval confirms
this construction, not a client-ID or purpose-only remedy. No new ontology,
reference equivalence, owner or lifecycle is proposed. If an implementation
cannot enforce it without changing those meanings, it must stop.

## Executable actors and complete Checker coverage

The ten registered Research designs are executable deterministic programs
(or separately hashed entry points/configurations in one immutable module
bundle), not ten role labels. Each version's executable closure includes its
instructions, tool bindings, method and profile. Only AD-R1 runs the ordinary
cycle. Other designs can remain dormant or perform authorized reservation
witnesses; dormant empirical computation returns CAPABILITY_UNSUPPORTED rather
than inventing market observations. Their actual program hashes still belong
in the separate run approval.

AD-R1 reads the committed formation DOCUMENT, TH-G1 and its current grant;
reserves and invokes the selected tool through the boundaries; validates the
receipt and commits its own typed Research Record and settlement; reads that
record back; and **derives** the Hypothesis proposal using the fixed template,
computed counts, exact closure/methods and future disjoint resolution member.
A successful, internally consistent result motivates the proposal; a tool
failure, missing input, wrong count/hash, missing Theme or inability to form
the declared question produces negative evidence/no proposal. It supplies
no PASS/decision/Apply field. The test driver may choose A or B, set an approved
fault and ask the program to advance; it may not construct a proposal and
submit it using the researcher's identity. Test mutation requests remain
explicit adversarial inputs, never attributed as successful researcher output.

Research cost stays with that design/lineage and original grant. Installing a
successor requires its registered bytes and an explicit new grant before it
can run; registration never moves OS identity or transfers reservations.
Observation runs as UID 20002 under AU-OBS-1 and commits the formation corpus
after Apply 1, before TR-16. Core may not impersonate it during recovery.

The existing packet's Checker contract §3 already covers all startup classes,
initial limits, grants, ten designs, second Checker, Theme and ordinary
Hypothesis registration. Keep its independent computation and S01–S08; update
its operational references to these corrections. Each Checker reads committed
input bytes and recomputes criteria in separate code, importing neither A/B,
the other Checker nor core admission predicate implementations. Checking A
only with B is not the chosen remedy: both could share the research defect,
and neither tool evaluates grants/limits/authority. Shared schemas/encoding
are allowed; shared scientific/admission predicates are not.

Add the bounded **Principal P-1 suspension** control expressly authorized by
CV1 Part V (lines 1670–1673): exact payload `policy=P-1`,
`scope=AU-RP-1`, `action=SUSPEND`, with reason and direct Principal authority.
Represent it as a Constitutional control Transition exercising that existing
right, not editing CV1 text or admitting a new policy. Checker observes the
named policy/grant, direct authority, current base, exact scope and absence
of unrelated mutations; proposer budget N/A, Checker budget funded. Decision
and Apply are Principal-only and affect subsequent P-1 decisions/Apply.
No free-form constitutional text or reinstatement interpreter is implemented.
The profile's preauthorized test variations include this one control for B12.

Only the Apply boundary/its continuation emits a P-1 decision event. An
ordinary caller requests evaluation, never supplies an authoritative decider
or approval. All P-1 predicates are evaluated at the current head, and again
at Apply; its event identifies the admitting Constitutional Transition and
exact Check. A prior policy decision is not a lease through suspension.

## Durable command retries and external dispatch

Keep the latest packet's durable unique `(actor, request_id)` plus exact
request-byte digest in the event transaction. Same-key same-bytes returns
that committed receipt; conflicting bytes refuse. A differently keyed duplicate
reaches CV1's domain predicate and records the appropriate refusal. Do not
replace request keys with “one Research Record per attempt”: CV1 permits
multiple evidence kinds and claims about the same work. A receipt/index can
be rebuilt from owning events; it never votes for a missing authoritative fact.

A single process-lifetime, nonblocking exclusive `flock` on
`/run/adaptive-research-harness/writer.lock` is required before opening command
sockets or dispatching. Keep the descriptor unpassed to children; never unlink
or replace the lock inode during a run. A competing core instance fails startup,
including while the first is merely paused. Kernel release after process death
is the mechanism, not elapsed time or a PID-file assertion. This is a
single-host implementation constraint, not a new owner of governed state.
SQLite durable uniqueness remains mandatory even with the process lock.

Every admitted attempt can acquire at most one **dispatch-claim RECEIPT**
using a unique constraint on the full attempt tuple. Commit it after attempt
admission and before handoff, naming request key, fixed tool, input hash and
service/worker generation. It establishes only that dispatch may have occurred;
it never admits work, settles cost or proves execution. Concurrent requests
cannot both obtain a claim. A duplicate returns in-progress or the retained
receipt and never sends another invocation. A claim surviving a crash is
uncertain; its absence is never used as proof of non-dispatch during recovery.
This is operational receipt metadata, not a new Evidence kind or standing.

Tool units have separate UIDs and their own lifetime instance locks. Core
connects to those fixed units; there is no setuid tool subprocess or arbitrary
program launch. A tool serializes each attempt/claim and may return its exact
retained receipt. Its receipt files are untrusted inputs until lawfully
committed. They supply no new caller, budget or permission. Retain this narrow
receipt lookup already specified in the packet; dropping it is optional
simplification, not a correctness remedy required for this cycle.

## Recovery and worker quiescence

Core recovery may inspect and perform only its own Apply/BIND/invalidation/
RELEASE continuation. A Principal settlement request comes from Principal
peer ingress. A grantee's reserve/attempt/result/settlement/close/proposal and
Checker work come from that actual registered executable under its own peer
identity. There is no `acting_as` or recovery-role override. The former-grantee
settlement exception does not grant the core former-grantee credentials.

For the same interrupted research/checking work, replacement dispatch waits
until the trusted operator supervisor establishes that the **original service
and worker generation cannot still dispatch**, including their queued IPC
and descendants. In the supported host this means stopping the relevant
root-managed units with control-group termination, observing their cgroups
empty and exact process generations terminated, and closing/discarding old
input channels before launching new generations. A worker that can spawn
outside its unit is outside the supported arrangement. Root remains trusted.

The supervisor's attributable receipt names run inventory, unit/cgroup,
boot ID, PID/start-time generation, stopped descendants and closed channel
identities. It is host evidence for the dispatch controller, not authorization
to append a ledger fact. The service validates that the receipt concerns the
old dispatch generation; it cannot accept a caller's Boolean `dead=true`.
If the supervisor is unavailable or any old unit/queue remains capable of
handoff, replacement dispatch refuses WORKER_NOT_QUIESCENT. No TTL, missing
receipt, cancellation request or fresh process name satisfies this check.

Quiescence proves **no future dispatch from the old generation**, not that
nothing ran. Fresh recovery never resumes the old attempt's dispatch in this
milestone, even if its claim is absent. It retains maximum liability and
recovers an exact receipt or records UNKNOWN at the admitted maximum through
the permitted settlement caller. Only then may an independently admitted,
new dispatch-index attempt rerun the work. A post-fence retry still refuses.
A known, uninterrupted, not-yet-sent admitted attempt may dispatch once even
after a fence, as CV1 permits; that is not the fresh-recovery retry branch.

Settlement/inspection do not require quiescence: valid liabilities can always
be settled under CV1's permitted callers. UNKNOWN settlement itself does not
assert that a still-running worker was stopped. No cleanup process erases a
late receipt or final-settlement conflict. Test-driver memory is never proof.
This conservative supported dispatch policy grants no additional CV1 right;
it intentionally provides no liveness guarantee while an old worker can act.

## Clock, expiry and attempt bytes

Use the existing durable synthetic clock and initial values. Readback must
be nondecreasing against both its durable tick and the greatest time in any
durable ledger/clock receipt. Missing/rolled-back state fails closed; never
reset to epoch or use local wall time. The high-water comparison is derived
from those receipts, not a competing clock. Equal instants are lawful.

| Operation | Fresh Evidence-clock requirement |
| --- | --- |
| Reservation | Yes. Omitted expiry becomes t + grant's seven-day duration. A supplied expiry must satisfy t < expiry <= t + duration; grant expiry independently gates new work |
| Attempt | Yes, for grant/reservation eligibility and pending liability admission |
| BIND | Yes, for funding eligibility and the recorded binding instant |
| Checker closure, P-1 decision/Apply, other expiry-dependent admission | Yes; no cached time or expired authority |
| CLOSED, elapsed invalidation, RELEASE/current expiry projection | Yes for time-dependent standing; frozen reservations never expire implicitly; release cannot revive an expired/fenced grant |
| Valid pending settlement | **No.** Its sequence, identity, units, provenance and permitted original caller/Principal are sufficient; make no fresh expiry/closure assertion |
| FENCE | No fresh time needed to establish Principal's sequence-ordered funding stop; it closes by fence, not by an expiry inference |
| Historical exact read/inspection | No time needed for bytes; present eligibility remains unknown without a current read |

Settlement on a clock outage replaces pending maximum with actual once and
retains every known fence/revocation/binding fact. It neither declares expiry
nor frees a frozen binding. A later time-dependent operation reads the clock
and evaluates closure. CV1 §III.5 gives settlement no expiry eligibility
predicate and no mandatory commitment-time field; §III.5's clock rule forbids
inventing one. This is not a new “ignore clock” exception for spending.

An attempt's `step` is a fixed token from its registered executable's step
catalog: `research-counts`, `replacement-counts`, `check-transition`, or
`verification-candidate`; its stable meaning is recorded in that design.
The input hash covers canonical bytes of `{schema_version, tool_id,
tool_spec_hash, executable_hash, step, parameters, input_refs}`. `input_refs`
is an ordered array of exact ledger/sequence/content-hash references and raw
payload hashes; parameters includes the fixed calculation thresholds and
relevant proposed Transition/hash for a Check. It excludes request ID,
dispatch index, attempt/ref receipt time and any expected outcome. Raw document
bytes are separately retained and verified against those hashes before use.
A/B therefore have distinct invocation hashes even for the same dataset.
The tool result's `input_sha256` means the raw canonical cohort DOCUMENT hash;
the attempt's `input_hash` means the complete invocation hash just defined.
Keep both explicit rather than comparing these different byte scopes.

Dispatch index starts at 0 and increments for a new invocation of the same
reservation/step/input-hash tuple. Duplicate identity refuses; new input does
not rewrite an old attempt. The replacement/quiescence guard covers the
interrupted work's originating step and input closure across tool selection,
not merely equality of the full input hash. Research Records include exact
snapshot identity/hash, source cutoff, all parameters, version/hash and a
reproducibility binding `(raw input hashes, invocation hash, expected result
hash)`. “Expected” here is the actual committed result to reproduce, never a
fixture approval label. Failed runs carry no fabricated successful result hash.
Checks retain “authored knowing the period”; synthetic data never earns standing.

## Trust claims and retained startup

R01, R12, R13's caller route, T06/T07 and former-grantee attribution in R04
require the Linux peer/UID/process boundary. Ledger/accounting parts of those
cases can be unit tested cooperatively, but their isolation claim cannot.
Other accounting/race predicates can be tested in cooperative mode with
explicitly assumed identity; final acceptance still uses the approved host.
A sealed ingress-only caller type prevents accidental in-process misuse;
Python access restrictions are not security against a process that owns the
interpreter/database. No same-UID library embedding claim is added.

Retain seventeen Applies, sixteen funded Checks, ten Research designs,
SRC-E dormant and the second Checker. CV1's three-item genesis alone could
support a smaller deployment, but the CV1 admission's explicit ten-design
inputs and the Principal's latest direction retain this setup. The eight-Apply
alternative would need a new scope decision and a separate answer for the
existing distinct-grantee pooled-budget witness. No reduction is requested
in the remaining approval packet. Both Checkers are exercised by S06 and
B12/own-subject tests; CK-B is not merely a decorative registration.
