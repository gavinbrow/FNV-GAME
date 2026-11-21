# Batch 8 independent candidate review

The current four candidate inventories were independently checked against the reference bytes and frozen Batch 7 ranges. All intervals are half-open. This is a candidate review, not a build or validation of the final selection, the generated objects, or the completeness of the known rewritten-range list.

| Inventory | Entries | Bytes | Zero | Nonzero |
|---|---:|---:|---:|---:|
| Other names | 26 | 41 | 5 | 36 |
| Conflicting/non-scalar type heads | 16 | 53 | 33 | 20 |
| Pointer candidates | 8 | 32 | 0 | 32 |
| Declared zero scalars | 10 | 29 | 29 | 0 |
| Total | 60 | 155 | 67 | 88 |

All 60 are mutually disjoint, raw-backed inside `.data` or `.rdata`, and wholly within a saved data-v3 chunk. None intersects the saved Batch 7 M3, selected DV1, DV1 produced, or the three recorded image-builder rewrite ranges. No non-pointer candidate intersects any original relocation or data-v3 symbolic field, including fields crossing an endpoint. Each pointer candidate contains exactly one such field, its own original relocation at its start; the reference dword matches its recorded target. These checks do not establish source type identity or that earlier source declarations cannot own a candidate range. Field and overlap checks must be repeated for the frozen combined selection, including any additions made after this review.

## Frozen selection audit

The frozen `batch8_selection.json` SHA-256 is `f0539b28be3c58729bb994534e19bc1d1410f80b88e027bdea9363878129990b`. It retains the complete Batch 7 selection unchanged and adds 61 objects: 2,843 bytes (248 zero, 2,595 nonzero). Its five stored evidence hashes match the current inventory files. Independent checks found no addition outside raw bounds or its data-v3 chunk, no mutual or saved M3/DV1/produced/rewrite collision, no alignment violation, and no unexpected overlapping field or relocation. Pointer contents match their recorded targets. The 2,688-byte sphere prefix has no interior units symbol boundary or data label; the source evidence supports only the selected accessed prefix, not the full original array size.

The selector explicitly checks the same recorded coverage, field and chunk constraints and preserves the base entries. Its recorded rewrite list includes two builder-written import ranges and a conservative TLS exclusion; the union is 7,900 bytes. Checks depend on these frozen inputs and do not by themselves establish types, original symbol identity, full source ownership, or fresh build behavior.

With the saved Batch 7 DV1 selection unchanged, predicted object provenance is 1,562,506 of 1,979,392 raw bytes. The other 416,886 bytes partition into 87,940 uncovered nonzero, 113,410 uncovered zero, 207,636 DV1 produced but unspliced outside rewrites, and 7,900 in the recorded rewrite union. The historical produced-unspliced total of 207,671 includes 35 bytes within that union; do not add both figures. Machine-readable details are in `inventory/b8_deferred_accounting.json`. These are predictions pending comparison with the fresh positive build summary. The 7,171 BSS addresses remain separately deferred with no file bytes.

## Command-record helper review

`b8_records.py` restricts its two arrays to 640 and 192 source-accessed 40-byte records and marks both as partial. It rejects original relocations that cross either range boundary or fall outside aligned permitted cells. Every relocated value must target a recognized image section; an unrelocated pointer-shaped cell must be zero and emits no relocation. This appropriately distinguishes null pointers from relocatable cells. The helper delegates chunk, claims, symbolic-field and rewritten-range checks to its caller; those are required for the frozen combined selection. The target x86 `ScriptFunctionInfo` layout is separately documented by static size and offset assertions in `include/ScriptFunctionInfo.h`. The other source view describes a parameter pointer at offset `0x14` with opaque surrounding bytes; its remaining pointer-shaped cells are relocation-based scaffolding and do not establish original source-level types. Compiled object bytes and relocation cells still require end-to-end checks.

## Final expanded selection audit

The later frozen `batch8_final_selection.json` has SHA-256 `42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7`. It preserves the Batch 7 entries and adds 64 entries totaling 36,597 bytes (13,613 zero; 22,984 nonzero). The earlier one-byte heads at `0x0103ae48` and `0x0103aef0` have been replaced by string prefixes and are not double-counted. All seven evidence hashes match. The three string prefixes, sphere prefix and two record prefixes have no interior units symbol address or data label.

Independent checks of every addition found no mutual overlap, saved M3/DV1/produced/recorded-rewrite overlap, raw-bound, alignment, or data-v3 chunk violation. Scalar and array entries have no overlapping reference relocation or symbolic field. Each pointer has its matching original relocation and value; the record helper validates both 40-byte-prefix ranges, and their symbolic fields exactly match their original relocation sites. This audit does not replace compiled object, final assembly or runtime verification.

With unchanged Batch 7 DV1 selection, the expanded selection predicts 1,596,260 of 1,979,392 bytes from objects. The remaining 383,132 comprise 67,551 uncovered nonzero, 100,045 uncovered zero, 207,636 produced-but-unspliced bytes outside recorded rewrites, and the 7,900-byte recorded rewrite union. These supersede the earlier frozen-selection prediction above. The final positive archive subsequently confirmed the selected-range totals, as recorded below.

## Final positive archived coverage

The final positive archived manifest and DV1 pieces pass `tools/verify_batch8_artifacts.py`: 8,263 M3 entries, 15,435 DV1 pieces, no drops or range overlaps, and 1,596,260 bytes across `.data` and `.rdata`. DV1 has five additional `.tls` bytes, excluded from that total. Direct reference-byte counts for the covered ranges are 1,075,796 nonzero and 520,464 zero. This confirms the final selection accounting above; `out/batch8-final/evidence/coverage-audit.json` records the checks. The archive audit validates range metadata and reference values, while separate image and relocation verification establishes build results.


The fresh promoted-default build archive independently passes the same audit: `out/batch8-promoted-default-verified/evidence/coverage-audit.json` reports 8,263 M3 entries and 15,435 DV1 pieces with 1,596,260 disjoint `.data`/`.rdata` bytes, including 1,075,796 nonzero and 520,464 zero reference bytes. Five DV1 `.tls` bytes are separate. This is archived-range evidence, with executable identity and relocation content checked separately.
