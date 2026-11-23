# Batch 12: a full build without the reference (planner brief, 2026-11-23)

## Where we are (verified by the planner)

- **Data side: done** (batches 9–11).
  - All initialised data comes from our objects or typed datasrc. The datasrc build is the default.
  - NOREF2 (`FNV_REF_IMAGE=<missing> FNV_M3_NOREF2=1`) gives c267a197… without reading reference data bytes.
- **NOREF2 does not rerun the code stage.** It reuses the build-v7 outputs of the last normal build.
- **Code-side survey (2026-11-23, read-only):** every non-padding `.text` byte already comes from our objects:
  - 69,029 recipe functions, 15,725 EH pieces, 1,086 contributions, 594 CRT objects;
  - 0 bytes copied, 0 undecompiled, 0 mismatching.
- **What the code stage still takes from the reference:**

  | Step | File | What it takes | Kind |
  |---|---|---|---|
  | 1 | `verify_v7.py` | Contribution acceptance | Byte check |
  | 2 | `assemble_v7.py` | Function byte check (0 rejects) | Verification only |
  | 3 | `assemble_v3.process` → `build_and_match.eh_sections` | EH funclet addresses, from the reference's parent code and unwind tables | **Layout** |
  | 4 | `assemble_v7.py` | EH exact-byte acceptance | Verification only |
  | 5 | `assemble_v7.py` | Relocation-field `agree`/`borrow` gating, against `orig_raw` | Gating |
  | 6 | `reloc-v7\binding_overlay.json` | ICF and CRT-global bindings | Reference-derived data |
  | 7 | `icf_v7.py` | Check against the reference | Check only |
  | 8 | `crt5.py` / `run_crt4` | CRT/STL objects located by byte search | **Layout** |
  | 9–11 | | Padding map, rebase test, ownreloc | Verification only |

- **Not checked yet:** whether `compile_units_v3.py` and `pinned-build\check_units_v3.py` read the reference.

## Goal

A complete build, code stage rerun and not reused, with `FNV_REF_IMAGE` pointing at a missing file, gives
c267a197… and passes gameplay. The reference is needed only in an opt-in verify mode.

All layout that used to come from the reference is frozen once, as JSON metadata in `runtime-next\m3\frozen\` (or a
sibling `frozen-code\`), from one normal verified run. No section bytes are frozen.

## Steps

### A. Freeze the code layout

All of this is metadata, written from one normal run. Patch `assemble_v7` and the other files to dump it.

1. **EH pieces.** Every accepted EH funclet/tail piece as (unit or contrib id, obj section, offset, size, parent,
   VA): 15,725 pieces plus the 437 contribution EH pieces.
2. **CRT/STL placement.** (library, member, section, offset, size) to VA: 594 code and 81 data.
3. **ICF and binding.** The ICF choices and the binding-overlay decisions as final per-field resolutions, or as the
   existing `binding_overlay.json` plus the ICF map. These are already ours; make sure nothing regenerates them from
   the reference in no-ref mode.
4. **The 2 borrowed fields** (`tail:k14:overlay-name`). Bind them in the overlay so borrowed = 0.

### B. No-ref mode for the code stage

Use an env flag, `FNV_CODE_NOREF=1`, implied by `FNV_M3_NOREF2=1`. In this mode:

- Function, contribution and EH placement come from `units.json`, `contrib_pieces.json` and the frozen EH list.
  `eh_sections` is not called.
- CRT placement comes from the frozen table; `crt5`'s byte search does not run.
- `agree`/`borrow` gating does not read `orig_raw`. Overlay and ICF are applied from the frozen decisions.
- Steps 2, 4, 7, 9, 10 and 11 (verification only) are skipped, and so is `verify_v7`'s reference byte check. The
  contribution compile runs; contributions are placed from the frozen addresses, and their bytes are not compared.
- Check `compile_units_v3.py` / `check_units_v3.py` and anything else in the chain. **Prove it** by running with
  `FNV_REF_IMAGE` set to a missing path: any file that still opens the reference must fail loudly.
- Point data-v1's EH funclet targets at the frozen EH list from step A1, instead of their own copy in
  `dv1_replay.json`, so there is one frozen layout artifact. Do this only if it is simple; otherwise leave it and
  say so.

### C. Acceptance

1. **No-ref build.** `FNV_REF_IMAGE=C:\nonexistent\missing-ref.exe FNV_M3_NOREF2=1`, with build-v7, reloc and
   layout all **rerun** (no reuse of old outputs: point the outputs at a fresh folder or clear them first, and say
   how). Result: c267a197…, plus one harness run PASS.
2. **Negative controls** in no-ref mode. Each must change the sha:
   - (a) shift one frozen EH piece VA by 0x10 in a copy of the frozen file;
   - (b) edit one datasrc literal, the existing dsv control.
3. **Default build.** Unchanged: c267a197…, ROUND TRIP OK.

### D. Records

- Update `C:\path\to\Decompilation\TODO.md`, `PLAN-M3.md` and `DESIGN-phase1.md`, with an env-var table.
- Write a short `runtime-next\m3\frozen\README.md` that lists each frozen file, what it holds, the script that
  regenerates it, and the fact that it was derived once from the reference in a verified run.

## Rules

- Make `.bak-m3b12` backups before editing pipeline files.
- Don't hand-edit `fnv_decomp/src`, `include` or `units.json`. Reading them is fine.
- Never touch the Steam install, the shipped exe or the reference image.
- Don't recursively scan `FNV\work`, `FNV\local` or `fnv_decomp\build\rebuild`.
- One build at a time.
- Don't commit or push.
- Light verification only.
- Delete the out folders of failed attempts.
- Out of scope: deriving layout with a real link (`/OPT:ICF`, link-v2). That is a separate, much larger project.
