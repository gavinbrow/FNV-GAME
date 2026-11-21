# Non-AI continuation results - 2026-11-19

Completed the next local pass without reconstructing game function bodies.
The concrete outputs are a searchable corpus for the whole class census,
additional decoded field shapes, tested private importer/indexing corrections,
and an archived-state selector replay. No production class/source, recipe,
selection, active build helper or executable was changed. All evidence remains
private and the two focused Terra workers are stopped.

## Reusable evidence, without per-class agent investigations

`export_atlas_evidence.py` exports a checksum-linked card for every one of the
2,999 existing PC class identities. It opens the pinned atlas read only and
joins exact decorated identities, preserving multiple definitions and missing
records. The complete export took about 34 seconds after database verification.

- 2,263 records have debug definitions; 736 have no exact definition.
- 39 records retain multiple alternatives; no automatic identity merge.
- The cards contain 8,548 distinct data-member records and 53,329 distinct
  single-method records, plus overload and base metadata. These are debug
  declarations, not newly decompiled functions or completed native classes.
- 2,085 records have at least one matching ordered PC direct-base/offset
  alternative. That says nothing by itself about field layout, object size,
  function return ABI, destructor/provider ownership or whole-class correctness.
- All 2,999 identities and card hashes were checked; independent SQL queries
  reproduce the distinct member counts. Every card explicitly remains unaccepted.

The new `atlas_evidence_query.py` retrieves a card by exact job ID or decorated
name and verifies its hash. It optionally attaches separately decoded field
shapes while retaining their Xbox origin and the raw original rendering.
No MCP packets, queue status or server endpoints were changed.

Example, from the workspace root:

```powershell
python runtime-next/m3/phase2/atlas_evidence_query.py --job P2N19-C-011861BC --field-shapes runtime-next/m3/out/non-ai-continuation-20261119/field-shapes-v2/result.json
```

## Field information recovered by decoding, not inference

The first corpus validation found 324 distinct data-member records with retained
unrendered type tokens. `decode_atlas_field_shapes.py` decodes their underlying
raw CodeView records with record-hash, size, divisibility and representation
checks. It decoded 322: 309 arrays, 8 bitfields and 5 pointers to compound types.
Two remain held: an ambiguous/missing complete element tag (`m_motors`) and an
unsupported pointer representation (`NoteActivationFn`). Twenty single-method
records also still contain unrendered type tokens; this field decoder does not
silently claim to resolve them.

For example, the query now supplies the 15-element pointer-array shape for
BGSBodyPartData's pPartArray. These are Xbox field facts; no PC member offset or
layout was installed from them.

The decoder was checked against fresh MSVC 2008 /Z7 records from an independently
specified own-data fixture: 4 array shapes, 2 bitfield layouts, a large encoded
integer and 3 malformed-record rejections pass. The field format is based on
LLVM 20.1.8 TypeRecord/TypeRecordMapping/TypeIndex primary definitions. This is
extraction of stored type information, not reconstruction of game bodies.

## Community importer correction, privately tested

The narrow x86 overlay restores three known declaration locations lost by
Clang's compressed textual paths, parses recognized calling-convention suffixes,
and corrects two virtual-slot calculations from 8-byte to 4-byte spacing.
Unsupported signatures are held rather than silently converted into void().

Actual output restores the four BaseFormComponent virtual signatures and three
TESModel declarations. TESContainer introduces no new virtual declarations in
this plugin header; its inherited methods remain separate. The run increases
structures 2,499 to 2,617 and vtable structures 103 to 151, including downstream
placeholders. Across 2,499 common structures, sizes stay unchanged; 48 field lists
and 7 slot lists change. Four focused tests pass. This is an experiment limited
to three pinned declaration locations, not a general Clang scope decoder or a
native C++ class adoption. All downstream field changes still require review.

The five-header aggregate experiment failed on missing UnorderedMap context.
A context-only retry using the existing containers.h reached a missing DWORD
prerequisite under the original importer prelude. Both attempts remain failed,
with exact inputs and diagnostics. Neither produced valid additional types or
an increased coverage result. No placeholder declarations were invented to pass.

## A concrete ABI conflict confirmed with the original compiler

The debug hkBool is a one-byte class; our current PC Havok view typedefs char.
Two privately generated interface-call probes use the same recorded signatures
and corrected overload order. MSVC 2008 emits a hidden return-storage argument
for the class view:6 argument pushes versus5 for the char view. Equal storage
size therefore does not establish interchangeable calling conventions.

This does not establish which view any given retail caller requires. It blocks
blind import of Xbox return signatures into existing PC typedef contexts. The
initial verifier counted frame setup as arguments; that failed diagnostic run
is preserved, and v2 counts from the first argument load and saves full decoded
instructions. No source implementation or native class acceptance is claimed.

## Library placement indexing correction and real selector replay

The library reader stores zero-based section keys, while COFF relocation target
section numbers are one based. In pinned libcmt typinfo.obj this makes the
provider's COL reference look up a TypeDescriptor section instead of its COL.
An opt-in-only correction and a +1-only library-selection migration are staged
privately. The active reader, flag behavior and selection remain untouched.

- Five real-object/synthetic checks pass, including default indexing and weak
  externals remaining unresolved.
- All 405 selected slices / 16,730 bytes independently match their pinned archive
  members and the original reference. No relocation enters or crosses a selected
  slice. Eight source sections have relocations outside selected split slices.
- The actual current library selector was replayed against the original saved
  state/selection and a privately reindexed saved state/migrated selection.
  Both produce identical 405 pieces / 16,730 bytes and match the archived output.
- The replay retained 8,268 M3 ownership ranges, 15,437 accepted nonlibrary claims,
  7 chunks, 150,462 symbolic fields and 351,931 original relocation sites. No
  empty substitutes were supplied for its checks.

This is archived-state replay, not fresh placement, a fresh build or gameplay.
The six-section type_info chain matches non-relocation reference bytes, but
five sections overlap existing M3/W ownership and the weak deleting destructor
remains unresolved. The correction does not authorize an alias or overwrite.

## What remains and how to use these results

The next integration milestone is a fully reviewed opt-in indexing correction
with freshly generated placement state, migrated selection, exact image and
relocation verification, deliberate controls and gameplay. Fresh placement may
change results; the archived replay cannot substitute for those gates. Provider
ownership and weak-destructor semantics remain separate obligations.

For class work, retrieve the cards first, generate only declarations supported
by the PC evidence, and use the original compiler to check affected units.
Return-ABI conflicts, unknown type representations, source-view inheritance and
destructor/provider ownership go to an exception list. A name or equal size
never closes a class. Broader header extraction needs the actual project build
context before another whole-header trial.

Production coverage stays 1,613,018 / 1,979,392 initialized bytes; no new physical
coverage, game function bodies or complete native classes are claimed. No new
packages were downloaded in this continuation. No game/reference files were
uploaded, no commits/exports were made, and no full game build was run because
production inputs were unchanged.

Private receipts are under `runtime-next/m3/out/non-ai-continuation-20261119`:
`atlas-index/index.json`, `atlas-index-validation.json`,
`cross-source/comparison.json`, `field-shapes-v2/result.json`,
`field-shape-check/result.json`, `bool-abi-v2/result.json`,
`importer/FINDINGS.md`, `placement/archived-selector-replay.json`, and
`final-receipt.json`. The cross-source comparison found 174 exact debug/community
name joins: 72 have an equal-size alternative and 102 have only different sizes.
Only 9 same-spelling fields were comparable, with 3 offset differences. These
numbers describe a limited source overlap, not automatic compatibility.
