FalloutNV self-built exe (private build)
=======================================

This exe was compiled and linked from this repo's decompiled source. You need your own installed copy of
Fallout: New Vegas: the exe brings no game data, and part of its own data and resources still comes from your
installed game at build time.

How to play
1. Don't put this exe in your Steam install folder, and don't replace the original FalloutNV.exe.
2. Make a new folder, for example C:\Games\FNV-selfbuilt, and copy FalloutNV_selfbuilt.exe into it.
3. Open PowerShell in that folder and link your install's Data folder (this only makes a link; nothing is copied or changed):
     New-Item -ItemType Junction -Path Data -Target "C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data"
4. Copy these from the install folder into the new folder: every *.dll next to FalloutNV.exe, and Fallout_default.ini.
5. Create steam_appid.txt containing 22380.
6. Start Steam, then run FalloutNV_selfbuilt.exe.

The exe starts directly (no Steam DRM wrapper). Saves go to Documents\My Games\FalloutNV, like the normal game.
Back that folder up first if you care about your saves.

Keep this build private. It contains code and data from the original game.
