exec(open('b8_array_check.py').read().split('for va,num,sz')[0])
import math
raw=refbytes(0x1187ac8,2688); d=struct.unpack('<336d',raw)
print('sphere',len(d),'finite',sum(map(math.isfinite,d)),'negative_zero',sum(x==0 and math.copysign(1,x)<0 for x in d),'range',min(d),max(d),'first',d[:9]); print('ends', raw[-48:].hex())
for va,count in [(0x1190910,640),(0x118e8e0,205)]:
 print(hex(va),collections.Counter((f-va)%40 for f in drel if va<=f<va+count*40))
