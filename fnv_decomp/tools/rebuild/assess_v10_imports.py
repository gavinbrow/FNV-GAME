"""Fixed V10 import evidence assessment; no DLL access, native tools or aliases."""
from __future__ import annotations
import argparse
import collections
import gzip
import json
from pathlib import Path
import re
import iat_code68_annotations as annotations
import import_projection as imports
import import_kernel32_extension as bounds
import normal_import_archive as archive

ROOT = Path(__file__).resolve().parents[2]
PINS = dict(catalog=imports.PLAN_PIN,
    fields='03c64e17917dfdacefbea440431fe52442da2bc0ea93fc2c19f4526044d78978',
    observation='d002831408a68ca88fe6adfedeb7288c0092bf7b818ea0be7d63a032994d0351',
    observation_review='8f093e34ada6f7c9e22900987ffbbfbf5182b5129b44e5ec838952a33443040f',
    groups='808c27db9ffdfa170c720c26edab50a42ca4b90bc471c78401203ec9b44f0b8a',
    diagnostic_review='a05ada7d2b8c8f33362fbc9462cbf2dbbf986ae682decf1788a272100faedfe2',
    CRT_review='b5271bc734e8f4d73c7e2fbe72d23af08639eae78d27be9d2daa37d512bb09e1',
    prior_native='0ec9b50fd9d94fb518b820075a3596da8eb9bea0f20d44f36606d37f53581ea3',
    prior_review='b1fe585cf034ef88ca6651fd62bd2512602f921c5760cbe197d0adec8c3910ea',
    recipes='62f2c8da5f0daa912abdf4576328706711c6561eef7f01c93a89cb71ad46fb6c',
    steam_source='eaba017a432bab03e90fb2c8c92a98826b9cdf004d0a22494dbf889bcc6c740c')
HELPER_PINS = {'tools/rebuild/iat_code68_annotations.py':'199e3d51b1ce2eb0e64cb1f780b81c2231cbd8b91a5fdc0460d196b07d7beed9',
    'tools/rebuild/iat_field_annotations.py':annotations.FROZEN_HELPER_SHA256,
    'tools/rebuild/import_projection.py':bounds.PROJECTION_PIN,
    'tools/rebuild/import_kernel32_extension.py':'15177c10e9b6469e0abab5c54e0ec6ef18afb9829cc275bef831795e9f358307',
    'tools/rebuild/normal_import_archive.py':bounds.PARSER_PIN,
    'tools/rebuild/runtime_code_pool.py':imports.NAMESPACE_HELPER_PIN}
SPECS = {'0x00fdf05c':(12,'KERNEL32.dll','EnterCriticalSection',8),
         '0x00fdf100':(53,'KERNEL32.dll','LeaveCriticalSection',13),
         '0x00fdf11c':(60,'KERNEL32.dll','SetThreadPriority',1),
         '0x00fdf488':(203,'steam_api.dll','SteamAPI_RunCallbacks',1)}
STEAM_CELL = '0x00fdf488'
OLD_KERNEL_SHA256 = 'b3932db045db5ed6ef775cd67a3d4045e8739c1417b4ba0994ca2bea78c1a7e9'
require, sha, digest = imports.require, imports.file_hash, annotations.digest


def location(row):
    return (row['component'],row['member'],row['root'],row['section'],row['offset'],row['symbol_index'],row['kind'],row['canonical'])


def typed_source_inventory(text, recipe):
    pattern = re.compile(r'extern\s+"C"\s+__declspec\s*\(\s*dllimport\s*\)\s+void\s+__cdecl\s+SteamAPI_RunCallbacks\s*\(\s*\)\s*;')
    matches = list(pattern.finditer(text))
    require(len(matches)==1 and recipe['source']=='src/staging/blk_006e0000_od.cpp' and recipe['compiler']=='sp1',
            'exact declared Steam source inventory differs')
    line = text.count('\n',0,matches[0].start())+1
    return dict(source=recipe['source'],source_sha256=PINS['steam_source'],recipe_index=2673,
        compiler=recipe['compiler'],flags=recipe['flags'],declaration_line=line,
        declaration=matches[0].group(),source_declared_signature=dict(linkage='extern C',dllimport=True,
            return_type='void',calling_convention='__cdecl',arguments=[]),
        SDK_header_or_binary_ABI_verified=False,owned_DLL_architecture_verified=False,
        owned_DLL_export_verified=False,DLL_load_performed=False,runtime_provider_adopted=False)


def assess(catalog, fields, groups, native, steam_inventory):
    require(len(fields)==45947, 'exact complete V10 field scope differs')
    before = digest(fields); view = annotations.census_view(fields,catalog)
    require(digest(fields)==before, 'normative V10 field ledger mutated')
    cells = imports.catalog(catalog)
    old = {p['original_IAT_va']:p for p in native['proposed_pointer_aliases']}
    require(len(old)==31 and native['native_library_generated'] is True and
            native['all_inputs_tools_sources_stable'] is True, 'accepted prior31 mapping differs')
    actual_groups = {g['symbol']:g for g in groups['groups'] if g['classification']=='IAT'}
    require(len(actual_groups)==4, 'exact four actual V10 IAT groups required')
    results=[]
    for base,(iid,dll,name,count) in SPECS.items():
        cell=cells[base]; canonical=cell['canonical_IAT_symbol']
        require(base not in old and cell['import_id']==iid and cell['dll']==dll and
                cell['export']==dict(kind='name',name=name), 'exact new original catalog identity differs')
        selected=[(i,row) for i,row in enumerate(view,1) if row['canonical']==canonical or
                  row['proof'].get('original_base')==base or row['proof'].get('original_target')==base]
        canonical_selected=[(i,row) for i,row in selected if row['canonical']==canonical]
        group=actual_groups.get(canonical)
        require(group is not None and group['original_bases']==[base], 'exact actual IAT group identity differs')
        blockers=[];evidence=[]
        if len(canonical_selected)!=count:
            blockers.append(dict(reason='CANONICAL_USE_COUNT_DIFFERS',claimed=count,actual=len(canonical_selected)))
        if len({location(row) for i,row in selected})!=len(selected):
            blockers.append(dict(reason='DUPLICATE_PHYSICAL_CELL_USE'))
        if collections.Counter(location(row) for i,row in canonical_selected)!=collections.Counter(location(row) for row in group['included_input_provenance']):
            blockers.append(dict(reason='CANONICAL_DIAGNOSTIC_USE_MULTISET_DIFFERS'))
        for ordinal,row in selected:
            proof=row['proof']
            positive=(row['canonical']==canonical and row['undefined'] is True and row['kind']==6 and
                proof.get('role')=='iat-cell' and proof.get('original_base')==proof.get('original_target')==base and
                proof.get('addend_bits')==0 and proof.get('classification')=='IAT_POINTER_CELL_NOT_FUNCTION_BODY' and
                (row['component']=='actual-entry' or proof.get('import_id')==iid) and
                proof.get('import_pointer_source_conflict') is not True)
            if not positive:blockers.append(dict(field_ordinal=ordinal,location=location(row),reason='UNPROVED_INCLUDED_IAT_USE'))
            evidence.append(dict(field_ordinal=ordinal,normative_row=fields[ordinal-1],census_view_row=row,
                normative_row_sha256=digest(fields[ordinal-1]),census_view_row_sha256=digest(row),use_gate_passed=bool(positive)))
        results.append(dict(original_IAT_va=base,canonical_IAT_symbol=canonical,import_id=iid,dll=dll,
            export=cell['export'],original_export_metadata=next(c['export'] for c in catalog['imports'] if c['original_IAT_va']==base),
            complete_V10_use_count=len(selected),claimed_canonical_use_count=count,canonical_use_count=len(canonical_selected),
            samebase_or_target_other_canonical_uses=len(selected)-len(canonical_selected),
            component_counts=dict(collections.Counter(r['component'] for i,r in selected)),
            all_current_source_use_proofs_pass=not blockers,source_use_blockers=blockers,complete_use_records=evidence,
            native_pointer_symbol=None,native_pointer_identity_verified=False,alias_applied=False,source_ABI_verified=False))
    kernel_results=[r for r in results if r['dll']=='KERNEL32.dll']
    eligible=[r for r in kernel_results if r['all_current_source_use_proofs_pass']]
    kernel_positive=len(eligible)==3
    old_kernel=sorted([p for p in old.values() if p['dll']=='KERNEL32.dll'],key=lambda p:p['original_IAT_va'])
    require(len(old_kernel)==12, 'old KERNEL32 twelve-import identity differs')
    proposal=None;definition=None
    if eligible:
        names=sorted([imports.simple_export_token(p['export']['name']) for p in old_kernel]+
                     [r['export']['name'] for r in eligible])
        new_count=12+len(eligible)
        require(len(names)==len(set(names))==new_count, 'exact eligible KERNEL32 superset differs')
        definition=('LIBRARY "KERNEL32.dll"\nEXPORTS\n'+''.join('    '+name+'\n' for name in names)).encode('ascii')
        stem={13:'thirteen',14:'fourteen',15:'fifteen'}[new_count]
        proposal=dict(dll='KERNEL32.dll',old_library='kernel32-twelve.lib',old_library_sha256=OLD_KERNEL_SHA256,
            new_library='kernel32-'+stem+'.lib',old_import_count=12,new_import_count=new_count,
            prior_pointer_identities=old_kernel,added_cells=[cells[r['original_IAT_va']] for r in eligible],
            proposed_definition='kernel32-'+stem+'.proposed.def',definition_sha256=imports.digest(definition),
            select_instead_of_old_library=True,descriptor_sharing_with_old_library_authorized=False)
    steam=next(r for r in results if r['original_IAT_va']==STEAM_CELL)
    steam['typed_source_inventory']=steam_inventory
    steam['provider_blockers']=['OWNED_STEAM_DLL_ARCHITECTURE_AND_EXPORT_NOT_VERIFIED',
        'SDK_BINARY_ABI_NOT_VERIFIED','RUNTIME_LIFECYCLE_AND_PROVIDER_NOT_ADOPTED']
    steam['native_library_proposed']=False
    unchanged=[dict(file=row['file'],sha256=row['sha256'],bytes=row['bytes']) for row in native['libraries'] if row['file']!='kernel32-twelve.lib']
    unchanged+=native['unchanged_libraries']
    require(len(unchanged)==3, 'other three selected libraries differ')
    return dict(schema_version=1,kind='V10-four-IAT-full-field-source-assessment',status='source-evidence-only',
        complete_normative_field_count=45947,normative_field_canonical_sha256=before,
        census_view_canonical_sha256=digest(view),normative_ledger_unchanged=True,
        census_scope='exact accepted V10 45947-field cohort only',per_cell_censuses=results,
        total_new_cell_use_records=sum(r['complete_V10_use_count'] for r in results),claimed_new_cell_use_records=23,
        kernel32_source_use_gate_pass=kernel_positive,
        eligible_kernel32_cells=[r['original_IAT_va'] for r in eligible],
        blocked_kernel32_cells=[r['original_IAT_va'] for r in kernel_results if not r['all_current_source_use_proofs_pass']],
        proposed_kernel32_replacement=proposal,unchanged_selected_libraries=unchanged,
        prospective_selected_native_cell_count=31+len(eligible),steam_remains_unaliased=True,
        new_native_library_generated=False,new_native_action_authorized=False,alias_applied=False,
        source_ABI_verified=False,runtime_provider_adopted=False,DLL_load_performed=False,imported_API_call_performed=False,
        executable_link_performed=False,Game_source_edited=False,original_objects_or_image_reread=False),definition


def run(args):
    out=Path(args.out).resolve();require(out.is_relative_to(ROOT/'build/rebuild'),'private output required')
    paths={key:Path(getattr(args,key)).resolve() for key in PINS}
    observed={paths[key]:value for key,value in PINS.items()};observed.update({ROOT/p:h for p,h in HELPER_PINS.items()})
    observed[Path(__file__).resolve()]=args.source_sha256
    def stable():require(all(sha(p)==h for p,h in observed.items()),'source/input drift')
    stable();data={key:bounds.read_bound(paths[key],PINS[key]) for key in PINS if key not in ('fields','steam_source')}
    require(paths['steam_source'].stat().st_size<=32*1024*1024,'typed source size bound')
    recipes=data['recipes']['units'] if isinstance(data['recipes'],dict) else data['recipes']
    inventory=typed_source_inventory(paths['steam_source'].read_text(),recipes[2673])
    with gzip.open(paths['fields'],'rb') as stream:
        raw=stream.read(256*1024*1024+1);require(len(raw)<=256*1024*1024 and stream.read(1)==b'','field decompression bound')
    fields=json.loads(raw);del raw
    result,definition=assess(data['catalog'],fields,data['groups'],data['prior_native'],inventory)
    old_path=paths['prior_native'].parent/'kernel32-twelve.lib'
    require(sha(old_path)==OLD_KERNEL_SHA256,'old KERNEL32 archive drift')
    parsed=archive.read_archive(old_path);old=[p for p in data['prior_native']['proposed_pointer_aliases'] if p['dll']=='KERNEL32.dll']
    require(len(parsed['imports'])==12 and all(sum(i['dll']==p['dll'] and i['export']==p['export'] and
        i['pointer_symbol']==p['proposed_pointer_symbol'] for i in parsed['imports'])==1 for p in old),'old actual native pointers differ')
    observed[old_path]=OLD_KERNEL_SHA256
    for row in result['unchanged_selected_libraries']:
        path=paths['prior_native'].parent/row['file'] if 'file' in row else ROOT/'build/rebuild/import-native-main-v2'/row['library']
        require(sha(path)==row['sha256'],'unchanged selected library drift');observed[path]=row['sha256']
    result['inputs']={key+'_sha256':value for key,value in PINS.items()}
    result['source_sha256']={str(p.relative_to(ROOT)).replace('\\','/'):h for p,h in observed.items() if p.is_relative_to(ROOT/'tools')}
    result['typed_source_read_only']=True;result['owned_Steam_DLL_read_or_loaded']=False
    stable();out.mkdir(parents=True,exist_ok=False);created=[]
    try:
        if definition is not None:
            path=out/result['proposed_kernel32_replacement']['proposed_definition']
            with path.open('xb') as stream:created.append(path);stream.write(definition)
        stable();path=out/'assessment.json'
        with path.open('x') as stream:created.append(path);json.dump(result,stream,indent=2,sort_keys=True);stream.write('\n')
        stable()
    except BaseException:
        for path in reversed(created):path.unlink()
        out.rmdir();raise
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(__doc__)
    for key in list(PINS)+['out','source_sha256']:parser.add_argument('--'+key.replace('_','-'),required=True)
    result=run(parser.parse_args());print(json.dumps(dict(status=result['status'],fields=45947,uses=23,
        kernel32_source_use_gate_pass=result['kernel32_source_use_gate_pass'],steam_unaliased=True)))
