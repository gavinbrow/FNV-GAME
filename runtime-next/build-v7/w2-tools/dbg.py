import sys,re,os
sys.path.insert(0,'.')
import w2lib as L, autosized as AS
from pathlib import Path
from capstone import *
md=Cs(CS_ARCH_X86,CS_MODE_32)
def dis(b,a): return ' ; '.join(f"{i.mnemonic} {i.op_str}" for i in md.disasm(b,a))
L.setup()
idx=int(sys.argv[1]); parent=int(sys.argv[2],16); cls=sys.argv[3]
u=L.U[idx]; text,nl=AS.read(L.FN/u['source']); lines=text.split(nl)
cd=AS.class_def(lines,cls,len(lines)-1)
print('class line',cd+1, lines[cd][:100])
trial=lines[:]; AS.insert_decl(trial,cd)
tmp=(L.FN/u['source']).parent/'w2tmp_dbg.cpp'; tmp.write_bytes(nl.join(trial).encode('latin1'))
ok,out=L.compile_src(idx,tmp.relative_to(L.FN).as_posix(),L.W2/'auto'/'dbg.obj'); tmp.unlink(); print(ok)
ev=L.evalunit(idx,L.W2/'auto'/'dbg.obj'); ev0=L.evalunit(idx)
for a,v in sorted(ev.items()):
    if v[0]=='tail' and int(v[4],16)==parent:
        ref=L.PE.read(a,v[1])
        ours=L.LASTDATA.get(a)
        print('   ours',dis(ours,a) if ours else None)
        print(hex(a),v[1:4],'ref',dis(ref,a))
