# Phase 2 first experiments (2026-11-18)

This file preserves the first experiment checkpoint. The active continuation,
installed TESContainer pilot, failed integration attempts and current combined
verification are recorded in `PROGRESS.md`; consult that before relying on the
historical untouched-source and positive-only statements below.

This is work after the accepted Phase 1 milestone. The canonical default remains
Batch 8, with selection SHA-256
`42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7`.
No protected decompilation source, header or unit recipe has been changed.

## Explicit scalar definitions instead of W wrappers

The opt-in selection under `../out/phase2-w-scalar/selection.json` has SHA-256
`0e0efb67b2a89260e5e78c7e49646aab4fdd252dd4b0a24116549b0f4c51596a`.
It preserves all 8,263 addresses and widths, replaces 22 W entries with
source-declared scalar types (114 bytes), and leaves the other 8,241 entries
identical. One of the original 23 leads was excluded for a conflicting unit
alias. This improves type quality within existing coverage; it adds no bytes
to the accepted 1,596,260 / 1,979,392 (80.6%) coverage figure.

`gen_m3.py` now supports explicit, validated scalar namespace, constness and
mangled identity metadata. Definitions preserve the declared C++ identity
while explicitly allocating file-backed storage in the required section.
Namespaced scalar use as an intra-object table host is rejected. Existing
selection entries retain their previous behavior.

Independent review checked all 22 namespace scopes, declarations, constness,
unit names and existing COFF external references. An isolated VC2008 fixture
compiled every candidate and passed exact emitted-name, storage, section,
byte, relocation and dynamic-initializer checks. Old/new generation of the
accepted selection produces identical C++ in all four object partitions.
See `ACCOUNTING.md` and `W-SCALAR-review.md` for evidence and limitations.

The serialized test run passed 61 existing tooling tests and six new scalar
tests. Four separate class-rename safety checks also passed. These tests are
distinct from the full image and gameplay acceptance checks.

Full opt-in build `../out/phase2-w-scalar-positive` passed with all 8,263
entries kept and zero dropped. The actual executable matches canonical
SHA-256 `c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f`.
Its 734,884-byte PE relocation directory exactly matches the accepted default
(SHA-256 `364b83a38aae50e6faf0a4f0512fdfa8b338bd1dab47b39fec0bd7b03fd26057`).
The coordinator independently checked the files, all 22 exact scalar entries,
the unchanged other 8,241 entries and identical selected M3/DV1 ranges.

Gameplay passed with 71.7 seconds of play, a newly written quicksave, cell
IDs `1291213 -> 1073541 -> 1291213`, configured F5/F6 inputs and native
QuitGame exit code 0 without forced kill. One recognized console-close
recovery restored the HUD. The saved WER list is empty; Event Log query
availability was not separately established. The fresh harness tag is
`build-all-940292-1795059397286417800`.

The archived selection, object files, manifests, tooling hashes and independent
`root-review.json` are under `../out/phase2-w-scalar-positive/evidence/`.
Positive helper checks cover configuration, provenance, verdict identity and
semantic cell restoration. The complete saved-run CLI requires a legacy
baseline and two control summaries; it was not passed for this selection.
New-selection mutation controls and a repeat run remain outstanding, and the
selection remains opt-in. The accepted Batch 8 default is unchanged.

## Class-name compiler experiment

A hash-pinned private overlay renames four source tokens from `FUN_00d698b0`
to `hkpConstraintViewer` in unit 2501. Original and overlay both compiled
with that unit's SP1 recipe, and all 16 mapped functions match the reference.
The compiler emits the expected 34-byte type descriptor. The existing W
owner spans 40 bytes and contains another relocation at offset 36, so
replacing the whole W owner with that descriptor would be incorrect.

The revised exact-symbol object comparison passed for all 16 functions:
raw code bytes and normalized relocations agree between original and overlay,
and both match the reference. The emitted descriptor's nonrelocated bytes and
independently resolved `type_info` relocation also match the reference. The
initial comparator's false mismatch from changing an unrelated literal symbol
is preserved separately; the corrected result is `coff-comparison-v2.json`.

The hierarchy analysis found a substantive mismatch: seven original base
descriptors versus six emitted by the surrogate, plus differing attributes on
the final two bases. See `HKP-HIERARCHY.md`. The experiment establishes neither
the full original hierarchy nor virtual slot identities, and makes no coverage
claim. Source collisions caused the
AudioLoadTask and BGSTerrainChunkLoadTask rename leads to be excluded.
See `RTTI-plan.md` and private `../out/phase2-hkp-constraint-viewer/` evidence.

The bounded camera-path vtable lead remains unresolved: its deleting
destructor's exact ABI and specialization identity need independent support.
No arbitrary target alias or base-method retargeting was installed. See
`VTABLE-plan.md`.

## Remaining work for the next batch

- Run the scalar selection's mutation controls and repeat acceptance before
  considering promotion; the current result is one successful opt-in run.
- Specify and independently verify the original hkp hierarchy and required
  virtual slots before generating a hierarchy overlay. Preserve the extra
  pointer in the W owner's remainder during any future descriptor replacement.
- Establish the camera-path specialization destructor target and normal weak
  external resolution without inserting a reference-fed target alias.
- Investigate library-owned placement separately. `LIBRARY-TRIAGE.md` accounts
  for 65,726 library-only annotated bytes within the existing remainder; most
  have runtime-data annotations rather than RTTI/vtable labels.
