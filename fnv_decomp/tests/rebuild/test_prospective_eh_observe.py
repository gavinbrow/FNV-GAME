"""Authored-only prospective EH scope and comparison checks; no game inputs."""
import contextlib,copy,struct,sys,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/rebuild'));sys.path.insert(0,str(ROOT/'tools'))
import prospective_eh_observe as observe
import prospective_eh_collect as collect
from test_parent_eh_adapter_lane08 import authored_parent

@contextlib.contextmanager
def valid_case(edit=None):
    case=authored_parent(object_edit=edit)
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'authored.obj';path.write_bytes(case['raw']);core=observe.oracle.Coff(path);obj=observe.coff.parse(core.data);f=case['recipe']['functions'][0]
        root=dict(original_address=f['address'],symbol=f['symbol'],size=f['size'],symbol_index=8,section=3,value=0)
        yield case,root,obj,core
def source_request():
    units=[]
    for index,addresses in collect.EXPECTED.items():
        rid='%04d-'%index+'a'*16;unit=dict(recipe_index=index,recipe_id=rid,object_sha256='b'*64,object='not-opened.obj',roots=[])
        unit['roots']=[dict(recipe_index=index,recipe_id=rid,object_sha256='b'*64,original_address=a,size=157) for a in sorted(addresses)];units.append(unit)
    inputs=[dict(path=p,sha256=h) for p,h in collect.AUTHORITY.items()]+[dict(path=p,sha256='c'*64) for p in collect.TOOLS]
    return dict(kind='prospective-UUID-seven-parent-EH-v1',authority_kind='qualified-caller-prospective-only',measured_V13_or_593_authority=False,units=units,DATA01204364_materialization_approved=False,authority=collect.AUTHORITY,inputs=inputs,permissions=dict(root_original_scope_confirmed=False),reference=None,reference_image_gate=None)
class Tests(unittest.TestCase):
    def test_noncontiguous_selected_original_comparison(self):
        with valid_case() as (case,root,obj,core):
            view=observe.inventory_parent(obj,root);result=observe.compare_parent(core,obj,view,case['recipe'],[case['recipe']],case['reference'],case['executable_ranges'])
            self.assertEqual(result['ordinary'][0]['verdict'],'match');self.assertTrue(all(r['local_MATCH'] for r in result['pieces']));self.assertTrue(result['metadata_comparisons'][0]['full_MATCH']);self.assertFalse(result['full_closure_verified']);self.assertTrue(result['ordinary'][0]['relocations'])
            spans=result['reference_scope'];self.assertFalse(any(r['start']<=0x20000ff8<r['start']+r['size'] for r in spans))
    def test_each_oracle_call_contains_one_selected_function(self):
        with valid_case() as (case,root,obj,core):
            recipe=copy.deepcopy(case['recipe']);recipe['functions'].append(dict(address='0x00999999',symbol='_unrequested',size=77));original=observe.oracle.eh_sections;calls=[]
            def checked(core,pe,unit,rows,names):calls.append(unit['functions']);return original(core,pe,unit,rows,names)
            with patch.object(observe.oracle,'eh_sections',side_effect=checked):observe.compare_parent(core,obj,observe.inventory_parent(obj,root),recipe,[recipe],case['reference'],case['executable_ranges'])
            self.assertEqual(calls,[[recipe['functions'][0]]])
    def test_false_piece_without_errors_is_preserved(self):
        with valid_case() as (case,root,obj,core):
            class Changed:
                def read(self,address,size):
                    raw=case['reference'].read(address,size)
                    return bytes([raw[0]^1])+raw[1:] if address==0x20000000 and size==8 else raw
            result=observe.compare_parent(core,obj,observe.inventory_parent(obj,root),case['recipe'],[case['recipe']],Changed(),case['executable_ranges'])
            self.assertFalse(result['pieces'][0]['local_MATCH']);self.assertEqual(result['errors'],[]);self.assertFalse(result['runtime_eligible'])
    def test_metadata_addend_selects_effective_noncontiguous_cut(self):
        def edit(obj):
            sec=obj['sections'][6];sec['payload']+=struct.pack('<I',8);sec['size']+=4;sec['relocs'].append((44,12,6))
            for symbol in obj['symbols'].values():
                if symbol['section']==6 and symbol['aux_count']==1:
                    raw=bytearray(symbol['aux']);struct.pack_into('<I',raw,0,sec['size']);struct.pack_into('<H',raw,4,len(sec['relocs']));symbol['aux']=bytes(raw)
        with valid_case(edit) as (case,root,obj,core):
            class Reference:
                def read(self,address,size):
                    original=bytearray(case['reference'].read(address,size));pointer=struct.pack('<I',0x20001000)
                    for i in range(size):
                        if 0x3000002c<=address+i<0x30000030:original[i]=pointer[address+i-0x3000002c]
                    return bytes(original)
            result=observe.compare_parent(core,obj,observe.inventory_parent(obj,root),case['recipe'],[case['recipe']],Reference(),case['executable_ranges']);field=result['metadata_comparisons'][0]['fields'][-1]
            self.assertEqual(field['addend'],8);self.assertEqual(field['expected_target'],0x20001000);self.assertTrue(field['comparison_MATCH'])
    def test_catch_and_unknown_flags_are_not_nocatch(self):
        def edit(obj):
            at=obj['symbols'][24]['value'];data=bytearray(obj['sections'][6]['payload']);struct.pack_into('<I',data,at+12,1);struct.pack_into('<I',data,at+32,99);obj['sections'][6]['payload']=bytes(data)
        with valid_case(edit) as (_,root,obj,_):
            view=observe.inventory_parent(obj,root);self.assertIn('CATCH_IP_OR_TYPELIST_FAMILY_REQUIRES_ADAPTER',view['unsupported']);self.assertIn('UNKNOWN_FUNCINFO_FLAGS',view['unsupported']);self.assertFalse(view['no_catch_family_approved'])
    def test_variable_piece_lengths_not_hardcoded(self):
        with valid_case() as (_,root,obj,_):
            obj['sections'][4]['size']+=10;obj['sections'][4]['payload']+=b'\x90'*10
            for s in obj['symbols'].values():
                if s['section']==4 and s['aux_count']==1:
                    raw=bytearray(s['aux']);struct.pack_into('<I',raw,0,obj['sections'][4]['size']);s['aux']=bytes(raw)
            view=observe.inventory_parent(obj,root);self.assertEqual([p['end']-p['start'] for p in view['pieces']],[8,37])
    def test_missing_handler_is_unknown(self):
        with valid_case() as (_,root,obj,_):
            obj['symbols'][19]['name']='_not_a_known_handler';view=observe.inventory_parent(obj,root);self.assertIn('MISSING_AMBIGUOUS_OR_FOREIGN_HANDLER',view['unsupported']);self.assertEqual(view['comparison_status'],'NOT_RUN')
    def test_native_execution_domains_are_retained_and_block_reads(self):
        for sn,flags in ((3,0x40301040),(4,0x40301040),(6,0x60501020)):
            with valid_case() as (case,root,obj,_):
                obj['sections'][sn]['flags']=flags;view=observe.inventory_parent(obj,root);self.assertTrue(any('DOMAIN_OR_BACKING' in r for r in view['unsupported']))
                backend=SimpleNamespace(read=lambda *_:self.fail('domain failure must precede original read'))
                with self.assertRaisesRegex(ValueError,'native domain'):observe.prepare_scope(obj,view,backend,case['executable_ranges'])
    def test_budget_and_wrong_domain_before_backend_read(self):
        backend=SimpleNamespace(read=lambda *_:self.fail('must not read'))
        ref=observe.ScopedReference(backend,[(0x1000,0x2000)])
        with self.assertRaises(ValueError):ref.allow(0x1000,4,'data','wrong')
        ref.allow(0x1000,4,'code','authored');ref.total=1024**2
        with self.assertRaises(ValueError):ref.read(0x1000,4)
    def test_default_request_denies_before_any_original_read(self):
        request=source_request();self.assertFalse(collect.validate_request(request)['original_reads_permitted'])
        with patch.object(collect,'bounded_hash',side_effect=AssertionError('original read')):
            with self.assertRaisesRegex(ValueError,'not confirmed'):collect.observe_request(request)
    def test_historical_2770_root_and_scratch_traversal_rejected(self):
        request=source_request();unit=next(u for u in request['units'] if u['recipe_index']==2770);unit['roots'][0]['original_address']='0x00c50610'
        with self.assertRaises(ValueError):collect.validate_request(request)
        request=source_request();request['units'][0]['recipe_id']='../../escape'
        with self.assertRaises(ValueError):collect.validate_request(request)
    def test_allocation_guard_and_hash_before_scratch(self):
        raw=bytearray(60);struct.pack_into('<H',raw,2,1);struct.pack_into('<I',raw,36,0x7fffffff)
        with tempfile.TemporaryDirectory() as directory:
            scratch=Path(directory)
            with self.assertRaisesRegex(ValueError,'allocation cap'):collect.copy_authenticated_buffer(bytes(raw),observe.sha(raw),scratch,'1445-'+'a'*16+'.obj',lambda:None)
            self.assertEqual(list(scratch.iterdir()),[])
            with self.assertRaisesRegex(ValueError,'SHA'):collect.copy_authenticated_buffer(b'authored','0'*64,scratch,'1445-'+'a'*16+'.obj',lambda:None)
    def test_scratch_is_identical_exclusive_and_bounded(self):
        with valid_case() as (case,_,_,_):
            with tempfile.TemporaryDirectory() as directory:
                scratch=Path(directory);name='1445-'+'a'*16+'.obj';p,_=collect.copy_authenticated_buffer(case['raw'],observe.sha(case['raw']),scratch,name,lambda:None);self.assertEqual(p.read_bytes(),case['raw'])
                with self.assertRaises(FileExistsError):collect.copy_authenticated_buffer(case['raw'],observe.sha(case['raw']),scratch,name,lambda:None)
                with self.assertRaisesRegex(ValueError,'unsafe'):collect.copy_authenticated_buffer(case['raw'],observe.sha(case['raw']),scratch,'../escape.obj',lambda:None)
    def test_execution_domains_use_PE_characteristics(self):
        data=bytearray(512);struct.pack_into('<I',data,0x3c,0x80);data[0x80:0x84]=b'PE\0\0';struct.pack_into('<H',data,0x86,1);struct.pack_into('<H',data,0x94,224);at=0x80+24+224;struct.pack_into('<III',data,at+8,4096,4096,4096);struct.pack_into('<I',data,at+36,0x40000040)
        pe=SimpleNamespace(data=data,base=0x400000);self.assertEqual(collect.executable_ranges(pe),[]);struct.pack_into('<I',data,at+36,0x60000020);self.assertEqual(collect.executable_ranges(pe),[(0x401000,0x402000)])
    def test_unbounded_input_and_measured_authority_rejected(self):
        request=source_request();request['inputs'][0]['limit']=2**40
        with self.assertRaises(ValueError):collect.validate_request(request)
        request=source_request();request['measured_V13_or_593_authority']=True
        with self.assertRaises(ValueError):collect.validate_request(request)
if __name__=='__main__':unittest.main()
