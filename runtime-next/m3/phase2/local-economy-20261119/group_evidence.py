"""Batch repeated evidence retrieval while retaining every original job identity."""
import collections,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[4]
P=R/'runtime-next/m3/out/phase2-web-backlog-20261119'
O=R/'runtime-next/m3/out/phase2-local-economy-20261119/evidence-groups'
KINDS={'source_identity_reconciliation','class_source_recovery','class_identity_recovery'}

def main():
    source=P/'job-ledger.json';raw=source.read_bytes();rows=json.loads(raw)
    groups=collections.defaultdict(list);other=[]
    for row in rows:
        paths=tuple(sorted(set(row.get('source_files',[]))))
        if row['kind'] in KINDS and paths:groups[row['kind'],paths].append(row['id'])
        else:other.append(row['id'])
    records=[];stats={}
    for (kind,paths),ids in sorted(groups.items()):
        key=json.dumps([kind,paths],separators=(',',':')).encode()
        records.append({'group_id':hashlib.sha256(key).hexdigest(),'kind':kind,'source_paths':paths,'job_ids':ids,'repeated_pathset':len(ids)>1})
    for kind in sorted(KINDS):
        selected=[g for g in records if g['kind']==kind]
        stats[kind]={'jobs':sum(r['kind']==kind for r in rows),'retrieval_groups_with_sources':len(selected),'repeated_groups':sum(len(g['job_ids'])>1 for g in selected),'jobs_in_repeated_groups':sum(len(g['job_ids']) for g in selected if len(g['job_ids'])>1)}
    covered=[i for g in records for i in g['job_ids']]+other
    if len(covered)!=len(rows) or len(set(covered))!=len(rows) or set(covered)!={r['id'] for r in rows}:raise ValueError('lost or duplicated job')
    if source.read_bytes()!=raw:raise ValueError('ledger changed')
    O.mkdir(parents=True,exist_ok=False)
    result={'ledger_sha256':hashlib.sha256(raw).hexdigest(),'jobs_preserved':len(rows),'stats':stats,'groups':records,'unbatched_job_ids':other,'scope':'evidence retrieval grouping only; no queue mutation, identity merge, priority decision or completion claim','reuse_gate':'Every source read must match its frozen profile hash; macro/namespace/packing/compiler contexts and native type identity remain separate.'}
    (O/'groups.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'jobs_preserved':len(rows),'stats':stats}))

if __name__=='__main__':main()
