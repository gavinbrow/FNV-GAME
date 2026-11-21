import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path.insert(0,str(M));import gen_m3 as G
s=json.load(open(M/'batch8_final_selection.json'))['entries'];a=0x11a9c30;e=next(x for x in s if x['va']==a);assert e['tc']=='W' and e['size']==264 and e['runs'][0]==['M',8] and e['ns']=='fnv_005c25f0';tail={'va':a+12,'tc':'W','size':252,'kind':'tail-m3','ns':'','named':False,'head':None,'runs':[['M',5]]+e['runs'][1:],'align':4}
raw=G.refbytes(a,e['size']);original=G.g_items(a,raw,e['runs']);parts=G.g_items(a+12,raw[12:],tail['runs']);assert original[0][3:]==parts[0] and original[1:]==parts[1:]
rels=[x-(a+12) for x in G.ORIG_SITES if a+12<=x<a+264];assert len(rels)==2
out={'scope':'One source-native NiPoint3 aggregate head; W tail remains synthetic and preserves old run items and two original relocations.','head':{'va':a,'size':12,'namespace':'fnv_005c25f0','class_name':'NiPoint3','symbol':'?DAT_011a9c30@fnv_005c25f0@@3VNiPoint3@1@A','source':{'path':'fnv_decomp/src/fallout_shared/tesscriptfunctions.cpp','class_line':50845,'declaration_line':50853}},'tail':tail,'tail_relocation_offsets':rels,'limitation':'Private fixture only; no evidence all 264 bytes belong to the class.'}
json.dump(out,open(H/'point3_candidate.json','w'),indent=2);print('head 12, tail 252, relocs',len(rels))
