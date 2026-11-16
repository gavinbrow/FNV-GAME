FalloutNV self-built exe (private build)
=======================================

This exe was compiled and linked from this repo's decompiled source. It's the game's program only. You need your
own installed copy of Fallout: New Vegas for the game content (the Data folder: maps, models, sounds, quests).

How to play without an installed copy (any PC)
1. Make a new folder, for example C:\Games\FNV-selfbuilt, and unzip this build release into it.
2. From the "game-data" release, download all six FNV-gamedata-*.zip parts (about 9.6 GB) into the same folder.
3. Double-click setup_play.cmd. It unpacks the parts (Data folder, DLLs, INIs); then delete the zips if you like.
4. Run FalloutNV_selfbuilt.exe. Steam doesn't need to be installed or running. Saves stay in this folder.

How to play with your installed copy
1. Make a new folder anywhere, for example C:\Games\FNV-selfbuilt, and unzip this release into it.
   Don't put it in your Steam install folder, and don't replace the original FalloutNV.exe.
2. Double-click setup_play.cmd (or run it with your install path:  setup_play.cmd "D:\Games\Fallout New Vegas").
   It finds your install, links its Data folder (nothing is copied or changed in the install), and copies the
   game's small DLLs and default INI next to the exe.
3. Run FalloutNV_selfbuilt.exe.

The exe starts directly; there is no Steam DRM wrapper. See the release notes for whether Steam needs to be open.
With your installed copy, saves go to Documents\My Games\FalloutNV like the normal game, so back that folder up
first if you care about it. With the game-data parts, the included Fallout.ini keeps saves and settings in the play
folder instead.

Keep this build private: it still contains code and data from the original game.
