# layout-v1: stage 4 free-layout static prototype (2026-11-15)
No source written, no image written, nothing launched. Inputs read-only: build-v6 (relocs_v6, strict image, contrib_pieces),
fnv_decomp/build/units.json, the reference exe. Scripts: stage1 (blocks) -> setup.py + stage2 (layouts, verify), stage3*, sweep.py
(capstone), pelevel.py, dataruns.py. Results: summary.json, layouts_result.json, sweep_result.json. Needs python with numpy and capstone.

## Model
- Movable blocks tile all of .text (73,741): 68,657 recipe functions, 1,862 recipe EH tails, 629 contributions, 1,983 "other"
  (CRT, EH outside recipe; boundaries inferred from strict-image runs, so approximate), 610 blobs (78,857 bytes, undecompiled or
  unknown, moved as rigid byte ranges). Trailing padding stays with its block; blocks keep their address mod 16.
- All code goes to a new region at VA 0x02000000 (old .text unused); .rdata/.data/imports/TLS untouched.
- Layouts: G (original order, +16 gap), U (units gathered, +256 between), R (U with each unit reversed), Z (random permutation of all blocks).
- Patched per layout: every REL32/DIR32 record (new value from the layout map L), the 3,152 original-.reloc DIR32 fields in .text that our
  records lack (value from the reference), and all 101,449 data->code fields from the original .reloc. The 1,141 DIR32 records absent from the
  original .reloc (constants such as 0xFFFFFF) are not remapped; 14 of them hold a value in .text range.

## Static proof (all four layouts)
- 520,287 record fields rewritten, read back from the moved text, mapped to the old address through the inverse layout map and compared with
  the target decoded from the reference bytes: 520,287 match, 0 mismatch. The 515,409 "agree" rows also equal our own recorded target.
- 101,449 of 101,449 data->code pointers map back correctly. No block overlaps.
- Caveat: this proves the map is consistent and the records point where the reference points. It is not independent of the reference
  (reloc-v5 NOTES: circularity) and nothing runs.
- Independent sweep (capstone, 4.12 M instructions): 322,953 rel32 branches leave their block; 320,720 are in our records (equals the record
  count). 2,233 are not: 2,229 inside blobs (undecompiled code), 4 in "other".

## Code->code references (cross-block, estimated universe 338,256)
| source | count | cumulative |
|---|---|---|
| our records, agree | 331,987 | 98.15% |
| + borrowed fields mapped via reference value (3,805 to code of 4,757) | 3,805 | 99.27% |
| + 62 disagree (wrong-copy callee; map reproduces the REFERENCE target, our own target would break) | 62 | 99.29% |
| + original-.reloc DIR32 not in records (165 to code) | 165 | 99.76% |
| rel32 in blobs, only by disassembly | 2,237 | remainder |
Borrowed fields are mappable (field position known, target from the reference) but not "ours".

## Data->code (101,449 fields: .rdata 98,619, .data 2,830)
These sections are copied from the reference, so none comes from our records (0%); the original .reloc covers 100% mechanically.
88,100 fields are in runs of 2 or more (vtables, function tables); 13,349 are singles (SEH handlers, unwind actions, callbacks).
91,500 hit a block start; 9,949 land mid-block (EH funclets, shared tails); 1,166 land in blobs. Risk: 7,156 aligned dwords in
.rdata/.data hold a .text-range value but are not in .reloc (297 equal a block start): stale or hidden code pointers to check.
The base-reloc table itself must be rewritten for moved fields. Jump tables inside .text: 861 runs (38,400 bytes) of DIR32 entries, all in
the original .reloc and in our records; 1,006 indirect jmps use a table operand.

## PE level
Entry 0x14092ee is in .bind (Steam wrapper). 373 dwords there hold text-range values (likely the real entry and checks) and .bind has no
base relocs, so a moved image needs wrapper-held values changed, which we must not do. TLS callbacks: none. Exports, load config (SafeSEH),
exception directory: none. No call/pop (call $+5) found.

## Blockers, priority order
1. Steam wrapper holds the real entry and probably integrity checks over .text; a moved image cannot start through it (stage 5).
2. Undecompiled blobs (78,857 bytes): rigid copies; 2,237 rel32 and about 3,000 DIR32 inside need disassembly or the .reloc.
3. Data->code: 101,449 pointers rely on the original .reloc, not our build; vtables, RTTI, SEH are not source-built. 297+ unrelocated candidates.
4. Borrowed 4,757 fields and 121 disagree (48 wrong callee): mappable only from reference values; fix sources to be self-contained.
5. 23 rel8 branches cross block boundaries (shared tails or my boundary inference); 192 blocks end without a terminator (60 flush, much of it
   decode noise): possible fall-through adjacency.
6. "Other" blocks (CRT, EH outside recipe) need true piece boundaries from assemble_v6 (not dumped).
7. Constants read as addresses (1,141 DIR32 not in .reloc): never remap without the oracle.
8. Position-dependent code beyond the above is undetected: runtime patching, hashing of .text, hardcoded address ranges.

## Non-launch tests
Write the moved text and compare it instruction by instruction with the reference (mask fields, map targets); check that every branch
target lands on an instruction start; walk the rewritten .reloc and the data->code map; emulate pure functions (Unicorn) in old and new
layout and compare. A real launch test needs a wrapper-free path.
