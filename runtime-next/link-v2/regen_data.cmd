@echo off
cd /d C:\Projects\Decompilation\runtime-next\link-v2
set DV3_CNAMES=1
set DV3_OUT=C:\Projects\Decompilation\runtime-next\link-v2\data_out
set DV3_SKIP=C:\Projects\Decompilation\runtime-next\link-v2\skip_ranges.json
set DV3_DROPT=C:\Projects\Decompilation\runtime-next\link-v2\dropt.json
python -I -c "import pathlib;[p.unlink() for p in pathlib.Path('data_out').glob('*.asm')]+[p.unlink() for p in pathlib.Path('data_out').glob('*.obj')]"
python -I ..\data-v3\gen.py || exit /b 1
call .\asm_data.cmd
