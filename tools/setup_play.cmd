@echo off
rem Prepare a play folder for FalloutNV_selfbuilt.exe from your own Fallout: New Vegas install.
rem Run it from the folder that holds FalloutNV_selfbuilt.exe:   setup_play.cmd ["<FNV install folder>"]
rem It links the install's Data folder (nothing copied, nothing in the install changed) and copies the small
rem companion DLLs and default INI next to the exe. Run it once per folder.
setlocal
set "HERE=%~dp0"
set "GAME=%~1"
if not exist "%HERE%FNV-gamedata-01.zip" goto findinstall
rem Game-data release parts are here: unpack them and skip the install lookup.
for %%z in ("%HERE%FNV-gamedata-*.zip") do (
  echo Unpacking %%~nxz ...
  "%SystemRoot%\System32\tar.exe" -xf "%%z" -C "%HERE%." || (echo Could not unpack %%~nxz & exit /b 1)
)
echo Ready. You can delete the FNV-gamedata-*.zip files now. Start FalloutNV_selfbuilt.exe from this folder.
exit /b 0
:findinstall
if not "%GAME%"=="" goto have
for /f "tokens=3,*" %%a in ('reg query "HKLM\SOFTWARE\WOW6432Node\Bethesda Softworks\FalloutNV" /v "Installed Path" 2^>nul ^| "%SystemRoot%\System32\find.exe" "Installed Path"') do set "GAME=%%b"
if "%GAME%"=="" set "GAME=C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas"
:have
if "%GAME:~-1%"=="\" set "GAME=%GAME:~0,-1%"
if not exist "%GAME%\Data\FalloutNV.esm" (
  echo Could not find Fallout New Vegas at "%GAME%".
  echo Run:  setup_play.cmd "C:\path\to\Fallout New Vegas"
  exit /b 1
)
echo Using game install: %GAME%
if exist "%HERE%Data" (echo Data already present, leaving it.) else (mklink /J "%HERE%Data" "%GAME%\Data" >nul || (echo Could not link Data & exit /b 1))
for %%f in ("%GAME%\*.dll") do if not exist "%HERE%%%~nxf" copy /y "%%f" "%HERE%" >nul
if not exist "%HERE%Fallout_default.ini" copy /y "%GAME%\Fallout_default.ini" "%HERE%" >nul
if not exist "%HERE%steam_appid.txt" (echo 22380)>"%HERE%steam_appid.txt"
echo Ready. Start FalloutNV_selfbuilt.exe from this folder.
exit /b 0
