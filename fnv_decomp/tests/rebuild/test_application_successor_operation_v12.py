import copy
import importlib.util
from pathlib import Path
import sys
import tempfile
import types
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('operation_v8_fixture',ROOT/'tools/rebuild/application_successor_operation_v12.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.old_main=sys.modules['__main__'];self.addCleanup(sys.modules.__setitem__,'__main__',self.old_main)
        path=self.root/'tools/rebuild/application_successor_fixed_v7.py';path.parent.mkdir(parents=True)
        path.write_bytes(b'main');main=types.ModuleType('__main__');main.__file__=str(path);sys.modules['__main__']=main
        self.main_pin={'path':'tools/rebuild/application_successor_fixed_v7.py','sha256':m.digest(b'main')}
        self.sources={}
        for name,rel in m.SOURCE_PATHS.items():
            p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);raw=('fixture '+name).encode();p.write_bytes(raw)
            self.sources[name]={'path':rel,'sha256':m.digest(raw)}
    def invoke(self,graph):return m.source_finder(self.root,graph,[],Path(sys.base_prefix),main_pin=self.main_pin)
    def test_exact_profile_and_no_implicit_expansion(self):
        self.assertEqual(len(m.SOURCE_PATHS),96)
        self.assertEqual(set(self.invoke(self.sources).snapshots),set(m.SOURCE_PATHS))
        missing=copy.deepcopy(self.sources);missing.pop('application_actual_factory_join_v5')
        extra=copy.deepcopy(self.sources);extra['foreign']={'path':'tools/foreign.py','sha256':'a'*64}
        renamed=copy.deepcopy(self.sources);renamed['application_actual_factory_join_v2']=renamed.pop('application_actual_factory_join_v5')
        path=copy.deepcopy(self.sources);path['application_actual_factory_join_v5']['path']='tools/rebuild/other.py'
        for graph in (missing,extra,renamed,path):
            with self.subTest(size=len(graph)),self.assertRaises(ValueError):self.invoke(graph)
    def test_wrong_bytes_and_hostile_preload_fail(self):
        bad=copy.deepcopy(self.sources);bad['crt_v14_four_alias_contract']['sha256']='a'*64
        with self.assertRaises(ValueError):self.invoke(bad)
        foreign=types.ModuleType('foreign_workspace');foreign.__file__=str(self.root/'evil.py')
        sys.modules[foreign.__name__]=foreign
        try:
            with self.assertRaises(ValueError):self.invoke(self.sources)
        finally:sys.modules.pop(foreign.__name__,None)
    def test_prepare_profile_and_dynamic_mapping_match(self):
        import ast
        spec=importlib.util.spec_from_file_location('prepare_v5_fixture',ROOT/'tools/rebuild/application_successor_prepare_v6.py')
        prepare=importlib.util.module_from_spec(spec);spec.loader.exec_module(prepare)
        self.assertEqual(m.SOURCE_PATHS,prepare.SOURCE_PATHS)
        wave=ast.parse((ROOT/'tools/rebuild/application_wave14_diagnostic.py').read_text())
        func=next(x for x in wave.body if isinstance(x,ast.FunctionDef) and x.name=='_prepare_from_authority')
        assign=next(x for x in ast.walk(func) if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='names' for t in x.targets))
        self.assertTrue(set(ast.literal_eval(assign.value).values()).issubset(m.SOURCE_PATHS))

if __name__=='__main__':unittest.main()
