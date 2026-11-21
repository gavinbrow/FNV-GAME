# Accepted non-AI compiler batch,2026-11-20

Accepted initialized coverage increased by858 bytes to1,613,876 /1,979,392.
The source recipe is f802 (3018units). No complete game classes or hand-decompiled
function bodies were added. This is accepted metadata/source-provider progress,
not a whole Phase2 completion percentage.

The original compiler emitted25 class-name descriptors (834 previously uncovered
bytes) from22 existing-header contexts. A native type_info source provider added
24 previously compiled/unplaced descriptor bytes. Its existing D/G methods are
now supplied by the native source object; four code relocation fields and nine
CRT helper fields were independently checked. All5497 old source/header files
are unchanged, with23 generator-added source files. Synthetic anchors stay in
excluded .m3emit sections. Default selection06250/library74e3/405/weak0 stay fixed.

Positive and repeat match canonical SHA256 c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f.
Relocation bytes match SHA256 364b83a38aae50e6faf0a4f0512fdfa8b338bd1dab47b39fec0bd7b03fd26057.
Both semantic runs passed menu/load/play/cell change/quicksave-load/clean exit.
Each watched12790 inputs, without metadata or digest drift. Deliberate value and
pointer overlay controls both failed roundtrip, changed their final hashes, and
changed only their intended payload plus the independently recomputed PE checksum.
Controls were not played. An audit address-mapping bug was fixed and the already
saved value image rechecked; no build was repeated for that audit correction.

Receipt: ../out/non-ai-resume-20261120/typeid-suite-acceptance.json
SHA074011cfe6860080a7401b31a76bdf2a61991c6fe4aca66210fe95e25a0ac8d1.
The accepted disjoint partition is updated; previous partition is preserved.
Remaining365516 bytes:190854 produced/unspliced,66842 uncovered nonzero,99920
uncovered zero,7900 rewritten. TLS5 is separate.

Additional concrete results remain private: canonical NiRTTI source cohort passes
932 actual compiler/function/EH/initializer checks; a real-header class factory
emits native inheritance/vtable metadata, with its graph matching after two
supported private class-key corrections and one method slot matching; actual
Microsoft LINK confirms native type_info fallback and strong-first behavior;
BSAudio22-byte descriptor passes compiler/anchor checks; the RTTI156-byte fix passes
an immutable older-epoch seven-object MASM roundtrip. These do not count as accepted
coverage or complete classes. Read the current ACTIVE.md for exact remaining
integration steps and source/weak-provider limitations. The user goal remains open.
