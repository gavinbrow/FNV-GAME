# link-v2: a real link.exe link (worker B, 2026-11-16) - state: link does not succeed yet; causes quantified

Gold-standard route: link our objects with the stock VC2008 link.exe. This round built the whole input pipeline and ran the first real links. No exe was produced, so the harness was NOT run
(harness.lock logic is present in direct-v1\harness.py; nothing launched).

## Pipeline (scripts in this folder, run in this order)
1. `build-v7` rebuild with `FNV_DUMP_SYMADDR=1` (new hook in assemble_v7.py) -> `symaddr.json`: per recipe unit, every external symbol name -> the address the verified build resolved it to (14 MB, includes overlay/ICF/sized-delete bindings).
2. `compile_contribs.py` -> `obj_contrib\` (1,088 accepted contributions compiled like the checker; all 1,088 ok).
3. `prep_objs.py` (+ `coffrw.py`, a COFF symbol/section rewriter): rewrites the 2,995 unit objects
   - recipe function definitions -> `C_<va>` (static functions made external); 69,036 code COMDATs kept, 99,144 unplaced code COMDATs physically removed (sections dropped, renumbered, their defined symbols become undefined);
   - undefined externals with a verified address -> `C_<va>` (143,926 symbol uses) / `D_<va>` (59,043); lib (libcmt/libcpmt) names and `__imp_` imports kept; `.sxdata` dropped, `@feat.00` cleared.
   `prep_contribs.py` does the same for the contribution objects (985 definitions -> `C_<va>`, 1,036 `C_` and 3,107 `D_` references, 96 without address).
4. data: `data-v3\gen.py` with `DV3_CNAMES=1` (all code targets as `C_<va>`, 65,237 `D_<va>` labels = data-v3's own 27,591 + 36,687 labels for every data address our objects name + 2,160 from contributions) -> `data_out\*.asm/.obj` (ml.exe).
5. `mk_implibs.py` + `build_implibs.cmd`: import libs from the original IAT description (`direct-v1\iat_spec.json`): def lines `decorated=undecorated` (so stdcall names import by plain name), including C++-mangled decls of API functions
   (`?GetTickCount@@YGKXZ`) and slot-address names (`IMP_/FUN_/DAT_<slot va>`); 13 DLLs (KERNEL32 147 symbols, USER32 46, steam_api 11, d3dx9_38 21, binkw32 8, ...). Remaining 30 `__imp_` names come from the SDK libs (wsock32, kernel32 ...).
6. `mk_rsp.py` -> `link.rsp`; `link1.cmd` runs `link.exe @link.rsp` (flags: /FIXED:NO /SUBSYSTEM:WINDOWS /ENTRY:WinMainCRTStartup /OPT:REF /OPT:NOICF /NODEFAULTLIB, libs: our import libs, SDK libs, libcmt, libcpmt); `loganalyze.py link1.log` groups the errors.
   Resources (`direct-v1\build\resources.res`) are not yet added to the rsp.

## Link results (4,090 objects: 2,995 unit + 1,088 contribution... + 7 data)
| link | LNK2005 duplicate | LNK2001 unresolved (data refs) | LNK2019 unresolved (code refs) |
|---|---:|---:|---:|
| 1. objects as compiled (no rewriting) | 5,714 | 31,547 | 15,407 |
| 2. rewritten, unplaced code removed, symbols address-named | 4,747 (4,556 names) | 86,608 (70,085 distinct names) | 1,785 (1,785 distinct) |
Symbol census of the raw objects (`symscan.py`): 178,792 defined names, 200,326 undefined names not defined by our objects (109,186 address-named, 90,713 other, 288 imports, 139 libcmt/libcpmt), 4,546 non-COMDAT duplicate definitions, 7,318 COMDAT duplicates (fine).
Address coverage of the 200K undefined names (`quant.py`): 118,330 code names map uniquely to a .text address, 49,983 to data (.rdata 19,949, bss 30,000, .data 3,188, .tls 398), 24,918 have no address (template instance methods/dtors, resolved in the build only per site through the overlay),
66 libcmt names are ambiguous, 29 names have several addresses per object (needs per-site rebinding, the overlay's by_field cases).

### What still fails after link 2, by cause
1. Data references from the objects' own data sections (70,085 names, 86,608 uses): vtables, RTTI, EH tables, string tables of the unit objects name virtual functions and statics that no object defines
   (48,783 plain names such as ?Init@BaseFormComponent@@UAEXXZ, 9,247 address-named names not mapped, 12,047 `C_` EH funclet addresses referenced from data-v3's captured EH tables). Cause: two copies of every data object exist (our unit data, data-v3's captured data) and the pieces name functions by recipe name.
   Fix (designed, not done): remove the data sections from the unit objects (code-only objects), rebind their local references (`$SG` strings through the sidecar, `__real@` constants, statics, vtable/RTTI/EH symbols) to `D_<va>` using data-v1's placement map of our pieces, and in data-v3 keep our objects' bytes for produced ranges instead of captured bytes; EH tables then come from our objects (their funclet symbols are local) and the 12,047 `C_` EH addresses disappear.
2. Duplicate definitions (4,556 names): 4,546 non-COMDAT data definitions defined in several units (variant units compiled from copies of the same source define the same globals, e.g. g_memoryManager), plus 10 recipe functions placed twice (`fn-duplicate-address`, two units define the same address).
   Rule to apply: one defining unit per address (the unit build-v7 places); other units' copy of a global is converted to an undefined reference `D_<va>` (same rewriting as for functions) - needs the data placement map from (1).
3. Code references unresolved (1,785): 1,320 names with no verified address (functions referenced only from unplaced code or only per-site), 203 address-named names not in the build's maps, 191 CRT/EH-region `C_` addresses (CRT functions: bind `C_<va>` to the libcmt symbol with /ALTERNATENAME from the symbol-name table), 71 imports (SDK lib names: add libs / more defs).
4. Not yet attempted: resources into the link, section merging like the original (.rdata/.data order), TLS (`.tls` template and the 398 tls names via SECREL), /FIXED:NO base-reloc check against `reloc-v7\ownreloc` output, the harness run.

## Reference-derived inputs of this link (all must be listed in any claim of independence)
- `symaddr.json`: addresses of names come from the verified build resolution = units.json symbol maps (Ghidra-derived), the binding overlay (reference call targets, reloc-v7), the ICF table, the sized-delete rule.
- data-v3 literals: every data byte not produced by our objects is the reference's bytes (strings, tables, vtables of classes with no unit) plus the pointer-field list from the original .reloc; D_ labels at every address any object names.
- the import tables: names and DLLs come from the reference IAT (iat_spec.json).
- the recipe function addresses used as `C_<va>` names (units.json).
- symbol-choice table: duplicates are not yet resolved; the intended rule is "the unit that build-v7 places owns the address" (units.json function list), recorded per address in `symaddr.json`/units.json.

# Update (same day, second pass): steps 1-4 of the approved plan
Pipeline now: `dump_secmap.py` (data-v1 placement of every (unit, section) piece -> secmap.json, 39,893 of 79,339 data sections placed) -> `prep3.py` (replaces prep_objs.py) -> `prep_contribs.py` -> data-v3 gen with
`DV3_CNAMES=1` (+ optional `DV3_SKIP` = ranges zeroed because our objects supply them) -> `mk_alias.py` (/ALTERNATENAME C_<va>=lib symbol) -> `mk_rsp.py` -> `link1.cmd` -> `loganalyze.py`.
prep3: recipe functions -> C_<va>; 99,144 unplaced code COMDATs and all `.sxdata` removed; data sections that data-v1 placed, and data sections not reachable from kept code/EH, are removed (64,014 sections) and every reference is
redirected to an appended undefined `D_<va>` (placed pieces at their placed address; defined data symbols with a verified address, 1,011); the symbol table is compacted (this linker reports unreferenced undefined externals; weak-external tags renumbered).

| step | LNK2005 | LNK2001 | LNK2019 | distinct unresolved names |
|---|---:|---:|---:|---:|
| raw objects | 5,714 | 31,547 | 15,407 | 38,812 |
| addresses + unplaced code removed | 4,747 | 86,608 | 1,785 | 32,535 + 4,556 dup |
| + placed data removed/redirected, unreachable COMDAT data removed, compacted symbols | 72 | 19,318 | 1,259 | 18,991 |
| + /ALTERNATENAME for CRT addresses (67 aliases) | 72 | 18,404 | 1,193 | 18,300 |
| + data-v3 without produced EH-table ranges (6,720 pieces zeroed) | 124 | 17,784 | 3,229 | 19,939 |

Remaining causes (last link, distinct names, by referencing object kind):
- 10,933 `C_<va>` code addresses referenced from data-v3 pointer fields (11,057 before the EH skip): the captured data points at original funclets/handlers/thunks that our objects only provide as compiler-generated `.text$x` COMDATs under local names;
  fix = rename those funclet symbols to `C_<va>` using data-v1/phase0's EH piece placement (section index -> original address), or drop the captured tables they sit in (the unproduced EH tables are not in the produced ranges, which is why the skip only removed 876).
- 5,377 deleting-destructor names `??_G/??_E<class>` and 980 dtor / 267 ctor names: referenced from kept data sections (vtables/RTTI of classes data-v1 could not place: names differ) and from compiler EH funclets (`.text$x`: 1,227 refs, destructor calls whose per-site
  target comes only from the overlay's by-field/by-unit table). Fix = give each kept vtable its original address (needs M3 class names or the reference-derived vtable list) and rebind funclet calls per site (reloc-level rewriting using the build's field log).
- 1,958 `D_<va>` labels not emitted (label would fall inside a pointer field or inside a zeroed skip range): emit as `EQU`/second label scheme.
- 132 other names, 125 C_ (CRT/EH region), 71 imports (more SDK libs or def entries), 24 address-named.
- 124 duplicate definitions: 72 data/globals defined in several units (rule: one defining unit per address; not applied), + 52 created by the EH skip.
Not done yet: steps 5-7 (resources, TLS, /FIXED:NO check, harness). No exe exists, so the harness was not run. All reference-derived inputs listed in the first section still apply (addresses by symaddr.json, captured data-v3 bytes, IAT names).

# Update 3 (after the usage-limit pause): rebuild confirmed, unblock list items 1-6 progress
Rebuild (clean, under the lock helper `lockrun.py`): filled_equals_reference true, coverage 100.000% (10,843,747 / 10,843,747 non-padding bytes), borrowed 0, rebase 0, inferred literals 0, `_emit` lines 0, nothing lost.
New hooks (env FNV_DUMP_SYMADDR=1): `fieldaddr.json` (unit -> field va -> resolved base address, per-site binding), `crt_defaddr.json` (libcmt/libcpmt function name -> address of the matched copy). Backups: assemble_v7.py.bak2-20261116-wB, crt5.py.bak2-20261116-wB.
Done since update 2 (link counts in the last column are of the final link of this round):
- EH pieces: 15,765 funclet/handler symbols of chosen (unit, section) pieces renamed to `C_<va>` (eh_pieces.py = data-v1 phase0's piece placement; one defining (unit, section) per address, recipe functions win) -> data-v3 `C_` unresolved 10,933 -> 533.
- Per-site binding at relocation level (coffrw.rebuild relnames): 387 funclet/function relocations bound to the address of their own field (fieldaddr.json).
- `.xdata` EH tables and unreferenced `.text$x` funclets are dropped when the stub's FuncInfo reference can be redirected to a placed address; weak externals (the `??_E`->`??_G` aliases) are dropped when unreferenced (cleared 5,377 ??_G/??_E names).
- `dedupe.py`: one defining object per data global (57 duplicated globals, 10 sections dropped, 6 mixed sections remain = 52 LNK2005).
- Function ownership follows the build (first unit that lists the address).
- 105 CRT `C_` addresses aliased to libcmt/libcpmt symbols (mk_alias.py now also reads crt_defaddr.json).
- Import libs regenerated (symaddr-based IAT slot mapping): unresolved `__imp_` names 77 -> 61.

| link | LNK2005 | LNK2001 | LNK2019 |
|---|---:|---:|---:|
| end of update 2 | 124 | 17,784 | 3,229 |
| EH piece symbols -> C_<va>, weak externals dropped, ownership | 52 | 1,375 | 1,154 |
| xdata/funclet pruning, per-site binding, CRT aliases, imports | 52 | 1,736 | 848 |
Remaining distinct unresolved (cats_last.txt): 559 destructor calls inside compiler funclets of functions whose EH tables are not placed (EH matching failed there, so there is neither an address for the funclet call nor a captured table to use),
533 data-v3 `C_` addresses (CRT/lib code of libcmt/libcpmt not matched to a lib symbol, 568 before aliasing minus 105), 107 + 64 more `C_` in unit code/data, 96 other names (operator delete overloads `??3...` and similar with no address), 61 imports
(Bink/D3DX/Steam/vorbis names: `lib /def` mis-forms the symbol or import name for decorated/cdecl entries; fix = write the short-import archive members directly: NAME_NOPREFIX / NAME_UNDECORATE / exact-name types), 18+15+17 misc.
Not done: item 3 (vtables with known original addresses beyond what the redirect already does: the `??_G/??_E` names are gone from the error list), item 4 (second-label scheme for D_ labels inside fields/skip ranges: the missing-D_ count is 0 in this link), resources and TLS, /FIXED:NO check, harness (no exe).

# Update 4: items (1)-(4) of the 2026-11-16 afternoon list
- (1) Imports: `mkimp.py` writes the short-import archive members directly (symbol = exact import name, NAME type, thunk + `__imp_` symbols, first linker member; member names truncated to 15 chars + `/`),
  plus `/ALTERNATENAME:__imp_<referenced decoration>=__imp_<import name>` (opts_imp.txt, 2 per differently decorated name). Result: 0 unresolved `__imp_` names (was 61); lib.exe /def mis-forms the symbol (extra `_`) or the import name for decorated/cdecl entries.
  Caveat: binkw32 exports are decorated names (`_BinkOpen@8`); members are by exact name, which is what the DLL exports.
- (2) Duplicates: `dedupe.py` additionally turns a duplicated global that sits in a mixed section into an undefined reference to the owner's definition (its bytes stay as dead padding in the non-owner's section): LNK2005 52 -> 0 (18 appear again with the CRT objects, see (3)).
- (3) CRT: `crt_place.json` (new dump of crt5's matched libcmt/libcpmt sections and their original addresses, FNV_DUMP_SYMADDR=1, backup crt5.py.bak3-20261116-wB) -> `mkcrt.py` extracts the 312 matched members from the libraries and adds alias symbols `C_<va>`/`D_<va>` at every symbol offset
  of the matched sections (1,005 aliases, statics included; all original external names are kept, so the library copy is never pulled in a second time); 15 more `.text$x` sections of those members were located by masked byte matching. data-v3: lib-produced ranges (755 pieces) are zeroed (`DV3_SKIP`),
  and 456 pointer fields whose target is CRT-region code no linked object defines are emitted as zero (`DV3_DROPT`; they sit in dead captured CRT EH tables, the library supplies its own). Contribution functions under other names are now `C_<addr>` too (+102).
- (4) EH stubs: 2,169 `__ehhandler$` stubs now load the ORIGINAL FuncInfo (`D_<va>` read from the original stub bytes at the address the build resolved for the handler); our own xdata/funclets behind them become unreachable and are dropped.
Link now: LNK2005 18, LNK2001 305, LNK2019 702 (cats_last.txt). Remaining: 559 dtor calls inside `.text$x` packs: a compiler funclet pack is one COMDAT that holds both located (chosen, `C_`) and unlocated funclets; the unlocated ones keep unresolved generic dtor names although nothing references them
(fix = split the pack at funclet boundaries or neutralise unreferenced funclets); 96 other names (operator delete overloads etc.); 18 `C_`; 17 address-named; 7 ctor; 18 dtor in data.
Not reached: resources/TLS, /FIXED:NO check, harness. No exe exists; no game instance was started.

# Update 5: pack splitting, revival, contribution binding, import descriptors (2026-11-16 evening)
Link now (no /FORCE): **LNK2005 0, LNK2001 9, LNK2019 19 = 28 references to 21 distinct names, LNK1120 "28 unresolved externals"** (was 18 / 305 / 702 at the end of Update 4). No exe is produced yet.
- (a) `coffrw.split_packs`: a `.text$x` COMDAT pack is split at symbol offsets into one COMDAT per piece (section symbol + its own symbols re-ordered together, relocation indexes renumbered; old pack header removed). 7,441 packs split. The reachability roots in `prep3` no longer include `.text$x` pieces without a `C_` leader (that was why the unlocated funclets were never dropped); unlocated funclets and their xdata are now dropped when unreferenced: dtor LNK2019 658 -> 88 -> 0.
- Revival (prep3 `revive` loop, max 8 passes): kept code that still names a removed unplaced COMDAT with no address keeps that COMDAT (real compiled code); also `revive_names.json` (names still unresolved after a link) revives their defining COMDATs in any object.
- Per-site binding is extended: relocation targets that are defined in a removed section count as unbound; funclet/function sections with several `C_` symbols compute the field address from the nearest preceding `C_` symbol (`cpos`); fields where `fieldaddr` has nothing are decoded from the reference bytes ONLY when the section is a byte-identical function (rel32/abs32 at the field VA); undefined names with an embedded address (`FUN_/DAT_/SUB_..._<8hex>`, now also for units) map to that address.
- Contributions (`prep_contribs.py`): names resolved from recipe symbols/fold aliases (units.json, 43); defined data (vtables with RTTI, statics) bound to the placed `D_<va>` and our copy dropped (280 sections; vtable address from `??_7..._<8hex>@@6B@`, `g_<8hex>`); the function that gets `C_<addr>` is the code section whose masked bytes equal the reference at that address (103 cases; before, the first symbol was picked, e.g. a `.text$yc` initializer); per-site binding by reference field for contribution code sections located by masked unique match (+ reloc-target consistency).
- `label_alias.py`: undefined `C_<va>` inside a function another object defines (SUB_ jump labels) become alias symbols in the defining object (bounded by recipe/piece size).
- Imports (`mkimp.py`): lib.exe-built stub libs supply the three import-descriptor objects per DLL (short-import members alone left `__IMPORT_DESCRIPTOR_<dll>` unresolved for d3dx9/steam_api/bink/vorbis/dsound/dinput8); ordinal imports (WSOCK32: accept, bind, inet_ntoa, listen, ntohs, setsockopt, gethostname, WSAStartup; XINPUT1_3 ordinal 2) written as ordinal short-import members; 33 import call thunks (`C_<va>` = `jmp [IAT slot]`) bound by `/ALTERNATENAME` to the import name. The first-linker-member offsets are now per symbol.
- CRT: `mkcrt.py` skips aliases already defined by our objects and across members (LNK2005 18 -> 0); `mkcrt2.py` finds unplaced libcmt/libcpmt code sections by masked content match (memmove copies, 14 aliases; run after a link, re-run `mk_rsp.py`). `mkthunks.py` emits `jmp [D_abs]` assembler thunks for code targets nobody defines whose original bytes are a bare indirect jump (1: C_009febd8). `/ALTERNATENAME:_WinMain@16=C_0086a850` (opts_extra.txt; address = the call target in the original wincrt0 startup).
- `resources.obj` (copy of direct-v1\build\resources.obj, read only) is on the link line. `/FIXED:NO` was already set.
- `regen_locked.cmd` = the steps that read build products (prep3, prep_contribs, label_alias, data-v3 gen, ml) - run through `lockrun.py` (build.lock); everything else (dedupe, mkimp, mkcrt*, mk_rsp, link1) needs no lock.
Remaining 21 names (all need a source/identity decision, none can be bound without a guess): 11 class-specific `operator delete(void*)` / `(void*,uint)` and dtors called from compiler funclets whose pieces are not byte-identical to the original (call field offsets differ, so the original call target cannot be read by offset; the original calls FUN_00aa1460-family functions): ExtraData/NiAVObject/Item/Shape80F/TESObjectDoorController/BSFadeNode/BSFaceGenMorphData, GuardBase04/FUN_00aa8ca0_cls dtors; 9 `Setting*`/`ResetSetting`/`FUN_0045cf30`/`SettingT_GameSettingCollection_` constructors called from contribution `.text$yc` dynamic initializers (identical initializer shapes: ambiguous by content, so no original address); `xA::a0 / xB::b0` (test classes in units 541/545/2788), 2 data (`g_target_00d53c90`, `g_target_00cc74d0`, `g_fnv_00e9ecc0_value_anchor` are pseudo-symbols with no original), 2 TLS (`tlsArr`, `g_debugTextTls`: need SECREL/.tls mapping), `__imp__FreeBlockImp@4` and `__imp_?Free@BoneRecordArray@..` (dllimport declarations with no IAT slot), `operator delete(void*,AllocationManager&)`, `DAT_0150e828`.
Still reference-derived inputs (to retire later): symaddr.json/fieldaddr.json (addresses the build resolved from units.json maps, overlay, ICF); data-v3 captured literals and pointer-field locations (symbolic.json); data-v1 `secmap.json` placement; FuncInfo addresses read from the original `__ehhandler$` stub bytes (EH stub redirect, 2,170); EH piece placement (eh_pieces.json) and per-site field decode from reference bytes (prep3 'reference field decode' 30, contributions); IAT names/DLLs (iat_spec.json) and ordinals; CRT member placement (crt_place.json, mkcrt2 content match); DV3_SKIP/DV3_DROPT (zeroed or dropped CRT pointer fields); WinMain target; the reference-located thunks.
Not reached: TLS template, base-reloc check, harness (no exe). No game instance was started. Backups: `*.bak-20261116-wB*` next to each edited script (prep3, prep_contribs, mkcrt, mkimp, mk_rsp).

# Update 6: first linked exe (2026-11-16 late)
**`link-v2\FalloutNV_linked.exe` links (link.exe exit 0, no /FORCE, no absolute-address fallback)**: 15.8 MB, `/FIXED:NO` with a base-reloc directory (0xB95B4 bytes), import table (14 DLLs incl. WSOCK32/XINPUT1_3 by ordinal), resources (`resources.obj` from direct-v1\build, read only), TLS directory (`.tls` 0x405 bytes, `_tls_used` from libcmt). Only warning: LNK4078 (extra `.text` section from the ml-built objects). Unresolved: 222 -> 0.
Changes since Update 5 (all backed up as `*.bak*-20261116-wB`):
- Contributions: their by-product `.text$yc/.text$yd/.CRT$XC*` (duplicate dynamic initializers) and unreachable by-product COMDAT code (deleting dtors) are dropped (the original initializers live in other units / the original table); this removed the 9 Setting/FUN_0045cf30 constructor references without defining any ctor.
- `supp\supp.cpp` + `mk_supp.py`: real forwarding `operator delete` functions (7 classes + `(void*,AllocationManager&)`) compiled with the VC2008 cl, forwarding to FUN_00aa1460 like the original funclets (checked in the original bytes: every funclet calls 0xaa1460). `supp\supp_data.asm`: absolute symbols `g_target_00d53c90`=0x65, `g_target_00cc74d0`=0x14, `g_fnv_00e9ecc0_value_anchor`=0 (the original functions are `mov eax, imm; ret`, the source takes `&sym`), `DAT_0150e828` as a 1-byte variable (original address beyond the image).
- Dtors: `/ALTERNATENAME:??1GuardBase04@@QAE@XZ=C_00ca0c30` and `??1FUN_00aa8ca0_cls=C_00aa8da0` (the real functions the original funclets jump to, read from the original EH funclets); the Setting dtor reference came from a dropped by-product.
- TLS: `?tlsArr@@3PAIA` = D_01272000 and `?g_debugTextTls...` = D_01272268 (both live in data-v3's TLS template, checked against the SECREL offsets in the original code); data-v3's `_TLS` segment is renamed `.tls$AAA` by `fix_sections.py` (after ml), `_CONSTPE` merged into `.rdata`.
- dllimport-declared data cells (`__imp__FreeBlockImp@4`, `__imp_?Free@BoneRecordArray...`): not IAT slots (the original code does `call [data cell]`), so they are bound to their D_ data address instead of being turned into imports; the declarations were NOT changed (changing them would change the call encoding and break byte matching).
- prep3: multi-symbol vtable sections (value != 0 symbols) are redirected to D_; static symbols of removed sections bound by address; `.text$yc/yd` stay removed.
- `mk_xcu.py`: the sources bind the C++ static-initializer table to original data (only 17 objects carry `.CRT$XCU`); the original table [0x00fdf4a4, 0x010113c0) (51,143 slots, 17,728 initializers) is emitted as a real `.CRT$XCU` section of `dd C_<va>` between libcmt's `__xc_a/__xc_z`, and zeroed in data-v3 (skip_ranges.json). `alias_apply.py` renames C_ references to libcmt/libcpmt symbols directly (ALTERNATENAME alone resolved some to 0); `/INCLUDE:` for every alias target.
- Tools: `dbgrun.py` (minimal debug loop: first access violation, registers, ebp chain, stack), `where.py` (map lookup + disassembly), `regen_locked.cmd` / `regen_data.cmd` (steps that need build.lock).
**Harness / run status**: `harness.py <exe> --play 120 --tag linkv2_1` -> FAIL "exited during startup code=0xc0000005" (no menu). Under dbgrun the process now gets through CRT init and 17,000+ initializers (esi walks the XC table) and faults inside initializer #~25-35 of the table (C_00fb66a0 -> C_00aa3880 -> C_00aa3cc0 -> C_00aa3e40, a virtual call `[obj->vtbl+8]` on an element found in a container whose data was not initialised as in the original run: the original data-v3 contents do not include the runtime state the original CRT/earlier code had set before this point). Next steps: (1) compare the order/contents of the XC table prefix with the original (xi table functions, `__initterm` of `__xi_a..__xi_z` run first); (2) check that D_ pointer fields into the C_ initializer area are reloc'd (base-reloc check) - done structurally (directory present), not yet diffed against ownreloc because the layout differs; (3) bisect by truncating the XC table.
Still reference-derived (additions to the earlier list): original XC table contents (mk_xcu), TLS offsets, supp constants (read from the original functions), alias names for dtors, `__imp_` data-cell addresses, reference field decode in prep3/prep_contribs.
Not done: base-reloc check against ownreloc, the 2-minute play, clean exit. No exe passes the harness yet.
