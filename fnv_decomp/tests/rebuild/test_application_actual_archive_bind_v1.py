"""Synthetic archive/member integrity, no native operations."""
import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_actual_archive_bind_v1 as bind
from test_application_link_cohort import obj


def fixture():
    data=obj();members=[{'name':'one.obj','projection':{'output_sha256':bind.coff.digest(data)}}]
    archive=bind.coff.archive([('one.obj',data)])
    return dict(archive_bytes=archive,archive_sha256=bind.coff.digest(archive),members=members,
                member_count=1,member_bytes={'one.obj':data})

class Tests(unittest.TestCase):
    def test_exact_archive_binds(self):self.assertFalse(bind.bind(**fixture())['link_approved'])
    def test_wrong_or_extra_archive_member_rejected(self):
        for mode in ('wrong','extra','reordered_ledger'):
            f=copy.deepcopy(fixture())
            if mode=='wrong':f['member_bytes']['one.obj']+=b'x'
            elif mode=='extra':f['member_bytes']['extra.obj']=b'x'
            else:f['members'][0]['name']='other.obj'
            with self.subTest(mode=mode),self.assertRaises(ValueError):bind.bind(**f)
    def test_wrong_archive_identity_rejected(self):
        f=fixture();f['archive_sha256']='0'*64
        with self.assertRaises(ValueError):bind.bind(**f)

if __name__=='__main__':unittest.main()
