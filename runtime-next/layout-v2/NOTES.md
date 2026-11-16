# layout-v2 (M4a): first runnable free-layout build (2026-11-16)

Tool: `python make_layout.py --layout G|U|R|REV|Z [--seed N] [--sweep] [--out F]` (G = same order in the new section = machinery check;
U = units gathered; R = U with each unit reversed; REV = whole block order reversed; Z = random permutation of super-blocks).
Input: direct-v1\FalloutNV_direct.exe (own imports + own .rsrc, bind-free). Output: FalloutNV_layout_<L>.exe in this folder. Nothing else is written.

## What it does
1. Block model of .text (model.py): units.json functions (68,657) + eh_tails (1,861) + build-v7 contrib_pieces (1,855) = atoms; trailing pad (CC/00/90) stays
   with the atom; everything between atoms is a rigid **gap block** (243 gaps, 288,937 B: CRT, EH pieces outside units, failed/undecompiled pieces and the `_emit`
   funclet contributions). Blocks keep their address mod 16. 72,616 blocks.
2. Fields: .text REL32 from build-v7 relocs_v7.tsv.gz (323,865, **OWN**), DIR32 absolute sites by the ownreloc rule (relocs_v7 agree/disagree + inferred_literals_v7.json,
   201,766 sites, **OWN**; the tool checks the set is identical to the reference .reloc sites in .text: True). SECREL records (2,027) are TLS offsets, not addresses, left alone.
   Original value of every field is read from the image (filled == reference), the target is mapped with the block map, the field is re-encoded at its new position.
3. Chains: a capstone sweep finds blocks that can fall through (no trailing pad, last instruction not a terminator: 40) and rel8 branches that leave their block (364,
   mostly decode noise in tables); the blocks between source and target are kept adjacent (344 chained boundaries, 72,272 super-blocks).
   The sweep also finds 47 rel32 branches not in the records; the 43 in gap blocks (undecompiled code) are used (**DIS**), 4 inside atoms ignored.
4. New section `.ntext` at RVA 0x1009000 (VA 0x1409000) holds the new .text; the old .text range is filled with 0xCC so any missed reference faults. Entry point,
   section table, SizeOfImage/SizeOfCode, checksum are rewritten.
5. Data->code pointers in .rdata/.data (vtables, EH/SEH tables, callbacks): 101,449 positions come from the **reference .reloc (BORROWED)**, values are mapped with our block map.
   7,156 aligned dwords in .rdata/.data hold a .text-range value but are not in .reloc (297 equal a block start); they are NOT remapped (`--remap-unreloc` experiment).
6. .reloc regenerated: data sites (reference positions) + the new text sites (351,931 sites, 734,888 B, same size as the original).
7. Imports, TLS directory (callback table empty), resources are untouched (imports and .rsrc already own, see direct-v1).

## Results
Harness (direct-v1\harness.py: menu, Continue, 120 s walk/turn/Pip-Boy, Esc-Quit-Exit, exit code, WER check), all PASS, exit code 0, no WER events:
| layout | order vs original | harness |
|---|---|---|
| G | identical order, moved to .ntext (old .text = 0xCC) | 40 s dbg run only, no crash |
| REV | whole order reversed (72,272 of 72,272 super-blocks moved) | PASS |
| Z | random permutation (seed 1) | PASS |
| U | units gathered | PASS |
Verdicts: direct-v1\harness-out\layout_REV|layout_Z|layout_Uerdict.json. Rebase check (direct-v1): FalloutNV_direct_aslr.exe (ImageBase 0x1000000 + DYNAMIC_BASE) really loads at another base (0x1c0000 seen with dbg.py) and passes the harness.
No crash occurred, so no hidden position-dependent code was found in the exercised paths (menu, load, world, Pip-Boy, exit). Not covered: combat, other cells, saving, audio/video paths not hit.
## Remaining borrowed / limits
- data->code pointer positions (101,449) from the reference .reloc; 7,156 unrelocated .text-range dwords in data left as is (297 equal a block start) - not exercised.
- gap blocks (243, 288,937 B) move rigidly; their rel32 not in records were found by capstone (43). Chains (344) are conservative heuristics.
- Old .text kept as an unused 0xCC section (not removed); layouts U/R keep unit groups only, no cross-unit tuning.

# M4b + M4c: make_image.py (self-assembled image, code AND data moved)
`python make_image.py --layout G|U|R|REV|Z [--keep-data-order] [--vr skip|remap] [--out F]` -> FalloutNV_image_<L>.exe. No reference exe is opened as a starting point; the PE headers
(DOS header, PE/optional header, 7 section headers, 16 data directories) are written by the script. Layout: .data(+714,908 B bss tail) .rdata (4 chunks, order reversed unless
--keep-data-order) CONST .tls .text .rsrc .reloc, contiguous from RVA 0x1000, every section at a different RVA than in the original, new code order as in M4a.
(A NOACCESS hole over the original image range was tried: Windows refuses images with a section gap of ~12 MB or more, error 193, so sections are contiguous.)

## Sources (exactly what is still reference-derived)
| part | source | reference-derived? |
|---|---|---|
| code bytes | build-v7 FalloutNV_v7_strict.exe .text (our placed pieces + gap blocks) + 465 bytes taken from the filled image (borrowed fields / failed EH pieces) | 465 B |
| code fields | relocs_v7.tsv.gz (323,865 REL32; 201,766 abs sites by the ownreloc rule + inferred_literals_v7.json), 43 extra rel32 in gap blocks by capstone | no (own rule == original .reloc, checked in M4a) |
| block boundaries / chains | units.json functions+eh_tails, contrib_pieces.json, gap blocks (243, 288,937 B, move rigidly), capstone sweep (344 chained boundaries) | no |
| data bytes | data-v3\out\*.obj raw section bytes (round trip byte-exact) | captured literals: strings/zero runs/hex bytes (122,184 of the pointer fields and all non-pointer bytes not produced by data-v1) come from the reference image via data-v3; 34% of bytes are produced from our objects |
| data pointers | obj relocations (symbol + addend -> new address of the symbol): 150,165 (positions = reference .reloc) ; the 297 `value-rule` fields are kept LITERAL (see below) | positions from the reference .reloc |
| imports | build_imports.py spec re-based to the new IAT/directory addresses, regenerated tables | slot order/IAT layout, hints, hint/name order from reference (iat_spec.json) |
| .rsrc | build_rsrc.py at the new RVA (inputs extracted from the installed exe at build time) | binary icons/bitmap/SPAFILE |
| TLS dir, entry | TLS directory is a data chunk (its VAs are obj relocations); entry = new address of WinMainCRTStartup (0xECC4DB) | CRT entry address found by call analysis |
| PE header constants | hard-coded (linker 9.0, OS/subsystem 5.0, stack/heap 1 MB/4 KB, dll flags 0x8000, timestamp 0x4E0D50ED) | copied from the reference header values |
| debug directory | dropped (zeroed) | - |

## Findings
- First data move crashed in zlib inflate (bogus input pointer). Cause: the 297 `value-rule` fields of data-v3 (aligned dwords whose value equals a function/piece start but that the
  original .reloc does not list) include accidental integers (zlib table/hash constants). Remapping them corrupts data; keeping them literal fixes it. `--vr remap` reproduces the crash.
  So the value rule is wrong for at least some of the 297; none of them was needed as a real pointer in the exercised paths. The remaining 7,126 look-alikes are left literal (not remapped).
- Bisect aids: `KEEP_SECS`/`DATA_ORIG` env vars place the data sections at their ORIGINAL RVAs (identity data map) - this passed with moved text before the value-rule fix was found.
- Several harness failures (exit 0xC0000417 = CRT invalid parameter during load, REV and Z images, some runs only) were caused by stale inputs: worker B rebuilds build-v7/units.json while I work,
  and the capstone sweep cache (fall-through / rel8 chains) was keyed by block INDEX, so a changed block list glued or unglued the wrong blocks. Fixes: snapshot.py freezes every input into
  layout-v2\snapshot (strict/filled .text, relocs, units, contrib pieces, data-v3 objects + symbolic), and the sweep cache is keyed by a hash of block boundaries + code bytes.
  (A second game instance in the same run folder is another possible collision, so harness.py takes an exclusive harness.lock: atomic create, PID + timestamp, stale after 20 min or dead PID.)
  Re-run `python snapshot.py` to pick up a newer build-v7/data-v3.

## Results (harness, snapshot inputs of 2026-11-16 07:10; 72,690 blocks)
| exe | what moved | harness |
|---|---|---|
| FalloutNV_image_REV.exe | code order reversed, data chunks reversed, all sections at new RVAs | basic 120 s + extended: PASS (twice) |
| FalloutNV_image_Z.exe | random code order, data chunks reversed | extended: PASS |
| FalloutNV_image_U.exe | units gathered | basic: PASS |
| FalloutNV_image_G.exe | code order kept, data moved | built, not run through the harness |
| direct-v1 FalloutNV_direct.exe (original layout) | nothing | extended: PASS (reference run) |
Extended = F5 quicksave (a new quicksave.fos appears in run\Saves), console `coc GSProspectorSaloonInterior` (cell change), walk, R + click, console `set gamehour to 20` (game-time change),
F9 quickload (world loads), then Esc/Quit/Exit with exit code 0 and no WER events. Screenshots in direct-v1\harness-out\image_*_ext\.
