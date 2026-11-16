struct Data {
    int unk00; int unk04; int unk08; int unk0C;
    int unk10; int unk14; int unk18; int unk1C;
    int unk20; int unk24; int unk28; int unk2C;
    int unk30; int unk34; int unk38;
    int* unk3C;
};
struct Owner {
    int unk00;
    int unk04;
    Data* unk08;
    int* FUN_00d75140();
};
int* Owner::FUN_00d75140() { return unk08->unk3C; }
