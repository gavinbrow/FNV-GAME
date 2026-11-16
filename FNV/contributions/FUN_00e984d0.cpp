struct FUN_00e984d0_Struct {
    int unk00;
    int unk04;
    int unk08;
    int (__cdecl *unk0c)(FUN_00e984d0_Struct*, int, int, int*, int);
};

void __cdecl FUN_00e984d0(FUN_00e984d0_Struct* a1, int a2, int a3)
{
    int local = 1;
    a1->unk04 += a1->unk0c(a1, a2, a3, &local, 1);
}
