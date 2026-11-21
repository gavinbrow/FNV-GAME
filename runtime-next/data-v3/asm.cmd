@echo off
if "%FNV_MSVC9_ROOT%"=="" set FNV_MSVC9_ROOT=C:\path\to\Decompilation\FNV\tools\vc2008
set PATH=%FNV_MSVC9_ROOT%\VC\bin;%PATH%
cd /d "%~dp0out"
for %%f in (*.asm) do ml.exe /c /coff /nologo /Cp /Fo %%~nf.obj %%f
