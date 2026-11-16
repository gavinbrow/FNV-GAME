extern void* DAT_0106ced8;
void* __cdecl _NiMalloc(unsigned int size);
void* __cdecl memset(void* destination, int value, unsigned int size);

struct FUN_006e0f20_Class {
    void** m_vtable;
    unsigned int m_hashSize;
    void* m_table;
    unsigned int m_entryCount;

    FUN_006e0f20_Class* __thiscall FUN_006e0f20(unsigned int hashSize);
};

FUN_006e0f20_Class* FUN_006e0f20_Class::FUN_006e0f20(unsigned int hashSize)
{
    m_vtable = &DAT_0106ced8;
    m_hashSize = hashSize;
    m_entryCount = 0;

    unsigned int allocationSize = m_hashSize * sizeof(void*);
    m_table = _NiMalloc(allocationSize);
    memset(m_table, 0, m_hashSize * sizeof(void*));
    return this;
}