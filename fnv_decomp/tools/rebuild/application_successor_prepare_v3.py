"""Hard-disabled, prepare-only V11 role-to-consumer adapter.

This source defines a proposed role schema, not an approved actual handoff.
No native tools, original reads, publication, or link authorization occur.
An independently reviewed fixed wrapper must authenticate this source and its
entire import closure, exact input/peer pins, lease and phase/journal lifecycle.
Actual emitted members and independently accepted peer schemas are not yet fixed.
"""
import hashlib
import importlib
import json
import re
import sys
from pathlib import Path

# Deliberately unset until actual accepted output and independent review.
SOURCE_GRAPH = None
ROLE_PINS = None
PEER_SCHEMAS = None

CORE_ROLES = frozenset({'baseline_report','baseline_observation','baseline_fields','baseline_response',
    'archive','semantic','factory','iat','crt','response','iat_peer','crt_peer',
    'factory_peer','handoff_peer','native_peer'})
REQUIRED_SOURCES = frozenset({'application_successor_compose_v12','application_actual_cohort_assembly_v10',
    'application_actual_cohort_semantic_v13','application_actual_factory_join_v2',
    'application_actual_archive_bind_v1','application_response_successor_v2',
    'post_v14_iat_crt_census_v5','application_link_diagnostic','exact_binding_stability',
    'application_import34_diagnostic','import_kernel32_fifteen','iat_code21_annotations',
    'normal_import_archive_bytes_v1'})
ROOT = Path(__file__).resolve().parents[2]


def require(ok, message):
    if not ok: raise ValueError(message)


def sha(data): return hashlib.sha256(data).hexdigest()


def digest_string(x): return type(x) is str and re.fullmatch('[0-9a-f]{64}',x) is not None


def parse(data):
    def pairs(items):
        result={}
        for k,v in items:
            require(k not in result,'duplicate JSON key');result[k]=v
        return result
    require(type(data) is bytes and len(data)<=128*1024*1024,'bounded JSON bytes required')
    return json.loads(data,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('nonfinite')))


def check_graph(actual):
    """The complete graph must equal a separately frozen exact pin map."""
    require(type(SOURCE_GRAPH) is dict and SOURCE_GRAPH and type(actual) is dict and
            actual==SOURCE_GRAPH and REQUIRED_SOURCES.issubset(actual), 'closed reviewed source graph required')
    for name,pin in actual.items():
        require(type(name) is str and re.fullmatch('[A-Za-z_][A-Za-z_0-9]*',name) and
                type(pin) is dict and set(pin)=={'path','sha256'} and
                type(pin['path']) is str and pin['path'].startswith('tools/') and digest_string(pin['sha256']),
                'invalid source graph pin')


def _fixed_module(name):
    """Only the already installed authenticated snapshot finder may load code."""
    require(type(SOURCE_GRAPH) is dict and name in SOURCE_GRAPH and sys.meta_path,
            'fixed module graph required')
    finder=sys.meta_path[0]
    require(getattr(finder,'snapshots',{}).get(name) is not None and
            sha(finder.snapshots[name])==SOURCE_GRAPH[name]['sha256'], 'snapshot module pin differs')
    module=importlib.import_module(name)
    require(getattr(module,'__loader__',None) is finder and sys.meta_path[0] is finder,
            'unreviewed or preloaded module')
    return module


def _fixed_replay(data, kernel_role, libraries, resources, identities):
    """Build V14's replay using bound data and fixed authenticated modules."""
    keys={'native','request','request_sha256','originals','expected_sources','catalog','prior_iat'}
    require(type(data) is dict and set(data)==keys and kernel_role in libraries.values(), 'replay data schema')
    old=_fixed_module('application_import34_diagnostic')
    producer=_fixed_module('import_kernel32_fifteen')
    annotations=_fixed_module('iat_code21_annotations')
    diagnostic=_fixed_module('application_link_diagnostic')
    parser=_fixed_module('normal_import_archive_bytes_v1')
    parsed=parser.parse_archive(resources[kernel_role])
    require(parsed['archive_sha256']==ROLE_PINS[kernel_role]['sha256'], 'kernel archive parse identity differs')
    library_rows={name:diagnostic.partial.native_archive(resources[role]) for name,role in libraries.items()}
    refs={name:{'sha256':ROLE_PINS[role]['sha256'],'bytes':len(resources[role])} for name,role in libraries.items()}
    return dict(data,old=old,producer=producer,annotations=annotations,parsed=parsed,
                libraries=library_rows,library_refs=refs)


def _arguments(resources, identities):
    """Mechanical proposed mapping, not an acceptance or peer-review check."""
    require(type(ROLE_PINS) is dict and ROLE_PINS and type(resources) is dict and type(identities) is dict,
            'reviewed exact roles required')
    roles=set(ROLE_PINS);members={r[7:]:r for r in roles if r.startswith('member:')}
    libraries={r[12:]:r for r in roles if r.startswith('iat_library:')}
    require(CORE_ROLES.issubset(roles) and roles==CORE_ROLES | set(members.values()) | set(libraries.values()) and members and len(libraries)==4 and
            all(n and '/' not in n and '\\' not in n for n in libraries) and
            len(members)+len(libraries)==len(roles-CORE_ROLES) and all(n and '/' not in n and '\\' not in n for n in members),
            'closed role set including emitted members required')
    require(set(resources)==roles==set(identities),'complete role inputs required')
    paths=set()
    for role in roles:
        pin=ROLE_PINS[role];ident=identities[role];data=resources[role]
        require(type(pin) is dict and set(pin)=={'path','sha256'} and type(pin['path']) is str and pin['path'] and
                not Path(pin['path']).is_absolute() and '..' not in Path(pin['path']).parts and
                pin['path'] not in paths and digest_string(pin['sha256']) and type(data) is bytes and
                sha(data)==pin['sha256'] and type(ident) is dict and
                set(ident)=={'requested_path','path','sha256','size','device','inode'} and
                ident['sha256']==pin['sha256'] and
                type(ident['size']) is int and ident['size']==len(data) and
                all(type(ident[k]) is int and ident[k]>=0 for k in ('device','inode')),'role physical identity differs')
        requested=(ROOT/pin['path']).absolute();resolved=requested.resolve(strict=True)
        require(resolved.is_relative_to(ROOT.resolve()) and ident['requested_path']==str(requested) and
                ident['path']==str(resolved), 'role path escaped or physical path differs')
        paths.add(pin['path'])
    semantic=parse(resources['semantic']);factory=parse(resources['factory']);iat=parse(resources['iat'])
    crt=parse(resources['crt']);response=parse(resources['response'])
    require(type(semantic) is dict and set(semantic)=={'wrappers','members','handoff','member_count','field_count',
            'namespace_by_member','expected_providers','expected_fields','component','selected_providers'},'semantic schema')
    require(type(factory) is dict and set(factory)=={'selections','outcomes','emitted'},'factory schema')
    require(type(iat) is dict and set(iat)=={'full_proofs','replay','kernel_role'} and
            type(crt) is dict and set(crt)=={'bindings','source_evidence','prior_crt'} and
            type(response) is dict and set(response)=={'old_out','new_out','inherited_aliases','fresh_uuid_identity','qualified_uuid'},
            'census or response schema')
    require(type(semantic['members']) is list and
            {m.get('name') for m in semantic['members'] if type(m) is dict}==set(members) and
            len(semantic['members'])==len(members),'exact member roles differ')
    member_bytes={name:resources[role] for name,role in members.items()}
    sem=dict(semantic,member_bytes=member_bytes)
    fac=dict(factory,members=sem['members'],wrappers=sem['wrappers'],member_bytes=member_bytes)
    replay=_fixed_replay(iat['replay'],iat['kernel_role'],libraries,resources,identities)
    iat=dict(full_proofs=iat['full_proofs'],replay=replay,peer_bytes=resources['iat_peer'],
             peer_sha256=ROLE_PINS['iat_peer']['sha256'])
    crt=dict(crt,peer_bytes=resources['crt_peer'],peer_sha256=ROLE_PINS['crt_peer']['sha256'])
    response=dict(response,new_archive=identities['archive']['path'])
    return dict(baseline_bytes={'report':resources['baseline_report'],'observation':resources['baseline_observation'],
             'fields':resources['baseline_fields']},semantic_inputs=sem,iat_inputs=iat,crt_inputs=crt,
             response_bytes=resources['baseline_response'],response_inputs=response,
             archive_bytes=resources['archive'],archive_sha256=ROLE_PINS['archive']['sha256'],
             archive_identity=identities['archive'],factory_inputs=fac,
             qualified_selected_providers=sem['selected_providers'])


def _phase_role_binding(operation, identities):
    """The exact ordered phase ledger must contain every role and nothing else."""
    require(type(operation) is dict and type(operation.get('input_bindings')) is list and
            type(operation.get('phases')) is list and type(ROLE_PINS) is dict and
            list(identities)==list(ROLE_PINS) and operation['input_bindings']==list(identities.values()) and
            sum(type(p) is dict and p.get('name')=='compose-v12' for p in operation['phases'])==1,
            'complete ordered role ledger differs')
    return identities['archive']


def _compose_v12_untrusted_fixture(resources, identities):
    """Pure consumer wiring only; this function does not authenticate inputs.

    Fixed name and kwargs, no delegate injection. Never an operational entry;
    only a future reviewed authenticated session may call the real composer.
    """
    args=_arguments(resources,identities)
    return importlib.import_module('application_successor_compose_v12').compose(**args)


def _prepare_inside_authenticated_session(resources,identities,graph,operation):
    """Unavailable until peer schemas are implemented and independently frozen."""
    check_graph(graph)
    args=_arguments(resources,identities)
    require(_phase_role_binding(operation,identities)==args['archive_identity'], 'archive phase differs')
    require(PEER_SCHEMAS is not None,'independent producer/peer consumers are not fixed')
    # Deliberately unconditional: non-None/caller booleans do not grant approval.
    raise RuntimeError('independent peer validation and fixed operation wiring not implemented')


def run():
    raise RuntimeError('prepare-only entry disabled until independently reviewed fixed artifacts and launcher exist')


if __name__=='__main__':run()
