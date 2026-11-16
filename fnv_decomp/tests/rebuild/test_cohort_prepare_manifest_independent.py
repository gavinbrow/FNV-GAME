"""Independent authored prototype boundaries; no real cohort/native inputs."""
from pathlib import Path
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cohort_prepare_manifest as subject
import application_link_diagnostic as diagnostic
from test_cohort_prepare_manifest import cohort,save_manifest


class IndependentPrototypeTests(unittest.TestCase):
    def test_two_cohorts_share_source_bytes_and_cannot_claim_admission(self):
        with tempfile.TemporaryDirectory() as td:
            before=subject.file_hash(subject.__file__)
            for version in (8,9):
                path,h,m,expected,_=cohort(Path(td)/str(version),version);r=subject.prepare(path,h)
                self.assertEqual((path.parent/'prepared/prepared-response.rsp').read_bytes(),expected)
                self.assertEqual(r['entrypoint_sha256'],before)
                self.assertEqual(r['status'],'synthetic-response-prepared-unqualified')
                for k in ('full_proof_admission_verified','production_ready','fresh_MATCH_performed','native_conformance_performed',
                          'native_LINK_permitted','game_execution_performed','provider_selected','runtime_eligible'):
                    self.assertIs(r[k],False)
            self.assertEqual(subject.file_hash(subject.__file__),before)

    def test_no_unknown_profile_phase_code_or_boolean_file_identity(self):
        with tempfile.TemporaryDirectory() as td:
            _,_,m,_,_=cohort(td,8)
            for field,value in [('phase','execute'),('scope','production'),('validator_id','arbitrary-profile'),('module','os'),('schema_version',True)]:
                bad=copy.deepcopy(m);bad[field]=value
                with self.subTest(field=field),self.assertRaises(ValueError):subject.validate_manifest(bad)
            for key in ('size','device','inode'):
                bad=copy.deepcopy(m);bad['inputs']['old_code']['identity'][key]=False
                with self.subTest(identity=key),self.assertRaises(ValueError):subject.validate_manifest(bad)

    def test_raw_manifest_and_actual_input_identity_are_mandatory(self):
        with tempfile.TemporaryDirectory() as td:
            path,h,m,_,paths=cohort(td,8);paths['old_code'].write_bytes(b'authored stale bytes')
            with self.assertRaises(ValueError):subject.prepare(path,h)
        with tempfile.TemporaryDirectory() as td:
            path,h,m,_,_=cohort(td,8);path.write_bytes(path.read_bytes()+b' ')
            with self.assertRaises(ValueError):subject.prepare(path,h)

    def test_identical_bytes_at_unselected_origin_are_not_selected_input(self):
        with tempfile.TemporaryDirectory() as td:
            path,_,m,_,_=cohort(td,9);origin=path.parent/'inputs/origin-user.lib'
            m['inputs']['old_user']=dict(relative_path='inputs/origin-user.lib',identity=diagnostic.identity(origin))
            with self.assertRaises(ValueError):subject.prepare(path,save_manifest(path,m))
            self.assertFalse((path.parent/'prepared').exists())

    def test_rehashed_baseline_cannot_add_force_or_duplicate_selected_token(self):
        for token in ('/FORCE:UNRESOLVED','/ENTRY:unreviewed'):
            with tempfile.TemporaryDirectory() as td:
                path,_,m,_,paths=cohort(td,8);p=paths['baseline_response'];p.write_bytes(p.read_bytes()+('"'+token+'"\n').encode())
                m['inputs']['baseline_response']['identity']=diagnostic.identity(p)
                with self.subTest(token=token),self.assertRaises(ValueError):subject.prepare(path,save_manifest(path,m))

    def test_success_report_cannot_describe_drifted_response_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            path,h,_,_,_=cohort(td,8);real=diagnostic.stable;calls=[]
            def tamper(bindings):
                calls.append(1)
                if len(calls)==2:(path.parent/'prepared/prepared-response.rsp').write_bytes(b'authored output drift\n')
                return real(bindings)
            with patch.object(diagnostic,'stable',side_effect=tamper):
                with self.assertRaises(ValueError):subject.prepare(path,h)
            self.assertFalse((path.parent/'prepared/synthetic-preparation.json').exists())

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as td:
            path,h,_,_,_=cohort(td,8);out=path.parent/'prepared';out.mkdir();marker=out/'keep.txt';marker.write_text('authored existing')
            with self.assertRaises(ValueError):subject.prepare(path,h)
            self.assertEqual(marker.read_text(),'authored existing')


if __name__=='__main__':unittest.main()
