"""Authored saved-result shadows; no original/archive/native inputs."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/rebuild'))
import cohort_prepare_shadow as shadow
import application_link_diagnostic as diagnostic


def raw(value):return (json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
def checksum(value):return hashlib.sha256(value).hexdigest()
def response(tokens):return ('\n'.join('"'+s+'"' for s in tokens)+'\n').replace('\n',os.linesep).encode()


def identity(path,sha='a'*64,index=1):
    return dict(requested_path=str(path),path=str(path),sha256=sha,size=99,device=10,inode=index)


def fixture(root,profile='saved-wave8-v1'):
    root=Path(root).resolve();spec=shadow.PROFILE[profile]
    paths={r:root/(('baseline/' if r.startswith('baseline') else 'cohort/')+
            ('link.rsp' if r.endswith('response') else r+'.json')) for r in shadow.ROLES}
    prior_iat=[dict(canonical='_authored_iat_%02d'%i,native_pointer='__imp__Authored%02d'%i,enabled=True,
                    complete_actual_uses=[dict(proof=dict(role='iat-cell',fixture=True))]) for i in range(27)]
    cohort_iat=copy.deepcopy(prior_iat)
    if profile=='saved-wave9-v1':cohort_iat += [dict(canonical='_authored_iat_%02d'%i,native_pointer='__imp__Authored%02d'%i,enabled=True,complete_actual_uses=[]) for i in range(27,31)]
    crt=['/ALTERNATENAME:_fixture_crt_%d=_FixtureCRT%d'%(i,i) for i in range(4)]
    historical={name:identity(shadow.ROOT/'build/rebuild'/rel,index=i+1) for i,(name,(_,rel)) in enumerate(spec['roles'].items())}
    baseline_bindings=[v for name,v in historical.items() if spec['roles'][name][0]=='baseline']
    cohort_bindings=[v for name,v in historical.items() if spec['roles'][name][0]=='cohort']
    for owner,bindings,preparer in [('baseline',baseline_bindings,'application_wave8_diagnostic'),
                                    ('cohort',cohort_bindings,spec['kernel'])]:
        bindings.append(identity(shadow.ROOT/'tools/rebuild'/(preparer+'.py'),shadow.PINS['tools/rebuild/'+preparer+'.py'],100))
    common_code=str(shadow.ROOT/'build/rebuild/authored-base-only.lib')
    prior_aliases=['/ALTERNATENAME:'+r['canonical']+'='+r['native_pointer'] for r in prior_iat]
    new_aliases=['/ALTERNATENAME:'+r['canonical']+'='+r['native_pointer'] for r in cohort_iat]
    old_out=paths['baseline_response'].parent;new_out=paths['cohort_response'].parent
    base_files=[common_code]
    if profile=='saved-wave9-v1':base_files += [historical['old_kernel']['requested_path'],historical['old_user']['requested_path']]
    base_tokens=['/NOLOGO','/OUT:'+str(old_out/'diagnostic.exe'),'/MAP:'+str(old_out/'diagnostic.map')]+base_files+prior_aliases+crt
    target_files=[common_code]
    if profile=='saved-wave9-v1':target_files += [historical['new_kernel']['requested_path'],historical['new_user']['requested_path']]
    expected=response(['/NOLOGO','/OUT:'+str(new_out/'diagnostic.exe'),'/MAP:'+str(new_out/'diagnostic.map')]+
                      target_files+[historical[n]['requested_path'] for n in spec['additions']]+new_aliases+crt)
    def result(kind,bindings,aliases,rsp,bytes_,count):
        return dict(kind=kind,status='prepared-no-native-LINK',command=['C:/AuthoredOnly/link.exe','@'+str(rsp)],response_sha256=checksum(bytes_),
            input_bindings=bindings,provenance={'_fixture':[dict(proof=dict(original_field=7+i,typed_bool=True,nested=[1,False,None])) for i in range(count)]},
            aliases=aliases,CRT_diagnostic_bindings=dict(tokens=crt,inherited_tokens_to_remove=crt,complete_fixture_proof={'arbitrary_complete_payload':[True,1,0,False]}),
            default_libraries={'fixture.lib':{'sha256':'b'*64}},selected_supplementary_providers=[dict(canonical='_fixture',object_sha256='c'*64,original_object_only=True)],
            full_included_field_count=count,selected_game_function_provider_count=10,ordinary_prepared_count=9,native_LINK_performed=False,
            executable_execution=False,runtime_eligible=False,provider_adopted=False,link_ready=False,whole_DATA_included=False,namespace_only=True,
            logical_CODE_address_only_aliases=[],unreviewed_CRT_aliases=[],complete_extra_saved_metadata={'unknown_preserved':[True,1,{'value':'authored-only'}]})
    baseline_bytes=response(base_tokens);base=result(spec['base_kind'],baseline_bindings,prior_iat,paths['baseline_response'],baseline_bytes,2)
    successor=result(spec['kind'],cohort_bindings,cohort_iat,paths['cohort_response'],expected,3)
    blobs=dict(baseline_result=raw(base),baseline_response=baseline_bytes,cohort_result=raw(successor),cohort_response=expected)
    for name in shadow.ROLES-set(blobs):blobs[name]=raw(dict(schema_version=1,kind='authored-saved-review',status='accepted-synthetic',
          whole_saved_receipt_sha256=checksum(blobs['baseline_result' if name.startswith('baseline') else 'cohort_result']),complete_review={'keep':[True,1]}))
    manifest=dict(schema_version=1,kind='cohort-saved-result-shadow-v1',phase='derived-shadow-only',scope='authored-fixture-only',profile=profile,
        kernel_sha256=shadow.PINS,files={name:dict(path=str(paths[name]),sha256=checksum(b)) for name,b in blobs.items()},historical_roles=historical,output_relative='shadow-output')
    return manifest,blobs,expected


def write_case(root,profile='saved-wave8-v1'):
    manifest,blobs,expected=fixture(root,profile)
    for name,b in blobs.items():
        p=Path(manifest['files'][name]['path']);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    path=Path(root).resolve()/'manifest.json';path.write_bytes(raw(manifest));h=shadow.file_hash(path)
    review=dict(schema_version=1,kind='cohort-shadow-source-input-review-v1',approved=True,root_authorized=True,reviewer='authored test reviewer',
        independent_source_input_review_pass=True,historical_validator_results_accepted=True,saved_reviews_accepted=True,manifest_sha256=h,
        kernel_sha256=shadow.PINS,files_sha256={k:v['sha256'] for k,v in manifest['files'].items()},allow_original_archive_native_game=False,
        source_sha256={name:shadow.file_hash(shadow.ROOT/name) for name in shadow.OWNED})
    rp=Path(root).resolve()/'review.json';rp.write_bytes(raw(review))
    return path,h,rp,shadow.file_hash(rp),expected


class CohortShadowTests(unittest.TestCase):
    def test_one_cli_runs_both_authored_profiles_with_same_source_bytes(self):
        initial=shadow.file_hash(shadow.__file__)
        with tempfile.TemporaryDirectory() as td:
            for profile in shadow.PROFILE:
                args=write_case(Path(td)/profile,profile)
                result=subprocess.run([sys.executable,shadow.__file__,'--manifest',str(args[0]),'--manifest-sha256',args[1],
                    '--review',str(args[2]),'--review-sha256',args[3]],capture_output=True,text=True,timeout=30)
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertTrue(json.loads(result.stdout)['response_byte_equivalence'])
                self.assertEqual((args[0].parent/'shadow-output/rederived_response.rsp').read_bytes(),args[4])
                self.assertEqual(shadow.file_hash(shadow.__file__),initial)
        result=subprocess.run([sys.executable,shadow.__file__,'--help'],capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_two_profiles_rederive_bytes_and_preserve_every_saved_json_value(self):
        with tempfile.TemporaryDirectory() as td:
            for profile in shadow.PROFILE:
                manifest,blobs,expected=fixture(Path(td)/profile,profile);original=copy.deepcopy(blobs)
                response_,facts=shadow.evaluate_shadow(manifest,blobs)
                self.assertEqual(response_,expected);self.assertEqual(blobs,original)
                for name,row in facts['preserved'].items():
                    decoded=json.loads(blobs[name]);self.assertEqual(row['canonical_json_sha256'],shadow.digest(decoded))
                    self.assertEqual(row['complete_top_level_sha256'],{k:shadow.digest(v) for k,v in decoded.items()})
                for flag in shadow.FALSE:self.assertIs(facts[flag],False)
                self.assertNotIn('command',facts)

    def test_typed_semantic_digest_distinguishes_bool_from_int(self):
        self.assertNotEqual(shadow.digest({'saved':True}),shadow.digest({'saved':1}))
        self.assertNotEqual(shadow.digest({'saved':False}),shadow.digest({'saved':0}))

    def test_saved_result_added_or_removed_or_changed_fields_fail_raw_seal(self):
        with tempfile.TemporaryDirectory() as td:
            manifest,blobs,_=fixture(td);changed=json.loads(blobs['cohort_result']);changed['extra']='unsealed'
            blobs['cohort_result']=raw(changed)
            with self.assertRaises(ValueError):shadow.evaluate_shadow(manifest,blobs)

    def test_loss_of_complete_normative_rows_is_not_reduced_to_flags(self):
        with tempfile.TemporaryDirectory() as td:
            manifest,blobs,_=fixture(td);value=json.loads(blobs['cohort_result']);value['provenance']['_fixture'].pop()
            blobs['cohort_result']=raw(value);manifest['files']['cohort_result']['sha256']=checksum(blobs['cohort_result'])
            with self.assertRaises(ValueError):shadow.evaluate_shadow(manifest,blobs)

    def test_alias_boolean_substitution_and_nonfinite_json_are_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            manifest,blobs,_=fixture(td);value=json.loads(blobs['cohort_result']);value['aliases'][0]['enabled']=1
            blobs['cohort_result']=raw(value);manifest['files']['cohort_result']['sha256']=checksum(blobs['cohort_result'])
            with self.assertRaises(ValueError):shadow.evaluate_shadow(manifest,blobs)
        for bad in ['{"x":NaN}','{"x":Infinity}','{"x":-Infinity}','{"x":1,"x":1}']:
            with self.assertRaises(ValueError):shadow.strict_json(bad)

    def test_exact_historical_origin_path_and_binding_not_bytehash_alone(self):
        with tempfile.TemporaryDirectory() as td:
            manifest,blobs,_=fixture(td,'saved-wave9-v1');manifest['historical_roles']['old_user']['path']='C:/authored/origin-user.lib'
            with self.assertRaises(ValueError):shadow.evaluate_shadow(manifest,blobs)
        with tempfile.TemporaryDirectory() as td:
            manifest,blobs,_=fixture(td);manifest['historical_roles']['code']['inode']+=1
            with self.assertRaises(ValueError):shadow.evaluate_shadow(manifest,blobs)

    def test_publication_directory_never_replaces_historical_response_out(self):
        with tempfile.TemporaryDirectory() as td:
            manifest,blobs,expected=fixture(td);value=json.loads(blobs['cohort_result'])
            manifest['files']['cohort_response']['path']=str(Path(td).resolve()/'shadow-output/link.rsp')
            value['command'][1]='@'+manifest['files']['cohort_response']['path'];blobs['cohort_result']=raw(value)
            manifest['files']['cohort_result']['sha256']=checksum(blobs['cohort_result'])
            with self.assertRaisesRegex(ValueError,'response bytes'):shadow.evaluate_shadow(manifest,blobs)

    def test_missing_extra_cross_cohort_and_large_blob_inputs_are_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            manifest,blobs,_=fixture(td)
            for changed in ({k:v for k,v in blobs.items() if k!='cohort_input_review'},dict(blobs,extra=b'{}')):
                with self.assertRaises(ValueError):shadow.evaluate_shadow(manifest,changed)
            with patch.object(shadow,'MAX_FILE_BYTES',8),self.assertRaises(ValueError):shadow.evaluate_shadow(manifest,blobs)
            manifest['profile']='saved-wave9-v1'
            with self.assertRaises(ValueError):shadow.evaluate_shadow(manifest,blobs)

    def test_derived_only_run_copies_full_results_and_never_opens_historical_libraries(self):
        with tempfile.TemporaryDirectory() as td:
            args=write_case(td,'saved-wave9-v1');original_open=Path.open;opened=[]
            def guarded(path,*a,**kw):
                opened.append(str(path));self.assertNotIn(path.suffix.lower(),('.lib','.obj','.exe'))
                return original_open(path,*a,**kw)
            with patch.object(Path,'open',guarded):result=shadow.run(*args[:4])
            out=Path(td)/'shadow-output';manifest=json.loads(Path(args[0]).read_text())
            for role in ('baseline_result','cohort_result'):
                self.assertEqual((out/(role+'.json')).read_bytes(),Path(manifest['files'][role]['path']).read_bytes())
            self.assertEqual((out/'rederived_response.rsp').read_bytes(),args[4]);self.assertTrue((out/'shadow-result.json').exists())
            self.assertFalse(result['fresh_original_inputs_checked'])

    def test_output_drift_retracts_only_owned_terminal(self):
        with tempfile.TemporaryDirectory() as td:
            args=write_case(td);original=diagnostic.stable;calls=[]
            def tamper(bindings):
                calls.append(1)
                if len(calls)==4:(Path(td)/'shadow-output/cohort_result.json').write_bytes(b'changed output')
                original(bindings)
            with patch.object(diagnostic,'stable',side_effect=tamper),self.assertRaises(ValueError):shadow.run(*args[:4])
            self.assertFalse((Path(td)/'shadow-output/shadow-result.json').exists())


if __name__=='__main__':unittest.main()
