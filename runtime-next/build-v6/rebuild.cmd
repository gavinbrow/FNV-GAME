@echo off
rem Re-verify newly accepted local-target contributions (+ their EH pieces) and reassemble build-v6. Needs ~2 min.
rem FNV_V5_FIXUPS stays unset (reference-assisted callee fixups are opt-in only).
if "%FNV_MSVC9_RTM_ROOT%"=="" set FNV_MSVC9_RTM_ROOT=C:\Projects\Decompilation\FNV\tools\vc2008rtm
set FNV_V5_FIXUPS=
python -I "%~dp0verify_v6.py" 12 && python -I "%~dp0assemble_v6.py" > "%~dp0run.log" 2>&1
set RC=%ERRORLEVEL%
if exist "%~dp0obj" rmdir /s /q "%~dp0obj"
type "%~dp0run.log" | findstr /c:"headline_pct" /c:"coverage_pct" /c:"ours_bytes" /c:"undecompiled_bytes" /c:"filled_equals"
exit /b %RC%
