"""Snapshot PSA candidate against saved placement and current V7 namespaces; no resolver changes."""
import hashlib,json,pickle,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';B=M/'out/phase2-flags-script-positive';O=M/'out/phase2-bgsbodypart-split-headers-proposal';OUT=O/'psa-effective-weak-snapshot.json'
sys.path[:0]=[str(RN/'data-v1'),str(RN/'data-v2'),str(RN/'data-v3'),str(RN)]
import place
PRIMARY='??_ETESModelPSA@@UAEPAXI@Z';FIELD=0x104541c
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError(OUT)
 prior=json.loads((O/'psa-weak-ownership.json').read_text());summary=B/'build-summary.json';prov=json.loads(summary.read_text())['provenance'];scratch=B/'evidence/data-v1-scratch';states={}
 for name in ('dv1_phase0.pkl','dv1_placed.pkl'):
  p=scratch/name
  if sha(p)!=prov['data_v1_scratch_sha256'][name]:raise ValueError('saved scratch digest mismatch')
  states[name]=pickle.loads(p.read_bytes())
 phase=states['dv1_phase0.pkl'];st=states['dv1_placed.pkl']
 if phase['notok']:raise ValueError('phase0 errors')
 phase_hits=[]
 for i,v in phase['res'].items():
  for sec in v.get('secs',[]):
   for r in sec.get('relocs',[]):
    if r[2]==PRIMARY:phase_hits.append({'unit':i,'section':sec['name'],'offset':r[0]})
 placed_hits=[]
 for k,sec in st.SEC.items():
  for r in sec['relocs']:
   if r[2]==PRIMARY:
    loc=st.placed.get(k);placed_hits.append({'units':sec['units'],'section':sec['name'],'field_va':loc[0]+r[0] if loc else None,'phase0_source':r[7]})
 units=B/'evidence/units.json';recipe=json.loads(units.read_bytes())['units'];bindings=[]
 for i,u in enumerate(recipe):
  if PRIMARY in u.get('symbols',{}):bindings.append((i,'symbol',u['symbols'][PRIMARY]))
  for f in u['functions']:
   if f['symbol']==PRIMARY or PRIMARY in f.get('fold_aliases',[]):bindings.append((i,'function',f['address']))
 icf=RN/'build-v7/icf_map.json';overlay=RN/'reloc-v7/binding_overlay.json';ov=json.loads(overlay.read_bytes());imap=json.loads(icf.read_bytes())
 lookup={'recipe_bindings':bindings,'phase0_relocations':phase_hits,'placed_relocations':placed_hits,'placed_global':st.gdef.get(PRIMARY),'current_v7_name':place.v7map.get(PRIMARY),
         'current_icf':imap.get(PRIMARY),'current_global_overlay':ov['global_name'].get(PRIMARY),
         'current_unit_overlays':[(k,v[PRIMARY]) for k,v in ov['by_unit_name'].items() if PRIMARY in v],
         'current_field_overrides':[(k,v) for k,v in ov['by_field'].items() if int(k,16)==FIELD]}
 if any(lookup.values()):raise ValueError('unexpected observed primary/field resolution')
 report={'scope':'saved flags-script-positive state plus separately hashed current V7 namespace, not candidate placement or live resolution','candidate_installed':False,
  'candidate_object_sha256':prior['candidate_object_sha256'],'prior_finite_ownership_sha256':sha(O/'psa-weak-ownership.json'),
  'saved_build_summary_sha256':sha(summary),'saved_units_sha256':sha(units),'saved_phase0_sha256':sha(scratch/'dv1_phase0.pkl'),'saved_placed_sha256':sha(scratch/'dv1_placed.pkl'),
  'current_v7_reloc_log_sha256':sha(RN/'build-v7/relocs_v7.tsv.gz'),'current_icf_sha256':sha(icf),'current_overlay_sha256':sha(overlay),'lookup':lookup,
  'precedence':{'v7_direct':'unit function map; unique global function; local placed section; unit symbol; unique global symbol; embedded-address heuristic; verified EH; imports',
                'v7_wrappers':'EH bindings can override; ICF applies when direct unresolved; field overlay then unit/global name overlay can override only under wrapper conditions',
                'data_v1':'phase0 resolved result first, then local placed section, unique placed global, unique V7 name; no generic weak fallback'},
  'contributions':'assemble_v7 consumes serialized contribution and EH piece records; deleted contribution COFFs are not asserted to be live final symbol providers',
  'limitations':['saved build has no candidate PSA primary relocation and weak mode disabled','current V7 namespace hashes are current files, not proven archived values of saved run','old provider closure is d569 and candidate not included','fresh candidate production namespace, placement, strong-primary precedence and final provider closure must be re-proved','no generic SEARCH_LIBRARY or live alias enabled']}
 OUT.write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({'output':str(OUT),'sha256':sha(OUT),'phase0_units':len(phase['res']),'placed_sections':len(st.SEC)}))
if __name__=='__main__':main()
