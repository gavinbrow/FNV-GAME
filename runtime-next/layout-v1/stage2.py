import sys; sys.path.insert(0,'.')
from common import *
import pickle, collections, json
SCR = r'C:\Users\cjhub\AppData\Local\Temp\claude\d3df7c44bb2dc2c7\04ce5394-2d00-49a0-970d-e3a38a4b457e\scratchpad'
S = pickle.load(open(SCR+r'\s1.pkl','rb'))
blocks=S['blocks']; F=S['F']; KIND=S['KIND']; SRC=S['SRC']; ST=S['ST']; ORG=S['ORG']; EXP=S['EXP']
pe=PE(); TV=0x401000; TS=12441088; TE=TV+TS
ref=np.frombuffer(pe.d,np.uint8)[1024:1024+TS]
refb=bytes(ref)
bs=np.array([b[0] for b in blocks],np.int64); be=np.array([b[1] for b in blocks],np.int64)
btype=np.array([b[2] for b in blocks]); bunit=np.array([b[3] for b in blocks])
u32=lambda a: np.frombuffer(pe.d,np.uint32)  # unused
text=np.frombuffer(pe.d,np.uint8)[1024:1024+TS]
def rd32(offs):  # offs: text offsets array
    o=np.asarray(offs,np.int64)
    return (text[o].astype(np.int64)|(text[o+1].astype(np.int64)<<8)|(text[o+2].astype(np.int64)<<16)|(text[o+3].astype(np.int64)<<24))
def s32(v): return np.where(v>=2**31,v-2**32,v)
orig_rel=np.array(sorted(pe.relocs()),np.int64)
orel_text=orig_rel[(orig_rel>=TV)&(orig_rel<TE)]; orel_data=orig_rel[orig_rel>=TE]
# ---- records
isT = np.isin(KIND,['REL32','DIR32'])
dup=len(F)-len(set(F.tolist()))
print('dup field va',dup, 'non-text fields',int(((F<TV)|(F>=TE)).sum()))
Fo=F-TV
v=rd32(Fo)  # reference raw value
Tref=np.where(KIND=='REL32', (F+4+s32(v))&0xffffffff, v)
agree=(ST=='agree')
print('agree rows with EXP==Tref:', int((agree&isT&(EXP==Tref)).sum()),'of',int((agree&isT).sum()))
print('status counts',collections.Counter(ST)); print('borrow EXP set',int(((ST=='borrow')&(EXP>=0)).sum()))
oset=set(orel_text.tolist())
inorig=np.array([x in oset for x in F.tolist()])
d32=KIND=='DIR32'
print('DIR32 recs',int(d32.sum()),'in original reloc',int((d32&inorig).sum()),'not in orig',int((d32&~inorig).sum()))
print('orig text relocs',len(orel_text),'covered by records',int(len(oset & set(F[d32].tolist()))))
# ---- layouts
def build_layout(name, rng=None):
    order=[]  # list of block indices in new order, with gap after
    nb=len(blocks)
    # groups
    grp={}; 
    for i in range(nb):
        u=bunit[i]
        key=('u',int(u)) if u>=0 else ('s',i)
        grp.setdefault(key,[]).append(i)
    gl=sorted(grp.values(), key=lambda l:l[0])
    if name=='G': seq=[(i,0x10) for i in range(nb)]
    elif name=='U': seq=[(i,0x100 if j==len(g)-1 else 0) for g in gl for j,i in enumerate(g)]
    elif name=='R': seq=[(i,0x100 if j==len(g)-1 else 0) for g in gl for j,i in enumerate(reversed(g))]
    elif name=='Z':
        p=np.random.default_rng(1).permutation(nb); seq=[(int(i),0) for i in p]
    pos=0; NS=np.zeros(nb,np.int64)
    for i,gap in seq:
        al=1
        a=int(bs[i]); 
        while al<16 and a%(al*2)==0: al*=2
        pos=(pos+al-1)//al*al
        # keep alignment congruent to original (mod 16, up to al)
        NS[i]=pos; pos+=int(be[i]-bs[i])+gap
    return NS,pos,seq
def mk_maps(NS):
    o=np.argsort(NS); return NS[o], o   # sorted new starts and block idx
def Lfun(NS,NB):
    def L(t):
        t=np.asarray(t,np.int64); m=(t>=TV)&(t<TE); out=t.copy()
        a=t[m]-TV; bi=np.searchsorted(bs,a,'right')-1
        out[m]=NB+NS[bi]+(a-bs[bi]); return out
    return L
def Linv(NS,NB,total):
    sv,o=mk_maps(NS)
    def inv(n):
        n=np.asarray(n,np.int64); m=(n>=NB)&(n<NB+total); out=n.copy()
        a=n[m]-NB; k=np.searchsorted(sv,a,'right')-1; bi=o[k]
        ok=a-NS[bi] < (be[bi]-bs[bi])
        r=TV+bs[bi]+(a-NS[bi]); r=np.where(ok,r,-1); out[m]=r; return out
    return inv
NB=0x02000000
# fields to patch
tgt_text=(Tref>=TV)&(Tref<TE)
res={}
# category masks over records
rec_code_target = isT & tgt_text
def classify_fields():
    c={}
    c['rec_total']=len(F)
    return c
# records in atoms vs blobs
fb=np.searchsorted(bs,Fo,'right')-1
fblk_blob=(btype[fb]=='blob')
print('record fields in blob blocks',int(fblk_blob.sum()))
summ=dict(layouts={})
# data->code analysis fields (orig reloc in data)
doff=np.array([pe.off(a) for a in orel_data],np.int64)
D=pe.d; dv=np.array([int.from_bytes(D[o:o+4],'little') for o in doff],np.int64)
dcode=(dv>=TV)&(dv<TE)
dsec=np.array([pe.sec_of(int(a)) for a in orel_data])
print('data relocs',len(orel_data),'->code',int(dcode.sum()),collections.Counter(dsec[dcode]))
tb=np.searchsorted(bs,dv[dcode]-TV,'right')-1
tt=collections.Counter(btype[tb]); print('data->code by target block type',tt)
atom_start=(dv[dcode]-TV)==bs[tb]
print('data->code at block start',int(atom_start.sum()),'mid-block',int((~atom_start).sum()))
# original reloc in text: classify target
oT=orel_text; ov=rd32(oT-TV); ocode=(ov>=TV)&(ov<TE)
print('orig text relocs target code',int(ocode.sum()),'data',int((~ocode).sum()))
pickle.dump(dict(),open(SCR+r'\s2.pkl','wb'))
# ---- per-layout: build moved text and verify
out={}
dset=set(F[d32].tolist())
rec_ok_mask=isT
for name in ['G','U','R','Z']:
    NS,total,seq=build_layout(name); L=Lfun(NS,NB); inv=Linv(NS,NB,total)
    new=np.full(total,0xcc,np.uint8)
    for i in range(len(blocks)): new[NS[i]:NS[i]+be[i]-bs[i]]=text[bs[i]:be[i]]
    # (a) records (agree & borrow & disagree; target from Tref -- agree rows equal EXP)
    sel=np.where(isT)[0]
    f=F[sel]; t=Tref[sel]; k=KIND[sel]
    # DIR32 not in original reloc -> do not remap (constants)
    keep=~((k=='DIR32')&~inorig[sel])
    sel=sel[keep]; f=f[keep]; t=t[keep]; k=k[keep]
    # field new location, target new
    Fn=L(f); Tn=L(t)
    val=np.where(k=='REL32',(Tn-(Fn+4))&0xffffffff,Tn&0xffffffff)
    # Fn is absolute new VA; convert to new-image offset
    fo=Fn-NB
    for sh in range(4): new[fo+sh]=((val>>(8*sh))&0xff).astype(np.uint8)
    # orig reloc DIR32 in text not in records
    miss=np.array([x for x in orel_text.tolist() if x not in dset],np.int64) if name=='G' else res['miss']
    res['miss']=miss
    mv=rd32(miss-TV); mn=L(mv); mf=L(miss)-NB
    for sh in range(4): new[mf+sh]=((mn>>(8*sh))&0xff).astype(np.uint8)
    # verify: read back and map via inv
    vb=(new[fo].astype(np.int64)|(new[fo+1].astype(np.int64)<<8)|(new[fo+2].astype(np.int64)<<16)|(new[fo+3].astype(np.int64)<<24))
    back=np.where(k=='REL32',(Fn+4+s32(vb))&0xffffffff,vb)
    bt=inv(back)
    okc=(bt==t)
    # agree rows: compare against our EXP too
    ag=(ST[sel]=='agree')
    eq_exp=(EXP[sel]==bt)
    # new gap/ord stats
    out[name]=dict(total_text_bytes=int(total),fields_patched_records=int(len(sel)),verify_ok=int(okc.sum()),verify_bad=int((~okc).sum()),
        agree_rows=int(ag.sum()),agree_rows_map_back_equals_our_target=int((eq_exp&ag).sum()),
        orig_reloc_fields_not_in_records_patched=int(len(miss)))
    print(name,out[name])
    # data->code
    dn=L(dv[dcode]); dback=inv(dn); out[name]['data_to_code_ok']=int((dback==dv[dcode]).sum()); out[name]['data_to_code_total']=int(dcode.sum())
    # ordering sanity: layout is a permutation
    out[name]['blocks_overlap']=int((np.sort(NS)[1:]<np.sort(NS)[:-1]+0).sum())
pickle.dump(out,open(SCR+r'\s2.pkl','wb'))
json.dump(out,open('layouts_result.json','w'),indent=1)
