# CODE56 exclusion successor

`prepared_code56_successor.from_bytes` authenticates the fixed parent epoch,
56-export handoff and member ledger, then derives a collision-exclusion snapshot.
It does not read original objects, load a producer, emit code or select an
application cohort. Publication also requires the separately authenticated final
handoff review, a reviewed fixed metadata runner, and a coordinator lease.

All 14,478 historical records remain verbatim and in the same order. This
preserves the logical overlay, reviewed EH and unbound IOTask identity modes.
The 56 new ordinary records use the exact original physical namespace and carry
their complete serialization maps, member hash, root, handoff ordinal and full
field-proof ledger bindings. Names and original addresses must remain disjoint.
The successor has 14,528 ordinary names and 14,534 broader exclusions. These
counts do not establish application adoption. The absent application adoption
flag and null application-selected count remain unchanged.

The constructor checks metadata joins; accepted producer and native conformance
remain distinct evidence. It does not replay a compiler, Oracle, root policy or
native archive operation. Historical input stability is not freshly asserted.
