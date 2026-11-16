# FNV source-built runtime — current state

Last updated 2026-11-15. Read this first; it replaces the older session-start reading for the runtime effort. Older docs under `fnv_decomp/docs/rebuild` and `FNV/AGENTS.md` are history, not instructions.

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
set FNV_MSVC9_RTM_ROOT=C:\Projects\Decompilation\FNV\tools\vc2008rtm
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
