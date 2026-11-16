# Fixed V10 import evidence assessment

`tools/rebuild/assess_v10_imports.py` examines exactly four unresolved original
IAT cells against the accepted 45,947-field V10 ledger. It uses the additive
CODE68 census view and selects every field whose canonical label, original
base or original target names each cell. Physical use multisets must agree
with the accepted actual diagnostic groups. The expected use counts are eight
EnterCriticalSection, thirteen LeaveCriticalSection, one SetThreadPriority and
one SteamAPI_RunCallbacks.

Each source-use predicate retains the frozen zero-addend DIR32 pointer-cell
rules, exact original base/target, role, import classification and catalog ID.
The normative ledger and original proofs remain unchanged. Unsafe records are
preserved with explicit per-cell blockers; they cannot be normalized into
positive evidence or invalidate unrelated cells silently.

Each KERNEL32 cell is decided independently. The tool proposes an exact superset
of the accepted twelve-import library containing only positive cells; thirteen
or fourteen names are retained if other cells have blockers. A fifteen-name
DEF is proposed only when all three pass. It verifies the
old native pointer identities and preserves USER32, GDI32 and SHELL32 hashes.
The new library would replace the old KERNEL32 library rather than share its
descriptor. The proposal is text only: this tool cannot invoke LIB, link an
executable or apply aliases. Later cohorts need their own complete use census.

Steam is kept separate. Its original identity is `steam_api.dll` plus
`SteamAPI_RunCallbacks`, import 203, original cell `0x00fdf488`. The assessment
preserves all current uses and the reconstructed source's explicit
`extern C`, `dllimport`, `void __cdecl` no-argument declaration, with the exact
source hash, declaration line, compiler and recipe flags. Those are typed source
facts, not proof of the owned DLL's architecture/export, SDK binary ABI or
runtime/lifecycle contract. The tool reads only the specified reconstructed
source file; it does not locate, read, load or execute a Steam DLL, generate a
Steam import library or shim, or change any Game source or protection code.

Inputs include the exact original catalog, accepted V10 observation/diagnostic
and reviews, full field gzip, existing native import collection, source recipe
and typed source. Sources and all old selected import libraries are hash-bound
before and after a new private report is written. Outputs require a fresh
directory under ignored `build/rebuild`; drift removes only newly owned files.
ABI verification, runtime provider adoption, DLL/API calls and alias activation
remain false.

```powershell
python tests/rebuild/test_assess_v10_imports.py -v
```
