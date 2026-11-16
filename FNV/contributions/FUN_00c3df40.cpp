struct FUN_00c3df40_Param1 {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    __int64 unk10;
};

struct FUN_00c3df40_Class {
    void __thiscall FUN_00c3e690(FUN_00c3df40_Param1* a1, __int64 a2);
    void __thiscall FUN_00c3df40(FUN_00c3df40_Param1* a1, int a2);
};

void __thiscall FUN_00c3df40_Class::FUN_00c3df40(FUN_00c3df40_Param1* a1, int a2)
{
    __int64 val = a1->unk10;
    val = (val & 0xFFFFFFFFFF00FFFFULL) + ((__int64)a2 << 16);
    this->FUN_00c3e690(a1, val);
}
