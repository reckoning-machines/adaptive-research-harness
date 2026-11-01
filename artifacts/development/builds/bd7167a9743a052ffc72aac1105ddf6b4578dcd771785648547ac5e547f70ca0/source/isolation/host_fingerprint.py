"""Read-only target-host inventory. Run on proposed Linux host before run approval."""
import hashlib
import json
import os
from pathlib import Path
import platform
import sqlite3
import subprocess
import sys


def fingerprint(root):
    import adaptive_research_harness.service
    import adaptive_research_harness.actors
    import adaptive_research_harness.checkers.a
    import adaptive_research_harness.checkers.b
    import adaptive_research_harness.tool_worker
    import adaptive_research_harness.tools_a
    import adaptive_research_harness.tools_b
    files={}
    for mod in list(sys.modules.values()):
        name=getattr(mod,'__file__',None)
        if not name:continue
        p=Path(name).resolve()
        if p.suffix=='.pyc':
            import importlib.util
            p=Path(importlib.util.source_from_cache(str(p)))
        if p.is_file() and not p.is_relative_to(Path(root).resolve()):files[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
    executable=Path(sys.executable).resolve();files[str(executable)]=hashlib.sha256(executable.read_bytes()).hexdigest()
    return {'kind':'LINUX_HOST_FINGERPRINT','os_release':Path('/etc/os-release').read_text(),
      'kernel':platform.release(),'architecture':platform.machine(),'python':sys.version,'sqlite':sqlite3.sqlite_version,
      'filesystem':subprocess.check_output(['findmnt','--noheadings','--output','FSTYPE','--target','/var/lib'],text=True).strip(),
      'systemd':subprocess.check_output(['systemctl','--version'],text=True).splitlines()[0],
      'runtime_files':files,'root':str(Path(root).resolve())}

if __name__=='__main__':
    from adaptive_research_harness.encoding import canonical
    print(canonical(fingerprint(sys.argv[1])).decode())
