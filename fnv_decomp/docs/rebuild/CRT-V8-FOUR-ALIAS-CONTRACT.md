# Existing four CRT bindings in the V8 cohort

The separate V8 contract covers 45,315 saved input fields: the unchanged
44,540-field V7 cohort, 723 CODE59 fields and 52 ModelLoader fields. It
retains the same four normal SP1 CRT bindings and adds no CRT alias.

| Normal provider | V7 uses | V8 uses |
|---|---:|---:|
| `@__security_check_cookie@4` | 100 | 102 |
| `___security_cookie` | 94 | 96 |
| `__wcsicmp` | 1 | 1 |
| `_strcat_s` | 3 | 3 |

The 202 uses are a complete candidate-input census. They do not establish
linker extraction or application runtime coverage. Normal SP1 LIBCMT owns
the fresh cookie family and shared locale, errno and invalid-parameter
state. Its data addresses need not equal the original CRT addresses.

The ordinary CODE59 pair comes from the exact compiler-owned `/GS` boundary
of recipe 0576's `main.cpp` source. Its cookie read maps raw section 24,
offset 10, symbol 28 to serialized section 2, offset 10, symbol 4. The check
maps raw section 24, offset 119, symbol 31 to serialized section 2, offset
119, symbol 5. Both retain their complete own-recipe source proofs from a
single indexed sealed context. The cookie scalar model follows the x86
compiler-generated pair and accepted normal storage declaration; the
four-byte relocation operand alone does not establish scalar width.

ModelLoader retains a separate generated-EH proof class. Its own-source
cookie read maps raw section 420, offset 21, symbol 762 to serialized
section 3, offset 21, symbol 4. Its generated check maps raw section 421,
offset 61, symbol 765 to serialized section 4, offset 61, symbol 6. Six
eight-byte cleanup pieces precede the complete handler interval `[48, 75)`.
An agreeing global recipe binding is a numeric witness and does not relabel
the generated field. Frame, lifetime and whole-application ABI remain open.

`tools/rebuild/crt_v8_four_alias_plan.py` binds both own-source hashes and
all invoked metadata helpers. It preserves every old raw source record,
checks the complete hydrated field view, and joins all four new uses to
their distinct source and serialized evidence. Choosing normal SP1 CRT
does not by itself require every caller's compiler label to be SP1.

`tools/rebuild/crt_v8_four_alias_contract.py` exposes the pure five-argument
`validate` API. The caller must remove all four exact inherited CRT tokens
before applying the enabled subset. Uncertainty in either cookie binding
disables both. The existing frame-handler and dynamic-cast obligations
receive no alias approval from this contract.

The contract and consumer remain diagnostic preparation inputs. Actual
prepared-source/input review and the separately delegated native operation
are required. These tools execute no application and grant no runtime ABI
or provider-adoption approval. All earlier V7 files remain frozen.
