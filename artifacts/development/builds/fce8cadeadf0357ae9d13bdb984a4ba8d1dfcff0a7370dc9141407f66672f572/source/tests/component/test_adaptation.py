from copy import deepcopy
import unittest
from adaptive_research_harness.actors import next_experiment
from adaptive_research_harness.tools_a import calculate
from adaptive_research_harness.encoding import Refusal,digest
from adaptive_research_harness.checkers import a,b
from .fabricated import profile,Input


class Adaptation(unittest.TestCase):
    def test_single_shock_selects_complement_control(self):
        doc=profile().artifacts['formation_cohort']['content'];before=deepcopy(doc)
        choice=next_experiment(calculate(doc),doc)
        self.assertEqual(choice['id'],'complement-control');self.assertTrue(choice['initial_failure'])
        self.assertEqual(doc,before)
    def test_changed_evidence_changes_next_experiment(self):
        doc=deepcopy(profile().artifacts['formation_cohort']['content']);doc['rows'][1]['shock_id']='new-independent-shock'
        choice=next_experiment(calculate(doc),doc)
        self.assertEqual(choice['id'],'independent-reproduction');self.assertIsNone(choice['initial_failure'])
    def test_no_large_sample_does_not_invent_a_candidate(self):
        doc=deepcopy(profile().artifacts['formation_cohort']['content'])
        for row in doc['rows']:row['size_units']=1
        with self.assertRaises(Refusal):next_experiment(calculate(doc),doc)
    def test_both_checkers_reject_forged_control_result(self):
        x=Input();p,_=x.hypothesis();rr=x.e[1]
        rr['body']['result']['adaptation']={'id':'complement-control','comparison_n':10,'comparison_k':9,'passes':True,'selection_ref':{'sequence':rr['seq'],'sha256':rr['sha256']}}
        rr['body']['reproducibility']['result_hash']=digest(rr['body']['result']);rr['sha256']=digest(rr['body'])
        p['body']['content']['motivation_closure']['refs'][1]['sha256']=rr['sha256']
        for checker in (a,b):
            result=checker.evaluate(x.snapshot(),p['transition_id'],'AD-CK-1.0','AU-CK-A',999,x.profile_dict())
            self.assertEqual(result['result'],'FAIL');self.assertEqual(result['criteria']['recomputation']['status'],'NOT MET')

    def test_both_checkers_accept_recomputed_control(self):
        x=Input();selection=x.add('E','RESEARCH_RECORD',{'kind':'SELECTION'},'AD-R1.0')
        p,_=x.hypothesis();rr=next(e for e in x.e if e['kind']=='RESEARCH_RECORD' and e['body'].get('result'))
        ref={'ledger':'E','sequence':selection['seq'],'sha256':selection['sha256']}
        rr['body']['result']['adaptation']={'id':'complement-control','comparison_n':10,'comparison_k':6,'passes':False,'selection_ref':ref}
        rr['body']['reproducibility']['result_hash']=digest(rr['body']['result']);rr['sha256']=digest(rr['body'])
        p['body']['content']['motivation_closure']['refs']=[p['body']['content']['motivation_closure']['refs'][0],ref,{'ledger':'E','sequence':rr['seq'],'sha256':rr['sha256']}]
        for checker in (a,b):
            result=checker.evaluate(x.snapshot(),p['transition_id'],'AD-CK-1.0','AU-CK-A',999,x.profile_dict())
            self.assertEqual(result['result'],'PASS',result['criteria'])
