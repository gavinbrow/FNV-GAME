# Current EHFile frame-handler obligation

The accepted V7 diagnostic exposes one CRT-contract obligation at original
`0x00ec3d33`: native compiler symbol `___CxxFrameHandler3`. Saved generated-EH
field evidence identifies it independently of a nearest-address or source-name
guess. This triage proposes no alias and changes no V7 input, producer, consumer
or accepted contract.

The exact caller is the owned handler of parent `0x005e0200`, recipe2656. Its
REL32 field is physical section242 +31, target symbol508, zero addend. The
projection preserves it as section4 +31, undefined symbol5, under canonical name
`_fnv_undefined_86b5006e5d6d2a0348c632bbd16e24c66b0a3804def721a1235e0f2a4af3c7e9`.
The V7 group retains that same parent, field and generated-field proof family.

The saved parent comparison covers a 161-byte ordinary body, an eight-byte
cleanup and a 27-byte handler, plus 44 bytes of owned metadata. All recorded
nonfield differences are zero. FuncInfo occupies metadata offsets [8,44),
preceded by an eight-byte unwind map. Handler field +26 points to FuncInfo at
original `0x0114b274`; its physical symbol1003 becomes projected symbol22 at
section5 +8. There is one unwind state, 0 to -1, with cleanup symbol995.
These ownership and comparison facts preserve the descriptor; they do not
approve its frame coordinates or the cleanup's source-member/lifetime role.

Saved normal-runtime evidence supplies a concrete provider candidate. The
accepted original EH fixture's preparation maps `___CxxFrameHandler3` to
`LIBCMT:_trnsctrl_.obj`, using the pinned SP1 `LIBCMT` hash. The selected-CRT
coordinate report identifies a complete 54-byte fixture handler range and its
forwarding chain through `frame.obj` and `lowhelpr.obj`. That report records
registration-node forwarding and the conditional equation:

```text
registration node = ordinary EBP - 12
cleanup EBP = registration node + 12 = ordinary EBP
```

Its explicit assumptions include the exact inspected handler/registration form
and ordinary nonvolatile-register preservation by intervening normal calls.
Its parent witness is unit802 and its source-authored fixture, rather than this
recipe2656 parent. Transfer of those coordinates to the current parent requires
an exact saved witness; equal names, handler sizes or a conventional public
four-argument declaration do not supply one.

The normal fixture range is not an observation of the original dispatcher body
at `0x00ec3d33`. The saved reports contain a map-visible member name and the
normal archive's hash, but no whole-member hash for `_trnsctrl_.obj`. No new
archive, image or object was read to strengthen that evidence. The bootstrap
preparation contains no `CxxFrameHandler3` provider entry and intentionally
passed no exception across its mixed-compiler boundaries. Its successful
startup/cookie tests cannot establish this EH contract.

The unresolved machine boundary includes the handler's hidden FuncInfo/register
state, incoming OS SEH arguments, registration-node layout and state/cookie
coordinates. This is a compiler-generated dispatch contract. No ordinary C
wrapper or newly invented typed function declaration resolves it. The saved
inputs do not contain an authoritative public header declaration for that
boundary, so this triage records the prototype as unknown.

Before any future normal functional adoption, the owner must reconcile the
current parent's exact frame/descriptor witness, unwind actions and cleanup
receiver/lifetime roles, SafeSEH registration, compatible CRT exception family,
cookie state and all remaining CODE/DATA dependencies. Broader catch, throw,
type-descriptor and callback ownership must remain explicit wherever reachable.
Normal CRT state must belong to the chosen fresh runtime; preserving original
numeric dependency addresses is not a substitute for those contracts. All
runtime ABI, source-member, frame and provider-selection flags remain false.
Original dispatcher byte identity is not a prerequisite to a reviewed normal
functional substitution; the unresolved current frame and lifetime contracts
are the material compatibility gates.
