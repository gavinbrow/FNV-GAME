# FNV source-built runtime — current state

## Accepted checkpoint - 2026-11-21

Development is paused. The latest accepted checkpoint is the native227 batch,
recipe f173f5dea82f859fdf87944ef72b851f769fce46a0dbc8de0eff8c25bc51aa23,
with 3,246 units and 5,749 source/include files. It adds 227 native RTTI
descriptors (7,942 bytes replacing existing placeholders), retaining the earlier
430 native runtime type records and 27 NiMemObject declaration corrections.
Initialized compiled-data coverage is 1,614,032 / 1,979,392 bytes (81.5%).

Five fresh serialized positive/control/repeat runs passed the expected image,
relocation, mutation, frozen-input and clean gameplay gates. See
`m3/phase2/NON-AI-NATIVE227-20261120.md` for the accepted result. Private candidate
proofs for additional source types and 123 descriptors are not installed.
Whole Phase 2 remains open. No new hard game-function bodies were reconstructed
in this batch. The remaining initialized-data partition includes 190,698 bytes
that already compile but remain unplaced.

The older dated material below is historical and does not override this
checkpoint. Detailed build products and private evidence remain local.

Last updated 2026-11-19. Start with `../TODO.md`, `BUILD-ALL.md` and `m3/phase2/PROGRESS.md` for the current verified gate and evidence. Historical Phase 1 evidence is in `m3/BATCH8-verification.md`. The 2026-11-15 progress material below is retained as history; standing privacy and workspace limits remain in force.

## Verified current results

The latest accepted default is `m3/out/phase2-native-source-repeat`, recipe
`825d444f...2d68`: 1,613,018 initialized data bytes (81.5%), 8,268 M3 entries,
15,842 DV1 pieces and 405 library pieces. Both no-overrides positive/repeat
runs, two fresh controls, exact image/relocations and semantic gameplay pass.
Actual seven-object archives independently pass 1,100 functions, 389 ordinary
EH sections and eight requested tails. The native BGSBodyPart table adds eight
bytes. PSA weak E and whole native-class recovery remain open.

The preceding next-data default at `m3/out/phase2-next-data-default-verified`
retains its three-control/default verification. Selection `a0a8...9c3a`,
library `74e3...9700` and automatic Cost watch are unchanged. Earlier source
6757 and d569 archives remain historical evidence. The next private NiMem
kind/API cohort uses 133 fresh pairs and 618 pinned reused units.

| Area | Current evidence |
|---|---|
| Code | 100% of non-padding `.text` compiled from source; zero undecompiled bytes, borrowed instruction-field bytes and instruction bytes copied from the reference. |
| M3 current bounded Phase 2 batch | 8,268 selected definitions, zero drops; initialized `.data`/`.rdata` object coverage 1,613,018 / 1,979,392 bytes (81.5%). Most of the original 849 KB of W scaffolding and opaque/prefix identities remain tracked. Whole native-class recovery is open. |
| Image | Final positive SHA-256 `c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f`; exact 734,884-byte relocation directory matches the fresh baseline. |
| Controls and gameplay | Fresh array-value and tail-pointer controls fail round trip and change actual hashes. Positive/repeat semantic runs pass at 70.1/70.0 seconds; repeat proves a new save, cells 1291213 -> 1073541 -> 1291213 and native exit 0. The preceding data batch retains its separate library-value proof. Earlier failures remain archived. |
| Default | `m3/out/phase2-native-source-repeat` passes with all M3/DV/weak overrides cleared. Defaults: `FNV_M3=1`, `FNV_M3_SEL=phase2/selection.json`, `FNV_M3_DV1=1`, `FNV_M3_DV1_EXT=1`, pinned `phase2/library_candidates.json` overlay; use `FNV_M3=0` for the legacy route or `FNV_M3_LIB=0` to omit library overlays. |
| Real-link experiment | Later `link-v2/NOTES.md` records zero unresolved symbols and 17,728 completed startup routines, followed by a crash inside steamclient.dll after reaching WinMain. This is separate from the passing layout-builder executable. |

Use `build-all.cmd --out <folder> --require-harness` for the coordinated build and test entry point. The Phase 1 acceptance milestone is closed with explicit deferrals; this does not claim all original globals/types are resolved. The accepted selection digest, exact remaining-byte partition, source-type limits, BSS and later-phase deferrals are in `m3/DESIGN-phase1.md` and `m3/BATCH8-deferrals.md`. The user authorized Phase 2 generator-backed work on 2026-11-18; keep the original matching gates.

The first Phase 2/W-typing experiment replaces 22 W entries (114 bytes) with source-declared scalar identities. Its later combined batch now passes the positive, three mutation controls, clean repeat, fresh no-overrides default and strict saved-result checks, and is promoted. Earlier experiment evidence is in `m3/phase2/RESULTS.md`.

The active Phase 2 continuation has installed a generator-backed TESContainer
header/override pilot for verification, including source-derived production
literal-label corrections. The actual fresh combined-v3 image is canonical with
exact relocation bytes; gameplay, three targeted controls and the clean repeat
all pass, including semantic cell restoration and clean exit. Strict saved-run
checks include all three controls. Accepted coverage is 1,602,654 initialized bytes, with 12 typed arrays
and 370 library pieces. The coordinator independently reviewed actual default
image/relocation bytes, scratch hashes and all 31 TESContainer functions. Failed
combined attempts are archived. See `m3/phase2/PROGRESS.md` and
`m3/phase2/COMPLETION.md` for the current source state and remaining whole-phase
requirements. No global class-recovery or whole-phase completion claim is made.

## Historical 2026-11-15 snapshot

The following figures, blockers, staged queue statements and rebuild commands describe that earlier state. They do not override the current results or entry point above.

## Where it stands

| Stage | State |
|---|---|
| 1. Game code from our compile | **98.92%** of non-padding `.text` (10,727,172 of 10,843,747 bytes), measured on `build-v4/FalloutNV_v4_strict.exe`. All 2,988 units compile; all 68,657 recipe functions are placed. |
| 2. Addresses resolved by our own build | About 98.4%: 512,341 relocation fields resolved; 8,152 (32,608 bytes) still borrowed from the reference, including 2,287 in C runtime code |
| 3. Rebase test (build at 0x10000000 vs reference rebased with its own `.reloc`) | 284 bytes differ in `.text`, all inside our produced code: about 1,141 absolute fields we produce that the original's table does not list (1,087 point outside the image) and some fields it lists that we don't. Not yet traced. |
| 4. Free layout (functions moved) | Not started |
| 5. Start a moved-layout build | Blocked: the entry point is the Steam wrapper. The only tested launch path is the in-memory overlay, which needs original addresses. |

**Update 2026-11-15 (later):**
- `contrib-v5/` adds the 625 web matches accepted by the MCP local targets.
  - Code from our compile: 99.14% (10,750,176 bytes). Undecompiled: 66,222 bytes.
  - 263 web targets are left, totalling 51,794 bytes.
  - Re-run with `contrib-v5\rerun.cmd`.
- `reloc-v5/` has the linking fixes. See `reloc-v5/NOTES.md`.
  - Borrowed fields: 8,020 → 4,877.
  - Rebase: 122 bytes differ on our own rules.
  - The 48 wrong-copy calls are source naming errors; `callee_fixups.json` lists them.
- The two assemblers have since been merged: see `build-v6/`.
  - Build-v6 results: 99.22% (10,759,145 bytes), 65,443 undecompiled, 4,878 borrowed fields, 629 web matches.
  - Rerun with `build-v6\rebuild.cmd` (about 80 s). This is now the current build.
- **Current build is `build-v7/`.** It replaces v6.
  - Coverage is 99.54% (10,793,638 bytes) and 27,239 bytes are undecompiled.
  - It handles flags and entry overrides and exception-handler pieces in web matches, and folds identical functions (ICF).
  - Rerun with `build-v7\rebuild.cmd` (about 3 min).
- `data-v1/` produces 30.1% of `.rdata`/`.data` from our objects: 580 KB of `.rdata` (34%) and 15 KB of `.data`.
  - 12,945 of the 101,449 data->code pointers come from our objects and agree with the reference. Our objects can supply at most 35.5% of them.
  - Most of those agreements are EH entries located through reference addresses.
  - 6,471 type descriptors don't match because our class names differ from the original's.
  - Rerun with `data-v1\rebuild.cmd`. Read `data-v1/NOTES.md` before using these figures.
- 181 new web targets (4,313 B of small static-init stubs) are staged in `FNV/scripts/staged-new-targets/`. They are not yet applied; `apply-additions.py` applies them.
  - The failing EH pieces are listed by owning function in `b-failed-eh-by-owner.json`.
- `layout-v1/` holds the static moved-layout prototype. All four layouts map back with 0 mismatches. Every pointer from data into code still depends on the original `.reloc`. See `layout-v1/NOTES.md` for the blocker list.
- The staged MCP server went live at 2026-11-15 19:00 UTC.
  - Eleven claimed targets keep their old catalog span. Run `FNV/scripts/staged-20261115/apply-deferred.py` once those claims end.
- Staged MCP server fixes (now live, see above) are in `FNV/scripts/staged-20261115/` (see `APPLY.md` sections 1-7). They are not yet live.
  - Security fixes.
  - Checker fixes for web-agent give-ups: EH-tail compare, `??__E`/`??__F` entries, `/Ob1` and `/hotpatch` flags, corrected `catalog.json` (892 targets) and 263 refreshed contexts.
  - Analysis found 173 of the 259 open targets were blocked by the checker, not by difficulty.

The runnable build (`build-v4/FalloutNV_v4_filled.exe`) equals the reference byte-for-byte. The overlay start test passed on the v1 build (60 s idle at the menu, `overlay-test/`).

The name-by-name LINK route is dropped: `link-triage/` shows it cannot converge. Don't feed the web queue for it.

## What is still missing (98,100 bytes plus borrowed fields)

| Gap | Bytes | What closes it |
|---|---|---|
| Undecompiled code (no recipe entry) | 90,080 | Write source. Largest is about 29 KB at 0x00f79710 (input-action table setup), plus static initializers at 0x00fda000 and 0x00fdcc30. This is the one area web agents could help with, since it is new source. |
| Failed exception-handler pieces | 7,813 | Pieces outside the recipe whose bytes don't match. Direct sized-delete fixes renumber `$SG` string labels in actor/highprocess/playercharacter/magicprojectile, so they need another approach. |
| Other | 207 | |

## Toolchains (all extracted from original Microsoft media, no system install)

| Compiler | Version | Folder | Env var |
|---|---|---|---|
| VC++ 2008 SP1 | 15.00.30729.01 | `FNV/tools/vc2008` | `FNV_MSVC9_ROOT` (optional; default) |
| VC++ 2008 RTM | 15.00.21022.08 | `FNV/tools/vc2008rtm` (script `FNV/scripts/install-toolchain-rtm.ps1`, from the Express disc) | `FNV_MSVC9_RTM_ROOT` (pass it to the process; it is not set persistently) |
| VC++ 2005 SP1 | 14.00.50727.762 | `FNV/tools/vc8sp1` (`msiexec /a` of the Vista SDK disc's `WinSDKCompiler-x86.msi` + `WinSDKBuild-x86.msi`) | `FNV_MSVC8_ROOT` (set at user level) |

The Vista SDK's full installer fails on Windows 11 at FxCop; don't use it.

## How to rebuild

```
set FNV_MSVC9_RTM_ROOT=C:\path\to\Decompilation\FNV\tools\vc2008rtm
python -I runtime-next/pinned-build/compile_units_v3.py 28     (about 30 s)
python -I runtime-next/build-v4/assemble_v4.py                 (about 30 s)
```

Results go to `build-v4/progress.json`. Source fixes are uncommitted in `fnv_decomp`; see `pinned-build/logs/src_fixes_v3.diff` (14 files).

Reference image: `FNV/work/worker1/FalloutNV.runtime-text.exe`. The installed Steam exe has encrypted code and is not a usable reference.

## Known weaknesses

- Most relocation targets come from the project's own symbol map, built to make the matcher pass, so agreement and the rebase test are partly circular.
- 48 calls resolve to a different copy of a function than the original used; cause unknown.
- Strict images keep non-`.text` sections (data, imports, resources) from the reference. Data is not from source at all.

## Standing limits

- Never send game binaries, disassembly or build data to web workers. Never print key files.
- Do not recursively scan `FNV/work`, `FNV/local` or `fnv_decomp/build/rebuild` (disk contention).
- Never bypass or strip the Steam wrapper.
- The local queue dispatcher and 15 unreviewed web submissions were left untouched.
