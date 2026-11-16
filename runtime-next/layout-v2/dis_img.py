import sys, pefile, capstone
pe=pefile.PE(sys.argv[1]); va=int(sys.argv[2],16); before=int(sys.argv[3]); n=int(sys.argv[4])
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
best=None
for k in range(0,16):
    st=va-before+k; d=pe.get_data(st-0x400000,before-k+n)
    ins=list(md.disasm(d,st))
    if any(i.address==va for i in ins) and len(ins)>5:
        # prefer alignments whose instruction before va is a call
        prev=[i for i in ins if i.address+i.size==va]
        if prev and prev[0].mnemonic=='call': best=ins; break
        best=best or ins
for i in best: print(hex(i.address),i.mnemonic,i.op_str,'   <<<' if i.address==va else '')
