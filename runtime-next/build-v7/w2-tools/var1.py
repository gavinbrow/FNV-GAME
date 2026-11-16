import sys, subprocess
sys.dont_write_bytecode = True
SRC='C:/Projects/Decompilation/fnv_decomp/src/staging/blk_00b80000_o2.cpp'
TMP='C:/Projects/Decompilation/fnv_decomp/src/staging/w2tmp_b8.cpp'
base=open(SRC,'rb').read().decode('latin1')
old="""        if (m_04.r_04[off])
        {
            ShaderLayout* shader = static_cast<ShaderLayout*>(static_cast<ISSBase*>(m_04.r_04[off]));"""
old=old.replace('\n','\r\n') if '\r\n' in base else old
variants={
 'v1': """        if (*(void**)((char*)m_04.r_04 + off * 4))
        {
            ShaderLayout* shader = static_cast<ShaderLayout*>(static_cast<ISSBase*>(*(void**)((char*)m_04.r_04 + off * 4)));""",
 'v2': """        if (*(off + m_04.r_04))
        {
            ShaderLayout* shader = static_cast<ShaderLayout*>(static_cast<ISSBase*>(*(off + m_04.r_04)));""",
 'v3': """        void** slot = &m_04.r_04[off];
        if (*slot)
        {
            ShaderLayout* shader = static_cast<ShaderLayout*>(static_cast<ISSBase*>(*slot));""",
}
import os
for k in sys.argv[1:]:
    new=variants[k]
    if '\r\n' in base: new=new.replace('\n','\r\n')
    assert base.count(old)==1
    open(TMP,'wb').write(base.replace(old,new).encode('latin1'))
    r=subprocess.run([sys.executable,'-I','compile1.py','2757:src/staging/w2tmp_b8.cpp'],capture_output=True,text=True); print(k,r.stdout.strip()[:200])
    r=subprocess.run([sys.executable,'-I','fndiff.py','2757','0xb94520'],capture_output=True,text=True); print(r.stdout.splitlines()[:2])
