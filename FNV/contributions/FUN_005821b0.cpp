extern char DAT_01183040;
extern char DAT_01186ab0;
extern "C" void* __cdecl FUN_00ec43fb(int input, int mode, const void* type, const void* name, int flags);

struct ControllerArchive : FUN_00581fb0_Class {
    void __thiscall FUN_005821b0(int source);
};

void ControllerArchive::FUN_005821b0(int source) {
    FUN_005822a0_cls* loaded = static_cast<FUN_005822a0_cls*>(FUN_00ec43fb(source, 0, &DAT_01183040, &DAT_01186ab0, 0));
    if (loaded == 0)
        return;
    for (unsigned int i = 0; i < 6; ++i) {
        FUN_00581fb0(i, loaded->FUN_005822a0(i));
    }
}