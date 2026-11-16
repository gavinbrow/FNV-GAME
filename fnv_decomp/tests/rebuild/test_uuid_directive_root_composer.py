import copy
from pathlib import Path
import struct
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import uuid_directive_root_composer as m

class DeclarationTests(unittest.TestCase):
    def setUp(self):
        self.d=dict(kind='explicit-normal-sdk-library-dependency-v1',library_name='uuid.lib',
                    absolute_path=r'C:\SDK\Lib\uuid.lib',sha256='1'*64,
                    required_response_token=r'C:\SDK\Lib\uuid.lib')
        self.b=dict(path=self.d['absolute_path'],sha256=self.d['sha256'])
        self.r=dict(kind='independent-normal-dependency-declaration-review-v1',status='accepted',
                    declaration_sha256=m.digest(self.d),reviewer='independent-reviewer')
        self.a=dict(declaration_sha256=m.digest(self.d),review_sha256=m.digest(self.r))
    def test_valid_is_obligation_not_selection(self):
        before=copy.deepcopy((self.d,self.r,self.a,self.b))
        result=m.validate_declaration(self.d,self.r,self.a,self.b)
        self.assertEqual(before,(self.d,self.r,self.a,self.b))
        self.assertFalse(result['dependency_selected']);self.assertFalse(result['dependency_loaded'])
        self.assertTrue(result['caller_authority_authentication_required'])
    def test_candidate_only_relative_or_wrong_token_rejected(self):
        for key,value in [('kind','bound-normal-sdk-search-candidate'),('absolute_path','x/uuid.lib'),
                          ('required_response_token','uuid.lib'),('library_name','other.lib'),('sha256','bad')]:
            d=copy.deepcopy(self.d);d[key]=value
            with self.assertRaises(ValueError):m.validate_declaration(d,self.r,self.a,self.b)
    def test_path_requires_stable_drive_or_complete_unc_and_no_traversal(self):
        for path in (r'\sdk\uuid.lib', r'C:\sdk\..\uuid.lib', r'\\server\uuid.lib',
                     r'\\?\C:\sdk\uuid.lib', r'\\.\C:\sdk\uuid.lib', r'C:uuid.lib'):
            d=copy.deepcopy(self.d);d['absolute_path']=path;d['required_response_token']=path
            b=dict(path=path,sha256=d['sha256'])
            r=dict(self.r,declaration_sha256=m.digest(d));a=dict(declaration_sha256=m.digest(d),review_sha256=m.digest(r))
            with self.assertRaises(ValueError):m.validate_declaration(d,r,a,b)

    def test_full_unc_is_accepted_with_exact_binding(self):
        path=r'\\server\share\sdk\uuid.lib'
        d=dict(self.d,absolute_path=path,required_response_token=path);b=dict(path=path,sha256=d['sha256'])
        r=dict(self.r,declaration_sha256=m.digest(d));a=dict(declaration_sha256=m.digest(d),review_sha256=m.digest(r))
        self.assertEqual(m.validate_declaration(d,r,a,b)['required_response_token'],path)

    def test_unreviewed_or_modified_binding_rejected(self):
        for key,value in [('status','pending'),('reviewer',''),('declaration_sha256','0'*64)]:
            r=copy.deepcopy(self.r);r[key]=value
            with self.assertRaises(ValueError):m.validate_declaration(self.d,r,self.a,self.b)
        b=copy.deepcopy(self.b);b['sha256']='2'*64
        with self.assertRaises(ValueError):m.validate_declaration(self.d,self.r,self.a,b)
    def test_same_hash_different_library_origin_is_rejected(self):
        b=dict(self.b,path=r'C:\OtherSDK\uuid.lib')
        with self.assertRaises(ValueError):m.validate_declaration(self.d,self.r,self.a,b)

    def test_pins_must_match(self):
        for k in self.a:
            a=copy.deepcopy(self.a);a[k]='0'*64
            with self.assertRaises(ValueError):m.validate_declaration(self.d,self.r,a,self.b)

class HeaderTests(unittest.TestCase):
    def fixture(self):
        payload=b'x'*93; head=struct.pack('<8sIIIIIIHHI',b'.drectve',0,0,93,60,0,0,0,0,0x100a00)
        raw=struct.pack('<HHIIIHH',0x14c,1,0,153,1,0,0)+head+payload
        h=dict(index=1,name='.drectve',size=93,flags=0x100a00,virtual_size=0,virtual_address=0,
               object_size=len(raw),raw_data_offset=60,section_count=1,optional_header_size=0,
               relocation_count=0,relocation_pointer=0,line_number_count=0,line_number_pointer=0)
        return raw,h,head,payload
    def test_exact_original_header_and_payload(self):
        raw,h,head,payload=self.fixture();self.assertEqual(m._header(raw,h),(head,payload))
    def test_header_drift_bounds_and_bool_index_fail(self):
        raw,h,_,_=self.fixture()
        for key,value in [('flags',0),('raw_data_offset',61),('size',92),('index',True)]:
            changed=dict(h);changed[key]=value
            with self.assertRaises(ValueError):m._header(raw,changed)
        with self.assertRaises(ValueError):m._header(raw[:50],h)

if __name__=='__main__':unittest.main()
