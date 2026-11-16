struct FUN_007aa2a0_shell : MessageMenu {
    void FUN_007aa2a0();
    int FUN_0059bb30();
    void FUN_00a1db20();
    void FUN_00a1d910();
    void* FUN_00726070(int, int);
};
struct TimerCalls { void FUN_00771520(); unsigned int FUN_00825c00(); };
struct TileCalls { bool FUN_00a01230(int); };
struct MenuActionCalls { void FUN_00700320(); };
void __cdecl FUN_007aa530();
extern double DAT_01012060;
void FUN_007aa2a0_shell::FUN_007aa2a0() {
    reinterpret_cast<TimerCalls*>(&MMTimer)->FUN_00771520();
    static unsigned int lastCheckTime = reinterpret_cast<TimerCalls*>(&MMTimer)->FUN_00825c00();
    if (reinterpret_cast<TimerCalls*>(&MMTimer)->FUN_00825c00() - lastCheckTime < 200) return;
    {
        lastCheckTime = reinterpret_cast<TimerCalls*>(&MMTimer)->FUN_00825c00();
        if (FUN_007a92a0()) {
            if (static_cast<unsigned char>(FUN_007a9280(reinterpret_cast<char*>(FUN_007a92a0()))) == 0) {
                if (reinterpret_cast<TileCalls*>(pTiles[0])->FUN_00a01230(0xfa3)) {
                    if (FUN_0059bb30() == 4) {
                        if (uiMessageStartTime == 0) {
                            FUN_00a1db20();
                        } else {
                            FUN_007aa530();
                            uiMessageStartTime = 0;
                        }
                    } else {
                        if (FUN_0059bb30() == 1) {
                            unsigned int message = FUN_007a92a0();
                            if (!uiMessageStartTime)
                                uiMessageStartTime = reinterpret_cast<TimerCalls*>(&MMTimer)->FUN_00825c00();
                            if (*reinterpret_cast<float*>(message + 0x44) > DAT_01012060) {
                                if (*reinterpret_cast<float*>(message + 0x44) <=
                                   (unsigned int)(reinterpret_cast<TimerCalls*>(&MMTimer)->FUN_00825c00() - uiMessageStartTime)) {
                                    if (message == *reinterpret_cast<FUN_006f2270*>(&g_011da53c)->GetLast()) {
                                        reinterpret_cast<MenuActionCalls*>(FUN_00726070(0x1772,1))->FUN_00700320();
                                        FUN_007aa530();
                                    } else {
                                        FUN_00a1d910();
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}