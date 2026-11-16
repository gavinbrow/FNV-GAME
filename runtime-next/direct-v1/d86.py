import sys,pefile
from capstone import *
pe=pefile.PE(sys.argv[1] if sys.argv[1].endswith('.exe') else 'FalloutNV_direct.exe')
a=sys.argv[-3]; va=int(sys.argv[-3],16); b=int(sys.argv[-2]); n=int(sys.argv[-1])
d=pe.get_data(va-b-0x400000,b+n)
for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(d,va-b): print(hex(i.address),i.mnemonic,i.op_str)
