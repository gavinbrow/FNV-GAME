"""Bound unit1592's vptr target using a source-owned sibling factory and RTTI."""
import copy,hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';O=R/'phase2-nimem-1592-psys-color-pointer-proof.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve prior evidence')
 recipe=R/'phase2-nimem-calendar-binding-v1/units.generated';obj=R/'phase2-nimem-combined-825d-run/unit-1592/candidate.obj';census=R/'phase2-class-census/census-v2.json'
 if sha(recipe)!='92b5d4058d196208672a6479f1d5e33414c2e022172fa3f3674d1d8e12ede9b8' or sha(obj)!='ffa6eb0d20842df957989f1640bb58e355533b30d16dd473ff18947a82c412d7':raise ValueError('recipe or object changed')
 units=json.loads(recipe.read_text())['units'];spec=units[1592];c=Coff(str(obj));pe=Pe(paths.REF_IMAGE);before=compare(c,pe,spec);sibling=next(x for x in before if x['address']=='0x00c2d180');target='??_7PSysColorModifierStandIn@@6B@';r=[x for x in sibling['relocations'] if x['symbol']==target]
 if sibling['verdict']!='match' or len(r)!=1 or not r[0]['match'] or r[0]['offset']!=28:raise ValueError('sibling factory table proof failed')
 reference_target=int(r[0]['observed'],16)
 if spec['symbols'][target]!=r[0]['observed'] or struct.unpack('<I',pe.read(0x00c2d240+31,4))[0]!=reference_target:raise ValueError('factory table targets differ')
 entries=[x for x in json.loads(census.read_text())['vtables'] if x['vtable_va']==reference_target]
 if len(entries)!=1 or entries[0]['locator']['type_name']!='.?AVNiPSysColorModifier@@' or entries[0]['locator']['subobject_offset']!=0:raise ValueError('RTTI primary identity differs')
 fixed=copy.deepcopy(spec);fixed['symbols']['?PTR_010bffe4@@3DA']=r[0]['observed'];after=compare(c,pe,fixed);sec,inf,err=eh_sections(c,pe,fixed,after,recipe_names(units));tails,bad,_,_,conf=eh_tails([fixed],[{'eh_sections':sec,'eh_inferred':{k:'0x%08x'%v for k,v in inf.items()}}],pe)
 if len(after)!=len(spec['functions']) or any(x['verdict']!='match' for x in after):raise ValueError('caller diagnostic does not pass')
 O.write_text(json.dumps({'recipe_sha256':sha(recipe),'candidate_object_sha256':sha(obj),'reference_sha256':sha(Path(paths.REF_IMAGE)),'census_sha256':sha(census),'source':'src/gamebryo2.2/corelibs/niparticle/nipsyscolormodifier.cpp','sibling_factory_result':sibling,'caller_address':'0x00c2d240','caller_field_offset':31,'derived_table_address':r[0]['observed'],'rtti_type':entries[0]['locator']['type_name'],'rtti_locator':entries[0]['locator']['va'],'rtti_hierarchy':entries[0]['locator']['hierarchy_va'],'diagnostic_binding':{'?PTR_010bffe4@@3DA':r[0]['observed']},'strict_functions':len(after),'strict_matches':sum(x['verdict']=='match' for x in after),'ordinary_eh_sections':len(sec),'ordinary_eh_failed':sum(not x[2] for x in sec),'ordinary_eh_errors':err,'ordinary_eh_bad_tails':bad,'ordinary_eh_conflicts':conf,'limitations':['binding is diagnostic and derives from independently matching sibling factory plus original RTTI, not address spelling','stand-in emitted hierarchy, vtable slot correctness, linker ownership, and full native class identity remain unproved','no recipe or source installed']},indent=2));print(json.dumps({'target':r[0]['observed'],'strict':len(after),'eh_failed':sum(not x[2] for x in sec),'errors':len(err),'sha256':sha(O)}))
if __name__=='__main__':main()
