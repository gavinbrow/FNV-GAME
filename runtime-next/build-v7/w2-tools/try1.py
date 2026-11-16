"""try1.py <name> : apply python expr transformation file; usage via function api"""
import sys, subprocess
sys.dont_write_bytecode = True
FN='C:/Projects/Decompilation/fnv_decomp/'
def trial(rel_src, idx, edits, addr, tmp_rel=None):
    """edits: list of (old,new) applied on text (\n normalized to file's nl). returns (ndiff/reason line, extra)"""
    base=open(FN+rel_src,'rb').read().decode('latin1')
    nl='\r\n' if '\r\n' in base else '\n'
    for o,n in edits:
        o=o.replace('\n',nl); n=n.replace('\n',nl)
        assert base.count(o)==1,(base.count(o),o[:60])
        base=base.replace(o,n)
    tmp=rel_src.rsplit('/',1)[0]+'/w2tmp.cpp'
    open(FN+tmp,'wb').write(base.encode('latin1'))
    try:
        r=subprocess.run([sys.executable,'-I','compile1.py','%d:%s'%(idx,tmp)],capture_output=True,text=True)
        if 'ok' not in r.stdout: return r.stdout[-300:]
        r=subprocess.run([sys.executable,'-I','fndiff.py',str(idx),addr],capture_output=True,text=True)
        return ' | '.join(r.stdout.splitlines()[:2])
    finally:
        import os; os.remove(FN+tmp)
