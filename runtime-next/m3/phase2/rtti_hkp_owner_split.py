"""Prepare, but never install, a checked RTTI/W ownership split proposal."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;PROJECT=M.parent.parent;OUT=M/'out/phase2-hkp-hierarchy-v1';EVID=M/'out/batch8-promoted-default-verified/evidence'
sys.path.insert(0,str(M));import gen_m3 as g


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    out=OUT/'owner-split-proposal.json'
    if out.exists():raise FileExistsError('refusing overwrite')
    selection=M/'batch8_final_selection.json';man=EVID/'m3_manifest.json';sel=json.loads(selection.read_text())['entries'];records=json.loads(man.read_text())['entries'];va=0x011b616c
    old=[e for e in sel if e['va']==va];archived=[e for e in records if e['va']==va]
    if len(old)!=1 or len(archived)!=1 or old[0]['tc']!='W' or old[0]['size']!=40 or archived[0]['fields']!=[[0,'',0],[36,'',0]]:raise ValueError('expected W owner differs')
    td_len=34;tail_va=va+td_len;tail_len=6;labels=sorted(int(v['va']) for v in json.loads((M.parent/'data-v3/out/data_labels.json').read_text())['data_labels'].values())
    raw=g.refbytes(tail_va,tail_len);runs=g.layout(tail_va,raw,None,labels)
    if raw[:2]!=bytes(2) or runs!=[['B',2],['P',1]] or tail_va+2 not in g.ORIG_SET:raise ValueError('tail layout or original relocation changed')
    target=int.from_bytes(raw[2:6],'little')
    if target!=0x0101142c or archived[0]['tgts'][1]!=target:raise ValueError('tail pointer target changed')
    proposal={'va':tail_va,'tc':'W','size':tail_len,'kind':'phase2-rtti-tail','ns':'','named':False,'head':None,'runs':runs,'align':2}
    built=g.build_entries([proposal])[0]
    if built['fields']!=[[2,'',0]] or built['tgts']!=[target]:raise ValueError('generator disagrees with tail cell')
    # Model compiler addend bytes and ensure the existing self-check accepts the
    # preserved target and rejects a distinct target; no object is generated here.
    ok=g.check_g(built,bytes(6),[(2,'_M3D_%08x'%target,0)],{})
    bad=g.check_g(built,bytes(6),[(2,'_M3D_%08x'%(target+4),0)],{})
    if ok is not None or bad is None:raise ValueError('tail self-check did not distinguish wrong target')
    claims=g.splice.RangeClaims();claims.add(va,td_len);claims.add(tail_va,tail_len)
    result={'schema_version':1,'scope':'uninstalled ownership split proposal; no byte coverage increase','inputs':{'selection_sha256':sha(selection),'archived_manifest_sha256':sha(man)},
       'remove_existing':{'va':va,'size':40,'symbol':archived[0]['sym']},
       'descriptor':{'va':va,'size':td_len,'symbol':'??_R0?AVhkpConstraintViewer@@@8','source_object':'2501.hierarchy.obj','original_reloc_offsets':[0]},
       'remaining_w':proposal,'tail_relocation':{'offset_within_tail':2,'reference_target':target,'same_as_removed_owner':True},
       'model_check':{'normal_target_accepted':True,'wrong_target_rejected':True},
       'status':'not selection-ready: descriptor object import, actual tail compilation, placement/overlap and full controls remain required'}
    with out.open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps({'descriptor_bytes':td_len,'tail_bytes':tail_len,'tail_runs':runs,'target':hex(target),'model_check':result['model_check']}))

if __name__=='__main__':main()
