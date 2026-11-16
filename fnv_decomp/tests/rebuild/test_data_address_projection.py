"""Invented DATA bytes/metadata only; no actual larger projection."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import data_address_projection as data


def fixture():
    sections=[dict(name='.data',start=0x1000,end=0x1040,raw_end=0x1040,executable=False,flags=0xc0000040),
        dict(name='.rdata',start=0x2000,end=0x2080,raw_end=0x2040,executable=False,flags=0x40000040),
        dict(name='.text',start=0x3000,end=0x3100,raw_end=0x3100,executable=True,flags=0x60000020)]
    rows=[]
    for offset,target in ((4,0x2008),(12,0x3007),(20,0x2008),(28,0x2060)):
        values=[offset,target-0x1000,'data',0,4,'raw',[]]
        rows.append(dict(original_record=values,site_identity=data.digest(values),original_site_va='0x%08x'%(0x1000+offset),
            original_target_va='0x%08x'%target,original_symbol_base_identity=None,original_symbol_addend=None))
    claims=[dict(start=0x2008,end=0x2010,family='SOURCE_PROJECTION_CANDIDATE',provider_selected=False,materialization_approved=False),
        dict(start=0x2008,end=0x2010,family='SOURCE_PROJECTION_CANDIDATE',provider_selected=False,materialization_approved=False)]
    payload=bytearray(bytes(range(64)))
    for r in rows:struct.pack_into('<I',payload,int(r['original_site_va'],16)-0x1000,int(r['original_target_va'],16))
    return rows,sections,claims,bytes(payload)


class AddressProjectionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)

    def fields(self):
        rows,sections,claims,payload=fixture()
        return data.assess_fields(rows,sections,claims,'a'*64,[],0x1000,64),payload

    def test_known_address_unknown_provider_admitted_without_four_role_namespace(self):
        fields,_=self.fields();self.assertEqual(len(fields),4)
        self.assertEqual(fields[0]['symbol'],fields[2]['symbol'])
        self.assertTrue(all(f['symbol'].startswith('_fnv_address_v1_') and f['provider_obligations_unresolved'] for f in fields))
        self.assertEqual(fields[0]['identity']['role'],data.DATA_ROLE)
        self.assertEqual(fields[1]['identity']['role'],data.CODE_ROLE)
        self.assertEqual(len(fields[0]['target_evidence']['source_owner_alternatives']),2)
        self.assertEqual(fields[3]['target_evidence']['backing'],'virtual-zero')

    def test_coordinate_and_role_identity_not_silently_merged(self):
        a=data.demand_identity('a'*64,0x2008,data.DATA_ROLE)[0]
        self.assertNotEqual(a,data.demand_identity('b'*64,0x2008,data.DATA_ROLE)[0])
        self.assertNotEqual(a,data.demand_identity('a'*64,0x2008,data.CODE_ROLE)[0])
        for role in ('data','code','iat-cell','crt-contract','unknown'):
            with self.assertRaises(ValueError):data.demand_identity('a'*64,0x2008,role)

    def test_special_selected_source_and_unknown_target_fail_whole_plan(self):
        for family in ('FRESH_IAT_CELL','FRESH_NORMAL_CRT_STATE','STATIC_TLS','LOADER_METADATA','RESOURCE_FORMAT','UNKNOWN'):
            rows,sections,claims,_=fixture();claims[0]['family']=family
            with self.assertRaises(ValueError):data.assess_fields(rows,sections,claims,'a'*64,[],0x1000,64)
        rows,sections,claims,_=fixture();claims[0]['provider_selected']=True
        with self.assertRaises(ValueError):data.assess_fields(rows,sections,claims,'a'*64,[],0x1000,64)
        with self.assertRaises(ValueError):data.assess_fields(rows,sections,[],'a'*64,[dict(start=0x2008,size=8)],0x1000,64)
        rows[0]['original_target_va']='0x00009999'
        with self.assertRaises(ValueError):data.assess_fields(rows,sections,[],'a'*64,[],0x1000,64)

    def test_source_domain_mixed_code_tls_and_bind_targets_fail(self):
        rows,sections,claims,_=fixture()
        with self.assertRaises(ValueError):data.assess_fields(rows,sections,claims+[dict(start=0x1000,end=0x1004,family='CRT')],'a'*64,[],0x1000,64)
        for name in ('.rsrc','.tls','.reloc'):
            s=copy.deepcopy(sections);s[1]['name']=name
            with self.assertRaises(ValueError):data.assess_fields(rows,s,claims,'a'*64,[],0x1000,64)
        s=copy.deepcopy(sections);s[1]['flags']|=0x20
        with self.assertRaises(ValueError):data.assess_fields(rows,s,claims,'a'*64,[],0x1000,64)
        s=copy.deepcopy(sections);s[2]['name']='.bind'
        with self.assertRaises(ValueError):data.assess_fields(rows,s,claims,'a'*64,[],0x1000,64)

    def test_field_width_bounds_raw_overlap_and_bridge_rejected(self):
        for key,value in (('original_symbol_addend',4),('original_symbol_base_identity','0x00002004'),('original_site_va','0x0000103e')):
            rows,sections,claims,_=fixture();rows[0][key]=value
            with self.assertRaises(ValueError):data.assess_fields(rows,sections,claims,'a'*64,[],0x1000,64)
        rows,sections,claims,_=fixture();rows[0]['original_record'][4]=8;rows[0]['site_identity']=data.digest(rows[0]['original_record'])
        with self.assertRaises(ValueError):data.assess_fields(rows,sections,claims,'a'*64,[],0x1000,64)
        rows,sections,claims,_=fixture();rows.append(copy.deepcopy(rows[0]))
        with self.assertRaises(ValueError):data.assess_fields(rows,sections,claims,'a'*64,[],0x1000,64)
        rows[-1]['original_site_va']='0x00001005'
        with self.assertRaises(ValueError):data.assess_fields(rows,sections,claims,'a'*64,[],0x1000,64)

    def test_all_fields_zeroed_and_nonrelocated_numbers_preserved(self):
        fields,payload=self.fields();path=self.root/'data.obj';path.write_bytes(data.coff_bytes(payload,fields,'_fnv_test_anchor',16))
        proof=data.validate_object(path,payload,fields,'_fnv_test_anchor',16)
        self.assertEqual((proof['fields'],proof['undefined_demands']),(4,3));self.assertEqual(proof['code_sections'],0)
        coff,_,_,_=data.strict_object(path);raw=struct.unpack_from('<I',coff.data,40)[0]
        for f in fields:self.assertEqual(struct.unpack_from('<I',coff.data,raw+f['offset'])[0],0)
        self.assertEqual(coff.data[raw:raw+4],payload[:4])
        self.assertTrue(all(s['section']==0 for s in coff.symbols.values() if s['name'].startswith('_fnv_address_v1_')))

    def test_original_pointer_fallback_wrong_word_and_double_add_rejected(self):
        fields,payload=self.fields();bad=bytearray(payload);struct.pack_into('<I',bad,4,0x2222)
        with self.assertRaises(ValueError):data.coff_bytes(bytes(bad),fields,'_fnv_test_anchor',16)
        fields[0]['addend']=4
        with self.assertRaises(ValueError):data.coff_bytes(payload,fields,'_fnv_test_anchor',16)

    def test_strict_reparse_missing_extra_retargeted_or_nonzero_relocation_rejected(self):
        fields,payload=self.fields();original=data.coff_bytes(payload,fields,'_fnv_test_anchor',16);path=self.root/'bad.obj'
        variants=[]
        bad=bytearray(original);struct.pack_into('<H',bad,52,3);variants.append(bad)
        bad=bytearray(original);struct.pack_into('<I',bad,64,0x2008);variants.append(bad)
        bad=bytearray(original);rel=60+len(payload);struct.pack_into('<I',bad,rel+4,0);variants.append(bad)
        bad=bytearray(original);struct.pack_into('<H',bad,rel+8,20);variants.append(bad)
        bad=bytearray(original);bad[61]^=1;variants.append(bad)
        bad=bytearray(original);struct.pack_into('<I',bad,56,0xe0500060);variants.append(bad)
        for bad in variants:
            path.write_bytes(bad)
            with self.assertRaises(ValueError):data.validate_object(path,payload,fields,'_fnv_test_anchor',16)

    def test_policy_is_fixed_whole_fragment_no_bridge_or_provider_adoption(self):
        path=Path(__file__).resolve().parents[2]/'runtime/data-arenas/address-demands-original-v1.json';p=json.loads(path.read_text());data.policy_contract(p)
        self.assertEqual(p['fields'],13869);self.assertEqual(p['fragment']['size'],255676)
        for change in ({'identity_bridges':[{}]},{'provider_selected':True},{'fields':13868}):
            bad=copy.deepcopy(p);bad.update(change)
            with self.assertRaises(ValueError):data.policy_contract(bad)

    def test_missing_projection_gate_before_metadata_or_owned_image(self):
        path=Path(__file__).resolve().parents[2]/'runtime/data-arenas/address-demands-original-v1.json';rp=self.root/'review.json';rp.write_text('{}')
        with patch.object(data,'metadata') as metadata,patch.object(data,'Pe') as image:
            with self.assertRaises(ValueError):data.project({},path,'owned','reference',self.root,rp,self.root/'out')
            metadata.assert_not_called();image.assert_not_called()

    def test_stale_protected_input_and_late_drift_fail(self):
        p=self.root/'input';p.write_bytes(b'invented');bindings={str(p):data.sha(p)};data.stable(bindings)
        p.write_bytes(b'changed')
        with self.assertRaises(ValueError):data.stable(bindings)

    def test_all_13869_invented_fields_bijection_and_last_unknown_blocks_whole(self):
        _,sections,claims,_=fixture();start=0x1000000;size=data.COUNT*4+4;rows=[];payload=bytearray(size)
        struct.pack_into('<I',payload,0,0x401234)  # Nonrelocated address-shaped number.
        for i in range(data.COUNT):
            offset=4+i*4;target=0x2008 if i%2 else 0x3007
            values=[start+offset-0x1000,target-0x1000,'data',0,4,'raw',[]]
            rows.append(dict(original_record=values,site_identity=data.digest(values),original_site_va='0x%08x'%(start+offset),
                original_target_va='0x%08x'%target,original_symbol_base_identity=None,original_symbol_addend=None))
            struct.pack_into('<I',payload,offset,target)
        fields=data.assess_fields(rows,sections,claims,'a'*64,[],start,size)
        path=self.root/'full-invented.obj';path.write_bytes(data.coff_bytes(bytes(payload),fields,'_fnv_test_anchor'))
        report=data.validate_object(path,bytes(payload),fields,'_fnv_test_anchor')
        self.assertEqual((report['fields'],report['undefined_demands']),(13869,2))
        rows[-1]['original_record'][1]=0x9999-0x1000;rows[-1]['site_identity']=data.digest(rows[-1]['original_record']);rows[-1]['original_target_va']='0x00009999'
        with self.assertRaises(ValueError):data.assess_fields(rows,sections,claims,'a'*64,[],start,size)

    def test_saved_metadata_full_closure_and_missing_v4_row_rejected(self):
        policy_path=Path(__file__).resolve().parents[2]/'runtime/data-arenas/address-demands-original-v1.json'
        p=json.loads(policy_path.read_text());paths={n:self.root/n for n in p['input_pins']}
        geometry=p['fragment']['arena_geometry'];domain=dict(event='DISJOINT_ARENA_DOMAIN',domain_id='synthetic-domain')
        p['fragment']['domain_ordinal']=2;legacy=[];values=[]
        with gzip.open(paths['owner_details'],'wt') as stream:
            stream.write(json.dumps(dict(geometry,event='ARENA_GEOMETRY'))+'\n');stream.write(json.dumps(domain)+'\n')
            for i in range(data.COUNT):
                site=data.START+i*4;v=[site-0x400000,0x1082a00-0x400000,'data',0,4,'raw',[]];values.append(v)
                r=dict(event='DATA_HIGHLOW_FIELD',site_identity=data.digest(v),original_record=v,original_site_va='0x%08x'%site,
                    original_target_va='0x01082a00',original_symbol_base_identity=None,original_symbol_addend=None)
                stream.write(json.dumps(r)+'\n');legacy.append(dict(site=site,original=dict(original=dict(record=r,ordinal=i+3))))
        fragment=dict(fragment_id=data.FRAGMENT,start=data.START,size=data.SIZE,flags=0xc0000040,alignment=4096,admitted=True,backing='raw',
            original_domain=dict(domain_id='synthetic-domain',families=['ORDINARY_UNCLASSIFIED'],overlap=False))
        paths['candidate_fields'].write_text(json.dumps(dict(candidates=[dict(fragment=fragment,fields=legacy)])))
        p['legacy_field_sequence_sha256']=hashlib.sha256(b''.join(data.canonical(r)+b'\n' for r in legacy)).hexdigest()
        for n in ('binding_details','address_evidence'):paths[n].write_text('{}')
        def write_v4(rows):
            with gzip.open(paths['data_details'],'wt') as stream:
                for v in rows:stream.write(json.dumps(v)+'\n')
            dp=dict(image=dict(base=0x400000),provenance=dict(nonexec_digest=p['nonexec_identity_sha256']),recipe_sha256=p['recipes_sha256'],
                detail_sha256=data.sha(paths['data_details']))
            paths['data_plan'].write_text(json.dumps(dp));p['input_pins']={n:data.sha(path) for n,path in paths.items()}
        write_v4(values)
        rows,domains,ordinals,bindings=data.metadata(paths,p,self.root)
        self.assertEqual((len(rows),len(domains),len(ordinals)),(13869,0,13869));data.stable(bindings)
        write_v4(values[:-1])
        with self.assertRaisesRegex(ValueError,'missing v4 field'):data.metadata(paths,p,self.root)


if __name__=='__main__':unittest.main()
