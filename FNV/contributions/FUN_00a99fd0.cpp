void* __cdecl FUN_00aa13e0(unsigned int bytes);

struct NiFogProperty : NiProperty
{
    unsigned short m_uFlags;
    float m_fDepth;
    NiColor m_kColor;

    static void* operator new(unsigned int, void* memory) { return memory; }

    __forceinline NiFogProperty()
    {
        m_uFlags = 0;
        m_fDepth = 1.0f;
        m_kColor = DAT_011f4998;
    }
};

NiFogProperty* __cdecl FUN_00a99fd0()
{
    void* memory = FUN_00aa13e0(sizeof(NiFogProperty));
    if (memory != 0)
        return new (memory) NiFogProperty;
    return 0;
}