@call C:\Projects\Decompilation\runtime-next\link-v2\env.cmd
cd /d C:\Projects\Decompilation\runtime-next\link-v2\implibs
for %%f in (*.def) do lib.exe /nologo /def:%%f /machine:x86 /out:%%~nf_imp.lib >nul
dir /b *.lib
