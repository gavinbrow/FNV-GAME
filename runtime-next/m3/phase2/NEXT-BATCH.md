# Next data/type batch proposal

This batch is now the accepted promoted default. The proposal details below describe its earlier staged state; the acceptance record supersedes pending-status statements. `next_batch_manifest.json` records exact input hashes, scope and fixture status; `audit_next_batch.py` independently reproduces the range reconciliation. The preceding 12-array + 370-library batch is now accepted at `out/phase2-promoted-default-verified`. Its standalone CLI smoke was preliminary evidence; full positive/controls/repeat/default gates subsequently passed.

The proposed M3 selection has 8,268 entries versus 8,265 in the current 12-array selection. It has exactly the same disjoint address union and no overlap with the current smoke's DV1 pieces. Four additional source-view heads replace 364 bytes of W scaffolding: a 12-byte NiPoint3, two 16-byte aligned `__m128` objects, and a 320-byte Cost245[16]. Their separately retained W tails total 320 bytes and preserve the original relocation sites (2, 1 and 1 respectively). Existing array-split tails are separate from that total. This is type-quality progress, not increased byte coverage.

The NiPoint3 head/tail fixture passed. The Cost245 source-view fixture passed the native symbol, 320+64 bytes and 59 original relocations; its 58 head relocations occur in source-declared integer fields. Those integer fields are transports for address-valued data in the fixture, not proven native pointer types. The hardened staged Cost245 helper rejects any relocation or symbolic field in the bool/padding or unaligned interior of an integer field. Its actual candidate-generator fixture now passes 2 entries / 384 bytes / 59 relocations without changing the accepted helper; see `out/phase2-cost245-proposal/isolated-fixture/result.json`. Shared integration and full-image gates remain.

The two SIMD heads require actual 16-byte alignment; the staged object reader checks section flags and symbol offset, the pseudo-unit records 16-byte alignment, and the staged image builder checks the translated final VA. The VC2008 fixture now exercises the actual candidate generator and passes native COFF symbols/bytes, section/symbol alignment, retained tail relocation and pseudo-unit 16-byte flags; see `out/phase2-align16/isolated-fixture/result.json`. Integrated placement and translated final-image checks remain outstanding. No class identity beyond these source views or unresolved aliases is claimed.

The proposed 405 library pieces / 16,730 bytes include **370 pieces / 6,374 bytes already present** in the 539,686-byte DV1 smoke: their VA, size, unit and compiled section digest match exactly. The other 35 pieces / **10,356 bytes are incremental and disjoint** from every smoke DV1 range: 4,014 zero and 6,342 nonzero reference bytes. The 6,160-byte whole atan section in the increment has overlapping *unselected* library annotations; the selected whole-section identity is supported by the current compiler archive and placement metadata, but alternative provenance is not resolved. The current smoke includes five `.tls` bytes and 539,681 `.data`/`.rdata` bytes; it is not itself the final combined build.

The proposed library hook separately validates whole sections and `st.PIECES` split intervals against fresh placement, archive/member/section hashes, field/relocation boundaries, alignment, current claims and recorded rewrites. Thirteen staged tests and a read-only temporary-placement dry run passed. Fresh archived placement, generated objects, targeted controls, unchanged baseline/relocation bytes and semantic gameplay still need verification.

Isolated commands, only in an authorized free compiler lane:

```powershell
python -I runtime-next/m3/phase2/compile_simd_fixture.py
python -I runtime-next/m3/phase2/compile_cost245_staged.py
```

The Cost245 fixture loads the staged hardened helper privately and records its hash; it does not require installing that helper into the accepted build. Both fixtures reject inherited negative-control mode before compilation. The sole verifier compiled them successfully on 2026-11-19. Their commands above are historical reproduction instructions: preserve the existing output directories and prepare new isolated paths for any new run. The 16-byte splice, placement and image-builder changes must be reviewed and integrated as a unit. Do not silently overwrite measured inputs or treat fixture success as a full-image or native-class completion claim.

## Accepted default (2026-11-19)

The fresh no-overrides promoted default passed the full gate; `../out/phase2-next-data-default-verified/evidence/root-default-review.json` records the canonical image, exact relocation directory, controls, repeat, gameplay, frozen inputs and source checks. The accepted raw `.data`/`.rdata` coverage is 1,613,010 of 1,979,392 bytes; five TLS bytes are separate. The 405 library pieces include 35 pieces / 10,356 bytes incremental to the preceding default. The four source-view heads replace 364 W bytes within the existing M3 address union, so they do not add coverage. Source-declared Cost245 integer fields remain transports, not proven pointer types.

The earlier pending descriptions below are historical proposal and fixture records. The disjoint current partition is generated from the accepted archived ranges in `accepted_range_partition.json`; `accepted_range_partition.before-next-data.json` preserves the prior record. This acceptance does not establish complete native class recovery.
