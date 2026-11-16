# Plan: self-compiled, playable FalloutNV (written 2026-11-16)

Decision (user, 2026-11-16): our own exe may start directly, without the SteamStub wrapper.
We never modify or unpack the shipped FalloutNV.exe or anything in the Steam install folder,
builds stay private, and no game bytes go to web workers.

## Where we are
- build-v7 code coverage is 99.82% of non-padding .text. Counting real source only (excluding 331 `_emit`
  byte-copy funclet targets), it is about 99.80%, with about 1.8 KB still to write.
- 19,609 B of relocation fields are still borrowed from the reference, and 48 calls resolve to the wrong copy of a function.
- Non-.text sections come from the reference. data-v1 produces about 30% of .rdata+.data from our objects.
- No source-built exe has ever started on its own. The only launch so far was the in-memory overlay at original addresses.

## Milestones (each one is a runnable, testable exe)
- **M1 Direct start at the original layout.** This is our own exe:
  - our code from build-v7, entry at our own CRT startup (WinMainCRTStartup from our objects), the .bind/wrapper section dropped;
  - an import directory and IAT generated from our objects' `__imp_` references (17 DLLs, about 280 slots);
  - resources from our own .rc;
  - data sections still from the reference for now.
  - It runs from an isolated test folder: a junction to the install's Data, copies of the companion DLLs, and steam_appid.txt. The install folder is never changed.
  - Pass: it reaches the main menu, then a save loads.
- **M2 Own every address field.** Borrowed relocation fields go to 0 and the wrong-copy callees are fixed. Our own .reloc is generated from our objects and the rebase test comes out clean. The M1 exe should then still run when loaded at a different base.
- **M3 Own data.** vtables, RTTI (original class names), EH tables, strings, CRT init arrays, TLS and initialized globals all come from our objects. This is the largest step, and data-v1 is the starting point.
- **M4 Real link / free layout.** All units and contributions go through link.exe (or our own linker) with symbolic references only. The exe is laid out in our own order, with no reference bytes.
- **M5 Playable regression harness.** Launch, reach the menu, load a save, play a scripted few minutes and exit cleanly. It runs after every build.

## Rules of the road
- Each step keeps the filled build's check (filled_equals_reference) and the rebase test green.
- Every edit gets a backup, and each workstream owns separate files.
