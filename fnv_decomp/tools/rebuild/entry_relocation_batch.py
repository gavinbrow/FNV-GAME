"""Fixed nineteen-field/six-TU private source overlays; never link or execute."""
from __future__ import annotations
import argparse
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import runtime_source_overlay as frozen
import entry_relocation_repair as first
import runtime_bind_plan as binding
from coff_inventory import Coff, peak_memory_bytes
from data_plan import Pe, file_hash
from import_plan import ImagePe, image_ok, parse_imports, require
from relocation_audit import Intervals, relocation_record
from compare import Coff as CompareCoff, compare as plain_compare
import toolchain

POLICY = ROOT/'runtime/source-overlays/entry-nineteen-existing-identities.json'
POLICY_SHA = '0144fbdf83e055d2910989b9a06588334a0d6101c8f8bd9e98af77256e453029'
PROPOSAL = ROOT/'runtime/source-overlays/entry-next-existing-identities.proposal.json'
TOOLS = frozen.TOOLS + ['tools/rebuild/entry_relocation_repair.py', 'tools/rebuild/entry_relocation_batch.py',
    'tools/rebuild/runtime_bind_plan.py', 'tools/rebuild/relocation_audit.py']


def sha(raw): return hashlib.sha256(raw).hexdigest()


def policy():
    raw = POLICY.read_bytes()
    require(sha(raw) == POLICY_SHA, 'fixed nineteen-field policy changed')
    return json.loads(raw)


def transform(raw, unit):
    require(unit in policy()['units'], 'unauthorized unit/transformation')
    require(sha(raw) == unit['source_sha256'], 'stale original source')
    edits = sorted(unit['edits'], key=lambda e:e['byte_offset'])
    end = 0
    for edit in edits:
        start = edit['byte_offset']; old = edit['old'].encode()
        require(start >= end and raw[start:start+len(old)] == old, 'overlapping/stale guarded source span')
        require(edit['new'].count('\n') == edit['old'].count('\n') and
                edit['new'].count('\r\n') == edit['old'].count('\r\n'), 'edit line context changed')
        end = start+len(old)
    result = raw
    for edit in reversed(edits):
        start = edit['byte_offset']; old = edit['old'].encode()
        result = result[:start]+edit['new'].encode()+result[start+len(old):]
    require(result.count(b'\n') == raw.count(b'\n') and result.count(b'\r\n') == raw.count(b'\r\n'), 'source line context changed')
    require(not re.search(rb'\b(__FILE__|__DATE__|__TIME__|__COUNTER__|__TIMESTAMP__)\b', raw), 'source path/time macro unsupported')
    return result


def snapshot(coff, name, size):
    found = [s for s in coff.symbols.values() if s['name'] == name and s['section'] > 0]
    require(len(found) == 1, 'selected native function ambiguous')
    symbol = found[0]; section = coff.sections[symbol['section']]
    require(section['flags'] & 0x20000020 and 0 <= symbol['value'] <= section['size']-size, 'selected native span invalid')
    raw = binding.section_payload(coff, symbol['section'])[symbol['value']:symbol['value']+size]
    fields = []
    for reloc in section['relocs']:
        record = relocation_record(coff, section, reloc)
        if record['offset'] < symbol['value']+size and record['offset']+max(1,record['width']) > symbol['value']:
            require(record['width'] == 4 and symbol['value'] <= record['offset'] <= symbol['value']+size-4, 'selected unsupported/straddling reference')
            target = coff.symbols[record['symbol_index']]
            semantic = dict(offset=record['offset']-symbol['value'], kind=record['kind'], addend=record['addend'],
                target={k:target[k] for k in ('name','section','value','storage','type','aux_count')})
            fields.append(dict(semantic=semantic, physical=record, target_symbol_index=target['index'], target_record=target))
    return raw, fields, dict(symbol_index=symbol['index'], section=symbol['section'], value=symbol['value'], size=size,
        section_flags=section['flags'], comdat=section['comdat'], selection=section['selection'], association=section['association'])


def verify_owner(before, after, owner, recipe):
    selected = owner['original_selected_owner']; name = selected['symbol']; size = selected['size']
    old, oldrefs, oldnative = snapshot(before, name, size)
    new, newrefs, newnative = snapshot(after, name, size)
    require(oldnative['section'] == selected['section'] and oldnative['value'] == selected['value'], 'original selected native identity changed')
    require({k:v for k,v in oldnative.items() if k not in ('symbol_index','section')} ==
            {k:v for k,v in newnative.items() if k not in ('symbol_index','section')}, 'selected span/COMDAT metadata changed')
    oldsem = [r['semantic'] for r in oldrefs]; remaining = list(newrefs); mask = set(); migrations = []
    for field in owner['fields']:
        off = field['function_offset']; name = field['proposed_target_symbol']
        require(struct.unpack_from('<I', old, off)[0] == int(field['target_va'],16), 'original operand differs')
        require(not any(r['offset'] < off+4 and r['offset']+4 > off for r in oldsem), 'original proposed field not missing')
        hits = [r for r in remaining if r['semantic']['offset'] == off]
        require(len(hits) == 1, 'new field missing or duplicated')
        hit = hits[0]; semantic = hit['semantic']; target = semantic['target']
        require(semantic['kind'] == 6 and semantic['addend'] == 0 and target['name'] == name and
                target['storage'] == 2 and target['aux_count'] == 0, 'new target not exact zero-addend EXTERNAL DIR32')
        named = [s for s in after.symbols.values() if s['name'] == name]
        require(len(named) == 1, 'new target symbol duplicated')
        if field['target_identity_basis'] == 'EXACT_OWN_RECIPE_DATA_SYMBOL':
            require(target['section'] == target['value'] == target['type'] == 0 and recipe['symbols'][name] == field['target_va'], 'data carrier definition/type/binding changed')
        else:
            expected = field['target_function']
            require(expected in recipe['functions'] and target['section'] > 0 and target['type'] == 32, 'code identity/type/binding changed')
            target_symbol = named[0]
            _, _, target_native = snapshot(after, expected['symbol'], expected['size'])
            _, _, original_target_native = snapshot(before, expected['symbol'], expected['size'])
            require(target_native['symbol_index'] == target_symbol['index'] and target_native['section'] == target['section'] and target_native['value'] == target['value'], 'code target not exact defined entry')
            require({k:v for k,v in target_native.items() if k != 'symbol_index'} ==
                    {k:v for k,v in original_target_native.items() if k != 'symbol_index'}, 'code target native section/span identity changed')
        remaining.remove(hit); mask.update(range(off,off+4))
        migrations.append(dict(original_field=field['entry_binding_reference'], original_target=field['target_va'],
            new_physical=hit, source_field_offset=off, original_status='MISSING_COFF_RELOCATION', overlay_status='EXACT_DIR32'))
    require([r['semantic'] for r in remaining] == oldsem, 'other selected relocations changed')
    require(all(a == b for i,(a,b) in enumerate(zip(old,new)) if i not in mask), 'selected non-field bytes changed')
    return dict(function_va=owner['function_va'], original_native=oldnative, overlay_native=newnative,
        migrations=migrations, non_field_bytes_equal=True, other_relocations_equal=True)


def complete_matches(rows, recipe, owners):
    require(first.row_identities(rows) == first.row_identities(recipe['functions']) and bool(rows), 'complete recipe comparison rows differ')
    require(all(r['verdict'] == 'match' for r in rows), 'plain original comparison failed')
    for owner in owners:
        s = owner['original_selected_owner']
        hits = [r for r in rows if r['symbol'] == s['symbol']]
        require(len(hits) == 1 and hits[0]['size'] == hits[0]['compiled_extent'] == s['size'], 'selected compiled extent differs')


def fresh_functions(coff, recipe):
    rows = []
    for spec in recipe['functions']:
        _, _, native = snapshot(coff, spec['symbol'], spec['size'])
        rows.append(dict(spec, section=native['section'], value=native['value'], verdict='match'))
    return rows


def inventory(coff):
    # Object hash binds every auxiliary record, including opaque ones. Parsed
    # metadata is evidence, not replacement source or an adopted runtime input.
    _,_,_,symptr,_,_,_ = coff.unpack('<HHIIIHH',0)
    symbols = []
    for symbol in coff.symbols.values():
        n = symbol['aux_count']; entry = dict(symbol)
        entry['auxiliary_record_sha256'] = sha(coff.take(symptr+(symbol['index']+1)*18,n*18)) if n else None
        symbols.append(entry)
    return dict(sections=list(coff.sections.values()), symbols=symbols, directives=coff.directives)


def source_bound_rows(coff, unit, pe, highlows, selection):
    functions = fresh_functions(coff, unit['recipe'])
    entries = {int(a,16):s for a,s in selection['selections'].items()}
    code = Intervals([(a,a+s['size'],dict(address=binding.va(a),**s)) for a,s in entries.items()])
    iat = {int(i['original_IAT_va'],16):i for i in parse_imports(pe)}
    counts = Counter()
    rows = list(binding.scan_unit(coff,unit,functions,functions,pe,highlows,code,entries,iat,counts))
    return rows, dict(counts), functions


def migrations_match(oldrows, newrows, spec):
    key = lambda r:(r['function_va'],r['source_field_offset'])
    event = 'MISSING_ORIGINAL_HIGHLOW_SOURCE_MIGRATION_BLOCKER'
    old = {key(r) for r in oldrows if r['event'] == event}
    new = {key(r) for r in newrows if r['event'] == event}
    wanted = {(o['function_va'],f['function_offset']) for o in spec['owners'] for f in o['fields']}
    require(wanted <= old and new == old-wanted, 'complete unit missing-field migration differs')
    for owner in spec['owners']:
        for field in owner['fields']:
            hits = [r for r in newrows if key(r) == (owner['function_va'],field['function_offset']) and r['event'] != event]
            require(len(hits) == 1 and hits[0]['coff_relocation']['kind'] == 6 and
                hits[0]['coff_relocation']['symbol'] == field['proposed_target_symbol'] and
                hits[0]['exact_original_target_va'] == field['target_va'] and
                hits[0]['proof_consistency'] == 'EXACT_OWN_SOURCE_RESOLUTION', 'fresh source binding migration differs')
    return dict(original_missing_count=len(old), overlay_missing_count=len(new), repaired_count=len(wanted),
                unresolved_original_fields=[dict(function_va=a,offset=b) for a,b in sorted(new)])


def save_gzip(path, rows):
    with Path(path).open('xb') as raw:
        with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as stream:
            for row in rows: stream.write((json.dumps(row,sort_keys=True,separators=(',',':'))+'\n').encode())


def run(args):
    require(args.compile_only is True and os.name == 'nt', 'explicit Windows compile-only operation required; no prepare mode')
    started = time.monotonic(); p = policy(); this = Path(__file__).resolve()
    require(file_hash(this) == args.implementation_sha256, 'reviewed implementation differs')
    observations = {this:args.implementation_sha256,POLICY:POLICY_SHA,PROPOSAL:p['proposal_sha256']}
    data = {}
    for name,path in frozen.DEFAULTS.items():
        data[name] = frozen.read_bound(path,frozen.PINS[name]); observations[path] = frozen.PINS[name]
    evidence = {}
    for relative,pin in p['inputs'].items():
        observations[ROOT/relative] = pin
        if relative.endswith(('absolute-triage-evidence-v1.json','entry-dependencies-next-projects-v1.json')):
            evidence[Path(relative).name] = frozen.read_bound(ROOT/relative,pin)
    reference = Path(args.reference).resolve(); observations[reference] = frozen.PINS['reference']
    doctor = Path(args.doctor).resolve(); observations[doctor] = file_hash(doctor)
    tc = json.loads(doctor.read_text())['toolchains']['sp1']; compiler_root,_ = toolchain.layout(tc['root']); cl = compiler_root/'VC/bin/cl.exe'
    require(tc['ready'] and tc['version'] == '15.00.30729.01' and tc['cl_sha256'] == data['manifest']['toolchains']['sp1']['cl_sha256'] == file_hash(cl), 'compiler differs')
    for name in ('VC/bin/cl.exe','VC/bin/c1xx.dll','VC/bin/c2.dll'): observations[compiler_root/name] = file_hash(compiler_root/name)
    for name,pin in data['retained']['inputs']['tools_sha256'].items(): observations[ROOT/name] = pin
    for name in TOOLS: observations.setdefault(ROOT/name,file_hash(ROOT/name))
    index = ROOT/'build/function_index.json'; require(not index.exists() and data['retained']['inputs']['function_index_present'] is False, 'optional index state differs')
    prepared = []
    for spec in p['units']:
        idx = spec['recipe_index']; unit = data['manifest']['units'][idx]; recipe = data['recipes']['units'][idx]; proof = data['retained']['units'][idx]
        require(unit['recipe_id'] == spec['recipe_id'] and unit['recipe'] == recipe and recipe['source'] == spec['source'] and recipe['compiler'] == spec['compiler'] == 'sp1' and recipe['flags'] == spec['flags'], 'original recipe differs')
        require(len(recipe['functions']) == spec['expected_complete_function_rows'] and first.row_identities(proof['verified_functions']) == first.row_identities(recipe['functions']) and all(r['verdict'] == 'match' for r in proof['verified_functions']), 'complete retained rows differ')
        require(proof['recipe_id'] == unit['recipe_id'] and proof['object_sha256'] == unit['object_sha256'] and
                proof['source_sha256_recorded'] == proof['source_sha256_current'] == unit['source_sha256'] == spec['source_sha256'], 'original source/object ancestry differs')
        source = ROOT/spec['source']; observations[source] = spec['source_sha256']
        original = (frozen.DEFAULTS['manifest'].parent/data['manifest'].get('object_root_relative','.')/unit['object']).resolve(); observations[original] = unit['object_sha256']
        for h in spec['headers']:
            path = (ROOT if h['kind'] == 'source' else compiler_root)/h['path']; observations[path] = h['sha256']
            if h['kind'] == 'source':
                text = path.read_text()
                require(not re.search(r'\b(__FILE__|__DATE__|__TIME__|__COUNTER__|__TIMESTAMP__)\b',text), 'source header context unsupported')
        for owner in spec['owners']:
            require(data['selection']['selections'][owner['function_va']] == owner['original_selected_owner'], 'selected original owner differs')
            for field in owner['fields']:
                original_rows = [r for r in evidence['absolute-triage-evidence-v1.json']['rows'] if
                    (r['recipe_id'],r['function_va'],r['function_offset']) == (spec['recipe_id'],owner['function_va'],field['function_offset'])]
                require(len(original_rows) == 1 and all(field.get(k) == v for k,v in original_rows[0].items()), 'original triage field differs')
                entry_rows = [r for r in evidence['entry-dependencies-next-projects-v1.json']['original_missing_fields'] if
                    (r['recipe_id'],r['function_va'],r['source_field_offset']) == (spec['recipe_id'],owner['function_va'],field['function_offset'])]
                require(len(entry_rows) == 1 and all(entry_rows[0].get(k) == v for k,v in field['entry_binding_reference'].items()), 'original reachable binding differs')
        prepared.append((spec,unit,original,transform(source.read_bytes(),spec)))
    require(len(prepared) == 6 and sum(len(s['owners']) for s,_,_,_ in prepared) == 10 and sum(len(o['fields']) for s,_,_,_ in prepared for o in s['owners']) == 19, 'fixed batch census differs')
    require(all(file_hash(path) == pin for path,pin in observations.items()), 'stale protected input')
    out = frozen.new_output(args.out,observations); out.mkdir(parents=True)
    def note(state,**fields):
        with (out/'progress.jsonl').open('a',encoding='utf-8') as stream:
            stream.write(json.dumps(dict(state=state,**fields))+'\n'); stream.flush(); os.fsync(stream.fileno())
    note('started',implementation_sha256=args.implementation_sha256)
    ancestry = dict(kind='fnv-original-recipe-ancestry',inputs={str(k):v for k,v in observations.items()},
        units=[dict(recipe_id=u['recipe_id'],recipe_index=u['recipe_index'],original_source_sha256=u['source_sha256'],original_object_sha256=u['object_sha256'],owners=s['owners']) for s,u,_,_ in prepared])
    frozen.save(out/'original-ancestry.json',ancestry)
    report = dict(kind='fnv-entry-nineteen-overlay-result',status='error',input_stability_verified=False, units=[],
        game_execution=False,link_performed=False,provider_selected=False,runtime_eligible=False,runtime_closure_verified=False,game_fixups_approved=0)
    try:
        image = ImagePe(reference); ok,hits,probes = image_ok(image); require(ok,'original image probes failed')
        pe = Pe(reference)
        try:
            highlows = sorted(pe.base+r for r in pe.relocations())
            for spec,unit,original,generated in prepared:
                folder = out/spec['recipe_id']; folder.mkdir(); source = folder/Path(spec['source']).name; obj = folder/'overlay.obj'
                with source.open('xb') as stream: stream.write(generated)
                command = [cl,'/c','/nologo']+unit['recipe']['flags']+['/I'+str((ROOT/spec['source']).parent),'/I'+str(ROOT/'include'),'/showIncludes',source,'/Fo'+str(obj)]
                require(all(file_hash(path) == pin for path,pin in observations.items()) and file_hash(source) == sha(generated), 'input drift before compile')
                note('compile_started',recipe_id=spec['recipe_id'])
                code,text = toolchain.run(command,compiler_root,ROOT,timeout=120)
                with (folder/'compile.log').open('x',encoding='utf-8') as stream: stream.write(text)
                require(code == 0 and obj.is_file(),'overlay compile failed')
                obj_hash = file_hash(obj); frozen.generated_stability(source,obj,sha(generated),obj_hash)
                includes = [Path(x.strip()).resolve() for x in re.findall(r'(?im)^Note: including file:\s*(.+)$',text)]
                allowed = {((ROOT if h['kind'] == 'source' else compiler_root)/h['path']).resolve() for h in spec['headers']}
                require(set(includes) <= allowed and (bool(includes) or not allowed), 'actual include origin outside fixed closure')
                before,after = Coff(original),Coff(obj); require(sha(after.data) == obj_hash,'object drift during parse')
                geometry = [verify_owner(before,after,o,unit['recipe']) for o in spec['owners']]
                comparable = CompareCoff(obj); require(sha(comparable.data) == obj_hash,'object drift before oracle')
                rows = plain_compare(comparable,image,unit['recipe'])
                sanitized = [{k:v for k,v in r.items() if k != 'byte_differences'} | dict(byte_difference_offsets=[d['offset'] for d in r['byte_differences']]) for r in rows]
                frozen.save(folder/'comparison.json',dict(rows=sanitized)); complete_matches(rows,unit['recipe'],spec['owners'])
                oldrows,oldcounts,_ = source_bound_rows(before,unit,pe,highlows,data['selection'])
                newrows,newcounts,functions = source_bound_rows(after,unit,pe,highlows,data['selection'])
                migration = migrations_match(oldrows,newrows,spec)
                lane = dict(original_object_sha256=unit['object_sha256'],overlay_object_sha256=obj_hash,original_source_sha256=spec['source_sha256'],generated_source_sha256=sha(generated))
                for row in newrows: row.update(overlay_lane=lane,producer_sha256=args.implementation_sha256)
                save_gzip(folder/'source-bindings.jsonl.gz',newrows)
                allphysical = [dict(section=sec['index'],**relocation_record(after,sec,r)) for sec in after.sections.values() for r in sec['relocs']]
                frozen.save(folder/'native-inventory.json',dict(object_sha256=obj_hash,**inventory(after),all_physical_fields=allphysical))
                frozen.save(folder/'migration.json',dict(original_ancestry_sha256=file_hash(out/'original-ancestry.json'),lane=lane,geometry=geometry,
                    census=migration,original_highlow_partition=oldcounts,overlay_highlow_partition=newcounts,original_global_missing_census_unchanged=88,original_entry_missing_census_unchanged=47))
                frozen.generated_stability(source,obj,sha(generated),obj_hash)
                artifacts = {p.name:file_hash(p) for p in (source,obj,folder/'comparison.json',folder/'source-bindings.jsonl.gz',folder/'native-inventory.json',folder/'migration.json',folder/'compile.log')}
                report['units'].append(dict(recipe_id=spec['recipe_id'],recipe_index=spec['recipe_index'],lane=lane,actual_includes=[str(p) for p in includes],
                    flags=unit['recipe']['flags'],context_adaptations=['original-source-directory include search','/showIncludes'],plain_comparison_rows=len(rows),
                    fresh_verified_functions=functions,migration=migration,artifacts=artifacts))
                note('unit_verified',recipe_id=spec['recipe_id'],object_sha256=obj_hash)
        finally: pe.close()
        del image
        require(sum(u['plain_comparison_rows'] for u in report['units']) == 619,'batch row census differs')
        require(not index.exists() and all(file_hash(path) == pin for path,pin in observations.items()),'protected input drift at completion')
        for u in report['units']:
            folder = out/u['recipe_id']; require(all(file_hash(folder/name) == pin for name,pin in u['artifacts'].items()),'generated artifact drift at completion')
        manifest = dict(schema_version=1,kind='fnv-runtime-source-overlay-manifest',policy_sha256=POLICY_SHA,
            producer_sha256=args.implementation_sha256,original_ancestry_sha256=file_hash(out/'original-ancestry.json'),units=report['units'],
            binding_scope='all original recipe function rows; all object physical fields inventoried separately; unowned metadata/data fields have no invented original mapping',
            alternate_owner_selection_performed=False,provider_selected=False,runtime_eligible=False,link_ready=False,runtime_closure_verified=False)
        frozen.save(out/'runtime-overlays.json',manifest)
        report.update(status='pass_pending_independent_review',input_stability_verified=True,generated_artifacts_stability_verified=True,
            original_ancestry_sha256=file_hash(out/'original-ancestry.json'),runtime_overlays_sha256=file_hash(out/'runtime-overlays.json'),image_gate=dict(hits=hits,probes=probes))
        note('verified_pending_review')
    except Exception as error:
        report['error'] = str(error); note('failed',error_type=type(error).__name__)
    report.update(elapsed_seconds=time.monotonic()-started,observer_peak_memory_bytes=peak_memory_bytes(),compiler_child_peak_memory_measured=False)
    frozen.save(out/'result.json',report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compile-only',action='store_true',required=True)
    for name in ('reference','doctor','out'): parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--implementation-sha256',required=True)
    args = parser.parse_args()
    try: result = run(args)
    except (ValueError,OSError,KeyError,TypeError) as error: parser.exit(2,'batch rejected: '+str(error)+'\n')
    print(result['status']); return 0 if result['status'] == 'pass_pending_independent_review' else 1


if __name__ == '__main__': raise SystemExit(main())
