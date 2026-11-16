import sys,gzip,struct,collections,re,json
sys.path.insert(0,(__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\runtime-next\pinned-build'))
sys.path.append((__import__('os').environ.get('FNV_PY_SITE', r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')))
sys.dont_write_bytecode=True
import assemble_v3 as A
pe=A.Pe(A.IMG); orig=pe.data
peo=struct.unpack_from('<I',orig,0x3c)[0]
rrva,rsz=struct.unpack_from('<II',orig,peo+24+96+5*8)
p=A.rva2off(pe,rrva);tbl=set();end=p+rsz
while p<end:
    pg,bs=struct.unpack_from('<II',orig,p)
    if bs==0:break
    for k in range((bs-8)//2):
        w,=struct.unpack_from('<H',orig,p+8+2*k)
        if w>>12==3: tbl.add(pg+(w&0xfff))
    p+=bs
imgsz=struct.unpack_from('<I',orig,peo+24+56)[0]
TEXT_VA=pe.base+pe.sections[0][0]
def load_rows(path='../build-v4/relocs_v4.tsv.gz'):
    rows=[]
    with gzip.open(path,'rt') as f:
        next(f)
        for l in f: rows.append(l.rstrip('\n').split('\t'))
    return rows
UNITS=json.load(open((__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\fnv_decomp\build\units.json')))['units']
def fnaddrs():
    d=collections.defaultdict(set)
    for u in UNITS:
        for f in u['functions']:
            for n in [f['symbol']]+f.get('fold_aliases',[]): d[n].add(int(f['address'],16))
    return d
def rd(va,n=4):
    o=A.va2off(pe,va,n); return orig[o:o+n]
