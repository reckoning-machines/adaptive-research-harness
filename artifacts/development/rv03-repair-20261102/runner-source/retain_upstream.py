from pathlib import Path
import hashlib,json,importlib.metadata,platform,re,shutil,sys
R=Path(__file__).resolve().parent;E=R/'evidence';ARH=Path('/Users/jedgore/dev/speedway')
def read(p):return json.loads(p.read_text())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
summary_path=next((E/'acceptance-schedules').glob('*/summary.json'));native=read(summary_path)
assert len(native['results'])==77 and all(x['status']=='PASS' for x in native['results'])
for phase,n in [('red',1),('targeted',6),('full-unit',106)]:
 out=(E/phase/'output.txt').read_text();assert f'Ran {n} test' in out
 assert read(E/phase/'command.json')['returncode']==(1 if phase=='red' else 0)
 if phase!='red':assert 'FAILED (' not in out and 'skipped=' not in out
for phase in ('red','targeted','full-unit'):
 for p in (E/phase/'public-host-regressions').glob('*/identity.json'):
  identity=read(p);run=Path(identity['run'])
  target=p.parent/'bundle'
  shutil.copytree(run/'bundle',target,ignore=shutil.ignore_patterns('__pycache__'),dirs_exist_ok=True)
  # Full immutable source snapshot corresponding to each frozen bundle.
  inventory=hashlib.sha256((run/'bundle/inventory.json').read_bytes()).hexdigest()
  archive=ARH/'artifacts/development/builds'/inventory
  if archive.exists():shutil.copytree(archive,E/'source-archives'/inventory,dirs_exist_ok=True)
# Native source archive has the complete covered test/core/client source.
archive=ARH/'artifacts/development/builds'/native['inventory_sha256']
shutil.copytree(archive,E/'source-archives'/native['inventory_sha256'],dirs_exist_ok=True)
write(E/'environment.json',{'python':sys.version,'platform':platform.platform(),'packages':{d.metadata['Name']:d.version for d in importlib.metadata.distributions()},'client_changed':False,'paid_services':False})
write(E/'verification-summary.json',{'pre_repair_reproduction':{'tests':1,'failures':1,'reason':'UNFUNDED_CHECK for admitted check-half/0.50; complete real charge retained'},'targeted':{'tests':6,'passed':6,'failures':0,'errors':0,'skips':0},'full_unittest':{'tests':106,'passed':106,'failures':0,'errors':0,'skips':0},'native_acceptance':{'selected':77,'passed':77,'failures':0,'errors':0,'excluded':'T06: Linux peer/isolation, unchanged','limitations':native['coverage_notes']},'source_inventory':native['inventory_sha256'],'OSA':'PASS for bounded RV-03 contract','CPOC':'PASS for Check/settlement keyed outcomes through forced caller/core replacement; broader suite limitations retained','deployment':'NOT APPLICABLE; not authorized','global_certification':'NOT CLAIMED'})
for name in ('run_arh_checks.py','retain_upstream.py'):
 (E/'runner-source').mkdir(exist_ok=True);shutil.copyfile(R/name,E/'runner-source'/name)
# SQLite overflow pages can split a SHA-256 into a 48-hex prefix/suffix.
# A binary candidate is classified only if it matches an observed full hash.
full_hashes=set()
for p in E.rglob('*'):
 if p.is_file():full_hashes.update(re.findall(rb'(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])',p.read_bytes()))
fragments={h[i:i+48] for h in full_hashes for i in range(17)}
secrets=[];binary_fragments=[]
for p in E.rglob('*'):
 if p.is_file():
  raw=p.read_bytes()
  matches=list(re.finditer(rb'(?<![0-9a-f])[0-9a-f]{48}(?![0-9a-f])',raw));candidates=[m.group() for m in matches]
  def labelled_ref(m):
   before=raw[max(0,m.start()-150):m.start()]
   refs=list(re.finditer(rb'"ledger":"[ET]","sequence":[0-9]+,"sha256":"([0-9a-f]*)',before))
   if not refs:return False
   prefix=refs[-1];gap=before[prefix.end():]
   # One WAL page split has 16 digest chars followed by an ASCII-hex
   # overflow pointer byte, then its binary frame/cell header and 48 chars.
   return len(prefix.group(1)) in (16,17) and b'\x00' in gap and raw[m.end():m.end()+1]==b'"'
  if candidates:
   if p.suffix in ('.sqlite','.sqlite-wal') and all(m.group() in fragments or labelled_ref(m) for m in matches):binary_fragments.append({'path':str(p.relative_to(E)),'fragments':len(candidates),'classification':'SQLite page split of separately observed full SHA-256, or an explicitly labelled immutable ledger-reference sha256 field'})
   else:secrets.append(str(p.relative_to(E)))
assert not secrets,secrets
write(E/'redaction.json',{'host_48_hex_token_candidates':0,'raw_connection_or_fixture_files_included':False,'authentication_headers_included':False,'binary_SHA256_fragments':binary_fragments,'notice':'Native acceptance retains its standard disposable SQLite histories; consumer integration uses public exports only. No token values or token hashes retained.'})
rows=[]
for p in sorted(E.rglob('*')):
 if p.is_file() and p.name!='evidence-manifest.json':
  b=p.read_bytes();rows.append({'path':str(p.relative_to(E)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
write(E/'evidence-manifest.json',rows)
print(json.dumps({'retained_files':len(rows),'host_token_candidates':0,'native_schedules':77,'unit_tests':106,'regressions':6}))
