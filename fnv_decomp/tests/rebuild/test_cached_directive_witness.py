"""Authored fixtures only: no saved objects, native input or frozen-global patches."""
import copy
import hashlib
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_directive_witness as m
from test_uuid_directive_occurrence_witness import fixture,repin


def authored(address='0x0045b020'):
    root,contract,negative,raw,header,binding,authority=fixture(address)
    binding['path']=r'C:\SDK\Lib\uuid.lib'
    args=[root,contract,negative,raw,header,binding,authority];repin(args)
    declaration=dict(kind='explicit-normal-sdk-library-dependency-v1',library_name='uuid.lib',
        absolute_path=binding['path'],sha256=binding['sha256'],required_response_token=binding['path'])
    review=dict(kind='independent-normal-dependency-declaration-review-v1',status='accepted',
        declaration_sha256=m.witness.digest(declaration),reviewer='independent-fixture')
    auth=dict(declaration_sha256=m.witness.digest(declaration),review_sha256=m.witness.digest(review))
    return args+[declaration,review,auth]


def fake_proposal(root,contract,negative,raw,header,binding,authority):
    spans=[];pos=0
    for i,token in enumerate(m.witness.TOKENS,1):
        start=raw.index(token.encode('ascii'),pos);end=start+len(token)
        spans.append(dict(ordinal=i,start=start,end=end,token=token));pos=end
    occ=[]
    for i,(b,ids) in enumerate(zip(negative['blockers'],([1],[2],[1,2,3,4])),1):
        occ.append(dict(ordinal=i,blocker_id=b['blocker_id'],blocker_sha256=m.witness.digest(b),
                        blocker=copy.deepcopy(b),directive_ordinals=ids))
    return dict(schema_version=1,kind='typed-uuid-directive-occurrence-discharge-proposal',
       policy_id=m.witness.POLICY,caller_authority_authentication_required=True,root=copy.deepcopy(root),
       contract_sha256=m.witness.digest(contract),original_negative=copy.deepcopy(negative),
       original_negative_sha256=m.witness.digest(negative),original_negative_unchanged=True,
       raw_section_hex=raw.hex(),raw_section_sha256=hashlib.sha256(raw).hexdigest(),header=copy.deepcopy(header),
       binding=copy.deepcopy(binding),authority=copy.deepcopy(authority),
       proposed_blocker_occurrences=occ,directive_occurrences=spans,**{k:False for k in m.FALSE_FLAGS})


def call(args,proposal_fn=fake_proposal):
    return m._qualify_core(*args,proposal_fn=proposal_fn,declaration_fn=m.composer.validate_declaration)


class CandidateTests(unittest.TestCase):
    def test_both_authored_fixture_roots_preserve_order_and_negative(self):
        for address in ('0x0045b020','0x00c5d4e0'):
            args=authored(address);before=copy.deepcopy(args);out=call(args)
            self.assertEqual(args,before);self.assertEqual(out['original_negative'],args[2])
            self.assertEqual(out['required_future_response_token'],args[7]['absolute_path'])
            self.assertEqual([x['ordinal'] for x in out['proposal']['proposed_blocker_occurrences']],[1,2,3])
            self.assertEqual([x['directive_ordinals'] for x in out['proposal']['proposed_blocker_occurrences']],[[1],[2],[1,2,3,4]])
            self.assertEqual(bytes.fromhex(out['proposal']['raw_section_hex']),args[3])
            for k in m.FALSE_FLAGS:self.assertIs(out[k],False)
            self.assertFalse(out['ordinary_graph_closure']);self.assertFalse(out['composition_proved'])
            self.assertFalse(out['SDK_identity_freshly_observed']);self.assertFalse(out['response_token_observed'])

    def test_unqualified_public_wrapper_rejects_authored_certificate(self):
        for addr in ('0x0045b020','0x00c5d4e0'):
            with self.assertRaises(ValueError):m.qualify(*authored(addr))
        with self.assertRaises(TypeError):m.qualify(*authored(),proposal_fn=fake_proposal)

    def test_unknown_root_and_identity_drift_rejected(self):
        for mutate in (lambda a:a[0].update(original_address='0x00000001'),
                       lambda a:a[0].update(recipe_id='changed'),lambda a:a[0].update(symbol_index=True),lambda a:a[0].update(value=False)):
            args=authored();mutate(args)
            with self.assertRaises((ValueError,KeyError)):call(args)

    def test_order_multiplicity_and_unparsed_bytes_rejected(self):
        for mutate in (lambda a:a[2]['blockers'].pop(1),lambda a:a[2]['blockers'].append(copy.deepcopy(a[2]['blockers'][0])),
                       lambda a:a[2]['blockers'].reverse(),lambda a:a.__setitem__(3,a[3]+b'/FORCE')):
            args=authored();mutate(args)
            with self.assertRaises((ValueError,IndexError)):call(args)

    def test_non_uuid_directives_and_original_negative_changes_fail(self):
        for directive in (b'/INCLUDE:x',b'/NODEFAULTLIB',b'/FORCE',b'/ALTERNATENAME:a=b'):
            args=authored();args[3]=(directive+b' '+args[3])[:93]
            with self.assertRaises((ValueError,IndexError)):call(args)
        for flag in ('closure_observed','graph_observation_complete','root_closure_candidate'):
            args=authored();args[2][flag]=True
            with self.assertRaises(ValueError):call(args)

    def test_unreviewed_declaration_or_physical_origin_cannot_be_substituted(self):
        for changed in (r'\sdk\uuid.lib',r'C:\OtherSDK\uuid.lib'):
            args=authored();args[5]['path']=changed
            with self.assertRaises(ValueError):call(args)

    def test_review_and_exact_full_path_dependency_required(self):
        for mutate in (lambda a:a[8].update(status='pending'),lambda a:a[7].update(required_response_token='uuid.lib'),
                       lambda a:a[5].update(path=r'C:\OtherSDK\uuid.lib'),lambda a:a[9].update(review_sha256='0'*64)):
            args=authored();mutate(args)
            with self.assertRaises(ValueError):call(args)

    def test_mutated_proposal_flags_or_occurrence_rejected(self):
        for mutate in (lambda p:p.update(provider_selected=True),
                       lambda p:p['proposed_blocker_occurrences'][1].update(ordinal=1),
                       lambda p:p['proposed_blocker_occurrences'][0].update(directive_ordinals=[2]),
                       lambda p:p['proposed_blocker_occurrences'][0].update(directive_ordinals=[True]),
                       lambda p:p['proposed_blocker_occurrences'][2].update(directive_ordinals=[True,2,3,4]),
                       lambda p:p.update(schema_version=True),lambda p:p.update(ordinary_graph_closure=True),
                       lambda p:p.update(caller_authority_authentication_required=False),
                       lambda p:p.update(policy_id='other')):
            def bad(*args):
                out=fake_proposal(*args);mutate(out);return out
            with self.assertRaises(ValueError):call(authored(),bad)

if __name__=='__main__':unittest.main()
