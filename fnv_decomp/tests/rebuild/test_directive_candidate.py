"""Invented examples only; no original game data or private fixture imports."""
import copy
import hashlib
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import directive_candidate as m


def example():
    root=dict(original_address='synthetic-root',recipe_id='synthetic-recipe',recipe_index=3,symbol='example',
              symbol_index=2,section=2,value=0,size=7,object_sha256='1'*64,source_sha256='2'*64)
    native={k:root[k] for k in ('original_address','symbol','symbol_index','section','value','size')}
    contract=dict(recipe_id=root['recipe_id'],roots=[native],provenance={k:root[k] for k in
                   ('recipe_id','recipe_index','object_sha256','source_sha256')},fields=[{'unknown':None}])
    tokens=['/DEFAULTLIB:"demo.lib"','/DEFAULTLIB:"demo.lib"','/DEFAULTLIB:"LIBCMT"','/DEFAULTLIB:"OLDNAMES"']
    blockers=[dict(code='UNSUPPORTED_IMPLICIT_LINKER_DIRECTIVE',evidence=tokens[0],blocker_id='a'*64),
              dict(code='UNSUPPORTED_IMPLICIT_LINKER_DIRECTIVE',evidence=tokens[1],blocker_id='a'*64),
              dict(code='DIRECTIVE_CONTRACT_DIFFERS',evidence=copy.deepcopy(tokens),blocker_id='b'*64)]
    negative=dict(recipe_id=root['recipe_id'],roots=[native],contract_identity_sha256=m._digest(contract),blockers=blockers,
                  closure_observed=False,graph_observation_complete=False,root_closure_candidate=False,unknown={'keep':True})
    raw=b' '.join(x.encode('ascii') for x in tokens)+b'  '
    header=dict(index=1,name='.drectve',size=len(raw),flags=0x100a00,virtual_size=0,virtual_address=0,
                object_size=100+len(raw),raw_data_offset=100,section_count=2,optional_header_size=0,
                relocation_count=0,relocation_pointer=0,line_number_count=0,line_number_pointer=0)
    declaration=dict(kind='explicit-normal-sdk-library-dependency-v1',library_name='demo.lib',
                     absolute_path=r'C:\ExampleSDK\demo.lib',sha256='3'*64,required_response_token=r'C:\ExampleSDK\demo.lib')
    review=dict(kind='independent-normal-dependency-declaration-review-v1',status='accepted',
                declaration_sha256=m._digest(declaration),reviewer='synthetic-reviewer')
    declarations=[dict(declaration=declaration,review=review)]
    profile=dict(root=copy.deepcopy(root),contract_sha256=m._digest(contract),negative_sha256=m._digest(negative),
                 section_sha256=hashlib.sha256(raw).hexdigest(),header_sha256=m._digest(header),tokens=tokens,
                 blockers=[dict(blocker=copy.deepcopy(blockers[0]),directive_ordinals=[1]),
                           dict(blocker=copy.deepcopy(blockers[1]),directive_ordinals=[2]),
                           dict(blocker=copy.deepcopy(blockers[2]),directive_ordinals=[1,2,3,4])],
                 declarations=[dict(declaration_sha256=m._digest(declaration),review_sha256=m._digest(review))])
    registry=dict(schema_version=1,kind='directive-candidate-finite-registry-v1',profiles=[profile])
    registry_review=dict(kind='independent-directive-registry-review-v1',status='accepted',
                         registry_sha256=m._digest(registry),reviewer='synthetic-reviewer')
    return dict(root=root,contract=contract,negative=negative,raw_section=raw,header=header,registry=registry,
                registry_review=registry_review,registry_sha256=m._digest(registry),
                registry_review_sha256=m._digest(registry_review),declarations=declarations)


def repin(a):
    p=a['registry']['profiles'][0]
    p['contract_sha256']=m._digest(a['contract']);p['negative_sha256']=m._digest(a['negative'])
    p['section_sha256']=hashlib.sha256(a['raw_section']).hexdigest();p['header_sha256']=m._digest(a['header'])
    a['registry_sha256']=m._digest(a['registry']);a['registry_review']['registry_sha256']=a['registry_sha256']
    a['registry_review_sha256']=m._digest(a['registry_review'])


class CandidateTest(unittest.TestCase):
    def test_candidate_preserves_negative_duplicate_occurrences_and_future_obligation(self):
        a=example();before=copy.deepcopy(a);out=m.qualify(**a)
        self.assertEqual(a,before);self.assertEqual(out['original_negative'],a['negative'])
        self.assertEqual([x['directive_ordinals'] for x in out['blocker_occurrences']],[[1],[2],[1,2,3,4]])
        self.assertEqual(bytes.fromhex(out['raw_section_hex']),a['raw_section'])
        self.assertEqual(out['required_future_dependencies'][0]['required_response_token'],a['declarations'][0]['declaration']['absolute_path'])
        self.assertEqual(out['required_future_dependencies'][0]['sha256'],a['declarations'][0]['declaration']['sha256'])
        self.assertEqual(out['required_future_dependencies'][0]['declaration_sha256'],m._digest(a['declarations'][0]['declaration']))
        self.assertEqual(out['required_future_dependencies'][0]['review_sha256'],m._digest(a['declarations'][0]['review']))
        for k in ('ordinary_graph_closure','certificate_rewritten','composition_proved','projection_performed','provider_selected',
                  'runtime_eligible','ABI_verified','library_selected','library_loaded','duplicate_linker_semantics_proved',
                  'admission_approved','emission_performed','SDK_identity_freshly_observed','response_token_observed'):
            self.assertIs(out[k],False)
        self.assertIs(out['caller_authority_authentication_required'],True)

    def test_registry_review_and_authority_required(self):
        for change in (lambda a:a.update(registry_sha256='0'*64),lambda a:a['registry_review'].update(status='pending'),
                       lambda a:a['registry'].update(schema_version=True),lambda a:a['registry_review'].update(reviewer='')):
            a=example();change(a)
            if a['registry_review'].get('status')!='pending' and a['registry'].get('schema_version') is True:repin(a)
            with self.assertRaises(ValueError):m.qualify(**a)

    def test_unknown_or_changed_root_and_source_hashes_fail(self):
        for change in (lambda a:a['root'].update(original_address='different'),lambda a:a['root'].update(value=False),
                       lambda a:a['contract']['provenance'].update(source_sha256='4'*64)):
            a=example();change(a);repin(a)
            with self.assertRaises(ValueError):m.qualify(**a)

    def test_duplicate_order_ordinal_types_and_coverage(self):
        for change in (lambda a:a['negative']['blockers'].pop(1),
                       lambda a:a['registry']['profiles'][0]['blockers'][0].update(directive_ordinals=[True]),
                       lambda a:a['registry']['profiles'][0]['blockers'][1].update(directive_ordinals=[1]),
                       lambda a:a['negative']['blockers'].reverse()):
            a=example();change(a);repin(a)
            with self.assertRaises(ValueError):m.qualify(**a)

    def test_unknown_directive_and_tail_rejected_even_if_repinned(self):
        for token in ('/INCLUDE:example','/FORCE','/NODEFAULTLIB','/ALTERNATENAME:x=y'):
            a=example();a['registry']['profiles'][0]['tokens'][0]=token
            a['raw_section']=token.encode()+b' '+a['raw_section'];a['header']['size']=len(a['raw_section'])
            a['header']['object_size']=100+len(a['raw_section']);repin(a)
            with self.assertRaises(ValueError):m.qualify(**a)
        a=example();a['raw_section']+=b' /FORCE';a['header']['size']=len(a['raw_section']);a['header']['object_size']=100+len(a['raw_section']);repin(a)
        with self.assertRaises(ValueError):m.qualify(**a)

    def test_header_and_false_flag_validation(self):
        for key,value in (('flags',0),('index',True),('raw_data_offset',0),('relocation_count',1)):
            a=example();a['header'][key]=value;repin(a)
            with self.assertRaises(ValueError):m.qualify(**a)
        for key in ('closure_observed','graph_observation_complete','root_closure_candidate'):
            a=example();a['negative'][key]=True;repin(a)
            with self.assertRaises(ValueError):m.qualify(**a)

    def test_declaration_review_full_path_and_finite_dependency(self):
        for value in (r'\folder\demo.lib',r'C:demo.lib',r'C:\ExampleSDK\..\demo.lib',r'\\?\C:\demo.lib',r'C:\ExampleSDK\other.lib'):
            a=example();d=a['declarations'][0]['declaration'];d['absolute_path']=d['required_response_token']=value
            r=a['declarations'][0]['review'];r['declaration_sha256']=m._digest(d)
            a['registry']['profiles'][0]['declarations'][0]=dict(declaration_sha256=m._digest(d),review_sha256=m._digest(r));repin(a)
            with self.assertRaises(ValueError):m.qualify(**a)
        a=example();a['declarations'][0]['review']['status']='pending'
        with self.assertRaises(ValueError):m.qualify(**a)

    def test_path_rejects_windows_reserved_and_ambiguous_components(self):
        for value in (r'C:\ExampleSDK\NUL\demo.lib',r'C:\ExampleSDK\temp.\demo.lib',
                      r'C:\ExampleSDK\temp \demo.lib',r'C:\ExampleSDK\COM1.txt\demo.lib',
                      r'C:\ExampleSDK\CONIN$\demo.lib',r'C:\ExampleSDK\COM¹\demo.lib',
                      r'\\server\demo.lib',r'\\.\C:\demo.lib'):
            a=example();d=a['declarations'][0]['declaration'];d['absolute_path']=d['required_response_token']=value
            r=a['declarations'][0]['review'];r['declaration_sha256']=m._digest(d)
            a['registry']['profiles'][0]['declarations'][0]=dict(declaration_sha256=m._digest(d),review_sha256=m._digest(r));repin(a)
            with self.assertRaises(ValueError):m.qualify(**a)
        a=example();d=a['declarations'][0]['declaration'];value=r'\\server\share\sdk\demo.lib'
        d['absolute_path']=d['required_response_token']=value;r=a['declarations'][0]['review'];r['declaration_sha256']=m._digest(d)
        a['registry']['profiles'][0]['declarations'][0]=dict(declaration_sha256=m._digest(d),review_sha256=m._digest(r));repin(a)
        self.assertEqual(m.qualify(**a)['required_future_dependencies'][0]['required_response_token'],value)

    def test_duplicate_profile_and_unregistered_root(self):
        a=example();a['registry']['profiles'].append(copy.deepcopy(a['registry']['profiles'][0]));repin(a)
        with self.assertRaises(ValueError):m.qualify(**a)
        a=example();a['registry']['profiles'][0]['root']['recipe_id']='different';repin(a)
        with self.assertRaises(ValueError):m.qualify(**a)

if __name__=='__main__':unittest.main()
