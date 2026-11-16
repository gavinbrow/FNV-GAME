struct FUN_00eb5f10_Tail {
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18;
    int unk1c; int unk20; int unk24; int unk28; int unk2c; int unk30;
    void FUN_00a86bf0();
};
struct FUN_00eb5f10_Small { FUN_00eb5f10_Small* FUN_00eb6b90(void*, int, int, int, int); };
struct FUN_00eb5f10_Large { void* FUN_00eba1b0(void*, unsigned short, int, int, int, int); };
struct FUN_00eb5f10_Manager { void* FUN_00aa3e40(unsigned int); };
extern int _DAT_011f426c;
extern int _DAT_011f4270;
extern int _DAT_011f4274;
extern char UNK_010f1b44;
struct FUN_00eb5f10_Class {
    void** vtable; float unk04; void* unk08; unsigned char unk0c; int unk10; int unk14; int unk18;
    FUN_00eb5f10_Tail unk1c; int unk50;
    FUN_00eb5f10_Class* FUN_00eb5f10(unsigned short kind, int arg2, int arg3, int arg4, int arg5);
};
FUN_00eb5f10_Class* FUN_00eb5f10_Class::FUN_00eb5f10(unsigned short kind, int arg2, int arg3, int arg4, int arg5) {
    vtable = (void**)&UNK_010f1b44;
    FUN_00eb5f10_Manager* manager = (FUN_00eb5f10_Manager*)&_g_memoryManager;
    void* object;
    if (kind > 1) {
        object = manager->FUN_00aa3e40(0x8c);
        object = object ? ((FUN_00eb5f10_Large*)object)->FUN_00eba1b0(this, kind, arg2, arg3, arg4, arg5) : 0;
    } else {
        object = manager->FUN_00aa3e40(0x98);
        object = object ? ((FUN_00eb5f10_Small*)object)->FUN_00eb6b90(this, arg2, arg3, arg4, 0) : 0;
    }
    unk08 = object;
    unk04 = 0.0f;
    unk10 = _DAT_011f426c;
    unk14 = _DAT_011f4270;
    unk18 = _DAT_011f4274;
    unk1c.FUN_00a86bf0();
    unk0c = 0;
    unk50 = 0;
    return this;
}