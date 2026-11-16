# CRT frontier lane 03

The fixed lane contains 48 original targets and 658 physical source fields.
It is a partition of the full entry-graph unknown executable frontier, not a
list of actual unresolved LINK errors. No provider, alias, object, executable
or runtime compatibility is approved by this investigation. The reference
sources, recipe, oracle, existing parsers and provider helpers are unchanged.

`tools/rebuild/crt_lane03.py` reads only the pinned dispatch packet, its own
178 exact source paths, the retained doctor metadata and named index members
of the three pinned normal CRT libraries. The first pass saved source hashes,
declaration/use excerpts, actual native section definitions, public aliases,
member undefineds and complete relocation records. Source names remain
hypotheses. Shared sections, interior entries and non-function native exports
were excluded from original observation rather than assigned guessed bounds.

After independent source and metadata review, one delegated read-only pass
observed 17 fixed targets, 2,876 total text bytes. Each range was at most
869 bytes, below the authorized 4 KiB per target and 256 KiB total limits.
The complete reference hash was checked before and after; the PE header's
exact text geometry was checked and only the approved fixed ranges were
read as code. No text search, original-code execution or old-code forwarding
occurred. The tool emitted no instruction bytes or disassembly.

| Original target | Named native export | SP1 / RTM complete non-relocation result |
|---|---|---|
| `0x00ec7c56` | `__invalid_parameter_noinfo` | Equal |
| `0x00ec5fce` | `??_M@YGXPAXIHP6EX0@Z@Z` | Equal |
| `0x00ec7ec0` | `__strnicmp` | Equal |
| `0x00ec6da0` | `_strcmp` | Equal |
| `0x00ec7f1e` | `__splitpath_s` | Equal |
| `0x00ec9a5e` | `_fopen_s` | Equal |
| `0x00ec8d08` | `_strtol` | Equal |
| `0x00ecdd16` | `__gcvt` | Equal |
| `0x00ec6bb5` | `_vsprintf_s` | Equal |
| `0x00ec7d50` | `_clock` | Equal |
| `0x00ecc104` | `_fgets` | Equal |
| `0x00ec716d` | `_bsearch` | Equal |
| `0x00ecc250` | `__alldiv` | Equal |
| `0x00ecda70` | `_fflush` | Equal |
| `0x00401460` | `_memcpy` | Failed: 662 differing non-relocation bytes |
| `0x004564f0` | `__mbsnicmp` | Failed: 21 differing non-relocation bytes |
| `0x0046fd30` | `__mbsicmp` | Failed: 18 differing non-relocation bytes |

The 14 positive target observations account for 360 physical caller fields;
the three negative hypotheses account for 123. Eleven section-boundary exclusions
account for 109 fields, and 20 targets without a named hypothesis account for
66 fields. All 48 targets remain in the metadata, including application
functions and static-local cleanup functions. Negative comparisons establish
that the selected direct member model failed; they do not identify a wrapper
or authorize substitution. In particular, the memcpy-like caller spellings
do not establish a direct CRT function at the original base.

All relocation fields in each compared native section were masked precisely,
with signed REL32 or DIR32 addends accounted for and each original destination
recorded privately. No dependency destination identity was promoted. Equal
non-relocation bytes therefore remain separate from complete relocation
identity and from a callable normal-CRT substitution. VC8 was independently
compared and often failed where SP1/RTM agreed; equal VC8 sections do not prove
cross-version state, EH or caller compatibility.

## Caller contracts and remaining family obligations

Exact installed SP1/RTM/VC8 `string.h`, `stdlib.h`, `stdio.h`, `time.h` and
`mbstring.h` declarations were retained with header hashes in a separate private
contract receipt. The normal declarations and the actual own-source uses give
the following concrete remaining gates:

- String comparison uses require ordinary cdecl pointer/count arguments and
  an integer result. `strcmp` is case sensitive; `_strnicmp` is bounded and
  case insensitive. Locale, multibyte/code-page state and invalid-parameter
  behavior belong to the chosen single CRT. Neither failed multibyte hypothesis
  inherits a provider from a similar name or from another comparison function.
- `_splitpath_s` has nine arguments: input path plus four output-buffer/size
  pairs. A recovered void-return alias ignores the normal error result. Buffer
  capacities, optional output rules, errno and invalid-parameter ownership
  still need the actual caller/data inclusion review.
- `fopen_s`, `fgets` and `fflush` form part of a stream family. Source uses expose
  a stream output pointer and path/mode strings, a writable destination plus
  signed count and stream, and a stream argument respectively. Their stream
  objects, descriptors, buffers, locks, EOF/error state and cleanup must belong
  to the same fresh CRT as open/read/seek/tell/close elsewhere. Passing copied
  old FILE storage is not established by these function observations.
- `strtol` uses text/end-pointer/radix arguments. The normal signed-long return
  conflicts with recovered unsigned-int aliases at two callers; x86 register
  width agreement does not settle overflow, negative input or errno policy.
  `_gcvt` requires its actual precision/buffer contract and normal conversion
  state; absence of recovered declaration excerpts is retained as unknown.
- `vsprintf_s` needs destination capacity, format and the actual x86 `va_list`
  boundary, including format/argument type agreement. The recovered signed-int
  capacity spelling needs a valid positive range before a normal size_t call.
- `clock` uses normal `clock_t`/failure and process-clock semantics. A recovered
  `int()` alias alone does not settle units, wraparound or failure consumers.
  `bsearch` requires the normal element size/count and cdecl comparator contract,
  valid array storage and comparator lifetime; its source declaration is not
  inferred from the public export.
- `__invalid_parameter_noinfo` normally has a void/no-argument boundary and
  delegates to the CRT invalid-parameter policy. Recovered unsigned-return
  declarations remain visible. Returned-EAX consumption and error-handler
  lifetime require review before a normal functional alias is adopted.
- The vector destruction iterator and `__alldiv` are native compiler helpers.
  A public C prototype is not manufactured for them. The vector iterator's
  stdcall argument block, destructor callback convention, element stride/count,
  unwind behavior and EH family must be reconciled; existing recovered callback
  types conflict. The 64-bit division helper needs the actual generated operand,
  result and stack-cleanup convention, including divide exceptions.

The rejected shared/interior math, string-copy and stack-probe entries remain
unresolved. No ordinary cast wrapper establishes their x87, stack probing,
register preservation or return conventions. The table proposes evidence for
future contract review, not a provider alias table ready for LINK.

## Frozen private evidence and review

The metadata receipt is `crt-lane03-metadata-v1.json`, SHA-256
`b7387f5acd49069ce670d7a5b989778d115c512b71754961840ffa5568915baa`.
The independent lane02 source review is SHA-256
`5fbdc1dc680802e7887a3db5050c8a14ef22404dc507016c843dfff740711027`.
The fixed observation receipt is `crt-lane03-observation-v1.json`, SHA-256
`be96828b689345d269eaadf5edd7c6b79fa86a28e5208a4d9fd04020b42a091a`.
The old-header receipt is SHA-256
`3557ba819d20f47fdedd3b82aca14d8955c900029a50c94b9c5f2bbd97b6e9f1`.
These private metadata artifacts contain original-address evidence and source
provenance, never copied game bytes. Lane02 independently reconciled all 51
eligible comparisons, all 325 relocation fields across the three compiler
families and the exact 17-target/2,876-byte budget against the saved metadata.
The saved-artifact outcome review is SHA-256
`097e30e41dd40f22c051d626187f24c8ea724f66ac5a4a4358cfbdf73d250cf2`;
it involved no original-image reread. All ABI, provider-selection and
runtime-eligibility flags remain false. Eight synthetic tests pass, including signed addends, exact relocation
masking, malformed fields, range limits and rejection of a shared-entry section.
