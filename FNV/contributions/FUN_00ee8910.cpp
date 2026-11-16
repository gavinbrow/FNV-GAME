struct FUN_00a7b2e0_shell { void FUN_00a7b2e0(); };
struct FUN_00a5b950_shell { void FUN_00a5b950(int); };
void* __cdecl FUN_00aa1070(int);

struct FUN_00ee8910_obj
{
    void* vfptr;
    int unk04;
    int unk08;
    int m_countA;
    int unk10;
    int m_countB;
    int m_zero18;
    int unk1c;
    int m_zero20;
    void* m_arrA;
    int unk28;
    void* m_arrB;
    FUN_00ee8910_obj* FUN_00ee8910(int, int, int);
};

FUN_00ee8910_obj* FUN_00ee8910_obj::FUN_00ee8910(int a, int b, int c)
{
    ((FUN_00a7b2e0_shell*)this)->FUN_00a7b2e0();
    vfptr = &DAT_0110129c;
    ((FUN_00a5b950_shell*)this)->FUN_00a5b950(a);
    m_countA = b;
    m_zero18 = 0;
    if (b != 0) {
        m_arrA = FUN_00aa1070(b * 8);
    } else {
        m_arrA = 0;
    }
    m_countB = c;
    m_zero20 = 0;
    if (c != 0) {
        m_arrB = FUN_00aa1070(c * 8);
    } else {
        m_arrB = 0;
    }
    return this;
}
