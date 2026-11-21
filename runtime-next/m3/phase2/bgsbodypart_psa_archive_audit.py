"""Read-only archived production PSA namespace diagnostic; never resolves weak E."""
import argparse,hashlib,json,pickle,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp'
sys.path[:0]=[str(F/'tools'),str(RN),str(RN/'pinned-build'),str(RN/'data-v1'),str(RN/'data-v2'),str(RN/'data-v3')]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
import coff_weak,place,paths
NAMES=('??_ETESModelPSA@@UAEPAXI@Z','??_GTESModelPSA@@UAEPAXI@Z','??1TESModelPSA@@UAE@XZ');IDS=(253,370,425,620,621,2909,2910);FIELD=0x0104541c
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--pins',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();root=a.archive.resolve();pins=json.loads(a.pins.read_text());out=a.out.resolve()
 if not out.is_relative_to((M/'out').resolve()) or out.exists():raise ValueError('fresh private output required')
 required=['build-summary.json','evidence/units.json','evidence/data-v1-scratch/dv1_phase0.pkl','evidence/data-v1-scratch/dv1_placed.pkl','evidence/icf_map.json','evidence/capture-manifest.json','evidence/relocs_v7.tsv.gz']+['evidence/%04d.obj'%i for i in IDS]
 for n in required:
  q=root/n
  if not q.is_file() or pins.get(n)!=sha(q):raise ValueError('missing or unpinned archive '+n)
 summary=json.loads((root/'build-summary.json').read_bytes());prov=summary['provenance'];scratch=root/'evidence/data-v1-scratch'
 for n in ('dv1_phase0.pkl','dv1_placed.pkl'):
  if prov['data_v1_scratch_sha256'][n]!=sha(scratch/n):raise ValueError('scratch provenance mismatch '+n)
 if any(x.get('rc') for x in summary['steps']):raise ValueError('failed build step')
 if sha(root/'evidence/units.json')!='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68':raise ValueError('unexpected recipe')
 if sha(Path(paths.REF_IMAGE))!='df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7':raise ValueError('reference changed')
 u=json.loads((root/'evidence/units.json').read_bytes())['units'];pe=Pe(paths.REF_IMAGE);objects={};objinfo={};details=[];names=recipe_names(u)
 for i in IDS:
  c=Coff(str(root/('evidence/%04d.obj'%i)));objects[i]=c;rows=compare(c,pe,u[i]);sec,inferred,errors=eh_sections(c,pe,u[i],rows,names);details.append({'eh_sections':sec,'eh_inferred':inferred,'errors':errors});objinfo[str(i)]={'sha256':pins['evidence/%04d.obj'%i],'functions':len(rows),'matches':sum(x['verdict']=='match' for x in rows),'failures':[{'address':x['address'],'errors':x.get('errors',[])} for x in rows if x['verdict']!='match'],'eh_sections':sec,'eh_errors':errors}
 tails,bad_tails,tail_inferred,_,tail_conflicts=eh_tails([u[i] for i in IDS],details,pe)
 c=objects[620];sym=[]
 for i,s in c.symbols.items():
  if s['name'] not in NAMES:continue
  row={'index':i,'name':s['name'],'section':s['section'],'storage':s['storage'],'type':s['type']}
  if s['storage']==105:
   idx=coff_weak.fallback_index(c,i,allow_unsupported=True);row['fallback']=c.symbols[idx]['name'];ptr=struct.unpack_from('<I',c.data,8)[0];row['characteristic']=struct.unpack_from('<I',c.data,ptr+(i+1)*18+4)[0]
   try:coff_weak.resolve_fallback(c,i,lambda v:(None,None));row['weak_mode_rejects_search_library']=False
   except coff_weak.WeakResolutionError:row['weak_mode_rejects_search_library']=True
  if s['section']>0:
   sec=c.sections[s['section']];row.update(section_size=len(sec['data']),section_flags=sec['flags'],relocations=[{'offset':x,'symbol':c.symbols[y]['name'],'type':z} for x,y,z in sec['relocs']])
  sym.append(row)
 phase=pickle.loads((scratch/'dv1_phase0.pkl').read_bytes());st=pickle.loads((scratch/'dv1_placed.pkl').read_bytes())
 if phase['notok']:raise ValueError('phase0 errors')
 hits=[]
 for k,s in st.SEC.items():
  for r in s['relocs']:
   if r[2] in NAMES:
    loc=st.placed.get(k);hits.append({'units':s['units'],'section':s['name'],'name':r[2],'field_va':loc[0]+r[0] if loc else None,'phase0_source':r[7]})
 capture=json.loads((root/'evidence/capture-manifest.json').read_bytes()); overlay_path=root/'evidence/binding_overlay.json'
 if overlay_path.exists():raise ValueError('unexpected archived overlay: audit requires captured absence')
 if capture.get('binding_overlay')!='absent at runtime-next/build-v7/binding_overlay.json':raise ValueError('overlay absence not captured')
 for i in IDS:
  matches=[x for x in capture['objects'] if x['unit']==i]
  if len(matches)!=1 or matches[0]['sha256']!=pins['evidence/%04d.obj'%i] or any(matches[0][k]!=u[i][k] for k in ('source','compiler','flags')):raise ValueError('capture object/recipe mismatch')
 icf=json.loads((root/'evidence/icf_map.json').read_bytes());primary=NAMES[0]
 bindings=[]
 for i,x in enumerate(u):
  if primary in x.get('symbols',{}):bindings.append([i,'symbol',x['symbols'][primary]])
  for f in x['functions']:
   if primary in [f['symbol']]+f.get('fold_aliases',[]):bindings.append([i,'function',f['address']])
 result={'scope':'archived production evidence; weak E remains deferred','archive_pins_sha256':sha(a.pins),'summary_sha256':sha(root/'build-summary.json'),'objects':objinfo,'recipe_eh_tail_count':len(tails),'bad_tails':bad_tails,'tail_conflicts':tail_conflicts,'unit620_symbols':sym,'phase0_unit_count':len(phase['res']),'placed_relocations':hits,'placed_global_names':{n:st.gdef.get(n) for n in NAMES},'recipe_primary_bindings':bindings,'archived_icf_primary':icf.get(primary),'binding_overlay':'absent per pinned capture manifest; no overlay contents inferred','limitations':['strict mapped function failures require independent source and literal proof','placed state reflects actual data-v1 handling but does not authorize weak fallback','archive pins must be generated from same completed run','V7 name lookup, image field ownership and actual code provider resolution require separate authoritative checks','no E alias or resolver activation']}
 for n in required:
  if sha(root/n)!=pins[n]:raise ValueError('archive changed during audit '+n)
 out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'output':str(out),'unit620_symbols':sym,'placed_hits':len(hits),'failures':{k:len(v['failures']) for k,v in objinfo.items()}}))
if __name__=='__main__':main()
