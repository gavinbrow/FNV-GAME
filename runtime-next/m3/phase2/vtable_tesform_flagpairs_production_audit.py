"""Audit actual post-transaction objects against prior objects, source owners and graph."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe
from rtti_hkp_viewer_compare import relocated
import paths,class_metadata_compare as cm,rtti_mirror_compare as mm
A=M/'out/phase2-flags-script-production-after';B=M/'out/phase2-flags-script-production-before';O=M/'out/phase2-flags-script-production-audit.json';C=M/'out/phase2-class-census/census-6757.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('no overwrite')
 run=json.loads((A/'compile-result.json').read_bytes());uf=F/'build/units.json';units=json.loads(uf.read_bytes())['units'];census=json.loads(C.read_bytes())
 if sha(uf)!=run['recipe_sha256'] or census['inputs']['units_sha256']!=sha(uf):raise ValueError('recipe mismatch')
 rows={x['index']:x for x in run['results']}
 for i in (2,998,1111,1112):
  if rows[i]['status']!='ok' or rows[i]['rc'] or sha(A/('%04d.obj'%i))!=rows[i]['object_sha256']:raise ValueError('object mismatch')
 c=Coff(str(A/'0998.obj'));pe=Pe(paths.REF_IMAGE);folds=[]
 for va,names in [('0x004011b0',['?Unk_27@TESForm@@UBE_NXZ','?Unk_28@TESForm@@UBE_NXZ']),('0x004011d0',['?Unk_29@TESForm@@UAE_NXZ','?Unk_2A@TESForm@@UAE_NXZ'])]:
  v=int(va,16);owners=[(i,f) for i,u in enumerate(units) for f in u['functions'] if int(f['address'],16)<v+26 and v<int(f['address'],16)+f['size']]
  if len(owners)!=1 or owners[0][0]!=998 or owners[0][1]['symbol']!=names[0] or owners[0][1].get('fold_aliases')!=names[1:]:raise ValueError('owner mismatch')
  for n in names:
   raw,rel=relocated(c,n,26,{})
   if rel or raw!=pe.read(v,26):raise ValueError('fold body mismatch')
  folds.append({'address':va,'size':26,'owner_unit':998,'symbols':names,'reference_match':True,'relocations':0})
 graph=cm.compare_class(A/'0002.obj',units[2],units,census,'.?AVBGSEncounterZone@@');table=graph['tables'][0]
 if not table['graph_fields_equal'] or len(table['slots'])!=78:raise ValueError('class graph mismatch')
 eh={}
 for i in (2,998,1111,1112):
  x=mm.exception_sections(Coff(str(B/('%04d.obj'%i))));y=mm.exception_sections(Coff(str(A/('%04d.obj'%i))))
  if x!=y:raise ValueError('EH mismatch '+str(i))
  eh[str(i)]=len(x)
 result={'scope':'actual saved production object and named EH section-tail comparisons; no final placement or ODR claim','recipe_sha256':sha(uf),'compile_result_sha256':sha(A/'compile-result.json'),'objects':{str(i):sha(A/('%04d.obj'%i)) for i in (2,998,1111,1112)},'folds':folds,'eh_named_section_tails':eh,'class_metadata':graph}
 O.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'folds':len(folds),'eh':eh,'matched':sum(x['match'] for x in table['slots'])}))
if __name__=='__main__':main()
