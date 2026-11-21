"""Replay NiRef fixture with source-backed atomic helper diagnostic, no installation."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;sys.path[:0]=[str(H),str(R/'fnv_decomp/tools'),str(R/'runtime-next')]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
from rtti_hkp_viewer_compare import relocated
import paths
D=M/'out/phase2-niref-primary-inline-fixture';A=M/'out/phase2-native-source-positive/evidence';OUT=D/'source-atomic-owner-replay.json';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError(OUT)
 m=json.loads((D/'manifest.json').read_text());prior=json.loads((D/'lane-comparison.json').read_text());cap=json.loads((A/'capture-manifest.json').read_text());record=next(x for x in cap['objects'] if x['unit']==633);owner=A/'0633.obj';cand=D/'612/candidate.obj'
 if h(D/'manifest.json')!='84940ae66aefdbb57cb06d7b7f6b051825e3d601766b3532149fc0e808eca89a' or h(owner)!=record['sha256'] or h(cand)!=prior['results']['612']['candidate']['object_sha256']:raise ValueError('input differs')
 recipe=json.loads((A/'units.json').read_text())['units'];spec=recipe[633];fn=next(f for f in spec['functions'] if f['address']=='0x004019a0')
 if fn['symbol']!='?WaitForSingleObjectEx@@YAKPAJ@Z' or fn['size']!=15:raise ValueError('source owner changed')
 source=R/'fnv_decomp'/spec['source'];freeze=json.loads((M/'out/phase2-native-source-positive-freeze/inputs-before.json').read_text());key=str(source.resolve());sourcehash=h(source)
 if freeze[key]['sha256']!=sourcehash:raise ValueError('owner source differs from captured source')
 text=source.read_text(encoding='utf-8-sig');anchor='unsigned long WaitForSingleObjectEx(long* value)\n{\n    return InterlockedDecrement(value);\n}'
 if anchor not in text.replace('\r\n','\n'):raise ValueError('owner source contract differs')
 obj=Coff(str(owner));c=Coff(str(cand));old,orls=relocated(obj,fn['symbol'],15,{});new,nrls=relocated(c,'?NiAtomicSubtract@@YAIAAI@Z',15,{})
 if old!=new or orls!=nrls or len(orls)!=1 or orls[0][2]!='__imp__InterlockedDecrement@4':raise ValueError('helper body or import differs')
 parent=json.loads((D/'units.generated').read_text())['units'];u=copy.deepcopy(parent[612]);name='?NiAtomicSubtract@@YAIAAI@Z'
 if name in u['symbols']:raise ValueError('unexpected preexisting helper binding')
 u['symbols'][name]='0x004019a0';pe=Pe(paths.REF_IMAGE);checks={}
 for i,spec in ((612,u),(1503,parent[1503])):
  o=D/str(i)/'candidate.obj';co=Coff(str(o));rr=compare(co,pe,spec);sec,inf,err=eh_sections(co,pe,spec,rr,recipe_names(parent));checks[str(i)]={'object_sha256':h(o),'functions':len(rr),'matches':sum(x['verdict']=='match' for x in rr),'failures':[{'address':x['address'],'errors':x['errors']} for x in rr if x['verdict']!='match'],'eh_sections':len(sec),'eh_failed':[x for x in sec if not x[2]],'eh_errors':err,'eh_inferred':{k:hex(v) for k,v in inf.items()}}
 if any(x['matches']!=x['functions'] or x['eh_failed'] or x['eh_errors'] for x in checks.values()):raise ValueError('diagnostic replay failed')
 pecheck=compare(obj,pe,dict(spec,functions=[fn]));
 if len(pecheck)!=1 or pecheck[0]['verdict']!='match':raise ValueError('source owner does not match reference')
 fact=prior['candidate_niref_sections'];dtor=next(x for x in fact['612']['sections'] if x['symbol']=='??1NiRefObject@@UAE@XZ');wrapper=next(x for x in fact['612']['sections'] if x['symbol']=='??_GNiRefObject@@UAEPAXI@Z');o2=next(x for x in fact['1503']['sections'] if x['symbol']=='??_GNiRefObject@@UAEPAXI@Z')
 if dtor['section_size']!=33 or wrapper['section_size']!=46 or o2['section_size']!=44:raise ValueError('native body extent differs')
 out={'scope':'private unit-local source-backed atomic helper diagnostic; no recipe edits','fixture_sha256':h(D/'manifest.json'),'prior_comparison_sha256':h(D/'lane-comparison.json'),'owner_capture_sha256':h(A/'capture-manifest.json'),'owner_object_sha256':h(owner),'owner_source_sha256':sourcehash,'helper_symbol':name,'source_owner_symbol':fn['symbol'],'source_owner_address':fn['address'],'equal_helper_bytes_and_import_reloc':True,'diagnostic_unit_local_binding':{name:'0x004019a0'},'checks':checks,'612_native_destructor':dtor,'612_native_G_wrapper':wrapper,'1503_competing_G_wrapper':o2,'weak_aux':{'612':fact['612']['weak_aux'],'1503':fact['1503']['weak_aux']},'optimized_clone':prior['optimized_clone'],'limitations':['this diagnostic compares source owner and emitted helper, not a binding inferred from caller reference field','612 G46 and 1503 G44 are competing same-name COMDAT definitions: final provider/weak and unit ownership proof required','public header change requires full affected consumer/ODR review','165 matches do not establish full image or runtime acceptance']}
 OUT.write_text(json.dumps(out,indent=2));print(json.dumps({'sha256':h(OUT),'checks':{k:(v['matches'],v['functions'],len(v['eh_failed']),len(v['eh_errors'])) for k,v in checks.items()}}))
if __name__=='__main__':main()
