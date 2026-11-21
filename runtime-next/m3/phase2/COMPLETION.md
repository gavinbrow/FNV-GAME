# Phase 2 completion requirements

The active user goal is to finish Phase 2, with Terra workers. The first scalar
experiment is one small part of that goal. Passing its remaining controls does
not close the class, inheritance, virtual-method or placeholder-type work.

The phase definition in `PLAN-M3.md` requires a header per native class, original
virtual-function order and compiler-emitted RTTI/vtables, with constructors no
longer storing hard-coded vtable addresses. W scaffolding must gain supported
types alongside this work. Preserve all original function matching gates.

## Evidence required

1. A reconciled class/subobject registry covering the reference metadata,
   existing source definitions and all unit aliases. Each class needs supported
   kind/name, namespace/template identity, inheritance/access, subobject layout,
   virtual signatures/order, overrides and deleting-destructor behavior. A
   lexical name match or a shared original address is not sufficient.
2. Deterministic generators for the corresponding headers/source/recipe edits,
   including affected include closures and conflicting surrogate declarations.
   All affected functions must pass the unchanged compiler/relocation matching
   gates, including EH and thunks. Constructors must use the native class model.
3. Exact compiler-generated class-data records and references, with original
   relocation sites, proven ownership/extent and no W-remainder loss or overlap.
   Record newly placed bytes separately from improved types within old coverage.
4. Source-supported replacement of placeholder types. Preserve unresolved
   extents and aliases explicitly during work; they are not completed native
   types merely because the compiler can reproduce reference bytes.
5. For every accepted integration batch: frozen inputs, canonical executable,
   exact relocation directory, deliberate value/pointer controls that fail the
   round-trip check and change the image, semantic gameplay/save/cell/exit
   verification, complete saved-run checks and clean repeats before promotion.
6. Reconcile every remaining class/type item against those requirements before
   claiming whole-phase completion. Startup/TLS/EH ordering and the standard
   linked-build crash remain later-phase gates, not substitutes for Phase 2.

## Current measurable baseline

`native_class_inventory.py` reads file-backed, relocated x86 RTTI records and
checks complete locator/base-array chains and preorder interval consistency.
Its private `out/phase2-class-census/census-v2.json` records:

- 2,999 recognized class/struct type descriptors;
- 2,833 hierarchy records;
- 3,268 RTTI-prefaced table leads with a contiguous relocated code-pointer prefix;
- 2,682 distinct locator root type descriptors;
- 2,187 table leads with unit vtable-symbol mappings and 35 mapped addresses
  rejected by these structural checks;
- 1,520 simple names with a lexical source definition somewhere.

A separate scan found 3,000 `.data` class/struct-name prefixes; 2,999 passed the
same header/name invariants. Seven synthetic tests check malformed input,
file backing, relocation requirements, subtree boundaries and code-prefix
termination. Those counts describe observed records and discovery limits, not
recovered native classes or a whole-phase completion percentage. Tables without
recognized RTTI, null/interrupted pointer runs, source-only types, preprocessor
branches, templates/namespaces, class extent and all virtual signatures still
need reconciliation. No class is automatically admitted by the census.

The accepted default is the native-source batch (81.5% initialized data-byte
coverage), verified at `out/phase2-native-source-repeat`: recipe 825d,
1,100 functions, 389 ordinary EH sections, eight tails, exact image/relocations,
two fresh controls and semantic positive/repeat gameplay pass. Coverage is
1,613,018 bytes; PSA weak E and the whole class registry remain open.
The preceding next-data batch at `out/phase2-next-data-default-verified` retains
positive/three controls/repeat/fresh default, exact image/relocations and
semantic gameplay. Its 364 source-view typed bytes preserve old coverage;
35 library pieces add 10,356 raw bytes. These are bounded milestones.
The preceding accepted source snapshot is recipe `6757c8a0...8d0c`, with complete
bounded positive/control/repeat evidence at `out/phase2-flags-script-repeat`.
It preserves that byte coverage and does not close the class registry.
It includes a local TESContainer source/header/table pilot, native scalars and
bounded arrays, and whole compiler-library pieces. No whole native-class
registry or global class-consolidation milestone is claimed. Four workers currently
own class/header recovery, virtual/destructor resolution, W/library data, and
the exclusive compiler/build/gameplay lane. The coordinator owns independent
review, the cross-class census and integration.
