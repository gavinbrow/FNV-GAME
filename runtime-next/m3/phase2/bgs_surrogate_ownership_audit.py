"""Audit removed BGSE surrogate deleting destructor ownership evidence."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';D=M/'out/phase2-bgs-load-typed-v4-mirror';O=M/'out/phase2-bgs-surrogate-ownership.json';sys.path[:0]=[str(F/'tools'),str(RN/'pinned-build')]
from compare import Coff
import coff_weak
OLD_E='??_EFUN_00525ce0@@UAEPAXI@Z';OLD_G='??_GFUN_00525ce0@@UAEPAXI@Z';NATIVE_E='??_EBGSEncounterZone@@UAEPAXI@Z';NATIVE_G='??_GBGSEncounterZone@@UAEPAXI@Z'
def sha(b):return hashlib.sha256(b).hexdigest()
def weak(c,name):
 matches=[i for i,s in c.symbols.items() if s['name']==name and s['storage']==105]
 if len(matches)!=1:raise ValueError('weak alias missing/ambiguous '+name)
 n=coff_weak.fallback_index(c,matches[0],allow_unsupported=True);return c.symbols[n]['name']
def relocs(c,name):
 return [{'section':i,'offset':off,'kind':k,'section_symbols':sorted(x['name'] for x in c.symbols.values() if x['section']==i and not x['name'].startswith('.'))} for i,s in enumerate(c.sections) if s for off,idx,k in s['relocs'] if c.symbols[idx]['name']==name]
def body(c,name):
 s=c.named(name);sec=c.sections[s['section']];data=sec['data'][s['value']:];rs=[(o-s['value'],k,c.symbols[i]['name']) for o,i,k in sec['relocs'] if o>=s['value']];return {'size':len(data),'sha256':sha(data),'relocations':rs}
def main():
 if O.exists():raise FileExistsError('refusing overwrite')
 run=json.loads((D/'compile-result.json').read_text());rows={x['tag']:x for x in run['outcomes']};objs={}
 for tag in ('original','candidate'):
  p=D/(tag+'.obj')
  if rows[tag]['rc'] or not rows[tag]['trace_valid'] or sha(p.read_bytes())!=rows[tag]['object_sha256']:raise ValueError('compiled object changed')
  objs[tag]=Coff(str(p))
 a=objs['original'];b=objs['candidate'];oldweak=weak(a,OLD_E);na=weak(a,NATIVE_E);nb=weak(b,NATIVE_E)
 if (oldweak,na,nb)!=(OLD_G,NATIVE_G,NATIVE_G):raise ValueError('weak fallback mismatch')
 native_a=body(a,NATIVE_G);native_b=body(b,NATIVE_G)
 if native_a!=native_b or native_a['size']!=44:raise ValueError('retained native G differs')
 old_reloc=relocs(a,OLD_E);candidate_reloc=relocs(b,OLD_E)
 if len(old_reloc)!=1 or old_reloc[0]['section_symbols']!=['??_7FUN_00525ce0@@6B@'] or candidate_reloc or relocs(a,OLD_G) or relocs(b,OLD_G):raise ValueError('surrogate relocation scope changed')
 unitfile=F/'build/units.json';units=json.loads(unitfile.read_text())['units'];mapped=[]
 for i,u in enumerate(units):
  for name in (OLD_E,OLD_G):
   if name in u.get('symbols',{}) or any(f['symbol']==name or name in f.get('fold_aliases',[]) for f in u['functions']):mapped.append({'unit':i,'symbol':name})
 if mapped:raise ValueError('surrogate now recipe-mapped')
 files=sorted((RN/'pinned-build/obj_v3').glob('*.obj'));hits={OLD_E:[],OLD_G:[]};index=hashlib.sha256()
 for p in files:
  data=p.read_bytes();index.update(p.name.encode()+b'\0'+hashlib.sha256(data).digest())
  for name in hits:
   if name.encode() in data:hits[name].append(p.name)
 if any(v!=['0002.obj'] for v in hits.values()):raise ValueError('surrogate referenced by another production COFF')
 dvpath=M/'gen/dv1_pieces.json';m3path=M/'gen/m3_manifest.json';dv=json.loads(dvpath.read_text());m3=json.loads(m3path.read_text());va=0x0102cbbc;overlaps=[]
 for label,entries in [('dv1',dv['pieces']),('m3',m3['entries'])]:
  for x in entries:
   if x['va']<va+4 and va<x['va']+x['size']:overlaps.append({'kind':label,'va':x['va'],'size':x['size']})
 if overlaps:raise ValueError('vtable first slot is owned by a selected piece')
 sympath=RN/'data-v3/symbolic.json';s=json.loads(sympath.read_text());base=s['sections']['.rdata']['va'];slot=[x for x in s['fields'] if x[0]=='.rdata' and base+x[1]==va]
 if len(slot)!=1 or slot[0][2]!='?ClearData@TESForm@@UAEXXZ':raise ValueError('symbolic field evidence differs')
 out={'scope':'bounded current-object and selected-first-slot evidence; complete table and final image ownership remain gated','mirror_obj_sha256':{k:sha((D/(k+'.obj')).read_bytes()) for k in objs},'production_object_count':len(files),'production_object_index_sha256':index.hexdigest(),'exact_symbol_object_hits':hits,'surrogate_recipe_mappings':mapped,'original_surrogate_weak_fallback':oldweak,'native_weak_fallback_original':na,'native_weak_fallback_candidate':nb,'original_surrogate_e_relocations':old_reloc,'candidate_surrogate_e_relocations':candidate_reloc,'retained_native_g_body':native_a,'native_g_bodies_equal':True,'vtable_first_slot_va':'0x0102cbbc','selected_piece_overlaps':overlaps,'current_symbolic_first_slot':slot[0],'input_sha256':{'units':sha(unitfile.read_bytes()),'dv1':sha(dvpath.read_bytes()),'m3':sha(m3path.read_bytes()),'symbolic':sha(sympath.read_bytes())},'limitations':['surrogate original vtable section has a real weak E relocation; it is not selected at the first slot in current M3/DV1 evidence','symbolic captured first-slot mapping does not establish full native vtable ownership','exact-name production COFF scan does not prove semantic identity of differently named symbols','final image and relocation checks required after source transaction']}
 O.write_text(json.dumps(out,indent=2));print(json.dumps({'objects':len(files),'surrogate_hits':hits,'original_surrogate_relocations':len(old_reloc),'native_g_equal':True,'slot_overlaps':len(overlaps)}))
if __name__=='__main__':main()
