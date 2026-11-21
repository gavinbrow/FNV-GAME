import tempfile,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_mirror_prepare as m
class MirrorTests(unittest.TestCase):
 def test_location_sensitive_nested_lookup(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);(p/'src').mkdir();(p/'include').mkdir();(p/'src/main.cpp').write_text('#include "A.h"\n');(p/'include/A.h').write_text('#include "B.h"\n');(p/'src/B.h').write_text('source');(p/'include/B.h').write_text('include')
   graph=m.walk(p,'src/main.cpp',{});edge=next(x for x in graph['edges'] if x['include']=='B.h');self.assertEqual(edge['resolved'],'include/B.h')
 def test_enclosing_header_search_and_override(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);(p/'src/a').mkdir(parents=True);(p/'include').mkdir();(p/'src/a/main.cpp').write_text('#include "../parent.h"\n');(p/'src/parent.h').write_text('#include "a/child.h"\n');(p/'src/a/child.h').write_text('#include "leaf.h"\n');(p/'src/leaf.h').write_text('leaf')
   graph=m.walk(p,'src/a/main.cpp',{'src/parent.h':b'#include "a/child.h"\n'});self.assertTrue(any(x['resolved']=='src/leaf.h' for x in graph['edges']))
 def test_unresolved_and_escape(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);(p/'src').mkdir();(p/'include').mkdir();(p/'src/main.cpp').write_text('#include "missing.h"\n#include <stdlib.h>\n');g=m.walk(p,'src/main.cpp',{});self.assertEqual(len(g['unresolved']),2)
   with self.assertRaises(ValueError):m.logical('../escape')
 def test_transition_corrupt_rejected(self):
  with self.assertRaises(ValueError):m.transition(b'bad',b'bad',b'bad')
if __name__=='__main__':unittest.main()
