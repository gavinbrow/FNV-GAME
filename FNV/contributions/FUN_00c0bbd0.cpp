struct FUN_00c0bbd0_Value {
    char unk00;
    char unk01;
    char unk02;
    char unk03;
    char unk04;
    char unk05;
    char unk06;
    char unk07;
    int unk08;
};

struct FUN_00c0bbd0_Entry {
    char unk00;
    char unk01;
    char unk02;
    char unk03;
    char unk04;
    char unk05;
    char unk06;
    char unk07;
    FUN_00c0bbd0_Value* unk08;
    FUN_00c0bbd0_Value* unk0c;
};

struct FUN_00c0bbd0_Arg {
    char unk00;
    char unk01;
    char unk02;
    char unk03;
    char unk04;
    char unk05;
    char unk06;
    char unk07;
    char unk08;
    char unk09;
    char unk0a;
    char unk0b;
    char unk0c;
    char unk0d;
    char unk0e;
    char unk0f;
    char unk10;
    char unk11;
    char unk12;
    char unk13;
    char unk14;
    char unk15;
    char unk16;
    char unk17;
    char unk18;
    char unk19;
    char unk1a;
    char unk1b;
    char unk1c;
    char unk1d;
    char unk1e;
    char unk1f;
    char unk20;
    char unk21;
    char unk22;
    char unk23;
    FUN_00c0bbd0_Entry* unk24;
};

extern int DAT_011f95e4;
extern int DAT_011f95e8;

void __stdcall FUN_00c0bbd0(FUN_00c0bbd0_Arg* arg)
{
    arg->unk24->unk08->unk08 = DAT_011f95e4;
    arg->unk24->unk0c->unk08 = DAT_011f95e8;
}