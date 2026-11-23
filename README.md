# FNV-GAME: a decompilation of Fallout: New Vegas that rebuilds the game executable

This repository holds C++ source code decompiled from the Steam release of *Fallout: New Vegas* (PC, version
1.4.0.525), plus the build system that compiles that source with the original Microsoft compilers and assembles it
into a working `FalloutNV` executable.

The decompiled source comes from **[momusdigital/fnv_decomp](https://github.com/momusdigital/fnv_decomp)** and its
contributors. See [CREDITS.md](CREDITS.md).

## Licence and credit

Original contributions owned by gavinbrow are free to use, modify and
redistribute under the [MIT licence](LICENSE), including commercially. This
covers original source and header changes anywhere in the repository,
including `fnv_decomp/` and `FNV/`, along with tools and documentation. Other
contributors must expressly license their contributions on these terms.
Keep the copyright and permission notices with copies or substantial portions
to provide attribution. Please also retain [CREDITS.md](CREDITS.md).

This permission covers only rights held by the licensing contributor. It does
not relicense upstream code or grant rights in the original game. Mixed files
retain the restrictions on their pre-existing contents;
[fnv_decomp/LICENSE](fnv_decomp/LICENSE) grants no licence to the upstream
source or its contributors' work. The complete reconstructed game is therefore
not offered under MIT.

## Trademarks

*Fallout*, *Fallout: New Vegas* and related names are trademarks of their respective owners. This project is not
affiliated with or endorsed by any of them. See [fnv_decomp/README.md](fnv_decomp/README.md) and
[fnv_decomp/LICENSE](fnv_decomp/LICENSE) for the licence and the intended purposes (research, modding and game
preservation).

## Status

- **Code: 100% built from source.** Every function of the executable's code is produced by compiling the source in
  `fnv_decomp/`; the compiled functions match the original bytes. The build lays out the code itself and resolves
  its own relocations.
- **Data: 100% built from source.** All initialised data is typed C++ in
  [runtime-next/m3/datasrc/](runtime-next/m3/datasrc/), compiled and placed by the build.
- **The exe is byte-identical to the original.** The build produces `FalloutNV_selfbuilt.exe` with SHA-256
  `c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f`, the same image as the original program.
- **The build can run without the original executable image.** With `FNV_M3_NOREF2=1` the reference image is not
  read; the layout comes from the frozen JSON metadata in [runtime-next/m3/frozen/](runtime-next/m3/frozen/)
  (addresses, identities and header constants only). The preflight check still wants `FalloutNV.exe` in
  `FNV_GAME_DIR`. The result has the same SHA-256.
- **Playable:** the self-built `FalloutNV_selfbuilt.exe` starts directly (without the Steam DRM wrapper), loads a
  save and plays; an automated harness exercises start, load, play, cell change, quicksave/quickload and exit.
  See [README-PLAY.md](README-PLAY.md).

See [docs/STATUS.md](docs/STATUS.md) and [runtime-next/m3/DESIGN-phase1.md](runtime-next/m3/DESIGN-phase1.md) for
the detailed records.

## Folder map

| Path | What it is |
|---|---|
| `fnv_decomp/` | The decompiled C++ source. `src/` (implementation), `include/` (headers), `build/units.json` (the recipe: every translation unit with its compiler, flags and the functions it must reproduce), `tools/` (matching and compare tools), `tests/`, `docs/`, `runtime/` (startup host and link-contract data), `third_party/` (zlib 1.2.1). It has its own [README](fnv_decomp/README.md) on how to contribute. |
| `runtime-next/` | The build pipeline that turns the source into an executable. `build-all.cmd` is the entry point; stage folders are described in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). |
| `FNV/` | Small project-side inputs of the build: `contributions/` (about 4,000 accepted per-function source files), `scripts/local_targets.py` and `local/mcp/local-targets/*.json` (their catalog and state). |
| `tools/` | Maintenance scripts: `export_repo.py` (fills this repository from the working tree), `export_extra.txt` (the file list for `FNV/`), `publish_release.py`, `setup_play.cmd` (prepares a play folder). |
| `docs/` | Project documentation, starting with [ARCHITECTURE.md](docs/ARCHITECTURE.md). |
| `README-PLAY.md` | How to run the self-built executable with a game install. |

## How to build

Requirements: Windows, Python 3.12 with `numpy`, `capstone` and `pefile`, the Microsoft Visual C++ 2008 (SP1 and
RTM) and 2005 SP1 toolchains the game was built with (not included), and a folder with the game files (`FNV_GAME_DIR`).

1. Set the environment variables from [runtime-next/paths.py](runtime-next/paths.py) (every one has a default that
   only suits the original author's machine, so set them all):

   | Variable | Meaning |
   |---|---|
   | `FNV_PROJ_ROOT` | Root of this checkout (`build-all.cmd` derives it from its own location if unset). |
   | `FNV_GAME_DIR` | A *Fallout: New Vegas* game folder. Read only. |
   | `FNV_MSVC9_ROOT` | VC 2008 SP1 toolchain root (cl, ml, cvtres, libs). |
   | `FNV_MSVC9_RTM_ROOT` | VC 2008 RTM toolchain root. |
   | `FNV_MSVC8_ROOT` | VC 2005 SP1 toolchain root. |
   | `FNV_REF_IMAGE` | The reference executable image, a read-only oracle used for checking in the default build. Never copied or modified. Not needed with `FNV_M3_NOREF2=1` (set it to a missing path). See [runtime-next/BUILD-ALL.md](runtime-next/BUILD-ALL.md). |
   | `FNV_PY_SITE` | Optional extra `site-packages` folder holding `numpy`, `capstone`, `pefile`. |
   | `FNV_MYGAMES` | Optional read-only source of INI files and saves for the harness. |

2. Run the build:

   ```
   runtime-next\build-all.cmd --out C:\path\to\output
   ```

   To build without the reference image, with the frozen JSON layout:

   ```
   set FNV_REF_IMAGE=C:\nonexistent\missing-ref.exe
   set FNV_M3_NOREF2=1
   runtime-next\build-all.cmd --out C:\path\to\output-noref2 --no-harness
   ```

   Useful options: `--no-harness` (skip the in-game test, which needs an interactive desktop), `--require-harness`
   (fail if it does not pass), `--layout G`, `--skip-data-v1`. A run takes roughly 5 to 20 minutes depending on
   the machine and options.

3. Results appear in the output folder: `FalloutNV_selfbuilt.exe`, `build-summary.txt` / `.json` (coverage and
   provenance numbers), `harness-verdict.json` and per-step logs in `logs\`.

The build never writes into the game folder. Full details: [runtime-next/BUILD-ALL.md](runtime-next/BUILD-ALL.md).

## How to play

See [README-PLAY.md](README-PLAY.md). In short: put the built exe in its own folder together with the six
`FNV-gamedata-*.zip` parts from the `game-data` release, run `tools\setup_play.cmd` (it unpacks the `Data` folder,
DLLs and INIs), then start `FalloutNV_selfbuilt.exe`. No installed copy or Steam is needed. If you do have an
install, `setup_play.cmd` can link its `Data` folder instead; don't replace the original `FalloutNV.exe` there.

## Contributing

Source-level contributions (renaming, comments, readability) are described in
[fnv_decomp/README.md](fnv_decomp/README.md). Any change must keep every function byte-identical when compiled.

## Keeping this repository tidy

This repository is generated: `python tools/export_repo.py` copies the buildable parts of the working tree and
leaves out experiments, debug scripts, logs and build products (see the ban lists at the top of that script), and
rewrites personal absolute paths to placeholders.
