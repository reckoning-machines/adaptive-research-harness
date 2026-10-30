# Runbook

How to run the Adaptive Research Harness first cycle on one machine. What
each command does, where its output goes, and what it does not cover.
[BUILD.md](BUILD.md) describes the implementation; this file is only the
operating procedure.

## Requirements

- Python 3.12 from a standard distribution. The harness uses only the
  standard library and SQLite; nothing is installed.
- macOS or Linux. The commands below run on the development machine without
  any virtual machine.
- Run every command from the repository root.

Set `PYTHONDONTWRITEBYTECODE=1` on each command so that no bytecode is
written next to the covered source. The examples below include it.

## Run the example cycle

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m acceptance.local --example
```

This creates a disposable SQLite store, runs the seventeen-step startup
through the public commands with computed Checks, lets researcher AD-R1 form
a hypothesis from synthetic data, has an independent Checker recompute it,
registers it through policy P-1 and Apply, repeats the calculation with tool
B, and runs one diagnostic experiment whose negative result is preserved. It
prints the question, the counts, the simulated cost, the evidence references
and the next permitted action. Nothing outside the machine is contacted.

## Run the workbench

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m workbench --port 8765
```

Then open `http://127.0.0.1:8765/` in a browser on the same machine. The
server binds to loopback only. Choose a cohort and press Start. Starting
freezes a bundle, starts the core and tool workers as processes and runs
the startup sequence, which takes a few seconds. The page then offers one
button at a time, naming the actor and operation it will perform. Each
press runs one existing actor operation or Principal command; the core
decides whether it is permitted. Click a stage card to see the record it
rests on. Accounting, refusals, the independent reader and raw records are
behind the expandable sections at the bottom.

Close run stops the processes and leaves the state in place. Opening a
listed run starts fresh processes against that state and continues from
the next permitted step when every file in the run's inventory still
matches the tree. Otherwise it opens read-only, labelled so, and nothing
can be continued. Ctrl-C in the terminal closes every live run.

The three cohorts are declared in `workbench/cohorts.json`. The original
equals the admitted formation cohort. The other two are second Observations
of the same synthetic item with different rows; each carries its own name,
its edits and the formation content hash inside the document, and the page
lists every observation on the ledger with its variant and content hash.

The same cycle runs headless, and is what the retained demo runs under
`artifacts/development/workbench/` came from:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m workbench --demo
```

## Run the test suites

Unit, component and workbench tests. The workbench tests start real core,
tool and actor processes and take about a minute:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -v
```

Cooperative acceptance cases, including the process-death schedules:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m acceptance.local --jobs 4
```

List the catalog without running anything:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m acceptance --list
```

Static checks, inventory verification and CLI help:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m compileall -q adaptive_research_harness acceptance build_support tests
PYTHONDONTWRITEBYTECODE=1 python3 build_support/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m adaptive_research_harness --help
```

## Where output goes

Each acceptance invocation writes under `artifacts/development/`:

- `builds/<digest>/` holds the code inventory, the build metadata and a
  complete snapshot of the covered source for that run. The digest names
  the source bytes only; working-tree status and the build environment are
  in `build_metadata.json` beside it, outside the digest. Changing source
  during a run fails verification.
- `workbench/<run>/` holds one workbench run: its bundle, its retained state
  and a `workbench.json` naming the cohort, the cohort content hash and the
  inventory digest.
- A run directory per invocation holds one JSON report per case, a
  `summary.json`, the unit results and the retained disposable store under
  `state/<case>/`.

Reports name the inventory digest, the tested files, the snapshot and the
store path, and state `os_isolation` as `UNVERIFIED` for every local run.
Earlier reports are kept. The JSON reports and snapshots are committed as
evidence. The SQLite stores and their write-ahead files are ignored by git
and stay on the machine that produced them.

A store created by any of these commands is disposable. It carries a
`DISPOSABLE.json` marker and is never production genesis.

## Drive the core directly

The public command interface is:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m adaptive_research_harness command OP --actor ID --request FILE
```

The request file is JSON. The actor is authenticated by the transport, not
by the string on the command line. In the local fixture that is a
per-process token; on Linux it is the peer process UID mapped through
`isolation/roles.json`. Knowing an actor's name confers nothing.

## What the local runs do not establish

- Operating-system isolation. Core, researchers, Checkers, tools and the
  reader run as separate processes under the same user. Linux UID, socket,
  file and cgroup enforcement is templated under `isolation/` and needs a
  dedicated disposable Ubuntu host with systemd. Case T06 is excluded
  locally for that reason.
- Case B10 substitutes a whole-core outage for a Transition-ledger-only
  read failure.
- The Checker language has no supported input that reaches the
  constitutional NOT DETERMINABLE or STOP branch, so that branch is not
  exercised.
- Any real provider, billing, market data, trading or framework adapter.
  Every charge is simulated and every data source is synthetic.

## Linux host procedure

The `isolation/` directory holds systemd unit templates, the fixed account
map and a read-only host fingerprint collector. The intended host is a
dedicated disposable Ubuntu 24.04 machine with native ext4, systemd and
cgroup v2. Staging the covered tree, collecting the fingerprint and running
the full catalog there is described in the
[run packet](docs/builds/first_cycle_20261029/run_approval_packet.md). That
procedure has not been executed.
