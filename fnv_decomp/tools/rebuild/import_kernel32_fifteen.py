"""Strict Win32-only KERNEL32 twelve-to-fifteen import preparation and identity join."""
from __future__ import annotations
import argparse,copy,gzip,json,re
from pathlib import Path
import assess_v10_imports as assessment_tool
import import_projection as imports
import import_kernel32_extension as bounds
import normal_import_archive as archive

ROOT=Path(__file__).resolve().parents[2]
PINS=dict(catalog=imports.PLAN_PIN,
    assessment='e3ee933ca871553453ff0bac698b33a6eb44bf6c2442405c83acfe95b0075abe',
    assessment_review='d5f52a7b43938c03a9ecdd503d4dd51505c90b18c88e81d7bf776b8615c6a2ad',
    fields='03c64e17917dfdacefbea440431fe52442da2bc0ea93fc2c19f4526044d78978',
    groups='808c27db9ffdfa170c720c26edab50a42ca4b90bc471c78401203ec9b44f0b8a',
    prior_native='0ec9b50fd9d94fb518b820075a3596da8eb9bea0f20d44f36606d37f53581ea3',
    prior_review='b1fe585cf034ef88ca6651fd62bd2512602f921c5760cbe197d0adec8c3910ea')
HELPER_PINS=dict(assessment_tool.HELPER_PINS,**{'tools/rebuild/assess_v10_imports.py':
    'fe148aafdcd4af8dca5b89b2815df8acebbbc7832fbacdde6aa68b63d48a2a68'})
DELTA={base:spec for base,spec in assessment_tool.SPECS.items() if spec[1]=='KERNEL32.dll'}
OLD_KERNEL_SHA256=assessment_tool.OLD_KERNEL_SHA256
UNCHANGED=(('user32-sixteen.lib','19c6cb80185784829b38c2e6d03672c5b06cbf2e96c4245a4c6b73adc973e132',4742),
    ('provider-000.lib','2627bd866f27b6d867d85f305e1d0fd0a002c4dc14f5037189c1f645d0dfdd91',1704),
    ('provider-002.lib','ed07b437804514dbd5f61888fb2051a83a694ab3563585183146547ec0045c9a',1944))
FALSE_FLAGS=bounds.FALSE_FLAGS
require,sha=imports.require,imports.file_hash


def validate_fields(assessment,fields,groups,catalog,native):
    steam=next(r for r in assessment['per_cell_censuses'] if r['original_IAT_va']==assessment_tool.STEAM_CELL)
    replay,definition=assessment_tool.assess(catalog,fields,groups,native,steam['typed_source_inventory'])
    require(all(assessment.get(key)==value for key,value in replay.items()),'complete V10 assessment replay differs')
    require(replay['kernel32_source_use_gate_pass'] is True and
            set(replay['eligible_kernel32_cells'])==set(DELTA) and not replay['blocked_kernel32_cells'],
            'strict fifteen-import source delta is not fully eligible')
    return definition


def prepare(catalog,assessment,review,native):
    cells=imports.catalog(catalog)
    require(review.get('kind')=='v10-import-assessment-independent-outcome-review' and
            review.get('schema_version')==1 and review.get('status')=='accepted_metadata_only' and
            review['assessment_sha256']==PINS['assessment'] and
            assessment['kernel32_source_use_gate_pass'] is True and
            set(assessment['eligible_kernel32_cells'])==set(DELTA) and not assessment['blocked_kernel32_cells'],
            'accepted strict Win32 source assessment differs')
    old=native['proposed_pointer_aliases']
    require(native.get('kind')=='fnv-v8-four-import-successor-native-collection' and native.get('schema_version')==1 and
            len(old)==len({p['original_IAT_va'] for p in old})==31 and native['native_library_generated'] is True and
            native['all_inputs_tools_sources_stable'] is True and all(native.get(k) is False for k in FALSE_FLAGS),
            'prior 31-pointer identity/state differs')
    for p in old:
        cell=cells[p['original_IAT_va']]
        require(all(p[k]==cell[k] for k in ('canonical_IAT_symbol','dll','export')) and
                p['alias_applied'] is False and p['source_ABI_approved'] is False and p['runtime_provider_adopted'] is False,
                'old pointer identity or promotion differs')
    require(not set(DELTA)&{p['original_IAT_va'] for p in old},'new Win32 cells overlap prior mappings')
    prior=sorted([p for p in old if p['dll']=='KERNEL32.dll'],key=lambda p:p['original_IAT_va'])
    require(len(prior)==12,'old KERNEL32 twelve-cell scope differs')
    for base,(iid,dll,name,count) in DELTA.items():
        require(cells[base]['import_id']==iid and cells[base]['dll']==dll and cells[base]['export']==dict(kind='name',name=name),
                'new Win32 catalog identity differs')
    chosen=[cells[p['original_IAT_va']] for p in prior]+[cells[base] for base in DELTA]
    metadata={row['original_IAT_va']:row for row in catalog['imports']}
    chosen=[dict(c,original_export_metadata=metadata[c['original_IAT_va']]['export'],
                 lookup_source=metadata[c['original_IAT_va']].get('lookup_source')) for c in sorted(chosen,key=lambda c:c['original_IAT_va'])]
    names=sorted(imports.simple_export_token(c['export']['name']) for c in chosen)
    require(len(names)==len(set(names))==15,'strict fifteen-export superset differs')
    definition=('LIBRARY "KERNEL32.dll"\nEXPORTS\n'+''.join('    '+name+'\n' for name in names)).encode('ascii')
    proposal=assessment['proposed_kernel32_replacement']
    require(proposal['old_library_sha256']==OLD_KERNEL_SHA256 and proposal['new_import_count']==15 and
            proposal['prior_pointer_identities']==prior and proposal['definition_sha256']==imports.digest(definition),
            'accepted proposed Win32 superset differs')
    unchanged=[dict(file=name,sha256=h,bytes=size) for name,h,size in UNCHANGED]
    user=[row for row in native['libraries'] if row['file']=='user32-sixteen.lib']
    require(len(user)==1 and all(user[0][k]==unchanged[0][k] for k in ('file','sha256','bytes')),
            'unchanged USER32 native identity differs')
    other={row['library']:row['sha256'] for row in native['unchanged_libraries']}
    require(all(other.get(name)==h for name,h,size in UNCHANGED[1:]),'unchanged GDI32/SHELL32 identities differ')
    steam=copy.deepcopy(next(r for r in assessment['per_cell_censuses'] if r['original_IAT_va']==assessment_tool.STEAM_CELL))
    require(steam['native_library_proposed'] is False and len(steam['provider_blockers'])==3 and
            steam['native_pointer_symbol'] is None,'Steam source-only context was promoted')
    return dict(schema_version=1,kind='fnv-kernel32-fifteen-import-request',status='offline-prepared',
        replacement=dict(old_library='kernel32-twelve.lib',old_library_sha256=OLD_KERNEL_SHA256,
                         new_library='kernel32-fifteen.lib',old_import_count=12,new_import_count=15),
        cells=chosen,prior_pointer_aliases=copy.deepcopy(old),prior_kernel32_aliases=prior,
        unchanged_libraries=unchanged,new_kernel32_all_use_censuses=[copy.deepcopy(r) for r in assessment['per_cell_censuses'] if r['dll']=='KERNEL32.dll'],
        complete_V10_field_count=45947,new_Win32_use_count=22,Steam_inventory_context=steam,
        Steam_remains_unaliased=True,Steam_native_library_proposed=False,
        definition=dict(file='kernel32-fifteen.def',sha256=imports.digest(definition)),
        normative_field_canonical_sha256=assessment['normative_field_canonical_sha256'],
        census_view_canonical_sha256=assessment['census_view_canonical_sha256'],
        global_caller_census_verified=False,native_library_generated=False,**FALSE_FLAGS),definition


def reconcile(request,parsed,request_sha256):
    require(request.get('kind')=='fnv-kernel32-fifteen-import-request' and request.get('schema_version')==1 and
            request.get('native_library_generated') is False and request.get('global_caller_census_verified') is False and
            request.get('Steam_remains_unaliased') is True and request.get('Steam_native_library_proposed') is False and
            all(request.get(k) is False for k in FALSE_FLAGS) and isinstance(request_sha256,str) and
            re.fullmatch('[0-9a-f]{64}',request_sha256),'Win32 request state differs')
    require(request['replacement']==dict(old_library='kernel32-twelve.lib',old_library_sha256=OLD_KERNEL_SHA256,
            new_library='kernel32-fifteen.lib',old_import_count=12,new_import_count=15),'Win32 replacement scope differs')
    require(parsed['both_indexes_agree'] is True and len(parsed['imports'])==15 and len(parsed['ordinary_members'])==3 and
            all(i['machine']==0x14c for i in parsed['imports']),'new native archive shape differs')
    old={p['original_IAT_va']:p for p in request['prior_pointer_aliases']}
    require(len(old)==31 and len(request['cells'])==15 and not set(DELTA)&set(old),'prior/new Win32 cell coverage differs')
    aliases=[copy.deepcopy(p) for p in old.values() if p['dll']!='KERNEL32.dll']
    for cell in request['cells']:
        hits=[i for i in parsed['imports'] if i['dll']==cell['dll']=='KERNEL32.dll' and i['export']==cell['export']]
        require(len(hits)==1,'actual Win32 DLL/export differs')
        item=hits[0];base=cell['original_IAT_va']
        require(item['import_type']==0 and item['pointer_symbol']=='__imp_'+item['symbol'] and
                cell['canonical_IAT_symbol']==imports.unresolved(base,'iat-cell'),'pointer/canonical role differs')
        if base in old:
            require(item['pointer_symbol']==old[base]['proposed_pointer_symbol'] and cell['export']==old[base]['export'] and
                    cell['dll']==old[base]['dll'],'old Win32 pointer identity changed')
        else:
            require(base in DELTA and (cell['import_id'],cell['dll'],cell['export']['name'])==DELTA[base][:3],
                    'unexpected new import or Steam substitution')
        aliases.append(dict(original_IAT_va=base,canonical_IAT_symbol=cell['canonical_IAT_symbol'],
            proposed_pointer_symbol=item['pointer_symbol'],dll=cell['dll'],export=cell['export'],library='kernel32-fifteen.lib',
            member_offset=item['member_offset'],pointer_indirection_preserved=True,alias_applied=False,
            source_ABI_approved=False,runtime_provider_adopted=False))
    require(len(aliases)==34 and all(len({p[k] for p in aliases})==34 for k in ('original_IAT_va','canonical_IAT_symbol','proposed_pointer_symbol'))
            and all(p['alias_applied'] is False and p['source_ABI_approved'] is False and p['runtime_provider_adopted'] is False for p in aliases)
            and all(p['dll']!='steam_api.dll' for p in aliases),'combined pointer coverage/promotion differs')
    return dict(schema_version=1,kind='fnv-kernel32-fifteen-import-native-collection',status='collected-awaiting-independent-conformance',
        request_sha256=request_sha256,inputs=request['inputs'],source_sha256=request['source_sha256'],replacement=request['replacement'],
        library=dict(file='kernel32-fifteen.lib',sha256=parsed['archive_sha256'],bytes=parsed['archive_bytes']),parsed_archive=parsed,
        proposed_pointer_aliases=sorted(aliases,key=lambda p:p['original_IAT_va']),unchanged_libraries=request['unchanged_libraries'],
        old_31_pointer_identities_preserved=True,replacement_identity_verified=True,native_library_generated=True,
        Steam_remains_unaliased=True,Steam_native_library_proposed=False,global_caller_census_verified=False,**FALSE_FLAGS)


def run(args):
    out=Path(args.out).resolve();require(out.is_relative_to(ROOT/'build/rebuild'),'private output required')
    paths={k:Path(getattr(args,k)).resolve() for k in PINS};observed={paths[k]:h for k,h in PINS.items()}
    observed.update({ROOT/p:h for p,h in HELPER_PINS.items()});observed[Path(__file__).resolve()]=args.source_sha256
    def stable():require(all(sha(p)==h for p,h in observed.items()),'source/input drift')
    stable();data={k:bounds.read_bound(paths[k],PINS[k]) for k in PINS if k!='fields'}
    with gzip.open(paths['fields'],'rb') as stream:
        raw=stream.read(256*1024*1024+1);require(len(raw)<=256*1024*1024 and stream.read(1)==b'','field decompression bound')
    fields=json.loads(raw);del raw
    validate_fields(data['assessment'],fields,data['groups'],data['catalog'],data['prior_native'])
    require(data['prior_review']['status']=='accepted_metadata_conformance_only' and
            data['prior_review']['collection_sha256']==PINS['prior_native'],'prior native review differs')
    request,definition=prepare(data['catalog'],data['assessment'],data['assessment_review'],data['prior_native'])
    old=paths['prior_native'].parent/'kernel32-twelve.lib';require(sha(old)==OLD_KERNEL_SHA256,'old Kernel12 drift')
    parsed=archive.read_archive(old);require(len(parsed['imports'])==12,'old native count differs')
    for p in request['prior_kernel32_aliases']:
        require(sum(i['dll']==p['dll'] and i['export']==p['export'] and i['pointer_symbol']==p['proposed_pointer_symbol'] for i in parsed['imports'])==1,
                'old actual pointer identity differs')
    observed[old]=OLD_KERNEL_SHA256
    for row in request['unchanged_libraries']:
        path=paths['prior_native'].parent/row['file'] if row['file']=='user32-sixteen.lib' else ROOT/'build/rebuild/import-native-main-v2'/row['file']
        require(sha(path)==row['sha256'] and path.stat().st_size==row['bytes'],'unchanged library drift');observed[path]=row['sha256']
    request['inputs']={k+'_sha256':h for k,h in PINS.items()}
    request['source_sha256']={str(p.relative_to(ROOT)).replace('\\','/'):h for p,h in observed.items() if p.is_relative_to(ROOT/'tools')}
    stable();out.mkdir(parents=True,exist_ok=False);created=[]
    try:
        p=out/'kernel32-fifteen.def'
        with p.open('xb') as stream:created.append(p);stream.write(definition)
        stable();p=out/'preparation.json'
        with p.open('x') as stream:created.append(p);json.dump(request,stream,indent=2,sort_keys=True);stream.write('\n')
        stable()
    except BaseException:
        for p in reversed(created):p.unlink()
        out.rmdir();raise
    return request


if __name__=='__main__':
    parser=argparse.ArgumentParser(__doc__)
    for key in list(PINS)+['out','source_sha256']:parser.add_argument('--'+key.replace('_','-'),required=True)
    result=run(parser.parse_args());print(json.dumps(dict(status=result['status'],kernel32_imports=15,pointer_proposals=34,Steam_unaliased=True)))
