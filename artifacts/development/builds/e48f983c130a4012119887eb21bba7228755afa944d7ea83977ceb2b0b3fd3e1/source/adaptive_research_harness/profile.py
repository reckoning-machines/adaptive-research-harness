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
        """Compatibility name: automatic private-development traceability.

        Separate artifact/host approvals were superseded by the Principal.
        Linux entrypoints still enforce fixed UIDs, peers and runtime grants.
        No file at permit_path confers runtime authorization.
        """
        import sys
        if require_linux:require(sys.platform=='linux' and sys.version_info[:2]==(3,12),'UNSUPPORTED_HOST')
        self.verify_files(root)
        return {'inventory_sha256':self.inventory_hash,'allow_apply_zero':True,
                'scope':'PRINCIPAL_AUTHORIZED_DISPOSABLE_SYNTHETIC_DEVELOPMENT'}
