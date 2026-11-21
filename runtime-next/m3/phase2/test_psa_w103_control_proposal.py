"""Private synthetic tests for proposed W103 controls."""
import importlib.util
from pathlib import Path
p=Path('runtime-next/m3/phase2/psa_w103_control_proposal.py');s=importlib.util.spec_from_file_location('x',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
td={'va':0x1196e20,'data':bytes([0]*8+[46]+[0]*17),'relocs':[(0,'M5T_010f1ee0',0)],'reloc_va':[0x10f1ee0],'entry':{'unit':620,'kind':'rtti0','size':26}}
col={'va':0x110fbe8,'data':bytes(20),'relocs':[(12,'M5T_01196e20',0),(16,'M5T_0110fbfc',0)],'reloc_va':[0x1196e20,0x110fbfc],'entry':{'unit':620,'kind':'rtti4','size':20}}
a,_=m.mutate([td,col],'psatd');assert a[0]['data'][8]==47 and td['data'][8]==46 and a[1]==col
b,_=m.mutate([td,col],'psacol');assert b[1]['reloc_va']==[0x11831e8,0x110fbfc] and col['reloc_va'][0]==0x1196e20 and b[0]==td
for mode,rows in [('psatd',[]),('psacol',[td])]:
 try:m.mutate(rows,mode);raise AssertionError('expected rejection')
 except ValueError:pass
print('PASS 4 synthetic checks')
