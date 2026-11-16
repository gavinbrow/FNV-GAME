@echo off
rem link-v2: steps that read build products (obj_v3, data-v1 strict exe, units.json) - run under lockrun.py
cd /d C:\Projects\Decompilation\runtime-next\link-v2
python -I prep3.py || exit /b 1
python -I prep_contribs.py || exit /b 1
python -I label_alias.py || exit /b 1
set DV3_CNAMES=1
set DV3_OUT=C:\Projects\Decompilation\runtime-next\link-v2\data_out
set DV3_SKIP=C:\Projects\Decompilation\runtime-next\link-v2\skip_ranges.json
set DV3_DROPT=C:\Projects\Decompilation\runtime-next\link-v2\dropt.json
python -I ..\data-v3\gen.py || exit /b 1
call asm_data.cmd
