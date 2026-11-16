import sys, json, collections
sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
import numpy as np
from pathlib import Path
sys.argv=['x']
import importlib.util
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import uncovered_v2 as U
J=json.loads((HERE/'logs'/'uncovered_v2.json').read_text())
rs=U.rs; text=U.text; cover=U.cover; nontriv=U.nontriv
runmask=np.zeros(rs,np.uint8)
for r in J['runs']: runmask[r['start']:r['end']]=1
lib=np.zeros(rs,np.uint8)
for m in J['lib_matches']: a=m['va']-U.TEXT_VA; lib[a:a+m['size']]=1
eh=np.zeros(rs,np.uint8)
for at,sz,ok,par,unit,inrec in json.loads((HERE/'logs'/'pieces_all_v2.json').read_text()):
    a=at-U.TEXT_VA
    if 0<=a and a+sz<=rs: eh[a:a+sz]=1
nt=nontriv&(runmask==1)
print('total nt',int(nt.sum()))
print('lib only',int((nt&(lib==1)&(eh==0)).sum()),'eh only',int((nt&(eh==1)&(lib==0)).sum()),'both',int((nt&(eh==1)&(lib==1)).sum()))
rest=nt&(lib==0)&(eh==0)
print('remaining',int(rest.sum()))
# remaining: split by whether inside a run that has project symbols
symmask=np.zeros(rs,np.uint8)
rem_by=collections.Counter()
for r in J['runs']:
    s,e=r['start'],r['end']; n=int(rest[s:e].sum())
    if not n: continue
    k='run-has-symbol-map-names' if r['symbols_in_run'] else 'run-has-no-names'
    rem_by[k]+=n
print(rem_by)
# remaining by 4K-ish clusters: list the biggest runs by remaining bytes
rows=[]
for r in J['runs']:
    s,e=r['start'],r['end']; n=int(rest[s:e].sum())
    if n: rows.append((n,r['va'],r['length'],r['symbols_in_run'],r['sample_names'][:3],r['prologues'],r['jt']))
rows.sort(reverse=True)
for x in rows[:12]: print(x)
# jump-table-like dword tables in remaining
import re
