extern "C" void* g_011f4074;
extern int DAT_01096f1c;
void* __cdecl FUN_00a7d330(void*);

struct ArraySource {
    virtual ~ArraySource();
    void* m_pBase;
    unsigned short m_usMaxSize;
    unsigned short m_usSize;
    unsigned short m_usESize;
    unsigned short m_usGrowBy;
    void FUN_0096ad30(unsigned int newSize);
    void FUN_0096ae90(unsigned int index, void** result);
};
struct AssignmentMember {
    void* FUN_00a69720(const int*);
};
struct FUN_00a564d0_shell {
    void FUN_00a38080(ArraySource* source);
    void FUN_00a564d0(ArraySource* source);
};
void FUN_00a564d0_shell::FUN_00a564d0(ArraySource* source) {
    FUN_00a38080(source);
    void* result = FUN_00a7d330(g_011f4074);
    unsigned int index = source->m_usSize;
    if (index >= source->m_usMaxSize)
        source->FUN_0096ad30(index + source->m_usGrowBy);
    source->FUN_0096ae90(index, &result);
    result = reinterpret_cast<AssignmentMember*>(reinterpret_cast<char*>(this) + 0x30)->FUN_00a69720(&DAT_01096f1c);
    index = source->m_usSize;
    if (index >= source->m_usMaxSize)
        source->FUN_0096ad30(index + source->m_usGrowBy);
    source->FUN_0096ae90(index, &result);
}