# Non-AI integration results, 2026-11-19

This continuation executed the previously staged routes. It did not reconstruct
any new game function bodies. Phase 2 remains open. The accepted default still
covers **1,613,018 / 1,979,392 initialized data bytes**; this is a data-coverage
measure, not a Phase 2 completion percentage. No new physical coverage or fully
reconciled native class is claimed in this pass.

## What actually ran

### Fresh placement and five full builds

The one-based COFF library-section correction was exercised with **fresh
placement from no seeded placements**, followed by the real library selector.
A fresh zero-based placement on the same frozen inputs isolated five changed
placements/tier assignments. Three duplicate weekday strings moved to copies
already owned by M3. The old migrated 405-record selection failed closed.

A private 402-record / 16,702-byte selection holding those three strings passed.
Its actual initialized-data union is **1,612,990 bytes**, 28 below the accepted
default; it adds no new physical coverage. The 405-record archived-state replay
was valid only for its saved placement state and was not substituted for this
fresh result.

Five new full builds were run serially: positive, PSA value mutation, PSA pointer
mutation, library value mutation, and clean positive repeat. The final independent
saved-run audit passes. Both positive images equal the canonical SHA-256
`c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f`.
All five have the exact expected 734,884 relocation bytes. Both positives pass
menu, load, approximately 70 seconds of play, cell change, quicksave/quickload
with cell restoration, and clean exit. Each deliberate mutation fails the
round-trip check and changes the final image hash, with an exact artifact-level
mutation proof. Mutated images were not gameplay tested.

Each run watched 12,726 inputs with no observed/final input changes and retained
fresh objects, placement states, source manifests and configuration receipts.
Native unit620's 16 functions and 16 located EH records pass in every run.
The temporary helper was restored after each run; canonical defaults and the
protected source/recipe were not promoted or edited.

Evidence: `../out/non-ai-integration-20261119/suite-acceptance.json`, the five
`../out/non-ai-index-v2-*` run directories, and
`../out/non-ai-continuation-20261119/fresh-placement/`.

### A usable Ghidra type archive

The unchanged community import script now runs through the already installed
PyGhidra/JPype path. Its target-identity preflight passes. A metadata-only private
program compiler setting also makes the installed RTTI models validate two
already known descriptors. A separate 90-second bulk RTTI attempt timed out;
its final recovery count is unknown and is not counted as a successful scan.

The saved `xnvse-community.gdt` was independently reopened: 3,120 selected
community types, 3,204 types including dependencies, and 32-bit pointer data
organization. TESModel, TESContainer and BGSBodyPartData layout/path/size views
match the saved project; five sampled pointer fields remain four bytes after
export/reopen. These are source-derived views. The imported project contains
1,918 structures with no defined components, and the importer applied **zero
symbols, vtables or function names**. Imported packing/alignment is not native
ABI proof. None of these counts establishes completed native classes.

Artifact: `../out/non-ai-integration-20261119/community-import-v5/xnvse-community.gdt`.
Its adjacent provenance and pointer-validation receipts identify sources,
revisions, hashes, target and limitations. No new package download was needed.

### Original CRT and compiler-generated metadata

The pinned CRT libraries were searched directly: 908 parsed library objects,
plus the actual 2,995 recipe objects. No strong `type_info` vector-deleting
destructor was found in those scoped inputs. Original Microsoft LINK was tested
with a tiny private fixture and a strong-definition control: actual library
fallback and strong override both behave as expected. The fixture executables
were never run. This does not justify a blanket weak-symbol alias policy.

Compiled-byte/reference graph matching uniquely located three existing CRT
function candidates of 16, 33 and 112 bytes. The 112-byte helper still needs its
dependency/provider/EH ownership resolved. Byte identity alone does not establish
the original source owner; an existing V7 choice uses an alternate CRT name.

A new private source view includes the installed original `<typeinfo>` header
and expresses **already accepted destructor logic** as `type_info::~type_info()`.
No new function implementation was reconstructed. The compiler emits the
deleting destructor and RTTI automatically. The accepted surrogate profile
matches seven of eight records but emits a 45-byte deleting destructor; adding
`/Ob0` gives 35 bytes. The observed difference is stack-cleanup encoding. The
final native-only `/Ob0 /Os` trial passes **all eight records**: 49 function bytes
and 101 metadata bytes, exact extents, nonrelocation bytes, relocation identities
and independently checked targets. Weak auxiliary records match the actual CRT
`SEARCH_LIBRARY=2` form and target name/strong definition; no EH/dynamic-init
sections were added. Both earlier mismatching trials are preserved.

This is a verified **private source candidate**, not accepted whole-class/ODR
ownership or integration. It remains uninstalled. See
`../out/non-ai-integration-20261119/private-probes-acceptance.json` and the
`typeinfo-native-{proposal,noinline,size}` directories. An initial precompile
weak-audit assumption was corrected after direct symbol-table inspection; the
receipt explains the correction. No compiled result was overwritten.

The three weekday arrays also compile as read-only, relocation-free const-char
storage with exact original bytes (28 total). Their known CRT consumers point
to the other duplicate copies, so the old copies' native storage identity is
unproven. This synthetic fixture is uninstalled and adds no accepted coverage.

## What this improves, and the remaining work

The corrected placement route has now passed the actual image/gameplay/control
gates. The community declarations are available in a reusable, checked Ghidra
artifact. One original-header CRT candidate now produces the expected native
metadata and code through compiler settings, using existing implementation logic.
These are concrete executed results, rather than additional task packets.

The next useful implementation step is a narrow generator-backed ownership
integration: reconcile the CRT candidate with current contribution/library
providers, preserved weak semantics, M3 overlap claims and ODR, then run affected
native compiler checks before any full-build promotion. The duplicate strings
need native ownership evidence before they can close the 28-byte gap. Broader
community extraction needs real preprocessor/build context (the aggregate trials
still stop at missing `UnorderedMap`/`DWORD` prerequisites). Imported definitions
and Xbox debug declarations still require PC layout, inheritance, virtual order
and return-ABI reconciliation before they replace native class definitions.

This is the end of this bounded continuation, not proof that all useful
non-decompilation work is exhausted. All four Terra tasks have completed.
Final source/default/reference hashes and clear locks are recorded separately in
`../out/non-ai-integration-20261119/final-receipt.json`.
