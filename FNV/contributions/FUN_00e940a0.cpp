struct FUN_00e940a0_Global {
    int unk_00;
    int unk_04;
    int unk_08;
    int unk_0c;
    int unk_10;
    int unk_14;
    int unk_18;
    int unk_1c;
    int unk_20;
    int unk_24;
    int unk_28;
    int unk_2c;
    int unk_30;
    int unk_34;
    int unk_38;
    int unk_3c;
    int unk_40;
    int unk_44;
    void* unk_48;
};

extern FUN_00e940a0_Global* DAT_011f4a64;

struct FUN_00e940a0_Class {
    void* m_00;
    void __thiscall FUN_00e940a0();
};

extern "C" void __cdecl operator delete(void* p, unsigned int size);

void __thiscall FUN_00e940a0_Class::FUN_00e940a0() {
    if (DAT_011f4a64 != 0) {
        void* p = DAT_011f4a64->unk_48;
        if (p != 0) {
            DAT_011f4a64->unk_48 = 0;
            if (p == m_00) {
                m_00 = 0;
            }
            operator delete(p, 0x48);
        }
    }
}
