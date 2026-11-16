# CRT frontier lane two

The lane is a fixed partition of the original executable frontier, containing
48 targets and 658 physical fields. It is not an application LINK error list:
the dispatch packet attaches an actual V4 unresolved group only to `0x00ecc071`.
All original target, role, caller, spelling, addend and physical field records
remain in the private contract report. No alias or provider is selected.

`tools/rebuild/crt_lane02.py` proposes 23 named native CRT exports for comparison.
Recovered source names are hypotheses. The tool resolves each exact name through
the existing bounded archive-member reader in SP1, RTM and VC8, then requires a
complete, unique function section at symbol value zero, at most 4 KiB. Missing,
ambiguous, multi-function and oversized sections remain unresolved. It does not
find a convenient byte prefix or infer a function boundary from a nearby symbol.

The metadata phase reads the pinned dispatch packet, doctor and named native
members only. The separate probe phase additionally requires an independently
approved source bundle and contract hash. Each fixed original target is read
once, for the largest reviewed complete native section, wholly within checked
`.text`; smaller family comparisons reuse that observation. Total target reads
are capped at 256 KiB, each at 4 KiB. No original target discovery, whole-section
search, execution, executable generation or recursive dependency probe exists.

Every supported DIR32 and REL32 field is preserved with its native symbol,
storage, section, value and signed addend. The existing relocation observer
derives each original destination and checks image geometry and HIGHLOW shape.
This accounts for fields without proving the destination's identity. Complete
nonrelocation agreement is reported separately from relocation identity, and
both original identity and provider approval remain false. A mismatch is kept.

Normal functional CRT adoption is a separate contract decision. Byte identity
does not select a CRT version or close caller declarations. In particular:

- `_fwrite` involves CRT descriptor, stream, locking and error ownership.
  `_access` separately needs path/mode and filesystem/error policy. A normal
  stream must be created, used and closed by one compatible
  CRT family, with no borrowed original `FILE` or copied lock state.
- `_msize` needs a live allocation owned by its chosen CRT heap. An address with
  the expected numeric shape is not an allocation or ownership proof.
- String comparison and conversion can depend on locale, errno and invalid
  parameter policy. A normal CRT would own fresh state; an old dependency's
  numeric destination is not a reason to alias old storage.
- Math helpers require the actual x87/return and error-policy contract. Recovered
  int/pointer/void spellings and helper calling conventions are retained as
  contradictory evidence rather than rewritten into an approved prototype.
- Throwing support requires compiler, EH, type and frame ownership. A named
  helper section alone does not approve mixed-family exception propagation.

Non-CRT and compiler-generated destructor targets remain unclassified. Nothing
in this lane changes the reference recipes, source, oracle or blocked DATA bridge.

Synthetic checks run with:

```powershell
python -m unittest discover -s tests/rebuild -p test_crt_lane02.py -v
```

The current ten checks cover complete native spans, metadata output shape, JSON
span round trips, and
rejection of interior, shared, oversized, unsupported, overlapping and out-of-span
native fields. A first metadata attempt failed its final output-shape check
without emitting a report. The corrected read-only rerun completed successfully.

The emitted private contract report retains 54 complete native sections across
18 targets. Five further hypotheses (`sin`, `strchr`, `tan`, `sqrt`, `atan2`)
remain unprobed in all three compiler families because their named sections did
not satisfy the conservative unique complete-function gate. The maximum native
extent per target totals 1,891 bytes. Independent source and contract review
accepted this finite request. An initial probe preflight rejected the tuple/list
representation difference between in-memory spans and saved JSON, before reading
the reference. Exact JSON normalization corrected that representation check;
the successor contracts retain identical native fields and bounds.

## Fixed observations and caller evidence

The independently reviewed successor read 18 fixed targets once, totaling
1,891 bytes, and compared all 54 complete SP1/RTM/VC8 sections. The checked
reference hash and all protected inputs were stable before and after. No
original code was executed, forwarded, searched or emitted. Every one of the
171 native relocation fields is retained, including errors for failing models.

| Original target | Named native export | SP1 / RTM complete nonrelocation result |
|---|---|---|
| `0x00ec61c0` | `_memset` | Equal |
| `0x00ec65a6` | `_strcpy_s` | Equal |
| `0x00ec6bd2` | `_strcat_s` | Equal |
| `0x00ec623a` | `_sprintf` | Equal |
| `0x00ec7750` | `_strstr` | Equal |
| `0x00ec8a19` | `_strncmp` | Equal |
| `0x00ec7ce3` | `_memmove_s` | Equal |
| `0x00ecbf05` | `__access` | Equal |
| `0x00ecc300` | `__allmul` | Equal |
| `0x00ec7894` | `__CxxThrowException@8` | Equal |
| `0x00ecc5f8` | `_strtok_s` | Equal |
| `0x00ec89e9` | `_isalnum` | Equal |
| `0x00ec8feb` | `__strlwr_s` | Equal |
| `0x00ecb086` | `_fwrite` | Equal |
| `0x00ecc071` | `__wcsicmp` | Equal |
| `0x00ecd31f` | `__msize` | Equal |
| `0x00eca6d3` | `_atol` | Failed |
| `0x00ec858a` | `__stricmp` | Failed |

The 16 positive target models have 529 source fields; the two negative models
have 14. Five excluded section models have 33 fields, and 25 targets without
a named model have 82. These groups account for all 48 targets and 658 fields.
Only five VC8 models agree, so the observations do not identify a unique CRT
family. A failed direct model does not identify a wrapper or approve an alias.
The zero-relocation `strncmp` and multiplication models compare every byte in
their selected complete native sections; an independent original boundary index
and compiler-helper calling contract are still separate evidence.

The private source/header receipt verifies 167 exact packet source hashes and
retains declaration/use excerpts, contradictory COFF spellings and 24 named
native header files across all three compiler families. The observed local
declarations support these concrete compatibility gates:

- `memset` has the normal pointer/int/size_t boundary and pointer result, while
  some recovered aliases return void or use signed counts. Caller inclusion
  must preserve valid writable extents and count ranges before functional use.
- `strcpy_s`, `strcat_s` and `memmove_s` normally return errno_t. Recovered
  pointer and void returns remain contradictions. One memmove alias even
  declares its third word as an integer and fourth as a pointer; matching
  register widths do not approve argument meaning or returned-pointer use.
- `fwrite` callers pass buffer, item size, count one and stream. Its normal
  size_t item-count result and actual FILE owner must be respected. Source
  occurrences do not establish unified open/write/close, buffering or locks.
- `_msize` is declared as size_t cdecl with a heap pointer. No recovered source
  declaration excerpt was found for its compiler-visible alias; allocation and
  heap family provenance remain open.
- Throw-helper callers use a two-word stdcall boundary, including a null/null
  rethrow-shaped use. Recovered exception-object and information-pointer types
  conflict. This does not close throw metadata, destructor callbacks or EH
  family ownership. No handwritten public prototype is inferred for `__allmul`.

All normal-functional adoption, ABI and provider-selection flags remain false.
The receipt records 44 relocation-shape error entries across negative family
models; these are evidence that those models failed, not discarded fixups.
Even positive models leave their old dependency identities unresolved.

## Private receipt identities

Successor contracts `crt-lane02-contracts-v2.json` have SHA-256
`075ad82bdfa73b83c6249ec26d439d591b44f45b4ca76b19840e33530b1d9d46`.
The exact source-review receipt has SHA-256
`6be15b6a1dcb1496497f51c5939009ecc3da3a41b2d25c563e2f2a62a15fd170`.
Observation `crt-lane02-observation-v1.json` has SHA-256
`8b2484c22a5810bd78d92353652298c2f1564b3c87290c9c2f830ecd23a5d79c`.
Independent saved-artifact reconciliation has SHA-256
`e7916e8c24c0180c9ef8d0b38856cfe5d2311e7f963c0c3ffe6707d9b5cf8fbc`;
it checked all 54 comparisons, 171 fields, exact contracts and budget without
rereading the original image. Source/header evidence has SHA-256
`83ab38d184f3f5b38d3b0d4fa82fc1700f0e840b2e79aa37b71dec7f126cef9b`.

Two bounded metadata operations after the failed probe were completed before
the worker received the scheduler's release notice; their resource leases are
therefore reported as uncertain, rather than retroactively asserted. The final
original observation ran only after a fresh explicit lease and exact peer gate.
