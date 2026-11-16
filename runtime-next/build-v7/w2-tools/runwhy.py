import sys, json, collections
sys.dont_write_bytecode = True
sys.path.insert(0,'.')
from concurrent.futures import ProcessPoolExecutor
import ehdiag as D
U=None
def init():
    global U; U=D.setup()
def job(i):
    D.WHY.clear()
    if not U[i].get('eh_tails'): U[i]['eh_tails'] = [{'address': '0x0', 'size': 0, 'dummy': True}]
    r = D.A.process((i, U[i])); out=[]
    for t in r['tails']:
        if not t['ok']:
            out.append(dict(at=t['address'], size=len(t['data']) if t['data'] else None, parent=t['parent'], why=[list(map(str,x[1:])) for x in D.WHY if x[0]==t['address']], hasdata=t['data'] is not None))
    return i, out
if __name__=='__main__':
    fe=json.load(open('../gaps/failed_eh.json'))
    idx=sorted({x['unit_index'] for x in fe})
    res={}
    with ProcessPoolExecutor(10, initializer=init) as ex:
        for i,o in ex.map(job, idx): res[i]=o
    json.dump(res,open('why.json','w'))
    print(len(idx), sum(len(v) for v in res.values()))
