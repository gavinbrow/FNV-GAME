# hkpConstraintViewer hierarchy evidence

Read-only analysis of the original reference RTTI records and the private unit-2501 overlay object is recorded in `out/phase2-hkp-constraint-viewer/hierarchy-analysis.json`; `rtti_hierarchy_analysis.py` reproduces the metadata using exclusive output. No source, selection, compiler output or current build was changed. These are observed x86 RTTI records and source-surrogate names, not independent proof of semantic inheritance or correct vtable implementations.

The four original complete-object locators all point to the same type descriptor and class hierarchy. Their subobject offsets are 0, 8, 32 and 40, with signature and constructor displacement zero. The overlay emits four locators with those same numeric fields. That agreement does **not** establish equivalent hierarchy or slot targets: the original hierarchy descriptor has signature 0, attributes `0x1` and seven preorder base descriptors; the overlay has signature 0, attributes `0x1` and six.

| Original descriptor name | Contained bases | PMD `(mdisp, pdisp, vdisp)` | Attributes |
|---|---:|---|---|
| `hkpConstraintViewer` | 6 | `(0, -1, 0)` | `0x40` |
| `hkpWorldViewerBase` | 4 | `(0, -1, 0)` | `0x40` |
| `hkReferencedObject` | 1 | `(0, -1, 0)` | `0x40` |
| `hkBaseObject` | 0 | `(0, -1, 0)` | `0x40` |
| `hkProcess` | 0 | `(8, -1, 0)` | `0x40` |
| `hkpPhysicsContextWorldListener` | 0 | `(32, -1, 0)` | `0x4d` |
| `hkpWorldPostSimulationListener` | 0 | `(40, -1, 0)` | `0x4d` |

The overlay preorder is `hkpConstraintViewer`, `D698B0Base`, `D698B0BaseA`, `D698B0BaseB`, `D698B0BaseC`, `D698B0Listener`; contained-base counts are 5, 3, 0, 0, 0, 0. Their PMDs are respectively `(0,-1,0)`, `(0,-1,0)`, `(0,-1,0)`, `(8,-1,0)`, `(32,-1,0)`, `(40,-1,0)`, and all have attributes `0x40`. In particular, the final two original descriptors have different attributes (`0x4d`), and the original has an extra base descriptor. Equal offsets alone do not prove that a surrogate corresponds to a particular original type, nor that changing base names alone would recreate the graph.

The isolated rename can produce the matched type-name descriptor, but the emitted hierarchy and dependent base-array records remain incompatible. Keep these records and vtables deferred. A safe next proposal is an evidence-only graph specification that records each original descriptor, preorder relationship, access/attribute interpretation and required source methods; independently verify those relationships against source and MSVC ABI before generating any reconstructed hierarchy. Only after that review should an isolated hierarchy overlay be proposed. Preserve the existing 40-byte W owner and the Phase 1 selection until separate byte/relocation and overlap checks prove a replacement.

## Later seven-base isolated hypothesis

A separate deterministic overlay (`rtti_hkp_hierarchy_overlay.py`) adds the reference-observed `hkBaseObject` under `hkReferencedObject`, maps the other local surrogate base names to their observed native names, and tests protected listener inheritance. The related `hkpVehicleViewer` source independently declares `hkpWorldViewerBase` with a protected `hkpPhysicsContextWorldListener`; it does not independently prove the exact constraint viewer's access or full ABI. Other translation units contain many declarations of these native names, so compatibility and ODR identity remain unverified.

The verification worker compiled the isolated hierarchy overlay with the pinned unit-2501 VC2008 SP1 recipe. The private `coff-hierarchy-comparison.json` reports all 16 mapped function bodies and normalized code relocations equal to the original object, all 16 matching the reference comparator, and seven of seven observed preorder base names/counts/PMDs/attributes equal to the original. Four locator offsets also agree. This is a material improvement over the earlier name-only overlay, but numeric/identity graph matching alone does not establish independent reference-resolved metadata placement or source-level identity.

The generic `class_metadata_compare.py` finds four emitted tables and four matching reference graph-field sets, but each emitted table contains only one slot. The observed code-pointer prefix counts for locator offsets 0/8/32/40 are 3/7/3/3, and none of the four emitted placeholder slot targets resolves via normal source maps. All four vtables therefore remain incomplete and cannot be integrated as native replacements. This check does not assert complete original vtable extents beyond the observed prefix.

`rtti_hkp_owner_split.py` also prepares an uninstalled ownership proposal for the currently selected 40-byte W object: a 34-byte emitted type descriptor followed by a six-byte W tail, whose two zero bytes precede the original relocation at tail offset 2 to `0x0101142c`. The existing W self-check model accepts that target and rejects a changed target. A private actual-compiler tail fixture is queued; descriptor import, actual combined placement, vtable repair, nonoverlap and full-image controls remain separate gates. These are ownership/type improvements inside already-produced bytes, not new byte coverage.
