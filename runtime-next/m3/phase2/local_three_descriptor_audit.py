"""Inspect three descriptor candidates using archived phase0 and placement state."""
import hashlib,json,pickle,struct,sys
from pathlib import Path
M=Path(__file__).resolve().parent.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';E=R/'phase2-native-source-positive/evidence';OUT=R/'phase2-local-economy-20261119/reuse-placement/three-descriptor-audit.json';sys.path[:0]=[str(RN/'data-v1'),str(F/'tools'),str(RN)]
import place,paths
from compare import Pe
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve existing audit')
 p0=E/'data-v1-scratch/dv1_phase0.pkl';pp=E/'data-v1-scratch/dv1_placed.pkl';symbolic=E/'data-v3-symbolic.json';pieces=E/'dv1_pieces.json';lib=E/'library_candidates.json';recipe=E/'units.json'
 state=pickle.loads(pp.read_bytes());phase=pickle.loads(p0.read_bytes())['res'];fields=json.loads(symbolic.read_text());selected=json.loads(pieces.read_text())['pieces'];libraries=json.loads(lib.read_text())['candidates'];units=json.loads(recipe.read_text())['units'];pe=Pe(paths.REF_IMAGE);base=fields['sections']['.data']['va'];out=[]
 for va,size in ((0x01186744,44),(0x0119dc4c,48),(0x011ac8e0,29)):
  hits=[(k,t) for k,(a,t) in state.placed.items() if a==va and len(state.SEC[k]['data'])==size]
  if len(hits)!=1:raise ValueError('placed state identity ambiguous '+hex(va))
  key,tier=hits[0];s=state.SEC[key];res,origin=state.resolve(s);reference=pe.read(va,size);data=bytearray(s['data']);masked=bytearray(data);refmasked=bytearray(reference)
  for off,kind,*_ in s['relocs']:
   if kind!=6:raise ValueError('unexpected relocation')
   masked[off:off+4]=b'\0'*4;refmasked[off:off+4]=b'\0'*4
   if off in res:struct.pack_into('<I',data,off,res[off])
  near=[{'va':base+x[1],'evidence':x[4],'origin':x[5],'target':x[2]} for x in fields['fields'] if x[0]=='.data' and va-3<=base+x[1]<va+size]
  value_rules=[x for x in near if x['evidence']=='value-rule'];chosen=[x for x in selected if x['va']<va+size and va<x['va']+x['size']];ids=s['units'];library_evidence=[{'unit':x['unit'],'library':x['library'],'member':x['member'],'archive_sha256':x['archive_sha256']} for x in libraries if x['unit'] in ids];library_evidence=list({(x['unit'],x['library'],x['member']):x for x in library_evidence}.values())
  if len(ids)==1 and ids[0]<100000:
   u=ids[0];refs=[(unit,sec) for (unit,sec),k in state.KEYOF.items() if k==key];psec=next(x for x in phase[u]['secs'] if x['k']==refs[0][1]);assert psec['defs']==s['defs'];block='value-rule-field-inside-or-adjacent' if value_rules else 'no blocker established by bounded checks'
   origin_info={'unit':u,'source':units[u]['source'],'coff_section_index':refs[0][1],'phase0_present':True}
  else:
   origin_info={'pseudo_units':ids,'section_indices':[(unit,sec) for (unit,sec),k in state.KEYOF.items() if k==key],'phase0_present':False,'archived_library_member_evidence':library_evidence};block='library pseudo-units excluded by default unit selector; current opt-in library selector additionally rejects relocatable sections; type_info relocation unresolved in archived state'
  out.append({'va':'0x%08x'%va,'size':size,'coff':{'kind':s['kind'],'section':s['name'],'flags':'0x%08x'%s['flags'],'definitions':[d[0] for d in s['defs']],'relocations':[{'offset':x[0],'kind':x[1],'symbol':x[2],'resolved':('0x%08x'%res[x[0]]) if x[0] in res else None,'resolution_source':origin.get(x[0])} for x in s['relocs']],'origin':origin_info},'archived_placement':{'tier':tier,'selected_piece_overlaps':len(chosen)},'reference_comparison':{'all_nonrelocation_bytes_equal':masked==refmasked,'all_relocations_resolved':len(res)==len(s['relocs']),'resolved_full_bytes_equal':len(res)==len(s['relocs']) and bytes(data)==reference},'value_rule_fields':value_rules,'original_reloc_fields':[x for x in near if x['evidence']=='orig-reloc'],'primary_blocker':block,'limits':['no selector mutation, source edit or new alias','source/object/relocation ownership remains required','placement was archived, not a claim about an active rebuild']})
 OUT.write_text(json.dumps({'inputs_sha256':{str(p.relative_to(R)):sha(p) for p in (p0,pp,symbolic,pieces,lib,recipe)},'reference_sha256':sha(Path(paths.REF_IMAGE)),'records':out},indent=2));print(json.dumps([{'va':x['va'],'blocker':x['primary_blocker'],'masked_equal':x['reference_comparison']['all_nonrelocation_bytes_equal']} for x in out]));print('sha256',sha(OUT))
if __name__=='__main__':main()
