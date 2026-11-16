struct NiObjectData {
    void* m_p0;
    void* m_p4;
    void* m_p8;
    void* m_pc;
    unsigned int m_value;
};

struct FUN_00c879e0_Class {
    void* m_p0;
    void* m_p4;
    NiObjectData* m_p8;

    void __thiscall FUN_00c879e0(unsigned int* result);
};

void __thiscall FUN_00c879e0_Class::FUN_00c879e0(unsigned int* result)
{
    *result = (this != 0 && m_p8 != 0) ? m_p8->m_value : 0u;
}