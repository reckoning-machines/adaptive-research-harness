"""Render fixed Linux units/account manifests into this tree. Build only."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'isolation/generated'
INSTALL='/opt/adaptive-research-harness'
BUNDLE=INSTALL+'/docs/builds/first_cycle_20261029/run_bundle'
RUN='/run/adaptive-research-harness'
STATE='/var/lib/adaptive-research-harness'
COMMON=f'--bundle {BUNDLE} --root {INSTALL} --run-approval /etc/adaptive-research-harness/run-approval.json'


def render():
    OUT.mkdir(exist_ok=True)
    accounts=[('harness-core',20000,20050),('harness-principal',20001,20054),('harness-observe',20002,20054),('harness-clock',20003,20053),('harness-ck1',20011,20054),('harness-ck2',20012,20054)]
    accounts += [(f'harness-r{i:02d}',20020+i,20054) for i in range(1,11)]
    accounts += [('harness-tool-a',20101,20101),('harness-tool-b',20102,20102)]
    groups={'harness-clients':20050,'harness-clock-channel':20053,'harness-control':20054,'harness-tool-a':20101,'harness-tool-b':20102}
    services={}
    services['core']={'user':'harness-core','gid':20050,'state':'core','socket':'core/commands.sock',
      'command':f'serve {COMMON} --socket {RUN}/core/commands.sock --state {STATE}/core --clock-socket {RUN}/clock/clock.sock --tool-a-socket {RUN}/tool-a/tool.sock --tool-b-socket {RUN}/tool-b/tool.sock --supervisor-receipts {STATE}/supervisor',
      'groups':'harness-clock-channel harness-tool-a harness-tool-b','paths':[STATE+'/core']}
    services['clock']={'user':'harness-clock','gid':20053,'state':'clock','socket':'clock/clock.sock','command':f'clock-service {COMMON} --socket {RUN}/clock/clock.sock --state {STATE}/clock','groups':'','paths':[STATE+'/clock']}
    for label,tool in [('tool-a','SYN-A-1'),('tool-b','SYN-B-1')]:
        services[label]={'user':'harness-'+label,'gid':20101 if label=='tool-a' else 20102,'state':label,'socket':label+'/tool.sock',
          'command':f'tool-service {COMMON} --tool {tool} --socket {RUN}/{label}/tool.sock --state {STATE}/{label}','groups':'','paths':[STATE+'/'+label]}
    actors={'observe':'Observation function','ck1':'AD-CK-1.0','ck2':'AD-CK-2.0'}
    actors.update({f'r{i:02d}':f'AD-R{i}.0' for i in range(1,11)})
    for label,actor in actors.items():
        services[label]={'user':'harness-'+label,'gid':20054,'state':label,'socket':label+'/control.sock','command':f'actor-service {COMMON} --actor "{actor}" --socket {RUN}/{label}/control.sock --state {STATE}/{label} --core-socket {RUN}/core/commands.sock','groups':'harness-clients','paths':[STATE+'/'+label]}
    units=[]
    for label,s in services.items():
        unit='harness-'+label+'.service';units.append(unit)
        content=f'''[Unit]
Description=Adaptive Research Harness fixed {label} process
After=local-fs.target

[Service]
Type=simple
User={s['user']}
Group={s['gid']}
SupplementaryGroups={s['groups']}
WorkingDirectory={INSTALL}
Environment=PYTHONPATH={INSTALL} PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
ExecStart=/usr/bin/python3 -s -m adaptive_research_harness {s['command']}
Restart=no
KillMode=control-group
SendSIGKILL=yes
TimeoutStopSec=5
UMask=0027
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
PrivateNetwork=yes
RestrictAddressFamilies=AF_UNIX
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
RestrictSUIDSGID=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes
CapabilityBoundingSet=
ReadWritePaths={RUN}/{label} {' '.join(s['paths'])}

[Install]
WantedBy=multi-user.target
'''
        (OUT/unit).write_text(content)
    (OUT/'accounts.json').write_text(json.dumps({'accounts':[{'name':n,'uid':u,'gid':g} for n,u,g in accounts], 'groups':groups,
       'supplementary':{'harness-principal':['harness-clients','harness-clock-channel'],'harness-core':['harness-clock-channel','harness-tool-a','harness-tool-b'],**{'harness-'+label:['harness-clients'] for label in actors}},
       'services':services,'units':units},indent=2)+'\n')
    (OUT/'harness-supervisor.service').write_text(f'''[Unit]
Description=Adaptive Research Harness disposable test supervisor
After=local-fs.target
[Service]
Type=simple
User=root
Group=harness-control
WorkingDirectory={INSTALL}
Environment=PYTHONPATH={INSTALL} PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
ExecStart=/usr/bin/python3 -s -m isolation.supervisor --root {INSTALL} --bundle {BUNDLE} --permit /etc/adaptive-research-harness/run-approval.json
Restart=no
UMask=0027
''')

if __name__=='__main__':render()
