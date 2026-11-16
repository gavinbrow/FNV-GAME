struct FUN_00e012f0_class;

struct NotifyTarget {
    virtual void Slot00();
    virtual void Slot04();
    virtual void Notify(void*, unsigned short);
};

struct NotifyRoot {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    NotifyTarget* target;
};

struct FUN_00e012f0_class {
    int unk00;
    unsigned short m4;
    unsigned short unk06;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    FUN_00e012f0_class* FUN_00e012f0(unsigned int flags);
};

extern "C" void __cdecl FUN_00e49f40();
typedef void (__thiscall *InitialiseFunction)(FUN_00e012f0_class*);
extern "C" NotifyRoot* __cdecl FUN_00c85750();

FUN_00e012f0_class* FUN_00e012f0_class::FUN_00e012f0(unsigned int flags) {
    reinterpret_cast<InitialiseFunction>(FUN_00e49f40)(this);
    if (flags & 1) {
        NotifyRoot* root = FUN_00c85750();
        root->target->Notify(this, m4);
    }
    return this;
}
