"""Frozen build specifications and explicit exact-artifact run-approval gate."""
from __future__ import annotations
from pathlib import Path
import os
import stat
from .encoding import decode, raw_digest, digest, require

SPEC_MANIFEST = '063b442e83690851a890bdc885cc39ba39545362f38d505b67edd046c12b3884'
CV1 = 'c56a9cf50a7e9efadad8f2f2be6605e82c758f18d4096ba07eaaf86a8f8b7a64'


class Profile:
    def __init__(self, bundle):
        self.bundle = Path(bundle)
        self.setup = decode((self.bundle/'setup.json').read_bytes())
        self.artifacts = decode((self.bundle/'designs_and_methods.json').read_bytes())
        self.designs = {d['content']['AgentDesignVersionId']: d['content'] for d in self.artifacts['designs']}
        self.grants = {g['content']['AuthorizationId']: g['content'] for g in self.setup['grants']}
        self.roles = {int(k): v for k, v in decode((self.bundle/'roles.json').read_bytes()).items()}
        self.inventory = decode((self.bundle/'inventory.json').read_bytes())
        self.inventory_hash = raw_digest((self.bundle/'inventory.json').read_bytes())
        require(self.inventory['specification_manifest'] == SPEC_MANIFEST, 'WRONG_SPECIFICATION')
        require(self.setup['constitution']['sha256'] == CV1, 'WRONG_CONSTITUTION')
        self.code_root = self.bundle.parents[2] if self.bundle.name == 'run_bundle' else None

    def verify_files(self, root):
        root = Path(root).resolve()
        for entry in self.inventory['files']:
            path = (root/entry['path']).resolve()
            require(path.is_relative_to(root) and path.is_file(), 'ARTIFACT_UNREACHABLE')
            require(raw_digest(path.read_bytes()) == entry['sha256'], 'ARTIFACT_CHANGED', entry['path'])

    def development_permission(self, root, state):
        """Operator-authorized disposable development; automatic traceability only."""
        marker=Path(state)/'DISPOSABLE.json'
        require(marker.is_file(),'DISPOSABLE_MARKER_REQUIRED')
        record=decode(marker.read_bytes())
        require(record.get('disposable') is True and record.get('run_id'),'DISPOSABLE_MARKER_REQUIRED')
        self.verify_files(root)
        return {'inventory_sha256':self.inventory_hash,'allow_apply_zero':True,
                'scope':'DISPOSABLE_SYNTHETIC_DEVELOPMENT','run_id':record['run_id']}

    def approve_run(self, permit_path, root, *, require_linux=True):
        """Only trusted operator can install this after distinct human run approval."""
        import sys
        path = Path(permit_path)
        require(path.is_file(), 'RUN_APPROVAL_REQUIRED')
        st = path.stat()
        require(st.st_uid == 0 and not st.st_mode & (stat.S_IWGRP | stat.S_IWOTH), 'UNTRUSTED_RUN_APPROVAL')
        permit = decode(path.read_bytes())
        require(permit.get('kind') == 'EXACT_ARTIFACT_RUN_APPROVAL' and
                permit.get('inventory_sha256') == self.inventory_hash and
                permit.get('principal_approval_record_sha256') and
                permit.get('allow_apply_zero') is True, 'RUN_APPROVAL_REQUIRED')
        if require_linux:
            require(sys.platform == 'linux' and sys.version_info[:2] == (3, 12), 'UNSUPPORTED_HOST')
        self.verify_files(root)
        if require_linux:
            hp=path.with_name('host-fingerprint.json')
            require(hp.is_file(),'HOST_FINGERPRINT_REQUIRED')
            hs=hp.stat();require(hs.st_uid==0 and not hs.st_mode&(stat.S_IWGRP|stat.S_IWOTH),'UNTRUSTED_HOST_FINGERPRINT')
            require(raw_digest(hp.read_bytes())==permit.get('host_fingerprint_sha256'),'HOST_FINGERPRINT_REQUIRED')
            host=decode(hp.read_bytes())
            import platform
            import sqlite3
            require(host['kernel']==platform.release() and host['python']==sys.version and host['sqlite']==sqlite3.sqlite_version and host['filesystem']=='ext4','HOST_CHANGED')
            for filename,expected in host['runtime_files'].items():
                require(raw_digest(Path(filename).read_bytes())==expected,'RUNTIME_CHANGED',filename)
        return permit
