import importlib.util
import os
import tempfile
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('path_fixture',ROOT/'tools/rebuild/successor_windows_path_observation_v2.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def info(file_id,attrs=0):return {'volume':1,'file_id':file_id,'attributes':attrs,'links':1,'final_path':r'\\?\Volume{fixture}'+'\\'+str(file_id)}

class Backend:
    def __init__(self):
        self.rows={r'C:\fixture':info(1,m.FILE_ATTRIBUTE_DIRECTORY),r'C:\fixture\input':info(2),
                   r'C:\fixture\out':info(3,m.FILE_ATTRIBUTE_DIRECTORY)}
        self.closed=[];self.opened=[]
    def open(self,path):
        if path not in self.rows:raise FileNotFoundError(path)
        self.opened.append(path);return path
    def info(self,handle):return dict(self.rows[handle])
    def close(self,handle):self.closed.append(handle)

class Tests(unittest.TestCase):
    def setUp(self):self.backend=Backend()
    def observe(self):return m.observe_snapshot([r'C:\fixture\input'],[r'C:\fixture\out\link.log'],r'C:\fixture\out\control',backend=self.backend)
    def test_snapshot_explicitly_non_authorizing_and_closes_handles(self):
        result=self.observe();self.assertEqual(result['status'],'OBSERVED_NOT_AUTHORIZED')
        self.assertFalse(result['race_free_creation_established']);self.assertFalse(result['native_link_authorized'])
        self.assertEqual(self.backend.closed,list(reversed(self.backend.opened)))
    def test_reparse_parent_and_missing_parent_fail(self):
        self.backend.rows[r'C:\fixture\out']['attributes']|=m.FILE_ATTRIBUTE_REPARSE_POINT
        with self.assertRaises(ValueError):self.observe()
        self.assertEqual(self.backend.closed,list(reversed(self.backend.opened)))
        self.backend=Backend();del self.backend.rows[r'C:\fixture\out']
        with self.assertRaises(FileNotFoundError):self.observe()
    def test_existing_output_or_control_even_hardlink_is_rejected(self):
        for path in (r'C:\fixture\out\link.log',r'C:\fixture\out\control'):
            self.backend=Backend();self.backend.rows[path]=info(2)
            with self.subTest(path=path),self.assertRaises(ValueError):self.observe()
    def test_ambiguous_or_duplicate_paths_rejected(self):
        with self.assertRaises(ValueError):m.observe_snapshot([r'C:\fixture\input'],[r'c:\FIXTURE\INPUT'],r'C:\fixture\out\control',backend=self.backend)
        with self.assertRaises(ValueError):m.observe_snapshot([r'C:\fixture\input'],[r'C:\fixture\out\name.'],r'C:\fixture\out\control',backend=self.backend)
    def test_cleanup_failure_attempts_every_handle_and_reports_all(self):
        attempted=[]
        def broken(handle):
            attempted.append(handle)
            if handle==r'C:\fixture':raise OSError('close-failure-'+str(len(attempted)))
        self.backend.close=broken
        with self.assertRaises(ExceptionGroup) as caught:self.observe()
        self.assertEqual(attempted,list(reversed(self.backend.opened)))
        self.assertGreaterEqual(len(caught.exception.exceptions),2)
        self.assertTrue(all(isinstance(x,OSError) for x in caught.exception.exceptions))

    def test_cleanup_group_preserves_primary_failure(self):
        self.backend.rows[r'C:\fixture\out\link.log']=info(2)
        attempted=[]
        def broken(handle):
            attempted.append(handle)
            if handle==r'C:\fixture':raise OSError('close failed')
        self.backend.close=broken
        with self.assertRaises(ExceptionGroup) as caught:self.observe()
        self.assertEqual(attempted,list(reversed(self.backend.opened)))
        self.assertTrue(any(isinstance(x,ValueError) and 'already exists' in str(x) for x in caught.exception.exceptions))
        self.assertTrue(any(isinstance(x,OSError) and 'close failed' in str(x) for x in caught.exception.exceptions))

    @unittest.skipUnless(os.name=='nt','Windows-only synthetic temporary fixture')
    def test_windows_backend_on_disposable_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'input.bin';source.write_bytes(b'fixture')
            backend=m.WindowsReadOnlyBackend()
            result=m.observe_snapshot([str(source)],[str(root/'output.bin')],str(root/'control'),backend=backend)
            self.assertEqual(result['status'],'OBSERVED_NOT_AUTHORIZED')
            self.assertEqual(len(result['protected_identities']),1)
            self.assertFalse(result['race_free_creation_established'])

    def test_changed_component_identity_rejected(self):
        old=self.backend.info;seen={}
        def changed(handle):
            row=old(handle);seen[handle]=seen.get(handle,0)+1
            if handle==r'C:\fixture' and seen[handle]>1:row['file_id']=99
            return row
        self.backend.info=changed
        with self.assertRaises(ValueError):self.observe()

if __name__=='__main__':unittest.main()
