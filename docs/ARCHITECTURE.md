# Architecture

A short map of how the source in `fnv_decomp/` becomes a running executable, and what lives where. For how to run
the build, see the top-level [README](../README.md) and [runtime-next/BUILD-ALL.md](../runtime-next/BUILD-ALL.md).

## The idea

1. The game's code was decompiled into C++ translation units, one recipe entry per unit in
   `fnv_decomp/build/units.json` (source file, compiler version, flags, and the functions it must reproduce).
2. Each unit is compiled with the same Microsoft compiler the game was built with (VC 2008 SP1/RTM, some units VC
   2005), so the object code matches the original function by function.
3. The pipeline in `runtime-next/` then places those compiled functions and the data into a PE image, resolves
   every address and relocation itself, writes its own import table and resources, and produces
   `FalloutNV_selfbuilt.exe`.
4. An automated harness launches the result against an installed copy of the game.

The original executable and game folder are only ever read, as an oracle and as the source of the data that is not
yet generated from source.

## Build pipeline stages

`runtime-next/build_all.py` (run through `build-all.cmd`) runs these steps, logging each to `<out>\logs\NN-name.log`
and stopping at the first failure:

| Step | Folder / script | What it does |
|---|---|---|
| 0 preflight | `build_all.py`, `paths.py`, `buildlock.py` | Checks that the game, reference image and toolchains exist; takes a machine-wide build lock. `paths.py` is the single place for the environment variables. |
| 1 compile-units | `pinned-build/compile_units_v3.py` | Compiles every recipe unit (about 3,000) in parallel with its pinned compiler into object files. |
| 2 build-v7 | `build-v7/` (`verify_v7.py`, `assemble_v7.py`, `icf_v7.py`), `reloc-v7/ownreloc.py` | Re-verifies the accepted per-function contributions (`FNV/contributions`), assembles the code image, folds identical functions the way the linker did (ICF), and generates its own `.reloc`. Uses `reloc-v5/` (relocation resolution) and `coverage-v3/` (exception-handling stubs and library code). |
| 3 data-v1 | `data-v1/`, `data-v2/libsecs.py` | Places the data pieces (`.rdata`, `.data`, `.xdata`) that our objects produce, including data of the CRT and STL library members. |
| 4 dump-pieces | `data-v3/dump_pieces.py` | Exports the placed data pieces for the next stage. |
| 5 data-v3 | `data-v3/` | Turns the data into symbolic MASM, assembles it with `ml.exe`, and proves it round-trips to the same bytes. |
| 6 snapshot | `layout-v2/snapshot.py` | Freezes the inputs of the image maker so the image step is reproducible. |
| 7 make-image | `layout-v2/make_image.py` (with `make_layout.py`, `model.py`), `direct-v1/` | Builds the final PE: block model of `.text`, free layout (`--layout G` keeps the original order), own import table (`build_imports.py`, `iat_spec.json`) and own resources (`res-src/`, `rc_lite.py`, `build_rsrc.py`). Output: `FalloutNV_selfbuilt.exe`. |
| 8 harness | `direct-v1/harness.py` | Optional. Starts the exe, loads a save, plays for a while, changes cell, quicksaves and loads, exits; writes a verdict. Needs an interactive desktop. |

Stage folders are named after their generation (`-v1`, `-v2`, ...); superseded generations are not exported.

## Main subsystems in the source (`fnv_decomp/src`)

| Folder | Contents |
|---|---|
| `fallout/` | Game-specific code (about 760 files), grouped by area: AI, audio, dialogue, interface and so on. |
| `fallout_shared/` | Form, component and animation types shared across the game code (the largest group of headers). |
| `gamebryo2.2/` | The Gamebryo 2.2 engine (`corelibs`): the `Ni*` scene graph, rendering, animation and math classes. |
| `havok/` | The Havok physics and animation libraries (animation, common, physics) and the `bhk*` wrappers live in `bshavok/`. |
| `bscore/`, `bssystem/`, `bssystemutilities/`, `bsmain/` | Bethesda's base layer: heaps and memory, files and archives (BSA), threads, system utilities, bounds and utility types. |
| `bsshader/` | The shader classes of the renderer (the largest folder by file count). |
| `bsmenu/`, `bsaudio/` | Menu and font rendering, audio. |
| `speedtree/` | SpeedTree vegetation integration. |
| `sdk/` | Third-party SDK pieces (FaceGen). |
| `funclets/`, `generated/` | Compiler-generated or machine-assembled pieces: exception-handling funclets and small generated helpers. |
| `unmapped/` | Compiler runtime and library code that is not attributed to a named subsystem (`_ctype`, `_filbuf`, ...). |
| `staging/` | Code grouped by address block while it awaits a proper home. |
| `include/` (next to `src/`) | Shared headers. |

Other folders in `fnv_decomp/`:

- `build/units.json`: the recipe. `build/image_check.json`: reference checks.
- `tools/`: `build_and_match.py` compiles every unit and compares each function with your own game image;
  `compare.py`, `compare_builds.py`, `msvc.py` and `function_spans.py` support it. Subfolders under `tools/` hold
  the more specialised checks (`rebuild`, `coff-directives`, `resource-source`, `rtti-abi`, `rtti-runtime-probe`,
  `runtime-readiness`), with matching test suites under `tests/`.
- `runtime/`: the startup host, test probes and JSON contracts used when linking a runnable program (code pools,
  data arenas, source overlays).
- `third_party/`: zlib 1.2.1 and the patch the game needs.
- `docs/rebuild/`: working documents of the rebuild effort.

## Inputs outside the source tree

| Input | Where it comes from |
|---|---|
| Installed game (resources, companion DLLs, `Data`, INI files) | Your own copy, read only (`FNV_GAME_DIR`). |
| Reference image | Read-only oracle (`FNV_REF_IMAGE`). |
| MSVC 2005/2008 toolchains, `ml.exe`, `cvtres.exe` | Your own installation (`FNV_MSVC*_ROOT`). Not included. |
| `FNV/contributions/*.cpp` and `FNV/local/...` | Included in this repository (project-authored). |
| Object caches, `.reloc`, symbolic data, snapshot | Generated by the build; not stored. |

## How this repository is produced

`tools/export_repo.py` copies `fnv_decomp/`, `runtime-next/` and the files listed in `tools/export_extra.txt` from
the working tree, skipping binaries, logs, scratch, experiments and backups, and replacing personal absolute paths
with placeholders.
