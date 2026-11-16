struct FUN_00501c10_Class {
    void FUN_00501c10(int a);
};
struct FUN_007df120_Class {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    void FUN_007df120(int a);
};
void FUN_007df120_Class::FUN_007df120(int a)
{
    ((FUN_00501c10_Class*)((char*)this + 0x20))->FUN_00501c10(a);
}