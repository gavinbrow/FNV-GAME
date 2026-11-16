"""Authored response policy fixtures; no Game or native input."""
import pathlib
import sys
import unittest

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_wave13_diagnostic as m


class Tests(unittest.TestCase):
    def setUp(self):
        self.old=pathlib.Path('prior');self.out=pathlib.Path('next');self.archive=pathlib.Path('new.lib')
        self.iat=['/ALTERNATENAME:iat%d=pointer%d'%(i,i) for i in range(34)]
        self.crt=['/ALTERNATENAME:crt%d=normal%d'%(i,i) for i in range(4)]
        self.tokens=['/OUT:'+str(self.old/'diagnostic.exe'),'/MAP:'+str(self.old/'diagnostic.map')]
        self.tokens+=['prior%d.lib'%i for i in range(29)]+self.iat+self.crt

    def run_response(self, tokens=None, iat=None, crt=None):
        text='\n'.join('"'+t+'"' for t in (self.tokens if tokens is None else tokens))
        return m.response_tokens(text,self.old,self.out,self.archive,self.iat,self.crt,
            self.iat if iat is None else iat,self.crt if crt is None else crt)

    def test_only_archive_and_destinations_change(self):
        out=self.run_response()
        self.assertEqual(len(out),70)
        self.assertEqual(out[:2],['/OUT:'+str(self.out/'diagnostic.exe'),'/MAP:'+str(self.out/'diagnostic.map')])
        self.assertEqual(out[2:31],self.tokens[2:31])
        self.assertEqual(set(out[31:]),set(self.iat+self.crt+[str(self.archive)]))

    def test_disabled_inherited_aliases_are_removed(self):
        out=self.run_response(iat=self.iat[:-1],crt=self.crt[:2])
        self.assertNotIn(self.iat[-1],out)
        self.assertTrue(all(t not in out for t in self.crt[2:]))
        self.assertTrue(all(out.count(t)==1 for t in self.iat[:-1]+self.crt[:2]))

    def test_unreviewed_or_duplicate_alias_rejected(self):
        for tokens in [self.tokens+['/ALTERNATENAME:extra=unknown'], self.tokens+[self.iat[0]]]:
            with self.assertRaises(ValueError):self.run_response(tokens=tokens)
        with self.assertRaises(ValueError):self.run_response(iat=self.iat+['/ALTERNATENAME:extra=unknown'])

    def test_duplicate_archive_or_missing_destination_rejected(self):
        with self.assertRaises(ValueError):self.run_response(tokens=self.tokens+[str(self.archive)])
        with self.assertRaises(ValueError):self.run_response(tokens=self.tokens[1:])


if __name__=='__main__':unittest.main()
