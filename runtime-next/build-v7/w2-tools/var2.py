import sys, subprocess, re
sys.dont_write_bytecode = True
SRC='C:/Projects/Decompilation/fnv_decomp/src/staging/blk_00b80000_o2.cpp'
TMP='C:/Projects/Decompilation/fnv_decomp/src/staging/w2tmp_b8.cpp'
base=open(SRC,'rb').read().decode('latin1')
nl='\r\n' if '\r\n' in base else '\n'
i=base.index('    for (unsigned int off = 34; off < 116; ++off)'); j=base.index('}'+nl+nl+'namespace nb',i)
old=base[i:j]
print(repr(old))
V={
'a':"""    for (unsigned int off = 34; off < 116; ++off)
    {
        void* e = m_04.r_04[off];
        if (e)
        {
            ShaderLayout* shader = static_cast<ShaderLayout*>(static_cast<ISSBase*>(e));
            shader->Call120();
        }
    }
""",
'b':"""    for (unsigned int off = 34; off < 116; ++off)
    {
        if (m_04.r_04[off])
        {
            ShaderLayout* shader = static_cast<ShaderLayout*>(static_cast<ISSBase*>(m_04.r_04[off]));
            shader->Call120();
        }
    }
""".replace('off < 116','off != 116'),
'c':"""    unsigned int off = 34;
    do
    {
        if (m_04.r_04[off])
        {
            ShaderLayout* shader = static_cast<ShaderLayout*>(static_cast<ISSBase*>(m_04.r_04[off]));
            shader->Call120();
        }
        ++off;
    } while (off < 116);
""",
'd':"""    for (unsigned int off = 34; off < 116; ++off)
    {
        if (m_04.r_04[off])
        {
            ShaderLayout* shader = static_cast<ShaderLayout*>(static_cast<ISSBase*>(m_04.r_04[off]));
            shader->Call120();
        }
    }
""".replace('m_04.r_04[off]','this->m_04.r_04[off]'),
}
for k in sys.argv[1:]:
    new=V[k].replace('\n',nl)
    open(TMP,'wb').write((base[:i]+new+base[j:]).encode('latin1'))
    r=subprocess.run([sys.executable,'-I','compile1.py','2757:src/staging/w2tmp_b8.cpp'],capture_output=True,text=True); 
    r=subprocess.run([sys.executable,'-I','fndiff.py','2757','0xb94520'],capture_output=True,text=True); print(k,r.stdout.splitlines()[:2])
