struct FUN_00cf4ce0_class {
    int unk00;
    int unk04;
    void* unk08;
    int unk0c;
    int unk10;
    int unk14;
    void* unk18;
    void FUN_00cf4ce0(void* newAction);
};

struct FUN_00c90510_class {
    void FUN_00c90510();
};

struct FUN_00c905b0_class {
    void FUN_00c905b0();
};

struct FUN_00c976a0_class {
    void FUN_00c976a0(void*, void*);
};

struct FUN_00c92bd0_class {
    void FUN_00c92bd0(void*, void*);
};

void FUN_00cf4ce0_class::FUN_00cf4ce0(void* newAction)
{
    ((FUN_00c90510_class*)newAction)->FUN_00c90510();
    if (unk18) {
        if (unk08) {
            ((FUN_00c976a0_class*)unk08)->FUN_00c976a0(this, unk18);
        }
        ((FUN_00c905b0_class*)unk18)->FUN_00c905b0();
        unk18 = 0;
    }
    unk18 = newAction;
    if (unk08) {
        ((FUN_00c92bd0_class*)unk08)->FUN_00c92bd0(this, newAction);
    }
}