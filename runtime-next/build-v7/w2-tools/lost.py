import sys,pickle
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
import numpy as np
A=pickle.load(open(sys.argv[1]+'.pkl','rb')); B=pickle.load(open(sys.argv[2]+'.pkl','rb'))
G=pickle.load(open('../gaps/dump.pkl','rb')); TV=G['TEXT_VA']; ref=G['ref']; pad=np.isin(ref,(0xcc,0))
oa=(A['Wm']>0)&(A['B']==0)&~pad; ob=(B['Wm']>0)&(B['B']==0)&~pad
l=np.flatnonzero(oa&~ob); g=np.flatnonzero(ob&~oa)
print('lost',len(l),'gained',len(g)); print([hex(TV+x) for x in l[:20]])
