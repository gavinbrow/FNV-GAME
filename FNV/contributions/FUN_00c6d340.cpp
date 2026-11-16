__declspec(thread) unsigned int hkThreadModeSlots[174];

struct CallbackTarget {
    void FUN_00c905b0();
};
extern CallbackTarget* DAT_01267bb8;

struct ScopedThreadMode {
    unsigned int previous;

    __forceinline ScopedThreadMode()
        : previous(hkThreadModeSlots[173]) {
        hkThreadModeSlots[173] = 16;
    }

    __forceinline ~ScopedThreadMode() {
        hkThreadModeSlots[173] = previous;
    }
};

void __cdecl FUN_00c6d340() {
    ScopedThreadMode scope;
    if (DAT_01267bb8)
        DAT_01267bb8->FUN_00c905b0();
}