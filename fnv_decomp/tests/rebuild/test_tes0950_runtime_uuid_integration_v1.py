import copy
import hashlib
from pathlib import Path
import sys
import unittest
from unittest import mock

sys.path.insert(0,str(Path(__file__).resolve().parent))
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
from test_coff_code_archive import section, symbol, aux, object_bytes
import coff_code_archive as coff
import runtime_code_pool as pool
import tes0950_runtime_uuid_integration_v1 as prod


class Tes0950RuntimeIntegration(unittest.TestCase):
    def setUp(self):
        self.raw=b'authored-only-input'
        self.root=copy.deepcopy(prod.ROOT);self.root['object_sha256']=hashlib.sha256(self.raw).hexdigest()
        self.export=pool.canonical({k:self.root[k] for k in ('recipe_id','object_sha256','symbol_index')})
        self.contract={'verified_match':True,'fields_complete':True,'missing_fields_complete':True,
            'missing_fields':[],'parent_eh':[], 'fields':[
                {'coff_relocation':{'offset':offset,'kind':20,'addend':0},
                 'exact_original_target_va':address,'classification':'SELECTED_CODE_ENTRY',
                 'proof_consistency':'EXACT_OWN_SOURCE_RESOLUTION'}
                for offset,address in zip(prod.OFFSETS,prod.TARGET_ORDER)]}
        self.negative={'closure_observed':False,'root_closure_candidate':False}
        self.providers={prod.ADDRESS:{k:self.root[k] for k in ('recipe_id','object_sha256','symbol_index')}}
        for address,(recipe,obj,index) in prod.TARGETS.items():
            self.providers[address]={'recipe_id':recipe,'object_sha256':obj,'symbol_index':index}
        self.witnesses=[{'header':{},'binding':{},'witness_authority':{},'declaration':{},'review':{},'declaration_authority':{}}]
        self.patches=mock.patch.multiple(prod,ROOT=self.root,EXPORT=self.export,
            CONTRACT_SHA=prod.witness.digest(self.contract),NEGATIVE_SHA=prod.witness.digest(self.negative))
        self.patches.start();self.addCleanup(self.patches.stop)

    def validate(self):
        return prod.validate_saved_inputs(self.raw,self.contract,self.negative,self.witnesses,self.providers,[])

    def test_exact_scope_and_provider_identity(self):
        self.assertTrue(self.validate())
        bad=copy.deepcopy(self.providers);bad[prod.TARGET_ORDER[0]]['symbol_index']+=1
        with self.assertRaisesRegex(ValueError,'target physical owner'):
            prod.validate_saved_inputs(self.raw,self.contract,self.negative,self.witnesses,bad,[])
        with self.assertRaisesRegex(ValueError,'collision'):
            prod.validate_saved_inputs(self.raw,self.contract,self.negative,self.witnesses,self.providers,[self.export])
        with self.assertRaisesRegex(ValueError,'identity'):
            prod.validate_saved_inputs(self.raw+b'x',self.contract,self.negative,self.witnesses,self.providers,[])

    def test_repinning_a_changed_field_still_rejected(self):
        changed=copy.deepcopy(self.contract);changed['fields'][2]['coff_relocation']['addend']=1
        with mock.patch.object(prod,'CONTRACT_SHA',prod.witness.digest(changed)):
            with self.assertRaisesRegex(ValueError,'field bindings'):
                prod.validate_saved_inputs(self.raw,changed,self.negative,self.witnesses,self.providers,[])

    def test_authored_wrapped_producers_preserve_directives_and_archive(self):
        directive=b' /DEFAULTLIB:"uuid.lib" /DEFAULTLIB:"uuid.lib" /DEFAULTLIB:"LIBCMT" /DEFAULTLIB:"OLDNAMES" '
        projected=object_bytes([section('.drectve',directive,flags=0x00100a00),section('.text',b'code')],
            [symbol('.drectve',1,storage=3,auxiliary=aux(len(directive),selection=0)),
             symbol('.text',2,storage=3,auxiliary=aux(4)),symbol(self.export,2,typ=32)])
        directive_sha=hashlib.sha256(directive).hexdigest()
        composition={'original_negative_unchanged':True,'base_certificate_sha256':prod.NEGATIVE_SHA,
                     'proposal':{'raw_section_sha256':directive_sha},'discharged_blocker_occurrences':[{}, {}, {}]}
        proof={'exports':[self.export],'fields':[{} for _ in range(6)],'original_negative_certificate_preserved':True}
        with mock.patch.object(prod,'DIRECTIVE_SHA',directive_sha), \
             mock.patch.object(prod.composer,'compose',return_value=composition) as cm, \
             mock.patch.object(prod.projection,'project_member',return_value=(projected,proof)) as pm:
            archive,receipt=prod.produce(self.raw,self.contract,self.negative,self.witnesses,self.providers,existing_exports=[])
        self.assertEqual(coff.read_archive(archive)['index'],[(self.export,'tes0950.obj')])
        self.assertEqual(receipt['duplicate_uuid_occurrences'],2)
        self.assertFalse(receipt['target_providers_selected']);self.assertFalse(receipt['original_byte_match_claimed'])
        self.assertEqual(cm.call_count,1);self.assertEqual(pm.call_count,1)

    def test_mocked_projection_cannot_promote_provider(self):
        composition={'original_negative_unchanged':True,'base_certificate_sha256':prod.NEGATIVE_SHA,
                     'proposal':{'raw_section_sha256':prod.DIRECTIVE_SHA},'discharged_blocker_occurrences':[{}, {}, {}],
                     'provider_selected':True}
        with mock.patch.object(prod.composer,'compose',return_value=composition):
            with self.assertRaisesRegex(ValueError,'composition'):
                prod.produce(self.raw,self.contract,self.negative,self.witnesses,self.providers,existing_exports=[])

if __name__=='__main__': unittest.main()
