struct FUN_00877db0_Embedded {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
};

struct FUN_00877db0_Class {
    int unk00;
    FUN_00877db0_Embedded unk04;

    FUN_00877db0_Class();
};

FUN_00877db0_Class::FUN_00877db0_Class()
    : unk00(0),
      unk04()
{
}