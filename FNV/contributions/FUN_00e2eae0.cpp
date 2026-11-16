struct FUN_00e2eae0_Result {
    void __thiscall FUN_00e2eae0(int* param);
};

struct FUN_00e2eae0_class {
    virtual void* vf00();
    virtual void* vf04();
    virtual void* vf08();
    virtual void* vf0c();
    virtual void* vf10(void* arg);
    virtual void* vf14();
    virtual void* vf18();
    virtual void* vf1c();
    virtual void* vf20();
    virtual FUN_00e2eae0_Result* vf24();
    void __thiscall FUN_00e2eae0(int* param);
};

struct FUN_00cbbd80_Local {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    int unk7c;
    int unk80;
    int unk84;
    int unk88;
    void __thiscall FUN_00cbbd80();
};

struct FUN_00d61df0_Obj {
    void __thiscall FUN_00d61df0(void* value);
};

struct FUN_00c85750_Object {
    virtual void* vf00();
    virtual void* vf04();
    virtual void* vf08();
    virtual void* vf0c();
    virtual void vf10(void* arg1, int arg2);
};

struct FUN_00c85750_Owner {
    void* unk00;
    void* unk04;
    void* unk08;
    FUN_00c85750_Object* unk0c;
};

extern int DAT_01063cbc;

FUN_00c85750_Owner* __cdecl FUN_00c85750();

void __thiscall FUN_00e2eae0_class::FUN_00e2eae0(int* param) {
    FUN_00e2eae0_Result* result = vf24();
    if (result != 0) {
        result->FUN_00e2eae0(param);
    }

    FUN_00cbbd80_Local local;
    local.FUN_00cbbd80();

    void* value = vf10(&local);

    FUN_00d61df0_Obj* target = (FUN_00d61df0_Obj*)param;
    target->FUN_00d61df0(&DAT_01063cbc);
    target->FUN_00d61df0(value);

    FUN_00c85750_Object* allocator = FUN_00c85750()->unk0c;
    int handle = local.unk08;
    local.unk04 = 0;
    if ((handle & 0x80000000u) == 0) {
        allocator->vf10((void*)local.unk00, handle & 0x3fffffff);
    }
}
