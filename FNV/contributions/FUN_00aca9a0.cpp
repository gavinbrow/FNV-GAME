struct FUN_00ec3280_class {
    void __thiscall FUN_00ec3280();
};

struct FUN_00aca9a0_base {
    int* vtable;
};

struct FUN_00aca9a0_class {
    FUN_00aca9a0_base* m_p;

    void __thiscall FUN_00aca9a0();
};

void __thiscall FUN_00aca9a0_class::FUN_00aca9a0()
{
    unsigned int value1 =
        *reinterpret_cast<unsigned int*>(
            reinterpret_cast<unsigned char*>(m_p) +
            reinterpret_cast<unsigned int*>(m_p->vtable)[1] +
            0x28);

    if (value1 != 0) {
        unsigned int value2 =
            *reinterpret_cast<unsigned int*>(
                reinterpret_cast<unsigned char*>(m_p) +
                reinterpret_cast<unsigned int*>(m_p->vtable)[1] +
                0x28);

        reinterpret_cast<FUN_00ec3280_class*>(value2 + 4)->FUN_00ec3280();
    }
}