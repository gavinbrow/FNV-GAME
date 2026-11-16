#include <windows.h>
extern "C" int DAT_010d1464;
struct EmbeddedItem {
    int m00,m04,m08,m0c,m10,m14,m18,m1c,m20,m24,m28,m2c,m30;
    void __thiscall FUN_00dd7200();
};
struct EmbeddedMember { void __thiscall FUN_00dd7ec0(); };
struct FUN_00d5ffd0_class {
    void* vtable;
    void __thiscall FUN_00d5ff50();
    void __thiscall FUN_00cbf1a0();
    void __thiscall FUN_00d5ffd0();
};
void FUN_00d5ffd0_class::FUN_00d5ffd0() {
    vtable = &DAT_010d1464;
    FUN_00d5ff50();
    EmbeddedItem* end = reinterpret_cast<EmbeddedItem*>(reinterpret_cast<char*>(this)+0xa94);
    for(int i=40;i>=0;--i) {
        (--end)->FUN_00dd7200();
    }
    reinterpret_cast<EmbeddedMember*>(reinterpret_cast<char*>(this)+0x28)->FUN_00dd7ec0();
    DeleteCriticalSection(reinterpret_cast<CRITICAL_SECTION*>(reinterpret_cast<char*>(this)+4));
    FUN_00cbf1a0();
}