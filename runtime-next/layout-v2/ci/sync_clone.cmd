@echo off
rem re-export the live tree into FNV-GAME (staging, untracked) and copy it over ci-test (no .git, nothing deleted)
set FNV_PROJ_ROOT=C:\Projects\Decompilation
python C:\Projects\Decompilation\runtime-next\layout-v2\ci\make_export_extra.py || exit /b 1
python C:\Projects\Decompilation\FNV-GAME\tools\export_repo.py || exit /b 1
robocopy C:\Projects\Decompilation\FNV-GAME C:\Projects\Decompilation\ci-test /E /XD .git /NFL /NDL /NJH /NJS /NP >nul
exit /b 0
