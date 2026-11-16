exec(open('setup.py').read())
# 1. Z bad
NS,total,seq=build_layout('Z'); L=Lfun(NS,NB); inv=Linv(NS,NB,total)
sel=np.where(isT & ~((KIND=='DIR32')&~inorig))[0]
t=Tref[sel]; bt=inv(L(t)); bad=np.where(bt!=t)[0]
for b in bad[:5]:
    i=sel[b]; print('BAD field',hex(F[i]),KIND[i],ST[i],ORG[i],'target',hex(t[b]),'-> back',hex(bt[b]))
    k=np.searchsorted(bs,t[b]-TV,'right')-1; print(' block',hex(bs[k]+TV),hex(be[k]+TV),btype[k])
# 2. missing orig relocs by block type
miss=np.array([x for x in orel_text.tolist() if x not in dset],np.int64)
mb=np.searchsorted(bs,miss-TV,'right')-1
print('missing by block type',collections.Counter(btype[mb]))
mv=rd32(miss-TV); print('missing target code',int(((mv>=TV)&(mv<TE)).sum()),'data',int(((mv<TV)|(mv>=TE)).sum()))
print('missing target code by tgt blk', collections.Counter(btype[np.searchsorted(bs,mv[(mv>=TV)&(mv<TE)]-TV,'right')-1]))
# 3. record refs: cross-block
tb=np.searchsorted(bs,np.where(tgt_text,Tref,TV)-TV,'right')-1; fbk=np.searchsorted(bs,Fo,'right')-1
ct=isT&tgt_text
print('records w/ code target',int(ct.sum()),'same block',int((ct&(tb==fbk)).sum()),'cross block',int((ct&(tb!=fbk)).sum()))
for k_ in ('REL32','DIR32'): print(k_,'code-target cross-block',int((ct&(tb!=fbk)&(KIND==k_)).sum()),'same',int((ct&(tb==fbk)&(KIND==k_)).sum()))
print('records code-target by status',collections.Counter(ST[ct]))
cb=ct&(tb!=fbk)
print('cross-block by status',collections.Counter(ST[cb]),'by origin',collections.Counter(ORG[cb]))
# DIR32 text-range but not in orig reloc: constants
c=(KIND=='DIR32')&~inorig; print('dir32 not in orig: tgt in text',int((c&tgt_text).sum()), 'of',int(c.sum()))
# borrowed: code-target, cross-block
bo=(ST=='borrow'); print('borrow code-target',int((bo&ct).sum()),'cross',int((bo&cb).sum()),'of',int(bo.sum()))
print('disagree',int((ST=='disagree').sum()),'code tgt',int(((ST=='disagree')&ct).sum()))
# DIR32 in-text orig relocs targeting code by block: from records + missing
oc_total=int(((ov:=rd32(orel_text-TV))>=TV).sum())
print('orig text relocs->code', int(((ov>=TV)&(ov<TE)).sum()))
# data->code with unaligned/stale? and pointers not in reloc
for nm,va,vs,rp,rs in pe.secs:
    if nm in ('.rdata','.data'):
        n=(min(vs,rs)//4); a=np.frombuffer(pe.d,np.uint32,count=n,offset=rp).astype(np.int64)
        va_abs=pe.base+va+np.arange(n)*4
        m=(a>=TV)&(a<TE)
        rset=np.isin(va_abs,orel_data)
        # candidates: value == start of a block, not in reloc
        bi=np.searchsorted(bs,a[m]-TV,'right')-1; isstart=(a[m]-TV)==bs[bi]
        print(nm,'dwords in text range',int(m.sum()),'in reloc',int((m&rset).sum()),'not in reloc',int((m&~rset).sum()),'not-in-reloc & block-start',int((isstart&~rset[m]).sum()))
