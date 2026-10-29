"""Root test supervisor: fixed unit/cgroup operations, no governed writer access.

May archive whole stopped test stores; it never opens or seeds the database.
Every operation is gated by the separately approved run and host inventory.
"""
import argparse
from pathlib import Path
import os
import shutil
import subprocess
import threading
import time
from adaptive_research_harness.encoding import decode,require,digest,Refusal
from adaptive_research_harness.clock import durable_write
from adaptive_research_harness.host import generation,still_alive
from adaptive_research_harness.profile import Profile
from adaptive_research_harness.transport import serve,LifetimeLock
from acceptance.catalog import CASES,DEATH_POINTS

BASE=Path('/var/lib/adaptive-research-harness')
RUN=Path('/run/adaptive-research-harness')
ARCHIVE=Path('/var/lib/adaptive-research-harness-acceptance')


def command(*args):return subprocess.check_output(['systemctl',*args],text=True).strip()


def cgroup(unit):
    value=command('show',unit,'--property=ControlGroup','--value')
    return Path('/sys/fs/cgroup'+value) if value.startswith('/') else None


def generations(unit):
    group=cgroup(unit);out=[]
    if group and group.exists():
        for path in group.rglob('cgroup.procs'):
            for pid in path.read_text().split():
                try:out.append(generation(int(pid)))
                except Refusal:pass
    return group,out


class Supervisor:
    def __init__(self,profile,cfg):self.profile=profile;self.cfg=cfg;self.units=cfg['units'];self.lock=threading.Lock()
    def stop(self,units=None):
        units=units or self.units
        before={u:generations(u) for u in units}
        # No socket activation units exist. Mask prevents new queued starts while
        # control-group termination drains already accepted work and descendants.
        command('mask','--runtime',*units)
        command('stop',*units)
        jobs=command('list-jobs','--no-legend','--no-pager').splitlines()
        for line in jobs:
            cols=line.split()
            if len(cols)>1 and cols[1] in units:command('cancel',cols[0])
        remembered=BASE/'supervisor/observed-kills.json'
        killed=decode(remembered.read_bytes()) if remembered.exists() else []
        all_generations=[g for _,gs in before.values() for g in gs]
        if set(self.units)<=set(units):
            all_generations += [g for item in killed for g in item['generations']]
            require(all(not still_alive(g) for g in all_generations),'WORKER_NOT_QUIESCENT')
        empty=[]
        for unit,(group,gs) in before.items():
            if group is None:continue
            require(not group.exists() or 'populated 0' in (group/'cgroup.events').read_text(),'WORKER_NOT_QUIESCENT')
            require(all(not still_alive(g) for g in gs),'WORKER_NOT_QUIESCENT');empty.append(str(group))
        receipt={'kind':'HOST_QUIESCENCE','inventory_sha256':self.profile.inventory_hash,
          'stopped_units':units,'terminated_generations':all_generations,'empty_cgroups':empty,
          'activation_jobs_cancelled':True,'old_channels_closed':True,
          'closed_channels':[str(RUN/s['socket']) for s in self.cfg['services'].values()],
          'proof':'Root stopped and masked fixed units; KillMode=control-group; cgroups empty and recorded generations absent before restart.'}
        core_generations=before.get('harness-core.service',(None,[]))[1]
        if set(self.units)<=set(units):core_generations += [g for item in killed if item['unit']=='harness-core.service' for g in item['generations']]
        for gen in core_generations:
            path=BASE/'supervisor'/(digest(gen)+'.json');durable_write(path,receipt);os.chmod(path,0o644)
        return receipt
    def start(self,units=None):
        units=units or self.units;command('unmask','--runtime',*units);command('start',*units)
        return {'status':'STARTED','units':units}
    def new_case(self,name):
        require(name.split('.')[0] in CASES or name.startswith('D-'),'INVALID_CASE')
        require('/' not in name and '..' not in name and len(name)<100,'INVALID_CASE')
        self.stop()
        current=BASE/'current-case.json';ARCHIVE.mkdir(exist_ok=True,mode=0o755)
        if current.exists():
            old=decode(current.read_bytes())['case'];dest=ARCHIVE/old
            require(not dest.exists(),'CASE_ALREADY_RETAINED');dest.mkdir(mode=0o755)
            for label in self.cfg['services']:
                src=BASE/label
                if src.exists():shutil.move(str(src),str(dest/label))
            shutil.copytree(BASE/'supervisor',dest/'supervisor')
            current.rename(dest/'current-case.json')
        for label,s in self.cfg['services'].items():
            import pwd
            path=BASE/label;path.mkdir(exist_ok=True);os.chown(path,pwd.getpwnam(s['user']).pw_uid,s['gid']);os.chmod(path,0o700)
        durable_write(current,{'case':name,'inventory_sha256':self.profile.inventory_hash});self.start()
        return {'status':'NEW_EMPTY_CASE','case':name,'no_genesis_performed':True}
    def handle(self,who,b):
        require(who['uid']==20001,'UNAUTHORIZED')
        with self.lock:
            op=b['op']
            if op=='new-case':return self.new_case(b['case'])
            if op=='quiesce':return self.stop()
            if op=='restart':
                proof=self.stop();return {'proof':proof,'restart':self.start()}
            if op in ('stop','start','kill'):
                unit=b['unit'];require(unit in self.units,'INVALID_UNIT')
                if op=='stop':return self.stop([unit])
                if op=='start':return self.start([unit])
                group,gens=generations(unit)
                remembered=BASE/'supervisor/observed-kills.json';old=decode(remembered.read_bytes()) if remembered.exists() else []
                durable_write(remembered,old+[{'unit':unit,'generations':gens}])
                command('kill','--signal=KILL','--kill-whom=all',unit)
                deadline=time.monotonic()+5
                while any(still_alive(g) for g in gens) and time.monotonic()<deadline:time.sleep(.05)
                require(all(not still_alive(g) for g in gens),'PROCESS_STILL_ALIVE')
                return {'status':'KILL_REQUESTED','unit':unit,'generations':gens,'not_quiescence_proof':True}
            if op=='barriers':
                return {'barriers':[{'path':str(p),'content':decode(p.read_bytes())} for label in self.cfg['services'] for p in (BASE/label).glob('*.paused')]+[{'path':str(p),'content':decode(p.read_bytes())} for p in (BASE/'core/faults').glob('*.paused')]}
            if op=='release-barrier':
                path=Path(b['path']).resolve();require(path.is_relative_to(BASE) and path.suffix=='.paused' and path.is_file(),'INVALID_BARRIER')
                release=path.with_suffix('.release');durable_write(release,{'root_release':True});os.chmod(release,0o644)
                return {'status':'RELEASED','path':str(path)}
            if op=='pause-actor':
                label=b['actor'];require(label in ('ck1','ck2','r01'),'INVALID_ACTOR')
                require(b['point'] in ('checker_during_computation','checker_after_result'),'INVALID_POINT')
                durable_write(BASE/label/'next-fault.json',{'point':b['point']});os.chmod(BASE/label/'next-fault.json',0o644)
                return {'status':'ARMED'}
            if op=='processes':return {u:{'cgroup':str(generations(u)[0]),'generations':generations(u)[1]} for u in self.units}
            if op=='probe-isolation':return self.probe()
            if op in ('rollback-clock','restore-clock'):
                self.stop(['harness-clock.service'])
                path=BASE/'clock/clock.json';receipts=[decode(line) for line in path.with_suffix('.receipts').read_bytes().splitlines()]
                require(bool(receipts),'CLOCK_UNAVAILABLE')
                value=receipts[0] if op=='rollback-clock' else receipts[-1]
                durable_write(path,value);os.chown(path,20003,20053)
                self.start(['harness-clock.service']);return {'status':'INJECTED' if op=='rollback-clock' else 'RESTORED','value':value}
            if op=='artifact-probe':
                import tempfile
                with tempfile.TemporaryDirectory() as d:
                    root=Path(d)
                    installed=Path('/opt/adaptive-research-harness')
                    for item in self.profile.inventory['files']:
                        dest=root/item['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(installed/item['path'],dest)
                    changed=root/'adaptive_research_harness/checkers/a.py';changed.write_bytes(changed.read_bytes()+b'\n# injected candidate alteration\n')
                    try:self.profile.verify_files(root)
                    except Refusal as exc:return {'status':'CANDIDATE_REFUSED','reason':exc.code,'scope':'Full copy of installed closure; live installed bytes untouched.'}
                    raise Refusal('ARTIFACT_GATE_FAILED')

            if op=='competing-core':
                # Same fixed binary/unit command in a transient systemd unit;
                # it must fail at the stable lifetime lock, before socket setup.
                s=self.cfg['services']['core']
                result=subprocess.run(['systemd-run','--wait','--pipe','--collect','--unit=harness-contender','--uid=harness-core','--gid=harness-clients',
                  '--setenv=PYTHONPATH=/opt/adaptive-research-harness','--setenv=PYTHONDONTWRITEBYTECODE=1',
                  '/usr/bin/python3','-s','-m','isolation.contender'],capture_output=True,text=True)
                return {'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
            raise Refusal('INVALID_SUPERVISOR_OPERATION')
    def probe(self):
        result=[]
        for user in ('harness-r01','harness-tool-a','harness-tool-b'):
            for path,access in [(BASE/'core/harness.sqlite','read'),(Path('/opt/adaptive-research-harness/adaptive_research_harness/engine.py'),'write'),(BASE/'ck1','read')]:
                proc=subprocess.run(['runuser','-u',user,'--','/usr/bin/python3','-c',
                    'import os,sys; p=sys.argv[1]; fd=os.open(p, os.O_RDWR if sys.argv[2]=="write" else os.O_RDONLY); os.close(fd)',str(path),access],capture_output=True,text=True)
                result.append({'user':user,'path':str(path),'access':access,'denied':proc.returncode!=0,'stderr':proc.stderr})
        return {'probes':result}


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--bundle',required=True);p.add_argument('--permit',default=None);args=p.parse_args()
    require(os.getuid()==0,'ROOT_REQUIRED');profile=Profile(args.bundle);profile.approve_run(args.permit,args.root)
    cfg=decode((Path(args.root)/'isolation/generated/accounts.json').read_bytes());supervisor=Supervisor(profile,cfg)
    with LifetimeLock(RUN/'supervisor/supervisor.lock'):serve(RUN/'supervisor/control.sock',supervisor.handle,{20001})

if __name__=='__main__':main()
