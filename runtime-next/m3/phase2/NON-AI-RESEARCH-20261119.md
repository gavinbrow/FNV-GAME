# Phase 2: existing evidence and non-AI alternatives

Research date: 2026-11-19. This is a research recommendation, not an integration
receipt. No workers were started, queue records changed, packages installed,
release archives downloaded, source proposals applied, or builds run.

## Finding

Processing the entire prepared queue through individual AI investigations is
not the best default. Prioritize evidence reuse and deterministic analysis,
then use agents for unresolved source questions. Compilation remains necessary
for this project's exact matching requirement, but compilation and automated
comparison do not themselves consume model tokens.

The prepared count is a coverage inventory, not a count of functions still to
decompile. In particular, 7,405 of 12,739 packets are source identity surveys.
Their 86,938 lexical names are not 86,938 distinct native classes. The remaining
5,334 packets include class investigations, data typing, BSS work, and the
accepted private workflow test; they are not all new function implementations.
The separate 67 placement groups concern 190,878 bytes already compiled but
not placed. Placement still needs symbol, extent, relocation, and ownership
proof; it is not necessarily a simple copy operation.

Sources for local counts: the existing final job tally and
`../out/phase2-web-backlog-20261119/summary.json`. No census was rerun.

## Existing public work worth evaluating

| Resource | Verified capability or published contents | Application and limit |
|---|---|---|
| [FNV source atlas](https://github.com/amarkham23/fnv-source-atlas/blob/main/README.md) and [v0.5.0 release](https://github.com/amarkham23/fnv-source-atlas/releases/tag/v0.5.0) | PC/Xbox mapping tools and a queryable database with extracted CodeView types, members, signatures, virtual-table observations and typed globals. Published archive is about 752 MiB compressed / 3.93 GiB extracted. | Strong candidate for replacing missing-evidence investigations with database lookups. Xbox observations are leads for the PC target, not interchangeable addresses/layouts. Release contents and mapping accuracy have not been tested locally. The tooling license does not license the database's third-party material. |
| [1001Bits/BethesdaGhidraScripts](https://github.com/1001Bits/BethesdaGhidraScripts) | Explicit PC New Vegas 1.4.0.525 x86 support, xNVSE-derived types, Clang header parsing, generated importers and additional binary analysis passes. | Evaluate on an isolated analysis project. Distinguish source-backed types from inferred names. The upstream doodlum project alone is not the same FNV-supporting fork. README support was verified; no importer was installed or executed. |
| [xNVSE GameForms.h](https://github.com/xNVSE/NVSE/blob/master/nvse/nvse/GameForms.h), [yUI CommonLib TESContainer](https://github.com/yvileapsis/yUI-NVSE/blob/main/CommonLib/Bethesda/TESContainer.hpp), [JohnnyGuitar](https://github.com/carxt/JohnnyGuitarNVSE) | Community declarations, offsets, class relationships and plugin-facing interfaces already exist. TESContainer has a documented 0xC layout. | Compare specific declarations rather than reconstructing everything afresh. Plugin declarations may be partial or intentionally model binary interfaces differently. Preserve source provenance and applicable licenses. |
| [Current momusdigital source](https://github.com/momusdigital/fnv_decomp), [PDB naming documentation](https://github.com/momusdigital/fnv_decomp/blob/main/PDB_NAMES.md) | This is already our upstream source base. Current online documentation also describes automated PC/Xbox naming links and machine-readable mapping records. | Check upstream deltas and the referenced mapping branch before duplicating work. A newer upstream result is not automatically compatible with our frozen recipe. Do not merge or replace the live tree during research. The published function-match total does not claim a standalone rebuilt game. |

One concrete caution: the inspected xNVSE BGSBodyPartData declaration represents
TESModel and BGSPreloadable as members, while
[yUI's declaration](https://github.com/yvileapsis/yUI-NVSE/blob/main/CommonLib/Bethesda/BGSBodyPartData.hpp)
uses multiple inheritance. Both describe size 0x74. This illustrates why matching
size and class spelling alone cannot establish the native inheritance model.
It does not establish which declaration should be installed in our project.

Another specific lead: [yUI's TESModel header](https://github.com/yvileapsis/yUI-NVSE/blob/main/CommonLib/Bethesda/TESModel.hpp)
includes an unknown virtual at slot 7. Our existing TESMODEL-SLOT7-OWNERSHIP.md
already establishes an eight-entry family but leaves the exact semantic
signature unresolved. The community header is additional evidence to compare,
not proof that its proposed return type is correct.

## Non-AI recovery tools

| Tool | What it can do | Limitation relevant here |
|---|---|---|
| [Ghidra RecoverClassesFromRTTIScript](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/Decompiler/ghidra_scripts/RecoverClassesFromRTTIScript.java) | Uses RTTI to recover hierarchies and identify constructors/destructors; uses PDB types when present and decompiler data flow otherwise. | Its own documentation calls it a prototype. Inferred members can remain undefined placeholders. Existing local RTTI extraction already covers part of this work; measure incremental output rather than counting it all as new. |
| [CMU Pharos / OOAnalyzer](https://github.com/cmu-sei/pharos) | Specifically supports 32-bit x86 Microsoft C++ programs. Uses symbolic analysis and Prolog rules to recover class/method associations, members and inheritance. | Good architectural fit for this target; not demonstrated here on FNV. It is a research tool with setup and analysis costs. Try only if the simpler evidence sources leave a concrete gap. Its published corpus accuracy is not an FNV completion estimate. |
| [LLVM llvm-pdbutil](https://www.llvm.org/docs/CommandGuide/llvm-pdbutil.html) | Dumps types, classes, globals and symbol records from PDBs without AI. | Needs actual debug information. An executable's PDB path or a generated names-only PDB cannot supply missing original type records. Xbox compiler debug data requires PC corroboration. |
| [Google BinDiff](https://github.com/google/bindiff) | Matches similar functions and can transfer analysis names/comments; supports Ghidra through its disassembly export workflow. | Useful for comparable binaries, especially another PC build or editor. Similarity is evidence, not exact source or cross-platform layout proof. Do not assume Xbox PowerPC-to-PC matching is automatic. |
| [ReClass.NET](https://github.com/ReClassNET/ReClass.NET) | Runtime memory inspection, RTTI display, node dissection and C++ structure generation. | A focused fallback for fields not resolved statically. Observation needs controlled experiments; an automatically generated padded structure is not a completed semantic type. |

The Ghidra script explicitly distinguishes recovered data from assumed types.
[CMU's OOAnalyzer paper](https://www.sei.cmu.edu/library/using-logic-programming-to-recover-c-classes-and-methods-from-compiled-executables/)
also demonstrates automated recovery, rather than a guarantee of exact original
source. These are ways to reduce manual reasoning, not replacements for the
existing byte/EH/relocation checks.

## What can be extracted, and what cannot

The PC executable is already a source of class names, RTTI base graphs, vtable
targets, literals, initialization patterns and field accesses. Local
native_class_inventory/rtti tools and the final job census have already used
some of this evidence. Repeat extraction only to obtain something missing,
such as field constraints, special-member associations or normalized identities.

Debug type records, when available, can recover substantially more names and
type information than RTTI alone. They generally do not contain the original
function implementation text. Optimization also erases or merges distinctions
that cannot reliably be reconstructed from executable bytes alone.

I did not establish the existence of a publicly available complete original PC
retail source tree or an exact full PC retail PDB that solves this phase. The
other [ieee802dot11ac/fnv project](https://github.com/ieee802dot11ac/fnv) targets
an Xbox 360 MemDebug executable and is work in progress, not a drop-in PC source
replacement. The current momusdigital project is already our starting point.

## Recommended next experiment before spending on the queue

1. Keep broad worker dispatch stopped. Treat the 7,405 survey packets as a
   searchable index until a concrete source change needs one. Do not send every
   lexical name to an agent by default.
2. Check for already-held public metadata first, then evaluate a pinned version
   of the atlas, upstream mapping records and community headers. Preserve each
   fact's platform, build, provenance and confidence. Bulk downloads remain a
   separate action under the workspace's download rule.
3. Benchmark a fixed sample of 20 representative native class records: simple
   leaf classes, shared form components, multiple inheritance, templates and
   destructor-sensitive cases. Include TESContainer, TESModel and BGSBodyPartData.
   Query/import/extract once per evidence source; do not build a new general
   framework before proving a useful missing fact.
4. For each sample record, count independently: existing evidence reused;
   newly supported bases/members/slots; unresolved conflicts; usable source
   candidate; successful isolated native check; accepted production change.
   A name import is not a recovered class. Record wall time and model usage.
5. Generate compatible declarations and repeated table/data patterns by rules
   where evidence is sufficient. Group source views using actual preprocessor,
   namespace, pack and compiler contexts; never merge by spelling alone.
6. Run the existing compiler/comparison tools directly for affected units,
   serially under the current locks. Cache results only with complete matching
   input/dependency identities. One coordinator reviews exceptions and reports
   results; it need not spend a model turn on each successful compiler operation.
7. Send only the unresolved, valuable cases to web agents. Integrate compatible
   passing changes in batches, preserving the existing image, negative-control,
   relocation and gameplay gates. Do not redefine Phase 2 completion merely to
   reduce the count.

The first outcome to seek is measured reduction in unresolved work on this
sample. No percentage saving, whole-phase delivery date, or guaranteed class
completion rate is supported yet. If imports mostly duplicate local knowledge,
report that and stop that route rather than building another tooling layer.

Prepared MCP packets remain useful as stable evidence containers and as the
residual exception queue. They do not need to dictate the recovery algorithm.
