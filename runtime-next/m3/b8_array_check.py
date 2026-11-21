exec(open('b8_types_certify.py').read().split('accepted=[];')[0])
for va,num,sz in [(0x1190910,640,40),(0x118e8e0,205,40),(0x1187ac8,112,24)]:
 end=va+num*sz
 print(hex(va),hex(end),'b7',[(hex(e['va']),esize(e)) for e in selected if e['va']<end and va<e['va']+esize(e)][:12]); print('dv1',[(hex(a),b-a) for a,b in dv1 if a<end and va<b][:10]); print('prod',[(hex(a),b-a) for a,b in prod if a<end and va<b][:10]); print('names',list(map(hex,[x for x in bnds if va<x<end]))[:20]); print('labels',len([x for x in labels if va<x<end]),'relocs',len([x for x in drel if va<=x<end]),'fields',len([x for x in fldS if va<=x<end]))
