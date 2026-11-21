# Non-AI route benchmark â€” 2026-11-19

The requested trials are complete. The atlas/database route and community
header-extraction route produced useful real outputs. Bounded Ghidra class
recovery failed on an analysis/model prerequisite and is not a demonstrated
recovery route here. No production source/default, MCP job or game image was
changed. These are tooling/evidence results, not completed native classes.

## 1. Debug-type database: successful actual experiment

Downloaded the pinned [FNV source atlas v0.5.0](https://github.com/amarkham23/fnv-source-atlas/releases/tag/v0.5.0)
archive (788,788,765 bytes), verified its published SHA-256, extracted the
4,222,132,224-byte SQLite database, verified its own checksum and passed SQLite
quick_check. Queries use readonly immutable SQLite mode; no server is needed.
The total download/verification/extraction receipt records about 35 seconds.

The fixed 20-class sample produced exact CodeView unique-name definition
matches for all 20 in 0.594 seconds. Nineteen have one definition; TESContainer
has two alternatives retained separately. This includes the two template
specializations and hkaRaycastInterface, for which our lexical source index
had no definition. Extracted sample occurrences: 137 data members, 776 single
method entries and 135 overloads, including duplicate alternatives. These are
record occurrences, not newly recovered facts or distinct finished methods.

PC RTTI direct-base names agree for all 20; direct-base offsets agree for 18.
BGSBodyPartData and TESObjectTREE have different secondary-base offsets.
Even base-offset agreement is insufficient: Xbox TESForm is 40 bytes whereas
the accepted PC view is 24. BGSBodyPartData's Xbox size is 132 versus PC116.
No uniform platform-offset adjustment was applied.

A single availability join across the existing PC census finds:

| Existing PC class records | Exact Xbox debug definitions |
|---|---:|
| One definition | 2,224 |
| Multiple alternatives | 39 |
| No exact definition | 736 |
| Total with at least one definition | 2,263 of 2,999 |

This is evidence availability, not a Phase2 completion percentage or guaranteed
agent savings. Full facts were exported only for the fixed20 sample. Missing
exact matches can include identity/platform differences, not just missing code.

Two concrete uses:

- TESModel has GetAsModelTextureSwap returning TESModelTextureSwap* at virtual
  byte offset28. Independent PC reference reads verify the corresponding
  null-return and this-return methods in TESModel/TextureSwap tables. This adds
  semantic/debug evidence supporting the accepted pointer-return view, without
  proving every member, destructor provider or cross-unit definition.
- hkaRaycastInterface supplies two castRay signatures and virtual offsets4/8,
  plus a destructor at0. A private declaration/dispatch probe generated from
  those records was compiled with the actual MSVC2008 SP1 compiler. Straight
  record-order emission produced offsets8/4; reversing the overload group
  produced4/8. Both outcomes are asserted against decoded COFF instructions.
  This demonstrates a necessary generator rule; it is not a whole-class retail
  byte match. The probe adapts Xbox calling convention to PC member convention,
  uses debug-derived hkBool storage and forward-declared vector types, and does
  not implement constructors/destructors or establish complete return ABI.

Reusable local files: `atlas/benchmark.py`, `benchmark.json`, `class-cards/`,
`census-presence.json`, `pc_crosscheck.py`, `pc-crosschecks.json`,
`native_probe.py`, `native-probe/result.json`, and database/download receipts.

## 2. Community type importer: successful extraction/generation

Pinned [BethesdaGhidraScripts](https://github.com/1001Bits/BethesdaGhidraScripts)
v1.2.2 at dabb919186e0dde601908adfa5b174f699525b66 and its xNVSE gitlink
68047f86558f1c4663f0c312e67780af4e85c6bc. Initial execution returned zero types
because clang.exe was absent. Downloaded its pinned portable LLVM20.1.8 archive
(939,541,912 bytes), verified the locked hash, and extracted the executable and
resource headers privately, without a system install.

The real upstream pipeline then produced **41 enums, 2,499 structures and
103 vtable structures**, and generated its target-identified xNVSE-only Ghidra
script. The script was not executed in Ghidra. Optional PDB-derived merges were
excluded. A separate in-process libclang parse extracted all three requested
sample definitions at sizes12/24/116; it is distinct from the successful real
pipeline. Diagnostics were suppressed by upstream flags, not a warning-clean
native compiler proof.

Important output defects/limits: TESModel and TESContainer generated empty
virtual-method lists despite header declarations; BGSBodyPartData represents
TESModel/BGSPreloadable as member fields instead of the local base views. Some
entries are opaque or synthesized template placeholders. The2,499 count is
therefore not 2,499 native class recoveries. Pinned xNVSE TESModel stops at slot06
and does not supply slot07. Do not bulk-copy this output into production C++.

See `community/FINDINGS.md`, `result.json`, `upstream-result.json`,
`run_upstream.py`, and the generated-script/compiler download receipts.

## 3. Traditional class recovery: bounded negative result

Installed Ghidra12.1.4/Java21 were actually executed. Docker CLI was available
but its Linux engine was not, so OOAnalyzer was not run. Isolated headless RTTI
probes used both an archived rebuilt PE and the exact original decrypted PC
reference. With normal analysis disabled, the original-reference analyzer
returned true but emitted Visual Studio PE model errors and produced zero class
symbols/RTTI labels. A short standard-analysis attempt exceeded its requested
time limit and was stopped. Address selection did not bound internal scanning.

This is a setup/model failure, not evidence of absent RTTI or a successful class
recovery. No additional recovered classes are claimed beyond our existing census.
Do not spend on OOAnalyzer/container setup or repeat whole-image analysis until
there is a specific residual question and a reproducible compatible setup.
See `recovery/RESULT.md` and `recovery/result.json` for scripts, command logs,
versions and final worker findings.

## Decision and next work

Use the atlas as the first evidence source, then community declarations. Generate
proposals with deterministic queries/rules and test affected units locally. Send
unresolved platform, ownership, layout and method conflicts to agents, rather
than treating every prepared packet as an independent AI reconstruction task.
The downloaded corpus and toolchain are cached for reuse.

The next source batch should use a small platform-compatible family, retaining
all ambiguities, with exact PC field/vtable/constructor/destructor checks and
original-compiler function/EH/relocation verification. Only passing proposals
proceed to batched image/control/gameplay gates. This trial installed no native
classes and changed no binary coverage. No complete original source leak was
obtained; debug records and community declarations are partial evidence sources.
No function implementation text is recovered by a type lookup.

Full private outputs: `runtime-next/m3/out/non-ai-benchmark-20261119`.
