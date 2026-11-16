struct FUN_00d76990_State {
    int unk00;
    float unk04;
    void FUN_00d7d2a0();
};

struct FUN_00d76990_Class {
    int unk00;
    int unk04;
    FUN_00d76990_State* unk08;
    void FUN_00d76990(float value, bool clearFlag);
};

void FUN_00d76990_Class::FUN_00d76990(float value, bool clearFlag) {
    if (clearFlag)
        *(reinterpret_cast<unsigned char*>(unk08) + 0x1b5) = 0;
    unk08->unk04 = value;
    unk08->FUN_00d7d2a0();
}
