"""Failure-path tests for the single-file transaction, using private fake roots."""
import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('unit775_apply_under_test',HERE/'apply_unit775.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
LIVE_F=mod.F;LIVE_T=mod.T;LIVE_V=mod.V

class TransactionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        root=Path(self.tmp.name);f=root/'fnv_decomp';t=root/'transaction';v=root/'validation'
        t.mkdir();(v/'unit-0775').mkdir(parents=True)
        for name in ('manifest.json','source.original','source.generated'):shutil.copyfile(LIVE_T/name,t/name)
        shutil.copyfile(LIVE_V/'result.json',v/'result.json')
        shutil.copyfile(LIVE_V/'unit-0775/mirror-manifest.json',v/'unit-0775/mirror-manifest.json')
        closure=json.loads((v/'unit-0775/mirror-manifest.json').read_bytes())['original_inputs']
        for name in set(closure)|{'build/units.json','include/TESContainer.h'}:
            dst=f/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(LIVE_F/name,dst)
        self.target=f/'src/fallout_shared/inventorychanges_ctxr_variant.cpp'
        self.old=(t/'source.original').read_bytes();self.new=(t/'source.generated').read_bytes();self.t=t;self.root=root
        self.patch=patch.multiple(mod,R=root,F=f,T=t,V=v,TARGET=self.target);self.patch.start();self.addCleanup(self.patch.stop)
        def guard():
            lock=root/'build.lock';lock.open('x').close();return [lock]
        self.guard=patch.object(mod.locks,'acquire_guard',side_effect=guard);self.guard.start();self.addCleanup(self.guard.stop)
    def test_apply_restore(self):
        mod.run('apply');self.assertEqual(self.target.read_bytes(),self.new)
        mod.run('restore');self.assertEqual(self.target.read_bytes(),self.old)
        self.assertFalse((self.root/'build.lock').exists())
    def test_unknown_state_rejected(self):
        self.target.write_bytes(b'unknown')
        with self.assertRaises(ValueError):mod.run('apply')
        self.assertEqual(self.target.read_bytes(),b'unknown');self.assertFalse((self.root/'build.lock').exists())
    def test_changed_payload_rejected(self):
        (self.t/'source.generated').write_bytes(b'altered')
        with self.assertRaises(ValueError):mod.run('apply')
        self.assertEqual(self.target.read_bytes(),self.old)
    def test_changed_header_rejected(self):
        (mod.F/'include/TESContainer.h').write_bytes(b'altered')
        with self.assertRaises(ValueError):mod.run('apply')
        self.assertEqual(self.target.read_bytes(),self.old)
    def test_busy_gameplay_rejected(self):
        lock=self.root/'runtime-next/direct-v1/harness.lock';lock.parent.mkdir(parents=True);lock.touch()
        with self.assertRaises(ValueError):mod.run('apply')
        self.assertEqual(self.target.read_bytes(),self.old)
    def test_marker_failure_rolls_back(self):
        with patch.object(mod.json,'dump',side_effect=OSError('injected marker failure')):
            with self.assertRaises(OSError):mod.run('apply')
        self.assertEqual(self.target.read_bytes(),self.old)
        self.assertFalse((self.t/'applied.json').exists());self.assertFalse((self.t/'apply-result.json').exists())
        self.assertFalse((self.root/'build.lock').exists())
    def test_recover_known_new_state(self):
        self.target.write_bytes(self.new);mod.run('recover');self.assertEqual(self.target.read_bytes(),self.old)
    def test_second_apply_refused(self):
        mod.run('apply')
        with self.assertRaises((ValueError,FileExistsError)):mod.run('apply')
        self.assertEqual(self.target.read_bytes(),self.new)

if __name__=='__main__':unittest.main()
