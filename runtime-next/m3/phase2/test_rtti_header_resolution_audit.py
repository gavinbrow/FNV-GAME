import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));from rtti_header_resolution_audit import resolve
class ResolutionTests(unittest.TestCase):
 def test_header_directory_precedes_include_path(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);(p/'a').mkdir();(p/'b').mkdir();(p/'a/x.h').write_text('a');(p/'b/x.h').write_text('b');self.assertEqual(resolve(p/'a/header.h','x.h',[p/'b']), (p/'a/x.h').resolve())
 def test_missing_is_unknown(self):
  with tempfile.TemporaryDirectory() as tmp:self.assertIsNone(resolve(Path(tmp)/'header.h','missing.h',[]))
if __name__=='__main__':unittest.main()
