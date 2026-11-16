struct FUN_00e03120 {
    virtual ~FUN_00e03120();
    short unk04;
    short unk06;
    int unk08;
    int unk0C;
    int unk10;
    bool unk14;

    FUN_00e03120(const int* param1, const int* param2, int param3);
};

FUN_00e03120::FUN_00e03120(const int* param1, const int* param2, int param3)
    : unk06(1)
{
    unk08 = *param1;
    unk0C = *param2;
    unk10 = param3;
    unk14 = ((char*)&unk08)[1] != ((char*)&unk0C)[1];
}
