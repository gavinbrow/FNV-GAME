import struct,glob,os
LIBDIRS=[r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\PlatformSDK\Lib',r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\lib']
def members(path):
    d=open(path,'rb').read(); assert d[:8]==b'!<arch>\n'
    p=8
    while p<len(d):
        h=d[p:p+60]; size=int(h[48:58]); body=d[p+60:p+60+size]; yield h[:16].decode('latin1').strip(),body
        p+=60+size+(size&1)
def import_objs(path):
    for n,b in members(path):
        if len(b)>=20 and struct.unpack_from('<HH',b,0)==(0,0xffff):
            ver,mach,ts,sz,hint,flags=struct.unpack_from('<HHIIHH',b,2)
            names=b[20:].split(b'\0')
            yield dict(sym=names[0].decode(),dll=names[1].decode(),hint=hint,type=flags&3,nametype=(flags>>2)&7,mach=mach)
def scan():
    out={}
    for dd in LIBDIRS:
        for f in glob.glob(dd+'/*.lib'):
            try:
                for o in import_objs(f): out.setdefault((o['dll'].lower(),o['sym']),[]).append((os.path.basename(f),o['hint']))
            except Exception as e: pass
    return out
if __name__=='__main__':
    s=scan(); print(len(s)); import itertools
    for k,v in itertools.islice(s.items(),5): print(k,v)
