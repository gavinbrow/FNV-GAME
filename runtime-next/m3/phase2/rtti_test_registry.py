"""Lexical registry parser tests; no source or compiler required."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_class_registry as r

class RegistryTests(unittest.TestCase):
 def test_definitions_ignore_comments_and_strings(self):
  s='// class Ghost {};\nconst char* x="class Ghost {}";\nclass Real : public Base { struct Inner { int x; }; };'
  d=list(r.definitions(s,{'Ghost','Real'}));self.assertEqual(len(d),1);self.assertEqual(d[0]['name'],'Real');self.assertEqual(d[0]['line'],3)
 def test_balanced_nested_and_distinct_bodies(self):
  d=list(r.definitions('class A { struct B { int x; }; }; class A { int y; };',{'A'}));self.assertEqual(len(d),2);self.assertNotEqual(d[0]['lexical_token_sha256'],d[1]['lexical_token_sha256'])
 def test_includes_preserve_strings_but_drop_comments(self):
  s='#include "real.h"\n/*\n#include "fake.h"\n*/\n// #include "also_fake.h"\n';self.assertEqual(r.INCLUDE.findall(r.without_comments(s)),['real.h'])
 def test_unbalanced_definition_excluded(self):self.assertEqual(list(r.definitions('class A {',{'A'})),[])

if __name__=='__main__':unittest.main(verbosity=2)
