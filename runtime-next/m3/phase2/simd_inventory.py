import json,sys,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;root=M.parent.parent;sys.path.insert(0,str(M));import gen_m3 as G
sel=json.load(open(M/'batch8_final_selection.json'))['entries'];rows=[]
for a in (0x10cb620,0x10cb630):
 e=next(x for x in sel if x['va']==a);assert e['tc']=='W' and e['runs'][0]==['M',4] and a%16==0
 raw=G.refbytes(a,16);assert all(G._floatok4(raw[i:i+4],'M') for i in range(0,16,4));assert not any(a-3<=x<a+16 for x in G.ORIG_SITES)
 rows.append({'va':a,'size':16,'align':16,'symbol':e['decl'][0],'namespace':'fnv_00cd9d10','type_name':'__m128','source':{'path':'fnv_decomp/src/staging/blk_00cc0000_o2.cpp','class_line':28044,'declaration_line':28065 if a==0x10cb620 else 28069},'original_w_size':e['size']})
tail={'va':0x10cb640,'tc':'W','size':4,'kind':'tail-m3','ns':'','named':False,'head':None,'runs':[['P',1]],'align':4};assert 0x10cb640 in G.ORIG_SET
out={'scope':'Private two source-view SIMD objects plus retained one-pointer W tail; requires 16-byte COFF, original and translated output alignment.','entries':rows,'tail':tail,'tail_relocation_offsets':[0],'source_sha256':hashlib.sha256((root/'fnv_decomp/src/staging/blk_00cc0000_o2.cpp').read_bytes()).hexdigest()};json.dump(out,open(H/'simd_candidates.json','w'),indent=2);print('two 16-byte objects, one 4-byte W tail with original relocation')

