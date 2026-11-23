# Frozen inputs of the no-reference build (`FNV_M3_NOREF2=1`, batches 10 and 12)

Everything here is **metadata** (addresses, identities, decisions, header constants). No `.text`, `.rdata` or `.data` byte of the
reference image is stored in the files used by the no-reference build. Each file was derived once from the reference in one
normal, verified run (reference present, round trip OK) and is read back when the reference is absent. The JSON files and this README are exported to
FNV-GAME by `tools/export_repo.py`; the `ref_*` files listed at the end are not.

## Code stage (batch 12, `FNV_CODE_NOREF=1`, implied by `FNV_M3_NOREF2=1`)

Regenerate all six with one normal run (reference present; about 5 minutes; takes `build.lock` yourself):

    set FNV_CODE_FREEZE=1
    runtime-next\build-v7\rebuild.cmd

`assemble_v7.py` (`freeze_dump`) and `verify_v7.py` write the files at the end of the final pass; `codefreeze.py` reads them back.
The run must be a normal one (`FNV_ICF=1`, `FNV_OVERLAY=1`, reference present); the rebuilt `.text` must equal the reference
(`filled_equals_reference` true). `build-all` refuses `FNV_CODE_FREEZE`.

| File | Size | What it holds |
|---|---:|---|
| `code_eh.json` | 1,306,453 B | EH funclet/tail pieces: per task (unit index; 100000 + unit for EH variants) every located piece as [object section index, start, end, VA, matcher ok, parent] (20,969 pieces in 437 tasks) plus the verified `.xdata` bases; `accepted` = the 15,725 pieces the verified run placed, in placement order; `heals` = 228 fields borrowed by the piece placed first and resolved by another copy (with the resolved target); `place_borrow` = 264 (field, unit) pairs not agreeing at placement time; `place_skipbad` = 13 fields whose first byte was already placed and whose status was not agree |
| `code_crt.json` | 34,843 B | CRT/STL placement: 594 code sections and 81 data sections as (library, member index, section index, VA); `ovl` = the 1,575 fields where the binding overlay applied |
| `code_contrib.json` | 105,566 B | 1,086 accepted local-target contributions: entry symbol, EH bindings (name -> address), 437 EH funclet pieces [section, start, end, VA], verified `.xdata` bases, overlay-applied fields |
| `code_overlay.json` | 31,679 B | per task, the fields where `reloc-v7/binding_overlay.json` applied in the verified run (437 tasks, 3,103 fields); the overlay itself stays the data table it was |
| `code_meta.json` | 8,643 B | import slots (256 names -> IAT VA), 61 import thunks (IAT slot -> thunk VA), `text_sha256` of the final `.text` and `image_sha256` (hashes, no bytes) |
| `code_icf_map.json` | 14,773 B | the ICF fold decisions of `icf_v7.py` (copy of `build-v7/icf_map.json` of the verified run) |

In no-reference mode the build re-derives every byte: it compiles the contributions, runs `assemble_v7.py` (functions from
`units.json`, EH pieces and CRT sections placed at the frozen addresses, relocation fields resolved by the same resolver as
before), and compares the SHA-256 of the result with `code_meta.json` (`text_equals_frozen_hash` in `progress.json`; a mismatch
is reported, not fatal, so that a control run still produces an exe).

## Data stage (batch 10)

| File | Size | What it holds | Script |
|---|---:|---|---|
| `placement_map.json` | 2,759,330 B | identity hash -> VA of every placed piece (33,650) | `FNV_M3_DV1_FREEZE=m3\frozen` in a normal build (`dv1_splice.py` / `place.py`) |
| `dv1_replay.json` | 5,465,383 B | the 16,104 accepted data-v1 pieces: identity, VA, tier, kind, sha256 of OUR compiled bytes, target VAs (11,783 EH funclet targets among them), RTTI proof template | same |
| `dv3_meta.json` | 1,380 B | section sizes, bss extent, chunk boundaries, TLS directory fields | `m3\b10_freeze_dv3.py` |
| `pe_meta.json` | 1,715 B | PE header constants (also used by the code stage) | `m3\b10_standin.py --freeze-meta <reference exe>` (reads the headers only) |

## Not used by the no-reference build (batch 9 stage 3, `FNV_M3_NOREF=1`)

`ref_headers.bin` (1,024 B), `ref_data.bin.z` (524,181 B), `ref_reloc.bin.z` (338,244 B), `ref_meta.json` (1,605 B): the
stand-in image of the older stage-3 mode (`m3\b9_freeze.py`). They hold reference section bytes; `FNV_M3_NOREF2` does not read them.
