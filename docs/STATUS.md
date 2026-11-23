# Current status (2026-11-23)

Code and data are 100% built from source, and the exe is byte-identical to the original
(SHA-256 `c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f`). All initialised data is typed C++ in
`runtime-next/m3/datasrc/`. The build also runs without the reference image: set
`FNV_REF_IMAGE=C:\nonexistent\missing-ref.exe` and `FNV_M3_NOREF2=1`; the layout then comes from the frozen JSON
metadata in `runtime-next/m3/frozen/`. Details: `runtime-next/m3/DESIGN-phase1.md` (batches 9 to 12) and `TODO.md`.

The sections below record the earlier 2026-11-21 checkpoint and are kept as history.

# Accepted checkpoint and remaining work

Updated 2026-11-21. Development workers and gameplay/build runs are paused.

The latest accepted checkpoint uses 3,246 compilation units. Its private
verification ran five fresh serialized builds: positive, value mutation,
pointer mutation, residual-pointer mutation, and a clean repeat. Both clean
images matched the expected SHA-256 and passed menu, load, play, cell change,
quicksave/load, and clean exit. Each mutation failed the round-trip comparison
and changed the resulting image hash. The relocation table stayed identical.
Build products and the detailed captures are not part of this repository.

Accepted recipe SHA-256:
`f173f5dea82f859fdf87944ef72b851f769fce46a0dbc8de0eff8c25bc51aa23`.

Expected clean image SHA-256:
`c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f`.

## Accepted improvements

- 430 runtime type records use native name/parent structures.
- 227 additional native RTTI type descriptors replace 7,942 bytes of generated
  placeholders, using existing canonical headers.
- 27 declarations of the same NiMemObject type have consistent class keys.
- Initialized data produced from compiled objects totals 1,614,032 of
  1,979,392 bytes (81.5%). The latest descriptor batch improves ownership and
  typing without increasing this coverage figure.

This is not a Phase 2 completion percentage. Native type names and matching
descriptor bytes do not establish complete class layouts or inheritance.
No new hard game-function bodies were reconstructed in the latest batch.

## Remaining work

1. Compose the privately tested Settings, Havok, runtime-type, string, and
   allocation/deletion API changes into one source batch. Overlapping source
   and recipe changes require a fresh combined compiler check.
2. Finish integration of 123 additional privately probed native descriptors.
   Final producers, residual fragments, and a relocated mutation control still
   need verification. These candidates are not part of the accepted default.
3. Run the complete production comparison, relocation, mutation, gameplay,
   clean-repeat, and input-freeze gates before accepting either batch.
4. Continue recovering class layouts, inheritance, virtual function order,
   global ownership, and consistent compiler/linker symbol providers.
5. Address 190,698 initialized bytes that already compile but remain unplaced.
   The remaining initialized-data partition also contains 66,842 uncovered
   nonzero bytes, 99,920 uncovered zero bytes, and 7,900 rewritten bytes.
6. In later phases, finish startup/exception integration and the ordinary
   linker build. Its recorded Steam startup crash remains unresolved.

Private candidate passes are evidence for further work, not accepted source
integration or proof that the whole phase is complete.
