import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from harness_evidence import accepted_verdict


class VerdictTests(unittest.TestCase):
    def setUp(self):
        self.exe = os.path.abspath('test-final.exe')
        self.tag = 'build-all-unique-123'
        self.verdict = {'exe': self.exe, 'tag': self.tag, 'pass_': True}

    def test_valid_and_normalized_path(self):
        self.assertTrue(accepted_verdict(0, self.verdict, self.exe, self.tag))
        other = dict(self.verdict, exe=os.path.join(os.path.dirname(self.exe), '.', os.path.basename(self.exe)))
        self.assertTrue(accepted_verdict(0, other, self.exe, self.tag))

    def test_wrong_executable_or_tag(self):
        self.assertFalse(accepted_verdict(0, dict(self.verdict, exe=self.exe + '.other'), self.exe, self.tag))
        self.assertFalse(accepted_verdict(0, dict(self.verdict, tag='old-run'), self.exe, self.tag))

    def test_nonzero_exit_rejects_stale_pass(self):
        self.assertFalse(accepted_verdict(1, self.verdict, self.exe, self.tag))

    def test_missing_or_malformed_fields(self):
        for v in (None, [], {}, {'exe': self.exe, 'tag': self.tag}, dict(self.verdict, exe=None),
                  dict(self.verdict, tag=None), dict(self.verdict, exe='\0')):
            with self.subTest(verdict=v):
                self.assertFalse(accepted_verdict(0, v, self.exe, self.tag))
        for exe, tag in ((None, self.tag), ('', self.tag), (self.exe, None), (self.exe, '')):
            self.assertFalse(accepted_verdict(0, self.verdict, exe, tag))

    def test_truthy_non_boolean_is_rejected(self):
        for flag in (1, 'true', [True], False, None):
            with self.subTest(flag=flag):
                self.assertFalse(accepted_verdict(0, dict(self.verdict, pass_=flag), self.exe, self.tag))


if __name__ == '__main__':
    unittest.main()
