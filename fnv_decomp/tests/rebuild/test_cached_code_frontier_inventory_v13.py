"""Owner fixtures use authored COFF only, never saved Game metadata."""
import copy
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_code_frontier_inventory_v13 as inventory
import test_cached_frontier_code_factory_independent as authored


def fixture(field=True,safeseh=False):
    receipt,records,request,current,_=authored.fixture(field=field,safeseh=safeseh)
    receipt.update(schema_version=1,source_sha256=inventory.PINS['tools/rebuild/cached_root_observe.py'],
        operation_sha256=inventory.KNOWN['native_operation'])
    receipt['inputs']['qualified_request']['sha256']=inventory.QUALIFIED_REQUEST
    providers={r['original_address']:{k:v for k,v in r.items() if k not in ('original_address','recipe_index')} for r in request['roots']}
    for entry in providers.values():entry['planned_canonical_name']=inventory.base.pool.canonical({k:entry[k] for k in ('recipe_id','object_sha256','symbol_index')})
    roots=request['roots'];units={roots[0]['recipe_id']:dict(recipe_id=roots[0]['recipe_id'],recipe_index=roots[0]['recipe_index'],
        object_sha256=roots[0]['object_sha256'],source_sha256=roots[0]['source_sha256'])}
    for group in current['groups']:group['original_targets']=copy.deepcopy(group['original_bases'])
    return dict(records={}),receipt,request,providers,units,current,records


def registry(args):
    return inventory.extend_registry(*args[:5],expected_old=0,expected_new=2,expected_recipes=1)


class OwnerInventoryV13Tests(unittest.TestCase):
    def test_native_summary_identity_is_preserved_without_qualification_certificate(self):
        args=fixture();before=copy.deepcopy(args);result=registry(args)
        self.assertEqual(len(result['records']),2);self.assertEqual(args,before)
        for address,row in result['records'].items():
            s=row['summary'];a=row['authority']
            self.assertEqual(a['record_sha256'],s['record_sha256'])
            self.assertEqual(a['contract_identity_sha256'],s['contract_identity_sha256'])
            self.assertEqual(a['qualified_metadata_row_sha256'],s['qualified_metadata_row_sha256'])
            self.assertFalse(a['qualification_certificate_created'])
        self.assertFalse(result['certificate_created'])

    def test_union_is_evidence_only_and_negative_not_hydrated(self):
        args=fixture(field=False,safeseh=True);result=registry(args)
        ledger=inventory.classify_demands(args[5],args[3],args[4],result,set(),[],expected_code_count=2,expected_quarantines=set())
        self.assertEqual(len(ledger['metadata_requests']),1)
        self.assertEqual(result['native_union_summaries_evidence_only'],1)
        self.assertEqual(len(result['records']),2)
        self.assertEqual(sum(ledger['counts'].values()),2)
        self.assertFalse(ledger['closure_inferred'])

    def test_whole_native_census_is_required(self):
        args=fixture();args[1]['observations'].pop()
        with self.assertRaises(ValueError):registry(args)

    def test_fresh_process_cli_help(self):
        p=subprocess.run([sys.executable,str(ROOT/'tools/rebuild/cached_code_frontier_inventory_v13.py'),'--help'],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn('--operation',p.stdout)


if __name__=='__main__':unittest.main()
