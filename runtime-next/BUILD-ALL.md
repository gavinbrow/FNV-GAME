# build-all: one-command build of the self-compiled FalloutNV exe

`runtime-next\build-all.cmd --out <dir> [--no-harness] [--require-harness] [--layout G] [--skip-data-v1] [--play SECONDS]`

Output: `<dir>\FalloutNV_selfbuilt.exe`, `build-summary.txt` (release notes), `build-summary.json` (timings, provenance), `harness-verdict.json`, `logs\NN-step.log`.
Steps, in order (stop at the first failure; each step regenerates its outputs, so reruns are idempotent): compile all recipe units (pinned-build\compile_units_v3.py) ->
M3 globals -> build-v7\rebuild.cmd -> data-v1\rebuild.cmd + data-v3\dump_pieces.py -> M3 DV1 selection -> data-v3\rebuild.cmd -> layout-v2\snapshot.py -> layout-v2\make_image.py --layout G -> direct-v1\harness.py --extended.
Allow several minutes for the build and additional time for gameplay; per-step timings are saved. The harness needs an interactive desktop session; its failure is recorded but does not fail the build unless `--require-harness`.

## M3 data defaults (2026-11-19)

The verified defaults are `FNV_M3=1`, `FNV_M3_SEL=phase2/selection.json`, `FNV_M3_DV1=1`, `FNV_M3_DV1_EXT=1` when unset, with the pinned `phase2/library_candidates.json` overlay. The latest accepted metadata suite is W103 v4 positive/two mutation controls/clean repeat, followed by fresh no-overrides default build/gameplay at `m3/out/phase2-local-economy-default-retry-20261119`. Its SHA-256 is `c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f`; exact relocation bytes match the baseline. Initialized compiled-data coverage is 1,613,018 / 1,979,392 bytes (81.5%), with five TLS bytes separate. W103 replaces 103 placeholder bytes within that coverage. The first default attempt failed at menu/load and remains preserved as failed; the unchanged retry passed. See `m3/phase2/LOCAL-WORK-REPORT-20261119.md` and `m3/phase2/PROGRESS.md`; historical Phase 1 evidence remains in `m3/BATCH8-verification.md`.

The default M3 selection SHA-256 is `06250fe537e1f34eae3488444927e909acc64a04ec3ac46cf1af5b2cf9b931a4`; the library selection SHA-256 is `74e3815454a8926ee3d8f70abf939e8d61eadd7173a7514c93e66fee92589700`. Both canonical files are checked before compilation. Set `FNV_M3_LIB=0` to omit library overlays. Custom M3 selections do not acquire one automatically; use `FNV_M3_LIB=1` for the pinned overlay or supply both `FNV_M3_LIB_SELECTION` and `FNV_M3_LIB_SHA256`. Partial pairs and conflicting opt-outs fail. The automatic library path resolves relative to the M3 tools, independently of the working directory.

Set `FNV_M3=0` for the legacy non-M3 comparison build. Explicit selection/DV1/EXT overrides remain available; the canonical selection file is pinned by SHA-256. The driver resolves one child environment and records its effective settings. It clears inherited `DV_M3`/`DV3_SKIP`, then regenerates the needed artifacts. Active DV1 rejects `--skip-data-v1` and `FNV_M3_DV1_OUT` redirects because they could consume stale files. Direct stage scripts still require their explicit mode environment.

Gameplay verdicts use a unique run tag. A passing result requires a zero return code, matching executable path/tag and an exact passing verdict. The copied `harness-verdict.json` belongs to that accepted run; an old copy is cleared when the output folder is reused. The `--default` input to `m3/tools/verify_saved_runs.py` means the **legacy non-M3 baseline**, built with `FNV_M3=0` after promotion.

Extended gameplay uses the isolated profile's actual quicksave/quickload bindings and a read-only owning-cell probe: the cell must change after COC and return to the saved cell after quickload. Known pause/console states have bounded recovery; unknown states fail with screenshots. The default clean exit requests the game's native QuitGame command and still requires exit code 0 without forced termination. Direct harness `--exit-method menu` retains the older UI route for debugging. `--require-cell-state` adds the semantic checks to saved-run verification. The probe relies on the custom M3 image preserving original internal `.data` offsets; a future native-link image needs separate mapping validation. These checks establish cell/location restoration, not complete save-state equality.

The optional corrected library-section reader is enabled with
`FNV_DV1_LIB_COFF_INDEX_V2=1`. It requires fresh M3/DV1 and an explicit compatible
`FNV_M3_LIB_SELECTION` / `FNV_M3_LIB_SHA256` pair; the canonical 405-record
selection uses the default legacy index mode. The driver and frozen-run receipt
record the index mode and the reader hash. The verified experimental 402-record
selection holds three duplicate strings and covers 28 fewer initialized bytes;
it has not replaced the canonical selection. See
`m3/phase2/NON-AI-INTEGRATION-20261119.md` for the five-run verification evidence.

## Locks

- `build.lock` (machine wide: `C:\path\to\Decompilation\runtime-next\build.lock`, override with `FNV_BUILD_LOCK`): content `pid unixtime owner`. build-all holds it for the whole run; waits while a live holder exists, breaks locks of dead PIDs or older than 120 min.
  Other rebuilds: `python runtime-next\buildlock.py acquire <owner>` ... `python runtime-next\buildlock.py release <owner>`.
- `harness.lock` (`direct-v1\harness.lock`, override `FNV_HARNESS_LOCK`): one game instance per PC.

## Environment (defaults = today's local paths; `paths.py` is the shared helper, `layout-v2\ci\relocate_paths.py` rewrote the hard-coded literals into `os.environ.get(VAR, today's path)`)
| variable | meaning |
|---|---|
| FNV_PROJ_ROOT | checkout root (build-all.cmd derives it from its own location) |
| FNV_GAME_DIR | installed Fallout New Vegas folder; READ ONLY (resources, DLLs and Data junction for the harness) |
| FNV_REF_IMAGE | decrypted reference image `FalloutNV.runtime-text.exe`; READ ONLY, never copied |
| FNV_MSVC9_ROOT / FNV_MSVC9_RTM_ROOT / FNV_MSVC8_ROOT | VC 2008 SP1 / VC 2008 RTM / VC 2005 SP1 toolchains (cl, ml, cvtres) |
| FNV_PY_SITE | site-packages with numpy, capstone, pefile |
| FNV_MYGAMES | read-only source of Fallout.ini/FalloutPrefs.ini/Saves for the harness (default `~\Documents\My Games\FalloutNV`) |

## Inputs that live outside fnv_decomp\ and runtime-next\ and how each is handled
| input | handling |
|---|---|
| reference image (decrypted .text) | cannot be regenerated from the installed FalloutNV.exe: in the installed file `.text` is the SteamStub-encrypted copy (12.39 MB differ; every other section is identical). Read from `FNV_REF_IMAGE` (default `FNV\work\worker1\FalloutNV.runtime-text.exe` on the owner's PC), never copied |
| installed game (FalloutNV.exe resources, companion DLLs, Data, INIs, a save) | read only from `FNV_GAME_DIR` / `FNV_MYGAMES` |
| MSVC toolchains, ml.exe, cvtres.exe | on the owner's PC, `FNV_MSVC*_ROOT` |
| `FNV\scripts\local_targets.py`, `FNV\local\mcp\local-targets\{catalog,state,symbols,config}.json`, `FNV\contributions\*.cpp` (4,069 files) | ours, 22 MB: listed in `tools\export_extra.txt` (generated by `runtime-next\layout-v2\ci\make_export_extra.py`) |
| `runtime-next\direct-v1\res-src\resources.rc`, `manifest.xml` | ours: export_extra |
| obj caches (`pinned-build\obj_v3`, `build-v7\obj`), data-v1 scratch pickles, `data-v3\symbolic.json`, `layout-v2\snapshot` | regenerated by the build; unique per-run scratch under `.build-tmp`, with fresh pickles and SHA-256 hashes archived in `<out>\evidence\data-v1-scratch` before cleanup |
| binding overlay, icf maps, link-v2 json (<= 4 MB) | in the exported runtime-next json set |
