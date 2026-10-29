# Adaptive Research Harness private first-cycle build

A constitutional harness for evolving investment hypotheses, strategies and
research agents.

This checkout contains the bounded Python 3.12/SQLite implementation authorized
by the [build approval](docs/decisions/first_research_cycle_build_approval_addendum_20261029.md).
The [approved specification manifest](docs/plans/research_cycle_reconciled_20261029/manifest.json)
is preserved. No governed startup has run. The [run packet](docs/builds/first_cycle_20261029/run_approval_packet.md)
records the built inventory and separate initialization gate.

## Build checks

No installation or third-party packages are required. From the repository root:

```sh
PYTHONPYCACHEPREFIX=/private/tmp/arh-pycache python3 -m compileall -q adaptive_research_harness acceptance isolation build_support tests
PYTHONPYCACHEPREFIX=/private/tmp/arh-pycache python3 -m unittest discover -s tests -t . -v
PYTHONPYCACHEPREFIX=/private/tmp/arh-pycache python3 -m acceptance --list
PYTHONPYCACHEPREFIX=/private/tmp/arh-pycache python3 -m adaptive_research_harness --help
```

The tests use labelled fabricated inputs to pure calculations, empty SQLite
stores, and operational receipts. They never invoke genesis or register grants.
Regenerating the inventory with `python3 build_support/freeze.py` changes the
candidate approval digest if covered bytes change; passing checks does not
approve a changed build.

## Code and commit boundaries

| Module | Responsibility |
| --- | --- |
| `encoding`, `contracts` | Strict canonical bytes, exact units/time, finite commands and Check criteria |
| `storage`, `schema.sql` | WAL/FULL SQLite carrier, immutable records, atomic event/command receipts and durable uniqueness |
| `model` | Rebuildable Applied History, grants, liabilities, reservation and binding projections |
| `rules`, `engine` | Evidence and Transition admission, Principal/P-1 decisions, Apply continuation and atomic refusal/invalidation |
| `dispatch`, `host` | One claim per attempt; no fresh-process redispatch of old attempts; exact-generation quiescence before uncertain replacement |
| `clock` | Explicit durable synthetic time, append-only clock receipts, rollback/outage refusal |
| `actors` | Actual researcher, Observation worker, successor proposal and funded Checker orchestration |
| `checkers/a`, `checkers/b` | Independently implemented startup and narrow scientific criteria; no shared admission/calculation predicates |
| `tools_a`, `tools_b`, `tool_worker` | Separate synthetic calculations, simulated charges and retained untrusted receipts |
| `transport`, `service`, `client`, `__main__` | Linux peer-UID ingress, fixed actor processes, instance locks, thin command CLI |
| `isolation` | Fixed UID/systemd installation templates, target fingerprint and trusted stop/cgroup supervisor |
| `acceptance` | Commands-only startup, 51 named schedules, 20 process-death schedules, two forced terminal orders and independent fresh reader |

Evidence owns reservation sequence, attempt, settlement, observation and binding
acts. Transition owns proposal, Check, decision, invalidation and Apply. SQLite
co-location does not combine their separate commits. Researcher funding uses
only the proposal's literal prospective Evidence reference and conditional
append. A collision strands that immutable proposal. Request UUIDs and dispatch
claims are operational receipts, never reservation identities or authority.

Ordinary commands are `reserve`, `attempt`, `settle`, `close`, `fence`,
`propose`, `check-commit`, `decide`, `policy-decide`, `apply`,
`invalidate-request`, `release`, `research-commit`, `observation-commit` and the
one-time `genesis`. The exact fields are in the
[command schema inventory](docs/builds/first_cycle_20261029/run_bundle/command_schemas.json).
Read commands include `get`, paged `history`, `state`, `budget`, `obligations`,
`inspect-request`, `clock`, `profile`, `closure` and Principal-only
`dispatch-status`. `recover` inspects obligations or requests only Apply-owned
continuation. It cannot act as a grantee or Checker. Mutations return COMMITTED
or REFUSED with exact ledger references; ingress/storage failures return ERROR
or disconnect. On an unknown outcome, retry identical canonical payload under
the original UUID or inspect that UUID; an Apply may report a partial BIND stage.
A fresh UUID is a new command subject to domain duplication checks.

`python3 -m adaptive_research_harness command OP --actor ID --request FILE`
sends framed JSON over the command socket. The actor field asserts consistency
with Linux peer credentials. It supplies no identity. The service never exposes
a raw append, SQL, executable-launch or `acting_as` route.

## Supported host and trust

The reference host is a disposable Ubuntu 24.04 LTS machine with Python 3.12,
local ext4 and systemd. Fixed identities and permissions are in
[generated accounts](isolation/generated/accounts.json). Root/operator, the
protected core, and pinned actor executables are trusted. Agents cannot write
the database, installed code, run approval or another identity's state. Tools
cannot open the governed command socket. Root can bypass these controls and
is outside the adversarial caller model. In-process Python objects provide no
security against a process owning the interpreter or storage.

The clock and A/B tools run in separate fixed units and UIDs. Actor workers run
under their registered design's UID. The privileged fixture driver selects
registered actions and bounded adversarial stimuli; it never supplies a
successful research proposal or Check result. Only AD-R1 executes the ordinary
research cycle; the other nine registered researchers remain dormant except
for authorized reservation witnesses. Their empirical computation refuses
CAPABILITY_UNSUPPORTED. Registering a successor conveys no grant or UID mapping.

No services are installed or started by build checks. After separate approval,
the operator copies the inventory-covered tree to `/opt/adaptive-research-harness`
owned by root, with no group/world-writable code. Collect the actual host
fingerprint using `isolation.host_fingerprint`, approve its digest, and install
root-owned `host-fingerprint.json` and `run-approval.json` in
`/etc/adaptive-research-harness/`. The permit must name the exact inventory,
Principal approval-record and host-fingerprint hashes, `allow_apply_zero=true`,
and `runtime_scope=all-listed-cases-and-death-points`. No permit is supplied.

The installer checks the gate and refuses UID/GID collisions. It creates fixed
accounts/units and starts nothing. The trusted operator then starts the
supervisor. The Principal fixture invokes `python3 -m acceptance --execute`.
The runtime runner also checks the gate before requesting any empty case or
Apply 0. Every case retains its stopped store and report. Units have no network,
no automatic restart, read-only installed code, and control-group termination.
The supervisor masks/stops units, cancels starts, verifies empty cgroups and
terminated generations, and discards channels before replacement. UNKNOWN
settlement does not itself establish quiescence or prove no execution occurred.

## Limits

This build supports narrow synthetic research and registration. It does not
execute Predictions, Outcomes, Evaluations, standing, Paper Book, real billing,
live trading, framework adapters or arbitrary constitutional/scientific prose.
A broad CV1 grant does not make unsupported operations executable. Checker-authored
successor registration through its own funding path is unsupported; a separately
funded independent Checker may review a direct Principal control proposal.
Provider diversity is never claimed. A1 applies only to the approved synthetic
scope; CV1 lineage, own-subject and separate-funding restrictions remain.

Simulated charges demonstrate accounting and controlled local dispatch. They
say nothing about enforcement of external provider invoices. Durable command
retry is not an exactly-once guarantee for external action. No public release
or license has been selected.
