"""Two authored cohorts and adversarial schema/path/byte tests; no game inputs."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/rebuild'))
import cohort_prepare_manifest as subject
import application_link_diagnostic as diagnostic
import application_wave8_diagnostic as wave8
import application_wave9_diagnostic as wave9


def response(tokens):
    # Authored expected bytes, independently assembled rather than producer output.
    return ('\n'.join('"'+token+'"' for token in tokens)+'\n').replace('\n',os.linesep).encode()


def save_manifest(path, value):
    path.write_bytes((json.dumps(value,sort_keys=True,indent=2)+'\n').encode())
    return subject.file_hash(path)


def cohort(root, version):
    root=Path(root).resolve();(root/'inputs').mkdir(parents=True)
    data={'old_code':'old-code.lib','old_kernel':'kernel32-old.lib','old_user':'provider-003.lib',
          'new_code':'new-code.lib'}
    if version==8:data['new_eh']='new-eh.obj'
    else:data.update(new_kernel='kernel32-new.lib',new_user='user32-new.lib')
    paths={}
    for name,filename in data.items():
        path=root/'inputs'/filename;path.write_bytes(('AUTHORED FIXTURE ONLY '+name+'\n').encode());paths[name]=path
    # Same bytes are insufficient: this origin path is NOT the selected baseline token.
    origin=root/'inputs/origin-user.lib';origin.write_bytes(paths['old_user'].read_bytes())
    prior_iat=['/ALTERNATENAME:_authored_iat_%02d=__imp__Authored%02d'%(i,i) for i in range(27)]
    prior_crt=['/ALTERNATENAME:_authored_crt_%02d=_AuthoredCRT%02d'%(i,i) for i in range(4)]
    allowed=prior_iat if version==8 else prior_iat+['/ALTERNATENAME:_authored_iat_%02d=__imp__Authored%02d'%(i,i) for i in range(27,31)]
    new_iat=prior_iat[:25] if version==8 else allowed
    new_crt=prior_crt[:3] if version==8 else prior_crt[:2]
    old=root/'prior';out=root/'prepared'
    base_tokens=['/NOLOGO','/MACHINE:X86','/OUT:'+str(old/'diagnostic.exe'),'/MAP:'+str(old/'diagnostic.map'),
                 str(paths['old_code']),str(paths['old_kernel']),str(paths['old_user'])]+prior_iat+prior_crt
    baseline=root/'inputs/baseline.rsp';baseline.write_bytes(response(base_tokens));paths['baseline_response']=baseline
    additions=['new_code','new_eh'] if version==8 else ['new_code']
    replacements=[] if version==8 else [dict(from_role='old_kernel',to_role='new_kernel'),dict(from_role='old_user',to_role='new_user')]
    expected_tokens=['/NOLOGO','/MACHINE:X86','/OUT:'+str(out/'diagnostic.exe'),'/MAP:'+str(out/'diagnostic.map'),
                     str(paths['old_code']),str(paths['old_kernel' if version==8 else 'new_kernel']),
                     str(paths['old_user' if version==8 else 'new_user'])]+[str(paths[r]) for r in additions]+new_iat+new_crt
    expected=response(expected_tokens)
    manifest=dict(schema_version=1,kind='authored-cohort-response-prototype-v1',phase='prepare-only',scope='authored-synthetic-only',
        validator_id='frozen-wave%d-response-v1'%version,entrypoint_sha256=subject.file_hash(subject.__file__),kernel_sha256=subject.KERNEL_PINS,
        baseline_output_relative='prior',output_relative='prepared',
        inputs={name:dict(relative_path=path.relative_to(root).as_posix(),identity=diagnostic.identity(path)) for name,path in paths.items()},
        baseline_roles=['old_code','old_kernel','old_user'],addition_roles=additions,replacements=replacements,
        aliases=dict(prior_IAT=prior_iat,prior_CRT=prior_crt,allowed_IAT=allowed,new_IAT=new_iat,new_CRT=new_crt),
        expected_response_sha256=hashlib.sha256(expected).hexdigest())
    path=root/'manifest.json';digest=save_manifest(path,manifest)
    return path,digest,manifest,expected,paths


class CohortManifestPrototypeTests(unittest.TestCase):
    def test_two_authored_cohorts_have_exact_expected_bytes_and_identical_python_hashes(self):
        with tempfile.TemporaryDirectory() as td:
            initial=subject.file_hash(subject.__file__);seen=[]
            for version in (8,9):
                path,digest,manifest,expected,_=cohort(Path(td)/('v%d'%version),version)
                receipt=subject.prepare(path,digest);seen.append(receipt['entrypoint_sha256'])
                self.assertEqual((path.parent/'prepared/prepared-response.rsp').read_bytes(),expected)
                self.assertEqual(receipt['response_sha256'],hashlib.sha256(expected).hexdigest())
                for flag in ('production_ready','full_proof_admission_verified','native_LINK_permitted','provider_selected','runtime_eligible'):
                    self.assertIs(receipt[flag],False)
            self.assertEqual(seen,[initial,initial]);self.assertEqual(subject.file_hash(subject.__file__),initial)

    def test_public_frozen_kernel_equivalence_for_both_authored_manifests(self):
        with tempfile.TemporaryDirectory() as td:
            for version in (8,9):
                path,_,manifest,expected,paths=cohort(Path(td)/str(version),version)
                a=manifest['aliases'];old=path.parent/'prior';out=path.parent/'prepared';baseline=paths['baseline_response'].read_text()
                if version==8:
                    tokens=wave8.response_tokens(baseline,old,out,[str(paths[x]) for x in manifest['addition_roles']],a['prior_IAT'],a['prior_CRT'],a['new_IAT'],a['new_CRT'])
                else:
                    tokens=wave9.response_tokens(baseline,old,out,[(str(paths[r['from_role']]),str(paths[r['to_role']])) for r in manifest['replacements']],str(paths['new_code']),a['prior_IAT'],a['prior_CRT'],a['allowed_IAT'],a['new_IAT'],a['new_CRT'])
                self.assertEqual(response(tokens),expected)

    def test_same_cli_runs_both_cohorts_and_help_starts(self):
        with tempfile.TemporaryDirectory() as td:
            hashes=[]
            for version in (8,9):
                path,digest,_,expected,_=cohort(Path(td)/str(version),version)
                result=subprocess.run([sys.executable,subject.__file__,'--manifest',str(path),'--manifest-sha256',digest],capture_output=True,text=True,timeout=30)
                self.assertEqual(result.returncode,0,result.stderr);hashes.append(json.loads(result.stdout)['entrypoint_sha256'])
                self.assertEqual((path.parent/'prepared/prepared-response.rsp').read_bytes(),expected)
            self.assertEqual(len(set(hashes)),1)
        result=subprocess.run([sys.executable,subject.__file__,'--help'],capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_cli_manifest_and_selected_paths_with_spaces_are_not_shell_rewritten(self):
        with tempfile.TemporaryDirectory() as td:
            path,digest,_,expected,_=cohort(Path(td)/'authored package with spaces',9)
            result=subprocess.run([sys.executable,subject.__file__,'--manifest',str(path),'--manifest-sha256',digest],capture_output=True,text=True,timeout=30)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual((path.parent/'prepared/prepared-response.rsp').read_bytes(),expected)

    def test_no_executable_metadata_or_unknown_schema_profile_phase(self):
        with tempfile.TemporaryDirectory() as td:
            _,_,manifest,_,_=cohort(td,8)
            cases=[dict(manifest,phase='link'),dict(manifest,scope='production'),dict(manifest,validator_id='os.system'),
                   dict(manifest,module='other'),dict(manifest,template='eval'),dict(manifest,schema_version=True)]
            for bad in cases:
                with self.subTest(bad=bad.get('phase')),self.assertRaises(ValueError):subject.validate_manifest(bad)

    def test_exact_kernel_and_entrypoint_bytes_are_not_manifest_selected(self):
        with tempfile.TemporaryDirectory() as td:
            _,_,manifest,_,_=cohort(td,8)
            bad=copy.deepcopy(manifest);bad['kernel_sha256'][next(iter(bad['kernel_sha256']))]='f'*64
            with self.assertRaises(ValueError):subject.validate_manifest(bad)
            bad=copy.deepcopy(manifest);bad['entrypoint_sha256']='f'*64
            with self.assertRaises(ValueError):subject.validate_manifest(bad)

    def test_duplicate_json_member_and_raw_manifest_hash_drift_fail(self):
        with tempfile.TemporaryDirectory() as td:
            path,digest,_,_,_=cohort(td,8)
            path.write_bytes(path.read_bytes().replace(b'\n',b'\r\n'))
            with self.assertRaises(ValueError):subject.prepare(path,digest)
            with self.assertRaises(ValueError):subject.strict_json('{"phase":"prepare-only","phase":"prepare-only"}')

    def test_manifest_drift_between_loaded_bytes_and_identity_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path,digest,_,_,_=cohort(td,8);parse=subject.strict_json
            def changed_after_parse(text):
                value=parse(text);path.write_bytes(path.read_bytes()+b'\n');return value
            with patch.object(subject,'strict_json',side_effect=changed_after_parse),self.assertRaisesRegex(ValueError,'after loading'):
                subject.prepare(path,digest)

    def test_byteidentical_origin_library_cannot_replace_selected_physical_path(self):
        with tempfile.TemporaryDirectory() as td:
            path,_,manifest,_,_=cohort(td,9);origin=path.parent/'inputs/origin-user.lib'
            manifest['inputs']['old_user']=dict(relative_path='inputs/origin-user.lib',identity=diagnostic.identity(origin))
            with self.assertRaisesRegex(ValueError,'selected baseline'):subject.prepare(path,save_manifest(path,manifest))

    def test_baseline_token_must_occur_exactly_once(self):
        with tempfile.TemporaryDirectory() as td:
            path,_,manifest,_,paths=cohort(td,9)
            baseline=paths['baseline_response'];baseline.write_bytes(baseline.read_bytes()+response([str(paths['old_user'])]))
            manifest['inputs']['baseline_response']['identity']=diagnostic.identity(baseline)
            with self.assertRaisesRegex(ValueError,'occur once'):subject.prepare(path,save_manifest(path,manifest))

    def test_requested_resolved_device_inode_size_and_raw_hash_all_bound(self):
        with tempfile.TemporaryDirectory() as td:
            path,_,manifest,_,_=cohort(td,8)
            for key,value in [('requested_path','other'),('path','other'),('device',1),('inode',1),('size',1),('sha256','f'*64)]:
                bad=copy.deepcopy(manifest);bad['inputs']['old_code']['identity'][key]=value
                with self.subTest(key=key),self.assertRaises(ValueError):subject.prepare(path,save_manifest(path,bad))

    def test_relative_path_escape_and_unused_or_unknown_roles_fail(self):
        with tempfile.TemporaryDirectory() as td:
            _,_,manifest,_,_=cohort(td,8)
            for name in ('../outside','/absolute','C:/outside','inputs\\old-code.lib'):
                bad=copy.deepcopy(manifest);bad['inputs']['old_code']['relative_path']=name
                with self.subTest(name=name),self.assertRaises(ValueError):subject.validate_manifest(bad)
            bad=copy.deepcopy(manifest);bad['addition_roles'].append('unknown')
            with self.assertRaises(ValueError):subject.validate_manifest(bad)

    def test_unsupported_baseline_options_and_aliases_stay_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path,_,manifest,_,paths=cohort(td,8)
            baseline=paths['baseline_response'];baseline.write_bytes(baseline.read_bytes()+response(['/FORCE:UNRESOLVED']))
            manifest['inputs']['baseline_response']['identity']=diagnostic.identity(baseline)
            with self.assertRaises(ValueError):subject.prepare(path,save_manifest(path,manifest))
            bad=copy.deepcopy(manifest);bad['aliases']['new_IAT'].append('/ALTERNATENAME:_new=_not_reviewed')
            with self.assertRaises(ValueError):subject.prepare(path,save_manifest(path,bad))

    def test_output_is_exclusive_and_postpublication_drift_removes_report(self):
        with tempfile.TemporaryDirectory() as td:
            path,digest,_,_,_=cohort(td,8);subject.prepare(path,digest)
            with self.assertRaises(ValueError):subject.prepare(path,digest)
        with tempfile.TemporaryDirectory() as td:
            path,digest,_,_,paths=cohort(td,8);original=diagnostic.stable;count=[]
            def drift(bindings):
                count.append(1)
                if len(count)==4:paths['old_code'].write_bytes(b'changed authored input')
                original(bindings)
            with patch.object(diagnostic,'stable',side_effect=drift),self.assertRaises(ValueError):subject.prepare(path,digest)
            self.assertFalse((path.parent/'prepared/synthetic-preparation.json').exists())

    def test_written_response_drift_is_not_hidden_by_in_memory_expected_hash(self):
        with tempfile.TemporaryDirectory() as td:
            path,digest,_,_,_=cohort(td,9);original=diagnostic.stable;count=[]
            def tamper(bindings):
                count.append(1)
                if len(count)==2:(path.parent/'prepared/prepared-response.rsp').write_bytes(b'changed authored response')
                original(bindings)
            with patch.object(diagnostic,'stable',side_effect=tamper),self.assertRaises(ValueError):subject.prepare(path,digest)
            self.assertFalse((path.parent/'prepared/synthetic-preparation.json').exists())


if __name__=='__main__':unittest.main()
