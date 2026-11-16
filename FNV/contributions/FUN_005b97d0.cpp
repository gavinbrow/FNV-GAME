struct FUN_00664840_Class
{
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    char unk18;
    bool unk19;
};

FUN_00664840_Class* __cdecl FUN_00664840(int a1);

void __cdecl FUN_005b97d0(bool a1)
{
    FUN_00664840(1)->unk19 = a1;
}
