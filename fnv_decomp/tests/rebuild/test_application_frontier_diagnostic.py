"""Original response-selection regression cases; no native tool or game input."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_frontier_diagnostic as planner

def fixture():
    old=Path('old');out=Path('new')
    previous=['/ALTERNATENAME:iat%d=pointer%d'%(i,i) for i in range(26)]
    crt=['/ALTERNATENAME:crt%d=normal%d'%(i,i) for i in range(4)]
    tokens=['/NOLOGO','/OUT:'+str(old/'diagnostic.exe'),'/MAP:'+str(old/'diagnostic.map'),'old.lib','retained.lib']+previous+crt
    return dict(text='\n'.join('"'+x+'"' for x in tokens),old_out=old,out=out,old_kernel=Path('old.lib'),new_kernel=Path('new.lib'),
        additions=['first3.lib','code12.lib','EHFile.obj'],prior_IAT=previous,prior_CRT=crt,
        new_IAT=previous+['/ALTERNATENAME:new_IAT=new_pointer'],new_CRT=crt)

class ResponseTests(unittest.TestCase):
    def test_repeated_identical_source_pin_is_bound_once_conflict_fails(self):
        self.assertEqual(planner.source_pins({'parser':'a'},{'parser':'a','new':'b'}),{'parser':'a','new':'b'})
        with self.assertRaises(ValueError):planner.source_pins({'parser':'a'},{'parser':'b'})
    def test_exact_replacement_and_three_components_four_CRT_27IAT(self):
        args=fixture();actual=planner.response_tokens(**args)
        self.assertIn('new.lib',actual);self.assertNotIn('old.lib',actual)
        self.assertEqual(actual[:5],['/NOLOGO','/OUT:'+str(Path('new')/'diagnostic.exe'),'/MAP:'+str(Path('new')/'diagnostic.map'),'new.lib','retained.lib'])
        self.assertEqual(actual[5:8],args['additions']);self.assertEqual(len(actual),39)
    def test_prior_alias_missing_or_extra_unreviewed_alias_rejected(self):
        for mode in ('missing','extra'):
            args=fixture()
            if mode=='missing':args['text']=args['text'].replace('"'+args['prior_IAT'][0]+'"','')
            else:args['text']+='\n"/ALTERNATENAME:unreviewed=other"'
            with self.assertRaises(ValueError):planner.response_tokens(**args)
    def test_component_and_canonical_alias_collisions_rejected(self):
        for mode in ('component','alias'):
            args=fixture()
            if mode=='component':args['additions'][0]='retained.lib'
            else:args['new_CRT'][0]=args['new_IAT'][0].split('=')[0]+'=other'
            with self.assertRaises(ValueError):planner.response_tokens(**args)
    def test_output_or_kernel_destination_missing_rejected(self):
        for token in ('old.lib','/OUT:'+str(Path('old')/'diagnostic.exe')):
            args=fixture();args['text']=args['text'].replace('"'+token+'"','')
            with self.assertRaises(ValueError):planner.response_tokens(**args)
    def test_force_or_custom_entry_rejected(self):
        for token in ('/FORCE','/ENTRY:fake'):
            args=fixture();args['text']+='\n"'+token+'"'
            with self.assertRaises(ValueError):planner.response_tokens(**args)
    def test_disabled_CRT_subset_removes_all_old_tokens_before_subset(self):
        args=fixture();old=list(args['prior_CRT']);args['new_CRT']=old[2:]
        actual=planner.response_tokens(**args)
        self.assertFalse(set(old[:2]).intersection(actual));self.assertTrue(set(old[2:]).issubset(actual))

if __name__=='__main__':unittest.main()
