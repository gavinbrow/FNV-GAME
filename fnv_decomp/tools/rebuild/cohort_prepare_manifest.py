"""Off-side authored-cohort response prototype; never production admission.

One fixed CLI and typed manifest exercise frozen response-edit kernels. Full
cohort proof, namespace, MATCH and native admission remain outside this seam.
No compiler, linker, game process, module name or command comes from metadata.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
KERNEL_PINS = {
    'tools/rebuild/application_wave8_diagnostic.py': '5643730f3031086829286d14c102e7a374da10f16cec187532a6ab89c3e09669',
    'tools/rebuild/application_wave9_diagnostic.py': 'd54916fcb1880eea03217cf5067684cd9ddc02af18bfaab6fc5b63a3b0e65cc7',
    'tools/rebuild/application_link_diagnostic.py': '74cca67c3ec414931f4bfb26403338734f87da5eb28952e2327d008cbb79b379',
}
PROFILES = {'frozen-wave8-response-v1', 'frozen-wave9-response-v1'}
MANIFEST_KEYS = {'schema_version', 'kind', 'phase', 'scope', 'validator_id', 'entrypoint_sha256',
    'kernel_sha256', 'baseline_output_relative', 'output_relative', 'inputs',
    'baseline_roles', 'addition_roles', 'replacements', 'aliases', 'expected_response_sha256'}
IDENTITY_KEYS = {'requested_path', 'path', 'sha256', 'size', 'device', 'inode'}
ALIAS_KEYS = {'prior_IAT', 'prior_CRT', 'allowed_IAT', 'new_IAT', 'new_CRT'}
OPTIONS = {'/NOLOGO', '/MACHINE:X86', '/SUBSYSTEM:WINDOWS', '/INCREMENTAL:NO', '/VERBOSE:LIB', '/DEBUG'}


def require(condition, message):
    if not condition: raise ValueError(message)


def file_hash(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for part in iter(lambda:stream.read(1024*1024),b''):digest.update(part)
    return digest.hexdigest()


def strict_json(text):
    def unique(pairs):
        result={}
        for key,value in pairs:
            require(key not in result, 'duplicate JSON member')
            result[key]=value
        return result
    return json.loads(text,object_pairs_hook=unique)


def sha(value):
    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value), 'exact lowercase byte SHA-256 required')
    return value


def role(value):
    require(isinstance(value, str) and re.fullmatch('[a-z][a-z0-9_]{0,47}', value), 'closed data-role spelling required')
    return value


def relative(value, *, single=False):
    require(isinstance(value, str) and value and len(value) <= 240 and '\\' not in value
            and not value.startswith('/') and ':' not in value, 'relative manifest path required')
    parts=value.split('/')
    require(all(re.fullmatch('[A-Za-z0-9_.-]+', p) and p not in ('.', '..') for p in parts)
            and (not single or len(parts)==1), 'bounded relative manifest path required')
    return Path(*parts)


def kernels():
    for path, expected in KERNEL_PINS.items(): require(file_hash(ROOT/path)==expected, 'frozen response kernel changed')
    modules = {name: importlib.import_module(name) for name in
               ('application_wave8_diagnostic', 'application_wave9_diagnostic', 'application_link_diagnostic')}
    require(all(Path(m.__file__).resolve()==ROOT/'tools/rebuild'/(name+'.py') for name,m in modules.items()),
            'unexpected frozen kernel module')
    return modules


def validate_manifest(manifest):
    require(type(manifest) is dict and set(manifest)==MANIFEST_KEYS, 'exact prototype manifest schema required')
    require(type(manifest['schema_version']) is int and manifest['schema_version']==1
            and manifest['kind']=='authored-cohort-response-prototype-v1'
            and manifest['phase']=='prepare-only' and manifest['scope']=='authored-synthetic-only',
            'prototype is prepare-only and has no production admission')
    require(type(manifest['validator_id']) is str and manifest['validator_id'] in PROFILES and manifest['kernel_sha256']==KERNEL_PINS,
            'closed frozen response profile required')
    require(sha(manifest['entrypoint_sha256'])==file_hash(__file__), 'exact entrypoint bytes required')
    require(relative(manifest['baseline_output_relative'], single=True)!=relative(manifest['output_relative'], single=True),
            'fresh output distinct from inherited output required')
    inputs=manifest['inputs']; require(type(inputs) is dict and 1 <= len(inputs) <= 512, 'bounded exact input roles required')
    for name, entry in inputs.items():
        role(name);require(type(entry) is dict and set(entry)=={'relative_path','identity'}, 'exact role binding schema required')
        relative(entry['relative_path']); identity=entry['identity']
        require(type(identity) is dict and set(identity)==IDENTITY_KEYS, 'complete physical identity required')
        require(all(isinstance(identity[k], str) and identity[k] for k in ('requested_path','path')), 'both physical path spellings required')
        sha(identity['sha256'])
        require(all(type(identity[k]) is int and identity[k]>=0 for k in ('size','device','inode'))
                and identity['size'] <= 16*1024**2, 'bounded exact file metadata required')
    require('baseline_response' in inputs, 'baseline response role required')
    for key in ('baseline_roles','addition_roles'):
        value=manifest[key];require(type(value) is list and len(value)==len(set(value)) and all(role(v) in inputs for v in value), 'unique known role list required')
    replacements=manifest['replacements'];require(type(replacements) is list and len(replacements)<=2, 'bounded replacement list required')
    for entry in replacements:
        require(type(entry) is dict and set(entry)=={'from_role','to_role'}
                and role(entry['from_role']) in manifest['baseline_roles'] and role(entry['to_role']) in inputs,
                'exact selected-role replacement required')
    targets=[entry['to_role'] for entry in replacements]
    used=['baseline_response']+manifest['baseline_roles']+manifest['addition_roles']+targets
    require(len(used)==len(set(used)) and set(used)==set(inputs), 'all input roles consumed exactly once')
    aliases=manifest['aliases'];require(type(aliases) is dict and set(aliases)==ALIAS_KEYS, 'exact alias fact schema required')
    for value in aliases.values():
        require(type(value) is list and len(value)<=64 and len(value)==len(set(value))
                and all(isinstance(s,str) and s.startswith('/ALTERNATENAME:') and s.count('=')==1 and len(s)<=1024 for s in value),
                'bounded unique literal alias tokens required')
    if manifest['validator_id']=='frozen-wave8-response-v1':
        require(not replacements and len(manifest['addition_roles'])==2 and aliases['allowed_IAT']==aliases['prior_IAT'], 'exact frozen V8 response profile required')
    else:
        require(len(replacements)==2 and len(manifest['addition_roles'])==1, 'exact frozen V9 response profile required')
    sha(manifest['expected_response_sha256'])


def prepare(manifest_path, expected_manifest_sha256):
    """Run only against an authored fixture package, writing unqualified output."""
    manifest_path=Path(manifest_path).resolve(strict=True); sha(expected_manifest_sha256)
    require(manifest_path.is_file() and manifest_path.stat().st_size<=1024**2,
            'exact bounded manifest file required')
    manifest_bytes=manifest_path.read_bytes()
    require(len(manifest_bytes)<=1024**2 and hashlib.sha256(manifest_bytes).hexdigest()==expected_manifest_sha256,
            'exact loaded manifest bytes required')
    manifest=strict_json(manifest_bytes.decode('utf-8'));validate_manifest(manifest)
    mods=kernels(); diagnostic=mods['application_link_diagnostic']; root=manifest_path.parent
    manifest_identity=diagnostic.identity(manifest_path)
    require(manifest_identity['sha256']==expected_manifest_sha256, 'manifest changed after loading')
    bindings=[manifest_identity]; paths={}
    for name, entry in manifest['inputs'].items():
        path=(root/relative(entry['relative_path'])).absolute();resolved=path.resolve(strict=True)
        require(resolved.is_relative_to(root) and path.is_file(), 'input escapes authored fixture package')
        observed=diagnostic.identity(path)
        require(observed==entry['identity'], 'requested/resolved/content/physical identity differs: '+name)
        bindings.append(observed); paths[name]=path
    output=(root/relative(manifest['output_relative'],single=True)).absolute()
    require(output.resolve()==output and not output.exists()
            and not any(p.is_relative_to(output) for p in paths.values()), 'new exclusive fixture output required')
    old_output=root/relative(manifest['baseline_output_relative'],single=True)
    baseline_bytes=paths['baseline_response'].read_bytes()
    require(hashlib.sha256(baseline_bytes).hexdigest()==manifest['inputs']['baseline_response']['identity']['sha256'],
            'loaded baseline bytes differ')
    baseline=baseline_bytes.decode('utf-8');lines=baseline.splitlines()
    require(all(len(line)>2 and line.startswith('"') and line.endswith('"') for line in lines), 'quoted baseline response required')
    tokens=[line[1:-1] for line in lines]
    selected={str(paths[name]) for name in manifest['baseline_roles']}
    require(len(selected)==len(manifest['baseline_roles']) and all(tokens.count(path)==1 for path in selected),
            'each exact selected baseline input token must occur once')
    aliases=manifest['aliases'];allowed=OPTIONS|selected|set(aliases['prior_IAT'])|set(aliases['prior_CRT'])|{
        '/OUT:'+str(old_output/'diagnostic.exe'), '/MAP:'+str(old_output/'diagnostic.map')}
    require(all(token in allowed for token in tokens), 'unknown baseline token outside fixed prototype profile')
    additions=[str(paths[name]) for name in manifest['addition_roles']]
    if manifest['validator_id']=='frozen-wave8-response-v1':
        result=mods['application_wave8_diagnostic'].response_tokens(baseline,old_output,output,additions,
            aliases['prior_IAT'],aliases['prior_CRT'],aliases['new_IAT'],aliases['new_CRT'])
    else:
        replacements=[(str(paths[r['from_role']]),str(paths[r['to_role']])) for r in manifest['replacements']]
        result=mods['application_wave9_diagnostic'].response_tokens(baseline,old_output,output,replacements,additions[0],
            aliases['prior_IAT'],aliases['prior_CRT'],aliases['allowed_IAT'],aliases['new_IAT'],aliases['new_CRT'])
    # Match the frozen preparers' TextIO newline conversion byte-for-byte.
    response=diagnostic.response_text(result).replace('\n',os.linesep).encode('utf-8')
    require(hashlib.sha256(response).hexdigest()==manifest['expected_response_sha256'], 'expected authored response bytes differ')
    diagnostic.stable(bindings);kernels();require(file_hash(__file__)==manifest['entrypoint_sha256'], 'entrypoint drift')
    output.mkdir()
    report_path=output/'synthetic-preparation.json'; pending=output/'synthetic-preparation.pending.json'; linked=False
    try:
        response_path=output/'prepared-response.rsp'
        with response_path.open('xb') as stream:stream.write(response);stream.flush();os.fsync(stream.fileno())
        response_binding=diagnostic.identity(response_path)
        require(response_binding['sha256']==manifest['expected_response_sha256'] and response_binding['size']==len(response),
                'written response bytes differ')
        protected=bindings+[response_binding]
        receipt=dict(schema_version=1,kind='authored-cohort-response-prototype-result-v1',
            status='synthetic-response-prepared-unqualified',phase='prepare-only',validator_id=manifest['validator_id'],
            manifest_sha256=expected_manifest_sha256,response_sha256=hashlib.sha256(response).hexdigest(),
            entrypoint_sha256=manifest['entrypoint_sha256'],kernel_sha256=KERNEL_PINS,input_bindings=bindings,
            response_byte_encoding='utf8+native-newline',response_binding=response_binding,
            full_proof_admission_verified=False,production_ready=False,namespace_adopted=False,
            fresh_MATCH_performed=False,native_conformance_performed=False,native_LINK_permitted=False,
            native_operations_performed=False,game_execution_performed=False,provider_selected=False,runtime_eligible=False)
        diagnostic.stable(protected);kernels();require(file_hash(__file__)==manifest['entrypoint_sha256'], 'entrypoint drift')
        report_bytes=(json.dumps(receipt,sort_keys=True,indent=2)+'\n').encode('utf-8')
        with pending.open('xb') as stream:stream.write(report_bytes);stream.flush();os.fsync(stream.fileno())
        require(file_hash(pending)==hashlib.sha256(report_bytes).hexdigest(), 'written prototype report differs')
        diagnostic.stable(protected);kernels()
        os.link(pending,report_path);linked=True
        report_binding=diagnostic.identity(report_path)
        require(report_binding['sha256']==hashlib.sha256(report_bytes).hexdigest(), 'published prototype report differs')
        diagnostic.stable(protected+[report_binding]);kernels();require(file_hash(__file__)==manifest['entrypoint_sha256'], 'entrypoint drift')
        return receipt
    except BaseException:
        # Never leave an apparent completed prototype report after failed gates.
        if linked and report_path.exists() and os.path.samefile(report_path,pending):report_path.unlink()
        raise


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--manifest-sha256',required=True)
    args=parser.parse_args(argv)
    try: result=prepare(args.manifest,args.manifest_sha256)
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'cohort prototype rejected: '+str(error)+'\n')
    print(json.dumps({k:result[k] for k in ('status','validator_id','manifest_sha256','response_sha256','entrypoint_sha256','production_ready')}));return 0


if __name__=='__main__':raise SystemExit(main())
