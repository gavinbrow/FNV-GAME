"""Finite lane04 source-field and named CRT member proposals; no image reader.

Reuse lane01's existing named-member collector, never scan archives or original
code for possible providers. Names below are hypotheses, including explicitly
marked source-contract leads, and never authorize aliases or runtime adoption.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys

import crt_frontier_lane01 as shared

ROOT = Path(__file__).resolve().parents[2]
INDEX = '9db04c24f9030ba7bae153e54c01ef9475a4a1a203268bcbc3edc88136565ae9'
PACKET = '382f6153c8276f4ffec750eb6b97d0612fb285d966812a7e29f20619b52cec28'
NAMES = {
 '0x00ec782f': ('??_L@YGXPAXIHP6EX0@Z1@Z',),
 '0x00ec6130': ('_strlen',),
 '0x00ec44d0': ('_memcpy', '_memmove'),
 '0x00ec43fb': ('___RTDynamicCast',),
 '0x00ec7d40': ('_abs',),
 '0x00ec9774': ('_fprintf',),
 '0x00ec9f70': ('__CIcos',),
 '0x00ecadb8': ('_rand',),
 '0x00ec75b1': ('__isnan',),
 '0x00ec68e4': ('__stricmp',),
 '0x00eca0a0': ('__CIsin',),
 '0x00eca4a6': ('_sscanf',),
 '0x00ec7810': ('__allshl',),
 '0x00ecc6e6': ('_strtok',),
 '0x00ec658f': ('_atexit',),
 '0x00ec62c0': ('__ftol2_sse',),
 '0x00eca1d0': ('__CIacos',),
 '0x00ec6f20': ('_qsort',),
 '0x00eca7f4': ('_toupper',),
 '0x00ec7c66': ('_memcpy_s',),
 '0x00ec9130': ('_fmod',),
 '0x00ec85e3': ('__errno',),
 '0x00ec923c': ('__stat64',),
 '0x00ecada6': ('_srand',),
 '0x00ecd1c7': ('__malloc', '_malloc'),
 '0x00eca5d0': ('__CItan',),
 '0x00ecb562': ('_ftell',),
 '0x00ecc8e0': ('__except_handler4',),
 '0x00ecdacc': ('_feof',),
}
SOURCE_LEADS = {'0x00ec9774', '0x00ec7c66', '0x00ec85e3', '0x00ec923c'}

def coupling(va):
    if va in {'0x00ec9774', '0x00ecb562', '0x00ecdacc'}:
        return ['one CRT must own FILE creation, descriptor, locks, buffering, errors and close',
                'borrowed FILE pointer representation and lifetime remain unproved']
    if va in {'0x00ec68e4', '0x00eca7f4', '0x00ecc6e6', '0x00eca4a6'}:
        return ['normal fresh locale and per-thread state; old locale/tokenizer state is not reusable']
    if va in {'0x00ecadb8', '0x00ecada6', '0x00ec85e3'}:
        return ['normal CRT per-thread state ownership; retain errno/random state coupling']
    if va in {'0x00ecd1c7', '0x00ec7c66'}:
        return ['allocation/free or buffer ownership and invalid-parameter policy require whole-family review']
    if va in {'0x00ec782f', '0x00ec43fb', '0x00ecc8e0', '0x00ec62c0', '0x00ec7810'}:
        return ['compiler helper machine ABI is not established by a C++ recovered prototype',
                'EH/RTTI/frame or register contracts remain open where applicable']
    if va.startswith('0x00fd') or va.startswith('0x00fc'):
        return ['source static-destructor callback identity/lifetime and registration ownership unresolved']
    return ['call ABI, input ranges, outputs and source data lifetime remain unapproved']

def target_record(target, records, source_identity):
    va = target['original_target']; uses = target['field_uses']
    names = NAMES.get(va, ())
    return dict(original_target=va, field_count=len(uses), field_proofs=uses,
        physical_aliases=sorted({u['coff_relocation']['symbol'] for u in uses}),
        source_inputs=[dict(path=p, sha256=source_identity[p]) for p in
                       sorted({u['source_path'] for u in uses})],
        hypotheses=list(names), hypothesis_basis='finite source contract lead' if va in SOURCE_LEADS
                    else 'physical alias spelling' if names else 'no specific named CRT evidence',
        members={k:v for k,v in records.items() if k.split(':',1)[1] in names},
        actual_V4_unresolved_groups=target['actual_V4_unresolved_groups'],
        state_and_ABI_obligations=coupling(va),
        provider_selected=False, original_identity_proven=False, ABI_approved=False)

def run():
    packet_path=ROOT/'build/rebuild/application-frontier-dispatch-v1/crt-frontier-lane-04.json'
    index_path=packet_path.with_name('index.json')
    doctor_path=ROOT/'build/rebuild/doctor-all.json'
    pinned={packet_path:PACKET,index_path:INDEX,doctor_path:shared.DOCTOR}
    implementation={p:shared.sha(ROOT/p) for p in (
        'tools/rebuild/crt_frontier_lane04.py','tools/rebuild/crt_frontier_lane01.py',
        'tools/rebuild/crt_provider.py','tools/compare.py','tools/rebuild/toolchain.py')}
    for p,h in pinned.items(): shared.check(shared.sha(p)==h,'input identity differs')
    packet=json.loads(packet_path.read_text()); doctor=json.loads(doctor_path.read_text())
    shared.check(packet['lane']==4 and packet['target_count']==48 and packet['field_use_count']==657,
                 'lane scope differs')
    source_identity={}
    for target in packet['targets']:
        for use in target['field_uses']:
            p=use['source_path']; h=use['source_sha256']
            shared.check(p not in source_identity or source_identity[p]==h,'conflicting source identity')
            source_identity[p]=h
    for p,h in source_identity.items():
        shared.check(shared.sha(ROOT/p)==h,'source identity differs: '+p)
    records={}
    for compiler,h in shared.LIBS.items():
        lib=Path(doctor['toolchains'][compiler]['root'])/'VC/lib/libcmt.lib'
        shared.check(shared.sha(lib)==h,'library identity differs')
        pinned[lib]=h
        for name in sorted({n for names in NAMES.values() for n in names}):
            try: records[compiler+':'+name]=shared.metadata(lib,name)
            except ValueError as e: records[compiler+':'+name]=dict(export=name,unavailable=str(e))
    targets=[target_record(t,records,source_identity) for t in packet['targets']]
    for p,h in pinned.items(): shared.check(shared.sha(p)==h,'input changed')
    for p,h in source_identity.items(): shared.check(shared.sha(ROOT/p)==h,'source changed')
    for p,h in implementation.items(): shared.check(shared.sha(ROOT/p)==h,'implementation changed')
    report=dict(schema_version=1,kind='crt-frontier-lane04-named-member-proposals',
        packet_sha256=PACKET,index_sha256=INDEX,doctor_sha256=shared.DOCTOR,
        library_sha256=shared.LIBS,implementation=implementation,
        targets=targets,target_count=len(targets),field_count=sum(t['field_count'] for t in targets),
        source_count=len(source_identity),original_image_read=False,native_process_invoked=False,
        runtime_eligible=False,provider_selected=False,ABI_approved=False)
    out=ROOT/'build/rebuild/crt-frontier-lane04-metadata-v1.json'
    with out.open('x',encoding='utf-8') as f: json.dump(report,f,indent=2); f.write('\n')
    print(json.dumps(dict(output=str(out),sha256=shared.sha(out),targets=len(targets),
                         fields=report['field_count'],source_count=len(source_identity))))

if __name__=='__main__': run()
