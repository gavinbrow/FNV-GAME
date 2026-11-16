exec(open('setup.py').read())
b0=np.searchsorted(bs,Fo,'right')-1; b3=np.searchsorted(bs,Fo+3,'right')-1
s=np.where(b0!=b3)[0]; print('straddling fields',len(s))
for i in s[:10]: print(hex(F[i]),KIND[i],ST[i],ORG[i],SRC[i],hex(be[b0[i]]+TV), btype[b0[i]],btype[b3[i]])
# overlapping fields
o=np.argsort(F); ff=F[o]; print('overlapping record fields',int((np.diff(ff)<4).sum()))
