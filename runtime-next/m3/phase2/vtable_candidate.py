import hashlib,json,struct,gzip,sys
from pathlib import Path
H=Path(__file__).resolve().parent; RN=H.parent.parent; P=RN.parent
sys.path.insert(0,str(P/'fnv_decomp'/'tools'));sys.path.insert(0,str(H.parent))
from compare import Coff
import gen_m3 as G
E=H.parent/'out'/'batch8-promoted-default-verified'/'evidence'; obj=RN/'pinned-build'/'obj_v3'/'0001.obj'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
units=json.load(open(P/'fnv_decomp'/'build'/'units.json'))['units']; u=units[1]; name='??_7?$NiTPrimitiveArray@PAVBGSCameraPath@@@@6B@'; slot='??_E?$NiTPrimitiveArray@PAVBGSCameraPath@@@@UAEPAXI@Z'; c=Coff(str(obj)); sy=c.named(name); sec=c.sections[sy['section']]
assert sy['value']==4 and len(sec['data'])==8 and len(sec['relocs'])==2
rel=[]
for off,idx,k in sec['relocs']:
 sym=c.symbols[idx];v=struct.unpack('<I',G.refbytes(0x0103274c+off,4))[0]
 assert k==6 and 0x0103274c+off in G.ORIG_SET
 rel.append(dict(offset=off,kind=k,symbol=sym['name'],symbol_section=sym['section'],coff_addend=struct.unpack_from('<I',sec['data'],off)[0],reference_target='0x%08x'%v))
assert rel[1]['symbol']==slot and rel[1]['reference_target']=='0x0058bc90' and slot not in u['symbols']
assert not any(slot in x.get('symbols',{}) or any(f['symbol']==slot for f in x.get('functions',[])) for x in units)
placed=[line.strip() for line in gzip.open(RN/'data-v1'/'pieces.tsv.gz','rt') if line.startswith('0103274c\t')];assert '0103274c\t8\tV\tvtable' in placed
manifest=json.load(open(E/'m3_manifest.json'))['entries']; pieces=json.load(open(E/'dv1_pieces.json'))['pieces']
def covering(v):return [dict(va='0x%08x'%x['va'],size=x['size'],kind=x.get('kind'),source=source) for source,arr in [('m3',manifest),('dv1',pieces)] for x in arr if x['va']<=v<x['va']+x['size']]
assert all(not covering(x) for x in range(0x0103274c,0x01032754))
assert [r['offset'] for r in rel] == [0,4] and all(r['coff_addend']==0 for r in rel)
col=covering(0x0110ea28); assert any(x['source']=='dv1' and x['kind']=='rtti4' for x in col)
owner=[dict(unit=i,source=x['source'],function=f) for i,x in enumerate(units) for f in x.get('functions',[]) if int(f['address'],0)==0x0058bc90];assert len(owner)==1
result={'status':'proposed; vector/scalar deleting-destructor ABI identity and end-to-end build not established','unit':1,'source':u['source'],'class_declaration':'fnv_decomp/src/CameraPathManager.h:12','vftable_symbol':name,'object_section':sy['section'],'object_section_flags':'0x%08x'%sec['flags'],'object_bytes_hex':bytes(sec['data']).hex(),'object_sha256':sha(obj),'units_sha256':sha(P/'fnv_decomp'/'build'/'units.json'),'m3_manifest_sha256':sha(E/'m3_manifest.json'),'dv1_pieces_sha256':sha(E/'dv1_pieces.json'),'placement_evidence':placed,'piece_start':'0x0103274c','vftable_start':'0x01032750','piece_size':8,'reference_bytes_hex':G.refbytes(0x0103274c,8).hex(),'relocations':rel,'col_selected_coverage':col,'code_owner':owner,'alias_confidence':'reference slot points at implementation whose source has deleting-destructor-shaped behavior, but exact compiler ABI/name compatibility is unproved','checks_needed':['verify exact executable/manifest identity and all 8 bytes/relocations','confirm RTTI and vector-versus-scalar deleting destructor semantics with independent evidence','preflight protected generator diff and baseline compare','test in isolated compiler lane after coordinator grant','only then consider opt-in selection, controls, exact image/relocations and semantic harness']}
out=H.parent/'out'/'phase2-vtable'; out.mkdir(parents=True,exist_ok=True); json.dump(result,open(out/'vtable_candidate.json','w'),indent=2);print(json.dumps(result,indent=2))

