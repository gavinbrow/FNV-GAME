
extern "C" void __stdcall FUN_00ec5fce(void*, unsigned int, unsigned int, const void*);
extern "C" void FUN_004381b0();
struct FUN_00a5d3d0 {
    virtual void dummy();
    unsigned int m_uiRefCount;
    unsigned int m_uiFlags;
    ~FUN_00a5d3d0();
};
struct FUN_00cc1520 : FUN_00a5d3d0 {
    virtual void dummy();
    char* m_pName;
    unsigned int m_uiCount;
    void** m_pArray;
    ~FUN_00cc1520();
};
FUN_00cc1520::~FUN_00cc1520() {
    {
        TlsGuard_t guard(g_tlsBlock.m_2b4);
        if (m_pName) {
            char* header = m_pName - 4;
            FUN_00ec5fce(m_pName, 4, *reinterpret_cast<unsigned int*>(header), &FUN_004381b0);
            g_memoryManager.Deallocate(header);
        }
        if (m_pArray) {
            for (unsigned int i = 0; i < m_uiCount; ++i) {
                void* item = m_pArray[i];
                if (item)
                    g_memoryManager.Deallocate(item);
            }
            void** releaseArray = m_pArray;
            g_memoryManager.Deallocate(releaseArray);
        }
    }
}
