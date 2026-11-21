# Prepared backlog grouping research — 2026-11-19

Scope: local prepared metadata for accepted recipe `825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68`; no source rescan, compiler, downloads or queue changes. These are leads and cost opportunities, not completed classes or measured savings.

The prepared 12,739 packets separate into 7,405 lexical identity surveys and 5,334 primary source/data packets. Surveys cover 86,938 unlinked lexical names / 173,865 declaration occurrences; they are not native class counts. Primary work includes 2,999 census class records, 35 unclassified table leads, 840 W packets for 6,218 ranges / 878,262 bytes, 689 file-backed packets for 5,815 intervals / 167,596 bytes, 770 BSS packets for 7,171 names, and one accepted private workflow test. The 67 local placement groups (4,238 intervals / 190,878 bytes) are a different axis; do not add them as independent types or assume unspliced bytes are unrecovered source. The 7,900 rewritten bytes remain separate.

## Grouping measurements

From the prepared job ledger, 2,341 of the 7,405 survey packets share an identical nonempty source-file set with another survey packet. For class packets, 704 of 2,566 source-recovery packets and 76 of 433 identity-recovery packets share an identical nonempty source-file set with another packet of the same kind. These counts overlap within each set and measure batching opportunities, not proven duplicate work or savings. A wider path-inverted index finds 3,011 survey source paths and 2,421 class-source paths referenced by at least two packets; prominent staging/generated files can cause misleadingly large clusters and should be capped/split by actual owning class and compile context. Packet context totals are 82,875,233 bytes for surveys and 69,099,636 for other packets; these are packet-level sums and repeat shared context.

Among 2,999 census class records, 433 have zero lexical definitions, 590 have one and 1,976 have two or more. 874 decorated RTTI names contain template encoding; this is a lexical count, not a family or compatible-specialization count. Across 3,268 observed vtable prefixes, 56,415 cells contain 12,693 distinct target addresses; 46,567 cells use a target repeated at least once. Repeated targets are prompts to reuse independent owner/body evidence, not proof of method signature, whole-table extent or class identity: shared thunks, no-op bodies and folding matter.

Hierarchy records provide useful prioritization edges: BaseFormComponent occurs as a non-root base in 516 records, NiMemObject 500, hkBaseObject 494, hkReferencedObject 493, NiRefObject 488, NiObject 410 and TESForm 141. These are observations in 2,833 hierarchy records, not distinct classes proven compatible or proof that a single base edit is safe. A proposed base change must enumerate affected include closures and function/EH checks, not dispatch hundreds of independent class jobs.

Existing `rtti_class_registry.py` and `rtti_scoped_registry.py` provide lexical/namespace leads and include/recipe relationships; the saved registry's 1,963 identifier groups include 1,134 multiple-definition groups. Their lexical fingerprints, path co-occurrence and class spelling cannot prove C++ scope, preprocessing, ABI or ODR identity. Reuse the pinned source evidence index, compiler-context receipt (58 recorded profiles), source offsets and mapped-method hints before requesting another survey. Their recorded contexts are navigation aids and do not substitute for full include/pack/macro closure.

Data work should stay partitioned: source-supported declarations within W can share declaration/consumer and initializer analysis; uncovered zero/nonzero file-backed ranges need independent object extent and relocation/ownership evidence; BSS needs definition/linkage/lifetime evidence and has no file bytes. Of 840 W packets, 453 lack source evidence; of 689 uncovered-global packets, 426 are held. Automatically batching held tickets does not make them dispatchable. Existing W split, native PSA metadata/selector proof, TESContainer unit980, TESForm/BGSE evidence, and the 825d positive/repeat/control receipts are reusable only under their pinned inputs and stated scope; no uninstalled hypothesis should be counted as accepted.

## Fixed 20-record pilot

These are exact census IDs and lexical breadth, selected for comparison, not asserted recovered identities. Definition/file counts are the ledger's lexical leads, not unique translation-unit definitions.

| Class packet | RTTI name | Definitions / source files | Why include |
|---|---|---:|---|
| P2N19-C-01186C58 | `.?AVTESContainer@@` | 31 / 29 | accepted bounded component baseline |
| P2N19-C-011831E8 | `.?AVTESModel@@` | 113 / 115 | shared component and slot-seven ambiguity |
| P2N19-C-011861BC | `.?AVBGSBodyPartData@@` | 13 / 24 | multiple inheritance and destructor ownership |
| P2N19-C-0118AAE0 | `.?AVImageSpaceModifierInstanceDOF@@` | 11 / 18 | related effect-class graph |
| P2N19-C-0118AB68 | `.?AVImageSpaceModifierInstanceDRB@@` | 2 / 10 | sibling effect-class graph |
| P2N19-C-011854FC | `.?AUNiMemObject@@` | 247 / 205 | allocation API and class-key scope |
| P2N19-C-011840DC | `.?AVBGSEncounterZone@@` | 9 / 18 | many surrogate views and slot evidence |
| P2N19-C-01183040 | `.?AVBaseFormComponent@@` | 123 / 83 | widely shared four-slot base |
| P2N19-C-01183028 | `.?AVTESForm@@` | 333 / 305 | large inherited interface and 333 lexical leads |
| P2N19-C-011854E0 | `.?AVNiRefObject@@` | 194 / 165 | reference-counted lifetime and ODR |
| P2N19-C-0118ACE0 | `.?AVhkBaseObject@@` | 58 / 115 | Havok shared base hypothesis |
| P2N19-C-0118ACBC | `.?AVhkReferencedObject@@` | 148 / 134 | Havok refcount/base relationships |
| P2N19-C-011B0310 | `.?AVhkaRaycastInterface@@` | 0 / 2 | unresolved caller ABI and deleting destructor |
| P2N19-C-011B05F8 | `.?AVbhkRagdollController@@` | 4 / 7 | multiple inheritance and array cleanup |
| P2N19-C-01196E04 | `.?AVBGSBodyPart@@` | 16 / 15 | existing native source and metadata evidence |
| P2N19-C-01186060 | `.?AVTESObjectTREE@@` | 11 / 30 | destructor/fold owner overlap |
| P2N19-C-01183004 | `.?AVBGSDehydrationStage@@` | 12 / 20 | large form-derived slot family |
| P2N19-C-011A8AE8 | `.?AVNiPoint3Interpolator@@` | 3 / 17 | smaller leaf with existing evidence |
| P2N19-C-01186834 | `.?AV?$NiTArray@IV?$NiTMallocInterface@I@@@@` | 71 / 73 | templated family, integer specialization |
| P2N19-C-0118C8BC | `.?AV?$NiTPrimitiveArray@PAVTESModel@@@@` | 51 / 51 | templated family, pointer specialization |

## Minimal deterministic pilot

1. Read the pinned ledger, source index, hierarchy and vtable census once. Assign every sample record one stable RTTI descriptor ID; index lexical source paths, target addresses and hierarchy edges while retaining provenance and all ambiguities. Use exact repeated path sets only to batch evidence retrieval, never to merge classes. Keep template arguments and nested scopes intact.
2. For each of the 20 records, retrieve existing project receipts and source/recipe context first; compare old and proposed source views under actual include, pack, macros, compiler and flags. A type is reusable only if those contexts and source-backed semantic/ABI facts are established; record conflicts explicitly. Treat repeated target addresses as leads to independently proven owners, not aliases.
3. Measure per record: facts reused, newly supported member/base/slot, unresolved contradictions, candidate prepared, isolated compile/EH/relocation result and any later accepted production change. Group true shared dependencies for one coordinator review, but run actual compile checks only in the established serialized lane. Do not expand to the rest of the queue until this sample shows useful incremental facts and no false merges.

No benchmark, import, compiler run or projected token reduction was performed in this review. The sample is a planning instrument, not an implementation or acceptance result.
