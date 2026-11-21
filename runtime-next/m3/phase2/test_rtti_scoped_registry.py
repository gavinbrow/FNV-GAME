import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import rtti_scoped_registry as s
class Tests(unittest.TestCase):
 def test_global_namespace_nested_and_function(self):
  t='class TESContainer {}; namespace X { class TESContainer {}; class Outer { struct TESContainer {}; }; void f() { class TESContainer {}; } }'
  a=s.scopes(t,'TESContainer');self.assertEqual([x['category'] for x in a],['global','namespace','nested_class','local_or_unknown']);self.assertEqual(a[1]['qualified_name'],'X::TESContainer')
 def test_comments_and_literals_do_not_create_scopes(self):
  t='// namespace Bad {\nconst char* x="class TESContainer { }"; class TESContainer {};'
  self.assertEqual([x['category'] for x in s.scopes(t,'TESContainer')],['global'])
 def test_extern_linkage_transparent(self):
  a=s.scopes('extern "C" { class TESContainer {}; }','TESContainer');self.assertEqual(a[0]['category'],'global')
 def test_condition_recorded(self):
  a=s.scopes('#if FLAG\nclass TESContainer {};\n#endif\n','TESContainer');self.assertEqual(a[0]['conditional_directives'],['if FLAG'])
 def test_anonymous(self):
  self.assertEqual(s.scopes('namespace { class TESContainer {}; }','TESContainer')[0]['category'],'anonymous_namespace')
 def test_blank_lines_before_directive_preserve_positions_and_scope(self):
  source='namespace N {\n\n\n#if FLAG\n\nclass TESContainer {};\n#endif\n}'
  result=s.scopes(source,'TESContainer')[0]
  self.assertEqual(result['line'],6);self.assertEqual(result['qualified_name'],'N::TESContainer')
  self.assertEqual(result['conditional_directives'],['if FLAG'])
if __name__=='__main__':unittest.main()
