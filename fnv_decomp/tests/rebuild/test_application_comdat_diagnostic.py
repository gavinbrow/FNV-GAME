"""Authored response and typed native receipt policy; no private input reads."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/rebuild'))
import application_comdat_diagnostic as subject


class ResponseTests(unittest.TestCase):
    def test_canonical_alias_equality_preserves_all_identity_use_and_proof_values(self):
        fresh=[dict(canonical='authored%d'%i,positive_import_identity=('AUTHORED.dll','name','Api%d'%i),
            use_count=8 if i==0 else 7,enabled=True,complete_actual_uses=[dict(proof=dict(original_base='authored'))]) for i in range(34)]
        saved=json.loads(json.dumps(fresh));before=copy.deepcopy(fresh)
        self.assertIsNone(subject.unchanged_aliases(fresh,saved));self.assertEqual(fresh,before)
        for key,value in [('positive_import_identity',['AUTHORED.dll','name','Other']),('use_count',9),
            ('complete_actual_uses',[dict(proof=dict(original_base='changed'))]),('enabled',False),('canonical','other')]:
            altered=copy.deepcopy(saved);altered[0][key]=value
            with self.assertRaises(ValueError):subject.unchanged_aliases(fresh,altered)

    def test_equal_dependency_overlaps_are_merged_and_conflicts_rejected(self):
        self.assertEqual(subject.source_pins({'source':'same'},{'source':'same','other':'new'}),{'source':'same','other':'new'})
        with self.assertRaises(ValueError):subject.source_pins({'source':'old'},{'source':'changed'})
        subject.source_pins(subject.diagnostic.SOURCE_PINS,subject.HELPER_PINS,subject.PINS)

    def fixture(self):
        old=Path('authored-old');out=Path('authored-new');archive=Path('authored.lib')
        IAT=['/ALTERNATENAME:iat%d=native%d'%(i,i) for i in range(34)]
        CRT=['/ALTERNATENAME:crt%d=normal%d'%(i,i) for i in range(4)]
        tokens=['/OUT:'+str(old/'diagnostic.exe'),'/MAP:'+str(old/'diagnostic.map'),'/MACHINE:X86']+IAT+CRT
        text='\n'.join('"'+t+'"' for t in tokens)+'\n'
        return text,old,out,archive,IAT,CRT

    def test_single_addition_changes_only_two_destinations(self):
        args=self.fixture();before=args[0].splitlines();result=subject.response_tokens(*args)
        self.assertEqual(result[-1],str(args[3]));self.assertEqual(result[2:-1],[s[1:-1] for s in before[2:]])
        self.assertEqual(result[:2],['/OUT:'+str(args[2]/'diagnostic.exe'),'/MAP:'+str(args[2]/'diagnostic.map')])

    def test_preexisting_archive_or_missing_prior_alias_rejected(self):
        args=list(self.fixture());args[0]+='"'+str(args[3])+'"\n'
        with self.assertRaises(ValueError):subject.response_tokens(*args)
        args=list(self.fixture());args[0]=args[0].replace('"'+args[4][0]+'"\n','')
        with self.assertRaises(ValueError):subject.response_tokens(*args)

    def test_unreviewed_alias_or_force_rejected(self):
        for token in ['/ALTERNATENAME:new=unreviewed','/FORCE:UNRESOLVED']:
            args=list(self.fixture());args[0]+='"'+token+'"\n'
            with self.assertRaises(ValueError):subject.response_tokens(*args)


def native_fixture():
    flags={k:False for k in ('ABI_verified','Game_execution','archive_generated','compiler_performed','executable_linked','object_rewritten','provider_selected','runtime_eligible')}
    native=dict(kind='comdat-any-native-conformance-v1',schema_version=1,status='pass',input_stability_verified=True,collection_sha256='collection',
        components=[dict(label='comdat-any-code1',kind='archive',input_sha256='archive',receipt_sha256='producer',native_metadata_matches=True,
            facts=dict(members=1,exports=1,complete_native_linker_index=True,objects=[dict(all_native_metadata_matches=True)]))],**flags)
    peer=dict(kind='comdat-any-native-independent-review-v1',schema_version=1,status='accepted',receipt_sha256='receipt',archive_sha256='archive',collection_sha256='collection',
        native_commands_replayed=0,
        **{k:False for k in ('ABI_verified','game_execution','link_performed','provider_selected','runtime_eligible')})
    return native,peer,'archive','producer','receipt'


class NativeScopeTests(unittest.TestCase):
    def test_exact_successful_singleton(self):
        self.assertIsNone(subject.native_scope(*native_fixture()))

    def test_replay_count_is_integer_zero_not_boolean(self):
        for value in (False,True,1,'0'):
            args=list(native_fixture());args[1]['native_commands_replayed']=value
            with self.assertRaises(ValueError):subject.native_scope(*args)

    def test_failed_stale_or_unrelated_outcome_rejected(self):
        for target,key,value in [(0,'status','failed'),(0,'input_stability_verified',False),(1,'receipt_sha256','unrelated'),(1,'archive_sha256','old')]:
            args=list(native_fixture());args[target][key]=value
            with self.assertRaises(ValueError):subject.native_scope(*args)

    def test_extra_component_or_runtime_promotion_rejected(self):
        args=list(native_fixture());args[0]['components']*=2
        with self.assertRaises(ValueError):subject.native_scope(*args)
        args=list(native_fixture());args[1]['runtime_eligible']=True
        with self.assertRaises(ValueError):subject.native_scope(*args)


if __name__=='__main__':unittest.main()
