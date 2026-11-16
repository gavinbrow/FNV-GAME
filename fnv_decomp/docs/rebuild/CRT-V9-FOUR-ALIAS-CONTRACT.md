# Existing four CRT bindings in the V9 cohort

The separate V9 contract refreshes the same four normal SP1 CRT bindings
for 45,318 saved input fields. Every complete V8 raw field record is
preserved, including hydrated annotations; three ordinary CODE fields are
added. None introduces a use of the existing CRT aliases.

The complete alias census therefore remains 202: 102 cookie-check calls,
96 cookie-data references, one wide comparison and three secure append
calls. The normal CRT continues to own its fresh cookie family and shared
locale, errno and invalid-parameter state. Original CRT state addresses do
not constrain the normal provider's data addresses.

The three exact new maps are:

| Caller | Original section / offset / symbol | Serialized section / offset / symbol | Target |
|---|---|---|---|
| `0x004f8ac0` | 79 / 30 / 305 | 2 / 30 / 7 | `0x00406d30/code` |
| `0x0096aaf0` | 65 / 21 / 395 | 2 / 21 / 8 | `0x0096abc0/code` |
| `0x0096aaf0` | 65 / 36 / 394 | 2 / 36 / 7 | `0x0096aa40/code` |

All three are zero-addend REL32 fields with their exact saved source proofs.
The third included function, `0x005d43c0`, has no fields. The numeric
`0x00406d30/code` target remains distinct from the approved append identity
at `0x00406d50/code`; no name or provider follows from their proximity.

`crt_v9_four_alias_plan.py` joins the new raw/serialized records, verifies
the full snapshot and fresh provider namespace, and retains the accepted
202 binding rows unchanged. It uses saved metadata only, without replaying
the indexed source-context reader or rehydrating earlier cookie proofs.
Both own-source hashes, the units hash and invoked helper sources remain
bound. Ordinary and generated EH proof classes remain distinct.

`crt_v9_four_alias_contract.py` exposes the same pure five-argument
`validate` API. It checks the exact reviewed artifacts, full hydrated field
snapshot, canonical roles and complete use census, and rejects collisions
with enabled aliases. Cookie bindings remain coupled. Consumers remove all
four exact inherited CRT tokens before applying the enabled subset.

This refresh adds no CRT alias and does not approve the open frame-handler
or dynamic-cast contracts. All V8 files remain frozen. Prepared-input review
and a separately delegated diagnostic operation remain required; these
tools grant no native execution, runtime ABI or provider-adoption approval.
