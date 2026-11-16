# data-v3: symbolic data (worker B, 2026-11-16)

Goal: a complete symbolic description of .rdata, .data (+ its bss tail), .tls and CONST that a linker can relocate. Result: round trip proven (see below), 150,462 pointer fields symbolic.
Run `rebuild.cmd` (gen.py -> out\*.asm, ml.exe -> out\*.obj, verify.py, postproc.py). `symbolic.json` is the consumer file for layout tools.

## What is reference-derived (read this first)
- Every byte not produced by our objects is a typed literal captured from the reference image (strings as `db '...'`, zero runs as `db N dup(0)`, other bytes as hex `db`). No floats are typed: no reliable signal; they stay hex bytes.
- Pointer-field LOCATIONS: the original .reloc (150,165 sites in .rdata/.data, evidence `orig-reloc`), plus 297 sites found by a value rule (below). Both are reference-derived.
- Pointer TARGETS are read from the reference field values, then named: code target -> OUR function name (recipe `units.json` symbol, unique name, `+addend` if inside a function); code that is not a recipe function
  (EH funclets, CRT, thunks) -> `C_<va>`; data target -> label `D_<va>` defined by these objects (5,670 of them have an alias to our object symbol, `our_symbol` in out\data_labels.json).
- Produced-by-us origin is marked per field (`ours`: 28,278 fields lie in bytes data-v1 produces from our objects and equal the reference; `captured`: 122,184) and as ranges in out\produced_ranges.json
  (32,828 placed pieces: va, size, kind, tier, unit, public symbols). A layout tool can drop those ranges from the asm and take them from our objects; D_ labels inside produced pieces must then be defined by the piece (aliases listed).

## The 7,423 pointer-sized dwords without base reloc
Aligned dwords whose value lies inside the image and that the original .reloc does not list (1,335 in .data, 6,088 in .rdata).
Rule (`value-rule`): a dword is a pointer iff its value is exactly the start of a recipe function, a placed EH/contribution piece, or an address the original .reloc already targets. 297 fields qualify.
The other 7,126 are kept literal (out\literal_lookalikes.json): their values are in the text range but not at any known start (6,578 non-round text values: ints, hash/table data, packed words), round masks/sizes (0xff0000, 0x1000000, ...),
or data values. Expected error of the rule: by density about 40 accidental matches among the 297 (function starts are 0.7% of the text range); pointers to non-start code (mid-function labels) would be missed. 68 original reloc
sites are unaligned (packed structs); they are handled (emitted as `dd` inside the byte stream). Misaligned look-alikes are not scanned.

## Output
- out\rdata_00..03.asm (split at <= 40,000 relocations per object because COFF object relocation counts above 65,535 need the extended form), data_00.asm (.data + `_BSS` tail with 1,212 labels in 714,908 B),
  tls_00.asm (`_TLS`, rename to `.tls` after assembly), const_00.asm (`_CONSTPE`, rename to `CONST`). ml segment mapping: CONST -> `.rdata`, `_DATA` -> `.data`, `_BSS` -> `.bss`.
- out\manifest.json: file, section, original va, size (the original order and addresses; MASM cannot state 4 KB section alignment, the layout tool places the chunks).
- out\code_symbols.json: 45,482 code symbols the objects reference (name -> original va, kind). out\data_labels.json: 27,591 D_ labels (+ `our_symbol` aliases).
- symbolic.json: fields `[section, offset in section, target symbol, addend, evidence, origin, target kind]`; `sections`, `bss` give the original layout.

## Round trip (verify.py)
All 7 objects assembled at the original addresses (section VAs, chunk VAs from manifest.json), relocations resolved from the objects' own D_ symbols and code_symbols.json:
.rdata 1,716,736 B, .data 262,656 B, .tls 1,024 B, CONST 512 B equal the reference byte for byte; 150,462 relocations = 150,462 fields of symbolic.json with identical symbol and addend;
all 27,591 D_ labels sit at the VA in their name; bss tail 714,908 B present. Result: ROUND TRIP OK.

## Coverage (out\stats.json)
Fields: 150,462 symbolic (87,513 to recipe functions, 34 to address-named functions, 2,880 to EH/contribution pieces, 11,319 to other code `C_<va>`, 48,716 to data labels), 7,126 literal look-alikes.
Bytes in the asm: strings 359,163, zero runs 313,451, hex bytes 686,681, symbolic pointer fields 601,848. Bytes proven produced by our objects: data-v1 total 654 KB rdata + 23 KB data (34.2% of raw);
placed pieces span 1,035,346 B of .rdata (spans include pointer fields our objects leave unresolved and zero padding).
Not done: float typing, wide-string typing, the .tls template layout (kept as bytes), resources/.rsrc and imports (M1), alignment of chunks inside the final section (layout tool).
