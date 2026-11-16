struct FUN_0096ad30_This {
    int unk00;
    int unk04;
    unsigned short m_capacity;
    unsigned short m_count;
    unsigned short m_unk0C;
    unsigned short m_growth;
    void FUN_0096ad30(unsigned int);
    void FUN_0096ae90(unsigned int, void*);
};
void __stdcall FUN_00a97420(void*);
void* __cdecl FUN_00a7d330(void*);
void __stdcall FUN_00a98de0(FUN_0096ad30_This* p) {
    FUN_00a97420(p);
    void* item = FUN_00a7d330(*(void**)&g_011f5f0c);
    unsigned int count = p->m_count;
    unsigned int capacity = p->m_capacity;
    if (count >= capacity)
        p->FUN_0096ad30((unsigned int)p->m_growth + count);
    p->FUN_0096ae90(count, &item);
}