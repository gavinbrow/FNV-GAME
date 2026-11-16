struct Scratch16 {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    void FUN_00d60830(unsigned int a, unsigned int b);
    unsigned char* FUN_00d607e0(unsigned int* out);
    void FUN_00d60590();
};
struct FUN_00e04920_cls {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned int unk10;
    unsigned char m_flag14;
    unsigned int FUN_00e036b0(unsigned int a, unsigned int b, Scratch16* scratch, unsigned int c);
    unsigned int FUN_00e03ea0(unsigned int a, unsigned int b, Scratch16* scratch,
                                unsigned int c, unsigned int d, unsigned int e, unsigned int f);
    int FUN_00e04920(unsigned int a1, unsigned int a2, unsigned int a3,
                     unsigned int a4, unsigned int a5);
};

int FUN_00e04920_cls::FUN_00e04920(unsigned int a1, unsigned int a2,
                                   unsigned int a3, unsigned int a4, unsigned int a5)
{
    Scratch16 scratch;
    VObj* original = reinterpret_cast<VObj*>(a3);
    scratch.FUN_00d60830(a3, static_cast<unsigned int>(m_flag14));
    unsigned int result = FUN_00e036b0(a1, a2, &scratch, a4);
    FUN_00e03360(original, 16);
    FUN_00e03ea0(a1, a2, &scratch, a4, result, a5, 0);
    FUN_00e03360(original, 16);
    unsigned char* status = scratch.FUN_00d607e0(&a1);
    unsigned int success = (*status == 0);
    scratch.FUN_00d60590();
    return success;
}