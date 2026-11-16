# data-v2 PLAN: milestone M3 (own data), scoped 2026-11-16, no edits started

Inputs: `data-v1\NOTES.md`, `data-v1\progress.json` (what our objects produce today), `build-v7\relocs_v7.tsv.gz` (code references), the reference image (read only).
Tool: `classify.py` (this folder, read-only, 1 s) -> `classify.json`. It sorts every reference byte that data-v1 does not produce into categories by structure
(it reproduces the totals: .rdata 737,710 B and .data 169,699 B non-zero, import dir/IAT excluded). Rules claim bytes in this order: RTTI type descriptors,
vtables (+ their COL / hierarchy / base arrays / base class descriptors), EH tables, strings, code-referenced constants, rest. It is heuristic (a printable-looking table can be counted as
a string; vtable ownership bytes overlap a little with RTTI), good to about +-5% per category. "Owner" = the recipe unit of the first code reference (strings, constants) or of the first
recipe function in the vtable slots.

## 1. What is not produced (non-zero bytes)
| category | .rdata | .data | total | our objects hold it? | owner |
|---|---:|---:|---:|---|---|
| vtables with RTTI (3,039 vtables) | 162,741 | 0 | 162,741 | partly: 5,380 vtable pieces (100 KB) placed, 14,905 slot fields point at names defined nowhere | recipe unit of slot functions: almost all |
| code-pointer tables without RTTI (3,767 - 3,039 runs; includes CRT$XCU init arrays 42 KB, dispatch tables) | 88,104 | 7,460 | 95,564 | init arrays: yes (16 pieces, unique place missing); others: partly | units for 90%, 171 B no recipe function |
| RTTI type descriptors (3,000, in .data) | 0 | 104,809 | 104,809 | yes, 6,471 pieces / 207 KB, but with our class names (FUN_xxxx, Base5a) so bytes match nowhere | 986 of 990 slices owned by a unit |
| RTTI COL + hierarchy + base arrays + base class descriptors + COL ptr | 94,346 | 0 | 94,346 | yes (rtti1..rtti4 pieces, 200 KB, ambiguous because they embed type-descriptor addresses/names) | same classes as the vtables |
| strings (ASCII/UTF-16) | 284,522 | 1,238 | 285,760 | yes: 8,969 pieces placed (198 KB); 179 match nowhere (11 KB); the rest has no object or ambiguous duplicates | 191,417 B first-referenced by a recipe unit, 8,327 B by code outside the recipe, about 85 KB not code-referenced (tables of names, shared suffixes, false positives) |
| EH tables (FuncInfo, unwind/try/ip maps, catch types) | 4,136 | 16 | 4,152 | yes: 258,643 B already produced; 1,509 ambiguous + 41 no match left | functions' units |
| code-referenced constants <= 8 B (floats/doubles/ints) | 7,327 | 4,275 | 11,602 | yes: `__real@` COMDATs (692 placed, 4,205 B) | recipe units (11 KB owned, 2.5 KB code outside recipe) |
| code-referenced 9-64 B (small tables, float4, structs) | 19,348 | 3,722 | 23,070 | partly | 17.9 KB owned, 2.1 KB outside |
| code-referenced > 64 B (lookup tables, static arrays/structs, initialized globals) | 18,261 | 12,959 | 31,220 | mostly no: globals are `extern DAT_` in our source, 37 data-unit pieces exist | 4.5 KB owned, 1.3 KB outside, rest not attributable |
| other (not code-referenced: arrays/structs referenced from data, padding patterns) | 58,933 | 35,220 | 94,153 | mostly no | not attributable without the data-reference graph |
| total | 737,710 | 169,699 | 907,409 | | |
Not counted: 397,434 + 77,661 zero bytes (alignment padding, zero-initialized data inside the file), 1,548 B import dir/IAT (M1), BSS (no file bytes, 714,908 B of virtual tail,
349 pieces / 68,273 B known from our objects), .tls (709 B virtual; 638 produced, 54 pieces ambiguous).

## 2. Cheapest route per category, and order
Order is by (bytes unlocked) / (work, reference independence). Each step must keep filled == reference and the rebase/own-reloc checks.

1. **Finish placement of what our objects already hold (no source work)**, about 150-250 KB:
   - strings: 179 no-match (11 KB) are mostly strings whose bytes changed in our objects (alignment/padding, merged suffix pooling); place by "first free exact hit in unit order" for duplicate content
     (the linker with /GF pools one copy; the k-th duplicate takes the k-th address, as sgmap_w2 already does for $SG labels). Expected +85-200 KB of the 285 KB.
   - float/double pools `__real@`: same rule (+11 KB). EH tables: 1,509 ambiguous (43 KB) by the same ordering rule, + 41 no match (2 KB) to inspect (+4 KB unproduced remain).
   - CRT$XCU/$XIU init arrays (42 KB, 6,266 pointers, all resolved): the linker concatenates `.CRT$XCU` contributions in object order; reproduce by sorting our 16 pieces in unit order and placing the
     merged array at the one unique hit. Needs the link-order model of M4 only for placement of the array head (+42 KB).
2. **Original class names, then RTTI (199 KB) and vtables (250 KB), the biggest block, about 50% of the unproduced bytes.** Our classes carry placeholder names, so every type descriptor (".?AVname@@") mismatches and
   all COL/hierarchy/base-descriptor bytes depend on them. Route: (a) a name table class-in-our-source -> original name, taken from the reference's own RTTI strings (they are symbols of the game, like the Ghidra names; this is
   reference-derived metadata, to be stored once as a checked-in table, not per-byte copying); (b) rename the classes in source (about 3,000 classes, mechanical text rename per unit, recompile) and fix
   inheritance order where hierarchy descriptors differ; (c) declare every virtual slot so the vtable has its definitions: 14,905 slot fields (6,013 names: __purecall 1,196, Unk_/vfn_ named slots, scalar deleting dtors `??_E`)
   point at names defined nowhere; the functions exist (all code is ours) but under other names. Cheapest honest fix: make the override names match, class by class, as the code is renamed in (b); do not bind them by
   address (that would be another overlay). Risk: derived-class slots that resolve to the base method (seen in data-v1), i.e. our source's slot layout differs. Start with the 1,000 classes that already have a vtable
   placed and a unit (RTTI hit rate there is highest).
3. **Initialized globals and tables (.rdata 59 KB other + 18 KB large tables, .data 35 KB other + 13 KB large tables, about 125 KB).** Not in our objects: the decompiled source declares them `extern DAT_xxxx`.
   Route: generate definitions `DAT_xxxx = {initializer}` into a new unit per address range, with the initial bytes taken from the reference. This is data capture, not decompilation, and should be labelled as such
   (same status as `_emit`). Typed arrays/structs are better done by hand for the biggest 20 tables (lookup tables, key-name tables) and by byte capture for the rest. Strongly recommend doing it AFTER 1 and 2 so that
   strings/RTTI already placed shrink the "other" bucket (many "other" bytes are pointers to strings and vtables).
4. **Small constants (35 KB) not placed by step 1**: define as `static const` in the units that reference them, or accept as part of step 3.
5. **BSS / .data tail (714,908 B virtual) and TLS**: layout only; needs `DAT_` definitions with sizes (from the 349 pieces and from unit symbol maps) and the PE .tls template (data-v1: `.tls$` is not the PE layout).
   Do together with M4 (own linker layout); no file bytes involved.

Expected state after 1+2: about 60% of the 907 KB produced beyond data-v1's 30% (rdata 33.8%, data 5.8%) of the raw sections; after 3, all but BSS/TLS.

## 3. Dependencies and risks
- Everything in step 2 depends on the class-name table; building it costs one pass over the reference's RTTI (3,000 type descriptors) and a join with our vtable pieces via the vtable address (units.json symbols).
- The own .reloc for data (351,931 - 201,766 = 150,165 sites) comes for free once data is produced from objects: every DIR32 in an object section is a base-reloc site (same rule as .text, `reloc-v7\ownreloc.py`).
- 7,156 pointer-sized fields in data have no relocation in the original .reloc (layout-v1): they must stay unrelocated; the rule "COFF DIR32 to an in-image symbol" would add them wrongly.
- data-v1's H/L placements depend on reference addresses; steps 1-2 should use B/V tiers only, and report H/L separately.
- Check after each step: `data-v1\report.py` totals, filled == reference, rebase test (`build-v7\progress.json`), `cmp_strict.py` style non-regression of produced bytes.
