import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/rebuild'))
import application_crt_diagnostic_successor as successor

class ResponseTests(unittest.TestCase):
    def setUp(self):
        self.old = Path('old'); self.new = Path('new')
        self.tokens = ['/NOLOGO', '/OUT:old/diagnostic.exe', '/MAP:old/diagnostic.map', 'real.lib']
        self.tokens[1] = '/OUT:' + str(self.old / 'diagnostic.exe')
        self.tokens[2] = '/MAP:' + str(self.old / 'diagnostic.map')
        self.aliases = ['/ALTERNATENAME:canonical%d=normal%d' % (i, i) for i in range(4)]
    def response(self, tokens): return '\n'.join('"'+x+'"' for x in tokens)
    def test_only_destinations_and_four_aliases_change(self):
        actual = successor.successor_tokens(self.response(self.tokens), self.old, self.new, self.aliases)
        self.assertEqual(actual, ['/NOLOGO', '/OUT:'+str(self.new/'diagnostic.exe'), '/MAP:'+str(self.new/'diagnostic.map'), 'real.lib']+self.aliases)
    def test_reject_duplicate_destination(self):
        with self.assertRaises(ValueError): successor.successor_tokens(self.response(self.tokens+self.tokens[1:2]), self.old, self.new, self.aliases)
    def test_reject_alias_collision(self):
        with self.assertRaises(ValueError): successor.successor_tokens(self.response(self.tokens+[self.aliases[0]]), self.old, self.new, self.aliases)
    def test_reject_force(self):
        with self.assertRaises(ValueError): successor.successor_tokens(self.response(self.tokens+['/FORCE']), self.old, self.new, self.aliases)
    def test_reject_unquoted_token(self):
        with self.assertRaises(ValueError): successor.successor_tokens('real.lib', self.old, self.new, self.aliases)

if __name__ == '__main__': unittest.main()
