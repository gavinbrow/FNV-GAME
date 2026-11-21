import importlib.util,os,unittest,ast,tempfile,subprocess,sys,json
from pathlib import Path
H=Path(__file__).resolve().parent;S=H/'promotion-staged-v5';spec=importlib.util.spec_from_file_location('promotion_candidate',S/'config.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);c._M3_ROOT=str(H.parent.resolve())
class ConfigTests(unittest.TestCase):
 def resolved(self,raw,skip=False):
  env=c.configure(raw,promoted=True);c.validate_driver_options(env,skip_data_v1=skip,raw_environment=raw);return env
 def test_default_and_input_immutable(self):
  raw={};e=self.resolved(raw);self.assertEqual(raw,{});self.assertEqual(e['FNV_M3_SEL'],'phase2/selection.json');self.assertEqual(e['FNV_M3_LIB_SHA256'],c.DEFAULT_LIBRARY_SHA256);self.assertTrue(os.path.isabs(e['FNV_M3_LIB_SELECTION']))
 def test_legacy_off_and_dv1_off(self):
  self.assertNotIn('FNV_M3_LIB_SELECTION',self.resolved({'FNV_M3':'0'}));self.assertNotIn('FNV_M3_LIB_SELECTION',self.resolved({'FNV_M3_DV1':'0'}))
 def test_independent_library_optout(self):
  self.assertNotIn('FNV_M3_LIB_SELECTION',self.resolved({'FNV_M3_LIB':'0'}))
 def test_custom_m3_no_auto_library(self):
  self.assertNotIn('FNV_M3_LIB_SELECTION',self.resolved({'FNV_M3_SEL':'custom.json'}));self.assertEqual(self.resolved({'FNV_M3_SEL':'custom.json','FNV_M3_LIB':'1'})['FNV_M3_LIB_SHA256'],c.DEFAULT_LIBRARY_SHA256)
 def test_explicit_library_and_partial_rejection(self):
  raw={'FNV_M3_SEL':'custom.json','FNV_M3_LIB_SELECTION':'custom.json','FNV_M3_LIB_SHA256':'a'*64};self.assertEqual(self.resolved(raw)['FNV_M3_LIB_SELECTION'],'custom.json')
  for raw in ({'FNV_M3_LIB_SELECTION':'x'}, {'FNV_M3_LIB_SHA256':'b'*64},{'FNV_M3_LIB_SELECTION':'','FNV_M3_LIB_SHA256':'b'*64},{'FNV_M3_LIB':'0','FNV_M3_LIB_SELECTION':'x','FNV_M3_LIB_SHA256':'b'*64}):
   with self.assertRaises(ValueError):self.resolved(raw)
 def test_explicit_enable_requires_dv1(self):
  with self.assertRaises(ValueError):self.resolved({'FNV_M3_DV1':'0','FNV_M3_LIB':'1'})
 def test_explicit_library_enabled_without_promotion(self):
  raw={'FNV_M3':'1','FNV_M3_DV1':'1','FNV_M3_LIB':'1'};e=c.configure(raw,promoted=False);c.validate_driver_options(e,raw_environment=raw);self.assertEqual(e['FNV_M3_LIB_SHA256'],c.DEFAULT_LIBRARY_SHA256)
 def test_default_path_independent_of_cwd(self):
  old=os.getcwd()
  try:os.chdir(os.path.abspath(os.sep));e=self.resolved({});self.assertEqual(e['FNV_M3_LIB_SELECTION'],os.path.abspath(os.path.join(c._M3_ROOT,'phase2/library_candidates.json')))
  finally:os.chdir(old)
 def test_driver_checks_selection_before_compile(self):
  src=(S/'build_all.py').read_text();ast.parse(src);self.assertLess(src.index("with open(selection, 'rb')"),src.index("step(1, 'compile-units'"));self.assertLess(src.index("with open(env['FNV_M3_LIB_SELECTION'], 'rb')"),src.index("step(1, 'compile-units'"))
 def test_existing_config_checks_in_isolated_tree(self):
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp);(p/'tools').mkdir();(p/'config.py').write_bytes((S/'config.py').read_bytes());(p/'tools/test_m3_config.py').write_bytes((S/'test_m3_config.py').read_bytes());r=subprocess.run([sys.executable,str(p/'tools/test_m3_config.py')],capture_output=True,text=True,timeout=20);self.assertEqual(r.returncode,0,r.stdout+r.stderr)
 def test_driver_rejects_tampered_default_before_compiling(self):
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp);m=p/'m3';m.mkdir();(m/'phase2').mkdir();(m/'__init__.py').write_text('');(m/'config.py').write_bytes((S/'config.py').read_bytes());(m/'phase2/selection.json').write_text('tampered');(p/'build_all.py').write_bytes((S/'build_all.py').read_bytes())
   game=p/'game';game.mkdir();(game/'FalloutNV.exe').touch();(p/'reference.exe').touch();(p/'fn/build').mkdir(parents=True);(p/'fn/build/units.json').touch();(p/'sp/VC/bin').mkdir(parents=True);(p/'sp/VC/bin/cl.exe').touch();(p/'rt/VC/bin').mkdir(parents=True);(p/'rt/VC/bin/cl.exe').touch()
   values={'RN':str(p),'PROJ':str(p),'GAME_DIR':str(game),'REF_IMAGE':str(p/'reference.exe'),'FN':str(p/'fn'),'MSVC9_SP1':str(p/'sp'),'MSVC9_RTM':str(p/'rt'),'MSVC8':str(p/'sp'),'PY_SITE':str(p/'missing-site')};(p/'paths.py').write_text('\n'.join(k+' = '+repr(v) for k,v in values.items()));(p/'buildlock.py').write_text('def acquire(*a): return True\ndef release(*a): pass\n');(p/'harness_evidence.py').write_text('def accepted_verdict(*a): return False\n')
   env={k:v for k,v in os.environ.items() if not k.startswith('FNV_M3') and k not in ('DV_M3','DV3_SKIP','FNV_COFF_WEAK')};env['FNV_M3_LIB']='0'
   r=subprocess.run([sys.executable,str(p/'build_all.py'),'--out',str(p/'result'),'--no-harness'],cwd=p,env=env,capture_output=True,text=True,timeout=20);self.assertNotEqual(r.returncode,0);summary=json.loads((p/'result/build-summary.json').read_text());self.assertIn('default M3 selection SHA-256',summary['message']);self.assertEqual(summary['steps'],[])
if __name__=='__main__':unittest.main()



