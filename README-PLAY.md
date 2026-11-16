FalloutNV self-built exe (private build)
=======================================

This exe was compiled and linked from this repo's decompiled source. It's the game's program only. You need your
own installed copy of Fallout: New Vegas for the game content (the Data folder: maps, models, sounds, quests).

How to play
1. Make a new folder anywhere, for example C:\Games\FNV-selfbuilt, and unzip this release into it.
   Don't put it in your Steam install folder, and don't replace the original FalloutNV.exe.
2. Double-click setup_play.cmd (or run it with your install path:  setup_play.cmd "D:\Games\Fallout New Vegas").
   It finds your install, links its Data folder (nothing is copied or changed in the install), and copies the
   game's small DLLs and default INI next to the exe.
3. Run FalloutNV_selfbuilt.exe.

The exe starts directly; there is no Steam DRM wrapper. See the release notes for whether Steam needs to be open.
Saves go to Documents\My Games\FalloutNV like the normal game, so back that folder up first if you care about it.

Keep this build private: it still contains code and data from the original game.
