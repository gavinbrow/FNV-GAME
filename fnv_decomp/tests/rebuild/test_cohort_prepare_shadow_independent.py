"""Independent derived-only shadow checks against authored saved results."""
from pathlib import Path
import copy
import hashlib
import json
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cohort_prepare_shadow as shadow
from test_cohort_prepare_shadow import fixture,write_case


def replace_json(manifest,blobs,role,value):
    blobs[role]=(json.dumps(value,sort_keys=True)+'\n').encode()
    manifest['files'][role]['sha256']=hashlib.sha256(blobs[role]).hexdigest()


class IndependentPureShadowTests(unittest.TestCase):
    def test_both_profiles_keep_full_raw_and_typed_provenance_identity(self):
        for profile in shadow.PROFILE:
            with tempfile.TemporaryDirectory() as td:
                manifest,blobs,expected=fixture(Path(td),profile)
                for role in ('baseline_result','cohort_result'):
                    value=json.loads(blobs[role]);value['opaque_preserved_group']={'nested':[True,1,False,0,{'all':'kept'}]}
                    replace_json(manifest,blobs,role,value)
                before=copy.deepcopy((manifest,blobs));response,facts=shadow.evaluate_shadow(manifest,blobs)
                self.assertEqual(response,expected);self.assertEqual((manifest,blobs),before)
                self.assertTrue(facts['response_byte_equivalence']);self.assertTrue(all(facts[k] is False for k in shadow.FALSE))
                for role,info in facts['preserved'].items():
                    value=shadow.strict_json(blobs[role].decode())
                    self.assertEqual(info['raw_sha256'],hashlib.sha256(blobs[role]).hexdigest())
                    self.assertEqual(info['canonical_json_sha256'],shadow.digest(value))
                    self.assertEqual(info['complete_top_level_sha256'],{k:shadow.digest(v) for k,v in value.items()})
                self.assertNotEqual(shadow.digest(True),shadow.digest(1));self.assertNotEqual(shadow.digest(False),shadow.digest(0))

    def test_no_historical_library_path_is_resolved_statted_or_opened(self):
        for profile in shadow.PROFILE:
            with tempfile.TemporaryDirectory() as td:
                manifest,blobs,expected=fixture(Path(td),profile)
                historical={b['path'] for b in manifest['historical_roles'].values()}
                methods={name:getattr(Path,name) for name in ('resolve','stat','open','read_bytes')}
                def guarded(name):
                    def call(path,*a,**kw):
                        if str(path) in historical:raise AssertionError('historical library filesystem access: '+str(path))
                        return methods[name](path,*a,**kw)
                    return call
                from contextlib import ExitStack
                with ExitStack() as stack:
                    for name in methods:stack.enter_context(patch.object(Path,name,guarded(name)))
                    self.assertEqual(shadow.evaluate_shadow(manifest,blobs)[0],expected)

    def test_rebinding_wrong_origin_or_numeric_alias_cannot_substitute_history(self):
        for mode in ('origin','hash','bool_size','missing','duplicate_conflict'):
            with tempfile.TemporaryDirectory() as td:
                manifest,blobs,_=fixture(Path(td),'saved-wave9-v1');role='old_user';binding=manifest['historical_roles'][role]
                if mode=='origin':binding['requested_path']=binding['path']=str(Path(binding['path']).with_name('origin-user.lib'))
                elif mode=='hash':binding['sha256']='f'*64
                elif mode=='bool_size':binding['size']=True
                else:
                    value=json.loads(blobs['baseline_result'])
                    if mode=='missing':value['input_bindings']=[b for b in value['input_bindings'] if b['requested_path']!=binding['requested_path']]
                    else:
                        wrong=copy.deepcopy(binding);wrong['inode']+=1;value['input_bindings'].append(wrong)
                    replace_json(manifest,blobs,'baseline_result',value)
                with self.subTest(mode=mode),self.assertRaises(ValueError):shadow.evaluate_shadow(manifest,blobs)

    def test_response_alias_or_complete_result_substitution_is_fatal(self):
        for mode in ('response','command','crt','field_count','count_bool','missing_group','alias_enabled'):
            with tempfile.TemporaryDirectory() as td:
                manifest,blobs,_=fixture(Path(td),'saved-wave8-v1')
                if mode=='response':
                    blobs['cohort_response']+=b'"/FORCE"\n';manifest['files']['cohort_response']['sha256']=hashlib.sha256(blobs['cohort_response']).hexdigest()
                else:
                    value=json.loads(blobs['cohort_result'])
                    if mode=='command':value['command'][1]='@'+str(Path(td)/'shadow-output/link.rsp')
                    elif mode=='crt':value['CRT_diagnostic_bindings']['inherited_tokens_to_remove']=[]
                    elif mode=='field_count':value['full_included_field_count']+=1
                    elif mode=='count_bool':value['ordinary_prepared_count']=True
                    elif mode=='missing_group':del value['provenance']
                    else:value['aliases'][0]['enabled']=1
                    replace_json(manifest,blobs,'cohort_result',value)
                with self.subTest(mode=mode),self.assertRaises(ValueError):shadow.evaluate_shadow(manifest,blobs)

    def test_duplicate_JSON_nonfinite_and_blob_bounds_fail_closed(self):
        for raw in (b'{"key":1,"key":2}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":-Infinity}'):
            with self.subTest(raw=raw),self.assertRaises(ValueError):shadow.strict_json(raw.decode())
        with tempfile.TemporaryDirectory() as td:
            manifest,blobs,_=fixture(Path(td),'saved-wave8-v1')
            with patch.object(shadow,'MAX_FILE_BYTES',1):
                with self.assertRaises(ValueError):shadow.evaluate_shadow(manifest,blobs)
            with patch.object(shadow,'MAX_TOTAL_BYTES',1):
                with self.assertRaises(ValueError):shadow.evaluate_shadow(manifest,blobs)

    def test_loaded_prototype_inventory_or_kernel_substitution_is_fatal(self):
        for mode in ('prototype','inventory','kernel'):
            with tempfile.TemporaryDirectory() as td:
                with self.subTest(mode=mode):
                    if mode=='prototype':
                        with patch.object(shadow.prototype,'__file__',str(Path(td)/'cohort_prepare_manifest.py')):
                            with self.assertRaises(ValueError):shadow.source_gate()
                    elif mode=='inventory':
                        with patch.object(shadow.inventory_tools,'__file__',str(Path(td)/'coff_inventory.py')):
                            with self.assertRaises(ValueError):shadow.source_gate()
                    else:
                        with patch.object(shadow.prototype,'kernels',return_value={'application_link_diagnostic':SimpleNamespace(__file__=str(Path(td)/'fake.py'))}):
                            with self.assertRaises(ValueError):shadow.source_gate()


class IndependentShadowDriverTests(unittest.TestCase):
    def test_malformed_review_refuses_before_any_saved_role_read(self):
        for mode in ('extra_permission','reviewer','source_digest','unaccepted'):
            with tempfile.TemporaryDirectory() as td:
                args=list(write_case(td));manifest=json.loads(args[0].read_text());review=json.loads(args[2].read_text())
                if mode=='extra_permission':review['allow_native_tools']=True
                elif mode=='reviewer':review['reviewer']=['truthy non-string']
                elif mode=='source_digest':review['source_sha256'][next(iter(review['source_sha256']))]=True
                else:review['saved_reviews_accepted']=False
                args[2].write_bytes((json.dumps(review)+'\n').encode());args[3]=shadow.file_hash(args[2])
                role_paths={v['path'] for v in manifest['files'].values()};read=Path.read_bytes;opened=[]
                def record(path,*a,**kw):opened.append(str(path));return read(path,*a,**kw)
                with patch.object(Path,'read_bytes',record),self.subTest(mode=mode),self.assertRaises(ValueError):shadow.run(*args[:4])
                self.assertFalse(role_paths.intersection(opened));self.assertFalse((Path(td)/'shadow-output').exists())

    def test_all_eight_raw_inputs_preserved_and_rerun_does_not_change_terminal(self):
        with tempfile.TemporaryDirectory() as td:
            args=write_case(td,'saved-wave9-v1');manifest=json.loads(args[0].read_text())
            result=shadow.run(*args[:4]);out=Path(td)/'shadow-output';terminal=(out/'shadow-result.json').read_bytes()
            for role,ref in manifest['files'].items():
                suffix='.rsp' if role.endswith('response') else '.json'
                self.assertEqual((out/(role+suffix)).read_bytes(),Path(ref['path']).read_bytes())
            self.assertTrue(result['historical_snapshot_acceptance_external']);self.assertFalse(result['pure_evaluation_admission_verified'])
            self.assertTrue(all(result[k] is False for k in shadow.FALSE));self.assertNotIn('command',result)
            with self.assertRaises(ValueError):shadow.run(*args[:4])
            self.assertEqual((out/'shadow-result.json').read_bytes(),terminal)

    def test_saved_input_drift_after_evaluation_cannot_publish_success(self):
        import application_link_diagnostic as diagnostic
        with tempfile.TemporaryDirectory() as td:
            args=write_case(td);manifest=json.loads(args[0].read_text());calls=[];stable=diagnostic.stable
            def drift(bindings):
                calls.append(1)
                if len(calls)==2:Path(manifest['files']['cohort_input_review']['path']).write_bytes(b'changed saved review')
                return stable(bindings)
            with patch.object(diagnostic,'stable',side_effect=drift),self.assertRaises(ValueError):shadow.run(*args[:4])
            self.assertFalse((Path(td)/'shadow-output/shadow-result.json').exists())

    def test_foreign_terminal_race_is_preserved_on_exclusive_publish_failure(self):
        with tempfile.TemporaryDirectory() as td:
            args=write_case(td);foreign=b'foreign terminal created by authored race'
            def occupied(source,target):Path(target).write_bytes(foreign);raise FileExistsError('authored publication collision')
            with patch.object(shadow.os,'link',side_effect=occupied),self.assertRaises(FileExistsError):shadow.run(*args[:4])
            self.assertEqual((Path(td)/'shadow-output/shadow-result.json').read_bytes(),foreign)


if __name__=='__main__':unittest.main()
