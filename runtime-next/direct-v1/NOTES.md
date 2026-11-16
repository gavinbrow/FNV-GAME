# direct-v1 (M1) notes, 2026-11-16
Regenerate: `python make_direct.py` -> FalloutNV_direct.exe (from ../build-v7/FalloutNV_v7_filled.exe).
- Entry = 0xECC4DB (RVA 0xACC4DB) = WinMainCRTStartup (call __security_init_cookie; jmp __tmainCRTStartup @0xECC35D, which calls WinMain 0x86A850 at 0xECC46B). Found by locating the only call to 0x86A850.
- .bind section dropped (nothing in other sections / .reloc references VA 0x1409000-0x147B000); cert data dir zeroed; SizeOfImage 0x1009000; checksum fixed.
- BORROWED from reference (unchanged): import dir (RVA 0xD8062C in .data, 17 DLLs / 280 slots, intact and valid), IAT at 0xBDF000, TLS dir (0xD0147C, callback table empty), .rsrc, .rdata/.data, .reloc. Import dir NOT yet regenerated from our objects.
- run/: exe, companion DLLs, Data junction (create with PowerShell New-Item -ItemType Junction; Git-bash mklink mangles paths and makes a broken link), steam_appid.txt, Fallout.ini (user's copy + bUseMyGamesDirectory=0 in [General]), FalloutPrefs.ini (user's copy, bFull Screen=0, iAdapter=0), Saves\ (one copied save).
- bUseMyGamesDirectory=0 makes game read/write INIs, Saves, Plugins.txt relative to cwd, so nothing goes to Documents\My Games. Without FalloutPrefs.ini the exe spawns FalloutNVLauncher.exe (first-run behavior) - that was the early "launcher appears" confusion.
- Backups of My Games\FalloutNV and AppData\Local\FalloutNV in backup/. The accidental launcher run rewrote FalloutPrefs.ini (identical hash) and Local\NVDLCList.txt.
- Tools: dbg.py (ctypes debugger: crash regs/stack/ebp chain, --trace API log), d86.py (disasm helper).
- First crash was just the broken Data junction (null globals.xml lookup at 0xA087E5), not a code bug.
- Input: keybd_event with scancodes works (Down/Enter); mouse_event relative moves unreliable.

## Round 2 (2026-11-16)
### Own import tables (build_imports.py, iat_spec.json)
- make_direct.py now regenerates the import directory (RVA 0xD8062C, 18 descriptors), ILT blocks, hint/name stream, DLL names and the IAT image (RVA 0xBDF000) from iat_spec.json. `python build_imports.py --verify <exe>` -> region (6688 B) and IAT (1188 B) are BYTE-IDENTICAL to the reference tables. The two exe variants (own vs --borrowed) are byte-identical for that reason.
- Layout model (derived, reproduced exactly): descriptors in link order; ILT/IAT blocks sorted by IAT address; hint/name stream = per-DLL batch of hint/name entries (order = original linker member order, stored as `rank`), then the DLL name, even-padded; 'phase 2' entries (71 KERNEL32, 8 USER32, 2 ADVAPI32 = CRT-pulled members) come after the last DLL name with no names between; ordinal imports (XINPUT1_3 2,3; DSOUND 11; WSOCK32 x21 ...) have only ILT entries.
- What is still borrowed in the spec: slot order/IAT RVAs (dictated by the code's absolute addresses), per-entry hint values (the SDK libs here carry hint 0 for most, the original build used libs with real hints) and the hint/name member order. Validation (validate_imports.py): our 288 `__imp_` symbols in pinned-build/obj_v3 reference 162 slots by name + 9 by `IMP_<va>` name = 171 of 280 slots (the other ~109 are CRT/libcmt imports not present as our objects: HeapAlloc etc.); 204 of 256 named imports are found under the right DLL in the PlatformSDK import libs; the 52 others (steam_api 11, d3dx9_38 25 (SDK lib is d3dx9.lib), binkw32 9, libvorbisfile 6, DirectInput8Create) have no lib locally.
- Our objects' import symbols are C++-mangled stubs (`__imp_?Name@@YG...`, `?IMP_fdf0a8@fnv_...`), not real `__imp__Name@N`, so a real link.exe-produced table is M4 work.
### Own resources (res-src/resources.rc, rc_lite.py, build_rsrc.py, link_rsrc.py)
- rc.exe is NOT present locally; cvtres.exe (VC2008) is. Pipeline: extract_res.py (binary inputs from the installed exe -> build/res/, not source: FalloutNV.ico = icon group 101 + icons 1-12, bitmap180.bmp, spafile.bin) -> rc_lite.py (our mini rc: RCDATA/BITMAP/ICON/VERSIONINFO/manifest -> .res) -> cvtres.exe -> link_rsrc.py (lays out .rsrc$01/$02 like link.exe).
- Result .rsrc (834184 B) is BYTE-IDENTICAL to the reference. Quirks reproduced: SPAFILE's type is the *string* "RT_RCDATA" (original .rc used an undefined symbol), directory MajorVersion=4, data entry CodePage 1252, 4-byte data alignment (cvtres 9 uses 8), 'PADDING' pad bytes, leaf string block wLength excluding the trailing pad. manifest.xml in res-src is the installed exe's manifest (806 B text).
### Harness (harness.py)
- `python harness.py <exe> [--run DIR] [--play 120] [--tag T] [--exit-keys up,enter,enter]` -> harness-out/<tag>/verdict.json + screenshots. Main menu detected by the orange logo pixels, world by the orange HP/AP HUD; Continue (Down, Enter, Enter) loads the copied save; harness_watchdog.txt gets a Python traceback if the harness itself hangs.

### Harness results (new build-v7 filled exe copied 01:38; its bytes are identical to the previous filled exe)
- harness.py exit path: Esc -> pause menu (Continue/Save/Load/Settings/Help/Quit); first Down only activates the menu, so keys = down x6, enter (Quit), down, enter ("Main Menu / Exit Game / Cancel" -> Exit Game).
- direct_own (FalloutNV_direct.exe, own import table + own .rsrc): PASS, menu at ~49 s after launch, world loaded 3 s after Continue->Yes, 120 s of walk/turn/Pip-Boy, clean exit code 0, no WER/Application Error events. harness-out/direct_own/verdict.json.
- rebased_1000000 (rebase_exe.py: static rebase to ImageBase 0x1000000 using the image .reloc, 351,931 fields): PASS, same results.
- FalloutNV_direct_borrowed.exe is byte-identical to FalloutNV_direct.exe (own tables == reference tables), so it was not run separately.
