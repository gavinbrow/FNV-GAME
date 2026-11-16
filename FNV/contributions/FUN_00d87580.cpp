int __cdecl FUN_00cb0fa0(const char*, const char*);

static __forceinline int stringHash(const char* str)
{
    int hash = 0;
    if (*str) {
        const char* p = str;
        do {
            hash = 31 * hash + *p;
            ++p;
        } while (*p);
    }
    return hash & 0x7fffffff;
}

int FUN_00d87820_Class::FUN_00d87580(int key)
{
    const char* str = (const char*)key;
    hkCachedHashMap* table = (hkCachedHashMap*)this;
    int hash = stringHash(str);
    unsigned int slot = hash & table->m_hashMod;
    while (table->m_elem[slot] != 0xffffffffu) {
        if (table->m_elem[slot] == (unsigned int)hash &&
            FUN_00cb0fa0(str, (const char*)table->m_elem[table->m_hashMod + slot + 1]) == 0)
            return slot;
        slot = (slot + 1) & table->m_hashMod;
    }
    return table->m_hashMod + 1;
}