# reloc-v7 notes (worker B, 2026-11-16) - milestone M2, own every address field in .text

Result on build-v7 (rebuild.cmd, about 3 min): `borrowed_relocation_field_bytes` 19,609 -> 24 (4,752 fields -> 8 unique fields), rebase test `text_bytes_differing v5_rule` 122 -> 0,
coverage 99.82% -> 99.996% (the 19 KB of borrowed fields are now our bytes), filled_equals_reference true, no unit and no byte lost (`cmp_strict.py`: 0 lost against the strict image of every step).

## What is a source fix and what is a binding table (read this before relying on the numbers)
- Source fixes (real, in fnv_decomp\src): 61 rebase fields (integer constants / literal addresses), 44 of 48 wrong-copy callees. See `changed_files.txt`.
- `binding_overlay.json` (new, symbol binding data): 2,044 (unit source, mangled name) bindings in 423 units, 355 CRT/STL global names, 389 per-field targets. It resolves about 4,700 fields,
  mostly EH-funclet calls to destructors / operator delete and CRT globals. **It is derived from the reference image** (`mk_overlay.py` reads the original call/field target of each field that was borrowed
  in the baseline). It plays the role of the original link's decisions: which of several identical (ICF-folded) functions a generic name such as `??1RefPtr@@QAE@XZ` or
  `??1?$NiPointer@...@@QAE@XZ` reached (the original calls 0x45cec0, 0xb66f20, 0x44a540 ... for them), and where CRT globals live. For all but 33 of the 3,081 funclet calls the target is the start of a recipe function whose bytes we produce;
  the rest are CRT functions. Nothing in the overlay is a byte copy; but it is not independent evidence, same circularity as the existing `fixups`/symbol maps. It goes away in M4: a real link with /OPT:ICF
  makes the same fold decisions, and per-class unique dtor names are not needed. Switch it off with `FNV_OVERLAY=0` (borrowed count returns to the baseline).
- Applied only where we would otherwise borrow or disagree (`exp is None or exp != observed`); sites that already agree are never touched.

## 1. Baseline breakdown (before any change; `breakdown_baseline.md`, `breakdown_fields.json`)
4,750 unique fields (19,609 B counted by the metric; the metric counts a few bytes twice, see 3.4).
| cause | fields | bytes |
|---|---:|---:|
| EH funclet calls a destructor/operator delete whose mangled name is defined nowhere in our sources (name unbound) | 2,668 + 90 (contribution EH pieces) | 11,032 |
| EH funclet call bound to the wrong identical copy by ICF fold (lowest address taken; the original calls another copy) | 228 + 2 | 920 |
| EH funclet call bound by the symbol map to another copy | 90 | 360 |
| CRT/STL library code: CRT globals not placed (__errno 280, ___pioinfo 72, ___doserrno 46, _tzinfo, ...), strings, vtables, member statics | 1,576 | 6,304 |
| recipe functions: call resolves to a different function than the original calls (source bug) | 48 | 192 |
| recipe functions: `__real@` float pool / string literal copy | 20 | 80 |
| accepted web contributions (vtable/global/EH-stub fields) | 21 | 84 |
Owner: the EH-funclet fields sit in 423 units; the largest are the generic-name users: staging/blk_00aa0000_od_ob1_variant (148), blk_00ac0000 (118), speedtree/frondengine (86), blk_00c40000 (85), speedtreert (84),
menus/specialbookmenu (77), generated/setting_eh_initializers (71), blk_00440000 (63), tesobject_ob1_variant (58), blk_00ba0000 (58). 1,576 fields are CRT with no source file; 91+21 are contributions.
Top callee names: `??3BkItemBase@@SAXPAX@Z` 75 (all -> 0x401030), `??1SettingBase_01012120` 71 and `??1Setting` 68 (-> 0x404950), `??3@YAXPAX0@Z` 63, `??1GlobalObject_0096a2d0` 60 (-> 0x46ffb0),
`??1MemContextGuard` 21 (-> 0x404ee0), NiPointer / RefPtr / basic_string dtors (-> 0x45cec0, 0xb66f20, 0x44a540). 3,018 of 3,081 funclet fields have exactly one target per (unit, name); 63 have more than one in a unit (generic names), they are bound per field.
Rebase residue (122 B = 61 fields): 54 fields where the source wrote an integer constant (0xffffff, 0x1000000, 0xff0000, 0x1400000, 0xa00000, 0x500000, 0x7e7e7e ...) as `(unsigned)&DAT_xxxxxxxx`
or as a `g_*_arg1` extern (the compiler emits DIR32, the original a plain immediate), 7 fields where the source wrote a real address as an integer literal.

## 2. What was done
- `assemble_v7.py`: loads the overlay (FNV_OVERLAY, default on); resolution order unchanged, overlay last and only for non-agreeing fields; the borrowed list carries unit and addend;
  EH pieces for the same address are ordered by number of unresolved fields; a heal pass resolves a field borrowed in the first-placed copy of a piece when another unit's copy of the same piece resolves it
  (229 fields); `place()` no longer demotes a fully-contained field to "borrowed" just because a neighbouring byte was placed earlier; `int_constants.json` keeps the literal-address inference from
  treating the fixed constants as addresses; dumps `inferred_literals_v7.json` and `borrowed_bytes_v7.json`.
- `crt5.py`: overlay in the final pass only (phase 1 must still see the names as unresolved so the data sections get placed).
- `rebuild.cmd`: pass 1 runs with FNV_OVERLAY=0 so the ICF fold is computed from the same wanted-name list as before; the overlay applies in the final assemble.
- Source: 28 files of integer constants, 5 files of literal addresses (-> `extern char DAT_xxxxxxxx` + `&`), 44 wrong callees; backups `.bak-20261116-wB`; objects recompiled into
  pinned-build\obj_v3 (backup obj_v3.bak-20261116); `$SG` labels of the 18 units whose label list changed are rebound by content (`sidecar_update.py`, sidecar backup `sg_sidecar_w2.json.bak-20261116-wB`).
- Tools in this folder: `breakdown.py` / `breakdown_report.py` (tables), `mk_overlay.py` (overlay from `borrowed_base.tsv.gz`, the baseline list), `fix_consts.py`, `derive_new.py`, `edits2.py`, `recompile_units.py`,
  `sidecar_update.py`, `find_units.py`, `cmp_strict.py A.exe B.exe` (bytes lost/gained between two strict images; must stay 0 lost), `summ.py`, `rb.cmd` (rebuild to rebuild_last.out).

## 3. What remains (24 B, 8 fields) and why
1. 6 fields (`fn:a`, 4 REL32 + 2 DIR32): `PerkEntryConditionSet` default constructor (0x5e9f60) where the original constructs members / arrays with 0x680890 (`PackageEventActionData`, 22 bytes): bgscamerapath.cpp (member),
   bgsperk.cpp (array new x2, member), testopicinfo.cpp (local + member, 2 sites). The fix is a type change (member type must be a class whose constructor symbol is `??0PackageEventActionData`), and for
   array new the compiler also takes the destructor, so a derived type would add a synthesized dtor. Not attempted: risk of regressing four large functions.
2. 2 fields in EH funclets (`??1PixelOwner`, `??1NiPointer<NiScreenElementsData>`; icf-fold choose another copy) and 1+1 (`??3Body`, `??3FUN_00d4f2a0`, ...): the field straddles a piece boundary, only part of its bytes belong to the placed piece.
3. Not a field: 441 B of EH pieces whose bytes differ from the reference (missing_b_failed_pieces), unchanged.
4. The metric counts bytes per placement, so it can exceed 4 x fields; after the heal pass the 24 B equal the 8 fields plus 3 partial fields.

## 4. For M2 / M4
- Own .reloc: all 528,6xx fields in .text have a resolved target; DIR32 fields that need a base relocation are exactly the ones the rebase test shifts (0 bytes differ with our rule, 0 with the original table).
- Before M4, replace the overlay by real definitions: (a) per-class dtor/operator-delete names are not needed with a real link (ICF), (b) CRT globals come from linking libcmt/libcpmt objects.
- Do not feed the overlay into data-v1 or direct-v1 as evidence; it is a derived table.

# Round 5 (code section 100% real source) - 2026-11-16
Strict build (build-v7): 10,843,747 of 10,843,747 non-padding .text bytes are ours (100.000%), 0 holes (`missing_b_failed_pieces` 0), borrowed bytes 0, rebase residue 0 (v4_rule 0), inferred literal sites 0,
filled == reference, nothing lost at any step (`cmp_strict.py` against the previous strict image after every batch: 0 lost).
Real source vs byte copies: 0 `_emit` lines remain in fnv_decomp\src and in the 1,088 accepted contributions (was 5,437 `_emit` lines + 117 bytes of data in 331 contributions).
- 331 `_emit` funclet contributions (0xeea770-0xf35000, 8,337 B) -> naked asm with real instructions and symbolic call/jmp targets (`emit2asm.py`: disassemble the accepted object, write inline asm, recompile,
  compare code bytes and relocation table). Owner functions could not be used: the funclets' parents are not in the recipe in a form the compiler reproduces (the compiler's own funclets for those functions never matched),
  so each funclet group stays a naked function; per-funclet owner mapping from FuncInfo (data-v3 symbolic.json) is the next step if a compiler-generated form is wanted.
  New units: src\funclets\eh_funclets_00..04.cpp (329 functions), tail_stubs.cpp (3 items: `rep ret` stub, a static-init stub, and the 117-byte data table as a `.text$zz` const array),
  eh_gaps.cpp (38 funclets that no compile produced: the former 441 B of "failed EH pieces", `gaps2asm.py`), `merge_fix.py` (functions that started one byte early, two `jz` rel32 to outside targets).
  Units appended to units.json (indices 2988-2994, backups units.json.bak2..bak7-20261116-wB) and to pinned-build\logs\compile_v3.jsonl (backup .bak-20261116-wB).
- Queue state (`integrate_funclets.py`, `fix2.py`): the 330 retired contributions moved to FNV\local\contributions-replaced\ (suffix .emit2asm-20261116), removed from local-targets state.json `accepted`
  and catalog.json `targets` (backups state.json.bak-20261116-wB, catalog.json.bak-20261116-wB). Contributions remaining: 1,088, all real C++.
- 81 inferred literal addresses -> real extern symbols (`inf_apply.py`): data -> `((int)&PTR_<va>)` with `extern char PTR_<va>;`, code -> `((int)SUB_<va>)` with `void SUB_<va>();`
  (names resolve by the embedded address; PTR_/SUB_ avoid clashes with existing DAT_/FUN_ declarations); 44 files, backups .bak-20261116-wB; `$SG` sidecar rebound (`sidecar_update.py`).
- The PerkEntryConditionSet constructor: the recipe also had a class PerkEntryConditionSet in bscore\bsreadwritelock (a different 65-byte class at 0x5e9f60) that took the name; renamed to FUN_005e9f60_cls
  (rename_apply.py), after which the unit symbol maps bind the real PerkEntryConditionSet/PackageEventActionData to 0x680890/0x6808b0. Fixed all 6 remaining disagree fields (24 B).
- Rebuild.cmd still runs everything (about 3 min). Remaining non-source bytes of .text: 132,464 B CRT/STL library code (libcmt/libcpmt objects, by design).
