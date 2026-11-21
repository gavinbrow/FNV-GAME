# Research decision: reduce Phase 2 model usage

2026-11-19. Four existing Terra workers completed bounded independent research;
the coordinator reviewed their reports, checked public examples and independently
recomputed the repeated-path-set and class-definition counts. This is research
and metadata analysis, not a source integration or completed-class milestone.
No bulk archive downloads, new dependency installs, compiler/gameplay runs or
queue/source/server changes were made. The active research workers have stopped.

## Decision

Use existing metadata and deterministic extraction as the default evidence path.
Retain web agents for concrete unresolved questions after those paths have been
checked. Do not dispatch the prepared queue as thousands of unrelated reasoning
tasks, and do not start another general reverse-engineering tooling project.

The compiler remains the final local verifier of a source candidate. Running
existing scripts and reviewing compact exception reports can avoid a model turn
for every successful compile. Compilation cannot be omitted while retaining
the project's exact function/EH/relocation and image requirements.

## Measured reasons to change scheduling

The 12,739-packet inventory is not a count of undecompiled functions. In the
frozen job ledger:

| Kind | Packets | Packets in repeated identical nonempty source-file sets | Repeated sets |
|---|---:|---:|---:|
| Source-name surveys | 7,405 | 2,341 | 511 |
| Class source recovery | 2,566 | 704 | 187 |
| Class identity investigation | 433 | 76 | 27 |

These are evidence-retrieval batching opportunities, not safely removable jobs.
Source paths, lexical fingerprints and shared code addresses do not establish
C++ identity, preprocessing state, layout or compatible declarations.

The 2,999 class records split into 433 with no lexical definition, 590 with one
and 1,976 with multiple definitions; 874 names have template encodings. Existing
metadata is therefore sufficient to separate missing evidence, repeated source
views and template-family work before invoking a model. The proposed 20-record
sample in RESEARCH-BACKLOG-20261119.md was checked: all 20 unique IDs exist in the
frozen class ledger.

That report also measures shared bases in hundreds of hierarchy records. Reuse
their existing proofs and explicitly track dependencies. This is not a proposal
to replace a shared base across hundreds of consumers in one speculative edit;
the previous NiRefObject/NiMem experiments already demonstrate why that fails.

## Concrete public leads, beyond a generic tool list

1. [The public field mapping](https://raw.githubusercontent.com/mathisto/fnv_decomp/pdb-names-mapping/fields.jsonl)
   identifies AutoMemContext's offset-zero field as a previous-context value of
   type MEM_CONTEXT. This supports field semantics for an existing local case;
   it does not repair the known unit211 stack/EH mismatch.
2. [The class mapping](https://raw.githubusercontent.com/mathisto/fnv_decomp/pdb-names-mapping/classes.jsonl)
   links the existing FUN_004aa3d0_shell to BGSTextureUseMap through Xbox methods.
   Its source/evidence fields must remain attached. This is an identity lead
   even though the checked local PC RTTI census has no such descriptor, not a
   proven rename or completed PC class.
3. [Current upstream TESModel.h](https://github.com/momusdigital/fnv_decomp/blob/main/include/TESModel.h)
   supplies a pointer-returning GetAsModelMaterialSwap declaration where a
   community header instead has an unknown boolean virtual. It is a useful
   signature candidate for our unresolved slot question, subject to exact
   PC slot/caller, const and compiler verification.
4. [Current upstream DOF](https://github.com/momusdigital/fnv_decomp/blob/main/include/ImageSpaceModifierInstanceDOF.h)
   contains class/base/field and enum declarations, while
   [BGSBodyPartData](https://github.com/momusdigital/fnv_decomp/blob/main/include/BGSBodyPartData.h)
   declares three bases. These provide specific material to compare with local
   views; they do not authorize replacing our frozen tree or prove all consumers
   and native metadata match. These exact header paths were absent locally.
5. [xNVSE CommandInfo](https://github.com/xNVSE/NVSE/blob/master/nvse/nvse/CommandTable.h)
   supplies a reusable 0x28 record schema with parameter and handler fields.
   Repeated retail records can be checked by a rule once their original extents
   and pointer identities are established, rather than guessed row by row.
   Plugin registrations must remain separate from retail command records.

All upstream branches cited here move over time. Pin commits and hashes before
turning any of these observations into generator input. Existing reports record
source provenance; public visibility alone does not authorize copying code under
our license.

## Ranked routes

| Order | Route | Why this order | Success evidence |
|---|---|---|---|
| 1 | Query small existing mappings and compare saved local facts | New field/identity examples were actually inspected; no large database or toolchain is needed to establish initial usefulness. | Discriminating new fact with provenance and independent PC support. |
| 2 | Group source views using existing indexes, then bounded compiler-AST extraction | Much of the backlog concerns repeated declarations rather than missing machine-code bodies. Existing source indexes and 58 recorded compiler profiles provide a starting point. | Correctly separated compatible/conflicting views on a fixed sample, with no parse failures concealed. Modern Clang remains an extractor, not the VC2008 ABI authority. |
| 3 | Analyze repeated data by verified schema | Command/settings/other descriptor families may support one generator rule across many records. | Exact extents, members, relocations and residual partition; a pattern match alone is insufficient. |
| 4 | Query the richer FNV source atlas | [Its data model](https://github.com/amarkham23/fnv-source-atlas/blob/main/docs/DATA_MODEL.md) includes CodeView member/layout, method and typed-global records plus PC/Xbox alternatives. | Targeted needed type facts actually present and corroborated on PC. The published database has not been downloaded or queried here. |
| 5 | Targeted Ghidra class recovery or BTIGhidra inference | May add constructor/member evidence when source and debug records are insufficient. | A new supported answer for a previously named unresolved question; names/padding alone do not count. |
| 6 | OOAnalyzer or another whole decompiler | Greater setup cost and unmeasured target compatibility. Ordinary RetDec output does not directly address our existing matching-body/type-reconciliation problem. | Use only after a simpler route fails and the tool has a precise question to answer. |

No route has yet demonstrated an accepted production change from this research.
Do not express the grouping counts or tool-paper accuracy as a percentage of
Phase 2 completed or a promised token saving.

## Small executable research sequence

Start with the two public mapping cases above, recording existing/new/unknown
facts and exact PC corroboration. Then use the fixed 20 native-class records as
the comparison set for source-view extraction and available metadata. Separately
compare 10 previously accepted retail command records and 10 unresolved records
only where their original extents are independently known; stop that branch if
no such unresolved sample exists. Do not manufacture records to meet a quota.

Track the number of genuinely new supported facts, actual source candidates,
successful native checks and later accepted integrations as separate measures,
along with setup time and model effort. A route that only rediscovers known
facts stops. A useful route expands by a deterministic query/generator rule,
then sends its unresolved exceptions to agents. Whole image and gameplay gates
remain batched integration work under the existing locks.

## Research reports

- [Prepared backlog and exact 20-record sample](RESEARCH-BACKLOG-20261119.md)
- [Debug type/mapping evidence](RESEARCH-TYPES-20261119.md)
- [Community headers and structured data](RESEARCH-COMMUNITY-20261119.md)
- [Ghidra/OOAnalyzer/source AST assessment](RESEARCH-AUTOMATION-20261119.md)
- [BTIGhidra/Retypd and decompiler alternatives](RESEARCH-TYPE-INFERENCE-20261119.md)

The earlier NON-AI-RESEARCH-20261119.md is the initial survey. This decision
records the additional worker research and measured local grouping, not a
replacement of the accepted build or frozen MCP job manifests.
