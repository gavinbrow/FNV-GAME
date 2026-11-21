"""Read-only source-evidenced array and W-tail split inventory."""
import json,re,sys,collections
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent;sys.path.insert(0,str(M));import gen_m3 as G
j=lambda p:json.load(open(p,encoding='utf-8-sig')); base=j(M/'out/phase2-w-arrays/selection.json')['entries'];inv={int(g['addr'],16):g for g in j(M/'inventory/dat_globals.json')['globals']};orig=j(M/'batch8_final_selection.json')['entries']; units=j(M.parent.parent/'fnv_decomp/build/units.json')['units'];sites=G.ORIG_SITES; sj=j(R/'data-v3/symbolic.json');fields={G.SEC[r[0]]['va']+r[1] for r in sj['fields']}|set(sites); names=collections.defaultdict(set)
for u in units:
 for k in u.get('symbols',{}):
  for m in re.finditer(r'(?:DAT|PTR|UNK|OFF|BYTE|WORD|DWORD)_([0-9a-f]{8})',k):names[int(m.group(1),16)].add(k)
items=[]
for a,n,typ,ns,decl,line in [(0x11a7d40,256,'E','sa238a0','extern unsigned char DAT_011a7d40[256];',13141),(0x11aced8,36,'I','fnv_00af4550','extern unsigned int DAT_011aced8[9];',6153),(0x1093b6c,16,'H','fnv_009f9e50','extern int DAT_01093b6c[4];',6205)]:
 e=next(x for x in orig if x['va']==a);symbol=e['decl'][0];g=inv[a];assert g['decls']==[decl] and not g['defs'] and len(e['decl'])==1 and names[a]=={symbol};assert e['tc']=='W' and e['size']>=n and e['ns']==ns
 assert not any(a-3<=f<a+n for f in fields)
 o=0;tail=[]
 for kind,count in e['runs']:
  end=o+G.RUN_SZ[kind]*count
  assert not o<n<end
  if o>=n:tail.append([kind,count])
  o=end
 assert o==e['size'] and sum(G.RUN_SZ[k]*c for k,c in tail)==e['size']-n
 if tail:
  cut=a+n;assert not any(x<cut<x+4 for x in fields)
  assert not any(cut<=x<a+e['size'] for x in names)
  original=[x-cut for x in sites if cut<=x<a+e['size']]; expected=[];pos=0
  for kind,count in tail:
   if kind=='P':expected.extend(pos+4*i for i in range(count))
   pos+=G.RUN_SZ[kind]*count
  # P runs can contain non-relocated null cells; all actual relocations must
  # be fully contained within the retained pointer-run slots.
  assert set(original).issubset(expected)
 else:original=[]
 items.append({'va':a,'size':n,'element_type_code':typ,'namespace':ns,'symbol':symbol,'source_line':line,'original_w_size':e['size'],'tail_va':a+n if tail else None,'tail_size':e['size']-n,'tail_runs':tail,'tail_original_reloc_offsets':original,'limitation':'Tail remains address-named W scaffolding; native ownership/type unproven.'})
result={'scope':'Source-declared array candidates with exact source evidence, unique units key and W run-boundary splits; targeted source/COFF and end-to-end checks still required.','array_candidates':items,'array_bytes':sum(x['size'] for x in items),'coverage_change':0}
json.dump(result,open(H/'array_split_candidates.json','w'),indent=2);print('candidates',len(items),'bytes',result['array_bytes']);print([(hex(x['va']),x['size'],x['tail_size'],len(x['tail_original_reloc_offsets'])) for x in items])
