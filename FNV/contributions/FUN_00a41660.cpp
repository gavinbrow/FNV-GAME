struct MemoryManager_00a41660 { void __thiscall FUN_00aa4060(void*); };
extern MemoryManager_00a41660 DAT_011f6238;
extern char* DAT_0109b220;
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
struct Reference_00a41660 {
    virtual void Unused();
    virtual void Destroy();
    long count;
};
struct Entry_00a41660 {
    void* allocation;
    char* name;
    int unused;
    Reference_00a41660* reference;
};
struct Owner_00a41660 {
    Entry_00a41660 object;
    void __thiscall FUN_00a41610();
    void* __thiscall FUN_00a41660(unsigned char flags);
};
void* __thiscall Owner_00a41660::FUN_00a41660(unsigned char flags) {
    if (flags & 2) {
        int count = *(int*)((char*)this - 4);
        Entry_00a41660* it = &object + count;
        while (--count >= 0) {
            --it;
            DAT_011f6238.FUN_00aa4060(it->allocation);
            Reference_00a41660* ref = it->reference;
            if (ref) {
                if (InterlockedDecrement(&ref->count) == 0)
                    ref->Destroy();
            }
            char* value = it->name;
            if (value != DAT_0109b220)
                InterlockedDecrement((long volatile*)(value - 8));
        }
        void* header = (char*)this - 4;
        if (flags & 1) DAT_011f6238.FUN_00aa4060(header);
        return header;
    }
    FUN_00a41610();
    if (flags & 1) DAT_011f6238.FUN_00aa4060(this);
    return this;
}