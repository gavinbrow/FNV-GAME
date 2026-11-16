import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import crt_lane04_observer as observer

class ObserverTests(unittest.TestCase):
    def test_comparison_requires_entire_span(self):
        self.assertEqual(observer.compare_section(b'abc',b'abc',[]),(True,3))
        self.assertEqual(observer.compare_section(b'abc',b'abx',[]),(False,3))
        with self.assertRaises(ValueError):observer.compare_section(b'abc',b'ab',[])
    def test_only_supported_exact_relocation_mask(self):
        relocation=[dict(offset=1,kind=20)]
        self.assertEqual(observer.compare_section(b'a1234z',b'a5678z',relocation),(True,2))
        with self.assertRaises(ValueError):observer.compare_section(b'abcdef',b'abcdef',[dict(offset=5,kind=6)])
        with self.assertRaises(ValueError):observer.compare_section(b'abcdef',b'abcdef',[dict(offset=1,kind=7)])
    def test_duplicate_and_oversize_requests_rejected(self):
        row=dict(target='0x00ec6130',alternatives=[dict(reference_start='0x00ec6130',
            reference_size=4097,target_symbol_value=0)])
        with self.assertRaises(ValueError):observer.spans(dict(requests=[row]))
    def test_nonexact_entry_rejected(self):
        row=dict(target='0x00ec6130',alternatives=[dict(reference_start='0x00ec6131',
            reference_size=100,target_symbol_value=0)])
        with self.assertRaises(ValueError):observer.spans(dict(requests=[row]))
    def test_review_is_hash_bound(self):
        with self.assertRaises(ValueError):observer.review_gate(dict(status='approved'),{})

if __name__=='__main__':unittest.main()
