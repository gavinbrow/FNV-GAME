struct FUN_00d2bf30 {
    int* vtable;
    unsigned short unk04;
    unsigned short unk06;
    void* m8;
    unsigned char unk0c;
    FUN_00d2bf30(int mode);
};
extern void* __cdecl FUN_00ecdf44();
FUN_00d2bf30::FUN_00d2bf30(int mode) {
    unk06 = 1;
    vtable = &DAT_010ce6f4;
    unk0c = 0;
    char* base = static_cast<char*>(FUN_00ecdf44());
    if (mode == 2) {
        base += 0x40;
        m8 = base;
    } else {
        base += 0x20;
        m8 = base;
    }
}
