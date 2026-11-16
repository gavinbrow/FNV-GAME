
void* __cdecl FUN_00aa1070(unsigned int bytes);

struct FUN_00a7b690 {
    virtual void baseVirtual();
    FUN_00a7b690();
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
};

struct FNV_A90A50_ArrayBase {
    virtual void arrayVirtual();
    void* data;
    unsigned short length;
    unsigned short allocated;
    unsigned short size;
    unsigned short capacity;
    FNV_A90A50_ArrayBase() { length = 4; capacity = 4; allocated = 0; size = 0; data = FUN_00aa1070(16); }
};

struct FNV_A90A50_Array : FNV_A90A50_ArrayBase {
    virtual void arrayVirtual();
    FNV_A90A50_Array() {}
};

struct FUN_00a90a50 : FUN_00a7b690 {
    unsigned char unk58;
    unsigned char unk59;
    unsigned short unk5a;
    unsigned int unk5c;
    FNV_A90A50_Array member60;
    virtual void baseVirtual();
    FUN_00a90a50();
};

FUN_00a90a50::FUN_00a90a50() : unk58(0), unk59(0), unk5c(0) {}
