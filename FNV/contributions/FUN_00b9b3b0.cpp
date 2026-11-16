struct FUN_00b9abc0_class {
    void __thiscall FUN_00b9abc0(unsigned int arg1, unsigned int arg2);
};

struct FUN_00b9b3b0_class {
    void* m_000;
    void* m_004;
    void* m_008;
    void* m_00c;
    void* m_010;
    void* m_014;
    void* m_018;
    void* m_01c;
    void* m_020;
    void* m_024;
    void* m_028;
    void* m_02c;
    void* m_030;
    void* m_034;
    void* m_038;
    FUN_00b9abc0_class* m_003c;

    void __thiscall FUN_00b9b3b0(
        unsigned int arg1,
        unsigned int arg2,
        unsigned int arg3);
};

void __thiscall FUN_00b9b3b0_class::FUN_00b9b3b0(
    unsigned int arg1,
    unsigned int arg2,
    unsigned int arg3)
{
    reinterpret_cast<FUN_00b9abc0_class**>(&m_003c)[arg2]->
        FUN_00b9abc0(arg1, arg3);
}