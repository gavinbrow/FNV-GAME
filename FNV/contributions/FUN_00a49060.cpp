struct PosKeyData {
    void* vtable;
    int refs;
    unsigned int m_uiNumKeys;
    unsigned char* m_pkKeys;
    int m_eType;
    unsigned char m_ucKeySize;
    bool FUN_00a5d470(const PosKeyData* other);
    bool FUN_00a49060(const PosKeyData* other);
};
typedef bool (__cdecl* KeyEqual)(const void*, const void*);
extern KeyEqual DAT_011f3af8[];

bool PosKeyData::FUN_00a49060(const PosKeyData* other)
{
    if (!FUN_00a5d470(other))
        return false;

    if (m_uiNumKeys != other->m_uiNumKeys ||
        m_eType != other->m_eType ||
        m_ucKeySize != other->m_ucKeySize)
        return false;

    KeyEqual equalKeys = DAT_011f3af8[m_eType];
    for (unsigned int i = 0; i < m_uiNumKeys; ++i) {
        unsigned int offset = i * m_ucKeySize;
        const unsigned char* otherKey = other->m_pkKeys + offset;
        const unsigned char* currentKey = m_pkKeys + offset;
        if (!equalKeys(currentKey, otherKey))
            return false;
    }
    return true;
}