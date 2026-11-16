@echo off
set PATH=C:\Projects\Decompilation\FNV\tools\vc2008\VC\bin;%PATH%
cd /d C:\Projects\Decompilation\runtime-next\link-v2\data_out
for %%f in (*.asm) do ml.exe /c /coff /nologo /Cp /Fo %%~nf.obj %%f
python -I C:/Projects/Decompilation/runtime-next/link-v2/fix_sections.py
