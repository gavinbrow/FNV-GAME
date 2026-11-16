# FNV-GAME: a decompilation of Fallout: New Vegas that rebuilds the game executable

This repository holds C++ source code decompiled from the Steam release of *Fallout: New Vegas* (PC, version
1.4.0.525), plus the build system that compiles that source with the original Microsoft compilers and assembles it
into a working `FalloutNV` executable.

The decompiled source comes from **[momusdigital/fnv_decomp](https://github.com/momusdigital/fnv_decomp)** and its
contributors. See [CREDITS.md](CREDITS.md).

## Legal note (please read)

- **No game assets are included.** This repository contains no game files, no executables, no archives (`.bsa`),
  no plugins (`.esm`/`.esp`), no textures, models, sounds or videos, and no compiler or SDK files.
- **You need your own copy of the game.** The build reads (never writes) a legitimately installed copy of
  *Fallout: New Vegas*, and the result only runs together with the `Data` folder of that install.
- Built executables still contain data taken from the original program (see Status), so keep them private and do
  not redistribute them.
- *Fallout*, *Fallout: New Vegas* and related names are trademarks of their respective owners. This project is not
  affiliated with or endorsed by any of them. See [fnv_decomp/README.md](fnv_decomp/README.md) and
  [fnv_decomp/LICENSE](fnv_decomp/LICENSE) for the licence and the intended purposes (research, modding and game
  preservation).

## Status

- **Code: 100% from source.** Every function of the executable's code is produced by compiling the source in
  `fnv_decomp/`; the compiled functions match the original bytes. The build lays out the code itself and resolves
  its own relocations.
- **Data: partly still taken from the original executable.** Parts of the data sections (and some tables such as
  imports and resources) are still copied from the original exe, or from a legitimately installed game, while the
  rest is already generated from source. This is why a build needs a legitimate installed copy of the game and the
  reference image described below.
- **Playable:** the self-built `FalloutNV_selfbuilt.exe` starts directly (without the Steam DRM wrapper), loads a
  save and plays; an automated harness exercises start, load, play, cell change, quicksave/quickload and exit.
  See [README-PLAY.md](README-PLAY.md).
- Remaining work is mostly readability (many functions still carry placeholder names such as `FUN_00xxxxxx`) and
  moving the last pieces of data from "copied" to "generated".

Detailed, dated status notes live in [runtime-next/CURRENT.md](runtime-next/CURRENT.md).

## Folder map

| Path | What it is |
|---|---|
| `fnv_decomp/` | The decompiled C++ source. `src/` (implementation), `include/` (headers), `build/units.json` (the recipe: every translation unit with its compiler, flags and the functions it must reproduce), `tools/` (matching and compare tools), `tests/`, `docs/`, `runtime/` (startup host and link-contract data), `third_party/` (zlib 1.2.1). It has its own [README](fnv_decomp/README.md) on how to contribute. |
| `runtime-next/` | The build pipeline that turns the source into an executable. `build-all.cmd` is the entry point; stage folders are described in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). |
| `FNV/` | Small project-side inputs of the build: `contributions/` (about 4,000 accepted per-function source files), `scripts/local_targets.py` and `local/mcp/local-targets/*.json` (their catalog and state). |
| `tools/` | Maintenance scripts: `export_repo.py` (fills this repository from the working tree), `export_extra.txt` (the file list for `FNV/`), `publish_release.py`, `setup_play.cmd` (prepares a play folder). |
| `docs/` | Project documentation, starting with [ARCHITECTURE.md](docs/ARCHITECTURE.md). |
| `README-PLAY.md` | How to run the self-built executable with your own game install. |

## How to build

Requirements: Windows, Python 3.12 with `numpy`, `capstone` and `pefile`, the Microsoft Visual C++ 2008 (SP1 and
RTM) and 2005 SP1 toolchains the game was built with (not included), and your own installed copy of the game.

1. Set the environment variables from [runtime-next/paths.py](runtime-next/paths.py) (every one has a default that
   only suits the original author's machine, so set them all):

   | Variable | Meaning |
   |---|---|
   | `FNV_PROJ_ROOT` | Root of this checkout (`build-all.cmd` derives it from its own location if unset). |
   | `FNV_GAME_DIR` | Your installed *Fallout: New Vegas* folder. Read only. |
   | `FNV_MSVC9_ROOT` | VC 2008 SP1 toolchain root (cl, ml, cvtres, libs). |
   | `FNV_MSVC9_RTM_ROOT` | VC 2008 RTM toolchain root. |
   | `FNV_MSVC8_ROOT` | VC 2005 SP1 toolchain root. |
   | `FNV_REF_IMAGE` | The reference executable image used as the read-only oracle for the parts not yet generated from source. Never copied or modified. See [runtime-next/BUILD-ALL.md](runtime-next/BUILD-ALL.md). |
   | `FNV_PY_SITE` | Optional extra `site-packages` folder holding `numpy`, `capstone`, `pefile`. |
   | `FNV_MYGAMES` | Optional read-only source of INI files and saves for the harness. |

2. Run the build:

   ```
   runtime-next\build-all.cmd --out C:\path\to\output
   ```

   Useful options: `--no-harness` (skip the in-game test, which needs an interactive desktop), `--require-harness`
   (fail if it does not pass), `--layout G`, `--skip-data-v1`. A run takes roughly 5 to 20 minutes depending on
   the machine and options.

3. Results appear in the output folder: `FalloutNV_selfbuilt.exe`, `build-summary.txt` / `.json` (coverage and
   provenance numbers), `harness-verdict.json` and per-step logs in `logs\`.

The build never writes into the game folder. Full details: [runtime-next/BUILD-ALL.md](runtime-next/BUILD-ALL.md).

## How to play

See [README-PLAY.md](README-PLAY.md). In short: put the built exe in its own folder, run `tools\setup_play.cmd` (it
links the `Data` folder of your install and copies the small companion DLLs and default INI), then start
`FalloutNV_selfbuilt.exe`. Do not replace the original `FalloutNV.exe` in your install.

## Contributing

Source-level contributions (renaming, comments, readability) are described in
[fnv_decomp/README.md](fnv_decomp/README.md). Any change must keep every function byte-identical when compiled.

## Keeping this repository tidy

This repository is generated: `python tools/export_repo.py` copies the buildable parts of the working tree and
leaves out experiments, debug scripts, logs and build products (see the ban lists at the top of that script), and
rewrites personal absolute paths to placeholders.
