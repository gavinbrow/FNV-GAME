# Local Phase 2 work — 2026-11-19

Completed: the W103 positive/two-control/repeat suite and a fresh no-overrides
default build/gameplay are accepted. The 103-byte metadata conversion is now
the default. All four Terra workers are stopped and the build/gameplay lane is
idle. Protected source and recipe825d are unchanged.

Accepted output from this pass: **103 placeholder bytes replaced by five native
RTTI records; zero additional physical bytes covered; zero new function bodies;
zero fully reconciled native classes.** The larger counts below describe audited
evidence, not newly decompiled code. The 81.5% figure measures initialized binary
data coverage, not completion of Phase 2.

## Concrete results

| Work | Result | What it does not claim |
|---|---|---|
| Evidence retrieval grouping | All 12,739 packet IDs preserved. Repeated nonempty path sets group 2,341 surveys into 511 sets, 704 class-source packets into 187 sets, and 76 identity packets into 27 sets. | Shared paths do not establish identical types or removable jobs. |
| Fixed 20-class source sample | 862 exact indexed files checked against hashes; 1,328 lexical definitions grouped into 594 comparison groups. Three actual translation-unit contexts parsed without error-severity diagnostics. | Parser flags approximate VC2008; warnings, template lookup gaps and namespace/packing/ODR obligations remain explicit. |
| Retail command data | All 845 source-accessed rows checked. 844 fully covered by accepted data; one has an 8-byte uncovered prefix. All opcodes are sequential; 2,535 string pointers and 1,915 non-null handler targets pass bounded checks. | This is not proof of the full original arrays, native symbols or ownership. |
| Eight-byte fragment | Existing emitter produces the proposed two-pointer fragment privately. Both DIR32 sites and targets match exactly. | Not selected or counted as new coverage; alias/target/ownership and full integration gates remain. |
| Existing mapping leads | AutoMemContext's field semantics and the BGSTextureUseMap shell lead checked against current source and prior failures. | Neither supports an automatic class rename or a repair to the unit211 frame mismatch. |
| Already compiled placement backlog | All 67 administrative groups / 4,238 ranges / 190,878 bytes classified from saved metadata; three descriptor heads traced to archived objects and exact blockers. | No new selection-ready range certified from the ledgers alone. |
| Library pattern | 69 library RTTI0 records share a simple type_info relocation pattern; 12 have B-tier placement candidates. Existing project mappings corroborate the address, while provider ownership and library policy remain blockers. | No guessed alias or library-policy bypass was installed. |
| Unit775 cleanup | Guarded private proposal, eight isolated transaction tests, and an independent saved-object comparison: every parsed symbol and all sections except debug information agree. | Source not installed; no new class completion. Existing 32-function/30-EH fixture evidence is reused, not counted as new decompilation. |

## W103 verification and default

The bounded conversion replaces 103 W-placeholder bytes with five native,
compiler-generated unit620 RTTI records. The residual partition retains 1,499
bytes; all 61 original relocation sites are preserved (nine native, 52 residual).
No weak deleting-destructor fallback was enabled.

Corrected v4 positive and clean repeat pass the canonical executable hash,
exact 734,884-byte relocation directory, semantic menu/load/play/cell-change/
quicksave-load restoration and clean exit. Both deliberate controls fail the
round-trip check and change the image. Their only differences are the intended
payload field and independently verified derived PE checksum. All four actual
source-object checks pass 16 functions and 16 located EH checks each.

One earlier v3 run had a canonical executable and passing gameplay but omitted
the library-selection file from the actual frozen watch set; it remains
diagnostic. The corrected launch proves membership of all ten required pins
before building and records the additional verifier identities.

Fresh controls also exposed two verifier defects: successful no-harness status
was rejected, and the legitimate PE-checksum update was counted as an unrelated
mutation. The corrections preserve all byte/relocation/source checks, require
skipped gameplay for mutations, independently recompute both PE checksums and
reject every change outside the intended field/checksum. Four actual-auditor
in-memory tests accept the valid control and reject a wrong checksum, an
unrelated byte even with a recomputed checksum, and a missing mutation.

The staged default transaction changes exactly the canonical selection and its
digest in config.py. Its guard is bound to the completed suite's hash and checks
saved receipts, images, source preimages, locks and exact old/new payloads.
Four synthetic transaction tests and three bound-validator tests pass. The
fresh no-overrides default retry passed all artifact, saved-run, source-object
and semantic gameplay checks in `out/phase2-local-economy-default-retry-20261119`.
Its 12,714 frozen inputs remained stable. The final default receipt and accepted
ownership partition have been written.

The first fresh default attempt produced the same canonical image but failed
during menu/load: the process exited normally and screenshots did not show a
Continue confirmation. Its cause is unproven. That run remains failed, with
its own frozen inputs, summary, screenshots and captured artifacts. The fresh
retry used unchanged sources, harness and gates; no failed record was repaired
or relabelled. One successful retry does not establish the cause or fix of that
menu-input failure.

Physical initialized data coverage stays **1,613,018 / 1,979,392 bytes**. This
is an ownership/type improvement within existing coverage, not additional
coverage. The new split is M3 1,062,870 and DV1 550,148; five physical TLS bytes
remain separate. Protected C++ source and recipe825d are unchanged. No new
function bodies or fully reconciled native classes are claimed.

## Remaining work after these local routes

The source-view conflicts require supported native layouts, virtual contracts,
destructor/thunk identities and provider ownership. Identical names or lexical
fingerprints cannot settle them. Two sampled template records need a richer
identity join; modern Clang's parse success is not an original-compiler proof.

The command fragment needs final target/alias and integration evidence. Two
project descriptors intersect builder value-rule fields; the library descriptor
needs a supported resolver/provider model and a reviewed relocatable-library
path. These are recorded blockers, not reasons to override the current checks.
The larger external type database and additional recovery tools were not
downloaded or installed. Existing local Ghidra/Java and libclang were inspected;
another broad RTTI inventory would repeat facts already present.

Future work can retrieve shared evidence once, query existing mappings and
generate proposals for proven patterns. Agents should receive the unresolved
questions and conflicts. Keep small proven changes together for integration;
full image/gameplay verification has a substantial fixed local build cost.

## Private receipts and reusable local tools

All execution outputs are under
`runtime-next/m3/out/phase2-local-economy-20261119`:

- `evidence-groups/groups.json`: complete, lossless evidence grouping.
- `source-views/source-view-audit.json` and
  `full-context-probe/full-context-probe.json`: exact source observations.
- `commands/audit.json`, `schema-semantics.json` and
  `compiled-fragment/result.json`: command and private compile evidence.
- `reuse-placement/audit.json`, `three-descriptor-audit.json`,
  `ctype-typeinfo-audit.json`: mapping and placement findings.
- `pilot/independent-whole-object-review.json`: private source-cleanup evidence.
- `w103-v4-acceptance.json`: complete opt-in suite acceptance.
- `default-promotion/`: exact two-file payload, recovery guard and tests.
- `promoted-default-acceptance.json`: passing final fresh-default receipt.
- `accepted-partition-receipt.json`: guarded ownership-only metadata update.
- `final-local-receipt.json`: final scope, checks, limitations and evidence hashes.
- `ownership-recount.json`: independent source-byte ownership recount.

The helper scripts are local standard-library/libclang analyses or wrappers
around existing compilers/oracles. No web workers were dispatched, no MCP queue
was changed, no production decompilation source was rewritten, and no commits,
exports, uploads or downloads were performed.
