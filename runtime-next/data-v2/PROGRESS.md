# data-v2 PROGRESS (worker B, 2026-11-16)

Produced bytes = data-v1 report (`data-v1\progress.json`), file bytes of .rdata/.data that come from our objects and equal the reference. filled == reference after every step.

| step | .rdata | .data | .rdata+.data raw % | notes |
|---|---:|---:|---:|---|
| data-v1 baseline (2026-11-15) | 580,044 | 15,296 | 30.08 | |
| + CRT/STL library members' data sections (libcmt/libcpmt, pseudo-units 100000+, tier B) | 620,140 | 20,458 | 32.36 | `data-v2\libsecs.py`, hook in `data-v1\place.py` (DV_LIB=1) |
| + CRT$XCU init array (ascending runs, our 6,266 initializer addresses) | 631,916 | 20,458 | 32.96 | `data-v1\report.py` (DV_XCU=1): 11,776 B; the rule is in the code comment |
| + tier O (duplicate-content ordering rule) | 653,579 | 20,458 | 34.05 | `data-v1\place.py` (DV_ORDER=1): 201 pieces, 22,363 B |
| + class rename pilot (12 classes) | 653,690 | 20,862 | 34.07 | type descriptors +404 B, COL/hierarchy +~100 B; see below |

Category breakdown after the pilot is in `data-v1\progress.json` (`produced_bytes_by_kind`).

## Step 1 notes
- Strings: only 14 KB of unplaced string pieces were in our object set, so the ordering rule could not add much there; the large "unproduced strings" (285 KB) mostly lay in the CRT/STL libraries
  (data-v1 never loaded them) and in strings not referenced from our objects. Library members brought +45 KB (rdata +40 KB, data +5 KB).
- Init array rule: the original linker concatenates `.CRT$XCU` in ascending (link-order = address) runs; the reference holds three long ascending runs (1,845 / 1,249 / 668 dwords) of which 3,400+ entries are our compiled
  initializers. A dword is produced only if its value equals one of our resolved initializer addresses and lies in a run that is >= 80% ours and ascending. Order ambiguity: duplicates of a value (variant units) are merged.
- Tier O: pieces whose masked bytes are identical form a group; the group's pieces sorted by owning unit's first function address take the free reference hits in ascending order. Pointer fields count only where our value equals the reference.

## Step 2 pilot: class renames
Tooling (all in data-v2): `rename_scan.py`, `pilot_pick.py` / `pilot_pick2.py` (candidates from placed vtables whose COL names the class), `rename_apply.py` (source rename + recompile + proof + units.json update),
`kwswap.py` (class/struct keyword fix so `.?AV`/`.?AU` match), `msub.py` (mangled-name rename).
Checks per class, all enforced by the script: keyword of our definition vs RTTI V/U; `Old` appears in one source file; recompiled unit has the same symbol count and every symbol equals the textually renamed old symbol
(so `$SG`, `__unwindfunclet$`, vtable/RTTI names all follow); units.json (recipe) is updated with the same rename for that unit; on any failure the source and the object are restored.
Whole-build proof after the 12-class pilot: build-v7 rebuild: ours_bytes 10,843,312 (unchanged), 0 bytes lost / 0 gained against the strict image, borrowed 24, rebase 0, filled == reference.
data-v1 after the pilot: .data +404 B (type descriptors accepted), rtti1-4 +~100 B. The vtable pieces themselves were already placed (V tier); their names now match RTTI.
Backups: source `.bak-20261116-wB`, `fnv_decomp\build\units.json.bak-20261116-wB` (before the first rename), objects `pinned-build\obj_v3.bak-20261116-pilot` (before the pilot).

## Step 2 batches (state at the end of this round)
| batch | classes renamed | .rdata | .data | % | build-v7 proof |
|---|---:|---:|---:|---:|---|
| pilot | 12 | 653,690 | 20,862 | 34.07 | 0 lost / 0 gained, borrowed 24, filled == reference |
| batch1 (119 candidates: Old in one source file, New not in that file; 2 reverted because New collided with an existing recipe class: CharGenMenu, BSTaskletGroupData) | +69 net | 654,364 | 22,884 | 34.22 | same |
| batch2 (35 candidates after screening New against every class name in units.json) | +14 | 654,522 | 23,364 | 34.25 | same |
Total renamed: about 95 classes (renamed_*.json). Rejections are all caught by the script: keyword swap not possible (templates), method with the same name as the class (FUN_00626060), $SG shift, back-reference letter change
after struct->class (U0/U1), class already defined in an included header, New already a class in the recipe (merging two recipe classes changes symbol bindings; see CharGenMenu).
Why it does not scale yet: of 1,404 vtables whose COL names an original class with a simple name, only 212 have an Old identifier in exactly one source file; 2,972 of 3,039 vtables differ from our names,
but most are Primary/Secondary/Base placeholders for secondary vtables and templates. Next design step (not started): rename per (identifier, set of files) with the same check, merging classes by recipe address
(units.json functions) instead of by name; keep per-batch rebuild proof. Gains per class are small (about 30 B type descriptor + COL/hierarchy); the large wins (vtables 250 KB) need slot names resolved, not just class names.
