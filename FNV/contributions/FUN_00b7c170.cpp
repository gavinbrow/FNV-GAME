struct FUN_00b7c170_Entry {
    int unk00;
    int unk04;
    int unk08;
};

struct FUN_00b7c170_Container {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    FUN_00b7c170_Entry** unk24;
};

extern int DAT_0126f74c;
extern int DAT_011f95e8;

void __stdcall FUN_00b7c170(int index)
{
    FUN_00b7c170_Container* container =
        reinterpret_cast<FUN_00b7c170_Container*>(DAT_0126f74c);
    container->unk24[index]->unk08 = DAT_011f95e8;
}