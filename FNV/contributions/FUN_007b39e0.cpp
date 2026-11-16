extern "C" void* DAT_011da634;
extern "C" const char str_01075b10[];
extern "C" const char str_01075b5c[];

struct FUN_0048f200 {
    int unk00;
    int unk04;
    int unk08;
    FUN_0048f200();
    ~FUN_0048f200();
};
struct Tile_Set_Helper {
    void Set(int kind, int value);
};
struct PropertyObject : Tile_Set_Helper {
    void FUN_00a01350(int kind, int value, bool enabled);
    void FUN_00a04640(bool enabled);
};
struct InterfaceRoot {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c;
    int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68; int unk6c;
    int unk70; int unk74; void* unk78;
    PropertyObject* FUN_00a1ddb0(void* parent, const char* name, int mode);
};
int __cdecl FUN_00a00940(const char* name, int index);
struct FUN_007b39e0 : FUN_0048f200 {
    int unk0c;
    int unk10;
    PropertyObject* unk14;
    float unk18;
    int unk1c;
    int unk20;
    FUN_007b39e0(int low, int high);
};
FUN_007b39e0::FUN_007b39e0(int low, int high) {
    unk10 = 20;
    unk0c = 20;
    unk18 = 0.0f;
    unk1c = 0;
    unk14 = ((InterfaceRoot*)DAT_011da634)->FUN_00a1ddb0(((InterfaceRoot*)DAT_011da634)->unk78, str_01075b10, 0);
    unk14->Set(0x1004, low);
    unk14->FUN_00a01350(0xfc4, high, true);
    unk14->Set(0xfaf, 0);
    unk14->Set(FUN_00a00940(str_01075b5c, -1), 1);
    unk14->FUN_00a04640(false);
    unk20 = 0;
}