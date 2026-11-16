# Existing four CRT bindings in the combined V14 cohort

The separate V14 proposal covers 46,292 fields: the unchanged 46,237-field
V13 snapshot, 46 fields from the actual 21 emitted ordinary members, and
nine qualified UUID2768 fields. Requested batch counts are not used as
emission evidence. The fresh candidate namespace contains 14,555 providers.

The complete four-alias census increases from 202 to 204 uses: 103
cookie-check calls, 97 cookie-data references, one wide comparison and
three secure append calls. Both new uses belong to the same compiler-owned
GS pair in `CACHED-CODE-009-0087b400.obj`, recipe 0606:

| Original field | Serialized field | Normal provider |
|---|---|---|
| section 24 / offset 7 / symbol 199 | section 2 / offset 7 / symbol 5 | `___security_cookie` |
| section 24 / offset 50 / symbol 202 | section 2 / offset 50 / symbol 6 | `@__security_check_cookie@4` |

The exact own source is `src/fallout/misc/taskqueueinterface.cpp`. The void
member method takes a `TESObjectREFR*` and contains a union with a 32-byte
character array. Its pinned SP1 recipe uses `/MT /Od /Oy- /GS /EHsc /Gy /GF`;
the compiler generates the GS pair without a manual checker wrapper. The
ECX machineword argument, void helper result and normal 32-bit cookie
storage follow that i386 compiler boundary and the accepted normal CRT
storage model. Relocation operand width alone does not establish scalar
width. Choosing normal SP1 CRT does not impose that compiler on unrelated
callers without their own source evidence.

The original data-owner-required and explicit-CRT-candidate classifications
remain unchanged, as do false ABI and lifetime flags. The normal CRT owns
one fresh cookie family and the existing locale, errno and invalid-parameter
state. Its data addresses need not equal original CRT addresses. The
proposal adds no alias identity and approves no EH, RTTI or Steam binding.

`crt_v14_four_alias_plan.py` reuses the exact 21-member/46-field verifier and
the fixed UUID consumer. All nine UUID rows are compared as complete
canonical JSON records, including `original_field_proof`, `normative_field`
and unknown flags. Tuple/list forms of the same saved JSON are equivalent;
omitted fields or false-to-zero changes are not. The UUID consumer's
negative certificate occurrences and false closure, serialization,
selection, SDK-identity and runtime metadata remain in the proposal.

The producer binds accepted observer bytes and its peer review, both source
proof classes, all three own-source hashes, units and invoked helpers before
and after planning. It preserves the full observer ledger without walking
its 29,428 filesystem identity rows again; that underlying observation is
delegated to the accepted observer peer. This is a disclosed evidence scope,
not a replacement or weakening of the global identity checker.

`crt_v14_four_alias_contract.py` retains the pure five-argument `validate`
API, complete current field/namespace census and four-key policy. Uncertainty
in either cookie binding disables both. Consumers remove all four exact
inherited CRT tokens before applying the enabled subset. Earlier contracts
and sources remain frozen. Actual prepared-input review and a separately
delegated diagnostic operation remain required; no native execution,
provider adoption or runtime ABI approval is granted here.
