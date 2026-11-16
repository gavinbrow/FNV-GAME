
extern "C" unsigned int __cdecl FUN_00457fe0();
extern "C" int __cdecl FUN_00a00940(const char*, int);
extern "C" char str_01072108;
struct Fade {
    int state;
    int flags;
    float amount;
    void __thiscall FUN_00a0a270(float value, int enabled);
};
struct Resources {
    float __thiscall FUN_00a011b0(int id);
    Fade* __thiscall FUN_00a00e90(int id);
};
struct Widget {
    bool __thiscall FUN_00a01230();
};
struct HackingMenuDecomp : HackingMenu {
    Widget* __thiscall FUN_00726070(int id);
    void __thiscall FUN_0076a9d0();
};
void HackingMenuDecomp::FUN_0076a9d0() {
    static float delay = (*reinterpret_cast<Resources**>(reinterpret_cast<char*>(this) + 0x11c))->FUN_00a011b0(FUN_00a00940(&str_01072108, -1));
    if (*reinterpret_cast<int*>(reinterpret_cast<char*>(this) + 0x1c4) == 4 && FUN_00726070(0x1006)->FUN_00a01230()) {
        return;
    } else {
    static unsigned int nextUpdate = 0;
    if (FUN_00457fe0() > nextUpdate && *reinterpret_cast<Fade**>(reinterpret_cast<char*>(this) + 0x1d4) != 0) {
        (*reinterpret_cast<Fade**>(reinterpret_cast<char*>(this) + 0x1d4))->FUN_00a0a270(
            (*reinterpret_cast<Fade**>(reinterpret_cast<char*>(this) + 0x1d4))->amount == 1.0 ? 0.0f : 1.0f, 1);
        nextUpdate = static_cast<unsigned int>(FUN_00457fe0() + delay);
    } else if (*reinterpret_cast<Fade**>(reinterpret_cast<char*>(this) + 0x1d4) == 0) {
        *reinterpret_cast<Fade**>(reinterpret_cast<char*>(this) + 0x1d4) = (*reinterpret_cast<Resources**>(reinterpret_cast<char*>(this) + 0x11c))->FUN_00a00e90(0xfa3);
    }
    }
}