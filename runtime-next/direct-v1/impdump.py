import pefile,struct,json,sys
pe=pefile.PE(sys.argv[1] if len(sys.argv)>1 else 'FalloutNV_direct.exe')
imp=pe.OPTIONAL_HEADER.DATA_DIRECTORY[1]
dl=[]
for i in range(40):
    d=struct.unpack('<5I',pe.get_data(imp.VirtualAddress+20*i,20))
    if not any(d): break
    nm=pe.get_string_at_rva(d[3]).decode()
    ents=[];k=0
    while True:
        v=struct.unpack('<I',pe.get_data(d[0]+4*k,4))[0]
        if not v: break
        if v>>31: ents.append(('ord',v&0xffff,None,v))
        else:
            h=struct.unpack('<H',pe.get_data(v,2))[0]; ents.append(('name',h,pe.get_string_at_rva(v+2).decode(),v))
        k+=1
    dl.append(dict(dll=nm,oft=d[0],iat=d[4],name_rva=d[3],ents=ents))
if __name__=='__main__':
    rows=sorted((e[3],d['dll'],e[2],e[1]) for d in dl for e in d['ents'] if e[0]=='name')
    for r in rows[:30]: print(hex(r[0]),r[1:])
    for a,b in zip(rows,rows[1:]):
        exp=a[0]+2+len(a[2])+1; exp+=exp&1
        if exp!=b[0]: print('gap',hex(a[0]),a[2],'->',hex(b[0]),'exp',hex(exp))
    print(hex(rows[0][0]),hex(rows[-1][0]))
