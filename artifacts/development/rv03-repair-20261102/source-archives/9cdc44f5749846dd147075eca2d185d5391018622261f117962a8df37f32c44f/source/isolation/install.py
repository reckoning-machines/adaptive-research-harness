"""Explicit operator installation; not run during build. No dependency downloads."""
import argparse
import grp
import os
from pathlib import Path
import pwd
import shutil
import subprocess
from adaptive_research_harness.encoding import decode,require
from adaptive_research_harness.profile import Profile


def install(args):
    require(os.getuid()==0,'ROOT_REQUIRED')
    root=Path(args.root).resolve();require(root==Path('/opt/adaptive-research-harness'),'FIXED_INSTALL_ROOT')
    profile=Profile(root/'docs/builds/first_cycle_20261029/run_bundle')
    profile.approve_run(args.permit,root)
    cfg=decode((root/'isolation/generated/accounts.json').read_bytes())
    for name,gid in cfg['groups'].items():
        try:existing=grp.getgrgid(gid);require(existing.gr_name==name,'GID_COLLISION')
        except KeyError:subprocess.run(['groupadd','--gid',str(gid),name],check=True)
    for account in cfg['accounts']:
        name,uid=account['name'],account['uid']
        try:p=pwd.getpwuid(uid);require(p.pw_name==name and p.pw_gid==account['gid'],'UID_COLLISION')
        except KeyError:subprocess.run(['useradd','--system','--uid',str(uid),'--gid',str(account['gid']),'--no-create-home','--shell','/usr/sbin/nologin',name],check=True)
        for group in cfg['supplementary'].get(name,[]):subprocess.run(['usermod','--append','--groups',group,name],check=True)
    base=Path('/run/adaptive-research-harness');base.mkdir(exist_ok=True,mode=0o755)
    state=Path('/var/lib/adaptive-research-harness');state.mkdir(exist_ok=True,mode=0o755)
    for label,s in cfg['services'].items():
        uid=pwd.getpwnam(s['user']).pw_uid
        for parent in (base,state):
            d=parent/label;d.mkdir(exist_ok=True);os.chown(d,uid,s['gid']);os.chmod(d,0o750 if parent==base else 0o700)
    for d in (state/'supervisor',base/'supervisor'):
        d.mkdir(exist_ok=True);os.chown(d,0,20054);os.chmod(d,0o755 if d.parent==state else 0o750)
    reports=Path('/var/lib/adaptive-research-harness-reports');reports.mkdir(exist_ok=True);os.chown(reports,20001,20054);os.chmod(reports,0o700)
    for p in (root/'isolation/generated').glob('*.service'):
        target=Path('/etc/systemd/system')/p.name;shutil.copyfile(p,target);os.chmod(target,0o644)
    subprocess.run(['systemctl','daemon-reload'],check=True)
    print('Installed fixed units. No unit started; no clock or governed state initialized.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--permit',default=None);install(p.parse_args())
