# M3 plan: all exe data from source

Current status (2026-11-21): Phase 1 is accepted with explicit deferrals; Phase 2
is open and development is paused. The accepted checkpoint has 1,614,032 of
1,979,392 initialized data bytes from compiled objects. See
[docs/STATUS.md](docs/STATUS.md) and [TODO.md](TODO.md). The estimates and progress
figures below describe the original plan and its historical starting point.

Goal: every byte of `.rdata`, `.data`, `.tls` and `CONST` in `FalloutNV_selfbuilt.exe` is produced by compiling our
source (plus Microsoft's CRT/STL libraries), instead of being copied from the reference image. Values stay the
original's (that is what decompiled data is); what changes is that each piece becomes a typed definition in source
and every pointer in it becomes a real reference.

Live checklist: [TODO.md](TODO.md). Phase 1 design: [runtime-next/m3/DESIGN-phase1.md](runtime-next/m3/DESIGN-phase1.md).

## Starting point (build c267a197, 2026-11-16)

| Section | Size | From our build | Still copied |
|---|---|---|---|
| `.text` (code) | 12.44 MB | 100% of non-padding (10.84 MB) | 0 |
| `.rdata` | 1.72 MB | 654 KB (38.1%) | 1.06 MB (379 KB zeros) |
| `.data` (initialised part) | 263 KB | 23 KB (8.9%) | 239 KB (74 KB zeros) |
| `.tls` + `CONST` | 1.5 KB | 638 B | 898 B |
| `.rsrc` | 835 KB | rebuilt by us | images/version info from the install (stays that way) |
| imports, header constants | ~2 KB | tables rebuilt | names/order from the reference |

Correction found in phase 1 design: the "from our build" data figures above are data-v1 counters only. In the exe
itself every data byte currently comes from the data-v3 dump (reference values, with pointer fields re-linked
symbolically). Phase 1 adds the step that actually puts compiled bytes into the exe.

What the copied data is: ~122,000 pointer fields, RTTI for ~6,400 classes, ~5,400 vtables, 15,050 `DAT_` globals
with no source definition, ~157 KB strings, ~66 KB EH tables, 42 KB CRT init lists, float/lookup tables.

## Phases

| # | Phase | What | Estimate | Status |
|---|---|---|---|---|
| 1 | Globals | Turn the 15,050 `extern DAT_` declarations into real definitions (type from usage, value from the data-v3 dump), placed at their original address and counted as ours. Covers most strings, floats and tables too. | 2-3 weeks | **mostly done 2026-11-17** (opt-in `FNV_M3`): 78.8% of initialised data from our objects (35.9% source-declared or compiled units, 42.9% auto-typed scaffolding); ~97 KB non-zero left |
| 2 | Classes, vtables, RTTI | One header per class with virtuals in original order (original class names from fnv_decomp PR 42), so the compiler emits vtables and RTTI; constructors stop writing hard-coded vtable addresses. | 4-8 weeks | not started |
| 3 | Init lists, TLS, EH tables | Fall out of phases 1-2 (compiler-generated); check order and placement. | 1-2 weeks | not started |
| 4 | Real link | Link with link.exe from our objects only (link-v2 route: 1,025 link errors left, exe crashes in Steam API); imports from our declarations, resources from an .rc script. | 2-4 weeks | not started |
| 5 | Verify | After every batch: build byte-identical where expected, harness passes, "ours" counters rise. | ongoing | ongoing |

## Phase 1 approach

1. Inventory every `DAT_` address: declared types, users, section, initialised vs BSS, gap to the next symbol
   (`runtime-next/m3/inventory/`).
2. Design how a source definition is compiled, placed at its original VA, counted as ours, and replaces the
   matching range of the data-v3 dump, opt-in behind an env var so the default build is unaffected until verified.
3. Generator: emit definitions (type + initializer from the dump; pointer fields as references) into generated
   source under `runtime-next/m3/`.
4. Pilot: ~100-200 simple scalars in `.data` with one consistent type; then widen by kind (arrays, strings,
   floats, pointer tables, structs). Hard ones go to Sonnet agents in batches.
5. Each batch: full build byte-identical (sha256 c267a197...) and harness pass; record the counters in TODO.md.

## Rules

- Never modify `fnv_decomp/src`, `include` or `build/units.json` by hand outside the agreed generator outputs; the
  default build must stay byte-identical until a change is verified.
- New behaviour is opt-in (env var) until verified, then made default.
- Builds take `build.lock`; the harness takes `direct-v1/harness.lock`. One build at a time.
- Don't scan `FNV/work`, `FNV/local` or `fnv_decomp/build/rebuild` recursively.
- Agents: Haiku for simple extraction/structure work, Sonnet for design, generators and hard cases.
