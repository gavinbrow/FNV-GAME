import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import crt_lane01_observer as observer

class Lane01ObserverTests(unittest.TestCase):
    def row(self,target='0x00ec9610',size=326,value=0):
        return dict(target=target,alternatives=[dict(reference_start=hex(int(target,0)-value),
            reference_size=size,target_symbol_value=value)])
    def test_nonzero_symbol_entry(self):
        result,total=observer.bounds_for(dict(requests=[self.row('0x00ec9650',326,64)]))
        self.assertEqual(result['0x00ec9650'],(0x00ec9610,326));self.assertEqual(total,326)
    def test_alternatives_coalesce_without_losing_span(self):
        row=self.row(size=326);row['alternatives'].append(self.row(size=324)['alternatives'][0])
        self.assertEqual(observer.bounds_for(dict(requests=[row]))[1],326)
    def test_duplicate_oversize_and_bad_start_rejected(self):
        row=self.row()
        with self.assertRaises(ValueError):observer.bounds_for(dict(requests=[row,row]))
        with self.assertRaises(ValueError):observer.bounds_for(dict(requests=[self.row(size=4097)]))
        row['alternatives'][0]['reference_start']='0x00ec9611'
        with self.assertRaises(ValueError):observer.bounds_for(dict(requests=[row]))
    def test_outside_checked_text_rejected(self):
        with self.assertRaises(ValueError):observer.bounds_for(dict(requests=[self.row('0x00400000')]))
    def test_hashless_review_rejected(self):
        with self.assertRaises(ValueError):observer.review_gate(dict(status='approved'),{})

if __name__=='__main__':unittest.main()
