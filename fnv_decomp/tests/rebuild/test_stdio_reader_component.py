"""Authored COFF and stage-gate tests; no game input or native command."""
import copy
import importlib.util
from pathlib import Path
import struct
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/rebuild'))
import stdio_reader_component as m
import coff_code_archive as coff
from test_coff_code_archive import section,symbol,aux,object_bytes


def authored_leaf():
    body=bytearray(b'source-authored synthetic COFF payload!!!')[:39]
    assert len(body)==39
    body[20:24]=bytes(4)
    directives=b'/DEFAULTLIB:"LIBCMT" /DEFAULTLIB:"OLDNAMES"'
    return object_bytes([section('.drectve',directives,0x00100a00),section('.debug$S',b'debug',0x42000040),
        section('.text',bytes(body),relocs=[(20,9,20)]),section('.sxdata',struct.pack('<I',99),0x40300240)],
        [symbol('@comp.id',-1,value=1,storage=3),symbol('@feat.00',-1,value=1,storage=3),
         symbol('.drectve',1,storage=3,auxiliary=aux(len(directives),selection=0)),
         symbol('.debug$S',2,storage=3,auxiliary=aux(5,selection=0)),
         symbol('.text',3,storage=3,auxiliary=aux(39,1)),symbol(m.METHOD,3,typ=32),symbol('_fread',0,typ=32)])


def certificate(raw):
    return dict(closure_observed=True,root_closure_candidate=True,graph_observation_complete=True,
        blockers=[],namespace_approved=False,full_serialization_eligible=False,
        provenance=dict(object_sha256=coff.digest(raw)),retained_section_indices=[1,3],
        retained_primary_indices=[0,1,2,6,8,9],retained_runtime_section_indices=[3],omitted_definition_conversions=[])


def caller(count=4,defined=False,kind=20):
    code=bytes(4*count)
    return object_bytes([section('.text',code,relocs=[(4*i,3,kind)for i in range(count)])],
        [symbol('.text',1,storage=3,auxiliary=aux(len(code),count)),symbol('_own_source_consumer',1,typ=32),
         symbol(m.METHOD,1 if defined else 0,typ=32)])


class StdioReaderComponentTests(unittest.TestCase):
    def project(self,raw,c=None):
        c=certificate(raw)if c is None else c
        with patch.object(m,'CERTIFICATE',m.digest(c)):return m.pure_projection(raw,c)

    def test_exact_payload_directives_and_indices_preserved(self):
        raw=authored_leaf();output,receipt=self.project(raw);before,after=coff.parse(raw),coff.parse(output)
        self.assertEqual(receipt['mapping']['section_map'],{1:1,3:2})
        self.assertEqual(receipt['mapping']['symbol_map'],{0:0,1:1,2:2,6:4,8:6,9:7})
        self.assertEqual(receipt['mapping']['auxiliary_map'],{3:3,7:5})
        self.assertEqual(after['sections'][1],before['sections'][1])
        self.assertEqual(after['sections'][2]['payload'],before['sections'][3]['payload'])
        self.assertEqual(after['sections'][2]['relocs'],[(20,7,20)])
        self.assertEqual(coff.exports(output),[m.EXPORT])
        self.assertEqual(after['symbols'][7]['name'],m.FREAD)
        self.assertFalse(receipt['link_alias_applied'])
        self.assertFalse(receipt['provider_selected'])

    def test_wrong_exact_certificate_hash_rejected(self):
        with self.assertRaisesRegex(ValueError,'bare certificate'):m.pure_projection(authored_leaf(),certificate(authored_leaf()))

    def test_promoted_or_incomplete_certificate_rejected(self):
        raw=authored_leaf()
        for key,value in [('namespace_approved',True),('full_serialization_eligible',True),
            ('closure_observed',False),('blockers',[dict(code='REACHABLE_SAFESEH')]),
            ('retained_section_indices',[1,3,4]),('retained_primary_indices',[0,1,2,6,8,9,10]),
            ('omitted_definition_conversions',[9])]:
            c=certificate(raw);c[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.project(raw,c)

    def test_changed_original_hash_and_addend_rejected(self):
        raw=authored_leaf();c=certificate(raw);c['provenance']['object_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'object'):self.project(raw,c)
        obj=coff.parse(raw);bad=bytearray(raw)
        # Independent encoder places section payloads in section order.
        text=20+40*4+len(obj['sections'][1]['payload'])+len(obj['sections'][2]['payload'])
        bad[text+20]=1
        with self.assertRaisesRegex(ValueError,'field'):self.project(bytes(bad))

    def test_changed_reference_name_rejected(self):
        raw=authored_leaf();changed=coff.namespace(raw,[(9,'_different_stdio_function')])
        with self.assertRaisesRegex(ValueError,'physical'):self.project(changed)

    def test_typed_caller_four_actual_calls_and_no_body(self):
        self.assertEqual(len(m.consumer_shape(caller())),4)
        for raw in(caller(3),caller(5),caller(4,True),caller(4,False,6)):
            with self.assertRaises(ValueError):m.consumer_shape(raw)

    def test_actual_COFF_component_directives_are_not_bootstrap_contract(self):
        from coff_inventory import Coff
        expected=['/DEFAULTLIB:"uuid.lib"','/DEFAULTLIB:"uuid.lib"','/DEFAULTLIB:"LIBCMT"','/DEFAULTLIB:"OLDNAMES"']
        def parsed(tokens,directory):
            payload=' '.join(tokens).encode('ascii')
            raw=object_bytes([section('.drectve',payload,0x00100a00)],
                [symbol('.drectve',1,storage=3,auxiliary=aux(len(payload),selection=0))])
            path=Path(directory)/'authored.obj';path.write_bytes(raw);return Coff(path)
        with tempfile.TemporaryDirectory()as temp:
            self.assertEqual(len(m.validate_consumer_directives(parsed(expected,temp))),4)
            for tokens in(expected+['/INCLUDE:_FNV_BOOTSTRAP_EARLY_SLOT'],expected+['/DEFAULTLIB:MSVCRT'],
                expected[:-1],expected[1:],expected+['/DEFAULTLIB:UUID.LIB']):
                with self.subTest(tokens=tokens),self.assertRaisesRegex(ValueError,'consumer directives'):
                    m.validate_consumer_directives(parsed(tokens,temp))

    def test_public_external_existing_output_rejected(self):
        with tempfile.TemporaryDirectory()as temp,patch.object(m,'ROOT',Path(temp).resolve()):
            private=Path(temp)/'build/rebuild/new';self.assertEqual(m.private_directory(private),private)
            for p in(Path(temp)/'src/new',Path(temp).parent/'outside'):
                with self.assertRaises(ValueError):m.private_directory(p)
            private.mkdir(parents=True)
            with self.assertRaises(ValueError):m.private_directory(private)

    def test_no_opt_in_never_invokes_native_or_reads_image(self):
        with self.assertRaisesRegex(ValueError,'opt-in'):m.project(SimpleNamespace(allow_projection=False))
        with self.assertRaisesRegex(ValueError,'opt-in'):m.prepare(SimpleNamespace(allow_native_prepare=False))

    def test_review_wrong_flags_sources_or_checks_rejected(self):
        with tempfile.TemporaryDirectory()as temp,patch.object(m,'source_manifest',return_value={}):
            p=Path(temp)/'review.json'
            import json
            base=dict(schema_version=1,kind='stdio-reader-component-source-review',status='approved',reviewer='independent',
                sources={},allow_execute=False,allow_projection=True,checks={k:True for k in m.CHECKS})
            for key,value in [('allow_projection',False),('allow_execute',True),('sources',{'stale':'0'*64}),('checks',{})]:
                r=copy.deepcopy(base);r[key]=value;p.write_text(json.dumps(r))
                with self.subTest(key=key),self.assertRaisesRegex(ValueError,'source review'):m.review_gate(p,m.sha(p),'projection',{})

    def test_projection_review_gate_binds_hashes_and_execution_false(self):
        with patch.object(m,'source_manifest',return_value={}):
            proof=dict(kind='stdio-reader-projected',selected_sha256='1'*64,sources={},
                projection=dict(member_sha256='1'*64,certificate_sha256=m.CERTIFICATE))
            with self.assertRaisesRegex(ValueError,'review'):m.projection_review(proof,{})
            approval=dict(kind='stdio-reader-projection-review',status='approved',reviewer='other',
                selected_sha256='1'*64,allow_native_prepare=True,allow_execute=False,
                checks={k:True for k in ('complete_COFF_bijection','exact_root_certificate','unchanged_reference_comparison',
                    'one_unresolved_fread','typed_normal_FILE_consumer','normal_fread_functional_contract')})
            m.projection_review(proof,approval)
            approval['allow_execute']=True
            with self.assertRaises(ValueError):m.projection_review(proof,approval)

    def test_input_drift_and_optional_index_rejected(self):
        with tempfile.TemporaryDirectory()as temp,patch.object(m,'ROOT',Path(temp)):
            p=Path(temp)/'input';p.write_bytes(b'authored');observed={p:m.sha(p)}
            m.stable(observed);p.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'changed'):m.stable(observed)
            observed[p]=m.sha(p);idx=Path(temp)/'build/function_index.json';idx.parent.mkdir();idx.write_text('{}')
            with self.assertRaisesRegex(ValueError,'index'):m.stable(observed)

    def test_final_publication_drift_removes_only_new_receipt(self):
        with tempfile.TemporaryDirectory()as temp,patch.object(m,'ROOT',Path(temp)):
            out=Path(temp);protected=out/'protected';protected.write_bytes(b'owned');observed={protected:m.sha(protected)}
            real=m.save
            def changed(path,value):
                real(path,value)
                if Path(path).name=='projection.json':protected.write_bytes(b'drift')
            with patch.object(m,'save',side_effect=changed),self.assertRaisesRegex(ValueError,'changed'):
                m.publish_receipt(out,'projection.json',{},observed)
            self.assertFalse((out/'projection.json').exists())
            self.assertTrue((out/'failure.json').exists())
            self.assertEqual(protected.read_bytes(),b'drift')

    def test_host_is_typed_declaration_with_source_owned_file_lifetime(self):
        source=m.SOURCE.read_text()
        self.assertIn('void __thiscall ReadOrMarkFailed(void* buffer, unsigned int count);',source)
        self.assertNotIn('void FUN_00d2bcd0_class::ReadOrMarkFailed',source)
        self.assertEqual(source.count('reader.ReadOrMarkFailed('),4)
        for forbidden in('__fastcall','__asm','__declspec(naked)','ExitProcess(','system(','CreateProcess('):self.assertNotIn(forbidden,source)
        for required in('fopen(argv[1], "rb")','fclose(stream)','sizeof(FUN_00d2bcd0_class) == 20','offsetof(FUN_00d2bcd0_class, m_0c) == 12'):
            self.assertIn(required,source)
        self.assertLessEqual(len(m.INPUT),64)
        self.assertIn(m.INPUT.decode().replace('\n','\\n'),source)

    def linked_fixture(self,temp,alter=None):
        import crt_bootstrap_contract as native
        import data_plan,import_plan
        selected=Path(temp)/'selected.obj';consumer=Path(temp)/'consumer.obj'
        output,_=self.project(authored_leaf());selected.write_bytes(output);consumer.write_bytes(caller())
        mapfile=Path(temp)/'map';mapfile.write_text('authored map input')
        addresses={m.EXPORT:0x401000,'_fread':0x402000,'_own_source_consumer':0x403000,'_mainCRTStartup':0x405000}
        mapping={name:dict(address=address,owner='selected.obj'if name==m.EXPORT else 'consumer.obj'if name=='_own_source_consumer'else'LIBCMT:normal.obj')for name,address in addresses.items()}
        for name in('_fopen','_fseek','_ftell','_fclose','_exit','___security_cookie','___security_init_cookie'):
            mapping[name]=dict(address=0x406000+len(mapping)*16,owner='LIBCMT:normal.obj')
        game=bytearray(coff.parse(output)['sections'][2]['payload'])
        struct.pack_into('<i',game,20,addresses['_fread']-(addresses[m.EXPORT]+24))
        mode={'bad_target_section':False}
        if alter:alter(mapping,game,mode)
        class FakePe:
            base=0x400000
            def __init__(self,path):pass
            def close(self):pass
            def section(self,rva,size,required):
                return dict(flags=0xc0000040 if mode['bad_target_section']and rva==0x2000 else 0x60000020)
            def relocations(self):return []
            def unpack(self,fmt,offset):return(0x80 if offset==0x3c else 0x5000,)
            def read_rva(self,rva,size,allow_code=False):
                if rva==0x1000 and size==39:return bytes(game)
                if 0x3000<=rva<0x3010 and size==4:return struct.pack('<i',0x401000-(self.base+rva+4))
                raise AssertionError((rva,size))
        with patch.object(native,'map_symbols',return_value=mapping),patch.object(native,'validate_contributors',return_value={}),\
            patch.object(data_plan,'Pe',FakePe),patch.object(import_plan,'parse_imports',return_value=[dict(dll='KERNEL32.dll',export=dict(kind='name',name='ReadFile'))]):
            return m.inspect_link(Path(temp)/'not-executed.exe',mapfile,selected,consumer,{})

    def test_linked_actual_fread_function_and_four_typed_calls(self):
        with tempfile.TemporaryDirectory()as temp:
            result=self.linked_fixture(temp)
            self.assertTrue(result['Game_call_targets_normal_function'])
            self.assertEqual(len(result['typed_consumer_calls']),4)

    def test_linked_wrong_field_payload_data_target_or_extra_game_provider_rejected(self):
        cases=[lambda table,data,mode:struct.pack_into('<i',data,20,0),
            lambda table,data,mode:data.__setitem__(0,data[0]^1),
            lambda table,data,mode:mode.__setitem__('bad_target_section',True),
            lambda table,data,mode:table.__setitem__('_extra_game',dict(address=0x407000,owner='selected.obj')),
            lambda table,data,mode:table['_fread'].__setitem__('owner','KERNEL32:import.obj')]
        for case in cases:
            with self.subTest(case=case),tempfile.TemporaryDirectory()as temp,self.assertRaises(ValueError):self.linked_fixture(temp,case)


if __name__=='__main__':unittest.main()
