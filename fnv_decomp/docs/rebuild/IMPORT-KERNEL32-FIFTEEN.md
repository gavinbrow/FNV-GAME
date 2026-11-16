# Win32-only KERNEL32 fifteen-import successor

`tools/rebuild/import_kernel32_fifteen.py` prepares the fixed twelve-to-fifteen
KERNEL32 successor after the accepted V10 assessment. The only new cells are
EnterCriticalSection, LeaveCriticalSection and SetThreadPriority. All three
must be positive in that accepted assessment; the earlier assessment's
per-cell blocker policy is preserved rather than waived. The producer replays
the complete immutable 45,947-field scope and all 23 evidence records, retaining
22 Win32 uses and the separate one-use Steam inventory.

The private request kind is `fnv-kernel32-fifteen-import-request`, schema 1.
`replacement` binds the old twelve-import archive and new
`kernel32-fifteen.lib`, exact counts and definition hash. `cells` contains the
fifteen replacement identities; `prior_pointer_aliases` preserves all 31 old
native mappings. Three normalized unchanged library records bind USER32
sixteen, GDI32 one and SHELL32 two by filename, SHA-256 and byte count.
`new_kernel32_all_use_censuses` preserves all 22 Win32 uses, while
`Steam_inventory_context` preserves the accepted source facts and explicit
provider blockers. Steam is absent from the replacement cell list and aliases.

The offline tool calls no native binary and does not read a Steam DLL, SDK or
Game source. It uses only the prior accepted Steam source inventory as immutable
context. Original catalog hints and original full proofs remain separate from
new native hints and offsets. The actual old KERNEL32 archive is reparsed;
all selected source/input/library hashes are checked before and after new
private output is written. Outputs are exclusive under ignored `build/rebuild`.

`reconcile(request, parsed_kernel32, request_sha256)` consumes an actual bounded
normal-import archive parse. Its result kind is
`fnv-kernel32-fifteen-import-native-collection`, schema 1, with singular
`library={file,sha256,bytes}` and `parsed_archive`. It contains 34 distinct
canonical/native pointer proposals and positive mechanical flags
`old_31_pointer_identities_preserved`, `replacement_identity_verified` and
`native_library_generated`. The reviewed native collector adds command/tool
records and `all_inputs_tools_sources_stable` only after real pre/post checks.
Independent native conformance and a later full-cohort alias census remain
required.

The collector is limited to one LIB generation and two read-only DUMPBIN calls
under root delegation, independent source/input review and the coordinator's
CPU lease. It neither self-reserves nor replays uncertain operations. All old
libraries remain immutable, with the new archive selected instead of the old
KERNEL32 archive.

Steam remains unaliased: no Steam DEF, shim, stub, load, export observation or
SDK/runtime provider adoption occurs. Source ABI, provider/runtime eligibility,
alias application, compiler/executable linking and imported API calls remain
false for this component. No Game, DRM, EH or RTTI source is changed.

```powershell
python tests/rebuild/test_import_kernel32_fifteen.py -v
```
