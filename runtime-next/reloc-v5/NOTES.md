# reloc-v5 notes (2026-11-15)

Rebuild: `set FNV_MSVC9_RTM_ROOT=C:\Projects\Decompilation\FNV\tools\vc2008rtm` then
`python -I runtime-next/reloc-v5/assemble_v5.py` (about 80 s; needs obj_v3 as before). Writes no executables.
Optional: `FNV_V5_FIXUPS=1` applies `callee_fixups.json` (reference-assisted, see 3).
v4 and pinned-build are untouched. `assemble_v5.py` = v4 + changes below; `crt5.py` = new CRT matcher.
Files: `progress_v5.json` (summary), `progress_default.json` / `progress_fixups.json` (raw runs), `relocs_v5.tsv.gz`
(all fields), `borrowed_v5.tsv.gz` (remaining borrowed, with cause), `rebase_remaining_v5.json`,
`tail_alias_candidates.json`, `callee_fixups.json`, `xcheck_v5.json`, `placed_functions_v5.json.gz`.

## 1. Rebase test: 284 -> 122 bytes (61 fields) on own rules; 0 with the original .reloc
284 bytes = 142 fields x 2 bytes (delta 0x0FC00000 changes 2 bytes). Cause of every mismatch:
- 54 fields: integer constants (0xFFFFFF, 0x1000000, 0xFF0000, 0x1400000, 0xA00000, 0x500000, 0x7E7E7E...) that the
  decompiled source declares as DAT_xxxxxxxx / g_xxxxxxxx_argN externs. The compiler emits DIR32; the original has a plain
  immediate. We shift them, the original does not. Needs a source edit; not separable from real addresses without the table.
- 88 fields: the original relocates them, our source writes the address as an integer literal (vtable stores, global and
  function pointers), so there is no COFF relocation. v5 infers 81 from our own bytes (capstone: mov/push/lea/fld imm32 or
  disp32 equal to an exact address our build already knows, not a round constant; 0 false positives of 355 other candidates).
  7 missed (6 mov, 1 cmp into data that none of our symbol maps names).
- The 1,141 "not in table" DIR32s: 1,084 are `fs:[__tls_array]` (linker-absolute 0x2C, correct, no base reloc), 3 are small
  constants, 54 are the constants above. The 1,087 outside the image never caused a byte difference; v5 just excludes them.
- No mismatch is in jump tables, EH tables or CRT code. Remaining list with values: `rebase_remaining_v5.json`.
- With the original .reloc deciding which fields shift, 0 bytes differ (proves nothing else is wrong; not independent).

## 2. Borrowed fields: 8,020 -> 4,877 (4,829 with fixups); .text 86.224% -> 86.295%, filled == reference still true
Fixed (v4 logged them as borrowed):
- 2,023 TLS SECREL fields. v3 resolved them; v4 only ever counted DIR32/REL32/DIR32NB as agree. Now compared. (Target
  addresses still come from units.json, so same circularity as the rest.)
- about 1,140 CRT fields from library objects: small lib functions (8..23 bytes, unique location only; 34 matched), data
  sections of lib members matched into .data/.rdata (82 placed, unique only), statics resolved through the placement of the
  member's own section, `___ImageBase`. Each still has to equal the reference value or it stays borrowed.
Remaining 4,877:
- 3,611 (tail): EH funclets calling destructors / operator delete whose mangled name exists nowhere in the recipe or symbol
  maps (declared, never defined in our source). 2,295 of 2,308 names have a single target (2,275 of them a recipe function under another
  name) (`tail_alias_candidates.json`). Resolving them needs the original address, so not applied.
- 1,198 (CRT): about 370 are BSS/COMMON data (no bytes to match), the rest statics or data not uniquely placed, string
  literals, SEH tables, vtables, or a copy chosen by the original linker that differs from ours (53 disagree).
- 68: 48 wrong-callee (below) and 20 `__real@` float-pool fields where another pooled copy was used.

## 3. The 48 wrong-copy calls: cause found; not duplicates
None are duplicate/COMDAT/ICF copies (0 of 48 have equal bytes; sizes differ). Our source calls a different function than
the original: 23 call a real-looking name (e.g. ctor of BGSListForm) where the original called an address-named function,
14 a different real function (PerkEntryConditionSet vs PackageEventActionData ctor, GetGameHour vs GetDayOfMonth), 11 a
const-qualifier variant (GetSex QAE vs QBE). The matcher masks call targets, so it never noticed. Real fix is a source edit.
`FNV_V5_FIXUPS=1` forces the original callee (reference-assisted; verified to be a recipe function start): 48 -> agree.

## 4. Independent cross-check of call/address targets (`xcheck5.py`, `xcheck_v5.json`)
509,991 agreeing sites: only 24,876 (4.9%) are confirmed by a body our source defines under that very symbol at that address.
About 270,000 go to a bytes-verified function from our source under a different name (link between name and address rests on
the symbol map). 213,981 go to data, thunks, CRT or undecompiled code (no check possible this way). 1 conflict
(`??0PerkEntryConditionSet` resolves to 0x680890 at one site, defined elsewhere with different bytes).
So the circularity is real: most name->address links are unconfirmed by anything but the symbol map.
