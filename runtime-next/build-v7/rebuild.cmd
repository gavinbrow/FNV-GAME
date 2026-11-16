@echo off
rem Build-v7: re-verify accepted local-target contributions (record compiler/flags/entry, CRLF as the checker saw it, EH stub+funclets),
rem pass 1 assemble without ICF, ICF fold (icf_v7.py), final assemble. About 3 min. Needs 12 workers.
if "%FNV_MSVC9_RTM_ROOT%"=="" set FNV_MSVC9_RTM_ROOT=C:\Projects\Decompilation\FNV\tools\vc2008rtm
set FNV_V5_FIXUPS=
python -I "%~dp0verify_v7.py" 12 || exit /b 1
set FNV_ICF=0
rem wB: pass 1 runs without the binding overlay so the ICF fold is computed from the same wanted-name list as before (overlay applies in the final assemble only)
set FNV_OVERLAY=0
python -I "%~dp0assemble_v7.py" > "%~dp0run0.log" 2>&1 || exit /b 1
set FNV_ICF=1
set FNV_OVERLAY=1
python -I "%~dp0icf_v7.py" 8 || exit /b 1
python -I "%~dp0assemble_v7.py" > "%~dp0run.log" 2>&1
rem wB: own .reloc for .text (writes FalloutNV_v7_filled_ownreloc.exe, merges own_reloc into progress.json)
if not errorlevel 1 python -I "%~dp0..\reloc-v7\ownreloc.py" > "%~dp0ownreloc.log" 2>&1
set RC=%ERRORLEVEL%
if exist "%~dp0obj" rmdir /s /q "%~dp0obj"
if exist "%~dp0run0.log" del "%~dp0run0.log"
type "%~dp0run.log" | findstr /c:"headline_pct" /c:"coverage_pct" /c:"ours_bytes" /c:"undecompiled_bytes" /c:"filled_equals"
exit /b %RC%
