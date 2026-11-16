"""Derived-only qualification of frozen cohort response preparation.

Complete saved validator results are carried as accepted historical evidence,
never reconstructed as fresh admission. Only approved JSON/RSP bytes and public
kernel source are read. Historical input paths are never statted or opened.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import time

import cohort_prepare_manifest as prototype
import coff_inventory as inventory_tools

ROOT=Path(__file__).resolve().parents[2]
PROTO_PIN='7b8a070000543a65b27499b75cdcd60ab457dc5fbf8396803f98b8ef27a39424'
PINS=dict(prototype.KERNEL_PINS,**{'tools/rebuild/cohort_prepare_manifest.py':PROTO_PIN,
    'tools/rebuild/coff_inventory.py':'3518c044738046e7cd9c8be37a3b1077af750fb2e7a19db793b09999a07ee0d2'})
OWNED=('tools/rebuild/cohort_prepare_shadow.py','tests/rebuild/test_cohort_prepare_shadow.py',
       'docs/rebuild/COHORT-PREPARE-SHADOW.md')
ROLES={'baseline_result','baseline_response','baseline_outcome_review','cohort_result','cohort_response',
       'cohort_input_review','cohort_prepared_review','cohort_outcome_review'}
MANIFEST_KEYS={'schema_version','kind','phase','scope','profile','kernel_sha256','files','historical_roles','output_relative'}
REVIEW_KEYS={'schema_version','kind','approved','root_authorized','reviewer','independent_source_input_review_pass',
    'historical_validator_results_accepted','saved_reviews_accepted','manifest_sha256','kernel_sha256','files_sha256',
    'allow_original_archive_native_game','source_sha256'}
PROFILE={
 'saved-wave8-v1':dict(base_kind='fixed-broader-frontier-link-diagnostic',kind='fixed-wave8-CODE59-ModelLoader-link-diagnostic',
    kernel='application_wave8_diagnostic',additions=['code','eh'],replacements=[],roles={
      'code':('cohort','frontier-code-production-v5-v1/frontier-code.lib'),
      'eh':('cohort','parent-eh-model-loader-projection-v1/component.obj')}),
 'saved-wave9-v1':dict(base_kind='fixed-wave8-CODE59-ModelLoader-link-diagnostic',kind='fixed-wave9-three-CODE-four-IAT-link-diagnostic',
    kernel='application_wave9_diagnostic',additions=['code'],replacements=[('old_kernel','new_kernel'),('old_user','new_user')],roles={
      'code':('cohort','frontier-wave-v7-production-v1/V7-code.lib'),
      'old_kernel':('baseline','import-kernel32-nine-native-v1/kernel32-nine.lib'),
      'old_user':('baseline','application-link-inputs-v2/provider-003.lib'),
      'new_kernel':('cohort','import-v8-four-native-v1/kernel32-twelve.lib'),
      'new_user':('cohort','import-v8-four-native-v1/user32-sixteen.lib')})}
FALSE=dict(production_admission_approved=False,fresh_original_inputs_checked=False,fresh_MATCH_performed=False,
           fresh_native_conformance_performed=False,native_operations_performed=False,original_or_archive_read=False,
           game_execution_performed=False,provider_selected=False,runtime_eligible=False,automatic_adoption=False)
MAX_FILE_BYTES=64*1024**2
MAX_TOTAL_BYTES=96*1024**2


def require(condition,message):
    if not condition:raise ValueError(message)


file_hash=prototype.file_hash


def digest(value):
    h=hashlib.sha256();encoder=json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)
    for chunk in encoder.iterencode(value):h.update(chunk.encode('ascii'))
    return h.hexdigest()


def strict_json(text):
    def unique(pairs):
        value={}
        for key,item in pairs:
            require(key not in value,'duplicate saved JSON key');value[key]=item
        return value
    def nonfinite(_):raise ValueError('nonfinite saved JSON number')
    return json.loads(text,object_pairs_hook=unique,parse_constant=nonfinite)


def source_gate():
    require(Path(prototype.__file__).resolve()==ROOT/'tools/rebuild/cohort_prepare_manifest.py'
            and Path(inventory_tools.__file__).resolve()==ROOT/'tools/rebuild/coff_inventory.py',
            'unexpected loaded shadow producer module')
    for relative,h in PINS.items():require(file_hash(ROOT/relative)==h,'frozen shadow source dependency changed')
    modules=prototype.kernels()
    require(set(modules)=={'application_wave8_diagnostic','application_wave9_diagnostic','application_link_diagnostic'}
            and all(Path(module.__file__).resolve()==ROOT/'tools/rebuild'/(name+'.py') for name,module in modules.items()),
            'unexpected loaded response kernel module')
    return modules


def validate_manifest(manifest):
    require(type(manifest) is dict and set(manifest)==MANIFEST_KEYS,'exact shadow manifest schema required')
    require(type(manifest['schema_version']) is int and manifest['schema_version']==1
            and manifest['kind']=='cohort-saved-result-shadow-v1' and manifest['phase']=='derived-shadow-only'
            and manifest['scope'] in ('authored-fixture-only','accepted-saved-cohort')
            and type(manifest['profile']) is str and manifest['profile'] in PROFILE,'closed derived-only shadow profile required')
    require(manifest['kernel_sha256']==PINS,'fixed shadow producer pins required')
    prototype.relative(manifest['output_relative'],single=True)
    require(type(manifest['files']) is dict and set(manifest['files'])==ROLES,'complete eight-role saved evidence required')
    for role,spec in manifest['files'].items():
        require(type(spec) is dict and set(spec)=={'path','sha256'} and isinstance(spec['path'],str)
                and Path(spec['path']).is_absolute(),'exact absolute derived file specification required')
        require(Path(spec['path']).suffix.lower()==('.rsp' if role.endswith('response') else '.json'), 'derived JSON/RSP roles only')
        prototype.sha(spec['sha256'])
    require(type(manifest['historical_roles']) is dict and set(manifest['historical_roles'])==set(PROFILE[manifest['profile']]['roles']),
            'complete closed historical edit roles required')
    for name,binding in manifest['historical_roles'].items():
        require(type(binding) is dict and set(binding)==prototype.IDENTITY_KEYS,'complete historical physical binding required')
        prototype.sha(binding['sha256'])
        require(all(type(binding[k]) is int and binding[k]>=0 for k in ('size','device','inode')),'typed historical physical metadata required')
        _,relative=PROFILE[manifest['profile']]['roles'][name];token=str(ROOT/'build/rebuild'/relative)
        require(binding['requested_path']==binding['path']==token,'exact frozen selected historical token required')


def saved_result(value, expected_kind):
    required={'kind','status','command','response_sha256','input_bindings','provenance','aliases',
       'CRT_diagnostic_bindings','default_libraries','selected_supplementary_providers',
       'full_included_field_count','selected_game_function_provider_count','ordinary_prepared_count',
       'native_LINK_performed','executable_execution','runtime_eligible','provider_adopted','link_ready',
       'whole_DATA_included','namespace_only','logical_CODE_address_only_aliases','unreviewed_CRT_aliases'}
    require(type(value) is dict and required<=set(value) and value['kind']==expected_kind
            and value['status']=='prepared-no-native-LINK','complete frozen prepared-result structure required')
    require(all(value[k] is False for k in ('native_LINK_performed','executable_execution','runtime_eligible',
            'provider_adopted','link_ready','whole_DATA_included')) and value['namespace_only'] is True
            and value['logical_CODE_address_only_aliases']==[] and value['unreviewed_CRT_aliases']==[],
            'historical namespace-only admission scope differs')
    require(type(value['command']) is list and len(value['command'])==2
            and all(type(s) is str for s in value['command']) and value['command'][1].startswith('@'), 'saved response command identity required')
    prototype.sha(value['response_sha256'])
    require(type(value['input_bindings']) is list and type(value['provenance']) is dict
            and type(value['aliases']) is list and type(value['CRT_diagnostic_bindings']) is dict
            and type(value['default_libraries']) is dict and type(value['selected_supplementary_providers']) is list,
            'full proof groups cannot be substituted with flags')
    for binding in value['input_bindings']:
        require(type(binding) is dict and set(binding)==prototype.IDENTITY_KEYS
                and all(type(binding[k]) is int and binding[k]>=0 for k in ('size','device','inode'))
                and all(isinstance(binding[k],str) and binding[k] for k in ('requested_path','path')),
                'complete typed historical input identity required')
        prototype.sha(binding['sha256'])
    for k in ('full_included_field_count','selected_game_function_provider_count','ordinary_prepared_count'):
        require(type(value[k]) is int and value[k]>0,'typed historical cohort count required')
    require(all(type(rows) is list and all(type(r) is dict for r in rows) for rows in value['provenance'].values()),
            'full normative provenance rows required')
    require(sum('proof' in r for rows in value['provenance'].values() for r in rows)==value['full_included_field_count'],
            'complete normative field/provenance count differs')
    require(all(type(r) is dict and type(r.get('enabled')) is bool and isinstance(r.get('canonical'),str)
                and isinstance(r.get('native_pointer'),str) for r in value['aliases']),'full per-cell alias facts required')
    require(len({r['canonical'] for r in value['aliases']})==len(value['aliases']),'duplicate historical alias identity')
    require(type(value['CRT_diagnostic_bindings'].get('tokens')) is list,'complete CRT gate token result required')


def historical_binding(result, expected):
    # No Path.resolve/stat/hash here: these identities are historical evidence.
    matches=[row for row in result['input_bindings'] if row.get('requested_path')==expected['requested_path']]
    require(matches and all(digest(row)==digest(expected) for row in matches),'historical selected physical role binding differs')
    return expected['requested_path']


def evaluate_shadow(manifest,blobs):
    """Pure saved-evidence evaluation except the fixed public source pin gate."""
    validate_manifest(manifest);mods=source_gate()
    require(type(blobs) is dict and set(blobs)==ROLES and all(type(b) is bytes and len(b)<=MAX_FILE_BYTES for b in blobs.values())
            and sum(map(len,blobs.values()))<=MAX_TOTAL_BYTES,'bounded complete derived blobs required')
    for role,raw in blobs.items():require(hashlib.sha256(raw).hexdigest()==manifest['files'][role]['sha256'],'derived file byte identity differs: '+role)
    decoded={role:strict_json(raw.decode('utf-8-sig')) for role,raw in blobs.items() if not role.endswith('response')}
    require(all(type(value) is dict and value for value in decoded.values()),'complete JSON result/review objects required')
    before=digest(decoded);profile=PROFILE[manifest['profile']];base=decoded['baseline_result'];cohort=decoded['cohort_result']
    saved_result(base,profile['base_kind']);saved_result(cohort,profile['kind'])
    for name,result in (('baseline',base),('cohort',cohort)):
        response_role=name+'_response';expected=manifest['files'][response_role]
        require(result['command'][1]=='@'+expected['path'] and result['response_sha256']==expected['sha256'],
                'historical response path/hash differs from saved result')
        own='tools/rebuild/'+('application_wave9_diagnostic.py' if name=='cohort' and manifest['profile']=='saved-wave9-v1'
                             else 'application_wave8_diagnostic.py')
        # V7 baseline predates V8. Its complete source identities are carried but
        # not misrepresented as having been produced by a newer preparer.
        if not (name=='baseline' and manifest['profile']=='saved-wave8-v1'):
            rows=[r for r in result['input_bindings'] if r.get('requested_path')==str(ROOT/own)]
            require(rows and all(r.get('sha256')==PINS[own] for r in rows),'saved preparer source identity differs')
    prior_iat=['/ALTERNATENAME:'+r['canonical']+'='+r['native_pointer'] for r in base['aliases'] if r['enabled']]
    new_iat=['/ALTERNATENAME:'+r['canonical']+'='+r['native_pointer'] for r in cohort['aliases'] if r['enabled']]
    allowed_iat=['/ALTERNATENAME:'+r['canonical']+'='+r['native_pointer'] for r in cohort['aliases']]
    prior_crt=base['CRT_diagnostic_bindings']['tokens'];new_crt=cohort['CRT_diagnostic_bindings']['tokens']
    require(cohort['CRT_diagnostic_bindings'].get('inherited_tokens_to_remove')==prior_crt,'complete CRT inherited scope differs')
    selected={}
    for name,expected in manifest['historical_roles'].items():
        owner,_=profile['roles'][name];selected[name]=historical_binding(base if owner=='baseline' else cohort,expected)
    baseline_text=blobs['baseline_response'].decode('utf-8-sig')
    old_out=Path(manifest['files']['baseline_response']['path']).parent
    historical_out=Path(manifest['files']['cohort_response']['path']).parent
    additions=[selected[name] for name in profile['additions']]
    if manifest['profile']=='saved-wave8-v1':
        tokens=mods[profile['kernel']].response_tokens(baseline_text,old_out,historical_out,additions,prior_iat,prior_crt,new_iat,new_crt)
    else:
        replacements=[(selected[old],selected[new]) for old,new in profile['replacements']]
        tokens=mods[profile['kernel']].response_tokens(baseline_text,old_out,historical_out,replacements,additions[0],
                prior_iat,prior_crt,allowed_iat,new_iat,new_crt)
    response=mods['application_link_diagnostic'].response_text(tokens).replace('\n',os.linesep).encode('utf-8')
    require(response==blobs['cohort_response'],'exact saved response bytes not reproduced')
    require(digest(decoded)==before,'complete saved result/review structure changed')
    preserved={role:dict(raw_sha256=hashlib.sha256(blobs[role]).hexdigest(),canonical_json_sha256=digest(value),
                complete_top_level_sha256={k:digest(v) for k,v in value.items()}) for role,value in decoded.items()}
    facts=dict(schema_version=1,kind='derived-cohort-shadow-evaluation-v1',profile=manifest['profile'],
        response_sha256=hashlib.sha256(response).hexdigest(),response_byte_equivalence=True,
        complete_saved_structure_sha256=before,preserved=preserved,
        provenance_sha256={name:digest(result['provenance']) for name,result in (('baseline',base),('cohort',cohort))},
        historical_edit_bindings=manifest['historical_roles'],
        historical_snapshot_acceptance_external=True,pure_evaluation_admission_verified=False,
        reused_checks=['complete frozen validator results and all saved review contents',
                       'historical namespace/fullproof/MATCH/native conformance/input identities; no original replay'],
        derived_checks=['exact saved JSON/RSP bytes and public source pins','historical role and alias joins from complete results',
                        'response byte equivalence at historical target path','lossless full-result/provenance preservation'],**FALSE)
    return response,facts


def budget(start,output=None):
    require(time.monotonic()-start<=900,'shadow sampled 15-minute budget')
    peak=inventory_tools.peak_memory_bytes();require(peak is not None and peak<=1024**3,'shadow sampled 1-GiB peak memory budget')
    size=0
    if output is not None:
        for parent,dirs,files in os.walk(output,followlinks=False):
            require(all(not (Path(parent)/n).is_symlink() for n in dirs+files),'shadow output symlink')
            for name in files:size+=(Path(parent)/name).stat().st_size
        require(size<=128*1024**2,'shadow 128-MiB output budget')
    return dict(seconds=round(time.monotonic()-start,3),peak_memory_bytes=peak,output_bytes=size)


def read_json(path,expected,max_bytes=1024**2):
    require(Path(path).stat().st_size<=max_bytes,'bounded control JSON required');raw=Path(path).read_bytes()
    require(len(raw)<=max_bytes and hashlib.sha256(raw).hexdigest()==expected,'loaded control byte identity differs')
    return strict_json(raw.decode('utf-8-sig'))


def validate_review(review,manifest,manifest_sha256):
    require(type(review) is dict and set(review)==REVIEW_KEYS,'exact shadow source/input review schema required')
    require(review.get('kind')=='cohort-shadow-source-input-review-v1' and type(review.get('schema_version')) is int and review.get('schema_version')==1
            and review.get('approved') is True and review.get('root_authorized') is True
            and type(review.get('reviewer')) is str and review['reviewer'].strip()
            and review.get('independent_source_input_review_pass') is True
            and review.get('historical_validator_results_accepted') is True and review.get('saved_reviews_accepted') is True
            and review.get('manifest_sha256')==manifest_sha256 and review.get('kernel_sha256')==PINS
            and review.get('files_sha256')=={k:v['sha256'] for k,v in manifest['files'].items()}
            and review.get('allow_original_archive_native_game') is False
            and type(review.get('source_sha256')) is dict and set(review['source_sha256'])==set(OWNED),
            'exact independent source/input shadow authority required')
    prototype.sha(review['manifest_sha256'])
    for h in review['source_sha256'].values():prototype.sha(h)


def run(manifest_path,manifest_sha256,review_path,review_sha256):
    start=time.monotonic();manifest_path=Path(manifest_path).resolve(strict=True);review_path=Path(review_path).resolve(strict=True)
    manifest=read_json(manifest_path,manifest_sha256);validate_manifest(manifest)
    review=read_json(review_path,review_sha256)
    validate_review(review,manifest,manifest_sha256)
    diagnostic=source_gate()['application_link_diagnostic'];bindings=[]
    for relative,h in {**PINS,**review['source_sha256']}.items():
        require(file_hash(ROOT/relative)==h,'shadow source/input pin changed');bindings.append(diagnostic.identity(ROOT/relative))
    for path,h in ((manifest_path,manifest_sha256),(review_path,review_sha256)):
        row=diagnostic.identity(path);require(row['sha256']==h,'control file changed after loading');bindings.append(row)
    allowed=manifest_path.parent if manifest['scope']=='authored-fixture-only' else ROOT/'build/rebuild'
    blobs={};total=0
    for role,spec in manifest['files'].items():
        path=Path(spec['path']);require(path.resolve(strict=True).is_relative_to(allowed.resolve()),'derived role outside reviewed data root')
        require(path.stat().st_size<=MAX_FILE_BYTES,'derived role file size bound');raw=path.read_bytes();total+=len(raw)
        require(total<=MAX_TOTAL_BYTES and hashlib.sha256(raw).hexdigest()==spec['sha256'],'derived role bytes/total bound')
        row=diagnostic.identity(path);require(row['sha256']==spec['sha256'],'derived role changed after loading');bindings.append(row);blobs[role]=raw
        budget(start)
    out=allowed/prototype.relative(manifest['output_relative'],single=True)
    require(out.resolve()==out and not out.exists() and not any(Path(r['requested_path']).is_relative_to(out) for r in bindings),'exclusive shadow output required')
    response,facts=evaluate_shadow(manifest,blobs);budget(start);diagnostic.stable(bindings);out.mkdir()
    published=out/'shadow-result.json';pending=out/'shadow-result.pending.json';linked=False
    try:
        output_bindings=[]
        for role,raw in dict(blobs,rederived_response=response).items():
            name=role+('.rsp' if role.endswith('response') else '.json');path=out/name
            with path.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
            row=diagnostic.identity(path);require(row['sha256']==hashlib.sha256(raw).hexdigest(),'shadow copy changed');output_bindings.append(row)
        receipt=dict(facts,status='derived-shadow-equivalence-only',manifest_sha256=manifest_sha256,review_sha256=review_sha256,
            historical_snapshot_acceptance_review_sha256=review_sha256,
            source_sha256=review['source_sha256'],kernel_sha256=PINS,input_bindings=bindings,output_bindings=output_bindings,
            input_stability_verified=True,resource_observations=budget(start,out))
        diagnostic.stable(bindings+output_bindings);source_gate()
        data=(json.dumps(receipt,sort_keys=True,indent=2)+'\n').encode()
        with pending.open('xb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
        require(file_hash(pending)==hashlib.sha256(data).hexdigest(),'pending shadow receipt changed')
        diagnostic.stable(bindings+output_bindings);budget(start,out);os.link(pending,published);linked=True
        row=diagnostic.identity(published);require(row['sha256']==hashlib.sha256(data).hexdigest(),'published shadow receipt changed')
        diagnostic.stable(bindings+output_bindings+[row]);source_gate();budget(start,out);return receipt
    except BaseException:
        if linked and published.exists() and os.path.samefile(pending,published):published.unlink()
        raise


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('manifest','review'):parser.add_argument('--'+name,type=Path,required=True);parser.add_argument('--'+name+'-sha256',required=True)
    args=parser.parse_args(argv)
    try:r=run(args.manifest,args.manifest_sha256,args.review,args.review_sha256)
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'cohort shadow rejected: '+str(error)+'\n')
    print(json.dumps({k:r[k] for k in ('status','profile','response_byte_equivalence','production_admission_approved','resource_observations')}));return 0


if __name__=='__main__':raise SystemExit(main())
