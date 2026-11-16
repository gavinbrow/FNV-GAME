"""Authored COMDAT observer evidence and complete synthetic epoch fixtures."""
import copy
from pathlib import Path
import sys
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import comdat_any_frontier_factory as factory
from test_comdat_any_frontier_observer import fixture as original_fixture,rebind


def evidence_fixture():
    evidence=[];candidates=[];original=[]
    for i in range(2):
        raw,row,candidate=original_fixture(partial=i==1)
        if i:
            r=candidate['root'];r['original_address']='0x01002000';r['recipe_id']='authored-blocked';r['recipe_index']=1
            k=row['contract'];k['recipe_id']=r['recipe_id'];k['roots'][0]['original_address']=r['original_address']
            k['unit_verified_functions'][0]['address']=r['original_address'];k['provenance'].update(recipe_id=r['recipe_id'],recipe_index=1)
            row['recipe_id']=r['recipe_id'];row['certificate']=factory.base.ordinary.assess_object(factory.base.coff.parse(raw),k)
            row['blockers']=row['certificate']['blockers'];candidate['summary'].update(recipe_id=r['recipe_id'],roots=[r['original_address']])
            rebind(row,candidate)
        e=factory.observer.observe_member(raw,row,candidate);evidence.append(e);candidates.append(candidate);original.append((raw,row,candidate))
    receipt=dict(policy_id=factory.observer.POLICY,status='metadata-only',input_stability=True,optional_function_index_present=False,
        emitted=0,roots=2,observed_addresses=sorted(c['root']['original_address'] for c in candidates),composed_complete=1,
        unsupported=1,blocked=1,**factory.observer.FALSE)
    request=dict(roots=[c['root'] for c in candidates],candidates=candidates)
    return receipt,evidence,request,original


def match_row(root,name):
    return [dict(address=root['original_address'],symbol=name,size=root['size'],compiled_extent=root['size'],
        verdict='match',errors=[],relocations=[])]


def cohort_fixture():
    records=[]
    for i in range(14409):
        identity=dict(recipe_id='authored-parent-%d'%i,object_sha256='a'*64,symbol_index=i)
        records.append(dict(canonical=factory.base.pool.canonical(identity),namespace_identity=identity,
            category='ordinary' if i<14403 else 'application-candidate',authored_marker=dict(index=i)))
    parent=dict(kind='prepared-CODE-collision-exclusions',policy_id=factory.observer.selector.FRONTIER_POLICY,
        ordinary_prepared_count=14403,collision_exclusion_count=14409,records=records,
        exclusion_names=sorted(r['canonical'] for r in records),ordinary_names=sorted(r['canonical'] for r in records if r['category']=='ordinary'),
        application_selection_inferred_from_counts=False,provider_selected=False,runtime_eligible=False,application_manifest_adopted=False)
    members=[];providers={};units={}
    for i in range(68):
        a='0x%08x'%(0x03000000+i*32);rid='authored-cohort-%d'%i
        r=dict(original_address=a,recipe_id=rid,recipe_index=i,symbol='_authored%d'%i,symbol_index=31+i,
            section=1,value=0,size=16,object_sha256='%064x'%(i+1),source_sha256='%064x'%(i+500))
        identity={k:r[k] for k in ('recipe_id','object_sha256','symbol_index')};name=factory.base.pool.canonical(identity)
        providers[a]=dict({k:r[k] for k in ('recipe_id','object_sha256','source_sha256','symbol','symbol_index','section','value','size')},
            planned_canonical_name=name)
        units[rid]=dict(recipe_index=i,object_sha256=r['object_sha256'],source_sha256=r['source_sha256'])
        p=dict(policy_id=factory.base.POLICY,requested_roots=[r],exports=[name],original_object_sha256=r['object_sha256'],
            output_sha256='%064x'%(i+900),maps=dict(symbol_map={str(r['symbol_index']):0},section_map={'1':1}),
            before_comparison=match_row(r,r['symbol']),after_comparison=match_row(r,name))
        members.append(dict(name='authored-%d.obj'%i,projection=p))
    return parent,members,providers,units,'f'*64


class FactoryPureTests(unittest.TestCase):
    def test_cli_help_initializes_in_fresh_process(self):
        result=subprocess.run([sys.executable,str(ROOT/'tools/rebuild/comdat_any_frontier_factory.py'),'--help'],
            text=True,capture_output=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr);self.assertIn('--operation-sha256',result.stdout)

    def test_fresh_original_and_serialized_plain_comparisons_preserve_any_auxiliary(self):
        receipt,rows,request,original=evidence_fixture();raw,row,candidate=original[0];root=candidate['root']
        payload=factory.base.coff.parse(raw)['sections'][root['section']]['payload']
        pe=SimpleNamespace(read=lambda address,size:payload if (address,size)==(int(root['original_address'],16),root['size']) else b'')
        sys.path.insert(0,str(ROOT/'tools'))
        with tempfile.TemporaryDirectory() as directory:
            before=Path(directory)/'authored-before.obj';after=Path(directory)/'authored-after.obj';before.write_bytes(raw)
            output,projection,assessment=factory.verify_member(raw,row,candidate,rows[0],
                {root['original_address']:factory.observer.selector.root_identity(root)},[],before,after,pe,{})
            self.assertTrue(assessment['eligible']);self.assertTrue(projection['selection2_auxiliary_preserved'])
            self.assertEqual([p['verdict'] for p in projection['before_comparison']+projection['after_comparison']],['match','match'])
            proof=factory.field_proof_record(after.name,row,candidate,rows[0],projection,output)
            self.assertFalse(proof['original_base_closure_observed']);self.assertEqual(proof['fields'],[])

    def test_entire_eligible_set_and_blocked_ledger_preserved(self):
        receipt,rows,request,_=evidence_fixture();before=copy.deepcopy((receipt,rows,request))
        selected,ledger=factory.select_eligible(receipt,rows,request)
        self.assertEqual(len(selected),1);self.assertEqual(len(ledger),2);self.assertTrue(ledger[0]['selected'])
        self.assertFalse(ledger[1]['selected']);self.assertEqual((receipt,rows,request),before)

    def test_subset_or_counter_forgery_is_not_whole_observer_outcome(self):
        receipt,rows,request,_=evidence_fixture()
        with self.assertRaises(ValueError):factory.select_eligible(receipt,rows[:1],request)
        receipt['composed_complete']=True
        with self.assertRaises(ValueError):factory.select_eligible(receipt,rows,request)

    def test_epoch_appends_all68_and_preserves_every_parent_record(self):
        args=cohort_fixture();before=copy.deepcopy(args);result=factory.rebuild_latest_exclusions(*args)
        self.assertEqual(result['ordinary_prepared_count'],14471);self.assertEqual(result['collision_exclusion_count'],14477)
        old={r['canonical']:r for r in args[0]['records']};new={r['canonical']:r for r in result['records']}
        self.assertEqual({k:new[k] for k in old},old);self.assertEqual(args,before)

    def test_epoch_rejects_native_map_or_source_member_identity_conflicts(self):
        for mode in ('map','source','provider','duplicate'):
            args=cohort_fixture();p=args[1][0]['projection'];r=p['requested_roots'][0]
            if mode=='map':p['maps']['symbol_map'][str(r['symbol_index'])]=False
            elif mode=='source':r['source_sha256']='0'*64
            elif mode=='provider':args[2][r['original_address']]['planned_canonical_name']='wrong'
            else:args[1][1]=copy.deepcopy(args[1][0])
            with self.subTest(mode=mode),self.assertRaises(ValueError):factory.rebuild_latest_exclusions(*args)


if __name__=='__main__':unittest.main()
