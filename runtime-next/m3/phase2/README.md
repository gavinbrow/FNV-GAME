# M3 Phase 2: classes, virtual tables and RTTI

Current workflow (2026-11-19): the web-agent backlog is prepared and a real
public MCP source/feedback test passed32 function and30 EH checks. See
[final tally and handoffs](WEB-JOBS-TALLY-20261119.md). Source recovery is still
open; the test proposal was not installed. The historical continuation below
does not resume paid workers or the paused production integration/build lane.

Current accepted checkpoint: `out/phase2-native-source-repeat`, recipe 825d,
1,613,018 initialized bytes (81.5%) plus five physical TLS bytes. The eight new
bytes form the native BGSBodyPart table; 1,100 functions, 389 ordinary EH
sections, eight requested tails, two fresh controls and clean semantic repeat
pass. Remaining raw bytes total 366,374, including 190,878 produced/unspliced.
PSA weak E and whole-class/type recovery remain open. The paragraphs below
retain earlier checkpoint counts; use `PROGRESS.md` and
`accepted_range_partition.json` for the current disjoint partition.


Phase 2 investigation started on 2026-11-18 with four Terra workers. The latest
bounded data batch is now the accepted default: 1,613,010 of 1,979,392 initialized
`.data`/`.rdata` bytes (81.5%), up 16,750 bytes from Phase 1. Positive, three mutation
controls, clean repeat and a fresh no-overrides default build/gameplay gate pass.
Investigation inventories do not establish recovered native class layouts.

The latest accepted source checkpoint is recipe `6757c8a0...8d0c`, archived at
`out/phase2-flags-script-repeat`: 235 functions, 14 EH tails, 33/78 observed
BGSE slots, canonical positive/repeat images, deliberate controls and semantic
gameplay pass. This changes source/type quality without adding raw coverage.
Whole Phase 2 remains open; current private fixture gates are in `PROGRESS.md`.

The earlier accepted batch combines 22 scalar entries / 114 bytes, 12 bounded arrays
/ 2,612 bytes, 370 library pieces / 6,374 bytes and a 20-byte TESContainer table.
Typing replaces existing W coverage; only the library and table add raw bytes.
The latest batch adds 364 source-view typed bytes within prior coverage and
35 library pieces / 10,356 new bytes. Current stable dataset and actual artifact
proofs are at `out/phase2-next-data-default-verified`; full classes remain open.
The isolated class-name experiment passed its 16-function comparison but
exposed an incompatible hierarchy. See `RESULTS.md` for the complete record.

The active continuation is working toward the full Phase 2 goal. A subsequent
seven-base hkp hierarchy hypothesis reproduces the observed graph fields and
preserves the 16 functions, but all four emitted vtables remain incomplete.
The named-class census, source-definition registry, shared-class merge
experiments and expanded array candidates are in progress. See `PROGRESS.md`
and `COMPLETION.md`; no native-class batch is accepted by those inventories.

## Work streams

- `RTTI-plan.md`: original class names, class-versus-struct identity, alias
  collisions and a bounded generator proposal.
- `VTABLE-plan.md`: original virtual slot order, method signatures, deleting
  destructors and base/derived binding evidence.
- `ACCOUNTING.md`: disjoint remaining-byte accounting and source-supported
  opportunities to replace existing W placeholders with actual scalar types.
- `VERIFICATION-plan.md`: isolated compiler/COFF checks, all affected functions,
  ownership, relocation and full-image/gameplay acceptance requirements.
- `HKP-HIERARCHY.md` and `LIBRARY-TRIAGE.md`: exact class-metadata mismatch
  and runtime-library placement leads for subsequent batches.

The machine-readable inventories are analysis evidence. A unit-map symbol at
an original vtable address is a lead; it does not establish a native class
layout, a virtual method signature, or a safe global rename. Current produced
metadata must be distinguished from the archived Phase 1 artifacts.

## First batch rules

Prepare deterministic, bounded generator outputs and review exact changes.
The user's 2026-11-18 go-ahead authorizes Phase 2 generator-backed work and
satisfies the handoff's prior approval requirement for this scope. Changes to
`fnv_decomp/src`, `include` and `build/units.json` must use generators and keep
the official matching gates. The TESContainer pilot has since been installed
through a guarded reviewed generator transaction for the active combined test;
its bounded batch is accepted, while global class consolidation remains open. Isolated
overlays, compiler products and copied game-derived material belong under
`m3/out/phase2-*`; never export or commit them. Preserve existing notices.

Run compiler experiments, full builds and gameplay serially through the
verification worker. Reuse the accepted default only after confirming its
input hashes. New behavior remains opt-in until complete acceptance, including
new-range negative controls and semantic save/cell restoration, passes.

The linked acceptance evidence covers this bounded batch. Whole Phase 2 remains open.
