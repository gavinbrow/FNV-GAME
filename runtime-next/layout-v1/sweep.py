exec(open("setup.py").read()); bsl=bs.tolist(); import bisect
import capstone, time, json
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32); cs.skipdata=False
rec=set(F.tolist()); orel=set(orel_text.tolist())
# jump-table runs from original reloc
ot=orel_text; ovv=rd32(ot-TV)
cand=ot[(ovv>=TV)&(ovv<TE)]
runs=[]; i=0
while i<len(cand):
    j=i
    while j+1<len(cand) and cand[j+1]-cand[j]==4: j+=1
    if j-i+1>=3: runs.append((int(cand[i]-TV),int(cand[j]-TV+4)))
    i=j+1
print('jump/ptr table runs in .text',len(runs),'bytes',sum(b-a for a,b in runs))
rs_=[r[0] for r in runs]
tbl_blocks=collections.Counter()
st=dict(insns=0,rel32_ext=0,rel32_ext_rec=0,rel32_ext_unrec=0,rel32_ext_unrec_blockstart=0,rel32_int=0,rel8_ext=0,rel8_int=0,call_next=0,bad_decode=0,
        blocks_swept=0,last_nonterm=0,last_nonterm_nopad=0,jmp_table_idx=0,unrec_samples=[],rel8_samples=[],nopad_samples=[],blobs_rel32_ext=0,blobs_rel32_ext_dir=0)
T0=time.time()
by_btype=collections.defaultdict(lambda:collections.Counter())
rawb=bytes(text)
for bi in range(len(blocks)):
    a0,a1=int(bs[bi]),int(be[bi])
    seg=rawb[a0:a1]
    if all(x in (0xcc,0,0x90) for x in seg): continue
    st['blocks_swept']+=1
    # split by table runs
    k=bisect.bisect_right(rs_,a0)-1 if False else None
    pieces=[(a0,a1)]
    for (ra,rb) in runs:
        pass
    p=a0; segs=[]
    import bisect as _b
    ii=_b.bisect_left(rs_,a0)
    while ii<len(runs) and runs[ii][0]<a1:
        ra,rb=runs[ii]
        if ra>p: segs.append((p,ra))
        p=max(p,min(rb,a1)); ii+=1
    if p<a1: segs.append((p,a1))
    last=None; lastend=a0
    bt=btype[bi]
    for (sa,sb) in segs:
        off=sa
        while off<sb:
            got=False
            for (addr,size,mn,ops) in cs.disasm_lite(rawb[off:sb],TV+off):
                got=True
                st['insns']+=1
                o=addr-TV; b=rawb[o]
                tgt=None;kind=None;fo=None
                if size==5 and b in (0xe8,0xe9):
                    rel=int.from_bytes(rawb[o+1:o+5],'little',signed=True); tgt=addr+5+rel; kind=32; fo=addr+1
                    if rel==0 and b==0xe8: st['call_next']+=1
                elif size==6 and b==0x0f and 0x80<=rawb[o+1]<=0x8f:
                    rel=int.from_bytes(rawb[o+2:o+6],'little',signed=True); tgt=addr+6+rel; kind=32; fo=addr+2
                elif size==2 and (b==0xeb or 0x70<=b<=0x7f or 0xe0<=b<=0xe3):
                    rel=int.from_bytes(rawb[o+1:o+2],'little',signed=True); tgt=addr+2+rel; kind=8
                if tgt is not None and TV<=tgt<TE:
                    tbk=bisect.bisect_right(bs.tolist() if False else bsl,tgt-TV)-1
                    ext=(tbk!=bi)
                    if kind==32:
                        if not ext: st['rel32_int']+=1
                        else:
                            st['rel32_ext']+=1; by_btype[bt]['rel32_ext']+=1
                            if fo in rec: st['rel32_ext_rec']+=1; by_btype[bt]['rec']+=1
                            else:
                                st['rel32_ext_unrec']+=1; by_btype[bt]['unrec']+=1
                                if bs[tbk]==tgt-TV: st['rel32_ext_unrec_blockstart']+=1; by_btype[bt]['unrec_strong']+=1
                                if len(st['unrec_samples'])<8: st['unrec_samples'].append((hex(addr),hex(tgt),bt))
                    else:
                        if ext:
                            st['rel8_ext']+=1; by_btype[bt]['rel8_ext']+=1
                            if len(st['rel8_samples'])<8: st['rel8_samples'].append((hex(addr),hex(tgt),bt))
                        else: st['rel8_int']+=1
                if mn in ('jmp',) and '*' in ops and '0x' in ops: st['jmp_table_idx']+=1
                last=mn; lastend=o+size
                off=o+size
            if not got: off+=1; st['bad_decode']+=1
            elif off<sb: pass
            else: break
    if last is not None and last not in ('ret','jmp','int3','ud2','hlt','retn'):
        st['last_nonterm']+=1
        if lastend>=a1-0: 
            st['last_nonterm_nopad']+=1
            if len(st['nopad_samples'])<8: st['nopad_samples'].append((hex(a0+TV),last,bt))
print('sweep done',round(time.time()-T0),'s')
st['by_btype']={k:dict(v) for k,v in by_btype.items()}
json.dump(st,open('sweep_result.json','w'),indent=1)
print(json.dumps(st,indent=1))
