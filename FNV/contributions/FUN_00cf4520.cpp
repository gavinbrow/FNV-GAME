extern __declspec(thread) int g_iCC4740AllocTag;
struct CF4520AllocTagScope {
    int saved;
    CF4520AllocTagScope(int tag) {
        saved=g_iCC4740AllocTag;
        g_iCC4740AllocTag=tag;
    }
    ~CF4520AllocTagScope() { g_iCC4740AllocTag=saved; }
};
extern const char* DAT_01268738;
char* __cdecl FUN_00a7d330(const char* name);
struct CF4520Array {
    void* vtable;
    char** m_pBase;
    unsigned short m_usMaxSize;
    unsigned short m_usSize;
    unsigned short m_usESize;
    unsigned short m_usGrowBy;
    void FUN_0096ad30(unsigned int size);
    void FUN_0096ae90(unsigned int index, char* const& item);
    unsigned int Add(char* const& item) {
        unsigned int index=m_usSize;
        if(index>=m_usMaxSize) FUN_0096ad30(index+m_usGrowBy);
        FUN_0096ae90(index,item);
        return index;
    }
};
void __stdcall FUN_00cf4520(CF4520Array* array) {
    CF4520AllocTagScope tag(16);
    char* element=FUN_00a7d330(DAT_01268738);
    array->Add(element);
}