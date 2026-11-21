# Library-only produced-range triage

The final Phase 1 range partition contains 65,726 bytes annotated exclusively by library pseudo-unit ranges in the current `data-v3/out/produced_ranges.json`. This is a disjoint subset of the 207,636 produced-but-unspliced bytes; it is not an additional total. `library_triage.json` records per-extent kinds and pseudo-unit/member names; `library_triage.py` reproduces the mapping. The classification uses current metadata, which was not archived as a final-build input. IDs follow `data-v2/libsecs.py`: archive member order in local VC2008 SP1 `libcmt.lib` and `libcpmt.lib`. Archive SHA-256 values are recorded; paths within the compiler archives are reduced to member basenames.

| Current library kind annotations | Unique bytes |
|---|---:|
| `rdata-other-unit` only | 51,450 |
| `string` only | 5,694 |
| `data-unit` only | 5,192 |
| `eh-tables` only | 1,712 |
| `rdata-other` only | 816 |
| RTTI (`rtti0`, `rtti1`) only | 534 |
| `data`, `vtable`, `crt-init-array`, `float-const` only | 304 |
| Multiple kind annotations | 24 |
| Total | 65,726 |

The current DV1 selector explicitly rejects library objects as “not our unit”; therefore an authorized policy/ownership route is needed to splice library-produced pieces. Kind annotations alone do not prove which first-failure reason applied to an individual byte, or that each library candidate would pass placement, reference and relocation checks after such a policy change. The final DV1 log's library-rejection unique-uncovered figure is a separate per-reason union, not this subset and not additive across reasons.

A member-name heuristic labels 48,761 bytes solely with math-named archive members, 24 with math and other member names, and 16,941 with other names. Examples include `_pow_sse2_.obj`, `_pow_pentium4_.obj`, `_atan_table_.obj` and `_acos_sse2_.obj`. These names suggest compiler-runtime numeric data; they do not prove the exact source type or determine a phase. At 25,946 bytes, more than one archive member annotates the same byte, so individual member coverage in the JSON is deliberately non-additive. This rules out attributing the entire category to RTTI/vtable source-name or method issues. The small RTTI/vtable-labelled portions warrant inspection, while CRT initialization, EH and other library ownership/placement remain distinct questions; no universal Phase 2 assignment is implied.

No compiler, build, gameplay or source mutation was performed in this triage.

## Experimental bounded library route

`library_candidates.json` identifies 370 disjoint non-CRT-init/non-EH/non-class library pieces totaling 6,374 bytes. Each is a whole local compiler archive section with matching member/object and section digests, symbol offsets, alignment, reference bytes, no relocation or overlapping symbolic field, and no collision with final archived M3/DV1 ranges or recorded rewrites. The selection remains metadata-only; the private opt-in copy is `../out/phase2-library/selection.json` (SHA-256 `da19c0a782f6ba4ac986e992daf4af7ed67c282d0b70f35e8804a22227bce645`).

`library_overlay.py` adds a digest-pinned opt-in hook in `dv1_splice.py`; the default still excludes library units. The hook revalidates archive/member and section hashes, fresh placement and tier, exact section properties, symbol offsets, reference values, fields, chunk, alignment and current claims before any output is written. Seven synthetic fail-closed tests pass, including mismatched deduplicated owner/section keys, object digests, counts and duplicate candidates. The hook now also requires the fresh owner section key and reloads the original archive section to reject splits or incompatible deduplication. A read-only check against an existing mutable temporary placement pickle (SHA-256 `ed4984070b6078662d6cde7e1fbd56eacedeb20ffc668d0daf420112740887c3`) accepted all 370 / 6,374 bytes. This is not a fresh build or proof of subsequent placements; the temporary pickle changed later and is not a stable archive. A repeat against a later temporary pickle also accepted 370 pieces, but a concurrent writer cannot be excluded. The driver must explicitly reject a configured library selection when M3/DV1 is disabled and record the effective selection; it must not silently ignore the opt-in. Independent review, opt-in full build, targeted negative control and gameplay are outstanding.



Independent review of the strengthened hook confirmed that requiring the original owner/section key and reloading the exact archive section addresses the identified COMDAT-owner ambiguity. This is a code review, not an integration run; the driver provenance patch and full opt-in verification remain pending.

The targeted `p2lv` negative control marks only explicitly approved library DV1 pieces and mutates one byte of the first marked, non-relocating library piece at overlay load. It fails if such a piece is absent and logs the exact address and before/after byte; repeated synthetic loads choose the same mutation. This control and the library opt-in have not yet had full-build verification.

## PIECES and atan follow-on proposals

A read-only section-symbol inventory found 35 candidate ranges totaling 10,356 bytes beyond the original 6,374-byte whole-section proposal. Of these, 34 ranges / 4,196 bytes correspond to exact current `st.PIECES` boundaries and key/address/tier in a temporary placement snapshot; the remaining 6,160-byte `_atan_table_.obj` range is a whole section, not a PIECES split. The snapshot is mutable and diagnostic only.

The private `out/phase2-library-splits` staged hook verifies each split against the current archive's complete section digest, source flags and data, adjacent original definition boundaries, exact fresh PIECES key and range, remapped definitions, absence of original relocation crossings, as well as existing destination/field/alignment/claim checks. Thirteen synthetic whole/split tests and a read-only 404-piece/10,570-byte dry run passed. Independent code review found no core acceptance bug; a real build and controls remain required.

The separate private 405-piece/16,730-byte selection adds the 6,160-byte whole atan section. A temporary placement snapshot resolved `KEYOF[(100063,2)]` to the exact address and tier and the complete placed section matched the archive's data, flags, definitions and no relocations. Several smaller alternate library annotations occur within it; the proposal selects the whole object and excludes those alternatives. `propose_library_splits.py` reproduces both selections. The choice and all fresh placement data remain subject to independent review and full image verification; these amounts are not yet accepted coverage.
