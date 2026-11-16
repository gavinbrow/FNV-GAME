"""Synthetic saved outcomes; mock factory auth only, never real inputs."""
import copy,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_actual_factory_join_v1 as join


def fixture():
    root=dict(original_address='0x00401000',symbol='root',size=4);selection=dict(root=root)
    proof={'fixture':'wrapper'};data=b'authored'
    report=dict(verdict='match',address=root['original_address'],symbol='root',size=4,compiled_extent=4,errors=[],relocations=[])
    after=dict(report,symbol='export')
    projection=dict(output_sha256=join.cohort.digest(data),fields=[],exports=['export'],before_comparison=[report],after_comparison=[after])
    entry=dict(root=root,record={'contract':{'fields':[]}},projection=projection,
               assessment={'eligible':True,'strict_zero_consumer_replayed':True})
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

if __name__=='__main__':unittest.main()
