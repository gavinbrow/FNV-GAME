"""Lossless indexed recipe frames for an already verified binding stream.

This metadata cache supplies original rows to frozen validators. It creates no
contract, closure decision, provider, native object or runtime admission.
"""
from __future__ import annotations
import argparse
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import time
import zlib

import runtime_code_inventory as frozen
from coff_inventory import peak_memory_bytes, reconcile_recipes

ROOT=Path(__file__).resolve().parents[2]
POLICY='lossless-binding-context-cache-v1'
PINS=dict(binding='275714631903758efbf5a4f82e2428c6f51838f53b90d0c56d2e5dec5da1d804',
    rows='4dfc437064b16c1bb933008aebf7def8d279a903eef9cca24d0fedcc12d7d826',
    selection='48ae62cdc5b1754b9c4af674ef4716d53afb554882e174a93acf860eaf1c6cb1',
    manifest='bc62a5fb2553431b1e0547d11f366e52efb73096ea8ceb206c556ae5740a53eb',
    retained='04d44b73e81982f846bfe8d81806db72ea669586b579ff22007dfd6f7d831297',
    recipes='62f2c8da5f0daa912abdf4576328706711c6561eef7f01c93a89cb71ad46fb6c',
    planned_map='6cd5bf884bb28d460cfc92f63b765c15413904f58355844243ddd6b59b97001c')
TOOLS={'runtime_code_inventory.py':'c2fdbd52b4b7f4b7c68f9d80ad03708ba57d42b29e5938dfcf9769366a1ffd0b',
    'import_plan.py':'6b9237ab5951e7d4a2ac2f9b0c3435f0a667a9fdebac02a4534ba0e30ba98d9c',
    'runtime_gaps.py':'0399e0f91e94de781512a153ac598f4d5eb6210920bc58241542339c72904116',
    'data_plan.py':'e013ed5f217f9beeeaf571d089a36df22b645559063e826554179cea506f5bf8',
    'coff_inventory.py':'3518c044738046e7cd9c8be37a3b1077af750fb2e7a19db793b09999a07ee0d2'}
SEQUENCE='d59b03314c5e061745ccba02af72fc6da00a77ecda4e2d94fafb9e340cff2d6e'
MAX_OUTPUT=128*1024**2
MAX_JOURNAL=65536
MAX_FRAME_RAW=256*1024**2
MAX_LINE=262144
MAX_SECONDS=900
MAX_MEMORY=1024**3
FALSE=dict(provider_selected=False,runtime_eligible=False,ABI_verified=False,link_ready=False,
    namespace_approved=False,full_serialization_eligible=False,materialization_approved=False,
    native_tools_run=False,contract_created=False,admission_decision_created=False)
require=frozen.require
canonical=frozen.canonical
digest=frozen.digest
file_hash=frozen.file_hash


def budget(start):
    require(time.monotonic()-start<=MAX_SECONDS,'cache time bound exceeded')
    peak=peak_memory_bytes();require(peak is None or peak<=MAX_MEMORY,'cache memory bound exceeded')
    return peak


def dependencies():
    for name,h in TOOLS.items():require(file_hash(ROOT/'tools/rebuild'/name)==h,'cache validator dependency changed: '+name)
    require(Path(frozen.__file__).resolve()==ROOT/'tools/rebuild/runtime_code_inventory.py','foreign binding validator')
    return {ROOT/'tools/rebuild'/name:h for name,h in TOOLS.items()}


def verify_hashes(paths,message):
    require(all(file_hash(p)==h for p,h in paths.items()),message)


def make_rosters(manifest,proof,selections,planned,*,expected_units=2988,expected_selected=68657):
    units=sorted(manifest['units'],key=lambda u:u['recipe_index']); proofs={u['recipe_index']:u for u in proof['units']}
    require(len(units)==len(proofs)==expected_units and len({u['recipe_id'] for u in units})==expected_units and
        [u['recipe_index'] for u in units]==list(range(expected_units)), 'complete recipe roster differs')
    require(set(planned['providers'])==set(selections) and len(selections)==expected_selected and planned['materialized_exports']==0 and
        planned['provider_selected'] is False and planned['runtime_eligible'] is False,'planned selected roster differs/promoted')
    result=[];seen=set();physical=set()
    for unit in units:
        pv=proofs[unit['recipe_index']];frozen.check_unit(unit,pv)
        chosen=frozen.selected_rows(unit,pv,selections);roster=[]
        for f in chosen:
            address=f['original_address'];p=planned['providers'][address]
            require(address not in seen and p['recipe_id']==unit['recipe_id'] and p['object_sha256']==unit['object_sha256'] and
                p['source_sha256']==unit['source_sha256'] and (p['section'],p['value'],p['size'],p['symbol'])==(f['section'],f['value'],f['size'],f['symbol']), 'stale selected physical roster')
            key=(unit['recipe_id'],p['object_sha256'],p['symbol_index']);require(key not in physical,'duplicate physical selected roster')
            physical.add(key);seen.add(address)
            roster.append([address,f['symbol'],f['section'],f['value'],f['size'],p['symbol_index'],0,0])
        result.append(dict(recipe_index=unit['recipe_index'],recipe_id=unit['recipe_id'],object_sha256=unit['object_sha256'],
            source_sha256=unit['source_sha256'],recipe_unit_sha256=pv['recipe_unit_sha256'],roster=sorted(roster)))
    require(seen==set(selections),'selected roster incomplete')
    return result


class FrameWriter:
    def __init__(self,target,rosters,start):
        require(target.tell()==0,'frame target must be empty');self.target=target;self.rosters=rosters;self.start=start
        self.entries=[];self.ordinal=0;self.raw_hash=hashlib.sha256();self.data_hash=hashlib.sha256();self.global_seq=hashlib.sha256()
        self.current=-1;self.encoder=None;self._open()
    def _write(self,data):
        self.target.write(data);self.data_hash.update(data);self.comp_hash.update(data)
        require(self.target.tell()<=MAX_OUTPUT,'compressed cache bound exceeded')
    def _open(self):
        self.current+=1
        if self.current==len(self.rosters):self.encoder=None;return
        self.entry=dict(self.rosters[self.current],offset=self.target.tell(),preceding_ordinal=self.ordinal)
        require(self.entry['recipe_index']==self.current,'recipe roster order differs')
        self.entry['roster']=[list(r) for r in self.entry['roster']]
        self.encoder=zlib.compressobj(level=9,wbits=31);self.comp_hash=hashlib.sha256();self.raw_frame=hashlib.sha256();self.seq=hashlib.sha256()
        self.events=Counter();self.classes=Counter();self.kinds=Counter();self.consistency=Counter();self.functions=Counter();self.missing=Counter()
        self.raw_bytes=0;self.count=0
    def _close(self):
        self._write(self.encoder.flush())
        self.entry.update(compressed_bytes=self.target.tell()-self.entry['offset'],compressed_sha256=self.comp_hash.hexdigest(),
            raw_bytes=self.raw_bytes,raw_sha256=self.raw_frame.hexdigest(),row_count=self.count,
            first_ordinal=self.entry['preceding_ordinal']+1 if self.count else None,last_ordinal=self.ordinal if self.count else None,
            row_sequence_sha256=self.seq.hexdigest(),summary=dict(events=dict(self.events),target_classes=dict(self.classes),
                relocation_kinds=dict(self.kinds),proof_consistency=dict(self.consistency)),missing_fields=sum(self.missing.values()),missing_functions=len(self.missing))
        for row in self.entry['roster']:row[6:]=[self.functions[row[0]],self.missing[row[0]]]
        require(sum(row[6] for row in self.entry['roster'])==self.count,'foreign function in frame')
        self.entries.append(self.entry);self._open();budget(self.start)
    def accept(self,line):
        require(type(line) is bytes and 0<len(line)<=MAX_LINE,'original line bound/type differs')
        e=json.loads(line);index=e['recipe_index']
        require(type(index) is int and self.current<=index<len(self.rosters),'foreign/unsorted recipe frame')
        while self.current<index:self._close()
        require(e['recipe_id']==self.entry['recipe_id'],'foreign recipe identity')
        self.ordinal+=1;self.count+=1;require(self.ordinal<=1000000 and self.count<=150000,'row count bound')
        self.raw_bytes+=len(line);require(self.raw_bytes<=MAX_FRAME_RAW,'uncompressed recipe frame bound')
        self.raw_hash.update(line);self.raw_frame.update(line)
        item=canonical([self.ordinal,digest(e)]);self.seq.update(item);self.global_seq.update(item)
        self.events[e['event']]+=1;self.classes[e['classification']]+=1;self.functions[e['function_va']]+=1
        if e['coff_relocation'] is None:self.missing[e['function_va']]+=1
        else:
            self.kinds[str(e['coff_relocation']['kind'])]+=1;self.consistency[e['proof_consistency']]+=1
        self._write(self.encoder.compress(line))
        if self.count%256==0:budget(self.start)
    def finish(self):
        while self.encoder is not None:self._close()
        return dict(frames=self.entries,data_bytes=self.target.tell(),data_sha256=self.data_hash.hexdigest(),
            original_raw_sha256=self.raw_hash.hexdigest(),rows=self.ordinal,row_sequence_sha256=self.global_seq.hexdigest())


def build_frames(lines,target,rosters,selections,summary,*,required_missing=88,required_functions=59,expected_sequence=SEQUENCE,start=None):
    start=time.monotonic() if start is None else start;writer=FrameWriter(target,rosters,start)
    def captured():
        for line in lines:writer.accept(line);yield line
    reader=frozen.BindingReader(captured(),summary,selections)
    for roster in rosters:
        bucket=reader.take(roster['recipe_index']);del bucket;budget(start)
    census=reader.finish(required_missing,required_functions);result=writer.finish()
    require(result['row_sequence_sha256']==census['sequence_sha256']==expected_sequence,'global original sequence differs')
    result['binding_census']=census;return result


class OrdinalReader(frozen.BindingReader):
    def __init__(self,lines,summary,selections,preceding):
        self.seed=preceding;super().__init__(lines,summary,selections)
    def _advance(self):
        if self.seed is not None:self.ordinal=self.seed;self.seed=None
        super()._advance()


def frame_lines(stream,entry,start):
    stream.seek(entry['offset']);remaining=entry['compressed_bytes'];decoder=zlib.decompressobj(31)
    comp=hashlib.sha256();raw=hashlib.sha256();raw_bytes=0;buffer=b''
    while remaining:
        block=stream.read(min(65536,remaining));require(block,'truncated frame');remaining-=len(block);comp.update(block)
        pending=block
        while pending:
            part=decoder.decompress(pending,1024**2);pending=decoder.unconsumed_tail
            require(not decoder.unused_data,'extra/concatenated gzip member')
            raw.update(part);raw_bytes+=len(part);require(raw_bytes<=entry['raw_bytes']<=MAX_FRAME_RAW,'frame raw bound differs')
            buffer+=part
            parts=buffer.split(b'\n');buffer=parts.pop()
            for line in parts:
                line+=b'\n';require(len(line)<=MAX_LINE,'cached line bound');yield line
            require(len(buffer)<=MAX_LINE,'cached partial line bound');budget(start)
    require(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,'incomplete gzip frame')
    if buffer:yield buffer
    require(raw_bytes==entry['raw_bytes'] and raw.hexdigest()==entry['raw_sha256'] and comp.hexdigest()==entry['compressed_sha256'], 'frame byte hashes differ')


def _read_recipe(data_path,index,recipe_index,selections,unit,proof):
    """Read only one authenticated index range, retaining original row ordinals.

    The caller binds index SHA to the accepted cache receipt. This function does
    not hash unrequested frames or claim global freshness for a bounded read.
    """
    dependencies();require(index['policy_id']==POLICY and index['inputs']==PINS,'foreign cache lineage')
    require(type(recipe_index) is int and 0<=recipe_index<len(index['frames']),'unknown requested recipe')
    entry=index['frames'][recipe_index];frozen.check_unit(unit,proof)
    require((entry['recipe_index'],entry['recipe_id'],entry['object_sha256'],entry['source_sha256'],entry['recipe_unit_sha256'])==
        (recipe_index,unit['recipe_id'],unit['object_sha256'],unit['source_sha256'],proof['recipe_unit_sha256']), 'requested recipe lineage differs')
    selected=frozen.selected_rows(unit,proof,selections)
    expected=sorted((r['original_address'],r['symbol'],r['section'],r['value'],r['size']) for r in selected)
    require([tuple(r[:5]) for r in entry['roster']]==expected,'cached selected roster differs')
    start=time.monotonic()
    with Path(data_path).open('rb') as stream:
        before=os.fstat(stream.fileno());require(before.st_size==index['data_bytes'],'cache data size differs')
        reader=OrdinalReader(frame_lines(stream,entry,start),entry['summary'],selections,entry['preceding_ordinal'])
        bucket=reader.take(recipe_index);census=reader.finish(entry['missing_fields'],entry['missing_functions'])
        require(census['sequence_sha256']==entry['row_sequence_sha256'],'frame global-ordinal sequence differs')
        require(reader.ordinal==entry['preceding_ordinal']+entry['row_count'],'frame row count differs')
        for row in entry['roster']:
            b=bucket.get(row[0],dict(fields=[],missing_fields=[]))
            require(len(b['fields'])+len(b['missing_fields'])==row[6] and len(b['missing_fields'])==row[7], 'frame function roster counts differ')
        after=os.fstat(stream.fileno());require((before.st_size,before.st_mtime_ns,before.st_ctime_ns)==
            (after.st_size,after.st_mtime_ns,after.st_ctime_ns),'cache data changed during bounded read')
    return bucket,dict(recipe_index=recipe_index,raw_sha256=entry['raw_sha256'],compressed_sha256=entry['compressed_sha256'],
        row_count=entry['row_count'],first_ordinal=entry['first_ordinal'],last_ordinal=entry['last_ordinal'],
        whole_data_hash_verified_this_read=False,unrequested_frames_verified=False,**FALSE)


def validate_index(index):
    require(index['schema_version']==1 and index['policy_id']==POLICY and index['inputs']==PINS,'cache index lineage differs')
    require(index['units']==2988 and index['selected_functions']==68657 and index['rows']==490801 and
        index['row_sequence_sha256']==SEQUENCE and type(index['data_bytes']) is int and 0<index['data_bytes']<=MAX_OUTPUT and
        all(index[k] is False for k in FALSE),'cache index scope/promotions differ')
    offset=0;ordinal=0;selected=set();physical=set()
    for i,e in enumerate(index['frames']):
        require(all(type(e[k]) is int for k in ('recipe_index','offset','compressed_bytes','raw_bytes','preceding_ordinal','row_count','missing_fields','missing_functions')) and
            e['recipe_index']==i and e['offset']==offset and 0<e['compressed_bytes']<=MAX_OUTPUT and
            0<=e['raw_bytes']<=MAX_FRAME_RAW and e['preceding_ordinal']==ordinal and 0<=e['row_count']<=150000 and
            0<=e['missing_functions']<=e['missing_fields']<=e['row_count'],'frame index gap/overlap/bound')
        require(all(isinstance(e[k],str) and re.fullmatch('[0-9a-f]{64}',e[k]) for k in ('compressed_sha256','raw_sha256','row_sequence_sha256')), 'frame hashes malformed')
        require((e['first_ordinal'],e['last_ordinal'])==((ordinal+1,ordinal+e['row_count']) if e['row_count'] else (None,None)), 'frame ordinal range differs')
        require(e['roster']==sorted(e['roster']) and sum(r[6] for r in e['roster'])==e['row_count'],'frame roster/count differs')
        for r in e['roster']:
            require(len(r)==8 and r[0] not in selected and all(type(r[k]) is int for k in range(2,8)) and
                r[2]>0 and r[3]>=0 and r[4]>0 and r[5]>=0 and 0<=r[7]<=r[6],'selected roster record differs')
            key=(e['recipe_id'],e['object_sha256'],r[5]);require(key not in physical,'duplicate physical roster')
            selected.add(r[0]);physical.add(key)
        require(sum(r[7] for r in e['roster'])==e['missing_fields'] and sum(bool(r[7]) for r in e['roster'])==e['missing_functions'], 'frame missing roster differs')
        require(sum(e['summary']['events'].values())==sum(e['summary']['target_classes'].values())==e['row_count'] and
            sum(e['summary']['relocation_kinds'].values())==sum(e['summary']['proof_consistency'].values())==e['row_count']-e['missing_fields'], 'frame summary counts differ')
        offset+=e['compressed_bytes'];ordinal+=e['row_count']
    require(len(index['frames'])==index['units'] and len(selected)==index['selected_functions'] and
        ordinal==index['rows'] and offset==index['data_bytes'],'complete cache index differs')


def load_index(path,expected_sha256):
    with Path(path).open('rb') as source:raw=source.read(MAX_OUTPUT+1)
    require(len(raw)<=MAX_OUTPUT and hashlib.sha256(raw).hexdigest()==expected_sha256,'cache index size/hash differs')
    index=json.loads(raw);validate_index(index)
    require(len(raw)+index['data_bytes']+MAX_JOURNAL<=MAX_OUTPUT,'cache data/index size bound')
    return index


class BindingContextCache:
    """Load a receipt-bound index once; each read verifies only its frame.

    The trusted expected index hash comes from the reviewed cache receipt.
    Local Python object construction is not an authentication boundary.
    """
    def __init__(self,data_path,index_path,index_sha256):
        dependencies();self.data_path=Path(data_path).resolve()
        self.index=load_index(index_path,index_sha256);self.index_sha256=index_sha256
        self.metadata_sha256=digest({k:v for k,v in self.index.items() if k!='frames'})
        self.frame_metadata_sha256=tuple(digest(e) for e in self.index['frames'])
        require(self.data_path.name==self.index['data_file'],'cache data filename differs')
    def read_recipe(self,recipe_index,selections,unit,proof):
        require(type(recipe_index) is int and 0<=recipe_index<len(self.frame_metadata_sha256),'unknown requested recipe')
        require(digest({k:v for k,v in self.index.items() if k!='frames'})==self.metadata_sha256 and
            len(self.index['frames'])==len(self.frame_metadata_sha256) and
            digest(self.index['frames'][recipe_index])==self.frame_metadata_sha256[recipe_index], 'loaded cache index was modified')
        return _read_recipe(self.data_path,self.index,recipe_index,selections,unit,proof)


def run(args):
    start=time.monotonic();paths={n:Path(getattr(args,n)).resolve() for n in PINS}
    observed={p:PINS[n] for n,p in paths.items()};require(len(observed)==len(paths),'duplicate input paths')
    require(all(file_hash(p)==h for p,h in observed.items()),'cache input pins differ')
    observed.update(dependencies());observed[Path(__file__).resolve()]=file_hash(__file__)
    load=lambda n:json.loads(paths[n].read_bytes())
    binding,selection,manifest,proof,planned=[load(n) for n in ('binding','selection','manifest','retained','planned_map')]
    require(binding['details_sha256']==PINS['rows'] and all(binding['inputs'][n]==PINS[n] for n in ('selection','manifest','retained','recipes')), 'binding source joins differ')
    require(reconcile_recipes(manifest,paths['recipes'])['verified'],'authoritative recipe differs')
    rosters=make_rosters(manifest,proof,selection['selections'],planned)
    for name,h in proof['inputs']['tools_sha256'].items():
        p=(ROOT/name).resolve();require(p.is_relative_to(ROOT),'foreign proof dependency');require(file_hash(p)==h,'proof dependency differs');observed[p]=h
    out=Path(args.out).resolve();data=Path(args.data).resolve();idx=Path(args.index).resolve();progress=Path(str(out)+'.progress.jsonl')
    reserved=set(observed)
    for unit in manifest['units']:
        reserved.add((paths['manifest'].parent/manifest.get('object_root_relative','.')/unit['object']).resolve())
        reserved.add((ROOT/unit['source']).resolve())
    outputs=(out,data,idx,progress)
    require(all(p.is_relative_to(ROOT/'build/rebuild') for p in outputs),'cache outputs must stay private')
    require(len(set(outputs))==4 and not set(outputs)&reserved and not any(p.exists() for p in outputs),'exclusive output/input collision')
    optional=ROOT/'build/function_index.json';require(not optional.exists(),'optional index appeared')
    progress.parent.mkdir(parents=True,exist_ok=True);published=[]
    with progress.open('x',encoding='utf-8') as log:
        def note(v):
            log.write(json.dumps(dict(elapsed_seconds=round(time.monotonic()-start,3),**v))+'\n');log.flush();os.fsync(log.fileno())
            require(log.tell()<=MAX_JOURNAL,'cache progress journal bound')
        note(dict(state='started',pid=os.getpid(),source_rows_sha256=PINS['rows']))
        try:
            with tempfile.TemporaryFile() as stage:
                with gzip.open(paths['rows'],'rb') as lines:
                    result=build_frames(lines,stage,rosters,selection['selections'],binding['summary'],start=start)
                require(result['rows']==490801,'complete binding row count differs')
                index=dict(schema_version=1,policy_id=POLICY,inputs=PINS,units=2988,selected_functions=68657,**result,**FALSE)
                index['data_file']=data.name;index_bytes=canonical(index)+b'\n';validate_index(index)
                require(stage.tell()+len(index_bytes)+MAX_JOURNAL<=MAX_OUTPUT,'cache data/index output bound')
                for p,h in observed.items():require(file_hash(p)==h,'cache input changed before publication')
                require(not optional.exists(),'optional index appeared');budget(start);stage.seek(0)
                data.parent.mkdir(parents=True,exist_ok=True)
                with data.open('xb') as target:
                    published.append(data)
                    while block:=stage.read(1048576):target.write(block)
                    target.flush();os.fsync(target.fileno())
                require(file_hash(data)==result['data_sha256'],'published frame data differs from staged bytes')
                idx.parent.mkdir(parents=True,exist_ok=True)
                with idx.open('xb') as target:published.append(idx);target.write(index_bytes);target.flush();os.fsync(target.fileno())
                generated={data:result['data_sha256'],idx:hashlib.sha256(index_bytes).hexdigest()}
                verify_hashes(generated,'published cache artifacts differ')
            receipt=dict(schema_version=1,policy_id=POLICY,status='metadata-cache-only',inputs=PINS,data_sha256=file_hash(data),
                index_sha256=file_hash(idx),data_bytes=data.stat().st_size,index_bytes=idx.stat().st_size,units=2988,selected_functions=68657,
                rows=490801,binding_census=result['binding_census'],row_sequence_sha256=result['row_sequence_sha256'],original_raw_sha256=result['original_raw_sha256'],
                producer_sha256=observed[Path(__file__).resolve()],dependency_tools_sha256={p.relative_to(ROOT).as_posix():h for p,h in observed.items() if p.is_relative_to(ROOT/'tools')},
                input_stability=True,optional_function_index_present=False,lossless_cache_complete=True,peak_memory_bytes=budget(start),**FALSE)
            payload=canonical(receipt)+b'\n';require(len(payload)+data.stat().st_size+idx.stat().st_size+MAX_JOURNAL<=MAX_OUTPUT,'total cache output bound')
            out.parent.mkdir(parents=True,exist_ok=True)
            with out.open('xb') as target:published.append(out);target.write(payload);target.flush();os.fsync(target.fileno())
            generated[out]=hashlib.sha256(payload).hexdigest()
            for p,h in observed.items():require(file_hash(p)==h,'cache input changed after publication')
            verify_hashes(generated,'cache artifacts changed after publication')
            require(not optional.exists(),'optional index appeared after publication');budget(start)
            note(dict(state='complete',receipt_sha256=file_hash(out),data_sha256=receipt['data_sha256'],index_sha256=receipt['index_sha256'],rows=490801))
            return receipt
        except BaseException as error:
            for p in published:p.unlink(missing_ok=True)
            note(dict(state='failed',error_type=type(error).__name__));raise


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    for name in tuple(PINS)+('out','data','index'):p.add_argument('--'+name.replace('_','-'),dest=name,type=Path,required=True)
    try:r=run(p.parse_args(argv))
    except (ValueError,OSError,KeyError,TypeError,zlib.error) as error:p.exit(2,'binding cache rejected: '+str(error)+'\n')
    print(json.dumps({k:r[k] for k in ('rows','units','selected_functions','data_bytes','index_bytes')}));return 0


if __name__=='__main__':raise SystemExit(main())
