"""Synthetic response tokens only, never invokes LINK."""
import copy,hashlib,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_response_successor_v2 as v


def fixture():
    old=r'C:\old';new=r'C:\new';sdk=copy.deepcopy(v.uuid.EXPECTED_SDK)
    alias='/ALTERNATENAME:_old=_new'
    tokens=['/OUT:'+old+r'\diagnostic.exe','/MAP:'+old+r'\diagnostic.map',r'C:\work\existing.lib',sdk['path'],alias]
    data=v.diagnostic.response_text(tokens).encode('utf8')
    kwargs=dict(old_out=old,new_out=new,new_archive=r'C:\work\candidate.lib',inherited_aliases=[alias],
                current_aliases=[alias],fresh_uuid_identity=sdk,
                qualified_uuid=dict(policy_id=v.uuid.POLICY,kind='qualified-uuid2768-consumer-evidence-v1',
                  future_uuid_response_token=sdk['path'],dependency_identity=copy.deepcopy(sdk)))
    return data,kwargs


def run(data,kwargs):
    with patch.object(v,'V14_RESPONSE_SHA256',hashlib.sha256(data).hexdigest()): return v.transform(data,**kwargs)

class Tests(unittest.TestCase):
    def test_preserves_uuid_and_existing_tokens(self):
        data,kwargs=fixture(); result=run(data,kwargs)
        tokens=v.previous._parse(result['response_bytes'])
        self.assertEqual(tokens.count(kwargs['fresh_uuid_identity']['path']),1)
        self.assertFalse(result['link_approved'])

    def test_rejects_duplicate_archive_or_uuid(self):
        for archive in (r'C:\work\existing.lib',v.uuid.EXPECTED_SDK['path']):
            data,kwargs=fixture();kwargs['new_archive']=archive
            with self.subTest(archive=archive),self.assertRaises(ValueError):run(data,kwargs)

    def test_unreviewed_alias_or_changed_destination_rejected(self):
        for mode in ('alias','destination','identity'):
            data,kwargs=fixture()
            if mode=='alias':kwargs['current_aliases'].append('/ALTERNATENAME:_x=_y')
            elif mode=='destination':kwargs['old_out']=r'C:\wrong'
            else:kwargs['fresh_uuid_identity']['sha256']='a'*64
            with self.subTest(mode=mode),self.assertRaises(ValueError):run(data,kwargs)

if __name__=='__main__':unittest.main()
