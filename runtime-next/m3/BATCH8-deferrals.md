# Phase 1 Batch 8 deferred work

The frozen final selection is `batch8_final_selection.json`, SHA-256 `42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7`. The archived positive M3 and DV1 ranges contribute **1,596,260 of 1,979,392 raw `.data` and `.rdata` bytes**. The observed range accounting and machine-readable category definitions are in `inventory/b8_deferred_accounting.json`; `BATCH8-candidate-review.md` records the independent selection checks. The independent archived-range audit is `out/batch8-promoted-default-verified/evidence/coverage-audit.json`; separate build verification checks the image and relocations.

The remaining 383,132 bytes outside selected object coverage partition without overlap as follows:

| Remaining category | Bytes |
|---|---:|
| Uncovered nonzero, outside recorded builder rewrites | 67,551 |
| Uncovered zero, outside recorded builder rewrites | 100,045 |
| DV1 produced but not spliced, outside recorded rewrites | 207,636 |
| Recorded builder rewrite union | 7,900 |

The historical 207,671 produced-but-unspliced figure includes 35 bytes in the rewrite union; do not add it to that union. These are raw-byte categories, not a complete semantic classification or a phase assignment for every byte. The recorded rewrite union covers imports/IAT and a conservative TLS-directory exclusion; see `BATCH8-verification.md` for the builder audit.

- **CRT-related interval, Phase 3 investigation:** `BATCH8-other-tail-review.md` documents `[0x01000001, 0x010113c0)`, containing 6,214 original relocation sites whose targets and names strongly suggest initializer/callback tables. Its leading historical char spelling does not establish ownership, exact table boundaries or every target's role. It overlaps the uncovered-byte categories above and is not an additional byte count.
- **Produced but unspliced data, Phase 2 investigation:** `DESIGN-phase1.md` identifies RTTI with synthetic names and vtables needing real class/method information as major blockers. The 207,636-byte raw category is a placement accounting total; individual bytes have not all been independently classified as RTTI or vtables. The user's 2026-11-18 go-ahead satisfies the separately established Phase 2 approval gate; source changes must use generators and preserve matching checks. Updated accounting and experimental results are in `phase2/RESULTS.md`.
- **Other uncovered declarations and tails:** arrays, conflicting types, aliases and declarations whose bounds or original ownership are not established remain evidence work. In particular, the accepted command records and strings are source-accessed prefixes, not claims about complete object extents; see `BATCH8-command-prefixes.md` and `BATCH8-other-tail-review.md`. Uncovered zeros remain file-backed bytes, not BSS, and require the same ownership and placement evidence as other file bytes.
- **Memory-only definitions:** 7,171 distinct DAT-containing unit symbol addresses occur in the `.data` virtual tail and contribute **zero file bytes**. `BATCH8-bss-readiness.md` and `inventory/b8_bss_definition_candidates.json` distinguish 1,584 metadata-level scalar candidates from cases needing further declaration, linkage or layout work. Their sizes and placements are not end-to-end verified.
- **Existing W scaffolding:** approximately 849 KB of already selected auto-typed W objects still need real source identity and types, ongoing alongside Phase 2. This is within the object contribution, not an additional remaining-byte category.

Passing the Batch 8 verification gate supports closing that scoped Phase 1 verification milestone with these explicit deferrals. It does not establish that all Phase 1 data, source identities, BSS definitions or later phase work are complete.

## Correction to historical nonzero provenance

The original raw `.data` and `.rdata` contain 1,282,880 nonzero bytes and 696,512 zero bytes. The Batch 7 line in `DESIGN-phase1.md` stating 757,854 nonzero bytes from objects is inconsistent with its own remaining-byte figures; the saved Batch 7 range partition gives **1,052,812 nonzero** and 506,851 zero bytes from objects, totaling 1,559,663. The historical remaining nonzero figures 96,921 uncovered plus 133,147 produced but unspliced equal 230,068; 1,282,880 minus 230,068 is 1,052,812. The historical entry is preserved rather than silently rewritten.

A read-only count of reference bytes over the archived pilot M3 and DV1 manifest ranges independently gives 702,377 + 353,030 = **1,055,407 nonzero**, and 326,842 + 180,257 = **507,099 zero**, totaling 1,562,506. These are counts of reference values at the archived metadata ranges, not an independent proof of the assembled image's provenance.

The final positive archived ranges cover reference values of **1,075,796 nonzero** and **520,464 zero**, totaling 1,596,260. The archived M3 portion is 722,766 nonzero and 340,207 zero; DV1 is 353,030 nonzero and 180,257 zero.
