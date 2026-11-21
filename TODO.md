# TODO

## Current checkpoint - 2026-11-21

Development is paused. See [docs/STATUS.md](docs/STATUS.md) for the accepted
checkpoint, validation and remaining work. The older checklist below is
historical and does not override this section.

- [x] Finish Phase 1 with explicit deferred ranges and promote the verified default.
- [x] Accept 430 native runtime type records and 227 additional native RTTI descriptors.
- [x] Reach 1,614,032 / 1,979,392 initialized data bytes from compiled objects.
- [ ] Compose and verify the private Settings/Havok/type/string/allocation candidates.
- [ ] Finish integration and verification of 123 additional descriptor candidates.
- [ ] Resolve remaining class layouts, inheritance, virtual tables and global ownership.
- [ ] Place 190,698 bytes that already compile but remain outside the image.
- [ ] Finish later startup/exception work and fix the ordinary-linker Steam startup crash.

## Historical checklist through 2026-11-17

Plan and background: [PLAN-M3.md](PLAN-M3.md). Newest entries at the top of "Done".

## Now: M3 phase 1 (globals)

- [x] Inventory all `DAT_` globals -> `runtime-next/m3/inventory/dat_globals.json` (Haiku). 15,333 addresses,
      101,320 refs: `.data` 9,644, `.rdata` 5,603, `.text` 74 (jump/data in code), other 12. 7,710 are BSS
      (no file bytes; definitions only), 7,623 initialised. 12,379 have one declared type, 2,404 several, 550 none.
- [x] Design source-global placement -> `runtime-next/m3/DESIGN-phase1.md` (Sonnet). Finding: every data byte in
      the exe currently comes from the data-v3 dump; data-v1's "ours" figure was a counter only. Phase 1 adds a
      real splice in `make_image.py` behind `FNV_M3=1`.
- [x] Opt-in pipeline change: `runtime-next/m3/gen_m3.py`, `splice.py`, `m3secs.py`; hooks in build_all,
      data-v1 place/report, data-v3 verify, layout-v2 make_image/snapshot (backups `*.bak-m3p1`). Also fixed:
      data-v3 verify now exits 1 on round-trip failure.
- [x] Pilot batch 2026-11-16: 150 globals, 648 bytes (`.data` 504, `.rdata` 144) now come from our compiled
      `m3_data.obj`. Default and `FNV_M3=1` builds both sha256 c267a197...; negative control 26163165... (differs,
      as it must); harness PASS (menu, load, 69 s play, cell change, quicksave/load, exit). Builds in `runtime-next/m3/out/`.
- [x] Batch 2 2026-11-16: 682 globals, 2,405 bytes (`.data` 991, `.rdata` 1,414), `FNV_M3_SEL=batch2_selection.json`.
      sha256 c267a197... with and without; negative control differs; harness PASS. That uses up the plain
      scalars: the rest are pointers (4,816 rejected by type, 1,513 hold pointer fields), tables or BSS.
- [x] Batch 3 2026-11-16: +114 single-pointer globals (47 to code, 67 to data), so 796 globals, 2,861 bytes,
      114 relocations now from our object (`FNV_M3_SEL=batch3_selection.json`). Relocation support added to
      gen_m3/splice/m3secs/place/verify/make_image; data-v3 gen.py keeps skipped fields as "ghost" zero fields
      under `DV_M3` so chunk layout doesn't shift. sha256 c267a197... with and without; pointer negative control
      differs; harness PASS; `.reloc` identical (351,931 sites).
- [x] Batch 4 2026-11-16: +1,152 globals (68 arrays, 487 strings, 594 pointer tables, 3 mixed tables), so
      1,948 globals, 145,024 bytes (`.data` 12,558, `.rdata` 132,466) and 19,192 relocations from our object
      (`FNV_M3_SEL=batch4_selection.json`). sha256 c267a197... with and without; value and pointer negative
      controls differ; harness PASS.
- [x] Batch 5 2026-11-16: spliced 14,735 pieces of our compiled units into the exe (`FNV_M3_DV1=1`, new
      `m3/dv1_splice.py`): 524,598 bytes, 19,945 relocations (strings 195 KB, EH tables 254 KB, RTTI 44 KB,
      other rdata 26 KB, floats 4 KB, vtables 1 KB). sha256 c267a197... in staged and full builds; byte and
      reloc negative controls differ; harness PASS.
      **Initialised `.data`+`.rdata` now from our objects in the exe: 669,617 of 1,979,392 bytes (33.8%)**,
      up from 0 at the start of phase 1. Still from the dump: 1,309,775 (849,336 non-zero).
- [x] Batch 6 2026-11-16 (`FNV_M3_DV1_EXT=1`): +700 pieces (rtti2 arrays placed by verified link, unlocking
      rtti3), +8,694 bytes. Now 678,311 of 1,979,392 bytes (34.3%) from our objects. sha256 c267a197...;
      negative controls differ; harness PASS. Remaining skips need source changes (phase 2): RTTI with
      synthetic class names (~150 KB), vtable slots for undefined methods / `__purecall` (41 KB), vtable slots
      bound to base methods instead of overrides (31 KB).
- [x] Batch 7 2026-11-17: +6,251 objects, 881,352 bytes, 71,336 relocations (`FNV_M3_SEL=batch7_selection.json`,
      `m3/b7_select.py`, objects split over `m3_data_1..3.obj` for the 65,535-reloc limit). sha256 c267a197...;
      negative controls differ; harness PASS.
      - 32 KB: globals declared inside namespaces (real source names).
      - 849 KB: **auto-typed "W" objects** for bytes that no source declaration covers (tails after globals and
        after unit pieces). Typed only from the reference's own bytes and reloc sites (pointers, floats,
        strings, byte runs). The compiler now produces them, but they're scaffolding: named by address, no
        real type yet.
- **Phase 1 status (2026-11-17):** initialised `.data`+`.rdata` from our objects in the exe: 1,559,663 of
  1,979,392 bytes (78.8%). Of that: 710 KB from source-declared globals or compiled units (35.9%), 849 KB
  auto-typed scaffolding (42.9%). Still from the dump: 97 KB non-zero (other name forms `PTR_`/`OFF_` 33 KB,
  multi-type 38 KB, non-scalar types 19 KB, rewritten directories 6 KB) + 115 KB zeros. Plus 208 KB of unit
  data that compiles but can't be spliced until phase 2 fixes RTTI names and vtables.
- [ ] Batch 8: `PTR_`/`OFF_`/`_DAT_` names (33 KB), multi-type (38 KB), non-scalar types (19 KB)
- [ ] Make the `FNV_M3*` path the default build once it has run cleanly for a while
- [ ] Give the 849 KB of "W" scaffolding real types (ongoing, alongside phase 2)
- [ ] `.bss` definitions (7,171 names; no file bytes)
- [ ] Give real types to ~1,600 "scalar-typed" globals that are really tables, 12 mixed structs, 271 with conflicting types
- [ ] File-resident zero globals and `.bss` definitions
- [ ] Widen: arrays, strings, floats, pointer tables, structs
- [ ] Make it the default once verified

## Later

- [ ] M3 phase 2: classes, vtables, RTTI
- [ ] M3 phase 3: CRT init lists, TLS, EH tables
- [ ] M3 phase 4: real link (link-v2), imports and .rc resources
- [ ] `publish_release.py`: replace the exe zip on the `game-data` release instead of making build-N releases
- [ ] Flaky harness exit-menu forced kill
- [ ] Rest of PR 42: parameter, field, global and class names (needs a symbol-aware rename tool)
- [ ] Linked (link-v2) exe crashes in steamclient.dll at `SteamUser()->vtbl[9]`
- [ ] Disk cleanup: `game-data-pack` (9.6 GB, uploaded) and `ci-test` (~1 GB), on confirmation
- [ ] Browser port (deferred): recompile the exe to WebAssembly + Windows/DirectX layer

## Done

- 2026-11-16 Imported 2,775 original function names from fnv_decomp PR 42 into the name map (FNV-GAME 8173a81)
- 2026-11-16 Credits for momusdigital/fnv_decomp; playable `game-data` release with all data
