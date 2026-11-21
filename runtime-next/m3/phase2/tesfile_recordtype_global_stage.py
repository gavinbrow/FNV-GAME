"""Replace three false string dereferences with the source-supported record-type global."""
import copy,hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out/phase2-tesfile-recordtype-global';ARCH=M/'out/phase2-nimem-kind-production-archive';sys.path[:0]=[str(F/'tools'),str(RN),str(H)];import baseformcomponent_core_stage as core,tescontainer_install
from compare import Coff,Pe
from rtti_hkp_viewer_compare import relocated
import paths
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';PRE='5cbfa7a8145984a47bfaea1966f8f07b154917203ea925f60b58429a43a532f6';SOURCE='src/fallout_shared/tesfile.cpp';SYM='?DAT_011873c8@@3IA'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve existing proposal')
 raw=(F/'build/units.json').read_bytes();doc=json.loads(raw);units=doc['units'];u=units[995];old=(F/SOURCE).read_bytes()
 if sha(raw)!=BASE or sha(old)!=PRE or u['source']!=SOURCE or len(u['functions'])!=87 or units[587]['symbols'].get(SYM)!='0x011873c8':raise ValueError('source/recipe evidence differs')
 ap=ARCH/'0995.obj';archive=json.loads((ARCH/'manifest.json').read_text());record=next(x for x in archive['objects'] if x['unit']==995)
 if sha(ap.read_bytes())!=record['sha256'] or archive['recipe_sha256']!=BASE:raise ValueError('archive differs')
 c=Coff(str(ap));pe=Pe(paths.REF_IMAGE);facts=[]
 uses=[(section['name'],offset,c.symbols[j]['name']) for section in c.sections if section for offset,j,kind in section['relocs'] if c.symbols[j]['name'] in ('$SG7025','$SG8028','$SG8627')]
 if sorted(uses)!=[('.text',72,'$SG7025'),('.text',159,'$SG8028')]:raise ValueError('stale SG labels have other archived object users')
 for addr,offset,label in (('0x00472150',72,'$SG7025'),('0x004721d0',49,'$SG8632'),('0x00472bc0',159,'$SG8028')):
  f=next(x for x in u['functions'] if x['address']==addr);_,rr=relocated(c,f['symbol'],f['size'],{});q=[x for x in rr if x[0]==offset]
  if len(q)!=1 or q[0][1]!=6 or q[0][2]!=label or struct.unpack('<I',pe.read(int(addr,16)+offset,4))[0]!=0x11873c8:raise ValueError('original field evidence differs')
  sym=c.named(label);section=c.sections[sym['section']];end=section['data'].find(b'\0',sym['value']);data=section['data'][sym['value']:end+1]
  if data!=b'TOFTQ\0' or pe.read(0x11873c8,len(data))==data:raise ValueError('literal/global distinction changed')
  facts.append({'function':addr,'field_offset':offset,'old_label':label,'original_global':'0x011873c8','literal_sha256':sha(data),'reference_initial_sha256':sha(pe.read(0x11873c8,len(data)))})
 source=old;nl=b'\r\n' if b'\r\n' in source else b'\n';anchor=b'extern unsigned int kGroupFormType;'
 if source.count(anchor)<1 or b'extern unsigned int DAT_011873c8;' in source:raise ValueError('source declaration changed')
 source=source.replace(anchor,anchor+nl+b'extern unsigned int DAT_011873c8;',1)
 for find,count in ((b'*reinterpret_cast<const unsigned int*>("TOFTQ")',1),(b'*(unsigned int*)"TOFTQ"',2)):
  if source.count(find)!=count:raise ValueError('source literal count differs')
  source=source.replace(find,b'DAT_011873c8')
 candidate=copy.deepcopy(u);candidate['symbols'][SYM]='0x011873c8'
 for name in ('$SG7025','$SG8028','$SG8627'):
  if candidate['symbols'].pop(name,None)!='0x011873c8':raise ValueError('stale literal alias differs')
 changed=tescontainer_install.replace_unit(raw,995,candidate);newdoc=json.loads(changed)
 if [i for i,(a,b) in enumerate(zip(units,newdoc['units'])) if a!=b]!=[995] or any(doc[k]!=newdoc[k] for k in doc if k!='units') or candidate['functions']!=u['functions']:raise ValueError('recipe scope differs')
 before=core.walk(F,SOURCE,{});after=core.walk(F,SOURCE,{SOURCE:source})
 if set(before['files'])!=set(after['files']):raise ValueError('include graph changed')
 O.mkdir();(O/'source.original').write_bytes(old);(O/'source.generated').write_bytes(source);(O/'units.original').write_bytes(raw);(O/'units.generated').write_bytes(changed)
 for tag,graph in (('original',before),('candidate',after)):
  for rel,digest in graph['files'].items():
   data=source if tag=='candidate' and rel==SOURCE else (F/rel).read_bytes()
   if sha(data)!=digest:raise ValueError('source input changed')
   p=O/tag/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 mm={'schema_version':1,'source':SOURCE,'units_sha256':BASE,'unit':995,'original_inputs':before['files'],'original':before,'candidate':after,'production_include_order':['/I<mirror>/include'],'limits':['private global-vs-literal source hypothesis']};(O/'mirror-manifest.json').write_text(json.dumps(mm,indent=2))
 meta={'base_recipe_sha256':BASE,'candidate_recipe_sha256':sha(changed),'source_before_sha256':sha(old),'source_after_sha256':sha(source),'archived_object_sha256':sha(ap.read_bytes()),'source_other_unit':587,'source_other_unit_path':units[587]['source'],'source_other_unit_sha256':sha((F/units[587]['source']).read_bytes()),'reference_sha256':sha(Path(paths.REF_IMAGE).read_bytes()),'original_fields':facts,'removed_stale_aliases':['$SG7025','$SG8028','$SG8627'],'added_binding':{SYM:'0x011873c8'},'function_count':87,'recipe_eh_tails':len(u.get('eh_tails',[])),'scope':'three record type tests use a writable global, not bytes of a string literal','limits':['global startup initialization and runtime value remain unproved','all 87 source functions, 4 EH tails, other SG pool renumbering and actual production placement require proof','no source/recipe edits or compiler execution']}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'unit':995,'functions':87,'original_global_fields':3,'candidate_recipe_sha256':sha(changed)}))
if __name__=='__main__':main()
