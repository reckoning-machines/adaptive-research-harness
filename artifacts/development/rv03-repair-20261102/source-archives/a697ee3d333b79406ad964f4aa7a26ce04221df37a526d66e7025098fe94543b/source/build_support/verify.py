"""Read-only build-integrity checks; no core startup or governed writes."""
import hashlib
import json
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parents[1]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def verify():
    manifest=ROOT/'docs/plans/research_cycle_reconciled_20261029/manifest.json'
    assert sha(manifest)=='063b442e83690851a890bdc885cc39ba39545362f38d505b67edd046c12b3884'
    m=json.loads(manifest.read_bytes());covered=[]
    for group in ('baseline_inputs','build_specifications','review_evidence','historical_snapshots'):
        for item in m[group]:
            p=ROOT/item['path'];assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes'],str(p)
            covered.append(item)
    initial=Path('/private/tmp/arh-build-before.json')
    preserved=None
    if initial.exists():
        original=json.loads(initial.read_bytes())
        assert all((ROOT/p).is_file() and sha(ROOT/p)==s for p,s in original.items())
        preserved=len(original)
    inventory=ROOT/'docs/builds/first_cycle_20261029/run_bundle/inventory.json'
    inv=json.loads(inventory.read_bytes())
    for entry in inv['files']:assert sha(ROOT/entry['path'])==entry['sha256'],entry['path']
    new_text=[ROOT/'BUILD.md']
    for folder in ('adaptive_research_harness','build_support','acceptance','isolation','tests','docs/builds/first_cycle_20261029'):
        new_text += [p for p in (ROOT/folder).rglob('*') if p.suffix in ('.py','.sql','.md','.json','.service')]
    for p in new_text:
        raw=p.read_text();assert all(line==line.rstrip() for line in raw.splitlines()),str(p)+' trailing whitespace'
        if p.suffix=='.md':
            for href in re.findall(r'\]\(([^)]+)\)',raw):
                if '://' in href or href.startswith('#'):continue
                target=href.split('#')[0];assert (p.parent/target).exists(),(str(p),href)
    return {'status':'PASS','approved_files_verified':len(covered),'preexisting_files_preserved':preserved,
      'inventory_sha256':sha(inventory),'inventory_files_verified':len(inv['files']),
      'new_text_files_checked':len(new_text),'no_genesis_invoked':True}

if __name__=='__main__':print(json.dumps(verify(),sort_keys=True))
