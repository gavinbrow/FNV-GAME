import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
m = load('successor', 'tools/rebuild/application_successor_operation_v2.py')
stable = load('stable', 'tools/rebuild/exact_binding_stability.py')
def digest(data): return hashlib.sha256(data).hexdigest()

class SuccessorControls(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
    def put(self, name, data):
        (self.root / name).write_bytes(data)
        return {'path': name, 'sha256': digest(data)}
    def manifest(self):
        manifest = {'kind': 'successor-operation-manifest', 'schema_version': 1,
                    'sources': {'s': {'path': 's.py', 'sha256': 'a'*64}},
                    'inputs': {'x': {'path': 'x', 'sha256': 'b'*64}},
                    'operation': {'kind': 'prepare', 'native_link': False}}
        ref = self.put('manifest.json', m._canonical(manifest))
        reviews = {}
        for i, scope in enumerate(('source', 'input', 'operation')):
            review = {'kind': 'independent-successor-review', 'scope': scope,
                      'manifest_sha256': ref['sha256'], 'reviewer': 'reviewer'+str(i),
                      'subject_sha256': digest(m._canonical(manifest[{'source':'sources','input':'inputs','operation':'operation'}[scope]]))}
            reviews[scope] = self.put(scope+'.json', m._canonical(review))
        anchors = {'manifest': ref['sha256'], **{k:v['sha256'] for k,v in reviews.items()}}
        return manifest, ref, reviews, anchors
    def test_manifest_independent_bindings_and_tamper(self):
        manifest, ref, reviews, anchors = self.manifest()
        actual, ledger = m._manifest_fixture(self.root, ref, reviews, anchors)
        self.assertEqual(actual, manifest)
        self.assertEqual(len(ledger), 4)
        (self.root/'operation.json').write_text('{}')
        with self.assertRaises(ValueError): m._manifest_fixture(self.root, ref, reviews, anchors)
    def test_reject_duplicate_keys_and_unpinned_source(self):
        with self.assertRaises(ValueError): m._json(b'{"a":1,"a":2}')
        ref = self.put('source.py', b'x=1\n')
        ledger=[]
        self.assertEqual(m._source_snapshots_fixture(self.root, {'source':ref}, ledger)['source'], b'x=1\n')
        (self.root/'source.py').write_bytes(b'x=2\n')
        with self.assertRaises(ValueError): m._source_snapshots_fixture(self.root, {'source':ref}, [])
        with self.assertRaises(ValueError): m._read_pinned(self.root, {'path':'../escape','sha256':'a'*64}, [])
    def test_fresh_phase_full_duplicate_ledger(self):
        row={'requested_path':'a','path':'a','sha256':'a'*64,'size':1,'device':1,'inode':1}
        ledger=[row.copy(),row.copy()]; calls=[]
        def delegate(rows): calls.append(rows)
        first=m._phase_fixture(ledger,'pre',stable.stable_phase,delegate)
        second=m._phase_fixture(ledger,'post',stable.stable_phase,delegate)
        self.assertEqual(len(calls),2)
        self.assertEqual(len(calls[0]),1)
        self.assertEqual(first['input_bindings'],ledger)
        self.assertEqual(second['selection']['input_rows'],2)
    def test_exclusive_receipts_unknown_then_terminal(self):
        lease={'registry_sha256':'a'*64,'owner':'fixture','resource':'cpu','slot':1,'granted_utc':'fixture','max_seconds':1}
        child={'pid':1,'parent_pid':2,'create_time':'fixture','executable_sha256':'b'*64}
        start=self.root/'started.json'; terminal=self.root/'terminal.json'
        sha=m._start_receipt_fixture(start,operation_sha='c'*64,lease_identity=lease,child_identity=child)
        self.assertEqual(json.loads(start.read_bytes())['outcome'],'UNKNOWN')
        with self.assertRaises(FileExistsError): m._start_receipt_fixture(start,operation_sha='c'*64,lease_identity=lease,child_identity=child)
        with self.assertRaises(ValueError): m._terminal_receipt_fixture(terminal,started_path=start,started_sha='d'*64,outcome='completed',evidence={})
        m._terminal_receipt_fixture(terminal,started_path=start,started_sha=sha,outcome='failed',evidence={'reason':'fixture'})
        with self.assertRaises(FileExistsError): m._terminal_receipt_fixture(terminal,started_path=start,started_sha=sha,outcome='failed',evidence={})

if __name__ == '__main__': unittest.main()
