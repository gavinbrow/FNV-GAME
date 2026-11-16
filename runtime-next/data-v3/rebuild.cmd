@echo off
rem data-v3: symbolic .rdata/.data/.tls/CONST (+bss tail) as MASM, assembled with the local ml.exe, round trip proven. About 3 min.
rem produced_pieces.json comes from data-v1 (dump_pieces.py after data-v1\place.py; scratch pickle in %TEMP%), run it first if data-v1 changed.
set DV3=%~dp0
python -I "%DV3%gen.py" || exit /b 1
call "%DV3%asm.cmd" || exit /b 1
python -I "%DV3%verify.py" || exit /b 1
python -I "%DV3%postproc.py" > "%DV3%out\postproc.log"
copy /y "%DV3%out\symbolic.json" "%DV3%symbolic.json" >nul
