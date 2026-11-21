"""Exclusive compiler lane only: complete private M3 residual and tag fixture."""
import os,sys,json,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;P=M/'out/phase2-psa-metadata-ownership-proposal';out=P/'compiled-m3';pins=json.loads((P/'compiled-fixture-pins.json').read_bytes());h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if out.exists():raise FileExistsError(out)
for n,d in pins['tools'].items():
 if h(M/n)!=d:raise ValueError('tool changed '+n)
if h(P/'selection.provisional.json')!=pins['selection_sha256'] or h(R/'fnv_decomp/build/units.json')!=pins['recipe_sha256'] or h(M/'out/phase2-nimem-next-source-composed-u0620/independent-psa-section-review.json')!=pins['producer_review_sha256']:raise ValueError('input pin changed')
if any(k.upper() in ('CL','_CL_') or (k.upper().startswith('FNV_') and k.upper() not in ('FNV_PROJ_ROOT','FNV_MSVC9_ROOT','FNV_MSVC9_RTM_ROOT','FNV_MSVC8_ROOT')) for k in os.environ):raise ValueError('unexpected inherited compiler/build options')
os.environ['FNV_M3_SEL']=str((P/'selection.provisional.json').resolve());sys.path.insert(0,str(M));import gen_m3 as G
if G.ANYNEG:raise ValueError('negative controls not allowed')
import paths
if h(Path(paths.REF_IMAGE))!=pins['reference_sha256']:raise ValueError('reference changed')
out.mkdir();G.GEN=str(out.resolve());G.splice.GEN=G.GEN;G.splice.MANIFEST=str(out/'m3_manifest.json');G.splice.OBJ=str(out/'m3_data.obj');G.SELF=str((P/'selection.provisional.json').resolve());sys.argv=[str(H/'psa_m3_compiled_fixture.py')];G.main()
log=json.loads((out/'m3_gen.log.json').read_bytes());manifest=json.loads((out/'m3_manifest.json').read_bytes())['entries'];expected={0x110fc19:3,0x1196e1e:2,0x1196e3a:1494};found={x['va']:x for x in manifest if x['va'] in expected}
if log['dropped'] or set(found)!=set(expected) or any(found[k]['size']!=v for k,v in expected.items()):raise ValueError('residual entries incomplete')
entry=next(x for x in manifest if x['va']==0x1045408);obj=Path(G.splice.objpath(G.splice.OBJ,entry.get('obj',0)));c=G.splice.Coff(str(obj));sym=c.named(entry['sym']);sec=c.sections[sym['section']];refs=[(off-sym['value'],c.symbols[i]) for off,i,k in sec['relocs'] if sym['value']<=off<sym['value']+entry['size'] and k==6]
if len(refs)!=1 or refs[0][1]['name']!='_M3D_0110fbe8' or refs[0][1]['section']!=0 or G.splice.resolve(refs[0][1]['name'])!=0x110fbe8:raise ValueError('address tag not undefined or resolved')
outputs={p.name:h(p) for p in out.iterdir() if p.is_file()};(out/'fixture-result.json').write_text(json.dumps({'scope':'isolated generated M3 only; no DV1 or final image','pins_sha256':h(P/'compiled-fixture-pins.json'),'outputs':outputs,'residual_sizes':{hex(k):v for k,v in expected.items()},'retained_tag':'_M3D_0110fbe8','tag_section':0,'tag_target':'0x0110fbe8','selected':log['selected'],'kept':log['kept'],'dropped':log['dropped'],'limitations':['full selector must consume this compiled skip','fresh phase0 and image/runtime remain separate','PSA E vtable unchanged']},indent=2)+'\n');print('PASS isolated M3 residual and undefined tag')
