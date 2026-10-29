"""Build-only materialization. Never constructs Store, Engine or a governed event."""
import ast
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import platform
import sqlite3
import subprocess
import sys
import sysconfig

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from adaptive_research_harness.encoding import canonical, digest, raw_digest
from adaptive_research_harness.contracts import SCHEMAS
from adaptive_research_harness.profile import SPEC_MANIFEST

BUNDLE=ROOT/'docs/builds/first_cycle_20261029/run_bundle'


def write(name,value):
    path=BUNDLE/name;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(canonical(value)+b'\n')


def materialize():
    original=ROOT/'docs/plans/research_cycle_admission_20261029'
    setup=json.loads((original/'setup.json').read_bytes())
    artifacts=json.loads((original/'designs_and_methods.json').read_bytes())
    index={str(p.relative_to(ROOT)):raw_digest(p.read_bytes()) for p in sorted((ROOT/'adaptive_research_harness').rglob('*')) if p.suffix in ('.py','.sql')}
    imports={}
    for path in index:
        if not path.endswith('.py'):continue
        tree=ast.parse((ROOT/path).read_text())
        imports[path]=sorted(set(n.module or '' for n in ast.walk(tree) if isinstance(n,ast.ImportFrom))|set(a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names))
    write('code_index.json',{'files':index,'imports':imports,'scope':'Complete installed harness closure, conservative superset; independent criterion modules audited separately.'})
    for d in artifacts['designs']:
        c=d['content'];c['entrypoint']='adaptive_research_harness.service:run_agent'
        c['step_catalog']=['check-transition'] if c['method_class']=='CHECKER' else ['research-counts','replacement-counts','verification-candidate']
        c['executable_closure_sha256']=digest({'code':index,'configuration':deepcopy(c)})
        d['content_sha256']=digest(c)
    artifacts['status']='BUILT_PRIVATE_NOT_INITIALIZED'
    write('designs_and_methods.json',artifacts)
    setup['status']='BUILD_APPROVED_RUNTIME_NOT_INITIALIZED'
    setup['artifacts_file']='designs_and_methods.json'
    setup['artifacts_file_sha256']=raw_digest((BUNDLE/'designs_and_methods.json').read_bytes())
    write('setup.json',setup)
    roles={20001:'Principal',20002:'Observation function',20011:'AD-CK-1.0',20012:'AD-CK-2.0'}
    roles.update({20020+i:f'AD-R{i}.0' for i in range(1,11)})
    write('roles.json',{str(k):v for k,v in roles.items()})
    write('command_schemas.json',{k:{'required':sorted(v[0]),'optional':sorted(v[1])} for k,v in SCHEMAS.items()})
    write('host_profile.json',{'status':'PROPOSED_DISPOSABLE_HOST_NOT_PROVISIONED','os':'Ubuntu 24.04 LTS','python':'3.12.x','sqlite':'system Python sqlite3 with WAL/FULL and foreign keys','filesystem':'local ext4, no network filesystem','root':'/opt/adaptive-research-harness','runtime':'/run/adaptive-research-harness','state':'/var/lib/adaptive-research-harness','retained_cases':'/var/lib/adaptive-research-harness-acceptance','network':'disabled for all harness units','trust':'Root/operator, fixed installed core and registered actor programs are trusted; research inputs and tool results are not. No same-UID embedding security claim.','actual_host_fingerprint':None,'gate':'Disposable development is authorized; fingerprints and hashes are automatic traceability, not approval gates.'})
    return index,artifacts


def freeze(bundle=None):
    global BUNDLE
    if bundle is not None:BUNDLE=Path(bundle)
    index,artifacts=materialize()
    manifest=ROOT/'docs/plans/research_cycle_reconciled_20261029/manifest.json'
    assert raw_digest(manifest.read_bytes())==SPEC_MANIFEST
    approved=json.loads(manifest.read_bytes());covered=[]
    for group in ('baseline_inputs','build_specifications','review_evidence','historical_snapshots'):
        for item in approved[group]:
            assert raw_digest((ROOT/item['path']).read_bytes())==item['sha256'],item['path']
            covered.append(item['path'])
    paths=set(covered+[str(manifest.relative_to(ROOT))])
    for directory in ('adaptive_research_harness','build_support','tests','acceptance','isolation'):
        paths.update(str(p.relative_to(ROOT)) for p in (ROOT/directory).rglob('*') if p.is_file() and '__pycache__' not in str(p))
    paths.update(str(p.relative_to(ROOT)) for p in BUNDLE.iterdir() if p.is_file() and p.name!='inventory.json')
    paths.add('docs/decisions/first_research_cycle_build_approval_addendum_20261029.md')
    if (ROOT/'BUILD.md').exists():paths.add('BUILD.md')
    files=[{'path':p,'sha256':raw_digest((ROOT/p).read_bytes()),'bytes':(ROOT/p).stat().st_size} for p in sorted(paths)]
    status=subprocess.check_output(['git','status','--porcelain=v1'],cwd=ROOT,text=True).splitlines()
    tracked=subprocess.check_output(['git','ls-files','-m'],cwd=ROOT,text=True).splitlines()
    from acceptance.catalog import CASES,DEATH_POINTS
    inventory={'status':'DISPOSABLE_DEVELOPMENT_BUILD','specification_manifest':SPEC_MANIFEST,'files':files,
      'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
      'source_status':status,'dirty_tracked_files':{p:raw_digest((ROOT/p).read_bytes()) for p in tracked},
      'build_environment':{'python':sys.version,'python_executable':str(Path(sys.executable).resolve()),'python_executable_sha256':raw_digest(Path(sys.executable).resolve().read_bytes()),'sqlite':sqlite3.sqlite_version,'os':platform.platform(),'machine':platform.machine(),'filesystem':'APFS (kernel implementation)' if sys.platform=='darwin' else 'see host fingerprint','mount_evidence':subprocess.check_output(['mount'],text=True).splitlines() if sys.platform=='darwin' else []},
      'tool_executables':{'SYN-A-1':index['adaptive_research_harness/tools_a.py'],'SYN-B-1':index['adaptive_research_harness/tools_b.py'],'CHECK-A-1':index['adaptive_research_harness/checkers/a.py'],'CHECK-B-1':index['adaptive_research_harness/checkers/b.py']},
      'code_closure':index,
      'design_executables':{d['content']['AgentDesignVersionId']:d['content']['executable_closure_sha256'] for d in artifacts['designs']},
      'runtime_cases':list(CASES),'process_death_points':DEATH_POINTS,'forced_terminal_orders':['apply','invalidate'],
      'authority':'Principal-authorized disposable synthetic development; runtime grants still require lawful startup. No real provider or spending.',
      'host_profile':'docs/builds/first_cycle_20261029/run_bundle/host_profile.json',
      'run_gate':'No separate approval for disposable development. Runtime controls remain enforced.'}
    write('inventory.json',inventory)
    inventory_hash=raw_digest((BUNDLE/'inventory.json').read_bytes())
    import shutil
    archive=ROOT/'artifacts/development/builds'/inventory_hash
    if not archive.exists():
        archive.mkdir(parents=True);shutil.copyfile(BUNDLE/'inventory.json',archive/'inventory.json')
        for item in files:
            destination=archive/'source'/item['path'];destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/item['path'],destination)
    print(inventory_hash,flush=True)
    return inventory_hash

if __name__=='__main__':freeze()
