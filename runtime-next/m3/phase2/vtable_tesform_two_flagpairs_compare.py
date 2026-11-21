"""Compare paired flag/setter mirrors under the installed typed recipe."""
import copy,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths,class_metadata_compare as cm,rtti_mirror_compare as mirror
T=M/'out/phase2-tesform-two-flagpairs-mirror';B=M/'out/phase2-bgs-two-flagpairs-mirror';META=M/'out/phase2-tesform-two-flagpairs-setters/manifest.json';U=F/'build/units.json';C=M/'out/phase2-class-census/census-d569.json';OUT=M/'out/phase2-two-flagpairs-report.json'; D='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def objects(path,idx):
 man=path/'mirror-manifest.json';m=json.loads(man.read_bytes());run=json.loads((path/'compile-result.json').read_bytes())
 if m['units_sha256']!=D or run['unit_index']!=idx or run['mirror_manifest_sha256']!=sha(man):raise ValueError('compiled manifest mismatch')
 o={}
 for r in run['outcomes']:
  p=path/(r['tag']+'.obj')
  if r['rc'] or r.get('trace_valid') is not True or sha(p)!=r['object_sha256']:raise ValueError('object/trace mismatch')
  o[r['tag']]=Coff(str(p))
 if set(o)!={'original','candidate'}:raise ValueError('objects incomplete')
 return o

def main():
 if OUT.exists():raise FileExistsError('report exists')
 if sha(U)!=D:raise ValueError('recipe changed')
 meta=json.loads(META.read_bytes());units=json.loads(U.read_bytes())['units'];tu=units[998];bu=units[2];t=objects(T,998);b=objects(B,2);pe=Pe(paths.REF_IMAGE);census=json.loads(C.read_bytes())
 if census['inputs']['units_sha256']!=D:raise ValueError('census stale')
 pairs=[meta['getter'],meta['getter2']];rename={x['source_symbol']:x['canonical'] for x in pairs};normal={v:k for k,v in rename.items()};mapped=copy.deepcopy(tu);literal={};facts=[]
 for f in tu['functions']:
  a,ar=relocated(t['original'],f['symbol'],f['size'],{});z,zr=relocated(t['candidate'],rename.get(f['symbol'],f['symbol']),f['size'],normal)
  if a!=z or len(ar)!=len(zr):raise ValueError('TES raw/reloc count mismatch '+f['address'])
  for x,y in zip(ar,zr):
   if x==y:continue
   if (x[0],x[1],x[3])!=(y[0],y[1],y[3]) or not all(re.fullmatch(r'\$SG\d+',q[2]) for q in (x,y)):raise ValueError('nonliteral relocation mismatch '+f['address'])
   p=t['original'].named(x[2]);q=t['candidate'].named(y[2]);ps=t['original'].sections[p['section']];qs=t['candidate'].sections[q['section']]
   if p['value']!=q['value'] or ps['name']!='.rdata' or qs['name']!='.rdata' or ps['data']!=qs['data'] or ps['relocs'] or qs['relocs'] or x[2] not in tu['symbols']:raise ValueError('literal pool mismatch')
   value=tu['symbols'][x[2]]
   if y[2] in literal and literal[y[2]]!=value:raise ValueError('literal collision')
   literal[y[2]]=value;normal[y[2]]=x[2];facts.append({'function':f['address'],'offset':x[0],'before':x[2],'after':y[2],'binding':value,'pool_offset':p['value'],'pool_sha256':hashlib.sha256(ps['data']).hexdigest()})
 for f in mapped['functions']:
  for g in pairs:
   if f['symbol']==g['source_symbol']:
    if f['address']!=g['address'] or f['size']!=g['size'] or f.get('fold_aliases'):raise ValueError('getter owner mismatch')
    f['symbol']=g['canonical'];f['fold_aliases']=[g['fold_alias']]
 mapped['symbols'].update(literal)
 for f in tu['functions']:
  a,ar=relocated(t['original'],f['symbol'],f['size'],{});z,zr=relocated(t['candidate'],rename.get(f['symbol'],f['symbol']),f['size'],normal)
  if a!=z or ar!=zr:raise ValueError('TES normalized mismatch '+f['address'])
 foldfacts=[]
 for g in pairs:
  owners=[(i,f) for i,u in enumerate(units) for f in u['functions'] if int(f['address'],16)<int(g['address'],16)+g['size'] and int(g['address'],16)<int(f['address'],16)+f['size']]
  if len(owners)!=1 or owners[0][0]!=998 or owners[0][1]['symbol']!=g['source_symbol']:raise ValueError('overlapping fold owner')
  bodies=[]
  for name in (g['canonical'],g['fold_alias']):
   data,rel=relocated(t['candidate'],name,g['size'],{})
   if rel or data!=pe.read(int(g['address'],16),g['size']):raise ValueError('getter body mismatch')
   sym=t['candidate'].named(name);sec=t['candidate'].sections[sym['section']];start=sym['value'];nexts=[x['value'] for x in t['candidate'].symbols.values() if x['section']==sym['section'] and x['type']&0x20 and x['value']>start and not x['name'].startswith('__catch$')];end=min(nexts) if nexts else len(sec['data'])
   if end-start<g['size'] or any(x not in (0xcc,0x90) for x in sec['data'][start+g['size']:end]):raise ValueError('getter extent mismatch')
   bodies.append(name)
  foldfacts.append({'address':g['address'],'size':g['size'],'owner':g['source_symbol'],'symbols':bodies})
 for label,o,spec in [('TES original',t['original'],tu),('TES candidate',t['candidate'],mapped)]:
  rows=compare(o,pe,spec)
  if len(rows)!=128 or any(x['verdict']!='match' for x in rows):raise ValueError(label+' strict mismatch')
 for f in bu['functions']:
  a,ar=relocated(b['original'],f['symbol'],f['size'],{});z,zr=relocated(b['candidate'],f['symbol'],f['size'],{})
  if a!=z or ar!=zr:raise ValueError('BGSE function mismatch '+f['address'])
 diagnostic=copy.deepcopy(bu);diagnostic['symbols']['??1TESForm@@UAE@XZ']='0x00483630'
 for g in pairs:
  for n in (g['canonical'],g['fold_alias']):diagnostic['symbols'][n]=g['address']
 for s in meta['setters']:
  f=[f for f in tu['functions'] if f['address']==s['address']]
  if len(f)!=1 or s['method'] not in f[0]['symbol']:raise ValueError('setter source binding mismatch')
  diagnostic['symbols'][f[0]['symbol']]=s['address']
 for label,o in [('BGSE original',b['original']),('BGSE candidate',b['candidate'])]:
  rows=compare(o,pe,diagnostic)
  if len(rows)!=24 or any(x['verdict']!='match' for x in rows):raise ValueError(label+' strict mismatch')
 eh={}
 for label,obj in [('tes',t),('bgs',b)]:
  a=mirror.exception_sections(obj['original']);z=mirror.exception_sections(obj['candidate'])
  if a.keys()!=z.keys() or any(a[k]!=z[k] for k in a):raise ValueError('EH section mismatch '+label)
  eh[label]=len(a)
 graph=cm.compare_class(B/'candidate.obj',diagnostic,units,census,'.?AVBGSEncounterZone@@');tables=graph['tables']
 if len(tables)!=1 or not tables[0]['graph_fields_equal'] or tables[0]['emitted_slot_count']!=78:raise ValueError('graph mismatch')
 slots=tables[0]['slots'];checks=[x for x in slots if x['index'] in (38,39,40,41,42,43,51,52,53,54,55)]
 out={'scope':'private four generated getter bodies, two fold-owner proposals, three setter names; not global ODR proof','recipe_sha256':sha(U),'tes_obj_sha256':sha(T/'candidate.obj'),'bgs_obj_sha256':sha(B/'candidate.obj'),'functions':{'tes':128,'bgs':24},'literal_facts':facts,'folds':foldfacts,'eh_named_section_tails':eh,'graph':graph,'selected_slots':checks,'limitations':['all other TESForm class views and callers need ABI reconciliation','final fold placement and runtime behavior not proven']}
 OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'tes':128,'bgs':24,'folds':len(foldfacts),'eh':eh,'matched_slots':sum(x['match'] for x in slots),'selected_slots':checks}))
if __name__=='__main__':main()
