extern "C" void* __cdecl FUN_00aa13e0(unsigned int);

struct FUN_00cbc550 {
    int unk00, unk04, unk08, unk0c;
    int unk10, unk14, unk18, unk1c;
    int unk20, unk24, unk28, unk2c;
    int unk30, unk34, unk38, unk3c;
    static void* __cdecl operator new(unsigned int size) {
        return FUN_00aa13e0(size);
    }
    FUN_00cbc550();
};
FUN_00cbc550* __cdecl FUN_00cbc5e0() {
    return new FUN_00cbc550;
}