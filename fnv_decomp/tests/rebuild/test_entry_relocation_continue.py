"""Continuation scope and census guards; no private inputs or native work."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import entry_relocation_continue as continuation


class ContinuationTests(unittest.TestCase):
    def setUp(self):
        self.policy=continuation.policy()
        counts=[(213,114,2),(214,21,4),(272,21,3),(870,34,2),(2709,148,2),(2757,281,6)]
        self.units=[dict(recipe_index=i,plain_comparison_rows=n,migration=dict(repaired_count=r),
                         operation='reused_v1_verified_terminal' if i<1000 else 'compiled_v2') for i,n,r in counts]

    def test_only_four_successful_terminal_units_can_be_reused(self):
        previous=dict(status='error',units=self.units[:4])
        self.assertEqual(len(continuation.cached_units(previous,self.policy)),4)
        for bad in [dict(previous,status='pass'),dict(previous,units=self.units[:5]),dict(previous,units=self.units[:3])]:
            with self.assertRaises(ValueError):continuation.cached_units(bad,self.policy)
        broken=copy.deepcopy(previous);broken['units'][0]['migration']['repaired_count']=1
        with self.assertRaises(ValueError):continuation.cached_units(broken,self.policy)

    def test_final619_is_four_reused_and_only_two_new_compiles(self):
        continuation.final_census(self.units)
        for change in ('omitted','duplicate','row','repair','operation'):
            bad=copy.deepcopy(self.units)
            if change=='omitted':bad.pop()
            elif change=='duplicate':bad.append(copy.deepcopy(bad[-1]))
            elif change=='row':bad[-1]['plain_comparison_rows']-=1
            elif change=='repair':bad[-1]['migration']['repaired_count']-=1
            else:bad[0]['operation']='compiled_v2'
            with self.assertRaises(ValueError):continuation.final_census(bad)


if __name__=='__main__':unittest.main()
