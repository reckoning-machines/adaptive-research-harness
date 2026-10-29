# Supported Host, Storage and Wire Contracts

Status: **PROPOSED IMPLEMENTATION SPECIFICATION — NOTHING PROVISIONED.**

These choices implement CV1's existing owners and commit boundaries. They do
not grant agents storage access or make a role string an identity. The
command/owner mapping in the [implementation plan](../first_research_cycle_implementation_20261029.md)
remains part of this packet.

## 1. One supported isolation arrangement

Use one **disposable local Linux VM, Ubuntu 24.04 LTS, Python 3.12 standard
library and its SQLite binding**, with local ext4 storage. No third-party
Python packages, provider SDK, container runtime, framework or remote service
is required. Record exact installed patch/build versions at execution; these
version families are a proposed support target, not a certification of an
untested build. Provisioning/verification scripts belong to the later coding
scope; nothing is provisioned now. If a local VM is unavailable, deliver its
fixture and mark isolation unexecuted until it runs there. macOS same-user
tests cannot establish this Linux isolation claim.

Use root-managed service units and distinct unprivileged OS users without
login shells, sudo, capabilities or shared writable home directories:

| UID | OS identity | Authenticated application attribution |
| --- | --- | --- |
| 20000 | harness-core | Trusted service hosting Evidence and Transition boundaries; internal Apply role |
| 20001 | harness-principal | Human-controlled Principal CLI/approved fixture instructions |
| 20002 | harness-observe | Observation function; still requires active AU-OBS-1 |
| 20003 | harness-clock | Synthetic clock backend; no governed command right |
| 20011, 20012 | harness-ck1, harness-ck2 | AD-CK-1.0/AU-CK-A and AD-CK-2.0/AU-CK-B |
| 20021–20030 | harness-r01 through harness-r10 | AD-R1.0 through AD-R10.0 under AU-RP-1 |
| 20101, 20102 | harness-tool-a, harness-tool-b | Receipt-only synthetic workers; no agent authority |

Reject provisioning if a chosen UID/name is occupied by another account.
Group `harness-clients` GID 20050 permits Principal, Observation, Checkers and
researchers to connect; membership grants no operation. Tool/clock users are
not members. Root-managed mapping binds peer UIDs to these principals;
runtime grants/design membership come from Applied History, never the map
alone. An executable successor requires an explicitly pinned operator mapping
update and a lawful grant; registration never changes the map by itself.

| Path | Owner/mode and purpose |
| --- | --- |
| `/opt/adaptive-research-harness/` | root; directories 0755, files 0644/0755; installed code and exact packet, unwritable by all service/worker users |
| `/etc/adaptive-research-harness/` | root 0755, files 0644; immutable-at-run role map/build inventory, no provider credentials |
| `/var/lib/adaptive-research-harness/` | harness-core 0700; database/WAL/SHM 0600; no client access |
| `/run/adaptive-research-harness/` | harness-core:harness-clients 0750; command socket 0660 |
| `/var/lib/adaptive-research-harness-clock/` | harness-clock 0700; durable clock state 0600 |
| `/var/lib/adaptive-research-harness-tool-a/`, `...-tool-b/` | respective tool user 0700; receipt files 0600, not governed authority |

Each service unit uses `NoNewPrivileges=yes`, empty capabilities, private
temporary directory, protected home directories and read-only system view,
with only its owned state/run path writable. Use private network namespaces
and allow only AF_UNIX. Disable cross-user ptrace and arbitrary executable
loading. Launch fixed installed programs, never a client-supplied command.
Root installs static units for each identity; core cannot setuid/sudo to
Principal or Checker. Checker computation runs in its own UID's separate
installed executable, never a callback within core.

Authenticate each Unix-stream connection with Linux `SO_PEERCRED`; derive
actor from peer UID. A JSON actor/name/UID is only a consistency assertion.
Tool sockets are separate and accessible only to core and the relevant tool:
per-tool groups GIDs 20101/20102, directories 0750 and sockets 0660 owned by
the tool. They accept calculation/receipt requests, no governed commands.
Clock socket uses GID 20053 (core, clock, Principal supervisor); backend
permits read only to core and advance only to UID 20001. Ordinary workers
cannot use the backend, delete clock state or obtain a privileged connection.

Trusted components are the human operator/root, kernel/filesystem, installed
boundaries, configured clock and build/configuration. Compromised root/core
can rewrite the database; this is not cryptographic protection against the
administrator. The tested OS arrangement prevents agent/tool users from
opening raw storage, editing code or impersonating other UIDs. Authentication
survives revocation so a former grantee may settle pending work; spending
rights do not. No external billing credentials exist. A later provider
integration must keep such credentials with an explicitly admitted trusted
dispatcher, never an agent.

This supports hostile requests and fixed synthetic workers, not arbitrary
hostile/generated Python, a network multi-tenant service or kernel compromise.
Same-UID embedded wrappers are for unit tests, not the enforcement deployment.
A future public Python client calls the protected service; handing an agent
a writable database connection defeats this trust boundary.

## 2. Durable storage and commit outcome

One SQLite database, one writer service, no direct client connections. Enable
`journal_mode=WAL`, `synchronous=FULL`, `foreign_keys=ON`, 5,000 ms busy timeout;
verify settings on open. Use explicit short `BEGIN IMMEDIATE` transactions.
Timeout is an operational response, never permission. No network filesystem,
asynchronous durability mode or external blob store. Store immutable artifact
bytes as BLOBs with digest in the same transaction that first references them.
Backups preserve the complete SQLite snapshot including committed WAL state.

Logical tables carry Evidence entries, Transition lifecycle, ordered Apply
membership, artifact bytes and request receipts. Separate sequences/owners
remain separate in one database. Projections/indexes are reproducible caches.
Schema versions select readers; migrations cannot rewrite governed content or
reinterpret a historical pinned version.

Evidence BIND, Transition Apply or atomic refusal+invalidation, and Evidence
RELEASE remain **three separately durable boundaries**, never one hidden
transaction. Apply/invalidation have a unique terminal disposition for the
exact bind. Consumption derives from Apply, without an Evidence completion
record. Cross-ledger admission reads occur against exact authoritative heads
under the writer transaction; failed reads refuse.

Each mutating command commits its request receipt and authoritative event(s)
atomically within its owning boundary. Receipts are RECEIPT, not a second
ledger; lookup validates cited events. A crash before reply yields UNKNOWN
until inspection. Same `(authenticated principal, request_id)` plus identical
request bytes returns the original durable outcome. Same key/different bytes
refuses REQUEST_KEY_CONFLICT. Operational failure with no transaction is not
a durable outcome and may be retried after inspection.

A new request key for a settled attempt records ALREADY_SETTLED; it cannot
charge again. Same-key replay is not a new decision at a newer head.
Multi-stage `apply` returns reached references and remaining obligations; a
lost reply after BIND requires inspection of both ledgers, not a receipt
claiming full success. Substage keys derive from parent request plus stage;
each receipt commits with that stage only. Continuation rechecks CV1.

Transport/authentication logs are not invented CV1 Transitions. Authenticated
domain refusals commit at their available owning boundary with actor/request/
reason. If unavailable, return UNAVAILABLE/UNKNOWN, never claim a durable
refusal. An operational log has no authority.

## 3. Exact JSON, quantities and references

Wire framing is four-byte unsigned big-endian length, then one UTF-8 JSON
object; maximum 32 MiB per frame. No compression, pickle, executable expression
or client-supplied filesystem path. History pagination defaults to 100 records,
maximum 1,000, with immutable as-of marks; never silently truncate a Check
closure. Oversized input receives a transport refusal, no partial command.

Canonical content uses UTF-8, object keys sorted by Unicode code point, no
insignificant whitespace, no terminal newline. Field names are ASCII; arrays
preserve order. Strings retain exact Unicode scalar values, no NFC/NFKC
normalization. Escape quote and backslash, use `\b`, `\f`, `\n`, `\r`, `\t`
for those controls, lowercase `\u00xx` for remaining U+0000–001F; emit other
scalars as UTF-8. Reject invalid UTF-8, unpaired surrogates, duplicate keys,
unknown schema fields and noncanonical numerical representations. Booleans
and null use JSON spelling. Integers are base ten, no leading zero/plus or
negative zero. No JSON floats, NaN or Infinity. For these validated values
this is Python `json.dumps` with `ensure_ascii=False, sort_keys=True,
separators=(',', ':')`.

SHA-256 is 64 lowercase hex digits. `content_sha256`/`SourceRevision` cover
only their sibling `content` object's canonical bytes, not their own metadata.
File hashes cover complete bytes including pretty formatting/final newline.
Raw source documents and artifacts are retained and hashed as raw bytes;
never canonicalize CV1 or a governed statement in place.

Simulated units are nonnegative decimal strings with exactly two fractional
digits, parsed as arbitrary-precision integer hundredths; never binary floats.
Negative actuals/refunds are unsupported. Otherwise-valid actual overrun is
counted in full, not clipped to a tariff. Scientific ratios are exact integer
numerator/positive denominator. Research units and capital are never coerced.
Times are validated `YYYY-MM-DDTHH:MM:SS.sssZ` Gregorian UTC, exactly
milliseconds, no leap second/local offset. Intervals are integer milliseconds.

IDs are case-sensitive exact ASCII strings; punctuation does not determine
lineage. Explicit lineage/predecessor fields govern. Sequence numbers are
nonnegative integers in their own ledger. An empty Evidence head is `E=null`,
not an invented event zero. Before Apply 0, `N=null`; afterward N=0 means the
real genesis. Paper coordinate is reasoned N/A, never a null hiding an
unreachable existing ledger. First Check has a real Evidence head after its
funded attempt. Resolve object ID and exact hash/version, never “latest”.

Proposals contain every CV1 field for their class, immutable referenced bytes,
base, authority, declared consumption and reservation where applicable. Expand
templates using the setup rules before proposal; English symbolic references
are not runtime Evidence references. References contain ledger, sequence,
subject/version and hash, all checked for agreement. Schema discriminators
represent existing record kinds, not new governed objects.

Proposal schemas distinguish candidate content from admitted content. A
well-formed candidate may explicitly supply null for an incomplete class
field, so the Checker can record the applicable known failure; a completed
Apply may not. No default fills it. Mandatory transport/identity/reference
fields, scalar types and unit syntax still validate at ingress. Schema
refusal is not fabricated as a Check. This preserves failed proposals
without permitting malformed wire data to acquire authority.

## 4. Commands and permissions

Use `adaptive-research-harness <command> --request <json-file>` for mutation
and equivalent typed Python-client calls. Replies carry request ID, status,
authenticated actor, exact committed references and relevant as-of heads.
Input files are transport, not grants/decisions until committed lawfully.

| Command | Mandatory semantic inputs | Result and authoritative boundary |
| --- | --- | --- |
| `genesis` | Materialized three-item bootstrap, packet/build hashes; Principal peer | Apply 0 or refusal; Transition |
| `reserve` | Grant/design, amount, purpose (Theme/empirical/discovery or named Transition/verification subject), expiry | Reservation and derived totals; Evidence |
| `attempt` | Reservation, full CV1 work identity/dispatch index, tool/version/input hashes, maximum/tier | Pending attempt before work; Evidence |
| `tool-run`, `tool-receipt` | Admitted attempt, exact tool/input closure | Untrusted result/failure/usage receipt; no governed write |
| `research-commit` | Design/grant, closure/question/result or failure, typed claims, dataset/tool/reproducibility binding, attempt | Immutable Research Record; Evidence |
| `observation-commit` | Active grant, source/revision/slot/member, bytes, extraction/listing status | Observation/feed record; Evidence, Observation peer only |
| `settle` | Pending attempt, actual units or UNKNOWN-at-maximum, receipt/provenance | One settlement; Evidence, original permitted grantee/former grantee or Principal |
| `close`, `fence` | Reservation or grant, reason | CLOSED by lawful grantee; FENCE by Principal only; Evidence |
| `propose` | Exact class content/base/authority/budget/reservation/artifacts | Immutable proposal; Transition |
| `check-run`, `check-commit` | Proposal/base and Checker grant/reservation; then full computed Check/attempt/closure | Funded computation then Check; independent Checker/Transition |
| `decide` | Proposal/Check/current base; Principal decision/reason or request to evaluate P-1 | Decision/refusal; Transition, Principal or internal P-1 only |
| `apply` | Decided Transition and expected decision/base/bind refs | Staged BIND then Apply/refusal/invalidation; existing Apply role and owning boundaries |
| `invalidate-request` | Exact bind, requester and proposed ground | Apply continuation verifies ground/current clock; terminal fact only if eligible |
| `recover` | Inspect-only default, optionally named obligation | Derived obligations then authorized existing commands; no override |
| `get`, `history`, `inspect-request`, `budget`, `clock` | Exact subject/version/request key and as-of marks | Exact records/derived views; clock is Evidence `(t,E)` receipt and commits nothing |

CV1's full reservation/work/dispatch attempt tuple remains identity; a run ID
cannot replace it. There is no client generic append, BIND, RELEASE, mutable
balance or population-update command. A caller can request continuation but
only the internal Apply role requests binding/release. These are proposed
internal-library commands, not publication authorization.

Principal and registered participants may query committed research history
in this fixture; reads confer no mutations. Tool workers receive only exact
input bytes/attempt metadata forwarded by core and have no query access.
Claimed approvals/grants in output remain untrusted bytes. Principal-only
fixture controls are inaccessible through agent commands.

The separate fixture CLI is Principal/operator-only: `clock-advance` takes
an absolute tick; `fixture-fault` takes a case ID, exact request/attempt and
one of AFTER_START_FAILURE, DROP_TOOL_RESPONSE, DROP_COMMAND_REPLY,
OVERRUN_601, or PAUSE_AT_BOUNDARY. Faults are one-shot, recorded in the run
report and never set Check/decision/Apply fields. PAUSE names a boundary from
the acceptance death matrix; the supervisor uses barriers and terminates the
real selected PID, then starts a new process with no old process memory.
The core's ordinary authority predicates remain enabled during every fault.
OVERRUN_601 is permitted only for R09, with explicit simulated-fault receipt
provenance. No arbitrary replacement output or SQL injection control exists.

## 5. Dispatch and synthetic clock

Core invokes fixed A/B sockets only after attempt commit. The worker verifies
tool/input hash and returns result/failure, input/result hash, simulated actual
and invocation receipt. It can durably retain receipts in its own directory;
these settle nothing. Authorized callers must commit the returned Evidence
and cost. Absence of a receipt never proves absence of dispatch.

Interrupted handoff defaults to uncertainty. Preserve pending maximum; recover
an exact receipt or settle UNKNOWN. If old work may have run, another
invocation needs a newly admitted dispatch index and funding. In an uninterrupted
process, a not-yet-sent admitted request can be sent once. Fresh recovery
resumes that dispatch only on durable proof it never happened; this milestone
may conservatively treat all ambiguous handoffs as uncertain instead. No
exactly-once external execution follows from command deduplication. Tool
journals are receipts, not new owners of spending/permissions.

Serialize dispatch requests for an attempt inside the running service. A
duplicate while in flight returns IN_PROGRESS; after an exact receipt it
returns that receipt, never a second invocation. Tool workers likewise
serialize the tuple and return an existing receipt without recomputation.
After either process dies, an incomplete dispatch handshake is uncertain;
absence of an in-memory lock or receipt must not reopen the old invocation.
These conservative rules prevent parallel client requests from spending one
admitted maximum twice without asserting exactly-once external execution.

The clock stores a durable millisecond tick initialized once to zero in an
empty clock directory. Principal supervisor may advance to a larger/equal
absolute tick in the configured range. Backward/out-of-range/malformed advances
refuse. Persist via temporary file, fsync, atomic rename and directory fsync
before reply. Crash recovery yields old or new valid tick, never a torn value.
Missing/corrupt state for an existing run is CLOCK_UNAVAILABLE: no reinitializing
or system-time fallback. Restart of all components preserves timeline and run
inventory or refuses continuation.

Evidence boundary serializes backend time read and Evidence-head read under
its admission/read lock, returning `(t,E)`. Evidence appends never advance time;
equal instants are legal and sequences still order commits. Clock can advance
independently; a receipt is an instant, not a lease. Every time-dependent
boundary action makes a fresh read, never trusts cached client time. For
elapsed invalidation Apply continuation records a verified Evidence-clock
receipt, interval and requester. Equality at five minutes fails the elapsed
ground; strictly later permits a race, not automatic release. Apply may still
win after that interval before invalidation commits.

This synthetic clock establishes no production wall-clock assurance. Fixed
simulated charges demonstrate local accounting/admission, not control of any
external provider's billing.
