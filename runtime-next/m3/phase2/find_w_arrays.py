import json,re,sys,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;root=M.parent.parent;sys.path.insert(0,str(M));import gen_m3 as G
j=lambda p:json.load(open(p,encoding='utf-8-sig'));sel=j(M/'batch8_final_selection.json')['entries']; inv={int(x['addr'],16):x for x in j(M/'inventory/dat_globals.json')['globals']};units=j(root/'fnv_decomp/build/units.json')['units'];sj=j(M.parent/'data-v3/symbolic.json');fields={G.SEC[r[0]]['va']+r[1] for r in sj['fields']}|G.ORIG_SET;source=root/'fnv_decomp/src/fallout/misc/main.cpp';lines=source.read_text(encoding='utf-8').splitlines();items=[]
for a in range(0x11a7440,0x11a7d40,256):
 e=next(x for x in sel if x['va']==a);sym='?DAT_%08x@sa238a0@@3PAEA'%a;decl='extern unsigned char DAT_%08x[256];'%a;g=inv[a]
 assert e['tc']=='W' and e['size']==256 and e['decl']==[sym] and e['ns']=='sa238a0' and g['decls']==[decl] and not g['defs']
 keys={k for u in units for k in u.get('symbols',{}) if re.search(r'(?:DAT|PTR|OFF|UNK|BYTE|WORD|DWORD)_%08x\b'%a,k)};assert keys=={sym}
 assert not any(a-3<=f<a+256 for f in fields)
 pos=[i+1 for i,l in enumerate(lines) if l.strip()==decl];assert len(pos)==1 and 13130<=pos[0]<=13142
 items.append({'va':a,'size':256,'namespace':'sa238a0','element_type':'unsigned char','const':False,'symbol':sym,'source':{'path':'fnv_decomp/src/fallout/misc/main.cpp','line':pos[0]},'body_uses':'CharTable::FUN_00a238a0 bounds iChar to 0..255','original_w_alignment':e['align']})
out={'schema':1,'scope':'Nine exact 256-byte W ranges with explicit source array bounds, matching single unit symbol and no fields/relocations; selected ranges unchanged. Scope/alias checks and compiled identity remain required.','count':len(items),'bytes':sum(x['size'] for x in items),'entries':items,'deferred':{'va':0x11a7d40,'reason':'W range is 288 bytes: split 256-byte array and independently owned 32-byte tail before replacement'}}
json.dump(out,open(H/'w_array_candidates.json','w'),indent=2);print('w arrays',len(items),out['bytes'])
