"""One command to bring a project up for local development: setup written, bundle frozen, host started, startup signed.

    python3 -m arh_client.dev up examples/memo_returns --run /tmp/arh-memo [--charter "..."] [--regenerate]
    python3 -m arh_client.dev down /tmp/arh-memo

up needs the ARH checkout, found from ARH_ROOT or by walking up from the
project directory and the working directory. It writes the setup files
from project.json when they are missing, freezes a bundle into the run
directory, starts the local host, runs the startup sequence under the
Principal, Observation and Checker identities, prints the connection file
and stays up until Ctrl-C or down. A run directory that already holds a
bundle is reopened instead, and reopens only if the execution identity
still matches. Nothing here is OS isolation; the connection file is a
credential.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import importlib
import os
import sys
import time
from .protocol import require, HarnessError
from .project import Project


def find_root(start):
    env = os.environ.get('ARH_ROOT')
    if env: return Path(env)
    for base in (Path(start).resolve(), Path.cwd().resolve()):
        for p in (base, *base.parents):
            if (p / 'adaptive_research_harness' / 'local_host.py').is_file(): return p
    raise HarnessError('NO_CHECKOUT', 'set ARH_ROOT to the ARH checkout; the host runs from it')


def load_entrypoint(entrypoint):
    module, _, name = entrypoint.partition(':'); return getattr(importlib.import_module(module), name)


def start(project_dir, run, charter=None, regenerate=False, formation_date='2026-10-28'):
    """Bring the project up and return (host, project, fresh). The caller stops the host."""
    root = find_root(project_dir)
    for p in (str(root), str(root / 'client')):
        if p not in sys.path: sys.path.insert(0, p)
    project = Project.load(project_dir)
    if regenerate or not project.setup_exists(): project.write_setup()
    from adaptive_research_harness.local_host import LocalHost
    run = Path(run).resolve(); bundle = run / 'bundle'; state = run / 'state'; fresh = not bundle.exists()
    if fresh:
        from build_support.freeze import freeze
        freeze(bundle, project.directory)
    host = LocalHost(bundle, state, root=root); host.start(); host.serve_control()
    if fresh:
        from .connection import connect
        from .principal import Principal, Observer, startup, historical_document
        from .checking import Checker
        conn = host.connection_path
        principal = Principal(connect(conn, 'Principal')); observer = Observer(connect(conn, 'Observation function'))
        checker = Checker(connect(conn, project.actor('checker')), evaluate_fn=load_entrypoint(project.data['evaluator']['entrypoint']))
        def passing_check(tr):
            r = checker.check(tr); require(r.result == 'PASS', 'STARTUP_CHECK_FAILED', str(r.criteria)); return r.check_sequence
        text = charter or f"# Charter\n{project.data['question']}\n"
        doc = historical_document(text.encode(), 'charter.md', 'the Principal', note='run charter')
        if project.sources[0]['class'] == 'synthetic': doc.update({'class': 'synthetic', 'synthetic': True})
        try: startup(principal, observer, passing_check, tick=host.tick, formation_content=doc, formation_date=formation_date)
        except BaseException:
            host.close(); raise
    return host, project, fresh


def stop(run):
    from .host import HostControl
    return HostControl.from_file(Project.connection_file(run)).stop()


def main(argv=None):
    p = argparse.ArgumentParser(prog='python3 -m arh_client.dev', description=__doc__.split('\n\n')[1], formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='command', required=True)
    up = sub.add_parser('up'); up.add_argument('project'); up.add_argument('--run', required=True); up.add_argument('--charter', default=None); up.add_argument('--regenerate', action='store_true')
    down = sub.add_parser('down'); down.add_argument('run')
    a = p.parse_args(argv)
    if a.command == 'down': print(stop(a.run)); return 0
    host, project, fresh = start(a.project, a.run, a.charter, a.regenerate)
    print('project', project.name, '| run', 'started' if fresh else 'reopened', '| connection', host.connection_path, flush=True)
    try:
        while not host.stopping.is_set(): time.sleep(0.5)
    except KeyboardInterrupt: pass
    finally: host.close()
    return 0


if __name__ == '__main__': sys.exit(main())
