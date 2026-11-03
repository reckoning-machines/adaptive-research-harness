"""Build-only materialization. Never constructs Store, Engine or a governed event.

A bundle is frozen from a setup descriptor: the setup, the designs and
methods, the experiment profile, an optional cohort catalog and any file
modules the profile names. The default descriptor is the admitted synthetic
packet with its profile under experiments/synthetic_flow/. An external
experiment supplies a directory holding the same files.
"""
import ast
from copy import deepcopy
from pathlib import Path
import importlib.util
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
from adaptive_research_harness.experiment import Experiment

BUNDLE=ROOT/'docs/builds/first_cycle_20261029/run_bundle'
# Files that take part in a run or its recovery. A change to one of these turns
# an earlier run read-only. Tests, documents, build tooling and the Linux
# templates are in the build identity but not here.
EXECUTION_PREFIXES=('adaptive_research_harness/','client/arh_client/')
EXECUTION_FILES=('workbench/session.py','workbench/local_session.py','workbench/records.py','workbench/api.py','workbench/__main__.py',
                 'acceptance/local.py','acceptance/runtime.py','acceptance/reader.py')
SYNTHETIC={'setup':ROOT/'docs/plans/research_cycle_admission_20261029/setup.json',
           'artifacts':ROOT/'docs/plans/research_cycle_admission_20261029/designs_and_methods.json',
           'experiment':ROOT/'experiments/synthetic_flow/experiment.json',
           'cohorts':ROOT/'workbench/cohorts.json'}


def descriptor(setup=None):
    """A descriptor dict, from None (synthetic), a directory, or a dict."""
    if setup is None:return dict(SYNTHETIC)
    if isinstance(setup,dict):return dict(setup)
    d=Path(setup).resolve();cohorts=d/'cohorts.json'
    return {'setup':d/'setup.json','artifacts':d/'designs_and_methods.json','experiment':d/'experiment.json','cohorts':cohorts if cohorts.is_file() else None}


def write(name,value):
    path=BUNDLE/name;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(canonical(value)+b'\n')


def module_bytes(experiment_dir,spec):
    """Bytes of a tool module: an installed package module, or a file relative to the experiment file's directory."""
    m=spec['module']
    if m.endswith('.py'):
        path=(experiment_dir/m).resolve();assert path.is_relative_to(experiment_dir) and path.is_file(),m
        return path.read_bytes(),path
    origin=importlib.util.find_spec(m).origin;return Path(origin).read_bytes(),Path(origin)


def materialize(desc):
    setup=json.loads(Path(desc['setup']).read_bytes())
    artifacts=json.loads(Path(desc['artifacts']).read_bytes())
    experiment_path=Path(desc['experiment']).resolve();experiment_data=json.loads(experiment_path.read_bytes())
    experiment=Experiment(experiment_data);experiment_dir=experiment_path.parent
    index={str(p.relative_to(ROOT)):raw_digest(p.read_bytes()) for p in sorted((ROOT/'adaptive_research_harness').rglob('*')) if p.suffix in ('.py','.sql')}
    imports={}
    for path in index:
        if not path.endswith('.py'):continue
        tree=ast.parse((ROOT/path).read_text())
        imports[path]=sorted(set(n.module or '' for n in ast.walk(tree) if isinstance(n,ast.ImportFrom))|set(a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names))
    write('code_index.json',{'files':index,'imports':imports,'scope':'Complete installed harness closure, conservative superset; independent criterion modules audited separately.'})
    assert set(experiment.tools)==set(artifacts['tools']),'profile tools must equal the declared tool artifacts'
    designs={d['content']['AgentDesignVersionId'] for d in artifacts['designs']}
    grants={g['content']['AuthorizationId'] for g in setup['grants']}
    assert experiment.genesis['design'] in designs and experiment.genesis['grant'] in grants,'genesis pair must be declared'
    # Cohort catalog: declared synthetic variants of the formation item.
    # Metadata must equal the formation cohort; only rows may differ.
    formation=artifacts['formation_cohort']['content'];variants={}
    if desc.get('cohorts'):
        catalog=json.loads(Path(desc['cohorts']).read_bytes())
        for name,entry in catalog['cohorts'].items():
            doc=entry['content']
            assert {k:v for k,v in doc.items() if k not in ('rows','variant')}=={k:v for k,v in formation.items() if k!='rows'},name
            if name=='original':assert 'variant' not in doc and doc['rows']==formation['rows'],'original cohort must equal the formation cohort'
            else:
                v=doc['variant'];assert v['name']==name and v['of_item']==formation['item_id'] and v['of_content_sha256']==digest(formation) and v['edits']==entry['differs_from_formation'],name
            variants[name]={'description':entry['description'],'differs_from_formation':entry['differs_from_formation'],'expected_path':entry['expected_path'],'content':doc,'content_sha256':digest(doc)}
        assert variants['original']['content_sha256']==digest(formation),'original cohort must equal the formation cohort'
    artifacts['variant_cohorts']=variants
    # Tool executables: hashed bytes of each declared module; file modules are copied into the bundle.
    tool_executables={}
    for tool_id,spec in experiment.tools.items():
        raw,source=module_bytes(experiment_dir,spec);tool_executables[tool_id]=raw_digest(raw)
        if spec['module'].endswith('.py'):
            target=BUNDLE/'tools'/spec['module'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    for d in artifacts['designs']:
        c=d['content'];c.setdefault('entrypoint','adaptive_research_harness.service:run_agent')
        c['step_catalog']=experiment.steps_of('check') if c['method_class']=='CHECKER' else experiment.steps_of('research')
        assert set(c['tool_specs'])<=set(experiment.tools),c['AgentDesignVersionId']
        if c.get('program'):
            program=(experiment_dir/c['program']).resolve();assert program.is_relative_to(experiment_dir) and program.is_file(),c['program']
            c['program_sha256']=raw_digest(program.read_bytes())
            target=BUNDLE/'programs'/c['program'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(program.read_bytes())
        c['executable_closure_sha256']=digest({'code':index,'configuration':deepcopy(c)})
        d['content_sha256']=digest(c)
    artifacts['status']='BUILT_PRIVATE_NOT_INITIALIZED'
    write('designs_and_methods.json',artifacts)
    write('experiment.json',experiment_data)
    setup['status']='BUILD_APPROVED_RUNTIME_NOT_INITIALIZED'
    setup['artifacts_file']='designs_and_methods.json'
    setup['artifacts_file_sha256']=raw_digest((BUNDLE/'designs_and_methods.json').read_bytes())
    setup['experiment_file']='experiment.json'
    setup['experiment_file_sha256']=raw_digest((BUNDLE/'experiment.json').read_bytes())
    write('setup.json',setup)
    roles={20001:'Principal',20002:'Observation function'}
    checkers=[d['content']['AgentDesignVersionId'] for d in artifacts['designs'] if d['content']['method_class']=='CHECKER']
    researchers=[d['content']['AgentDesignVersionId'] for d in artifacts['designs'] if d['content']['method_class']!='CHECKER']
    roles.update({20011+i:name for i,name in enumerate(checkers)});roles.update({20021+i:name for i,name in enumerate(researchers)})
    write('roles.json',{str(k):v for k,v in roles.items()})
    write('command_schemas.json',{k:{'required':sorted(v[0]),'optional':sorted(v[1])} for k,v in SCHEMAS.items()})
    write('host_profile.json',{'status':'PROPOSED_DISPOSABLE_HOST_NOT_PROVISIONED','os':'Ubuntu 24.04 LTS','python':'3.12.x','sqlite':'system Python sqlite3 with WAL/FULL and foreign keys','filesystem':'local ext4, no network filesystem','root':'/opt/adaptive-research-harness','runtime':'/run/adaptive-research-harness','state':'/var/lib/adaptive-research-harness','retained_cases':'/var/lib/adaptive-research-harness-acceptance','network':'disabled for all harness units','trust':'Root/operator, fixed installed core and registered actor programs are trusted; research inputs and tool results are not. No same-UID embedding security claim.','actual_host_fingerprint':None,'gate':'Disposable development is authorized; fingerprints and hashes are automatic traceability, not approval gates.'})
    return index,artifacts,tool_executables


def freeze(bundle=None,setup=None):
    global BUNDLE
    if bundle is None:
        import uuid
        bundle=ROOT/'artifacts/development/run-bundles'/uuid.uuid4().hex/'bundle'
    BUNDLE=Path(bundle);desc=descriptor(setup)
    index,artifacts,tool_executables=materialize(desc)
    manifest=ROOT/'docs/plans/research_cycle_reconciled_20261029/manifest.json'
    assert raw_digest(manifest.read_bytes())==SPEC_MANIFEST
    approved=json.loads(manifest.read_bytes());covered=[]
    for group in ('baseline_inputs','build_specifications','review_evidence','historical_snapshots'):
        for item in approved[group]:
            assert raw_digest((ROOT/item['path']).read_bytes())==item['sha256'],item['path']
            covered.append(item['path'])
    paths=set(covered+[str(manifest.relative_to(ROOT))])
    for directory in ('adaptive_research_harness','build_support','tests','acceptance','isolation','workbench','experiments','client/arh_client'):
        paths.update(str(p.relative_to(ROOT)) for p in (ROOT/directory).rglob('*') if p.is_file() and '__pycache__' not in str(p))
    setup_dir=Path(desc['experiment']).resolve().parent
    setup_in_root=setup_dir.is_relative_to(ROOT)
    if setup_in_root:paths.update(str(p.relative_to(ROOT)) for p in setup_dir.rglob('*') if p.is_file() and '__pycache__' not in str(p))
    paths.add('docs/decisions/first_research_cycle_build_approval_addendum_20261029.md')
    if (ROOT/'BUILD.md').exists():paths.add('BUILD.md')
    files=[{'path':p,'sha256':raw_digest((ROOT/p).read_bytes()),'bytes':(ROOT/p).stat().st_size} for p in sorted(paths)]
    # The bundle's own files are identity too, listed under the stable virtual
    # prefix 'bundle/' and resolved against the bundle directory, so the
    # directory a run happens to use does not change the build identity.
    files+=[{'path':'bundle/'+str(p.relative_to(BUNDLE)),'root':'bundle','sha256':raw_digest(p.read_bytes()),'bytes':p.stat().st_size}
            for p in sorted(BUNDLE.rglob('*')) if p.is_file() and str(p.relative_to(BUNDLE)) not in ('inventory.json','build_metadata.json','environment.json')]
    def takes_part(entry):
        p=entry['path']
        if entry.get('root')=='bundle':return True
        if p.startswith(EXECUTION_PREFIXES) or p in EXECUTION_FILES:return True
        return setup_in_root and (ROOT/p).resolve().is_relative_to(setup_dir)
    execution_files=[{k:v for k,v in e.items() if k!='bytes'} for e in files if takes_part(e)]
    # Declared dependencies: the experiment directory may name the packages its tools and evaluator import.
    # Installed versions are recorded beside the bundle, outside the build identity, and compared on reopen.
    import importlib.metadata
    declared=json.loads((setup_dir/'dependencies.json').read_bytes()) if (setup_dir/'dependencies.json').is_file() else {'packages':[]}
    versions={}
    for name in declared.get('packages',[]):
        try:versions[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:versions[name]=None
    write('environment.json',{'python':platform.python_version(),'packages':versions,'declared':declared,
      'meaning':'Installed interpreter and declared package versions at freeze. Compared on reopen; a difference opens the run read-only. Outside the build identity.'})
    status=subprocess.check_output(['git','status','--porcelain=v1'],cwd=ROOT,text=True).splitlines()
    tracked=subprocess.check_output(['git','ls-files','-m'],cwd=ROOT,text=True).splitlines()
    from acceptance.catalog import CASES,DEATH_POINTS
    # Identity covers source bytes only. Working-tree status and the build
    # environment are recorded beside it as metadata, outside the digest, so
    # identical source yields one build identity.
    metadata={'identity':'build_metadata.json is metadata, not identity; inventory.json names the source',
      'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
      'source_status':status,'dirty_tracked_files':{p:(raw_digest((ROOT/p).read_bytes()) if (ROOT/p).is_file() else 'DELETED') for p in tracked},
      'setup_descriptor':{k:(str(v) if v else None) for k,v in desc.items()},
      'build_environment':{'python':platform.python_version(),'python_implementation':platform.python_implementation(),'executable_sha256':raw_digest(Path(sys.executable).resolve().read_bytes()),'sqlite':sqlite3.sqlite_version,'os':platform.platform(),'machine':platform.machine(),'filesystem':'APFS (kernel implementation)' if sys.platform=='darwin' else 'see host fingerprint','mount_evidence':subprocess.check_output(['mount'],text=True).splitlines() if sys.platform=='darwin' else []}}
    write('build_metadata.json',metadata)
    inventory={'status':'DISPOSABLE_DEVELOPMENT_BUILD','specification_manifest':SPEC_MANIFEST,'files':files,'execution_files':execution_files,
      'execution_identity':'files that take part in a run or its recovery; with environment.json they decide whether a retained run reopens live',
      'build_metadata':'build_metadata.json (status and environment; outside this identity)',
      'tool_executables':tool_executables,
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
        shutil.copyfile(BUNDLE/'build_metadata.json',archive/'build_metadata.json');shutil.copyfile(BUNDLE/'environment.json',archive/'environment.json')
        for item in files:
            destination=archive/'source'/item['path'];destination.parent.mkdir(parents=True,exist_ok=True)
            source=BUNDLE/Path(item['path']).relative_to('bundle') if item.get('root')=='bundle' else ROOT/item['path']
            shutil.copyfile(source,destination)
    print(inventory_hash,flush=True)
    return inventory_hash

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--setup',default=None);p.add_argument('--bundle',default=None);a=p.parse_args()
    freeze(a.bundle,a.setup)
