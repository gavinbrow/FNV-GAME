extern int DAT_011f36f4;
extern int DAT_011f36f8;
void __cdecl _Deallocate(void* p);

struct FUN_004d9070 {
    ~FUN_004d9070();
};

struct FUN_004d62a0_Class {
    int m_00;
    int m_04;
    int m_08;
    int m_0C;
    int m_10;
    int m_14;
    FUN_004d9070 m_18;
    int m_1C;
    int m_20;
    int m_24;
    int m_28;
    void* m_p2C;

    void __thiscall FUN_004d7490();
    void __thiscall FUN_004d7470();
    void __thiscall FUN_004d7440();
    ~FUN_004d62a0_Class();
};

FUN_004d62a0_Class::~FUN_004d62a0_Class()
{
    void* p = m_p2C;
    _Deallocate(p);
    FUN_004d7490();
    FUN_004d7470();
    FUN_004d7440();
    DAT_011f36f8 = 0;
    DAT_011f36f4 = DAT_011f36f8;
}
