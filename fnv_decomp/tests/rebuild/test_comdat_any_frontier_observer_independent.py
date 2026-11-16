"""Independent authored observer/reader tests; no original game inputs.

Operational harness replaces ONLY production acceptance/selector gates with an
authored one-root context. Native/row proof, gzip reader and publisher run real.
This harness cannot authenticate or authorize production inputs.
"""
from pathlib import Path
from argparse import Namespace
from contextlib import ExitStack
import copy
import gzip
import hashlib
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import comdat_any_frontier_observer as observer
from test_comdat_any_frontier_observer import fixture,rebind


class IndependentSelectedRowTests(unittest.TestCase):
    def test_actual_typed_negative_and_native_candidate_replay_unchanged(self):
        raw,row,candidate=fixture();before=copy.deepcopy((row,candidate));result=observer.observe_member(raw,row,candidate)
        self.assertEqual((row,candidate),before);self.assertFalse(result['original_negative_certificate']['closure_observed'])
        self.assertTrue(result['composed']['composed_omission_complete']);self.assertFalse(result['serialization_performed'])
        for key in observer.FALSE:self.assertIs(result[key],False)

    def test_native_partial_is_no_policy_with_every_original_occurrence(self):
        raw,row,candidate=fixture(partial=True);result=observer.observe_member(raw,row,candidate)
        self.assertIsNone(result['composed']);self.assertEqual(result['witnesses'],[])
        ids=[b['blocker_id'] for b in row['certificate']['blockers']]
        self.assertEqual(result['unsupported_summary']['original_blocker_ids'],ids)
        self.assertEqual(result['unsupported_summary']['remaining_blocker_ids'],ids)

    def test_record_extension_promotion_and_numeric_type_alias_refused(self):
        for mode in ('extra','schema_bool','false_zero','candidate_bool','graph_bool'):
            raw,row,candidate=fixture()
            if mode=='extra':row['borrowed_authority']=True
            elif mode=='schema_bool':row['schema_version']=True
            elif mode=='false_zero':row['provider_selected']=0
            elif mode=='candidate_bool':row['root_closure_candidate']=0
            else:row['graph_observation_complete']=0
            rebind(row,candidate)
            with self.subTest(mode=mode),self.assertRaises(ValueError):observer.validate_selected_row(row,candidate)

    def test_borrowed_request_source_scope_and_negative_state_refused(self):
        for mode in ('request','scope','source','root','negative'):
            raw,row,candidate=fixture()
            if mode=='request':row['contract']['provenance']['request_sha256']='9'*64
            elif mode=='scope':row['contract']['provenance']['scope_mode']='recipe-union'
            elif mode=='source':candidate['root']['source_sha256']='9'*64
            elif mode=='root':candidate['root']['recipe_index']=False
            else:row['closure_observed']=True
            rebind(row,candidate)
            with self.subTest(mode=mode),self.assertRaises(ValueError):observer.observe_member(raw,row,candidate)


class IndependentReaderTests(unittest.TestCase):
    def use(self,lines,count,wanted,check=lambda:None):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'authored.gz'
            with gzip.open(path,'wb') as f:
                for line in lines:f.write(line)
            return list(observer.read_selected_rows(path,count,wanted,check))

    def test_only_selected_JSON_is_parsed_and_all_lines_checked(self):
        _,row,candidate=fixture();calls=[]
        result=self.use([observer.selector.canonical(row)+b'\n',b'not JSON\xff\n'],2,{1:candidate},lambda:calls.append(1))
        self.assertEqual(result,[(candidate,row)]);self.assertEqual(len(calls),2)

    def test_short_extra_or_nonterminated_extent_cannot_complete(self):
        _,row,candidate=fixture();line=observer.selector.canonical(row)
        for lines,count in [([line+b'\n'],2),([line+b'\n',b'ignored\n'],1),([line],1)]:
            with self.subTest(count=count),self.assertRaises(ValueError):self.use(lines,count,{1:candidate})

    def test_independent_line_and_expansion_limits_are_enforced(self):
        _,row,candidate=fixture();line=observer.selector.canonical(row)+b'\n'
        with patch.object(observer,'MAX_ROW',len(line)-1):
            with self.assertRaises(ValueError):self.use([line],1,{1:candidate})
        with patch.object(observer,'MAX_DETAILS',len(line)-1):
            with self.assertRaises(ValueError):self.use([line],1,{1:candidate})

    def test_wrong_locator_and_selected_malformed_JSON_fail(self):
        _,row,candidate=fixture();candidate['authority']['ordinal']=2;candidate['summary']['ordinal']=2
        with self.assertRaises(ValueError):self.use([observer.selector.canonical(row)+b'\n'],1,{1:candidate})
        _,row,candidate=fixture()
        with self.assertRaises(ValueError):self.use([b'bad selected JSON\n'],1,{1:candidate})


class IndependentAuthoredOperationTests(unittest.TestCase):
    def setup_context(self,workspace):
        root=Path(workspace);private=root/'build/rebuild';private.mkdir(parents=True)
        area=private/'authored';area.mkdir();source=root/'src/authored.cpp';source.parent.mkdir();source.write_text('// authored fixture only\n')
        raw,row,candidate=fixture();source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
        candidate['root']['source_sha256']=source_hash;row['contract']['provenance']['source_sha256']=source_hash
        def save(name,value):
            p=area/name;p.write_text(json.dumps(value,sort_keys=True)+'\n');return dict(path=str(p),sha256=observer.base.file_hash(p))
        original_request=save('original-request.json',dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=[candidate['root']]))
        row['contract']['provenance']['request_sha256']=original_request['sha256'];candidate['authority']['request_sha256']=original_request['sha256']
        row['certificate']=observer.base.ordinary.assess_object(observer.base.coff.parse(raw),row['contract'])
        row['blockers']=row['certificate']['blockers'];rebind(row,candidate)
        details=area/'details.gz'
        with gzip.open(details,'wb') as f:f.write(observer.selector.canonical(row)+b'\n')
        detail_hash=observer.base.file_hash(details);candidate['authority']['details_sha256']=detail_hash
        receipt=save('original-receipt.json',dict(policy_id='new-frontier-ordinary-root-observation-v3',status='metadata-only',
            input_stability=True,optional_function_index_present=False,request_sha256=original_request['sha256'],
            observations=[candidate['summary']],details_sha256=detail_hash,**observer.base.collector.FALSE))
        candidate['authority']['receipt_sha256']=receipt['sha256']
        source_spec=dict(kind='new-frontier-v3',receipt=receipt,request=original_request,
            details=[dict(lane=None,path=str(details),sha256=detail_hash)])
        obj=area/'authored.obj';obj.write_bytes(raw);r=candidate['root'];p=row['contract']['provenance']
        manifest=save('manifest.json',dict(units=[dict(recipe_id=r['recipe_id'],source='src/authored.cpp',object='authored.obj')]))
        retained=save('retained.json',dict(units=[dict(recipe_id=r['recipe_id'],verified_functions=row['contract']['unit_verified_functions'],
            recipe_unit_sha256=p['recipe_unit_sha256'])],inputs=dict(tools_sha256={})))
        request=save('request.json',dict(roots=[r],candidates=[candidate]));context=save('context.json',dict(epoch='authored',request_sha256=request['sha256'],
            artifacts=dict(manifest=manifest,retained=retained,selection=save('selection.json',dict(selections={})),recipes=save('recipes.json',{})),acceptances={}))
        args=Namespace(request=Path(request['path']),request_sha256=request['sha256'],context=Path(context['path']),context_sha256=context['sha256'],
            review=area/'authored-review.json',review_sha256='0'*64,out=private/'output')
        key=tuple(candidate['authority'][k] for k in ('kind','receipt_sha256','request_sha256'))
        return root,args,{key:source_spec}

    def run_authored(self,root,args,sources,*,tamper=False):
        # Production authorization and complete actual selector are deliberately
        # NOT exercised or fabricated by this one-root operational unit harness.
        with ExitStack() as stack:
            stack.enter_context(patch.object(observer,'ROOT',root));stack.enter_context(patch.object(observer.base,'ROOT',root))
            stack.enter_context(patch.object(observer,'OWNED',()));stack.enter_context(patch.object(observer,'PINS',{}))
            stack.enter_context(patch.object(observer,'review_gate',return_value={}))
            stack.enter_context(patch.object(observer,'validate_request_context',return_value=sources))
            stack.enter_context(patch.object(observer.base,'reconcile_recipes',return_value=dict(verified=True)))
            stack.enter_context(patch.object(observer.base.collector,'validate_request',return_value=None))
            if tamper:
                publish=observer.base.finalize_success
                def drift(out,result,inputs,start,journal,note):
                    (out/'observations.jsonl.gz').write_bytes(b'authored drift');return publish(out,result,inputs,start,journal,note)
                stack.enter_context(patch.object(observer.base,'finalize_success',side_effect=drift))
            return observer.run(args)

    def test_first_row_journal_and_real_frozen_publication_complete(self):
        with tempfile.TemporaryDirectory() as td:
            root,args,sources=self.setup_context(td);result=self.run_authored(root,args,sources)
            self.assertEqual((result['roots'],result['composed_complete'],result['emitted']),(1,1,0))
            self.assertTrue((args.out/'receipt.json').exists());self.assertFalse((args.out/'abort.json').exists())
            events=[json.loads(line) for line in (args.out/'journal.jsonl').read_text().splitlines()]
            self.assertIn('observed_original_negative',[r['state'] for r in events])
            self.assertTrue(any('native_state' in r for r in events));self.assertTrue(all(result[k] is False for k in observer.FALSE))

    def test_protected_evidence_drift_cannot_leave_successful_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            root,args,sources=self.setup_context(td)
            with self.assertRaises(ValueError):self.run_authored(root,args,sources,tamper=True)
            self.assertFalse((args.out/'receipt.json').exists());self.assertTrue((args.out/'abort.json').exists())


if __name__=='__main__':unittest.main()
