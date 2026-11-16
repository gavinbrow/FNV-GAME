@echo off
rem data-v1: place our objects' .rdata/.data/.xdata pieces in the reference and write FalloutNV_data_strict.exe / _filled.exe.
rem Reads (never writes) pinned-build\obj_v3, build-v7 (icf_map, relocs, strict/filled exe) and the reference exe. About 10-20 min, 8 workers.
rem Run build-v7\rebuild.cmd first if its outputs are stale. Scratch pickles go to %TEMP%.
set DV=%~dp0
python -I "%DV%phase0.py" "%TEMP%\dv1_phase0.pkl" || exit /b 1
python -I "%DV%place.py" "%TEMP%\dv1_phase0.pkl" "%TEMP%\dv1_placed.pkl" > "%DV%place.log" 2>&1 || exit /b 1
python -I "%DV%report.py" "%TEMP%\dv1_placed.pkl" > "%DV%report.log" 2>&1
exit /b %ERRORLEVEL%
