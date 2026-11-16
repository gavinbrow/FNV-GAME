import stat
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'/'rebuild'))
import v14_stat_budget_census as subject


class CensusTests(unittest.TestCase):
    def plan(self):
        base=Path('C:/synthetic') if sys.platform=='win32' else Path('/synthetic')
        return {'kind':'v14-exact-source-reference-stat-only-plan','production_authorized':False,
            'paths':[{'role':'source','path':str(base/f'{i}.cpp'),'recipe_id':str(i)} for i in range(9)]+
                    [{'role':'reference','path':str(base/'reference.exe')}]}

    def test_exact_paths_observed_once_without_open(self):
        plan=self.plan(); calls=[]
        def fake(path):
            calls.append(path);return SimpleNamespace(st_mode=stat.S_IFREG,st_size=23,st_dev=1,st_ino=2,st_mtime_ns=3,st_file_attributes=0)
        result=subject.census(plan,fake)
        self.assertEqual(calls,[row['path'] for row in plan['paths']]);self.assertEqual(len(result),10)
        self.assertTrue(all(row['size']==23 for row in result))

    def test_duplicate_and_reparse_rejected(self):
        plan=self.plan();plan['paths'][1]['path']=plan['paths'][0]['path']
        with self.assertRaises(ValueError):subject.census(plan,lambda _:None)
        plan=self.plan()
        fake=lambda _:SimpleNamespace(st_mode=stat.S_IFREG,st_size=1,st_dev=1,st_ino=2,st_mtime_ns=3,st_file_attributes=0x400)
        with self.assertRaises(ValueError):subject.census(plan,fake)


class ControlTests(unittest.TestCase):
    def test_intent_precedes_targets_and_blocks_replay(self):
        import hashlib,json,tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); plan=root/'plan.json';raw=b'{}';plan.write_bytes(raw)
            out=root/'result.json';control=root/'control';observations=[]
            def fake_census(_):
                observations.append((control/'intent.json').exists());return []
            with patch.object(subject,'PLAN',plan),patch.object(subject,'PLAN_SHA256',hashlib.sha256(raw).hexdigest()), \
                    patch.object(subject,'OUTPUT',out),patch.object(subject,'CONTROL',control), \
                    patch.object(subject,'process_identity',return_value={'pid':1,'creation_filetime':2}), \
                    patch.object(subject,'census',side_effect=fake_census):
                subject.run()
                with self.assertRaises(FileExistsError):subject.run()
            self.assertEqual(observations,[True])
            self.assertEqual(json.loads((control/'terminal.json').read_text())['status'],'completed-not-admission')

    def test_failed_census_persists_terminal_and_blocks_replay(self):
        import hashlib,tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);plan=root/'plan.json';raw=b'{}';plan.write_bytes(raw)
            with patch.object(subject,'PLAN',plan),patch.object(subject,'PLAN_SHA256',hashlib.sha256(raw).hexdigest()), \
                    patch.object(subject,'OUTPUT',root/'result.json'),patch.object(subject,'CONTROL',root/'control'), \
                    patch.object(subject,'process_identity',return_value={'pid':1,'creation_filetime':2}), \
                    patch.object(subject,'census',side_effect=ValueError('synthetic')):
                with self.assertRaises(ValueError):subject.run()
                with self.assertRaises(FileExistsError):subject.run()
            self.assertTrue((root/'control'/'terminal.json').exists())

if __name__=='__main__':unittest.main()
