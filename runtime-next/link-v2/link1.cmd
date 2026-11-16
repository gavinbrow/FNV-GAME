@call C:\Projects\Decompilation\runtime-next\link-v2\env.cmd
cd /d C:\Projects\Decompilation\runtime-next\link-v2
link.exe @link.rsp > link1.log 2>&1
echo exit %errorlevel%
