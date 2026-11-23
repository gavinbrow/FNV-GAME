# Batch 10: data as source (planner brief, 2026-11-23)

## Where we are (verified by the planner)

| Stage | Result |
|---|---|
| Batch 9 stage 1 | Swept the uncovered non-zero and zero data into W placeholders: 89.9% of initialised data from our objects. |
| Batch 9 stage 2 | Covered the compiled-but-unplaced data and the leftovers. 1,971,492 of 1,979,392 B now come from our objects; the other 7,900 B are tool-built by `make_image.py`. The opt-in selection `batch9s2_selection.json` (sha256 b92f59ce…) builds c267a197…. |
| Batch 9 stage 3 | The "no-ref" mode it added is **not accepted as real progress**. Its stand-in image is built from `frozen/ref_data.bin.z` and `ref_reloc.bin.z`, which are compressed copies of the reference's data and `.reloc` sections. It moves the reference rather than replacing it. Keep it as a stepping stone only. |

Of the data from our objects, 559,131 B are real compiled unit and library pieces. **1,412,366 B are W placeholders**:
anonymous `M3_<va>` objects whose byte values `gen_m3.py` re-reads from the reference (`refbytes`) on every build.

## Goal

1. The data becomes source: typed, named C++ definitions with literal values. The build compiles them instead of
   regenerating placeholders from the reference.
2. The data path places that source without reading reference bytes.

## Steps

### A. Make `batch9s2` the default

- Set config.py's default selection to `batch9s2_selection.json`, with its digest, and keep the library and
  RTTI-literal flags it needs.
- Check: the default build (no env vars) gives c267a197…, and one harness run passes.

### B. Generate the data source

`m3/datasrc_gen.py` is a one-shot generator that may read the reference. Its output is
`runtime-next/m3/datasrc/*.cpp` plus `datasrc/index.json`, grouped by section and address range into files of
reasonable size.

Every W object becomes a definition with literal values and, where it can be derived automatically, a real type and
name:

- **RTTI:** MSVC RTTI layouts:
  - TypeDescriptor `{pVFTable, spare, name[]}`;
  - CompleteObjectLocator `{signature, offset, cdOffset, pTypeDescriptor, pClassDescriptor}`;
  - ClassHierarchyDescriptor;
  - BaseClassDescriptor and BaseClassArray.
  Named from the decorated type name: `.?AVFoo@@` gives `Foo`, so `RTTI_TD_Foo`, `RTTI_COL_Foo` and so on.
- **Vtables:** found through the CompleteObjectLocator pointer at `vtable[-1]`. Named `vtbl_Foo`, with
  `vtbl_Foo_at_<off>` for secondary bases. Typed as arrays of function pointers whose entries name the function
  symbols. Use names from `fnv_decomp/tools/function_names_data.py` and the units' symbols where they exist.
- **Other kinds:**
  - strings and wide strings become string literals, escaped correctly;
  - floats and doubles become float literals;
  - pointer tables become arrays of named symbols;
  - globals with `DAT_`/`PTR_`/namespaced names keep those names, with one canonical type;
  - zero blocks stay file-backed through the existing `__declspec(allocate)` mechanism.
- **Fallback:** whatever has no better type stays a byte or dword array, counted as "opaque".
- **Index:** each object's address goes in `index.json`, which also drives placement. Addresses are not
  recovered by matching bytes.
- **Build switch:** `FNV_M3_DATASRC=1` makes the build compile `datasrc/` for those objects, with no `refbytes`
  call for them.
- **Acceptance:** c267a197… with round trip OK; value and pointer negative controls (by editing a literal and a
  pointer in a datasrc copy) change the sha; one harness run.

### C. Placement without reference bytes

- **data-v1:** a placement map freezes each piece's identity (object, section, symbol and content hash) to its
  VA, from one normal run. In this mode `place.py`, `dv1_splice` and the library overlay use the map and fail
  loudly if a compiled piece's hash differs.
- **data-v3:** the base becomes zero-filled sections. Relocation sites are derived from the relocations our
  overlays produce. Freeze only metadata that is really needed (section sizes, chunk boundaries) as JSON, never
  section bytes.
- **Round trip:** the check against the reference runs only in verify mode.
- **Frozen inputs:** the no-ref path must no longer read `ref_data.bin.z` or `ref_reloc.bin.z`. Leave the files on
  disk but unused, and report so. Header constants go in JSON fields.
- **Acceptance:** `FNV_REF_IMAGE` points to a missing file and no reference section bytes are read on the data
  path. The result is c267a197…, and one harness run passes.
- **Scope:** code-side stages (build-v7 and friends) stay reference-dependent and out of scope. Reuse their outputs
  as stage 3 did.

## Rules

- Light verification only: sha, two negative controls, one harness run, and the default build unchanged.
- Backups `.bak-m3b10` before editing pipeline files.
- Don't hand-edit `fnv_decomp/src`, `include` or `units.json`.
- Never touch the Steam install, the shipped exe or the reference image.
- One build at a time.
- Don't commit or push.
