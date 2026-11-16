extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long* value);
extern "C" __declspec(dllimport) void __stdcall fnv_EnterCriticalSection(void* cs);
extern "C" __declspec(dllimport) void __stdcall fnv_LeaveCriticalSection(void* cs);
extern unsigned char DAT_011f4380;
void* __cdecl FUN_00aa1070(unsigned int size);
void __cdecl NiFreeAlias(void*);
extern "C" void* __cdecl memmove(void* dst, const void* src, unsigned int n);
struct ExtraName {
    const char* handle;
    operator const char*() const { return handle; }
};
struct NiTexture {
    void* m_pVTable;
    long m_refCount;
    const ExtraName& FUN_00a62660();
};
struct NiObjectNET {
    int m_00;
    int m_04;
    int m_08;
    int m_0c;
    NiTexture** m_data;
    unsigned short m_count;
    unsigned short m_capacity;
    void DeleteExtraData(unsigned short idx);
};
struct Holder : NiObjectNET {
    bool FUN_00a5ba40(NiTexture* p);
};
bool Holder::FUN_00a5ba40(NiTexture* p)
{
    if (!p)
        return false;
    InterlockedIncrement(&p->m_refCount);
    fnv_EnterCriticalSection(&DAT_011f4380);
    if (m_capacity < 1) {
        m_count = m_capacity = 1;
        m_data = (NiTexture**)FUN_00aa1070(4);
        m_data[0] = p;
        fnv_LeaveCriticalSection(&DAT_011f4380);
        return true;
    }
    if (m_count == m_capacity) {
        m_capacity = (unsigned short)(m_capacity * 2 + 1);
        NiTexture** newData = (NiTexture**)FUN_00aa1070(m_capacity * 4);
        memmove(newData, m_data, m_count * 4);
        NiFreeAlias(m_data);
        m_data = newData;
    }
    m_data[m_count] = p;
    ++m_count;
    unsigned short j;
    for (j = m_count; j < m_capacity; ++j)
        m_data[j] = 0;
    for (j = (unsigned short)(m_count - 1); j > 0; --j) {
        NiTexture**& data = m_data;
        int diff = data[j - 1]->FUN_00a62660() - data[j]->FUN_00a62660();
        if (diff == 0) {
            DeleteExtraData(j);
            fnv_LeaveCriticalSection(&DAT_011f4380);
            return false;
        }
        if (diff <= 0)
            break;
        NiTexture* tmp = m_data[j - 1];
        m_data[j - 1] = m_data[j];
        m_data[j] = tmp;
    }
    fnv_LeaveCriticalSection(&DAT_011f4380);
    return true;
}
