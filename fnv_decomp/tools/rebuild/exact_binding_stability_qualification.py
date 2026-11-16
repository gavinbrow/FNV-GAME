"""Pure saved-ledger qualification; never resolves or opens ledger paths."""
from __future__ import annotations
import hashlib
import json
import statistics
import time
import exact_binding_stability as selection

MAX_RAW_BYTES=96*1024*1024
MAX_REPEATS=3


def require(ok,message):
    if not ok:raise ValueError(message)


def _pairs(items):
    result={}
    for key,value in items:
        require(key not in result,'duplicate JSON key')
        result[key]=value
    return result


def _invalid_constant(value):
    raise ValueError('nonfinite JSON constant')


def _ledger_digest(ledger):
    digest=hashlib.sha256()
    for chunk in json.JSONEncoder(ensure_ascii=True,separators=(',',':'),allow_nan=False).iterencode(ledger):
        digest.update(chunk.encode('ascii'))
    return digest.hexdigest()


def evaluate(raw,*,expected_sha256,expected_counts):
    """Input SHA/counts come from separately accepted exact saved-input review.

    This proves selection equivalence and ledger preservation only. Timing is
    selection CPU/wall overhead, never the saved checker or historical file I/O.
    """
    require(type(raw) is bytes and len(raw)<=MAX_RAW_BYTES,'bounded raw derived receipt required')
    require(type(expected_sha256) is str and hashlib.sha256(raw).hexdigest()==expected_sha256,'saved receipt hash mismatch')
    require(type(expected_counts) is tuple and len(expected_counts)==3 and
            all(type(x) is int and x>=0 for x in expected_counts),'typed exact expected counts required')
    receipt=json.loads(raw,object_pairs_hook=_pairs,parse_constant=_invalid_constant)
    require(type(receipt) is dict and type(receipt.get('input_bindings')) is list,'complete saved input_bindings required')
    ledger=receipt['input_bindings']
    require(len(ledger)<=selection.MAX_ROWS,'bounded complete identity ledger required')
    before=_ledger_digest(ledger)
    # Independent full-dictionary baseline, without path or field projection.
    baseline=[];indices=[];seen=set()
    for index,row in enumerate(ledger):
        require(type(row) is dict,'dictionary identity required')
        key=json.dumps(row,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)
        if key not in seen:seen.add(key);baseline.append(row);indices.append(index)
    timings=[];facts=None
    for _ in range(MAX_REPEATS):
        started=time.perf_counter()
        unique,current=selection.select_exact_bindings(ledger)
        timings.append(time.perf_counter()-started)
        require(unique==baseline and current['first_occurrence_indices']==indices,'independent full-dictionary selection mismatch')
        require(facts is None or current==facts,'phase-local repeated selection mismatch')
        facts=current
    require(_ledger_digest(ledger)==before,'complete ledger changed during qualification')
    actual=(facts['input_rows'],facts['unique_rows'],facts['exact_duplicate_rows'])
    require(actual==expected_counts,'accepted saved counts mismatch')
    return dict(kind='exact-binding-selection-saved-only-qualification-v1',
        saved_receipt_sha256=expected_sha256,saved_receipt_bytes=len(raw),
        ledger_verbatim_json_sha256=before,selection=facts,
        independent_exact_dictionary_selection_equal=True,complete_ledger_preserved=True,
        selection_seconds=timings,selection_seconds_median=statistics.median(timings),
        omitted_duplicate_checks_per_phase=actual[2],
        actual_stability_delegate_called=False,historical_paths_opened=False,
        fresh_historical_identity_verified=False,storage_io_speedup_measured=False,
        native_called=False,production_adoption=False)
