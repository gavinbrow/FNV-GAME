"""Temporary authored files only; no game inputs or native tools."""
import hashlib,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_actual_cohort_phase_v2 as phase

class Tests(unittest.TestCase):
    def test_each_phase_freshly_checks_pinned_actual_file(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'input';p.write_bytes(b'first')
            identity=phase.diagnostic.identity(p)
            m=dict(operation_id='authored-operation',resources=[dict(role='source',identity=identity)])
            data=json.dumps(m).encode();sha=hashlib.sha256(data).hexdigest()
            for name in ('pre','post','publication'):
                self.assertFalse(phase.observe(manifest_bytes=data,manifest_sha256=sha,phase=name)['approval'])
            p.write_bytes(b'other')
            for name in ('pre','post','publication'):
                with self.subTest(name=name),self.assertRaises(ValueError):
                    phase.observe(manifest_bytes=data,manifest_sha256=sha,phase=name)

    def test_unrelated_consistent_hash_cannot_replace_physical_identity(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'input';p.write_bytes(b'first');i=phase.diagnostic.identity(p);i['sha256']='a'*64
            data=json.dumps(dict(operation_id='test',resources=[dict(role='source',identity=i)])).encode()
            with self.assertRaises(ValueError): phase.observe(manifest_bytes=data,manifest_sha256=hashlib.sha256(data).hexdigest(),phase='pre')

    def test_wrong_manifest_hash_and_duplicate_role_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'input';p.write_bytes(b'x');i=phase.diagnostic.identity(p)
            data=json.dumps(dict(operation_id='test',resources=[dict(role='source',identity=i)]*2)).encode()
            for sha in ('0'*64,hashlib.sha256(data).hexdigest()):
                with self.assertRaises(ValueError): phase.observe(manifest_bytes=data,manifest_sha256=sha,phase='pre')

if __name__=='__main__':unittest.main()
