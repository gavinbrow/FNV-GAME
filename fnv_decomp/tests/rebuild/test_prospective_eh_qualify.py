"""Authored dictionaries only; never reads game evidence or starts a process."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('authored_prospective_qualify',ROOT/'tools/rebuild/prospective_eh_qualify.py')
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)

def h(value):return q.digest(value)

def seal(bundle,anchors):
    """Authored expected anchors; deliberately not independently verified proof."""
    anchors['root_inputs']={r['root_address']:h(r) for r in bundle['roots']}
    anchors['witnesses']={q.claim_key(r['root_address'],e['obligation_id'],e['subject']):
        dict(sha256=e['witness_sha256'],facts_sha256=h(e['facts']))
        for r in bundle['roots'] for e in r['evidence'] if e['status']=='supported'}

def valid_case():
    anchors={k:h(k) for k in ('observation_sha256','review_sha256','request_sha256','image_sha256','producer_sha256')}
    anchors.update(objects={str(i):h(['object',i]) for i in set(q.ROOTS.values())},
        sources={str(i):h(['source',i]) for i in set(q.ROOTS.values())},
        source_lineage={str(i):h(['lineage',i]) for i in set(q.ROOTS.values())},
        cleanup_receipts={r:h(['cleanup-semantics',r]) for r in q.ROOTS},
        safe_seh_counts=dict(zip(q.ROOTS,[2,2,84,84,27,27,27])),
        frame_receipts={r:h(['frame',r]) for r in q.ROOTS},expanded_scopes={r:h(['expanded',r]) for r in q.ROOTS},
        highlow_directory_sha256=h('authored relocation-directory'))
    bundle=dict(kind='prospective-UUID-seven-qualification-input-v1',provenance={k:anchors[k] for k in ('observation_sha256','review_sha256','request_sha256','image_sha256','producer_sha256')},roots=[])
    for n,(root,index) in enumerate(q.ROOTS.items()):
        parent=100+n*3;code=parent+1;data=parent+2;base=0x20000000+n*0x10000;meta=0x30000000+n*0x10000
        targets=[]
        def target(i,name,section,value,domain,role,subtype,original):
            t=dict(index=i,name=name,section=section,value=value,storage=3 if section else 2,type=32 if domain=='code' else 0,aux_count=0,
                   original_base=original,canonical_role=role,semantic_domain=domain,contract_kind=subtype,
                   canonical_identity_sha256=h([role,domain,subtype,original]))
            if section:t['owner_root']=root
            targets.append(t)
        target(10+n*100,'authored_cleanup_'+str(n),code,0,'code','code','parent-owned-cleanup',base)
        target(11+n*100,'authored_unwind_'+str(n),data,0,'data','data','parent-owned-state',meta)
        target(12+n*100,'authored_handler_'+str(n),code,11,'code','code','parent-owned-handler',base+0x1000)
        target(13+n*100,'authored_info_'+str(n),data,8,'data','data','parent-owned-state',meta+8)
        target(20,'___CxxFrameHandler3',0,0,'code','crt-contract','cxx-frame-handler',0x70000000)
        target(21,'___security_cookie',0,0,'data','data','security-cookie',0x71000000)
        target(22,'@__security_check_cookie@4',0,0,'code','crt-contract','security-cookie-check',0x72000000)
        target(23,'authored_delete',0,0,'code','code','ordinary-function',0x73000000)
        targetmap={t['index']:t for t in targets};fields=[]
        def field(name,section,offset,kind,ti,addend=0):
            original_site=(int(root,16)+offset if section==parent else meta+offset if section==data else base+offset if offset<11 else base+0x1000+offset-11)
            fields.append(dict(original_site=original_site,original_target=targetmap[ti]['original_base']+addend,comparison_MATCH=True,field_id=name,owner_root=root,section=section,offset=offset,kind=kind,target_index=ti,target_name=targetmap[ti]['name'],addend=addend))
        field('action',data,4,'DIR32',10+n*100);field('unwind',data,16,'DIR32',11+n*100)
        field('parent-handler',parent,4,'DIR32',12+n*100);field('cookie',parent,21,'DIR32',21)
        field('cleanup-call',code,6,'REL32',23);field('checker',code,14,'REL32',22)
        field('info',code,23,'DIR32',13+n*100);field('handler',code,34,'REL32',20)
        sites=[dict(subject='metadata:'+str(offset),owner_root=root,section=data,offset=offset,field_id=name,target_index=ti,
                    addend=0,original_site=meta+offset,original_target=targetmap[ti]['original_base'],MATCH=True)
               for offset,name,ti in ((4,'action',10+n*100),(16,'unwind',11+n*100))]
        row=dict(root_address=root,recipe_index=index,object_sha256=anchors['objects'][str(index)],source_context_sha256=anchors['sources'][str(index)],
            parent=dict(section=parent,value=0,size=157,MATCH=True,errors=[]),
            owned_sections=[dict(section=code,parent_section=parent,domain='code',size=38,flags=0x20000000,backed=True),dict(section=data,parent_section=parent,domain='data',size=44,flags=0,backed=True)],
            pieces=[dict(section=code,start=0,end=11,original_start=base,original_end=base+11,owner_root=root,MATCH=True),dict(section=code,start=11,end=38,original_start=base+0x1000,original_end=base+0x1000+27,owner_root=root,MATCH=True)],
            field_inventory=copy.deepcopy(fields),physical_fields=fields,targets=targets,metadata_sites=sites,metadata_original_base=meta,
            funcinfo=dict(offset=8,magic=0x19930522,max_state=1,unwind_field_id='unwind',try_count=0,try_map=0,ip_count=0,ip_map=0,type_list=0,flags=1),state_graph=[dict(state=0,to_state=-1,action_field_id='action')],metadata_nonrelocation_MATCH=True,metadata_full_MATCH=True,evidence=[],inherited_blockers=[],EH_errors=[],unknown_diagnostics=[])
        count=anchors['safe_seh_counts'][root];members=[(j,rr) for j,(rr,ii) in enumerate(q.ROOTS.items()) if ii==index];sxrecords=[]
        for ordinal in range(count):
            if ordinal<len(members):
                j,rr=members[ordinal];st=dict(index=12+j*100,name='authored_handler_'+str(j),section=101+j*3,value=11,storage=3,type=32,aux_count=0)
                ts=dict(index=101+j*3,extent=38,flags=0x20000000,backed=True)
            else:
                st=dict(index=10000+index*200+ordinal,name='authored_foreign_'+str(index)+'_'+str(ordinal),section=1000+ordinal,value=0,storage=3,type=32,aux_count=0)
                ts=dict(index=1000+ordinal,extent=27,flags=0x20000000,backed=True)
            sxrecords.append(dict(ordinal=ordinal,target=st,target_section=ts,disposition='retained-own' if st['index']==12+n*100 else 'omission-claim',expanded_scope_sha256=anchors['expanded_scopes'][root]))
        row['safe_seh_inventory']=dict(section=5000+index,count=count,size=4*count,whole_table_captured=True,relocation_count=0,table_payload_sha256=h(['authored-SafeSEH-table',index]),section_aux=dict(kind='section-definition',length=4*count,relocations=0,selection=0,association=0),records=sxrecords)
        facts={q.CENSUS:dict(field_ids=sorted(f['field_id'] for f in fields),target_indices=sorted(targetmap),complete_physical_scope=True),
            q.FAMILY:dict(owner_root=root,cleanup_extent=11,handler_extent=27,basis='OWN_MATCHED_FIELDS_AND_EXPLICIT_RESOLVERS',handler_field_id='handler',handler_original_target=0x70000000,cookie_field_id='cookie',cookie_original_target=0x71000000,checker_field_id='checker',checker_original_target=0x72000000,cleanup_call_field_id='cleanup-call',cleanup_semantics_receipt_sha256=anchors['cleanup_receipts'][root],info_field_id='info'),
            q.FRAME:dict(owner_root=root,cleanup_extent=11,handler_extent=27,state_transitions=[[0,-1]],catch_count=0,normal_and_unwind_coordinates_distinct=True,frame_preservation_receipt_sha256=anchors['frame_receipts'][root],funcinfo_sha256=h(row['funcinfo']),state_graph_sha256=h(row['state_graph'])),
            q.SOURCE:dict(authority='HISTORICAL_COMPILER_OBJECT_SOURCE_LINEAGE',object_sha256=row['object_sha256'],source_sha256=row['source_context_sha256'],lineage_receipt_sha256=anchors['source_lineage'][str(index)]),
            q.GRAPH:dict(owner_root=root,expanded_scope_sha256=anchors['expanded_scopes'][root],retained_sections=[parent,code,data],whole_SafeSEH_accounted=True,SafeSEH_inventory_sha256=h(row['safe_seh_inventory']),no_unknown_omission_waiver=True)}
        for obligation in q.SINGLE:
            row['evidence'].append(dict(obligation_id=obligation,subject='parent',status='supported',family=q.FAMILIES[obligation],witness_sha256=h([root,obligation]),facts=facts[obligation]))
        for site in sites:
            fact=dict(image_sha256=anchors['image_sha256'],field_id=site['field_id'],section=data,offset=site['offset'],original_site=site['original_site'],original_target=site['original_target'],kind=3,addend=0,highlow_occurrences=1,directory_evidence_sha256=anchors['highlow_directory_sha256'])
            row['evidence'].append(dict(obligation_id=q.HIGHLOW,subject=site['subject'],status='supported',family=q.FAMILIES[q.HIGHLOW],witness_sha256=h([root,site['subject']]),facts=fact))
        bundle['roots'].append(row)
    seal(bundle,anchors);return bundle,anchors

class ClaimAccountingTests(unittest.TestCase):
    def setUp(self):self.b,self.a=valid_case();self.root=next(iter(q.ROOTS));self.row=self.b['roots'][0]
    def run_claim(self):return q.qualify_prospective_parent_eh(self.b,self.root,anchors=self.a)
    def test_authored_consistent_inputs_never_discharge_or_admit(self):
        before=copy.deepcopy((self.b,self.a));out=self.run_claim();self.assertTrue(out['schema_complete']);self.assertTrue(out['authored_claims_consistent']);self.assertEqual(out['discharged'],[]);self.assertEqual(len(out['obligations']),7)
        for name in q.FALSE_FLAGS:self.assertIs(out[name],False)
        self.assertEqual((self.b,self.a),before)
    def test_all_fourteen_site_records_required(self):
        self.b['roots'][6]['metadata_sites'].pop();seal(self.b,self.a)
        with self.assertRaises(q.QualificationError):self.run_claim()
    def test_missing_unknown_false_evidence_stays_distinct(self):
        for status in ('missing','unknown','false'):
            b,a=valid_case();row=b['roots'][0];row['evidence'][0]['status']=status;seal(b,a);out=q.qualify_prospective_parent_eh(b,self.root,anchors=a)
            first=out['obligations'][0];self.assertEqual(first['evidence_status'],status);self.assertFalse(first['discharged']);self.assertFalse(out['authored_claims_consistent'])
        self.row['evidence'].pop(0);seal(self.b,self.a);self.assertEqual(self.run_claim()['obligations'][0]['reason'],'MISSING')
    def test_empty_errors_cannot_hide_false_piece(self):
        self.row['pieces'][0]['MATCH']=False;seal(self.b,self.a);out=self.run_claim();self.assertTrue(out['observed_comparison_false']);self.assertFalse(out['authored_claims_consistent'])
    def test_full_census_rejects_missing_extra_and_wrong_index(self):
        for mutation in ('missing','extra','index'):
            b,a=valid_case();r=b['roots'][0]
            if mutation=='missing':r['physical_fields'].pop()
            elif mutation=='extra':r['physical_fields'].append(dict(r['physical_fields'][0],field_id='hidden',offset=30))
            else:r['physical_fields'][0]['target_index']=999
            seal(b,a)
            with self.assertRaises(q.QualificationError):q.qualify_prospective_parent_eh(b,self.root,anchors=a)
    def test_census_inventory_requires_exact_field_types(self):
        self.row['field_inventory'][0]['comparison_MATCH']=1
        seal(self.b,self.a)
        with self.assertRaises(q.QualificationError):self.run_claim()
    def test_physical_symbol_index_is_uint32(self):
        target=next(t for t in self.row['targets'] if t['name']=='___security_cookie')
        target['index']=0x100000000
        for key in ('field_inventory','physical_fields'):
            for field in self.row[key]:
                if field['target_name']==target['name']:field['target_index']=target['index']
        next(e for e in self.row['evidence'] if e['obligation_id']==q.CENSUS)['facts']['target_indices']=sorted(t['index'] for t in self.row['targets'])
        seal(self.b,self.a)
        with self.assertRaises(q.QualificationError):self.run_claim()
    def test_metadata_section_rejects_bool_even_when_equal_to_one(self):
        data=next(s for s in self.row['owned_sections'] if s['domain']=='data');old=data['section'];data['section']=1
        for target in self.row['targets']:
            if target['section']==old:target['section']=1
        for key in ('field_inventory','physical_fields'):
            for field in self.row[key]:
                if field['section']==old:field['section']=1
        for site in self.row['metadata_sites']:site['section']=True
        for e in self.row['evidence']:
            if e['obligation_id']==q.HIGHLOW:e['facts']['section']=True
            if e['obligation_id']==q.GRAPH:e['facts']['retained_sections']=sorted([self.row['parent']['section']]+[s['section'] for s in self.row['owned_sections']])
        seal(self.b,self.a)
        with self.assertRaises(q.QualificationError):self.run_claim()
    def test_physical_section_index_is_signed_coff_range(self):
        data=next(s for s in self.row['owned_sections'] if s['domain']=='data');old=data['section'];data['section']=0x8000
        for target in self.row['targets']:
            if target['section']==old:target['section']=data['section']
        for key in ('field_inventory','physical_fields'):
            for field in self.row[key]:
                if field['section']==old:field['section']=data['section']
        for site in self.row['metadata_sites']:site['section']=data['section']
        for e in self.row['evidence']:
            if e['obligation_id']==q.HIGHLOW:e['facts']['section']=data['section']
            if e['obligation_id']==q.GRAPH:e['facts']['retained_sections']=sorted([self.row['parent']['section']]+[s['section'] for s in self.row['owned_sections']])
        seal(self.b,self.a)
        with self.assertRaises(q.QualificationError):self.run_claim()
    def test_highlow_type_site_addend_target_and_duplicates(self):
        for key,value in [('kind',10),('original_site',1),('addend',4),('original_target',1),('highlow_occurrences',2),('image_sha256','f'*64)]:
            b,a=valid_case();e=next(e for e in b['roots'][0]['evidence'] if e['obligation_id']==q.HIGHLOW);e['facts'][key]=value;seal(b,a)
            with self.subTest(key=key),self.assertRaises(q.QualificationError):q.qualify_prospective_parent_eh(b,self.root,anchors=a)
    def test_no_eight_byte_cleanup_family_borrowing(self):
        for obligation in (q.FAMILY,q.FRAME):
            b,a=valid_case();e=next(e for e in b['roots'][0]['evidence'] if e['obligation_id']==obligation);e['facts']['cleanup_extent']=8;seal(b,a)
            with self.assertRaises(q.QualificationError):q.qualify_prospective_parent_eh(b,self.root,anchors=a)
    def test_declared_source_hash_is_not_compile_lineage(self):
        e=next(e for e in self.row['evidence'] if e['obligation_id']==q.SOURCE);e['facts']['authority']='DECLARED_OR_CURRENT_HASH_ONLY';seal(self.b,self.a)
        with self.assertRaises(q.QualificationError):self.run_claim()
    def test_same_base_canonical_subtype_conflict_rejected(self):
        self.row['targets'][0]['original_base']=self.row['targets'][1]['original_base'];seal(self.b,self.a)
        with self.assertRaises(q.QualificationError):self.run_claim()
    def test_cookie_cannot_be_crt_code(self):
        t=next(t for t in self.row['targets'] if t['name']=='___security_cookie');t['canonical_role']='crt-contract';seal(self.b,self.a)
        with self.assertRaises(q.QualificationError):self.run_claim()
    def test_foreign_root_stale_anchor_and_parent_association(self):
        with self.assertRaises(q.QualificationError):q.qualify_prospective_parent_eh(self.b,'0x00c50610',anchors=self.a)
        self.row['owned_sections'][0]['parent_section']+=1;seal(self.b,self.a)
        with self.assertRaises(q.QualificationError):self.run_claim()
        b,a=valid_case();a['image_sha256']='f'*64
        with self.assertRaises(q.QualificationError):q.qualify_prospective_parent_eh(b,self.root,anchors=a)
    def test_duplicate_blocker_ids_keep_occurrences_and_order(self):
        self.row['inherited_blockers']=[dict(id='UNKNOWN_AUX',ordinal=i,evidence_sha256=h(['blocker',i])) for i in (9,2)]
        seal(self.b,self.a);out=self.run_claim();self.assertEqual(out['unresolved_obligation_ids'][-2:],['UNKNOWN_AUX','UNKNOWN_AUX']);self.assertEqual([r['occurrence'] for r in out['obligations'][-2:]],[9,2]);self.assertFalse(out['authored_claims_consistent'])
    def test_caller_changed_root_without_expected_anchor_fails(self):
        self.row['EH_errors'].append('authored false diagnostic')
        with self.assertRaises(q.QualificationError):self.run_claim()

    def test_captured_state_and_FuncInfo_cannot_be_missing_or_unknown(self):
        for change in ('state','magic','flags'):
            b,a=valid_case();r=b['roots'][0]
            if change=='state':r['state_graph']=[]
            else:r['funcinfo'][change]=0
            seal(b,a)
            with self.assertRaises(q.QualificationError):q.qualify_prospective_parent_eh(b,self.root,anchors=a)
    def test_noncontiguous_code_target_addend_uses_effective_cut(self):
        for key in ('field_inventory','physical_fields'):
            f=next(x for x in self.row[key] if x['field_id']=='parent-handler')
            f.update(target_index=10,target_name='authored_cleanup_0',addend=11)
        # The handler record remains required by whole SafeSEH even though the
        # parent operand names the cleanup section with a cross-cut addend.
        # A zero-width extra reference would be invalid; use the existing info
        # operand's target record inventory only. This positive is rejected by
        # strict unconsumed-record policy, so retain an explicit native handler
        # reference by adding a separate parent operand in the authored fixture.
        t=next(x for x in self.row['targets'] if x['index']==12)
        f=dict(field_id='authored-direct-handler',owner_root=self.root,section=self.row['parent']['section'],offset=40,kind='DIR32',target_index=12,target_name=t['name'],addend=0,original_site=int(self.root,16)+40,original_target=t['original_base'],comparison_MATCH=True)
        self.row['physical_fields'].append(f);self.row['field_inventory'].append(copy.deepcopy(f))
        e=next(x for x in self.row['evidence'] if x['obligation_id']==q.CENSUS);e['facts']['field_ids']=sorted(x['field_id'] for x in self.row['physical_fields'])
        seal(self.b,self.a);self.assertTrue(self.run_claim()['authored_claims_consistent'])
    def test_whole_safe_seh_inventory_required(self):
        self.row.pop('safe_seh_inventory');seal(self.b,self.a)
        with self.assertRaises(q.QualificationError):self.run_claim()
    def test_unknown_foreign_safe_seh_occurrence_is_preserved(self):
        record=next(x for x in self.row['safe_seh_inventory']['records'] if x['disposition']=='omission-claim')
        record['disposition']='unresolved-other'
        e=next(x for x in self.row['evidence'] if x['obligation_id']==q.GRAPH);e['facts']['SafeSEH_inventory_sha256']=h(self.row['safe_seh_inventory'])
        seal(self.b,self.a);out=self.run_claim();self.assertFalse(out['authored_claims_consistent'])
        self.assertEqual(out['obligations'][-1]['reason'],'UNRESOLVED_SAFESEH_RETENTION');self.assertEqual(out['obligations'][-1]['occurrence'],record['ordinal'])

if __name__=='__main__':unittest.main()
