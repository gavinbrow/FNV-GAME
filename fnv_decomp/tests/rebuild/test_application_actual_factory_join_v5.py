"""Synthetic saved outcomes; mock factory auth only, never real inputs."""
import copy,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_actual_factory_join_v5 as join


def fixture():
    root=dict(original_address='0x00401000',symbol='root',size=4);selection=dict(root=root,authority=dict(contract_identity_sha256='contract',certificate_sha256='cert'))
    proof={'fixture':'wrapper'};data=b'authored'
    report=dict(verdict='match',address=root['original_address'],symbol='root',size=4,compiled_extent=4,errors=[],relocations=[])
    after=dict(report,symbol='export')
    projection=dict(output_sha256=join.cohort.digest(data),fields=[],exports=['export'],before_comparison=[report],after_comparison=[after])
    entry=dict(root=root,record={'contract':{'fields':[]}},projection=projection,
               assessment={'eligible':True,'blockers':[],'strict_zero_consumer_replayed':True,'serialization_performed':False,
                           'requested_roots':[root],'contract_identity_sha256':'contract','certificate_sha256':'cert'})
    outcome=dict(root=root,status='emitted',evidence=dict(original_plain_match=True,staged_plain_match=True,strict_reparse=True,complete_field_proof=True))
    return dict(selections=[selection],outcomes=[outcome],emitted=[entry],members=[dict(name='x.obj',projection=projection)],
                wrappers=[proof],member_bytes={'x.obj':data})


def check(args):
    with patch.object(join.factory,'validate_selected'),patch.object(join.driver,'field_proof_record',return_value={'fixture':'wrapper'}):
        return join.validate(**args)

class Tests(unittest.TestCase):
    def test_saved_evidence_grants_no_approval(self):
        result=check(fixture());self.assertTrue(result['saved_evidence_only']);self.assertFalse(result['link_approved'])
    def test_changed_or_missing_match_not_accepted(self):
        for mode in ('size','relocation','outcome','wrapper','bytes'):
            f=copy.deepcopy(fixture());p=f['members'][0]['projection']
            if mode=='size': p['before_comparison'][0]['compiled_extent']=3
            elif mode=='relocation': p['after_comparison'][0]['relocations']=[{'match':False,'expected':'a','observed':'b'}]
            elif mode=='outcome':f['outcomes'][0]['evidence']['staged_plain_match']=False
            elif mode=='wrapper':f['wrappers'][0]['fixture']='altered'
            else:f['member_bytes']['x.obj']=b'other'
            with self.subTest(mode=mode),self.assertRaises(ValueError):check(f)
    def test_subset_is_terminal_not_requested_forecast(self):
        f=fixture();f['selections'].append(dict(root=dict(original_address='0x00402000',symbol='other',size=4)))
        with self.assertRaises(ValueError):check(f)

    def test_comparison_relocations_match_full_contract_geometry(self):
        f=fixture();field=dict(source_field_offset=1,expected_original_target_va='0x12345678',coff_relocation={'kind':6})
        f['emitted'][0]['record']['contract']['fields']=[field]
        f['emitted'][0]['assessment']=dict(eligible=True,blockers=[],fields=[{'x':1}],exports=['export'],serialization_performed=False, **{k:False for k in ('provider_selected','runtime_eligible','ABI_verified','link_ready','native_tools_run','compiler_performed','executable_link_performed','game_execution_performed')})
        p=f['members'][0]['projection'];p['fields']=[{'x':1}]
        rel=dict(offset=1,kind=6,expected='0x12345678',observed='0x12345678',match=True)
        p['before_comparison'][0]['relocations']=[copy.deepcopy(rel)];p['after_comparison'][0]['relocations']=[copy.deepcopy(rel)]
        check(f)
        for key,value in [('offset',999),('kind',20),('expected','0x99999999')]:
            bad=copy.deepcopy(f); rr=bad['members'][0]['projection']['before_comparison'][0]['relocations'][0];rr[key]=value
            if key=='expected':rr['observed']=value
            with self.subTest(key=key),self.assertRaises(ValueError):check(bad)

    def test_assessment_blocker_or_zero_contract_identity_rejected(self):
        for key,value in [('blockers',['blocked']),('certificate_sha256','other'),('serialization_performed',True)]:
            f=fixture();f['emitted'][0]['assessment'][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):check(f)

    def test_nonzero_assessment_promotion_rejected(self):
        f=fixture();field=dict(source_field_offset=1,expected_original_target_va='0x12345678',coff_relocation={'kind':6})
        f['emitted'][0]['record']['contract']['fields']=[field];p=f['members'][0]['projection'];p['fields']=[{'x':1}]
        rel=dict(offset=1,kind=6,expected='0x12345678',observed='0x12345678',match=True)
        p['before_comparison'][0]['relocations']=[copy.deepcopy(rel)];p['after_comparison'][0]['relocations']=[copy.deepcopy(rel)]
        a=dict(eligible=True,blockers=[],fields=[{'x':1}],exports=['export'],serialization_performed=False, **{k:False for k in ('provider_selected','runtime_eligible','ABI_verified','link_ready','native_tools_run','compiler_performed','executable_link_performed','game_execution_performed')})
        f['emitted'][0]['assessment']=a;check(f)
        for key in ('provider_selected','runtime_eligible','serialization_performed'):
            bad=copy.deepcopy(f);bad['emitted'][0]['assessment'][key]=True
            with self.subTest(key=key),self.assertRaises(ValueError):check(bad)

    def test_zero_field_extra_promotion_rejected(self):
        for key in ('provider_selected','runtime_eligible','link_ready'):
            f=fixture();f['emitted'][0]['assessment'][key]=True
            with self.subTest(key=key),self.assertRaises(ValueError):check(f)

if __name__=='__main__':unittest.main()
