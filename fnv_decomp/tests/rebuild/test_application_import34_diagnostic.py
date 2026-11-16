import copy,sys,unittest,tempfile,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_import34_diagnostic as prep

def fixture():
    prior=['/ALTERNATENAME:cell%d=pointer%d'%(n,n) for n in range(31)];crt=['/ALTERNATENAME:crt%d=provider%d'%(n,n) for n in range(4)];allowed=prior+['/ALTERNATENAME:win%d=winptr%d'%(n,n) for n in range(3)]
    tokens=['/OUT:'+str(Path('old')/'diagnostic.exe'),'/MAP:'+str(Path('old')/'diagnostic.map'),'kernel12.lib','user16.lib','CODE68.lib']+prior+crt
    return ['\n'.join('"'+t+'"' for t in tokens),Path('old'),Path('new'),('kernel12.lib','kernel15.lib'),prior,crt,allowed,allowed,crt]
class Tests(unittest.TestCase):
    def test_replace_only_kernel_and_add_three_aliases(self):
        result=prep.response_tokens(*fixture());self.assertEqual(len(result),43);self.assertNotIn('kernel12.lib',result);self.assertIn('kernel15.lib',result);self.assertIn('CODE68.lib',result);self.assertIn('user16.lib',result);self.assertEqual(sum(t.startswith('/ALTERNATENAME:') for t in result),38)
    def test_disabled_old_alias_or_cookie_tokens_removed(self):
        args=fixture();args[7]=args[6][1:];args[8]=[];result=prep.response_tokens(*args);self.assertNotIn(args[4][0],result);self.assertNotIn(args[5][0],result)
    def test_changed_old_pointer_identity_rejected(self):
        args=fixture();args[6]=list(args[6]);args[6][0]+='changed'
        with self.assertRaises(ValueError):prep.response_tokens(*args)
    def test_unreviewed_steam_or_other_new_alias_rejected(self):
        args=fixture();args[7]=args[7]+['/ALTERNATENAME:steam=unproved']
        with self.assertRaises(ValueError):prep.response_tokens(*args)
    def test_unselected_library_path_or_extra_alias_rejected(self):
        for mode in ('path','alias'):
            args=fixture()
            if mode=='path':args[3]=('wrong-origin.lib','kernel15.lib')
            else:args[0]+='\n"/ALTERNATENAME:unreviewed=other"'
            with self.assertRaises(ValueError):prep.response_tokens(*args)
class NativeTests(unittest.TestCase):
    def fixture(self):
        from test_import_kernel32_fifteen import fixture,request_parse
        import import_kernel32_fifteen as producer
        data=fixture();request,parsed=request_parse();sources={'synthetic-reviewed-producer':'e'*64}
        request['inputs']={key+'_sha256':value for key,value in producer.PINS.items()};request['source_sha256']=sources
        receipt=producer.reconcile(request,parsed,'c'*64);receipt['all_inputs_tools_sources_stable']=True
        originals=dict(zip(('catalog','assessment','assessment_review','prior_native'),data[:4]))
        return receipt,request,'c'*64,parsed,producer,originals,sources
    def test_complete_prepare_and_actual_native_replay(self):self.assertEqual(len(prep.native_evidence(*self.fixture())['proposed_pointer_aliases']),34)
    def test_stale_failed_promoted_or_unstable_native_rejected(self):
        for key,value in [('request_sha256','a'*64),('status','failed'),('alias_applied',True),('old_31_pointer_identities_preserved',False),('all_inputs_tools_sources_stable',False)]:
            args=list(self.fixture());args[0][key]=value
            with self.assertRaises(ValueError):prep.native_evidence(*args)
    def test_changed_actual_library_request_source_or_steam_context_rejected(self):
        for kind in ('bytes','source','Steam','input'):
            args=list(self.fixture())
            if kind=='bytes':args[3]['archive_bytes']+=1
            if kind=='source':args[1]['source_sha256']={}
            if kind=='Steam':args[1]['Steam_remains_unaliased']=False
            if kind=='input':args[1]['inputs']={}
            with self.assertRaises(ValueError):prep.native_evidence(*args)
class ReuseTests(unittest.TestCase):
    def test_full_identity_coverage_preserves_duplicate_provenance(self):
        row=dict(requested_path='selected',path='physical',sha256='a'*64,size=4,device=1,inode=2);observed=[row,row];inherited=[row,row]
        before=copy.deepcopy((observed,inherited));prep.inherited_identity_coverage(observed,inherited);self.assertEqual((observed,inherited),before)
    def test_missing_changed_or_alternative_requested_identity_rejected(self):
        row=dict(requested_path='selected',path='physical',sha256='a'*64,size=4,device=1,inode=2)
        for key,value in [('requested_path','other'),('sha256','b'*64),('inode',3),('size',8)]:
            altered=dict(row);altered[key]=value
            with self.assertRaises(ValueError):prep.inherited_identity_coverage([altered],[row])
        with self.assertRaises(ValueError):prep.inherited_identity_coverage([row],[])
    def test_exact_selected_kernel_path_and_ancestry_required(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder).resolve();old=root/'build/rebuild/import-v8-four-native-v1/kernel32-twelve.lib';old.parent.mkdir(parents=True);old.write_bytes(b'authored fixture')
            sha=hashlib.sha256(old.read_bytes()).hexdigest();request=dict(replacement=dict(old_library=old.name,new_library='kernel32-fifteen.lib',old_library_sha256=sha));paths=dict(kernel_library=root/'new.lib');row=dict(requested_path=str(old),path=str(old),sha256=sha)
            text='"'+str(old)+'"';self.assertEqual(prep.selected_kernel_replacement(root,paths,request,text,[row]),(str(old),str(root/'new.lib')))
            row['requested_path']='unselected-same-bytes'
            with self.assertRaises(ValueError):prep.selected_kernel_replacement(root,paths,request,text,[row])
if __name__=='__main__':unittest.main()
