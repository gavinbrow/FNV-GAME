"""Stage source-backed implicit PSA method ownership transfer; never apply."""
import copy,hashlib,json,sys
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out';D=O/'phase2-bgsbodypart-native-destructor-rebase6757';P=O/'phase2-psa-owner-transfer';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths,tescontainer_install
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';DTOR='??1TESModelPSA@@UAE@XZ';WRAPPER='??_GTESModelPSA@@UAEPAXI@Z';OLD='?FUN_0051b950@FUN_0051b950_shell@@QAEXXZ';OLDW='?FUN_005e3c30@BGSTextureModel@@QAEPAXI@Z'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if P.exists():raise FileExistsError('preserve existing proposal')
 recipe=F/'build/units.json';raw=recipe.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=BASE:raise ValueError('recipe changed')
 doc=json.loads(raw);units=doc['units'];a=copy.deepcopy(units[620]);b=copy.deepcopy(units[2909]);fixture=json.loads((D/'manifest.json').read_text());compile=json.loads((D/'lane-compile.json').read_text());record=next(x for x in compile['outcomes'] if x['unit']==620 and x['tag']=='mirror');obj=D/'0620.mirror.obj';owner=O/'phase2-bfc-cohort-production-archive/2909.obj'
 if record['rc'] or record['object_sha256']!=sha(obj) or fixture['semantic_rebase']['new_units_sha256']!=BASE:raise ValueError('candidate proof differs')
 for name,digest in fixture['outputs'].items():
  if sha(D/name)!=digest:raise ValueError('candidate output changed '+name)
 hits=[]
 for address,size in ((0x51b950,19),(0x5e3c30,44)):
  matches=[(i,f) for i,u in enumerate(units) for f in u['functions'] if int(f['address'],16)<address+size and address<int(f['address'],16)+f['size']]
  if len(matches)!=1:raise ValueError('overlapping function owner')
  hits.append(matches[0])
 if hits[0][0]!=2909 or hits[0][1]['symbol']!=OLD or hits[0][1]['size']!=19 or hits[1][0]!=620 or hits[1][1]['symbol']!=OLDW or hits[1][1]['size']!=44:raise ValueError('owner scope changed')
 for name,ownerid in ((OLD,2909),(OLDW,620)):
  refs=[i for i,u in enumerate(units) if name in u.get('symbols',{}) or any(name in f.get('fold_aliases',[]) or name==f['symbol'] for f in u['functions'])]
  if refs!=[ownerid]:raise ValueError('legacy name has additional recipe consumer')
 c=Coff(str(obj));oc=Coff(str(owner));native,nr=relocated(c,DTOR,19,{'??1TESModel@@UAE@XZ':'??1TESModel@@QAE@XZ'});previous,pr=relocated(oc,OLD,19,{})
 if native!=previous or nr!=pr:raise ValueError('native destructor differs from 2909 owner')
 native,nr=relocated(c,WRAPPER,44,{DTOR:'??1BGSTextureModel@@UAE@XZ'});previous,pr=relocated(c,OLDW,44,{})
 if native!=previous or nr!=pr:raise ValueError('native deleting wrapper differs from source surrogate')
 for f in a['functions']:
  changes={'0x005e3be0':'??0TESModelPSA@@QAE@XZ','0x005e3c30':WRAPPER,'0x005e3c60':'??1BGSBodyPart@@QAE@XZ','0x005e45e0':'?QueueResourceLoad@BGSBodyPart@@UAEXW4IO_TASK_PRIORITY@@PAVQueuedFile@@@Z'}
  if f['address'] in changes:f['symbol']=changes[f['address']]
 moved=next(f for f in b['functions'] if f['address']=='0x0051b950');b['functions'].remove(moved);a['functions'].append({'address':'0x0051b950','symbol':DTOR,'size':19});a['symbols'].update({'??_7TESModelPSA@@6B@':'0x0104540c','??1TESModel@@UAE@XZ':'0x00489070','?FUN_005e3d50@BGSBodyPart@@QAEXXZ':'0x005e3d50','__ehhandler$??1BGSBodyPart@@QAE@XZ':'0x00ef9e3d',DTOR:'0x0051b950'})
 new=tescontainer_install.replace_unit(raw,620,a);new=tescontainer_install.replace_unit(new,2909,b);after=json.loads(new)
 if [i for i,(x,y) in enumerate(zip(units,after['units'])) if x!=y]!=[620,2909] or any(doc[k]!=after[k] for k in doc if k!='units'):raise ValueError('out of scope changes')
 spans=lambda us:Counter((f['address'],f['size']) for u in us for f in u['functions'])
 if spans(units)!=spans(after['units']):raise ValueError('global function span union changed')
 pe=Pe(paths.REF_IMAGE);ar=compare(c,pe,a);br=compare(oc,pe,b)
 if len(ar)!=16 or any(x['verdict']!='match' for x in ar) or len(br)!=44 or any(x['verdict']!='match' for x in br):raise ValueError('candidate owner strict function check failed')
 P.mkdir();(P/'units.original').write_bytes(raw);(P/'units.generated').write_bytes(new)
 for name,digest in fixture['outputs'].items():
  path=P/'bgs-candidate'/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((D/name).read_bytes())
 meta={'base_recipe_sha256':BASE,'candidate_recipe_sha256':sha(P/'units.generated'),'candidate_bgs_manifest_sha256':sha(D/'manifest.json'),'candidate_compiler_sha256':sha(D/'lane-compile.json'),'candidate_620_object_sha256':sha(obj),'old_2909_object_sha256':sha(owner),'eh_owner_review_sha256':sha(D/'independent-eh-owner-review.json'),'candidate_graph_sha256':sha(D/'graph-psa.json'),'source_owner':'unit 620 naturally emits implicit PSA destructor through a BGSBodyPart member','owner_transfer':{'address':'0x0051b950','size':19,'from_unit':2909,'old_symbol':OLD,'to_unit':620,'new_symbol':DTOR},'wrapper_remap':{'address':'0x005e3c30','size':44,'unit':620,'old_symbol':OLDW,'new_symbol':WRAPPER,'full_bytes_and_relocations_equal':True,'legacy_recipe_consumers':[620]},'unchanged_function_address_size_multiset':True,'strict_function_results':{'candidate_620':16,'archived_2909_remaining':44},'compiler_flags':{'620':units[620]['flags'],'2909':units[2909]['flags']},'legacy_generated_bodies':'both source surrogate bodies remain generated but their old recipe entries become unplaced; no source removed','limitations':['private source payload and recipe only; no live edits or compile','actual production code/EH, literal pools and source closures require fresh complete proof','weak vector-deleting symbol fallback and final COMDAT ownership require production/link review','RTTI/vtable ABI, full image and runtime remain separate']}
 (P/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'candidate_620_strict':16,'remaining_2909_strict':44,'recipe_sha256':sha(P/'units.generated')}))
if __name__=='__main__':main()
