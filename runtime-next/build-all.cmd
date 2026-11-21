@echo off
rem One-command build of the self-compiled FalloutNV exe.  Usage: build-all.cmd --out <dir> [--no-harness] [--require-harness] [--layout G] [--skip-data-v1]
rem Environment (defaults are the local paths): FNV_PROJ_ROOT FNV_GAME_DIR FNV_MSVC9_RTM_ROOT FNV_MSVC9_ROOT FNV_REF_IMAGE FNV_PY_SITE
setlocal
if "%FNV_PROJ_ROOT%"=="" for %%i in ("%~dp0..") do set "FNV_PROJ_ROOT=%%~fi"
if "%FNV_GAME_DIR%"=="" set "FNV_GAME_DIR=C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas"
if "%FNV_MSVC9_RTM_ROOT%"=="" set "FNV_MSVC9_RTM_ROOT=C:\path\to\Decompilation\FNV\tools\vc2008rtm"
if "%FNV_MSVC9_ROOT%"=="" set "FNV_MSVC9_ROOT=C:\path\to\Decompilation\FNV\tools\vc2008"
if "%FNV_MSVC8_ROOT%"=="" set "FNV_MSVC8_ROOT=C:\path\to\Decompilation\FNV\tools\vc8sp1"
if "%FNV_REF_IMAGE%"=="" set "FNV_REF_IMAGE=C:\path\to\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe"
set "PYTHONDONTWRITEBYTECODE=1"
set "PYEXE=python"
where python >nul 2>nul || set "PYEXE=C:\Python312\python.exe"
"%PYEXE%" "%~dp0build_all.py" %*
exit /b %ERRORLEVEL%
