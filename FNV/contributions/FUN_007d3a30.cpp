signed char __cdecl FUN_00703fa0();
struct OSGlobalsKeyed { void* FUN_00877720(int key); };
struct WheelAction { void FUN_00a24b70(); };
struct OptionsListSort { void FUN_007314c0(void (*comparator)(), int begin, int end); };
void __cdecl FUN_007cfe40();
void __cdecl FUN_007d3a30() {
    if (DAT_011daac0) {
        if (FUN_00703fa0() == 1) {
            reinterpret_cast<WheelAction*>(
                reinterpret_cast<OSGlobalsKeyed*>(g_osGlobals)->FUN_00877720(
                    *reinterpret_cast<int*>(reinterpret_cast<char*>(DAT_011daac0) + 0x1c8)
                )
            )->FUN_00a24b70();
            reinterpret_cast<StartMenu_Wrap*>(DAT_011daac0)->FUN_0075f6f0(StartMenu::FLAG_OPTIONS_DIRTY, true);
            reinterpret_cast<OptionsListSort*>(&DAT_011daac0->lbOptions)->FUN_007314c0(&FUN_007cfe40, 0, 0x7fffffff);
        }
    }
}