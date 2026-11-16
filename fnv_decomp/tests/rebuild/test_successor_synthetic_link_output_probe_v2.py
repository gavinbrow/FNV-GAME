import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('probe_fixture',ROOT/'tools/rebuild/successor_synthetic_link_output_probe_v2.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.folder=Path(self.tmp.name)/'once'
        compiler={'path':'compiler.exe','sha256':'a'*64,'size':1,'device':1,'inode':1}
        linker={'path':'link.exe','sha256':'b'*64,'size':1,'device':1,'inode':2}
        paths={'workspace':'work','source':'work/test.c','object':'work/test.obj','executable':'work/test.exe',
               'map':'work/test.map','control':'work/control'}
        self.profile={'kind':'authored-synthetic-vc2008-link-output-probe','version':1,'fixture_sha256':m.FIXTURE_SHA256,
          'compiler':compiler,'compiler_version':'15.00.30729.01','linker':linker,'paths':paths,
          'compile_argv':['compiler.exe','/nologo','/c','/GS-','/Od','/Fowork/test.obj','work/test.c'],
          'link_argv':['link.exe','/NOLOGO','/NODEFAULTLIB','/INCREMENTAL:NO','/SUBSYSTEM:CONSOLE','/ENTRY:main',
                       '/OUT:work/test.exe','/MAP:work/test.map','work/test.obj'],
          'lease':{'owner':'fixture','resource':'CPU_heavy','slot':1,'grant_sha256':'c'*64},
          'watchdog_sha256':'d'*64,'source_review_sha256':'e'*64,'operation_review_sha256':'f'*64,
          'seconds':180,'memory_bytes':1024,'output_bytes':1024}
        self.held={'profile_sha256':m.sha(m.canonical(self.profile)),
                   'parent':{'pid':1,'creation':10,'image':'python'},'child':{'pid':2,'creation':20,'image':'python'},
                   'job':'fixture','nonce':'a'*64}
    def test_disabled_and_authored_source(self):
        with self.assertRaises(RuntimeError):m.run()
        self.assertEqual(m._profile_fixture(self.profile),self.profile)
        with self.assertRaises(ValueError):m._begin_fixture(self.folder,self.profile,b'int stolen;',self.held,self.profile['lease'])
    def test_exact_commands_caps_and_reviews(self):
        for key,value in [('seconds',181),('memory_bytes',1073741825),('output_bytes',134217729),('fixture_sha256','0'*64)]:
            p=copy.deepcopy(self.profile);p[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):m._profile_fixture(p)
        p=copy.deepcopy(self.profile);p['link_argv'].append('/alter')
        with self.assertRaises(ValueError):m._profile_fixture(p)
        p=copy.deepcopy(self.profile);p['operation_review_sha256']=p['source_review_sha256']
        with self.assertRaises(ValueError):m._profile_fixture(p)
    def test_uncanonical_and_escaping_paths_rejected_even_with_matching_argv(self):
        for bad in ('work/../outside.c','work/./test.c','/absolute.c','work//test.c',
                    'work/test.c.','work/CON.txt','work\\outside.c','outside/test.c'):
            p=copy.deepcopy(self.profile);p['paths']['source']=bad;p['compile_argv'][-1]=bad
            with self.subTest(path=bad),self.assertRaises(ValueError):m._profile_fixture(p)
        p=copy.deepcopy(self.profile);p['paths']['control']='work/test.obj/subdir'
        with self.assertRaises(ValueError):m._profile_fixture(p)

    def test_dot_and_ambiguous_inventory_names_rejected(self):
        for name in ('.','..','file.','CON.txt','sub/name','a\\b'):
            row={'relative_path':name,'size':1,'sha256':'a'*64}
            with self.subTest(name=name),self.assertRaises(ValueError):m._inventory_fixture([],[row])

    def test_once_unknown_no_replay(self):
        m._begin_fixture(self.folder,self.profile,m.FIXTURE_SOURCE,self.held,self.profile['lease'])
        with self.assertRaises(ValueError):m._begin_fixture(self.folder,self.profile,m.FIXTURE_SOURCE,self.held,self.profile['lease'])
        self.assertIn(b'UNKNOWN',(self.folder/'intent.json').read_bytes())
    def test_missing_or_changed_session_rejected_before_journal(self):
        for held,lease in ((None,self.profile['lease']),(self.held,None)):
            with self.assertRaises(ValueError):m._begin_fixture(self.folder,self.profile,m.FIXTURE_SOURCE,held,lease)
        self.assertFalse(self.folder.exists())
    def test_inventory_is_bounded_unverified_metadata(self):
        row={'relative_path':'test.obj','size':1,'sha256':'a'*64};new={'relative_path':'test.exe','size':2,'sha256':'b'*64}
        observed=m._inventory_fixture([row],[row,new]);self.assertEqual(observed['added'],[new])
        self.assertFalse(observed['complete_process_io_observed']);self.assertFalse(observed['filesystem_race_free'])
        bad=dict(row,relative_path='../escape')
        with self.assertRaises(ValueError):m._inventory_fixture([],[bad])

if __name__=='__main__':unittest.main()
