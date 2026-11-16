"""Authored synthetic current-cohort IAT identities only."""
import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_import34_inputs as inputs
from test_application_wave9_inputs import census31

def census34():
    proposals,fields,catalog,libraries=copy.deepcopy(census31())
    for n in range(3):
        va='0x%08x'%(0x30000000+n*4);name='Last%d'%n;offset=12000+n*100
        canonical='_fnv_undefined_'+inputs.digest(inputs.diagnostic.canonical(dict(original_base=va,role='iat-cell')))
        catalog['imports'].append(dict(original_IAT_va=va,dll='LAST.dll',export=dict(kind='name',name=name,hint=n),import_id=1200+n))
        row=copy.deepcopy(proposals[0]);row.update(canonical_IAT_symbol=canonical,original_IAT_va=va,dll='LAST.dll',export=dict(kind='name',name=name),member_offset=offset,proposed_pointer_symbol='__imp__'+name);proposals.append(row)
        field=copy.deepcopy(fields[0]);field.update(canonical=canonical,member=name+'.obj');field['proof'].update(original_base=va,original_target=va,import_id=1200+n);fields.append(field)
        libraries['fixture.lib']['imports'].append(dict(dll='LAST.dll',export=dict(kind='name',name=name),machine=0x14c,import_type=0,name_type=2,symbol='_'+name,pointer_symbol='__imp__'+name,member_offset=offset))
        libraries['fixture.lib']['index'] += [dict(symbol='_'+name,member_offset=offset),dict(symbol='__imp__'+name,member_offset=offset)]
    return proposals,fields,catalog,libraries

class Tests(unittest.TestCase):
    def test_all34includes_last_new_cell(self):
        rows=inputs.import34_alias_census(*census34());self.assertEqual(len(rows),34);self.assertTrue(all(r['enabled'] for r in rows));self.assertEqual(rows[-1]['positive_import_identity'],('LAST.dll','name','Last2'))
    def test_old31_or_duplicate_proposal_rejected(self):
        with self.assertRaises(ValueError):inputs.import34_alias_census(*census31())
        args=list(census34());args[0][-1]=copy.deepcopy(args[0][0])
        with self.assertRaises(ValueError):inputs.import34_alias_census(*args)
    def test_unknown_nonzero_use_disables_only_its_cell(self):
        args=list(census34());bad=copy.deepcopy(args[1][-1]);bad['member']='bad.obj';bad['proof']['addend_bits']=4;args[1].append(bad)
        rows=inputs.import34_alias_census(*args);self.assertTrue(all(r['enabled'] for r in rows[:-1]));self.assertFalse(rows[-1]['enabled']);self.assertEqual(rows[-1]['use_count'],2)
    def test_wrong_native_pointer_identity_disables_one_cell(self):
        args=list(census34());args[3]['fixture.lib']['imports'][-1]['pointer_symbol']='__imp__Other'
        rows=inputs.import34_alias_census(*args);self.assertTrue(all(r['enabled'] for r in rows[:-1]));self.assertFalse(rows[-1]['enabled'])
if __name__=='__main__':unittest.main()
