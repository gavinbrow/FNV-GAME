extern char str_010ce9a4[];
extern char str_010ce9ac[];

extern "C" void* __cdecl FUN_00d06f80(void* apBuffer, int aiCount);

struct S_00d2f8f0_Elem {
    int unk00;
    int unk04;
    int unk08;
};

struct S_00d2f8f0_Array {
    S_00d2f8f0_Elem* m_pEntries;
    int m_iCount;

    S_00d2f8f0_Elem* begin() const { return m_pEntries; }
    S_00d2f8f0_Elem* end() const { return m_pEntries + m_iCount; }
};

struct S_00d2f8f0_ArgVtbl {
    void* unk00;
    void* unk04;
    void* unk08;
    void (__thiscall *unk0c)(void*, char*, int, int);
    void* unk10;
    void (__thiscall *unk14)(void*, int, char*, void*, int, void*);
};

struct S_00d2f8f0_Arg {
    S_00d2f8f0_ArgVtbl* m_pVtbl;
    int unk04;
    int unk08;
    int unk0c;
    char m_bFlag10;
};

struct S_00d2f8f0 {
    int unk00;
    int unk04;
    int unk08;
    S_00d2f8f0_Array m_arr;
    int m_iFlags;

    void FUN_00d2f8f0(S_00d2f8f0_Arg* apStream, int aiUnused);
};

void S_00d2f8f0::FUN_00d2f8f0(S_00d2f8f0_Arg* apStream, int aiUnused)
{
    if ((m_iFlags & 0x80000000u) == 0 || apStream->m_bFlag10 != 0) {
        void* pBuffer = m_arr.m_pEntries;
        unsigned int uiAlloc = (unsigned int)m_iFlags & 0x3fffffffu;
        uiAlloc *= sizeof(S_00d2f8f0_Elem);

        void* pResult = FUN_00d06f80(pBuffer, (int)uiAlloc);

        unsigned int uiArray = (unsigned int)m_arr.m_iCount;
        uiArray *= sizeof(S_00d2f8f0_Elem);

        apStream->m_pVtbl->unk14(apStream, 3, str_010ce9ac, m_arr.m_pEntries,
                                  (int)uiArray, pResult);
    }

    S_00d2f8f0_Elem* p = m_arr.begin();
    S_00d2f8f0_Elem* pEnd = m_arr.end();
    while (p != pEnd) {
        if (p->unk08 != 0) {
            apStream->m_pVtbl->unk0c(apStream, str_010ce9a4, p->unk08, 0);
        }
        ++p;
    }
}