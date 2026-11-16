# Existing four CRT bindings in the V10 cohort

The separate V10 contract covers 45,947 saved fields. It preserves all
45,318 complete V9 raw records, including annotations, and adds the exact
629 fields from 68 ordinary CODE members. The full original proof records
remain unchanged: 364 CODE, 261 DATA and four IAT fields. None adds a use of
an existing CRT alias or a CRT-contract field.

The global CRT census therefore remains 202 uses: 102 cookie-check calls,
96 cookie-data references, one wide comparison and three secure append
calls. The same normal SP1 CRT owns its fresh cookie family, locale, errno
and invalid-parameter state. Normal data addresses need not equal original
CRT state addresses. No additional CRT alias is introduced.

The pretriage joins exactly 68 original member envelopes and 629 normative
fields through the shared `application_link_wave10.verify_proof_ledger`
helper. It verifies ordered proof hashes, source roots, authority, output
member identities and physical fields, then retains the complete normative
records and their unknown flags. The source evidence is explicitly marked
as unenriched; there is no guessed hydration. The CRT-specific layer checks
recipe and addend identity and rejects an unexpected use or role collision
at an existing CRT key.

`crt_v10_four_alias_plan.py` reuses that join, reconciles it with the saved
pretriage, and checks every new physical-to-serialized map against the full
cohort ledger. Any attached original field proof must equal its normative
record. It preserves the four binding dictionaries and labels their
historical proof scope separately from V10's zero new CRT uses. It also
checks the fresh strong-definition namespace and complete 202-use census.

`crt_v10_four_alias_contract.py` exposes the same pure five-argument
`validate` API. It binds the reviewed contract and exact response, hashes
the full hydrated field view, checks each canonical role and use, and
rejects collisions with enabled aliases. Cookie bindings remain coupled.
Consumers remove all four exact inherited CRT tokens before applying the
enabled subset, so a disabled binding cannot survive through an earlier
response.

All V9 files remain frozen. This refresh approves neither the open frame
handler nor dynamic-cast boundary. Actual prepared-input review and a
separately delegated diagnostic operation remain required; these metadata
tools grant no native execution, provider adoption or runtime ABI approval.
