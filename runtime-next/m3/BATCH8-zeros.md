# Batch 8: zero-byte accounting

Reproducible read-only inventory: `python -I runtime-next/m3/tools/b8_zero_accounting.py`. The JSON records half-open virtual-address extents and the BSS address list. It partitions the 1,979,392 raw bytes of `.data` and `.rdata` using frozen Batch 7 M3 selections, frozen Batch 6 DV1 ranges and produced ranges. The three recorded image-builder rewrite ranges have final precedence. This is metadata and reference-byte analysis, not an image build.

| Category | Zero file bytes |
|---|---:|
| Uncovered outside recorded rewritten ranges | 113,658 |
| Rewritten by image builder | 1,482 |
| DV1 produced, not selected, outside rewritten ranges | 74,521 |
| M3 selected | 326,594 |
| DV1 selected | 180,257 |

The historical 115,137 uncovered zeros split into 113,658 still uncovered outside recorded rewritten ranges and 1,479 inside them. Three additional rewritten zeros were previously counted among produced-but-not-spliced (74,524 becomes 74,521); these figures therefore reconcile exactly. The three recorded ranges are disjoint and fully file-backed: their lengths are 1,188, 6,688 and 24 bytes, totaling 7,900 (6,418 nonzero and 1,482 zero). The historical 7,908-byte exclusion figure is stale; its eight-byte discrepancy has not been explained. Of these, 35 bytes (32 nonzero, three zero) previously fell in produced ranges. This classification applies only to the recorded rewrite list, whose completeness is not established.

Among the 113,658 uncovered zeros, 100,001 lie in intervals beginning at a known declaration. These interval counts are not proven object extents. Another 13,287 bytes are in 5,216 entirely zero candidate pieces; the remaining 370 uncovered zeros are in other pieces or excluded field windows. Candidate pieces are cut at all units symbol boundaries and inventory DAT addresses, data-v3 chunk boundaries, and field/relocation exclusions; they exclude previously claimed, produced and recorded rewritten ranges. Each is raw-backed and entirely zero. Their starts are not known declarations. They are *placement candidates*, not proof of independent source objects: a preceding declaration can own a tail, and the name scan does not prove all declaration extents. Review them against any newer selections and all builder rewrites before using them. Existing explicit-allocation fixtures establish compiler/loader feasibility only; compilation and end-to-end positive and negative controls remain necessary.

The raw-less `.data` virtual tail is separate from all file-byte totals. The units symbol-key scan finds 7,171 distinct DAT-containing addresses in that tail; the source DAT inventory separately flags 7,710 addresses as BSS. These count different inputs, not 14,881 objects; neither count gives object sizes. The 7,171 addresses are recorded in JSON and require definitions/layout work, with zero file-byte contribution.

## Declaration-supported zero globals

`tools/b8_zero_accept.py` produces `inventory/b8_zeros_accepted.json`. Ten globally declared scalar DAT addresses, 29 bytes total, have one consistent simple source declaration and matching global units symbol encoding. Each extent is all-zero, naturally aligned, raw-backed, within one data-v3 chunk, and avoids recorded claims, rewritten ranges, field windows and interior known names/labels. A targeted scan of `fnv_decomp/src` and `include` found no `_DAT`, PTR, OFF, UNK, BYTE, WORD or DWORD alias at these addresses. Entries include `file_backed: true` for explicit section allocation. The declaration inventory is lexical and preceding declarations do not establish reliable extents; these checks do not prove full source ownership. Recheck against concurrent Batch 8 selections before placement.

Fifty fixed-array declaration cases were conservatively deferred without matching array-mangling and extent proof. No padding pieces are accepted: an alignment-sized zero gap alone does not establish padding rather than part of a neighboring object. All BSS definitions remain deferred and contribute no file bytes. No target object or image build was performed for these candidates.

