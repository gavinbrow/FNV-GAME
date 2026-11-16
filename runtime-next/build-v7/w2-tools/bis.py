import subprocess,sys,re
SRC='C:/Projects/Decompilation/fnv_decomp/src/staging/blk_00b80000_o2.cpp.bak-20261115-w2'
TMP='C:/Projects/Decompilation/fnv_decomp/src/staging/w2tmp_b8.cpp'
base=open(SRC,'rb').read().decode('latin1')
nl='\r\n' if '\r\n' in base else '\n'
pat=re.compile(r'(struct (\w+) : NiMemObj'+nl+'\{'+nl+')')
ms=list(pat.finditer(base)); print(len(ms),[m.group(2) for m in ms][:5])
def test(sel):
    out=base
    for m in reversed(ms):
        if m.group(2) in sel: out=out[:m.end()]+"    static void operator delete(void*, unsigned int);"+nl+out[m.end():]
    open(TMP,'wb').write(out.encode('latin1'))
    subprocess.run([sys.executable,'-I','compile1.py','2757:src/staging/w2tmp_b8.cpp'],capture_output=True,text=True)
    r=subprocess.run([sys.executable,'-I','fndiff.py','2757','0xb94520'],capture_output=True,text=True); return r.stdout.splitlines()[1] if len(r.stdout.splitlines())>1 else r.stdout
names=[m.group(2) for m in ms]
for k in (6,7,8,9):
    print(k,test(set(names[:k])))
print('names9',names[9], 'only', test({names[9]}))
import collections
c=collections.Counter(re.findall(r'new (C\w+)',base[base.index('B94520Cls::FUN_00b94520()'):][:60000]))
print([(n,c[n]) for n in names])
