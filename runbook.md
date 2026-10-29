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

## Run the test suites

Unit and component tests:

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

- `builds/<digest>/` holds the code inventory and a complete snapshot of
  the covered source for that run. Changing source during a run fails
  verification.
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
