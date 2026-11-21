"""Derive strict TESForm recipe bindings from archived and actual production COFF."""
import collections,copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';OUT=M/'out/phase2-tesform-binding-repair-v2';sys.path[:0]=[str(F/'tools'),str(RN),str(RN/'build-v7'),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths,sgmap_w2,tescontainer_install
U=F/'build/units.json';OLD=RN/'pinned-build/obj_v3.bak-20261116/0998.obj';CUR=RN/'pinned-build/obj_v3/0998.obj';SIDE=RN/'build-v7/sg_sidecar_w2.json';SRC=F/'src/fallout_shared/tesform.cpp'
PIN={'units':'e883ac21f25808a7ebba172006e09ae803ae640bf12d389ad2c10641ddba1576','old_obj':'6e02e67f973a678bb7966b478eb224018e9a44b7e4f59f8db5b7cb4db03f7998','current_obj':'f2d60b88ed1be141c462242f5115fe47ab1c71367814c13b21b4e7107011234b','sidecar':'0218102fa6b18bba2c6f2663d9e478723cf49aa414def3f0f92829086020980c','source':'bb91ab9edc74a6606af5706cc5d4c6a5bcc39482ba02dcf787c5dcb785b65164','reference':'df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7'}
NAMES={'$SG8862','$SG8864','$SG8870','$SG9112','$SG8656','$SG8682'};PTR='?PTR_01187008@@3DA'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 inputs={k:Path(p).read_bytes() for k,p in [('units',U),('old_obj',OLD),('current_obj',CUR),('sidecar',SIDE),('source',SRC),('reference',paths.REF_IMAGE)]}
 for k,v in inputs.items():
  if sha(v)!=PIN[k]:raise ValueError('input changed '+k)
 doc=json.loads(inputs['units']);unit=doc['units'][998];old=Coff(str(OLD));cur=Coff(str(CUR));pe=Pe(paths.REF_IMAGE);base=compare(old,pe,unit)
 if len(base)!=128 or any(x['verdict']!='match' for x in base):raise ValueError('archived production strict reference not 128/128')
 side=json.loads(inputs['sidecar'])['998'];remap=sgmap_w2.remap(cur,unit['symbols'],side);index=collections.defaultdict(list)
 for _,name,content in sgmap_w2.sg_labels(old):index[content.split(b'\0',1)[0]].append(name)
 facts=[];changes={};currentlabels={name:content for _,name,content in sgmap_w2.sg_labels(cur)}
 for name in sorted(NAMES):
  content=currentlabels[name];value=content.split(b'\0',1)[0];oldnames=index[value]
  if len(oldnames)!=1:raise ValueError('nonunique prior string content '+name)
  prior=oldnames[0]
  if prior not in unit['symbols'] or name not in remap or unit['symbols'][prior]!=remap[name]:raise ValueError('source binding and sidecar conflict '+name)
  binding=remap[name];address=int(binding,16);sym=cur.named(name);sec=cur.sections[sym['section']]
  if sec['name']!='.rdata' or sec['relocs'] or pe.read(address,len(value)+1)!=value+b'\0':raise ValueError('pool/reference disagreement '+name)
  changes[name]=binding;facts.append({'production_label':name,'prior_label':prior,'source_bound_va':binding,'pool_offset':sym['value'],'pool_size':len(sec['data']),'pool_sha256':sha(sec['data']),'string_length_with_nul':len(value)+1,'string_sha256':sha(value+b'\0'),'sidecar_agrees':True,'reference_string_agrees':True})
 f=next(x for x in unit['functions'] if x['address']=='0x00485530');previous,oldrel=relocated(old,f['symbol'],f['size'],{});now,newrel=relocated(cur,f['symbol'],f['size'],{});offset=0x38
 rr=[r for r in newrel if r[0]==offset]
 if len(rr)!=1 or rr[0][1]!=6 or rr[0][2]!=PTR or rr[0][3]!=0 or any(r[0]==offset for r in oldrel):raise ValueError('unexpected pointer relocation shape')
 a=int.from_bytes(previous[offset:offset+4],'little');b=int.from_bytes(pe.read(int(f['address'],16)+offset,4),'little')
 if a!=b:raise ValueError('archived pointer immediate differs from original')
 changes[PTR]='0x%08x'%a;candidate=copy.deepcopy(unit)
 for k,v in changes.items():candidate['symbols'][k]=v
 checks=compare(cur,pe,candidate)
 if len(checks)!=128 or any(x['verdict']!='match' for x in checks):raise ValueError('production strict reference is not 128/128')
 raw=tescontainer_install.replace_unit(inputs['units'],998,candidate);generated=json.loads(raw)
 if any(doc[k]!=generated[k] for k in doc if k!='units') or [i for i,(x,y) in enumerate(zip(doc['units'],generated['units'])) if x!=y]!=[998]:raise ValueError('recipe scope changed')
 before=unit['symbols'];after=candidate['symbols']
 if {k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)}!=set(changes):raise ValueError('unexpected symbol edits')
 OUT.mkdir(exist_ok=False);(OUT/'units.original').write_bytes(inputs['units']);(OUT/'units.generated').write_bytes(raw)
 manifest={'schema_version':1,'scope':'recipe-only proposal; all other units, attributes, and symbol entries preserved','inputs_sha256':PIN,'generated_units_sha256':sha(raw),'function_count':128,'archived_reference_matches':128,'production_reference_matches':128,'string_facts':facts,'pointer_fact':{'function':f['address'],'field_offset':offset,'production_symbol':PTR,'archived_unrelocated_immediate':changes[PTR],'reference_field_matches':True,'production_relocation_kind':'DIR32','production_addend':0},'symbol_edits':[{'symbol':k,'before':before.get(k),'after':v} for k,v in sorted(changes.items())],'status':'private; production object, sidecar and source provenance pinned; integration and full build still required'}
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps({'symbol_edits':len(changes),'matches':128,'generated_units_sha256':sha(raw)}))
if __name__=='__main__':main()

