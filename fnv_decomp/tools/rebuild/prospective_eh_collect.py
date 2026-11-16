"""Finite prospective UUID-seven observation driver; validation is the default.

Source-phase requests cannot authorize reads. A separately reviewed successor,
root-confirmed original scope and coordinator CPU reservation precede --observe.
No compiler, linker, serializer, executable or service operations exist here.
"""
from __future__ import annotations
import argparse,hashlib,importlib,json,os,re,struct,sys,tempfile,time
from pathlib import Path
observer=None
peak_memory_bytes=lambda:None
FALSE=dict(runtime_eligible=False,provider_selected=False,ABI_verified=False,frame_contract_verified=False,no_catch_family_approved=False,full_closure_verified=False,emission_performed=False)

ROOT=Path(__file__).resolve().parents[2]
EXPECTED={1445:{'0x00c546c0'},2769:{'0x00c55200'},2770:{'0x00c5f240','0x00c43500'},2779:{'0x00c65530','0x00c618f0','0x00c616c0'}}
AUTHORITY={
'build/rebuild/uuid2768-factory-result-v2/receipt.json':'fdec31d202ebbed1e846c0c8198a384db995d05aab5433b75d475b4f820ba98c',
'build/rebuild/uuid2768-factory-result-v2/field-proofs.jsonl.gz':'4b7cb6ce64a9a84d461ef0ef536cd17c5952fe03b697e45e652e18c2f5e7cc31',
'build/rebuild/root-certificate-composer-v1/physical-provider-map.json':'6cd5bf884bb28d460cfc92f63b765c15413904f58355844243ddd6b59b97001c',
'build/rebuild/objects-20261103T030230Z-7cfc935c.json':'bc62a5fb2553431b1e0547d11f366e52efb73096ea8ceb206c556ae5740a53eb',
'build/rebuild/uuid-seven-source-dispatch-v1.json':'2a6e12dd10dd681e7d35714b83a2bc6189b9a76a402366283bc19ace2d290b3e',
'build/rebuild/uuid2768-prospective-closure-plan-v3.json':'db659e156110720c60463b83424ff4a034f0e1267343e0dce6f101bcb708ba95',
'build/rebuild/uuid-seven-selected-metadata-v2/bundle.json':'26008825f858fc61de9013bad3056314c4cc9ddff25b0c800cc267f38d5fbc3b',
'build/rebuild/uuid-seven-selected-metadata-v2/independent-outcome-review-v1.json':'11141f6baed65c8b1cba64e54676af2acd73be8dbe0dce00edb0b731ba1b7983',
'build/rebuild/cached-code-frontier-inventory-v13-v1/metadata-request.json':'fdfcd3773c0b3e50fa7cc9ec63982556825fb9e4eab2a9d0e77f30b429ea32c4',
'build/rebuild/cached-root-observation-v13-v1/receipt.json':'846087b14800e313181064f5a897c110f8d07cc261c89e8b2730a75ad04efc08'}
TOOLS=('tools/rebuild/prospective_eh_collect.py','tools/rebuild/prospective_eh_observe.py','tools/rebuild/coff_code_archive.py','tools/rebuild/coff_inventory.py','tools/build_and_match.py','tools/compare.py','tools/function_spans.py')
def need(ok,why):
    if not ok:raise ValueError(why)
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def bounded(path,limit,budget):
    budget();before=path.stat();need(before.st_size<=limit,'file cap');parts=[];size=0
    with path.open('rb') as stream:
        while True:
            budget();block=stream.read(min(1048576,limit-size+1))
            if not block:break
            size+=len(block);need(size<=limit,'growing file cap');parts.append(block)
    after=path.stat();need((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns),'file changed during read');return b''.join(parts)
def private(path):
    p=path.resolve();need(p.is_relative_to((ROOT/'build/rebuild').resolve()),'private output required');return p
def bounded_hash(path,limit,budget):
    budget();before=path.stat();need(before.st_size<=limit,'hash file cap');import hashlib
    h=hashlib.sha256();size=0
    with path.open('rb') as stream:
        while True:
            budget();block=stream.read(min(1048576,limit-size+1))
            if not block:break
            size+=len(block);need(size<=limit,'growing hash cap');h.update(block)
    after=path.stat();need((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns) and size==after.st_size,'file changed during hash');return h.hexdigest()
def validate_request(request,execute=False):
    need(request.get('kind')=='prospective-UUID-seven-parent-EH-v1' and request.get('authority_kind')=='qualified-caller-prospective-only','unknown/prospective authority required')
    need(request.get('measured_V13_or_593_authority') is False,'prospective roots are not measured roots')
    units=request['units'];need(len(units)==4,'four units required');seen=set()
    for unit in units:
        index=unit['recipe_index'];need(index in EXPECTED and index not in seen,'foreign/duplicate unit');seen.add(index)
        need(re.fullmatch('%04d-[0-9a-f]{16}'%index,unit['recipe_id']) is not None,'unsafe/mismatched recipe ID')
        roots=unit['roots'];need(len(roots)==len(EXPECTED[index]) and {r['original_address'] for r in roots}==EXPECTED[index],'exact seven root set required')
        need(all(r['size']==157 and r['recipe_id']==unit['recipe_id'] and r['recipe_index']==index and r['object_sha256']==unit['object_sha256'] for r in roots),'selected unit/root identity differs')
        need('0x00c50610' not in {r['original_address'] for r in roots},'historical 2770 root forbidden')
    need(seen==set(EXPECTED),'four exact recipes required')
    need(request.get('DATA01204364_materialization_approved') is False,'DATA scope forbidden')
    need(request.get('authority')==AUTHORITY,'exact prospective authorities required')
    declared={r['path']:r['sha256'] for r in request['inputs']};need(len(declared)==len(request['inputs']),'duplicate requested input')
    for row in request['inputs']:need(type(row.get('limit',64*1024**2)) is int and 0<row.get('limit',64*1024**2)<=64*1024**2,'unbounded requested input')
    need(all(declared.get(p)==h for p,h in AUTHORITY.items()),'authority input pins incomplete')
    need(all(p in declared and len(declared[p])==64 for p in TOOLS),'semantic producer pins incomplete')
    if execute:
        permit=request['permissions']
        need(permit.get('root_original_scope_confirmed') is True and permit.get('source_input_review_receipt_sha256') and permit.get('coordinator_CPU_lease_id'),'original scope/source input review/CPU lease not confirmed')
        need(request.get('reference') is not None and request.get('reference_image_gate') is not None,'reference scope not established')
    return dict(units=4,roots=7,original_reads_permitted=bool(execute),scope='prospective-only',**FALSE)
def allocation_preflight(raw):
    need(20<=len(raw)<=16*1024**2,'raw COFF cap');count=struct.unpack_from('<H',raw,2)[0];need(0<count<=8192 and 20+40*count<=len(raw),'COFF section count')
    declared=sum(struct.unpack_from('<I',raw,20+40*i+16)[0] for i in range(count));need(declared<=256*1024**2,'declared COFF allocation cap')
    return declared
def executable_ranges(pe):
    data=pe.data;header=struct.unpack_from('<I',data,0x3c)[0];need(data[header:header+4]==b'PE\0\0','PE signature');count=struct.unpack_from('<H',data,header+6)[0];optional=struct.unpack_from('<H',data,header+20)[0];need(0<count<=96,'PE section count');rows=[]
    for i in range(count):
        at=header+24+optional+40*i;virtual,rva,raw=struct.unpack_from('<III',data,at+8);flags=struct.unpack_from('<I',data,at+36)[0]
        if flags&0x20000000:rows.append((pe.base+rva,pe.base+rva+max(virtual,raw)))
    return rows
def copy_authenticated_buffer(raw,expected,scratch,name,budget):
    need(hashlib.sha256(raw).hexdigest()==expected,'buffer SHA differs');allocation_preflight(raw);need(re.fullmatch(r'[0-9]{4}-[0-9a-f]{16}\.obj',name) is not None,'unsafe scratch name')
    copied=scratch/name;need(copied.resolve().parent==scratch.resolve(),'scratch path escaped');budget()
    with copied.open('xb') as stream:st=os.fstat(stream.fileno());stream.write(raw);stream.flush();os.fsync(stream.fileno())
    need(bounded_hash(copied,16*1024**2,budget)==expected,'scratch copy differs');return copied,st
def observe_request(request):
    global observer,peak_memory_bytes
    validate_request(request,True)  # Before any original/authority input read.
    start=time.monotonic()
    def budget():
        need(time.monotonic()-start<=540,'observation deadline');peak=peak_memory_bytes();need(peak is None or peak<=1024**3,'observation memory cap')
    out=private(ROOT/request['output_directory']);need(out.parent==(ROOT/'build/rebuild').resolve() and out.name.startswith('prospective-uuid-seven-') and not out.exists(),'exclusive dedicated output required')
    pins={}
    for row in request['inputs']:
        p=(ROOT/row['path']).resolve();need(p not in pins,'duplicate input');pins[p]=(row['sha256'],row.get('limit',64*1024**2))
    # The actual operator must start a fresh process. Authenticate the complete
    # non-stdlib semantic import graph before importing any producer.
    need(not any(name in sys.modules for name in ('prospective_eh_observe','coff_code_archive','build_and_match','compare','function_spans','coff_inventory')),'fresh semantic process required')
    for name in TOOLS:
        p=(ROOT/name).resolve();need(p in pins and bounded_hash(p,1024**2,budget)==pins[p][0],'semantic source hash differs')
    sys.path.insert(0,str(ROOT/'tools/rebuild'));sys.path.insert(0,str(ROOT/'tools'))
    observer=importlib.import_module('prospective_eh_observe');peak_memory_bytes=importlib.import_module('coff_inventory').peak_memory_bytes
    expected_modules={'prospective_eh_observe':'tools/rebuild/prospective_eh_observe.py','build_and_match':'tools/build_and_match.py','compare':'tools/compare.py','function_spans':'tools/function_spans.py','coff_code_archive':'tools/rebuild/coff_code_archive.py','coff_inventory':'tools/rebuild/coff_inventory.py'}
    for module_name,rel in expected_modules.items():
        module=sys.modules.get(module_name);p=(ROOT/rel).resolve();need(module is not None and Path(module.__file__).resolve()==p,'shadowed semantic module');need(bounded_hash(p,1024**2,budget)==pins[p][0],'producer changed during import')
    for unit in request['units']:
        p=(ROOT/unit['object']).resolve();need(p not in pins,'object/input collision');pins[p]=(unit['object_sha256'],16*1024**2)
    ref=request['reference'];image=Path(ref['path']).resolve();need(image not in pins,'reference/input collision');pins[image]=(ref['sha256'],512*1024**2)
    need(not any(p.is_relative_to(out) or p==out for p in pins),'input/output collision')
    def stable():
        for p,(h,limit) in pins.items():need(bounded_hash(p,limit,budget)==h,'input/tool drift '+p.name)
    out.mkdir();scratch=Path(tempfile.mkdtemp(prefix='same-byte-parser-',dir=out));scratch_files=[];results=[];owned_output=None
    journal=(out/'operation.jsonl').open('xb')
    def note(row):journal.write((json.dumps(row,sort_keys=True)+'\n').encode());journal.flush();os.fsync(journal.fileno())
    try:
        note(dict(state='started',request_sha256=digest(request),prospective_only=True));stable()
        recipe_spec=request['recipe_manifest'];recipe_path=(ROOT/recipe_spec['path']).resolve();need(recipe_path in pins and pins[recipe_path][0]==recipe_spec['sha256'],'recipe input pin missing');recipes=json.loads(bounded(recipe_path,pins[recipe_path][1],budget))['units']
        pe=observer.oracle.Pe(image);need(observer.sha(pe.data)==ref['sha256'],'loaded reference drift')
        image_gate=request['reference_image_gate'];gate_path=(ROOT/image_gate['path']).resolve();need(gate_path==(ROOT/'build/image_check.json').resolve() and gate_path in pins and pins[gate_path][0]==image_gate['sha256'],'baseline image gate pin missing');need(observer.oracle.image_ok(pe)[0],'unchanged image gate failed')
        executable=executable_ranges(pe);global_names=observer.oracle.recipe_names(recipes)
        raw_total=0
        for unit in request['units']:
            budget();path=(ROOT/unit['object']).resolve();raw=bounded(path,16*1024**2,budget);raw_total+=len(raw);need(raw_total<=32*1024**2,'four-object raw cap');need(observer.sha(raw)==unit['object_sha256'],'loaded object drift');allocation_preflight(raw)
            # Exactly one payload hydration per unit; pre/post full integrity passes
            # are additional original reads, explicitly disclosed in the receipt.
            note(dict(state='scratch-planned',name=unit['recipe_id']+'.obj',directory=scratch.name))
            copied,copied_stat=copy_authenticated_buffer(raw,unit['object_sha256'],scratch,unit['recipe_id']+'.obj',budget)
            scratch_files.append((copied,copied_stat))
            core=observer.oracle.Coff(copied);need(observer.sha(core.data)==unit['object_sha256'],'frozen parser byte buffer differs');obj=observer.coff.parse(core.data);recipe=recipes[unit['recipe_index']]
            need(digest(recipe)==unit['recipe_sha256'],'recipe identity differs');unit_result=dict(recipe_id=unit['recipe_id'],object_sha256=unit['object_sha256'],payload_hydrations=1,integrity_full_file_passes=2,scratch_sha256=observer.sha(core.data),roots=[])
            for root in unit['roots']:
                budget()
                try:
                    view=observer.inventory_parent(obj,root)
                    try:view['comparison']=observer.compare_parent(core,obj,view,recipe,recipes,pe,executable,global_names)
                    except (ValueError,KeyError,struct.error) as error:view['comparison']=dict(status='UNSUPPORTED_OR_MISSING_COMPARISON',error_type=type(error).__name__,reason=str(error),reference_evidence=getattr(error,'scope_snapshot',None),**observer.FALSE)
                    unit_result['roots'].append(view)
                except (ValueError,KeyError,struct.error) as error:unit_result['roots'].append(dict(root=root,status='UNSUPPORTED_PHYSICAL_GRAPH',error_type=type(error).__name__,reason=str(error),**observer.FALSE))
                budget()
            results.append(unit_result)
            note(dict(state='unit-observed',recipe_id=unit['recipe_id'],root_count=len(unit_result['roots'])))
        stable();budget();report=dict(kind=request['kind'],authority_kind=request['authority_kind'],request_sha256=digest(request),status='observed-not-admission',units=results,scope='exact seven selected comparisons; no whole-unit EH scan/filter',scratch=dict(original_bytes_copied_not_serialized=True,files=[p.name for p,_ in scratch_files],cleanup_after_success=True,preserve_on_failure=True),**observer.FALSE)
        encoded=json.dumps(report,sort_keys=True,indent=2).encode();need(len(encoded)<=32*1024**2,'report cap');destination=out/'observation.json'
        with destination.open('xb') as stream:owned_output=os.fstat(stream.fileno());stream.write(encoded);stream.flush();os.fsync(stream.fileno())
        stable();budget();now=destination.stat();need((now.st_dev,now.st_ino)==(owned_output.st_dev,owned_output.st_ino),'published output replaced');need(observer.sha(bounded(destination,32*1024**2,budget))==observer.sha(encoded),'published output changed')
        for p,st in scratch_files:
            now=p.stat();need((now.st_dev,now.st_ino)==(st.st_dev,st.st_ino),'scratch replaced');need(p.resolve().is_relative_to(out) and p.parent==scratch,'scratch cleanup target');p.unlink()
        scratch.rmdir();note(dict(state='complete',sha256=observer.sha(encoded)));return dict(output=str(destination.relative_to(ROOT)),sha256=observer.sha(encoded),**observer.FALSE)
    except BaseException as error:
        if owned_output is not None:
            p=out/'observation.json'
            if p.exists() and (p.stat().st_dev,p.stat().st_ino)==(owned_output.st_dev,owned_output.st_ino):p.unlink()
        with (out/'failure.json').open('x') as stream:json.dump(dict(status='failed',error_type=type(error).__name__,reason=str(error),scratch_directory=scratch.name,scratch_preserved=[p.name for p,_ in scratch_files],additional_failed_copy_name_in_journal=True,**observer.FALSE),stream,indent=2)
        note(dict(state='failed',error_type=type(error).__name__))
        raise
    finally:journal.close()
def main():
    p=argparse.ArgumentParser();p.add_argument('--request',required=True);p.add_argument('--observe',action='store_true');args=p.parse_args();path=Path(args.request).resolve();need(path.stat().st_size<=1024**2,'request cap');request=json.loads(path.read_bytes())
    print(json.dumps(observe_request(request) if args.observe else validate_request(request)))
if __name__=='__main__':main()
