"""Seal an opt-in BGSE weak-primary resolution proposal against current V7/M3 inputs."""
import hashlib,json,pickle,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';sys.path[:0]=[str(F/'tools'),str(RN),str(RN/'data-v1'),str(RN/'pinned-build'),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import coff_weak,place,paths
PRIMARY='??_EBGSEncounterZone@@UAEPAXI@Z';FALLBACK='??_GBGSEncounterZone@@UAEPAXI@Z';OWNER='?Destroy@FUN_00525cb0_shell@@QAEPAU1@I@Z';VA=0x525cb0;SIZE=44
OUT=M/'out/phase2-bgse-effective-weak-proof.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('refusing overwrite')
 unitsfile=F/'build/units.json';units=json.loads(unitsfile.read_bytes())['units'];unit=units[2];obj=RN/'pinned-build/obj_v3/0002.obj';coff=Coff(str(obj));provider=M/'out/phase2-vtable-provider-closure.json';prov=json.loads(provider.read_bytes());entry=next(x for x in prov['objects'] if x['kind']=='recipe' and x['id']=='2')
 if entry['sha256']!=sha(obj) or sha(unitsfile) not in prov['manifests_sha256'].values() or prov['strong_definitions'][PRIMARY]:raise ValueError('provider snapshot mismatch')
 if any(x['kind'] in ('recipe','eh_variant','m3_generated') for x in prov['missing']) or prov['excluded_recipe'] or prov['scan_errors']:raise ValueError('incomplete relevant object cohort')
 p=[(i,x) for i,x in coff.symbols.items() if x['name']==PRIMARY and x['storage']==105]
 if len(p)!=1:raise ValueError('primary not unique weak external')
 idx,weak=p[0];tag=coff_weak.fallback_index(coff,idx,allow_unsupported=True);symptr=struct.unpack_from('<I',coff.data,8)[0];characteristic=struct.unpack_from('<I',coff.data,symptr+18*(idx+1)+4)[0]
 if characteristic!=2 or coff.symbols[tag]['name']!=FALLBACK:raise ValueError('weak metadata differs')
 defs=[x for x in coff.by_name[FALLBACK] if x['storage']==2 and x['section']>0]
 if len(defs)!=1:raise ValueError('fallback definition ambiguous')
 owners=[(i,f) for i,u in enumerate(units) for f in u['functions'] if int(f['address'],16)<VA+SIZE and VA<int(f['address'],16)+f['size']]
 if len(owners)!=1 or owners[0][0]!=2 or owners[0][1]['symbol']!=OWNER or int(owners[0][1]['address'],16)!=VA or owners[0][1]['size']!=SIZE:raise ValueError('owner ambiguous')
 x,xr=relocated(coff,OWNER,SIZE,{});y,yr=relocated(coff,FALLBACK,SIZE,{'??1BGSEncounterZone@@UAE@XZ':'?FUN_00525ce0@FUN_00525cb0_shell@@QAEXXZ'})
 if x!=y or xr!=yr or len(xr)!=2 or unit['symbols'].get('?FUN_00525ce0@FUN_00525cb0_shell@@QAEXXZ')!='0x00525ce0' or unit['symbols'].get('??3@YAXPAX@Z')!='0x00401030':raise ValueError('fallback body/normal callees mismatch')
 sym=defs[0];sec=coff.sections[sym['section']];nxt=[s['value'] for s in coff.symbols.values() if s['section']==sym['section'] and s['type']&0x20 and s['value']>sym['value'] and not s['name'].startswith('__catch$')];end=min(nxt) if nxt else len(sec['data'])
 if end-sym['value']<SIZE or any(v not in (0xcc,0x90) for v in sec['data'][sym['value']+SIZE:end]):raise ValueError('fallback extent differs')
 import copy
 spec=copy.deepcopy(unit);spec['functions']=[dict(owners[0][1],symbol=FALLBACK)];spec['symbols']['??1BGSEncounterZone@@UAE@XZ']='0x00525ce0';rows=compare(coff,Pe(paths.REF_IMAGE),spec)
 if len(rows)!=1 or rows[0]['verdict']!='match' or len(rows[0]['relocations'])!=2 or not all(r['match'] for r in rows[0]['relocations']):raise ValueError('fallback reference comparator failed')
 bindings=[]
 for i,u in enumerate(units):
  if PRIMARY in u.get('symbols',{}):bindings.append((i,'symbol',u['symbols'][PRIMARY]))
  for f in u['functions']:
   if PRIMARY==f['symbol'] or PRIMARY in f.get('fold_aliases',[]):bindings.append((i,'function',f['address']))
 if bindings:raise ValueError('primary recipe mapping exists')
 icf=RN/'build-v7/icf_map.json';imap=json.loads(icf.read_bytes());overlay=RN/'reloc-v7/binding_overlay.json';ov=json.loads(overlay.read_bytes());field=0x0102cbcc
 if PRIMARY in imap or PRIMARY in ov['global_name'] or any(PRIMARY in x for x in ov['by_unit_name'].values()) or any(int(k,16)==field for k in ov['by_field']):raise ValueError('primary/field override exists')
 pp=M/'out/phase2-native-methods-positive/evidence/data-v1-scratch/dv1_placed.pkl';summary=M/'out/phase2-native-methods-positive/build-summary.json';expected=json.loads(summary.read_bytes())['provenance']['data_v1_scratch_sha256']['dv1_placed.pkl']
 if sha(pp)!=expected:raise ValueError('archived placement digest mismatch')
 st=pickle.loads(pp.read_bytes());sites=[]
 for k,s in st.SEC.items():
  for r in s['relocs']:
   if r[2]==PRIMARY:
    pl=st.placed.get(k);sites.append({'units':s['units'],'offset':r[0],'section':r[3],'storage':r[5],'phase0_source':r[7],'phase0_value':r[8],'placed_va':pl[0] if pl else None,'field_va':pl[0]+r[0] if pl else None})
 if len(sites)!=1 or sites[0]['field_va']!=field or sites[0]['phase0_source'] is not None or st.gdef.get(PRIMARY) is not None or place.v7map.get(PRIMARY) is not None:raise ValueError('M3 lookup closure differs')
 out={'scope':'candidate-specific research proposal for effective current M3/V7 resolver, not MSVC linker semantics; no runtime activation','object_sha256':sha(obj),'recipe_sha256':sha(unitsfile),'provider_snapshot_sha256':sha(provider),'placed_pickle_sha256':sha(pp),'v7_reloc_log_sha256':sha(RN/'build-v7/relocs_v7.tsv.gz'),'icf_sha256':sha(icf),'overlay_sha256':sha(overlay),'primary':PRIMARY,'weak_characteristic':characteristic,'fallback':FALLBACK,'owner':OWNER,'owner_address':hex(VA),'owner_size':SIZE,'unique_owner':True,'body_and_reloc_equal':True,'strict_reference_match':True,'placed_sites':sites,'recipe_primary_bindings':bindings,'placed_global_definition':None,'v7_name_map':None,'icf_primary':None,'name_overlay':None,'field_overlay':None,'limitations':['provider snapshot lacks 1087 deleted contribution COFFs; final V7 consumes serialized pieces, not their symbol tables','explicit resolution design must preserve normal primary/field/ICF precedence and detect changed lookup namespace','snapshot evidence is not proof for future builds or other classes','full vtable/class layout, final image ownership and runtime remain separate']}
 OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'weak':characteristic,'body':True,'sites':len(sites),'field':hex(field)}))
if __name__=='__main__':main()
