import hashlib
from pathlib import Path
import sys
import unittest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'tools/rebuild'))
import startup_direct_variant_v1 as variant


class StartupDirectVariant(unittest.TestCase):
    def test_exact_source_diff_and_identity(self):
        original = variant.SOURCE.read_bytes()
        result = variant.transform(original)
        self.assertEqual(hashlib.sha256(result).hexdigest(),
                         'bb479ff05a8cbfc596d481082786c1e21358835b620d5eeccb32638972ee6111')
        newline = b'\r\n' if b'\r\n' in original else b'\n'
        for old, new in reversed(variant.REPLACEMENTS):
            new = new.replace(b'\n', newline)
            self.assertEqual(result.count(new), 1)
            result = result.replace(new, old, 1)
        self.assertEqual(result, original)

    def test_rejects_changed_source(self):
        with self.assertRaises(ValueError):
            variant.transform(variant.SOURCE.read_bytes() + b' ')


if __name__ == '__main__':
    unittest.main()
