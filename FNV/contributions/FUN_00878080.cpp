struct StateControl {
    bool __thiscall FUN_0044b130();
    void __thiscall FUN_0082f1f0();
};
struct ManagedEntry {
    void __thiscall FUN_00866a90();
};
void* __cdecl FUN_00401020();
ManagedEntry* __stdcall FUN_00401020(int mode, unsigned int index, bool* enabled);
struct FUN_00878080_Class {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    StateControl control;
    void __thiscall FUN_00878080(int unused);
};
void FUN_00878080_Class::FUN_00878080(int unused) {
    if (!control.FUN_0044b130()) return;
    if (reinterpret_cast<FUN_00878110_Class*>(FUN_00401020())->FUN_00878110() > 0) {
        bool enabled = true;
        {
            unsigned int index = 0;
            for (; index <= reinterpret_cast<FUN_00878110_Class*>(FUN_00401020())->FUN_00878110(); ++index) {
                FUN_00401020(0, index, &enabled)->FUN_00866a90();
            }
        }
        reinterpret_cast<FUN_00878130_Class*>(FUN_00401020())->FUN_00878130();
    }
    control.FUN_0082f1f0();
}