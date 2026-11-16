import sys; sys.path.insert(0,'.')
import coffrw,glob
b=open(r'C:\Projects\Decompilation\runtime-next\link-v2\obj_rw\1678.obj','rb').read()
ci=coffrw.comdat_info(b); print(len(ci)); 
s=coffrw.sections(b)
n=0
for k,(sel,num,ex) in list(ci.items())[:8]: print(k,s[k-1]['name'],hex(s[k-1]['flags']),sel,num,ex[:2])
