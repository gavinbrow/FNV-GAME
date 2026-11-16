"""One-shot saved-11 validation CLI; execution requires reviewed host supervision.

A separately reviewed host must bind this script, exact operation/review inputs,
a fresh lease, a process-tree Job limit and the once-only command. No prior V3
operation is resumed. This script never writes an object or an archive.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import os
import stat
from pathlib import Path, PurePosixPath
import time

ROOT=Path(__file__).resolve().parents[2]
OP_REL='build/rebuild/v14-v3-saved11-validation-operation-v1.json'
OP_SHA='b9fcbbdee3f3ce18231665a2ad0ebb2941cd232d07b3a7913607cbd87f660488'
OUT_REL='build/rebuild/v14-v3-saved11-validation-v1'
EVIDENCE_REL='build/rebuild/v14-v3-salvage-feasibility-v1/saved-hash-check.json'
EVIDENCE_SHA='3d4aca1dd3a6fce9de13006aa7d0e159c31cae35037980dff58c946263038f3f'
FEASIBILITY_REL='build/rebuild/v14-v3-salvage-feasibility-v1/independent-feasibility-review-v1.json'
FEASIBILITY_SHA='3d8d800ca9c72b8480e0025924c13362e9a854431f28d6456bc259740cd7fbe9'
FAILURE_REL='build/rebuild/v14-v3-failed-outcome-independent-v1/review.json'
FAILURE_SHA='a27d9a801a2027b8a47542381f71ae94e6008c364e2593c26ba7f2264ad00fc7'
PROGRESS_REL='build/rebuild/cached-frontier-code-v14-v3/progress.jsonl'
PROGRESS_SHA='ec0c9dad56efca7f50395419d63846cc9cd7ebecceef7507a5cd9db7ad972408'
DRIVER_REL='tools/rebuild/cached_frontier_code_factory_v14_driver.py'
DRIVER_SHA='918747fc4fb5bc4defbf9cd0a424aead024c2ba98cdcb4eb0843fa2dcc9a19a9'
SOURCE_ROLES=('tools/rebuild/v14_saved11_validation.py','tools/rebuild/v14_saved11_validation_runner.py',
              'tests/rebuild/test_v14_saved11_validation.py','tests/rebuild/test_v14_saved11_validation_runner.py')
FALSE=dict(new_object_emission=False,prior_batch_replay=False,prior_match_inferred=False,
           provider_selected=False,runtime_eligible=False,canonical_index_checked=False,function_index_present=False)


def _sha(value):
    return type(value) is str and len(value)==64 and all(c in '0123456789abcdef' for c in value)


def _private_path(relative):
    if type(relative) is not str or '\\' in relative:
        raise ValueError('canonical private relative path required')
    part=PurePosixPath(relative)
    if part.is_absolute() or part.as_posix()!=relative or any(x in ('','.','..') for x in part.parts):
        raise ValueError('canonical private relative path required')
    path=_regular_no_reparse(ROOT/relative,1024*1024)
    if not path.is_relative_to(ROOT/'build/rebuild'):
        raise ValueError('private input required')
    return path


def _regular_no_reparse(path,max_bytes):
    """Check the final input entry without following a reparse point."""
    path=Path(path)
    info=path.lstat()
    if (not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode) or
            getattr(info,'st_file_attributes',0)&0x400 or type(info.st_size) is not int or
            not 0<info.st_size<=max_bytes):
        raise ValueError('bounded regular non-reparse input required')
    return path.resolve(strict=True)


def _require_absent(path):
    """Reject any final entry, including a dangling symlink or junction."""
    try:
        Path(path).lstat()
    except FileNotFoundError:
        return
    raise FileExistsError('validation output already exists')


def validate_review(review,peer,operation_sha,reference_path):
    keys={'schema_version','kind','reviewer','approved','root_authorized','source_review_pass','input_review_pass',
          'resource_lease_required','operation_sha256','source_sha256','peer_review_path','peer_review_sha256',
          'reference_path','allow_reference_and_original_reads','allow_saved_object_reads','allow_native_tools',
          'allow_object_emission','allow_game_execution'}
    if (type(review) is not dict or set(review)!=keys or type(review['schema_version']) is not int or
            review['schema_version']!=1 or review['kind']!='v14-saved11-source-input-review-v1' or
            any(review[k] is not True for k in ('approved','root_authorized','source_review_pass','input_review_pass',
                'resource_lease_required','allow_reference_and_original_reads','allow_saved_object_reads')) or
            any(review[k] is not False for k in ('allow_native_tools','allow_object_emission','allow_game_execution')) or
            review['operation_sha256']!=operation_sha or review['reference_path']!=str(reference_path) or
            type(review['reviewer']) is not str or not review['reviewer'] or
            review['reviewer'] in ('/root/terra_factory_driver_v14','/root/terra_code_pipeline_v14') or
            type(review['source_sha256']) is not dict or set(review['source_sha256'])!=set(SOURCE_ROLES) or
            not all(_sha(v) for v in review['source_sha256'].values()) or not _sha(review['peer_review_sha256'])):
        raise ValueError('exact independent saved11 source/input review required')
    peerkeys={'schema_version','kind','reviewer','approved','operation_sha256','source_sha256','provider_selected','runtime_eligible'}
    if (type(peer) is not dict or set(peer)!=peerkeys or type(peer['schema_version']) is not int or peer['schema_version']!=1 or
            peer['kind']!='v14-saved11-complement-review-v1' or peer['approved'] is not True or
            peer['operation_sha256']!=operation_sha or peer['source_sha256']!=review['source_sha256'] or
            type(peer['reviewer']) is not str or not peer['reviewer'] or
            peer['reviewer'] in (review['reviewer'],'/root/terra_factory_driver_v14','/root/terra_code_pipeline_v14') or
            peer['provider_selected'] is not False or peer['runtime_eligible'] is not False):
        raise ValueError('distinct independent complementary review required')
    return True


def merge_field_facts(existing,incoming):
    """Reject conflicting original operands shared by two roots."""
    import cached_frontier_code_factory_v14_driver as d
    for site,fact in incoming.items():
        if site in existing and not d._typed_equal(existing[site],fact):
            raise ValueError('contradictory original field facts')
        existing[site]=fact


class ReceiptRetractionFailed(RuntimeError):
    """Canonical receipt could not safely be removed; quarantine required."""


def publish_receipt(out,receipt,inputs,start,*,small_metadata):
    """Attempt identity-safe retraction on failure; terminal remains mandatory."""
    import cached_frontier_code_factory_v13 as v13
    import cached_frontier_code_factory_v14_driver as d
    import v14_factory_output_publication as publisher
    pending=out/'receipt.pending.json';canonical=out/'receipt.json'
    if pending.exists() or pending.is_symlink() or canonical.exists() or canonical.is_symlink():
        raise FileExistsError('receipt exists; never retry')
    artifacts=receipt['output_sha256'];d._require_absent_index(ROOT/'build/function_index.json');d.stable_with_small_metadata(inputs,small_metadata);d._require_absent_index(ROOT/'build/function_index.json');v13.base.budget(start,out)
    publisher._verify(out,artifacts,128*1024*1024)
    body=(json.dumps(receipt,sort_keys=True,separators=(',',':'))+'\n').encode();created=None;linked=False
    try:
        with pending.open('xb') as stream:
            stream.write(body);stream.flush();os.fsync(stream.fileno())
        st=pending.stat(follow_symlinks=False);created=(st.st_dev,st.st_ino)
        d._require_absent_index(ROOT/'build/function_index.json');d.stable_with_small_metadata(inputs,small_metadata);d._require_absent_index(ROOT/'build/function_index.json');publisher._verify(out,dict(artifacts,**{'receipt.pending.json':hashlib.sha256(body).hexdigest()}),128*1024*1024)
        os.link(pending,canonical);linked=True
        d._require_absent_index(ROOT/'build/function_index.json');d.stable_with_small_metadata(inputs,small_metadata);d._require_absent_index(ROOT/'build/function_index.json');v13.base.budget(start,out)
        pins=dict(artifacts,**{'receipt.pending.json':hashlib.sha256(body).hexdigest(),'receipt.json':hashlib.sha256(body).hexdigest()})
        publisher._verify(out,pins,128*1024*1024)
        a=pending.stat(follow_symlinks=False);b=canonical.stat(follow_symlinks=False)
        if (a.st_dev,a.st_ino)!=(b.st_dev,b.st_ino) or (b.st_dev,b.st_ino)!=created:
            raise ValueError('receipt link identity differs')
    except BaseException as error:
        if linked and created is not None:
            try:
                st=canonical.stat(follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                if canonical.is_symlink() or (st.st_dev,st.st_ino)!=created:
                    raise ReceiptRetractionFailed('canonical identity changed; reconcile') from error
                try:
                    canonical.unlink()
                except OSError as failure:
                    raise ReceiptRetractionFailed('canonical retraction failed; reconcile') from failure
        raise
    return receipt


def run(args):
    import v14_saved11_validation as core
    import cached_frontier_code_factory_v14_driver as d
    import cached_frontier_code_factory_v13 as v13
    import cached_root_observe_v14 as native
    start=time.monotonic();inputs={};out=None;journal=None;report_file=None;writer=None;snapshot=None
    operation_input=Path(args.operation);review_input=Path(args.review)
    if (not operation_input.is_absolute() or operation_input!=ROOT/OP_REL or not review_input.is_absolute() or
            not _sha(args.review_sha256)):
        raise ValueError('exact operation and private reviewed input required')
    operation_path=_regular_no_reparse(operation_input,1024*1024)
    review_path=_regular_no_reparse(review_input,1024*1024)
    if operation_path!=(ROOT/OP_REL).resolve() or not review_path.is_relative_to(ROOT/'build/rebuild'):
        raise ValueError('exact operation and private reviewed input required')
    op=d.read_small_bound_json(operation_path,OP_SHA);review=d.read_small_bound_json(review_path,args.review_sha256)
    inputs[operation_path]=OP_SHA;inputs[review_path]=args.review_sha256
    peer_path=_private_path(review['peer_review_path']);peer=d.read_small_bound_json(peer_path,review['peer_review_sha256'])
    if not Path(args.reference).is_absolute():raise ValueError('absolute reviewed reference required')
    validate_review(review,peer,OP_SHA,Path(args.reference))
    if peer_path in inputs:raise ValueError('peer review duplicates operation/review input')
    inputs[peer_path]=review['peer_review_sha256'];small_metadata=(operation_path,review_path,peer_path)
    requested_out=Path(args.out)
    if not requested_out.is_absolute() or requested_out!=ROOT/OUT_REL:
        raise ValueError('exclusive exact private validation output required')
    _require_absent(requested_out)
    out=requested_out.resolve()
    if out!=(ROOT/OUT_REL).resolve():
        raise ValueError('exclusive exact private validation output required')
    reference_path=_regular_no_reparse(args.reference,128*1024*1024)
    if str(reference_path)!=review['reference_path']:
        raise ValueError('reference path identity differs')
    for rel,h in review['source_sha256'].items():v13.base.observe(ROOT/rel,h,inputs)
    v13.base.observe(ROOT/DRIVER_REL,DRIVER_SHA,inputs);d.pin_producer_dependencies(ROOT,inputs)
    evidence=native.read_bound_json(ROOT/EVIDENCE_REL,EVIDENCE_SHA)
    feasibility=native.read_bound_json(ROOT/FEASIBILITY_REL,FEASIBILITY_SHA)
    failure=native.read_bound_json(ROOT/FAILURE_REL,FAILURE_SHA)
    for rel,h in ((EVIDENCE_REL,EVIDENCE_SHA),(FEASIBILITY_REL,FEASIBILITY_SHA),(FAILURE_REL,FAILURE_SHA),(PROGRESS_REL,PROGRESS_SHA)):
        v13.base.observe(ROOT/rel,h,inputs)
    if (feasibility['status']!='unadmitted-candidate-only-fresh-validation-possible' or
            feasibility['hash_check_result_sha256']!=EVIDENCE_SHA or feasibility['admissible_now'] is not False or
            failure['status']!='failed-quarantined-no-replay' or failure['replay_authorized'] is not False):
        raise ValueError('prior failure/salvage evidence differs')
    saved=d.load_accepted_metadata(ROOT);qualification=d.load_qualification_metadata(ROOT,saved)
    for name in ('receipt','main_review','complement_review','positive_request','details'):
        rel,h=d.ACCEPTED[name];v13.base.observe(ROOT/rel,h,inputs)
    for role in ('qualified_receipt','qualified_inventory','qualified_request','qualified_registry','prepared_epoch',
                 'prepared_review','current_groups','current_review'):
        ref=native.ARTIFACT_PINS[role];v13.base.observe(ROOT/ref['path'],ref['sha256'],inputs)
    provider_state=d.load_provider_inputs(ROOT,saved,qualification)
    inputs.update({Path(p):h for p,h in provider_state['input_sha256'].items()})
    core.validate_scope(op,evidence,saved['positive_request'])
    request,selected,ledger,contexts=d.select_accepted_candidates(ROOT/d.ACCEPTED['details'][0],saved,
        qualification['qualified_request'],qualification['current_groups'],qualification['prepared_epoch'])
    selected_by_address={s['root']['original_address']:s for s in selected}
    expected={r['root']['original_address'] for r in op['members']}
    if len(expected)!=11 or not expected.issubset(selected_by_address) or any(a in core.FORBIDDEN for a in expected):
        raise ValueError('exact saved11 selection differs')
    for rel,h in provider_state['values']['retained']['inputs']['tools_sha256'].items():
        path=(ROOT/rel).resolve();
        if not path.is_relative_to(ROOT/'tools'):raise ValueError('foreign retained verifier')
        v13.base.observe(path,h,inputs)
    native_root=(ROOT/native.ARTIFACT_PINS['manifest']['path']).parent/provider_state['values']['manifest'].get('object_root_relative','.')
    native_root=native_root.resolve(strict=True);saved_root=(ROOT/'build/rebuild/cached-frontier-code-v14-v3').resolve(strict=True)
    if not native_root.is_relative_to(ROOT/'build/rebuild') or not saved_root.is_relative_to(ROOT/'build/rebuild'):
        raise ValueError('private object roots required')
    if any(p.is_relative_to(out) for p in inputs):raise ValueError('output overlaps protected metadata')
    d._require_absent_index(ROOT/'build/function_index.json');d.stable_with_small_metadata(inputs,small_metadata);out.mkdir(parents=True,exist_ok=False)
    try:
        journal=(out/'progress.jsonl').open('x',encoding='utf-8')
        def note(state,**facts):
            journal.write(json.dumps(dict(state=state,**facts),sort_keys=True)+'\n');journal.flush();os.fsync(journal.fileno());v13.base.budget(start,out)
        note('started',requested=11)
        reference=v13.base.observe(reference_path,v13.base.pool.PINS['reference'],inputs)
        pe=v13.checked_reference(reference);snapshot=v13.audit.SnapshotPe(reference,pe)
        highlow={snapshot.base+rva for rva in snapshot.relocations()}
        if len(highlow)!=351931:raise ValueError('fresh reference HIGHLOW census differs')
        exports=set(qualification['prepared_epoch']['exclusion_names']);facts={};validated=[]
        report_file=(out/'reports.jsonl.gz').open('xb')
        writer=gzip.GzipFile(fileobj=v13.metadata.BoundedSink(report_file,start,out),mode='wb',mtime=0)
        for row in op['members']:
            d._require_absent_index(ROOT/'build/function_index.json')
            root=row['root'];address=root['original_address'];selection=selected_by_address[address];record=contexts[address]
            unit=provider_state['units'][root['recipe_id']];proof=provider_state['proofs'][root['recipe_id']]
            source=_regular_no_reparse(ROOT/unit['source'],16*1024*1024)
            original=_regular_no_reparse(native_root/unit['object'],16*1024*1024)
            saved_path=_regular_no_reparse(saved_root/row['saved_member']['name'],16*1024*1024)
            if (not source.is_relative_to(ROOT) or not original.is_relative_to(native_root) or
                    not saved_path.is_relative_to(saved_root) or any(p.is_relative_to(out) for p in (source,original,saved_path))):
                raise ValueError('source/object path escaped exact protected roots')
            v13.base.observe(source,root['source_sha256'],inputs);v13.base.observe(original,root['object_sha256'],inputs)
            v13.base.observe(saved_path,row['saved_member']['sha256'],inputs)
            with original.open('rb') as f:raw=f.read(16*1024*1024+1)
            with saved_path.open('rb') as f:existing=f.read(16*1024*1024+1)
            report=core.verify_saved_member(row,record,selection,raw,existing,provider_state['providers'],exports,
                original,saved_path,pe,unit,proof,snapshot,highlow)
            merge_field_facts(facts,report['field_facts'])
            writer.write(native.canonical(report)+b'\n');validated.append(address);note('member_validated',original_address=address,saved_sha256=row['saved_member']['sha256'])
        if len(validated)!=11 or set(validated)!=expected:raise ValueError('complete unique saved11 validation required')
        writer.close();writer=None;report_file.flush();os.fsync(report_file.fileno());report_file.close();report_file=None
        snapshot.close();snapshot=None;d._require_absent_index(ROOT/'build/function_index.json');d.stable_with_small_metadata(inputs,small_metadata)
        note('terminal',validated=11);journal.close()
        artifacts={name:v13.base.file_hash(out/name) for name in ('progress.jsonl','reports.jsonl.gz')}
        receipt=dict(schema_version=1,kind='v14-saved11-validation-receipt',status='validated-unreviewed',
            operation_sha256=OP_SHA,review_sha256=args.review_sha256,validated=11,validated_addresses=validated,
            full_field_proof_records=11,unique_field_sites=len(facts),field_facts_sha256=v13.digest(sorted(facts.items())),
            input_stability=True,standalone_receipt_admission=False,observation_metadata_records_authenticated=89,
            positive_metadata_selection_count=15,protected_member_scope_count=11,
            excluded_member_payloads_accessed=False,output_sha256=artifacts,**FALSE)
        return publish_receipt(out,receipt,inputs,start,small_metadata=small_metadata)
    except BaseException as error:
        if journal is not None and not journal.closed:
            journal.write(json.dumps(dict(state='failed',error_type=type(error).__name__))+'\n');journal.flush();os.fsync(journal.fileno());journal.close()
        if out is not None and out.exists():
            with (out/'abort.json').open('x',encoding='utf-8') as stream:
                json.dump(dict(status='aborted-no-retry',error_type=type(error).__name__,**FALSE),stream);stream.flush();os.fsync(stream.fileno())
        raise
    finally:
        if writer is not None:writer.close()
        if report_file is not None:report_file.close()
        if snapshot is not None:snapshot.close()
        if journal is not None and not journal.closed:journal.close()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('operation','review','reference','out'):parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--review-sha256',required=True)
    try:result=run(parser.parse_args(argv))
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'saved11 validation rejected: '+str(error)+'\n')
    print(json.dumps(dict(status=result['status'],validated=result['validated'])))
    return 0


if __name__=='__main__':raise SystemExit(main())
