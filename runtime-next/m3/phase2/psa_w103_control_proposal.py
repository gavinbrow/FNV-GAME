"""Private proposed W103-only negative controls; does not alter production modules."""
import copy
MODES=('psatd','psacol')
def mutate(records,mode):
 if mode not in MODES:raise ValueError('unsupported control')
 out=copy.deepcopy(records);va=0x1196e20 if mode=='psatd' else 0x110fbe8;size=26 if mode=='psatd' else 20;kind='rtti0' if mode=='psatd' else 'rtti4';matches=[r for r in out if r['va']==va]
 if len(matches)!=1:raise ValueError('expected exactly one native piece')
 r=matches[0];e=r['entry']
 if e['unit']!=620 or e['kind']!=kind or e['size']!=size or len(r['data'])!=size:raise ValueError('unexpected native identity')
 if mode=='psatd':
  off=8
  if r['data'][off]!=46 or any(o<=off<o+4 for o,_,_ in r['relocs']):raise ValueError('unexpected TD field')
  data=bytearray(r['data']);data[off]^=1;r['data']=bytes(data)
  label='NEGATIVE CONTROL (psa type descriptor value): VA 01196e20 offset 8 changed from 2e to 2f'
 else:
  matches=[i for i,(o,n,a) in enumerate(r['relocs']) if o==12 and n=='M5T_01196e20' and a==0]
  if len(matches)!=1 or r['reloc_va'][matches[0]]!=0x1196e20:raise ValueError('unexpected COL relocation')
  i=matches[0];r['relocs'][i]=(12,'M5T_011831e8',0);r['reloc_va'][i]=0x11831e8
  label='NEGATIVE CONTROL (psa COL pointer): VA 0110fbe8 offset 12 retargeted 01196e20 to 011831e8'
 e['negctl']=mode
 return out,label
