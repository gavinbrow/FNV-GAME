# Accepted NiMemObject/BSAudio source batch - 2026-11-20

The combined batch is accepted. It corrects27 declarations of the same
NiMemObject type from class to struct and replaces the22-byte BSAudio descriptor
within an existing100-byte W block with native compiler output. The78-byte
remainder stays generated, packed and file-backed. One new source unit is added;
no hard function body is decompiled. Recipe B31f074d has3019 units and5522
source/include files. All430 previously accepted typed NiRTTI records remain.

## Proof

Five fresh runs at `../out/phase2-kind-bsaudio-20261120/` cover positive, p2bv,
p2bp, p2bw and repeat. Both clean images match canonical SHA256
`c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f`.
The734884-byte relocation directory retains SHA256
`364b83a38aae50e6faf0a4f0512fdfa8b338bd1dab47b39fec0bd7b03fd26057`.
Both clean runs pass menu/load/play, changed/restored cell, quicksave/load and
clean exit. Every run freezes12861 inputs with zero observed/final digest changes.

Each run captures13 compiler objects. Independent checks verify7217 NiRTTI
functions,1029 functions in the current kind cohort and16 other native functions;
they also check source hashes, code/relocation/EH/CRT pairing, exact native
descriptor bytes and provider/directive/anchor inventory. The five current kind
units include two data-only units; those do not count as function passes.

The intentional historical kind comparison exception is exactly the NiMemObject
class-to-struct descriptor name/symbol change. Function code and relocation
targets are checked separately. Three already-selected records gain matching
providers from6 to23; their data and relocation targets remain identical. The97
historical review flags and16 unresolved EH tails remain unresolved.

All three actual mutations fail round trip and change their intended field:
native name byte, native vtable pointer, and the packed tail's pointer at+2.
The independent audit allows no other PE differences except a separately
recomputed checksum. Controls never run gameplay. Actual archived M3 COFFs are
checked against the reference; manifest expected bytes alone are insufficient.
The selected union and original relocation-site policy are unchanged.

Six default-configuration tests also pass. The default selection is720cacfc;
library74e3/405 records/16730 bytes, weak mode0 and library index0 stay in effect.

Root audit SHA256:
`e94a3869b2ab16bec46da6cd94a1c3f9d24456551780f70c7992428c12e4779f`.
Receipt: `../out/phase2-kind-bsaudio-20261120/root-audit.json`.
Acceptance marker: `../out/phase2-kind-bsaudio-20261120/accepted.json`.

## Accounting

Initialized coverage remains1614032/1979392, with TLS5 separate. M3 contributes
1062848 and DV1 contributes551184;22 bytes migrate between providers. Remaining
365360 =190698 produced/unspliced +66842 nonzero +99920 zero +7900 rewritten.
The accepted partition SHA256 is
`f2a4717c2e50a51bfa8ce5b48b9bcb64e19a2b19f4fc851d7fcccec55b45c5f5`.
The previous partition is preserved as
`accepted_range_partition.before-kind-bsaudio-20261120.json`.

This is typed ownership progress, not added file coverage or complete classes.
The allocator sized-delete declaration is not part of this accepted batch.
Phase2 and the active goal remain open.

## Later private results, not accepted source

- All228 native-header probes in typeid-bulk-B31-v2 compile and match their R0
  bytes, original relocation, provider inventory and excluded anchor. Excluding
  BSAudio leaves227 candidates/7942 already-owned W bytes. V1 emitted unwanted
  CRT data through typeinfo; its16 deferred results are preserved. V2 uses the
  same vendor forward declaration as the accepted producer.
- The coupled draft partitions47 existing W owners into227 native records and
  250 remaining fragments. An actual compiler and the production checker pass
  all250 fragments, including physical file backing for89 zero fragments.
- A private hkClass experiment changes417 four-byte source surrogates to the
  canonical48-byte record. Both old/new versions match928+34 functions; paired
  bytes/relocation targets and raw EH/CRT match, and417 BSS extents do not overlap.
  A comparator address-format defect was corrected in a separate V2 report;
  the original failed receipt remains. Consumer aliases/ownership remain open.
- The minimal sized-delete declaration's first paired unit passes43/43 functions
  without code differences. The complete lexical scope is126 units/2534 functions;
  the full compiled cohort is still required.

Successful transaction-core pending files remain recovery journals. If needed
after lane termination, recover the BSAudio nine-file layer BEFORE the kind27
layer; then the accepted NiRTTI layer can return C8 to F802. Do not use the legacy
nonjournaled BSAudio CLI. No downloads/uploads/exports/commits or Steam/reference
changes were performed.
