"""Authored in-memory COFF; no original objects, compiler, link or executable."""
import copy
from pathlib import Path
import struct
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import overlay_code_projection as overlay
import coff_code_archive as coff
import runtime_code_pool as pool
from test_root_code_closure import fixture,omitted_function,retarget,sym,section


def encode(obj):
    strings=bytearray(4);symbols=bytearray()
    for i,s in sorted(obj['symbols'].items()):
        off=len(strings);strings.extend(s['name'].encode()+b'\0')
        symbols.extend(struct.pack('<IIIhHBB',0,off,s['value'],s['section'],s['type'],s['storage'],s['aux_count'])+s['aux'])
    struct.pack_into('<I',strings,0,len(strings));count=len(obj['sections']);pos=20+40*count;body=bytearray();headers=[]
    for i,s in sorted(obj['sections'].items()):
        raw=pos+len(body);body.extend(s['payload']);relptr=pos+len(body)
        body.extend(b''.join(struct.pack('<IIH',*r) for r in s['relocs']))
        headers.append(struct.pack('<8sIIIIIIHHI',s['name'].encode().ljust(8,b'\0'),0,0,s['size'],raw,relptr,0,len(s['relocs']),0,s['flags']))
    return struct.pack('<HHIIIHH',0x14c,count,0,pos+len(body),obj['symbol_count'],0,0)+b''.join(headers)+body+symbols+strings


def inputs(obj=None,contract=None):
    if obj is None:obj,contract=fixture()
    raw=encode(obj);parsed=coff.parse(raw);roots=contract['roots'];functions=contract['unit_verified_functions']
    bindings=copy.deepcopy(contract['fields'])
    for row in bindings:
        row.update(event='SELECTED_FUNCTION_COFF_RELOCATION',function_symbol=next(f['symbol'] for f in functions if f['address']==row['function_va']),
            original_field_va='0x%08x'%(int(row['function_va'],16)+row['source_field_offset']),overlay_unit_id='unit',
            actual_object_sha256=coff.digest(raw),actual_generated_source_sha256='b'*64)
        row['coff_relocation']['width']=4
    scope=[]
    for f in functions:
        si=next(i for i,s in parsed['symbols'].items() if s['name']==f['symbol'])
        scope.append(dict(address=f['address'],symbol=f['symbol'],size=f['size'],overlay_native=dict(section=f['section'],value=f['value'],symbol_index=si)))
    context=dict(overlay_unit_id='unit',roots=roots,original_ancestry=dict(recipe_id='authored',object_sha256='a'*64),
        actual_object=dict(sha256=coff.digest(raw)),actual_source_proof=dict(generated_source_sha256='b'*64),
        original_eh_proof_lineage=dict(original_retained_unit=dict(eh_sections=[])))
    unit=dict(scope=scope,parsed=parsed,registry_sha256='c'*64,observer_sha256='d'*64,parser_sha256='e'*64)
    providers={r['original_address']:dict(recipe_id='authored',object_sha256='a'*64,symbol_index=r['symbol_index']) for r in roots}
    coverage={a:dict(status='HISTORICAL_BLOCKED',physical_identity=p) for a,p in providers.items()}
    return raw,context,unit,bindings,providers,coverage


class OverlayProjectionTests(unittest.TestCase):
    def test_export_uses_old_logical_identity_not_new_native_object_identity(self):
        raw,c,u,b,p,cov=inputs();p['0x00500000']['symbol_index']=777
        plan=overlay.choose_group(c,u,b,p,cov,[],{})
        self.assertTrue(plan['candidate'])
        old=pool.canonical(p['0x00500000']);fresh=pool.canonical(dict(recipe_id='authored',object_sha256=coff.digest(raw),symbol_index=2))
        self.assertNotEqual(old,fresh)
        output,receipt=overlay.project(raw,c,u,b,p,cov,[],{},plan)
        self.assertEqual(coff.exports(output),[old]);self.assertEqual(receipt['exports'],[old])
        before,after=coff.parse(raw),coff.parse(output)
        self.assertEqual(before['sections'][1]['payload'],after['sections'][receipt['maps']['section_map'][1]]['payload'])
        self.assertEqual(receipt['old_logical_identities'][0]['symbol_index'],777)

    def test_native_inventory_cannot_omit_fields_or_change_a_primary(self):
        raw,c,u,b,p,cov=inputs();obj=u['parsed']
        inventory=dict(object_sha256=coff.digest(raw),sections=[dict(index=i,name=s['name'],size=s['size'],flags=s['flags'],
            payload_sha256=coff.digest(s['payload']),relocs=s['relocs']) for i,s in obj['sections'].items()],
            symbols=[dict(index=i,**{k:s[k] for k in ('name','section','value','type','storage','aux_count')},
                auxiliary_record_sha256=coff.digest(s['aux']) if s['aux_count'] else None) for i,s in obj['symbols'].items()],
            all_physical_fields=[dict(section=i,offset=off,symbol_index=si,kind=kind) for i,s in obj['sections'].items() for off,si,kind in s['relocs']])
        overlay.validate_inventory(obj,inventory,coff.digest(raw))
        for field in ('fields','primary','aux'):
            bad=copy.deepcopy(inventory)
            if field=='fields':bad['all_physical_fields']=[]
            elif field=='primary':bad['symbols'][0]['value']=1
            else:bad['symbols'][0]['auxiliary_record_sha256']='0'*64
            with self.assertRaises(ValueError):overlay.validate_inventory(obj,bad,coff.digest(raw))

    def test_omitted_defined_code_becomes_old_global_reference_never_extra_export(self):
        obj,contract=fixture();sec,ss,fn=omitted_function(obj,contract);retarget(obj,contract,fn)
        row=contract['fields'][0];row.update(derived_source_symbol_base_va='0x00500100',exact_original_target_va='0x00500100',classification='SELECTED_CODE_ENTRY',
            code_owners=[dict(address='0x00500100',offset=0)],code_ownership_ambiguous=False)
        raw,c,u,b,p,cov=inputs(obj,contract);target=dict(recipe_id='selected-target',object_sha256='f'*64,symbol_index=37);p['0x00500100']=target
        plan=overlay.choose_group(c,u,b,p,cov,[],{});self.assertTrue(plan['candidate'])
        output,receipt=overlay.project(raw,c,u,b,p,cov,[],{},plan);after=coff.parse(output)
        self.assertEqual(len(coff.exports(output)),1)
        ref=next(s for s in after['symbols'].values() if s['name']==pool.canonical(target))
        self.assertEqual((ref['section'],ref['value'],ref['storage']),(0,0,2))

    def test_current_baseline_export_name_or_physical_emission_blocks(self):
        raw,c,u,b,p,cov=inputs();name=pool.canonical(p['0x00500000'])
        self.assertFalse(overlay.choose_group(c,u,b,p,cov,[name],{})['candidate'])
        cov['0x00500000']['status']='EMITTED'
        self.assertFalse(overlay.choose_group(c,u,b,p,cov,[],{})['candidate'])

    def test_remaining_missing_root_cannot_be_exported_or_disappear(self):
        raw,c,u,b,p,cov=inputs();b.append(dict(function_va='0x00500000',coff_relocation=None,source_field_offset=8))
        plan=overlay.choose_group(c,u,b,p,cov,[],{})
        self.assertFalse(plan['candidate']);self.assertEqual(plan['blocked_missing_roots'],['0x00500000'])

    def test_fresh_parent_EH_and_old_unclosed_lineage_are_not_faked_empty(self):
        raw,c,u,b,p,cov=inputs();c['original_eh_proof_lineage']['original_retained_unit']['eh_sections']=[[1,2,True,'0x00500000',[]]]
        plan=overlay.choose_group(c,u,b,p,cov,[],{})
        self.assertFalse(plan['candidate'])
        self.assertIn('PARENT_EH_REQUIRES_CLOSURE_ADAPTER',{x['code'] for x in plan['attempts'][0]['blockers']})
        obj,contract=fixture();eh=section(obj,'.text$x',bytes(4),0x60501020,selection=1);ei=sym(obj,'__eh_body',eh,typ=32);retarget(obj,contract,ei)
        raw,c,u,b,p,cov=inputs(obj,contract)
        fresh=overlay.fresh_frame_facts(u['parsed'],overlay.closure_contract(c,u,b,c['roots'],{})['unit_verified_functions'],c['roots'],c['original_eh_proof_lineage'])
        self.assertTrue(any(x['kind']=='FRESH_NATIVE_PARENT_FRAME_REFERENCE' for x in fresh))

    def test_unknown_local_label_rule_is_not_waived_by_prior_bookkeeping_proof(self):
        obj,contract=fixture();sec,ss,fn=omitted_function(obj,contract);sym(obj,'$finished$900',sec,value=4,storage=6)
        raw,c,u,b,p,cov=inputs(obj,contract);plan=overlay.choose_group(c,u,b,p,cov,[],{})
        self.assertFalse(plan['candidate']);self.assertIn('LABEL_OMISSION_NOT_PROVED',{x['code'] for x in plan['attempts'][0]['blockers']})

    def test_duplicate_code_reference_records_keep_distinct_physical_indices(self):
        obj,contract=fixture();obj['symbols'][3].update(name='_callA',type=32)
        other=sym(obj,'_callB',0,typ=32);obj['sections'][1]['relocs'].append((8,other,20))
        obj['symbols'][0]['aux']=struct.pack('<IHHIhBBH',16,2,0,0,0,1,0,0)
        first=contract['fields'][0];first['coff_relocation'].update(symbol='_callA',symbol_type=32)
        first.update(derived_source_symbol_base_va='0x00600000',exact_original_target_va='0x00600000',classification='SELECTED_CODE_ENTRY',
            code_owners=[dict(address='0x00600000',offset=0)],code_ownership_ambiguous=False)
        second=copy.deepcopy(first);second.update(physical_offset=8,source_field_offset=8);second['coff_relocation'].update(offset=8,symbol_index=other,symbol='_callB',kind=20)
        contract['fields'].append(second)
        raw,c,u,b,p,cov=inputs(obj,contract);p['0x00600000']=dict(recipe_id='target',object_sha256='f'*64,symbol_index=77)
        plan=overlay.choose_group(c,u,b,p,cov,[],{});self.assertTrue(plan['candidate'])
        self.assertEqual(len(plan['namespace']['groups']),1)
        output,receipt=overlay.project(raw,c,u,b,p,cov,[],{},plan);after=coff.parse(output);name=pool.canonical(p['0x00600000'])
        self.assertEqual(len([s for s in after['symbols'].values() if s['name']==name]),2)
        indices=[r[1] for r in after['sections'][receipt['maps']['section_map'][1]]['relocs']]
        self.assertEqual(len(set(indices)),2)

    def test_stale_plan_and_extra_export_scope_rejected(self):
        raw,c,u,b,p,cov=inputs();plan=overlay.choose_group(c,u,b,p,cov,[],{});bad=copy.deepcopy(plan);bad['namespace']['expected_exports'].append('_invented')
        with self.assertRaises(ValueError):overlay.project(raw,c,u,b,p,cov,[],{},bad)
        with self.assertRaises(ValueError):overlay.project(raw[:-1]+b'X',c,u,b,p,cov,[],{},plan)

    def test_exact_whole_subsets_recomputed_instead_of_unioning_one_root_drops(self):
        obj,contract=fixture();sec,ss,fn=omitted_function(obj,contract)
        contract['roots'].append(dict(original_address='0x00500100',symbol=obj['symbols'][fn]['name'],symbol_index=fn,section=sec,value=0,size=16))
        raw,c,u,b,p,cov=inputs(obj,contract)
        both=overlay.choose_group(c,u,b,p,cov,[],{})
        self.assertEqual(len(both['contract']['roots']),2)
        c['original_eh_proof_lineage']['original_retained_unit']['eh_sections']=[[1,2,False,'0x00500100',[]]]
        one=overlay.choose_group(c,u,b,p,cov,[],{})
        self.assertTrue(one['candidate']);self.assertEqual([r['original_address'] for r in one['contract']['roots']],['0x00500000'])
        self.assertEqual(len(one['attempts'][0]['roots']),2)
        self.assertNotEqual(one['attempts'][0]['closure_sha256'],overlay.digest(one['closure']))

    def test_nonCODE_duplicate_alias_group_remains_blocked(self):
        obj,contract=fixture();other=sym(obj,'_other_data',0)
        obj['sections'][1]['relocs'].append((8,other,6));obj['symbols'][0]['aux']=struct.pack('<IHHIhBBH',16,2,0,0,0,1,0,0)
        row=copy.deepcopy(contract['fields'][0]);row.update(physical_offset=8,source_field_offset=8);row['coff_relocation'].update(offset=8,symbol_index=other,symbol='_other_data');contract['fields'].append(row)
        raw,c,u,b,p,cov=inputs(obj,contract);plan=overlay.choose_group(c,u,b,p,cov,[],{})
        self.assertFalse(plan['candidate']);self.assertIn('non-CODE logical aliases',plan['attempts'][0]['namespace_blocker'])

    def test_logical_provider_map_requires_complete_old_native_selection(self):
        selected={'0x00500000':dict(recipe_id='old',recipe_index=0,symbol='_f',section=3,value=0,size=16)}
        manifest=dict(units=[dict(recipe_id='old',object_sha256='a'*64)])
        row=dict(original_address='0x00500000',selected_native=dict(symbol='_f',section=3,value=0,size=16,symbol_index=42),physical_identity=dict(recipe_id='old',object_sha256='a'*64,symbol_index=42))
        self.assertEqual(overlay.logical_providers([row],selected,manifest)['0x00500000']['symbol_index'],42)
        for rows in ([],[row,row]):
            with self.assertRaises(ValueError):overlay.logical_providers(rows,selected,manifest)
        bad=copy.deepcopy(row);bad['physical_identity']['object_sha256']='b'*64
        with self.assertRaises(ValueError):overlay.logical_providers([bad],selected,manifest)


if __name__=='__main__':unittest.main()
