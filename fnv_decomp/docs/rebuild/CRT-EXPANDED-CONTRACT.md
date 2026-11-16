# Four CRT bindings in the expanded source cohort

The separate expanded contract carries the same four normal SP1 CRT bindings
into a 44,540-field candidate cohort. It adds no CRT alias. The earlier
44,353-field contract and the actual V6 diagnostic remain immutable. V6
removed exactly four unresolved groups, from 277 to 273, with none added;
the link still failed and no application was executed.

The new saved observation retains every V6 input field unchanged and adds
187 fields: 29 from three ordinary roots, 146 from twelve composed roots,
and twelve from the source-owned file method with its generated EH pieces.
The first two groups introduce no uses of the four CRT bindings. The file
method introduces one cookie-data read and one generated cookie-check call.

| Original identity / normal SP1 provider | V6 uses | Expanded uses |
|---|---:|---:|
| `0x00ec408c` / `@__security_check_cookie@4` | 99 | 100 |
| `0x011c16bc` / `___security_cookie` | 93 | 94 |
| `0x00ecc071` / `__wcsicmp` | 1 | 1 |
| `0x00406d50` / `_strcat_s` | 3 | 3 |

These are complete input-use censuses, not extracted-member or runtime
coverage claims. The source-owned normal CRT continues to own one fresh
cookie/complement/init family, locale, errno and invalid-parameter policy.
Old numeric dependency addresses need not equal the new CRT's addresses.
No old cookie or other CRT state is copied.

## Distinct proofs for the two new fields

The parent is `0x005e0200`, recipe `2656-e9bf85b93a320794`, built with the
SP1 compiler and `/MT /Od /Oy- /GS /EHsc /Gy`. Its original section 241,
offset 21, physical symbol 506 is a zero-addend DIR32 reference to
`___security_cookie`. It retains the exact own-recipe source proof and maps
to serialized section 3, offset 21, symbol 4.

The generated handler's original section 242, offset 21, physical symbol
509 is a zero-addend REL32 reference to `@__security_check_cookie@4`. It
retains `PARENT_OWNED_GENERATED_EH_FIELD` and
`EXACT_GENERATED_EH_FIELD_RESOLUTION`, mapping to serialized section 4,
offset 21, symbol 6. The accepted observer covers the complete handler
piece over section interval `[8, 35)`, with zero non-field differences.
The parent and generated field keep their separate source and witness
classes. An agreeing global recipe symbol corroborates a numeric target;
its presence or absence does not change the physical field's proof class.

The contract joins each field to its exact source object, serialized member,
raw integration row, accepted observation record, external identity and
recipe. It preserves the normal fastcall cookie-check boundary and paired
four-byte normal cookie owner. EH/frame lifetime and whole-application
runtime ABI remain unapproved; the contract does not add a frame-handler
alias or assert that the remaining EH dependencies are closed.

## Reviewed contract and consumer

`tools/rebuild/crt_frontier_adoption_plan.py` reads only pinned saved
metadata and the exact own-source hash. The v2 contract and response were
independently reviewed with all 44,540 fields, all 198 uses, all four normal
archive/member identities, 94 cookie recipe proofs and the full provider
namespace. All four bindings are enabled. Eight synthetic tests cover
the prepared-versus-link receipt chain, field provenance, conflicting recipe
bindings, serialized identities, failure evidence, cookie coupling and
selection of existing response tokens.

`tools/rebuild/crt_frontier_adoption_contract.py` supplies the pure consumer
API `validate(plan_bytes, review_bytes, response_bytes, fields,
strong_definitions)`. It opens no files or native tools. It checks exact
artifact hashes, the complete field snapshot, every canonical use and all
selected strong-definition names, then returns only the enabled existing
tokens and evidence. Seven synthetic tests cover source drift, extra or
missing uses, role changes, strong definitions and cookie-pair policy.

An uncertain alias is disabled; uncertainty in either cookie binding
disables both cookie bindings. A consumer must first remove all four exact
inherited V6 CRT tokens before appending the enabled subset. This keeps a
disabled alias from surviving through the old response. Other IAT aliases
and unresolved CRT identities receive no new interpretation from this gate.

The final private outputs are `application-crt-frontier-contract-v2.json`,
`application-crt-frontier-contract-peer-v2.json`, and
`application-crt-frontier-proposal-v2.rsp`. Earlier failed and disabled
proposals remain private audit records. An actual expanded diagnostic still
requires its independently reviewed prepared-input freeze and root's
operation delegation. The gate grants no native permission or runtime
adoption, and this work executes no application.
