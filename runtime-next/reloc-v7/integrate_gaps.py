import json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,r'C:\Projects\Decompilation\runtime-next\pinned-build')
import compile_units_v3 as CU
FN=CU.FN
good=json.load(open('gaps_out/good.json')); body=open('gaps_out/gaps.cpp',encoding='latin1').read()
rel='src/funclets/eh_gaps.cpp'
hdr='// funclets/eh_gaps.cpp: %d unwind funclets of the original whose compiled form never matched (formerly 0xCC holes in the strict build); naked asm with real instructions, symbolic call/jmp targets (SUB_<va>).\n\n'%len(good)
(FN/rel).write_bytes((hdr+body).replace('\r\n','\n').replace('\n','\r\n').encode('latin1'))
p=FN/'build'/'units.json'; shutil.copy(p,str(p)+'.bak4-20261116-wB')
d=json.loads(p.read_text()); units=d['units']
u=dict(source=rel,compiler='sp1',flags=['/MT','/O2','/GS','/EHsc','/Gy'],functions=[dict(address='0x%08x'%g['va'],symbol='?FUN_%08x@@YAXXZ'%g['va'],size=g['size']) for g in good],symbols={})
idx=len(units); units.append(u)
r=CU.one((idx,u,CU.find_toolchains())); print(rel,idx,r['status'],r['error'][:200]); assert r['status']=='ok'
p.write_text(json.dumps(d,indent=1).replace('\n','\r\n')+'\r\n')
open(r'C:\Projects\Decompilation\runtime-next\pinned-build\logs\compile_v3.jsonl','a').write(json.dumps(dict(index=idx,source=rel,compiler='sp1',status='ok',rc=0,error='',seconds=r['seconds']))+'\n')
