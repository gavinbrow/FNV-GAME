extern int DAT_0106ff84;
void* __cdecl FUN_00403d30(void*, int, unsigned int);
struct Base0071 {
    Base0071();
    ~Base0071();
    void* vtable;
    unsigned int unk04, unk08, unk0c, unk10, unk14, unk18, unk1c, unk20, unk24;
};
struct FUN_0071f240: Base0071 {
    unsigned int unk28, unk2c, unk30, unk34, unk38, unk3c, unk40, unk44;
    unsigned int unk48, unk4c, unk50;
    FUN_0071f240();
};
FUN_0071f240::FUN_0071f240() {
    vtable = &DAT_0106ff84;
    FUN_00403d30(&unk28, 0, 0x20);
    unk4c = 0;
    unk48 = 0;
    unk50 = 0;
}
