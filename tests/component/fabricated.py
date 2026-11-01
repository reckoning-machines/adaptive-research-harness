"""FABRICATED PURE-FUNCTION INPUT ONLY. Never an admitted history or runtime fixture.

These dictionaries exercise calculations. No Store, Engine, socket or Apply 0
is invoked; they cannot be used as acceptance initialization.
"""
from copy import deepcopy
from pathlib import Path
from adaptive_research_harness.profile import Profile,CV1
from adaptive_research_harness.encoding import digest,instant
from adaptive_research_harness.model import View
from adaptive_research_harness.actors import event_ref,invocation
ROOT=Path(__file__).resolve().parents[2]


_BUNDLE=None
def bundle():
    """A disposable bundle frozen from the current tree, once per process. The historical bundle under docs/builds is a record of an older tree."""
    global _BUNDLE
    if _BUNDLE is None:
        import os,uuid
        from build_support.freeze import freeze
        _BUNDLE=ROOT/'artifacts/development/run-bundles'/('component-'+uuid.uuid4().hex)/'bundle';freeze(_BUNDLE)
    return _BUNDLE
def profile():return Profile(bundle())


class Input:
    def __init__(self,full=True):
        self.profile=profile();self.e=[];self.t=[];self.n=0
        self.now=instant(self.profile.setup['clock']['epoch'])+1000
        self.add('T','APPLIED',{'n':0,'genesis':{'constitution_sha256':CV1,
            'design':self.profile.designs['AD-CK-1.0'],'grant':self.profile.grants['AU-CK-A']}},'Principal','FABRICATED-0')
        if full:
            for _,cls,subject,c in self.startup():self.fake_membership(cls,subject,c)
    def add(self,ledger,kind,body,actor='Principal',tr=None):
        rows=self.e if ledger=='E' else self.t
        e={'seq':len(rows)+1,'kind':kind,'actor':actor,'body':deepcopy(body),'sha256':digest(body),'time_ms':self.now}
        if ledger=='T':e['transition_id']=tr
        rows.append(e);return e
    def view(self):return View(self.e,self.t)
    def snapshot(self):return dict(self.view().export(),time_ms=self.now)
    def profile_dict(self):return {'setup':self.profile.setup,'artifacts':self.profile.artifacts,'inventory':self.profile.inventory}
    def propose(self,cls,subject,c,actor='Principal',tr=None,**kw):
        tr=tr or 'FABRICATED-'+str(len(self.t)+1)
        body=dict(transition_id=tr,base=self.n,**{'class':cls},subject=subject,content=deepcopy(c),budget='0.00',grant=None,funding_ref=None,delta={'O':0,'S':0,'A':0});body.update(kw)
        return self.add('T','PROPOSED',body,actor,tr)
    def fake_membership(self,cls,subject,c):
        p=self.propose(cls,subject,c);self.n+=1
        self.add('T','APPLIED',{'n':self.n,'bind':None},'Principal',p['transition_id'])
    def startup(self):
        p=self.profile
        yield 1,'AUTHORIZATION','AU-OBS-1',{'action':'GRANT','predecessor':None,'grant':p.grants['AU-OBS-1']}
        doc=p.artifacts['formation_cohort']['content']
        if not self.e:self.add('E','OBSERVATION',{'form':'DOCUMENT','document':doc,'synthetic':True},'Observation function')
        yield 2,'LIMITS','initial_limits',p.setup['initial_limits']
        for i in range(1,11):yield i+2,'AGENT_DESIGN',f'AD-R{i}.0',p.designs[f'AD-R{i}.0']
        yield 13,'AGENT_DESIGN','AD-CK-2.0',p.designs['AD-CK-2.0']
        for i,g in [(14,'AU-CK-B'),(15,'AU-RP-1')]:yield i,'AUTHORIZATION',g,{'action':'GRANT','predecessor':None,'grant':p.grants[g]}
        c=deepcopy(p.setup['theme']['content']);c['motivation_closure']={'N':self.n,'refs':[event_ref(self.e[0])]}
        yield 16,'THEME','TH-G1',c
    def reservation(self,amount='3.00',actor='AD-R1.0',grant='AU-RP-1',purpose=None):
        return self.add('E','RESERVATION',{'actor':actor,'lineage':self.view().lineage(actor),'grant':grant,'amount':amount,
            'purpose':purpose or {'kind':'Theme','id':'TH-G1'},'expiry_ms':self.now+604800000},actor)
    def attempt(self,r=None,actor='AD-R1.0'):
        r=r or self.reservation(actor=actor)
        inp=invocation(self.profile_dict(),'SYN-A-1','research-counts',[event_ref(self.e[0])],{'threshold':2})
        return self.add('E','ATTEMPT',{'reservation':r['seq'],'actor':actor,'grant':r['body']['grant'],'lineage':self.view().lineage(actor),
            'maximum':'1.00','input':inp,'input_hash':digest(inp),'step':'research-counts','dispatch_index':0,'tier':1,'admission_generation':None},actor)
    def hypothesis(self):
        doc=self.e[0]['body']['document'];result={'n':12,'k':8,'n_large':2,'k_large':2,'synthetic':True,'input_sha256':digest(doc)}
        rr=self.add('E','RESEARCH_RECORD',{'result':result,'reproducibility':{'result_hash':digest(result)}},'AD-R1.0')
        c=deepcopy(self.profile.artifacts['hypothesis_template']['content']);c['motivated_by']=['TH-G1',event_ref(rr)]
        c['motivation_closure']={'N':self.n,'refs':[event_ref(self.e[0]),event_ref(rr)]}
        p=self.propose('HYPOTHESIS',c['HypothesisId'],c,'AD-R1.0',budget='2.00',grant='AU-RP-1',funding_ref=len(self.e)+1)
        r=self.reservation('2.00',purpose={'kind':'Transition','id':p['transition_id']})
        return p,r
