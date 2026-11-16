# data-v1: .rdata/.data from our own objects (2026-11-15)
Linking work only; no source written. Reads (never writes) pinned-build/obj_v3, build-v7 (icf_map, relocs, strict/filled exe), the reference.
Run `rebuild.cmd` (about 3 min: phase0 16 s, place 70 s, report 1 min; needs python with numpy; pickles go to %TEMP%).
Outputs: FalloutNV_data_strict.exe, FalloutNV_data_filled.exe (SHA-256 df17889...97eb7 = reference, verified), progress.json, pieces.tsv.gz
(one row per placed piece: VA, size, tier, kind; no names), place.log, report.log. About 33 MB.

## What the images are
- strict = build-v7 strict (.text, sha d45f3fbb...) + our produced bytes in .rdata/.data; every other .rdata/.data byte is 0x00 (including the
  import directory/IAT: this is a measure image, not runnable). Other sections (.tls tail, CONST, .rsrc, .reloc, .bind) are still the reference.
- filled = strict with every unproduced byte (data and the .text holes, via build-v7's filled) taken from the reference: equals the reference.
  This also proves every byte we call produced equals the reference.
- A relocation field counts as produced only if our resolved value equals the reference; disagreeing or unresolved fields are left 0x00.

## Method
1. phase0.py (as build-v7 pass 1): per unit, every non-code section (.rdata*, .data*, .xdata$x EH tables, .CRT$XCU, .tls$, .bss), every relocation
   resolved with assemble_v3.resolve_field + ICF map + EH-piece locator (funclets); address hints from unit symbol maps / recipe names.
2. place.py: dedupe COMDATs (73,023 sections -> 59,905 unique pieces after splitting unit .rdata/.data at symbol boundaries), then tiers:
   B bytes with relocation fields masked: exactly one aligned hit in ref .rdata/.data  (9,740 pieces; 9,025 with 8+ unmasked bytes)
   V bytes + our own resolved values: exactly one hit                                (10,964)
   H no unique hit; map address, masked bytes verified there                         (5,874)
   L address read from the reference pointer in an already placed piece, bytes verified (5,398; mostly RTTI 1-4)
   Total 31,976 pieces placed. B vs map hint: 9,043 equal, 53 differ (possible mis-placement, kept).
3. report.py: resolves fields again with final placements (local data targets via placed pieces, externs via placed definitions), compares with ref.

## Bytes produced (.rdata 580,044 of 1,716,736 raw = 33.8%; .data 15,296 of 262,656 = 5.8%; .tls 638; total 30.1% of rdata+data)
eh-tables 258,643 | strings 198,376 | rtti4 32,619 | rtti1 29,775 | rdata unit-level 26,127 | rtti0 14,430 | vtables 13,432 (placed vtable
bytes 100,288 but only agreeing fields count) | rtti3 12,624 | rtti2 4,280 | float consts 4,205 | other 1,000.

## Data->code pointers (101,449: .rdata 98,619, .data 2,830)
| outcome | fields |
|---|---|
| we produce, equals reference | 12,945 (12.8%) |
| we resolve, differs from reference | 1,582 |
| in a placed piece, target unresolved (borrowed) | 11,765 |
| bytes produced but our object has no reloc record there | 30 |
| no placed piece at all | 75,127 |
Agree by source: EH piece locator 11,828 (funclet/handler addresses; locator anchors on the reference's handler-stub values, so weakest
independence), recipe functions 767, symbol maps 340, name-embedded 10. By tier: B 2,642, V 9,760 (V partly by construction), H 543.
Ceiling: our objects hold only 36,061 code-pointing data relocs (EH 15,238, vtables 14,527, CRT init array 6,266, other 30): 35.5% of 101,449.
Disagreements (1,582): c-map target differs 1,015; name-embedded address differs 498; recipe function differs 60; others 9.
Seen: derived class slot resolves to the base method (override/slot layout differs in our source), 'near' delta 16 bytes. No ICF-like identical copies.

## Not produced, by cause
- No object (65,388 pointers; vtables/EH of classes or code with no unit): the main gap. Needs the original linker's data or more source.
- Unresolved externs in placed vtables: 14,905 fields, 6,013 names, never defined in any object (5 are): __purecall 1,196, TESForm base virtuals
  (Unk_xx/vfn_xx and named), scalar-deleting dtors `??_E...`. 9,739 would be inferable from the reference's own values (circular; not counted).
- RTTI type descriptors: 6,471 pieces (207 KB) match nowhere because our class names (FUN_xxxx, Base5a) are not the original names; R1-R4 depend on them.
- CRT$XCU initializer arrays: 16 pieces, 42 KB, 6,266 pointers, all resolved but no unique place (merged across units by the linker).
- EH tables left: 1,509 ambiguous, 41 no match. Strings left: 179 no match (11 KB). TLS: 54 pieces (.tls$ is not the PE .tls layout).
- BSS: 349 unique pieces, 68,273 bytes; 177 have a map address in the .data virtual tail (714,908 bytes there). No file bytes; layout only.
- Unproduced in .rdata: 1,136,692 bytes = 397,434 zero + 1,548 import/IAT + 737,710 other; in .data: 247,360 = 77,661 zero + 169,699 other.
- Pointer-sized fields with no relocation in the original .reloc (7,156 per layout-v1) are not addressed here.

## Caveats
- Placement by H/L and all map hints depend on reference-derived addresses (Ghidra names in units.json); B and V placements do not.
- Per-piece alignment padding between COMDATs and gaps between pieces are not produced (zero bytes counted as unproduced).
- Jump tables are in .text in this toolchain (build-v7 text), so none appear in the data sections.
- Strict/filled are not runnable; the .reloc table is untouched.
