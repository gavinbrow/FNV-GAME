# Batch 11: finish the data (planner brief, 2026-11-23)

## Where we are (verified by the planner)

- **Batch 10 is done.** See `DESIGN-phase1.md`, "Batch 10 step A/B/C".
- **Default build** (batch9s2): c267a197…, round trip OK, harness PASS (`out\b10f-default`).
- **`FNV_M3_DATASRC=1`:** builds 59,658 typed definitions from `m3\datasrc\` and gives c267a197… (`out\b10b-datasrc`), harness PASS.
- **`FNV_REF_IMAGE=<missing> FNV_M3_DATASRC=1 FNV_M3_NOREF2=1`:** c267a197… (`out\b10e-noref2`), harness PASS. No
  reference section bytes are read on the data path.
- **Not built yet:** the final datasrc sources with the function-name comments.
- **Still left:**
  - 177,390 B of opaque arrays (18,249 objects);
  - 50,241 objects with generic kind+address names;
  - about 47 KB of our own compiled unit pieces that are identical to the original but unplaced, while placeholders
    cover the same bytes;
  - 11,783 EH funclet reloc targets taken from frozen JSON.

## Steps (in order, one build at a time)

### A. Make the data-as-source build the default

1. Build NOREF2 with the current commented datasrc. Check: c267a197….
2. Make `FNV_M3_DATASRC=1` the default in config.py. Keep a way to switch it off (`FNV_M3_DATASRC=0`). NOREF2
   stays opt-in, because the default build keeps the round-trip check against the reference.
3. Check: the default build with no env vars gives c267a197…, round trip OK, one harness run PASS.

### B. Replace placeholders with our own compiled pieces

- Find the compiled-but-unplaced unit and library pieces whose bytes and relocations already match the original
  (about 47 KB according to the batch 9 inventory; recount it).
- Place them through data-v1 and drop their datasrc definitions. Update `index.json` and `placement_map.json`.
- Pieces that only nearly match stay as placeholders. List them with the reason.
- Check:
  - default and NOREF2 builds both give c267a197…;
  - one value and one pointer negative control change the sha;
  - one harness run.
- Report the real-unit bytes before and after (now 559,131 B).

### C. Shrink the opaque data

Re-type the opaque objects in `datasrc_gen.py`, automatically and without guessing at meaning:

- **Kinds to detect:**
  - int/short/byte arrays with clear stride;
  - records of mixed pointer and int fields, found by period detection over the reloc pattern, emitted as named
    structs (`rec_<va>_t`);
  - GUIDs and bit tables;
  - types declared for that address in `fnv_decomp` headers or units, where one exists.
- **Names from cross-references:** use a name derived from the code that references each data object, from the
  build's `.text` relocations, where only one function uses it. Examples: `g_FUN_00ABCDEF_tbl`, or a real function
  name from `units.json` / `function_names_data.py`.
- **Output:** re-generate and keep `index.json` hashes valid.
- **Check:** sha, two controls, one harness run.
- **Report:** opaque bytes and generic-name counts before and after. Target: opaque under 60 KB, but stop when the
  remaining cases are one-offs.

### D. EH funclet targets from our own build

The 11,783 EH unwind-funclet reloc targets in `dv1_replay.json` should come from the EH tables of our own build-v7
output rather than the frozen copy (learned from the reference).

- If that is a small change, do it, and NOREF2 must still give c267a197….
- If it isn't small, report what it would take, and leave it.

### E. Records

- Rewrite `runtime-next\TODO.md` as a short checklist: done, left, and the opt-in env vars. It is currently 30 KB of
  stacked paragraphs; move the old text to `TODO-archive-20261123.md` unchanged.
- Add batch 9–11 results to `PLAN-M3.md` and `DESIGN-phase1.md`.

## Rules

- Make `.bak-m3b11` backups before editing pipeline files.
- Don't hand-edit `fnv_decomp/src`, `include` or `units.json`. Reading them is fine.
- Never touch the Steam install, the shipped exe or the reference image.
- One build at a time.
- Don't commit or push.
- Light verification only: sha, two negative controls, one harness run, and the default build unchanged. No
  multi-run suites.
- Delete the out folders of failed or superseded batch 11 attempts. Keep the accepted ones.
