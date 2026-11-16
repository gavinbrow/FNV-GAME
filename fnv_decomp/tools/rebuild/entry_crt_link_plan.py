"""Fixed entry CRT candidate aliases and one source-owned read component plan.

Saved metadata only. No native tools, image reads, object reads or adoption.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PINS = {
    'providers': ('entry-crt-provider-evidence-v1.json', 'f18aed478641b9502a262b608421757c9c9707f9f4f730d2b152db93bc5891f1'),
    'frontier': ('entry-dependencies-next-projects-v1.json', 'eca726d106f800b023c831280c7f2ce7eb3d448a00a570f827dcd264d7dfc803'),
    'inventory': ('runtime-code-inventory-native-v1.json', '02a77cce3f43c1786cd027e72ffb17e76ffe6766c2823872254015b6e40549f6'),
    'inventory_details': ('runtime-code-inventory-native-v1.jsonl.gz', '91cdc91af6530e6e80e2104cdfeb9bd6928e17fa0f75bcf066734985248f1031'),
    'binding_details': ('runtime-bind-plan-native-v2.jsonl.gz', '4dfc437064b16c1bb933008aebf7def8d279a903eef9cca24d0fedcc12d7d826'),
    'selection': ('function-selection-v2.json', '48ae62cdc5b1754b9c4af674ef4716d53afb554882e174a93acf860eaf1c6cb1'),
    'manifest': ('objects.json', 'bc62a5fb2553431b1e0547d11f366e52efb73096ea8ceb206c556ae5740a53eb'),
    'direct': ('entry-direct-crt-identification-v1.json', '1e9b4fb0280518a61904a779aad0fa62fa2d807186782c2b286208b2bef3ae09'),
    'append': ('entry-append-crt-identification-v1.json', '2e85d99790a64a1a7d488514d47f15d1db96367e9e2f3c8c952bc9df2c0fc1b0'),
}
# Explicit finite table; a same-address different-role record is deliberately open.
CANDIDATES = (
    ('0x00ec408c', 'crt-contract', '@__security_check_cookie@4'),
    ('0x00ec43fb', 'crt-contract', '___RTDynamicCast'),
    ('0x00ec6040', 'crt-contract', '__CIsqrt'),
    ('0x00ec62c0', 'crt-contract', '__ftol2_sse'),
    ('0x00ec658f', 'crt-contract', '_atexit'),
    ('0x00ec7894', 'crt-contract', '__CxxThrowException@8'),
    ('0x00ecb3a8', 'code', '_fread'),
    ('0x00ecc071', 'code', '__wcsicmp'),
    ('0x00406d50', 'code', '_strcat_s'),
    ('0x00ec6bd2', 'code', '_strcat_s'),
    ('0x00ec43fb', 'code', None),
)
FILE_ROOTS = {'0x00d2bcd0', '0x00d2bd30', '0x00d2bd50', '0x00d2bd60', '0x00d2bda0'}
LEAF = '0x00d2bcd0'
FALSE = dict(provider_selected=False, ABI_verified=False, runtime_eligible=False,
             link_ready=False, native_preparation_performed=False, emission_performed=False)


def require(value, message):
    if not value:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def sha(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            result.update(block)
    return result.hexdigest()


def undefined(base, role):
    return '_fnv_undefined_' + digest(dict(original_base=base, role=role))


def code_name(identity):
    return '_fnv_code_' + digest(identity)


def records(path):
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        for ordinal in range(1, 1000002):
            line = stream.readline(4 * 1024 * 1024 + 1)
            if not line:
                return
            require(ordinal <= 1000000 and len(line) <= 4 * 1024 * 1024, 'stream bounds')
            yield ordinal, json.loads(line)


def private_output(path):
    private = ROOT / 'build/rebuild'
    require(private.resolve() == private, 'private output root redirects elsewhere')
    out = Path(path).resolve()
    require(out.is_relative_to(private) and out != private, 'output must stay under ignored build/rebuild')
    return out


def field_identity(row):
    relocation = row['coff_relocation']
    require(row['proof_consistency'] == 'EXACT_OWN_SOURCE_RESOLUTION'
            and row['source_resolution_basis'] == 'OWN_RECIPE_BINDING'
            and relocation['symbol_section'] == 0 and relocation['symbol_storage'] == 2
            and relocation['symbol_value'] == 0 and relocation['kind'] == 20 and relocation['addend'] == 0,
            'candidate physical field is outside fixed undefined-zero-addend REL32 scope')
    return dict(recipe_id=row['recipe_id'], caller=row['function_va'], field_offset=row['source_field_offset'],
        section=row['physical_section'], physical_offset=row['physical_offset'],
        original_field_va=row['original_field_va'], symbol_index=relocation['symbol_index'],
        source_spelling=relocation['symbol'], kind=relocation['kind'], addend=relocation['addend'],
        ordinal=row['ordinal'], binding_row_sha256=row['sha256'],
        source=row['source'],source_sha256=row['source_sha256'],object_sha256=row['object_sha256'])


def mapping(providers, frontier):
    exports = {}
    for row in providers['previous_six_member_evidence'] + providers['new_indexed_member_evidence']:
        if row['compiler_family'] != 'sp1':
            continue
        name = row['symbol']
        require(name not in exports, 'ambiguous SP1 exported provider evidence')
        exports[name] = row
    groups = {}
    for row in providers['field_sites']:
        require(row['classification'] in ('EXPLICIT_NORMAL_CRT_CONTRACT_CANDIDATE',
            'UNSELECTED_EXECUTABLE_TARGET_UNCLASSIFIED'), 'unreviewed field class')
        role = 'crt-contract' if row['classification'] == 'EXPLICIT_NORMAL_CRT_CONTRACT_CANDIDATE' else 'code'
        key = (row['derived_source_symbol_base_va'], role)
        groups.setdefault(key, []).append(row)
    for target in ('0x00ec6bd2', '0x00ec43fb'):
        key = (target, 'code')
        require(key not in groups, 'unexpected duplicate scope in provider receipt')
        groups[key] = frontier['boundaries']['generated_or_unselected_code_unknown'][target]
    result = []
    require(set(groups) == {(base,role) for base,role,_ in CANDIDATES}, 'candidate scope differs')
    for base, role, export in CANDIDATES:
        sites = sorted([field_identity(r) for r in groups[(base, role)]], key=lambda r:r['ordinal'])
        require(len({r['ordinal'] for r in sites}) == len(sites), 'duplicate candidate binding reference')
        for row in groups[(base, role)]:
            require(row['exact_original_target_va'] == base, 'candidate final/base mismatch')
        proposed = None
        if export:
            require(export in exports, 'normal export lacks observed SP1 archive evidence')
            found = exports[export]
            proposed = dict(library='libcmt.lib', compiler_family='sp1', export=export,
                archive_sha256=found['archive_sha256'], member_header_offset=found['member_header_offset'],
                member_sha256=found['member_sha256'], section=found['definition']['section'],
                value=found['definition']['value'])
        # These finite preparation subsets are intentional; other observed callers
        # never inherit approval from a candidate address/role.
        subset = [s['ordinal'] for s in sites]
        if base == '0x00406d50':
            subset = [s['ordinal'] for s in sites if s['caller'] == '0x0086a850']
        elif base == '0x00ecb3a8':
            subset = [s['ordinal'] for s in sites if s['caller'] == LEAF]
        elif base in ('0x00ec6bd2','0x00ec43fb') and role == 'code':
            subset = []
        result.append(dict(original_base=base,role=role,expected_canonical_undefined=undefined(base,role),
            status='PROVISIONAL_NORMAL_CRT_CANDIDATE' if export else 'UNRESOLVED_ROLE_CALLER_CONTRACT',
            proposed_provider=proposed,observed_field_count=len(sites),physical_sites=sites,
            initial_preparation_site_ordinals=subset,provider_alias_emitted=False,
            substitution_kind='FUNCTION_TO_FUNCTION_NORMAL_CRT' if export else None,
            state_owner_proposal='one fresh normal SP1 static CRT' if export else None,
            original_dependency_address_identity_required_for_functional_substitution=False,
            actual_caller_contract_verified=False,
            functional_compatibility_assumptions=(
                ['x86 cdecl with two borrowed 16-bit-character string pointers and int comparison result.',
                 'Case-insensitive behavior and locale come from chosen fresh normal SP1 CRT.',
                 'Main tests result equal to zero; unsigned-char source placeholder for second operand is not a typed extent proof.',
                 'Both data providers must supply readable, null-terminated 16-bit strings for the call duration.',
                 'Normal CRT invalid-parameter policy is accepted; no old locale/errno/handler state is copied.']
                if base=='0x00ecc071' else
                ['x86 cdecl three arguments: writable char buffer, total unsigned capacity, borrowed const char source.',
                 'Observed 25-byte wrapper forwards all three stack words unchanged and returns callee EAX unchanged.',
                 'Full direct delegate has normal strcat_s nonrelocation shape and all three obligations accounted.',
                 'Main supplies capacity260 and ignores int return; only its three sites are proposed initially.',
                 'Destination is terminated and source valid for call; normal invalid-parameter/errno policy is accepted.']
                if base=='0x00406d50' else []),
            original_full_relocation_identity_verified=False,**FALSE))
    return result


def source_component(assessments, fields):
    require(set(assessments) == FILE_ROOTS and set(fields) == FILE_ROOTS, 'file component coverage differs')
    leaf = assessments[LEAF]
    require(leaf['physical_identity'] == dict(recipe_id='1821-ead65709d249dd91',
        object_sha256='c768b253bc216a32ff93300d2cd488a33c6c726c7aa01d9fb0e230fa7e396e4b',symbol_index=8),
        'leaf physical owner differs')
    require(leaf['selected_native']['section'] == 3 and leaf['size'] == 39
            and leaf['original_missing_fields'] == 0 and leaf['same_parent_piece_observations'] == 0
            and {b['code'] for b in leaf['blockers']} == {'SAFESEH_REQUIRES_CLOSURE'}, 'leaf policy evidence differs')
    require(len(fields[LEAF]) == 1 and fields[LEAF][0]['coff_relocation']['symbol_index'] == 9
            and fields[LEAF][0]['coff_relocation']['symbol'] == '_fread'
            and fields[LEAF][0]['source_field_offset'] == 20
            and fields[LEAF][0]['exact_original_target_va'] == '0x00ecb3a8', 'leaf fread field differs')
    require(undefined('0x00ecb3a8','code') == leaf['obligations'][0]['canonical_name'], 'namespace contract drift')
    return dict(initial_retained_root=LEAF,canonical_code_export=code_name(leaf['physical_identity']),
        initial_cpp_consumer_method='?ReadOrMarkFailed@FUN_00d2bcd0_class@@QAEXPAXI@Z',
        receiver_contract=dict(architecture='i386',calling_convention='thiscall',stream_pointer_offset=12,
            mutable_valid_flag_offset=16,minimum_borrowed_receiver_bytes=17,
            full_original_dynamic_type_verified=False,source_declared_object_extent_not_a_runtime_allocation_proof=True),
        lifecycle_evidence=[dict(original_address=address,assessment=assessments[address],fields=fields[address])
                            for address in sorted(FILE_ROOTS)],
        initial_included_game_data=[],initial_included_game_imports=[],
        approved_object_emission=False,
        required_before_prepare=['Separate reviewed ordinary-root SafeSEH exclusion certificate for exact recipe1821 root set.',
            'Reviewed finite code-symbol bridge and role-keyed fread provider alias for exact +20 field.',
            'One normal SP1 static CRT owns FILE creation/read/seek/tell/close, descriptors, locks and errors.',
            'Bound actual normal headers, libraries, source consumer, compiler, map and archive extraction evidence.'],
        required_before_execute=['Independent preparation/map/ABI review and explicit separate execution go.',
            'Borrow a fresh FILE pointer from the chosen normal CRT, with bounded writable buffer and receiver.',
            'No old FILE/descriptor/vtable/data copying; do not dispatch through original code addresses.',
            'Data-held fread pointer signatures and complete original object lifetimes remain outside this narrow run.'],
        source_behavior_checks=['Positive read keeps flag; zero-result read clears flag.',
            'Positive short read keeps flag; leaf conflates zero-result EOF and error.',
            'Bound count within signed int range because retained source tests (int)fread_result > 0.',
            'Normal caller checks actual item count, stream position and EOF/error separately.'], **FALSE)


def run(args):
    implementation = Path(__file__).resolve()
    tool_hash = sha(implementation)
    require(tool_hash == args.implementation_sha256, 'implementation pin differs')
    base, out = Path(args.metadata_dir).resolve(), private_output(args.out)
    paths = {key:base / name for key,(name,_) in PINS.items()}
    require(out not in set(paths.values()) | {implementation} and not out.exists(), 'output collision')
    for key,path in paths.items():
        require(sha(path) == PINS[key][1], 'input pin differs: '+key)
    data = {key:json.loads(path.read_text(encoding='utf-8')) for key,path in paths.items() if not key.endswith('_details')}
    require(data['inventory']['details_sha256'] == PINS['inventory_details'][1]
        and data['providers']['inputs']['objects.json'] == PINS['manifest'][1]
        and data['append']['prior_two_target_sha256'] == PINS['direct'][1], 'metadata join differs')
    # Do not copy the private disassembly in either identification artifact.
    normal = [r for r in data['direct']['targets']['0x00ecc071']['comparisons']
              if r['compiler_family'] in ('sp1','rtm') and r['symbol'] == '__wcsicmp']
    append = data['append']['comparisons']
    require(len(normal) == len(append) == 2 and all(r['all_nonrelocation_bytes_equal'] for r in normal+append),
            'direct helper nonrelocation evidence differs')
    require(all(r['complete_original_identity_verified'] is False for r in normal+append), 'partial evidence promoted')
    units = {u['recipe_id']:u for u in data['manifest']['units']}
    selected = data['selection']['selections']
    site_rows = list(data['providers']['field_sites'])
    for target in ('0x00ec6bd2','0x00ec43fb'):
        site_rows.extend(data['frontier']['boundaries']['generated_or_unselected_code_unknown'][target])
    for row in site_rows:
        unit,choice = units[row['recipe_id']],selected[row['function_va']]
        require(choice['recipe_id']==unit['recipe_id'] and choice['symbol']==row['function_symbol']
                and choice['section']==row['physical_section']
                and choice['value']+row['source_field_offset']==row['physical_offset']
                and 0<=row['source_field_offset']<=choice['size']-4,'candidate selected source join differs')
        identities=dict(source=unit['recipe']['source'],source_sha256=unit['source_sha256'],object_sha256=unit['object_sha256'])
        require(all(k not in row or row[k]==v for k,v in identities.items()),'candidate producer identity differs')
        row.update(identities)
    aliases = mapping(data['providers'], data['frontier'])
    assessments, fields = {}, {a:[] for a in FILE_ROOTS}
    for _,row in records(paths['inventory_details']):
        if row['event'] == 'SELECTED_CODE_SERIALIZATION_ASSESSMENT' and row['original_address'] in FILE_ROOTS:
            address = row['original_address']
            require(address not in assessments, 'duplicate component assessment')
            assessments[address] = row
    for ordinal,row in records(paths['binding_details']):
        if row['function_va'] not in FILE_ROOTS:
            continue
        address = row['function_va']
        clean = {k:row.get(k) for k in ('recipe_id','recipe_index','function_va','function_symbol','source_field_offset',
            'physical_section','physical_offset','original_field_va','exact_original_target_va','derived_source_symbol_base_va',
            'classification','source_resolution_basis','proof_consistency','coff_relocation')}
        fields[address].append(dict(clean,ordinal=ordinal,sha256=digest(row)))
    for address,assessment in assessments.items():
        refs = [dict(ordinal=r['ordinal'],sha256=r['sha256']) for r in fields[address]]
        require(refs == assessment['binding_row_references'], 'component exact field join differs')
        choice = data['selection']['selections'][address]
        require(all(choice[k] == assessment['selected_native'][k] for k in ('symbol','section','size','value'))
                and choice['recipe_id'] == assessment['physical_identity']['recipe_id'], 'component selected owner differs')
    component = source_component(assessments,fields)
    for key,path in paths.items():
        require(sha(path) == PINS[key][1], 'input changed during plan: '+key)
    require(sha(implementation) == tool_hash, 'implementation changed during plan')
    result = dict(schema_version=1,kind='fnv-entry-crt-provisional-link-plan',status='candidate-only',
        inputs={k:v[1] for k,v in PINS.items()},implementation_sha256=tool_hash,
        provider_candidates=aliases,source_owned_file_component=component,
        direct_entry_candidate_evidence=dict(wide_compare=normal,append_delegate=append,
            original_dependency_targets_retained_as_unverified=True),
        summary=dict(role_keys=len(aliases),observed_field_references=sum(a['observed_field_count'] for a in aliases),
            candidate_exports=sum(a['proposed_provider'] is not None for a in aliases),
            component_selected_owners=len(assessments),component_field_occurrences=sum(map(len,fields.values()))), **FALSE)
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('x',encoding='utf-8') as stream:
        json.dump(result,stream,sort_keys=True,separators=(',',':'))
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metadata-dir',type=Path,default=ROOT/'build/rebuild')
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--implementation-sha256',required=True)
    try:
        result = run(parser.parse_args(argv))
    except (ValueError,OSError,KeyError,TypeError) as error:
        parser.exit(2,'CRT plan rejected: '+str(error)+'\n')
    print(json.dumps(result['summary'],sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
