"""Read-only source-bounded retail command records and archived ownership."""
import bisect,collections,hashlib,json,struct,sys
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;sys.path.insert(0,str(M.parent/'data-v3'));import common as g
OUT=M/'out/phase2-local-economy-20261119/commands';E=M/'out/phase2-native-source-positive/evidence';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError(OUT)
 manifest=E/'m3_manifest.json';pieces=E/'dv1_pieces.json';entries=json.loads(manifest.read_bytes())['entries'];dv=json.loads(pieces.read_bytes())['pieces'];ranges=[]
 for kind,seq in [('M3',entries),('DV1',dv)]:
  for p in seq:ranges.append((p['va'],p['va']+p['size'],kind,p.get('name') or p.get('kind')))
 ranges.sort();assert all(a[1]<=b[0] for a,b in zip(ranges,ranges[1:]));sites=sorted(g.orig_reloc_sites());allowed={0,4,12,20,24,28,32};result=[]
 for table,base,count in [('console',0x118e8e0,205),('script',0x1190910,640)]:
  for i in range(count):
   va=base+40*i;raw=g.read_ref(va,40)
   if raw is None or len(raw)!=40:raise ValueError('not fully file backed')
   words=struct.unpack('<10I',raw);rel=[s-va for s in sites[bisect.bisect_left(sites,va-3):bisect.bisect_left(sites,va+40)]]
   if any(x<0 or x+4>40 or x not in allowed for x in rel):raise ValueError('unexpected relocation at '+hex(va))
   for off in allowed:
    val=words[off//4]
    if off not in rel and val:raise ValueError('unrelocated pointer cell '+hex(va+off))
    if off in rel and g.sec_of(val) not in ('.text','.data','.rdata','CONST','.tls'):raise ValueError('unknown target '+hex(val))
   overlaps=[{'lo':max(a,va)-va,'hi':min(b,va+40)-va,'kind':k,'owner':n} for a,b,k,n in ranges if a<va+40 and va<b];covered=sum(x['hi']-x['lo'] for x in overlaps)
   result.append({'table':table,'index':i,'va':va,'size':40,'raw_hex':raw.hex(),'sha256':hashlib.sha256(raw).hexdigest(),'opcode':words[2],'requires_ref_byte':raw[16],'parameter_count':struct.unpack_from('<H',raw,18)[0],'relocations':rel,'pointer_targets':{str(off):words[off//4] for off in sorted(allowed)},'accepted_coverage_bytes':covered,'accepted_owners':overlaps})
 summary={}
 for name in ('console','script'):
  rows=[x for x in result if x['table']==name];summary[name]={'rows':len(rows),'fully_covered':sum(x['accepted_coverage_bytes']==40 for x in rows),'partly_covered':sum(0<x['accepted_coverage_bytes']<40 for x in rows),'uncovered':sum(x['accepted_coverage_bytes']==0 for x in rows),'coverage_bytes':sum(x['accepted_coverage_bytes'] for x in rows),'relocation_sites':sum(len(x['relocations']) for x in rows),'reference_flag_values':dict(collections.Counter(str(x['requires_ref_byte']) for x in rows))}
 sample={'accepted':[{'table':x['table'],'index':x['index'],'va':x['va']} for x in result if x['accepted_coverage_bytes']==40][:10],'uncovered':[{'table':x['table'],'index':x['index'],'va':x['va']} for x in result if x['accepted_coverage_bytes']==0][:10]}
 data={'scope':'source-accessed prefixes, original file-backed observations; no ownership or full array extent inferred','inputs':{'reference_sha256':hashlib.sha256(g.ref).hexdigest(),'m3_manifest_sha256':sha(manifest),'dv1_pieces_sha256':sha(pieces),'source_sha256':{str(p.relative_to(P)):sha(p) for p in [P/'fnv_decomp/src/fallout_shared/tesscriptfunctions.cpp',P/'fnv_decomp/src/fallout_shared/tesparameters.cpp',P/'fnv_decomp/include/ScriptFunctionInfo.h']}},'schema':{'stride':40,'pointer_offsets':sorted(allowed),'basis':['tesscriptfunctions.cpp CommandDescription loops','tesparameters.cpp _CommandEntry parameter pointer','ScriptFunctionInfo.h field view; alias identity not independently proven']},'summary':summary,'sample':sample,'records':result,'limitations':['field storage evidence is not full native symbol or source type identity','partial/zero-overlap records cannot be selected without declaration, rewrite, chunk, field and alias proofs','no compiler, selector, image or runtime tests']}
 OUT.mkdir(parents=True);(OUT/'audit.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({'summary':summary,'sample':sample,'output_sha256':sha(OUT/'audit.json')}))
if __name__=='__main__':main()
