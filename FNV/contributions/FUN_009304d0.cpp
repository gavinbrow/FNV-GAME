struct NiPoint3 {
    float x;
    float y;
    float z;
};

extern NiPoint3 DAT_011f426c;

struct FUN_009304d0_shell {
    float unk00;
    NiPoint3 unk04;
    NiPoint3 unk10;
    unsigned int unk1c;
    float unk20;
    bool unk24;

    void* __thiscall FUN_009304d0();
};

void* __thiscall FUN_009304d0_shell::FUN_009304d0() {
    unk00 = 0.0f;
    unk04 = DAT_011f426c;
    unk10 = DAT_011f426c;
    unk20 = 0.0f;
    unk24 = true;
    return this;
}