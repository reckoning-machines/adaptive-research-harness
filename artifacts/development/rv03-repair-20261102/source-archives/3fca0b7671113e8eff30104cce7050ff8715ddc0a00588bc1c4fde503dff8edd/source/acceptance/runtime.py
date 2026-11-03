"""Real-core runtime fixtures. No direct SQL, state seeding or supplied Check outcome."""
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import time
import uuid
from adaptive_research_harness.client import Client
from adaptive_research_harness.encoding import require,Refusal,digest,instant
from adaptive_research_harness.transport import request

RUN=Path('/run/adaptive-research-harness')


def key():return str(uuid.uuid4())


def expect(result,status='COMMITTED',reason=None):
    assert result.get('status')==status,result
    if reason:assert result.get('reason')==reason,result
    return result


class Runtime:
    def __init__(self,case):
        require(os.getuid()==20001,'PRINCIPAL_FIXTURE_UID_REQUIRED')
        self.case=case;self.client=Client(RUN/'core/commands.sock','Principal')
        self.pool=ThreadPoolExecutor(8);self.ordinal=0;self.trace=[]
    def host(self,op,**payload):
        result=request(RUN/'supervisor/control.sock',dict(op=op,**payload));assert result.get('status')!='ERROR',result
        self.trace.append({'host':op,'result':result});return result
    def agent(self,actor,op,payload=None,request_id=None):
        r=request(RUN/actor/'control.sock',{'op':op,'payload':payload or {},'request_id':request_id})
        self.trace.append({'agent':actor,'op':op,'result':r});return r
    def adversarial(self,actor,command,payload,request_id=None):
        return self.agent(actor,'adversarial-command',{'case':self.case.split('.')[0],'command':command,'payload':payload,'request_id':request_id})
    def call(self,op,payload=None,request_id=None):
        r=self.client.call(op,payload,request_id);self.trace.append({'principal':op,'result':r});return r
    def read(self,op,payload=None):return self.client.query(op,payload)
    def ready(self):
        deadline=time.monotonic()+20
        while time.monotonic()<deadline:
            try:
                self.read('profile')
                if all((RUN/x/'control.sock').exists() for x in ['observe','ck1','ck2']+[f'r{i:02d}' for i in range(1,11)]) and (RUN/'clock/clock.sock').exists():return
            except (OSError,EOFError,Refusal):pass
            time.sleep(.05)
        raise AssertionError('Fixed units did not become ready')
    def tick(self,value):
        r=request(RUN/'clock/clock.sock',{'op':'advance','tick':value});assert 'time_ms' in r,r;return r
    def startup(self):
        self.host('new-case',case=self.case);self.ready()
        r=request(RUN/'clock/clock.sock',{'op':'initialize'});assert 'time_ms' in r,r
        return self.startup_records()
    def startup_records(self):
        p=self.read('profile');self.profile=p
        designs={d['content']['AgentDesignVersionId']:d['content'] for d in p['artifacts']['designs']}
        grants={g['content']['AuthorizationId']:g['content'] for g in p['setup']['grants']}
        expect(self.call('genesis',{'constitution_sha256':p['setup']['constitution']['sha256'],'design':designs['AD-CK-1.0'],'grant':grants['AU-CK-A']}))
        self.control('AUTHORIZATION','AU-OBS-1',{'action':'GRANT','predecessor':None,'grant':grants['AU-OBS-1']},tr='TR-1')
        self.tick(1000);self.formation=expect(self.agent('observe','observe'))['refs'][0]
        self.control('LIMITS','initial_limits',p['setup']['initial_limits'],tr='TR-2')
        for i in range(1,11):self.control('AGENT_DESIGN',f'AD-R{i}.0',designs[f'AD-R{i}.0'],tr=f'TR-{i+2}')
        self.control('AGENT_DESIGN','AD-CK-2.0',designs['AD-CK-2.0'],tr='TR-13')
        for n,g in [(14,'AU-CK-B'),(15,'AU-RP-1')]:self.control('AUTHORIZATION',g,{'action':'GRANT','predecessor':None,'grant':grants[g]},tr=f'TR-{n}')
        theme=deepcopy(p['setup']['theme']['content']);theme['motivation_closure']={'N':15,'refs':[self.formation]}
        self.control('THEME','TH-G1',theme,tr='TR-16')
        self.assert_startup();return self
    def propose_control(self,cls,subject,content,tr=None):
        self.ordinal+=1;tr=tr or f'TR-{self.case}-{self.ordinal}'
        payload={'transition_id':tr,'base':self.read('state')['N'],'class':cls,'subject':subject,'content':content,
          'grant':None,'budget':'0.00','funding_ref':None,'delta':{'O':0,'S':0,'A':0}}
        return tr,self.call('propose',payload)
    def check(self,tr,actor='ck1',passed=True):
        c=self.agent(actor,'check',{'transition_id':tr})
        if passed:
            expect(c['check']);assert c['computed_result']=='PASS',c
            return c['check']['refs'][0]['sequence']
        return c
    def decision(self,tr,check,policy=False):
        if policy:return expect(self.call('policy-decide',{'transition_id':tr,'check':check}))['refs'][0]['sequence']
        return expect(self.call('decide',{'transition_id':tr,'check':check,'decision':'ADMITTED','reason':'Exact approved bounded fixture control'}))['refs'][0]['sequence']
    def control(self,cls,subject,content,tr=None,checker='ck1'):
        tr,p=self.propose_control(cls,subject,content,tr);expect(p);check=self.check(tr,checker)
        decision=self.decision(tr,check);applied=expect(self.call('apply',{'transition_id':tr,'decision':decision}))
        return tr,applied
    def assert_startup(self):
        state=self.read('state');assert state['N']==16,state
        assert len([x for x in state['designs'] if x.startswith('AD-R')])==10
        ts=self.history('T');checks=[e for e in ts if e['kind']=='CHECK']
        assert len(checks)==16 and all(x['body']['result']=='PASS' and x['actor']=='AD-CK-1.0' for x in checks)
        assert self.read('budget',{'grant':'AU-CK-A'})['committed']=='4.00'
        assert len({e['body']['attempt'] for e in checks})==16
    def history(self,ledger):
        out=[];after=0;through=None
        while True:
            payload={'ledger':ledger,'after':after,'limit':1000}
            if through is not None:payload['through']=through
            page=self.read('history',payload);out+=page['records'];through=page['through'];after=page['next_after']
            if after>=through or not page['records']:return out
    def reserve(self,actor='r01',amount='3.00',request_id=None):
        i=int(actor[1:]);g=next(x['content'] for x in self.profile['setup']['grants'] if x['content']['AuthorizationId']=='AU-RP-1')
        scope=g['scope_by_grantee'][f'AD-R{i}.0'];purpose={'kind':'Theme','id':scope['themes'][0]} if scope.get('themes') else {'kind':'SearchFamily','id':scope['empirical_search_families'][0]}
        return self.agent(actor,'reserve',{'grant':'AU-RP-1','amount':amount,'purpose':purpose},request_id)
    def research(self,tool='SYN-A-1',stop=False):
        result=self.agent('r01','research',{'tool':tool,'stop_after':'attempt' if stop else None})
        assert result.get('status')!='ERROR',result
        if not stop:expect(result['record']);expect(result['settlement'])
        return result
    def candidate(self):
        rr=self.research()['record']['refs'][0]
        p=self.agent('r01','propose-hypothesis',{'research_ref':rr});expect(p['proposal']);expect(p['funding'])
        return p
    def decided(self):
        p=self.candidate();c=self.check(p['transition_id']);d=self.decision(p['transition_id'],c,True)
        return p,{'transition_id':p['transition_id'],'decision':d}
    def arm(self,target,kind,point=None):
        p={'target':str(target),'kind':kind,'case':self.case.split('.')[0]}
        if point:p['point']=point
        expect(self.call('fixture-fault',p),'ARMED')
    def barrier(self,point=None):
        deadline=time.monotonic()+20
        while time.monotonic()<deadline:
            for b in self.host('barriers')['barriers']:
                body=b['content']
                if point is None or body.get('point')==point:return b
            time.sleep(.05)
        raise AssertionError('Expected real process pause was not reached: '+str(point))
    def bound(self):
        p,request_body=self.decided();k=key();self.arm(k,'PAUSE_AT_BOUNDARY','after_bind_commit')
        future=self.pool.submit(self.call,'apply',request_body,k);self.barrier('after_bind_commit')
        self.host('restart');self.ready()
        binds=[e for e in self.history('E') if e['kind']=='BIND' and e['body']['transition_id']==p['transition_id']]
        assert len(binds)==1;request_body['bind']=binds[0]['seq']
        return p,request_body,binds[0]
    def fence(self,grant='AU-RP-1'):return expect(self.call('fence',{'grant':grant,'reason':self.case+' funding-stop witness'}))
    def revoke(self,grant='AU-RP-1',checker='ck1',action='REVOKE'):
        original=deepcopy(self.read('state')['grants'][grant]);self.ordinal+=1
        original['AuthorizationId']=grant+'-'+self.case+'-'+str(self.ordinal)
        return self.control('AUTHORIZATION',original['AuthorizationId'],{'action':action,'predecessor':grant,'grant':original},checker=checker)
    def settle(self,attempt):return self.agent('r01','settle-pending',{'attempt':attempt})
    def verify_artifacts(self):
        from adaptive_research_harness.profile import Profile
        Profile('/opt/adaptive-research-harness/docs/builds/first_cycle_20261029/run_bundle').verify_files('/opt/adaptive-research-harness')
    def finish(self):
        # A fresh independent process re-reads command histories; no driver state
        # supplies authoritative facts. Kept separate from core model predicates.
        import subprocess,sys
        result=subprocess.run([sys.executable,'-m','acceptance.reader'],capture_output=True,text=True)
        assert result.returncode==0,result.stdout+result.stderr
        self.trace.append({'independent_reader':result.stdout})
        self.pool.shutdown(wait=False,cancel_futures=True)
        return {'case':self.case,'status':'PASS','trace':self.trace}
