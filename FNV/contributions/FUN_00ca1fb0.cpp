struct FNVTaskElement {};
extern "C" void __fastcall FUN_00d1fa10(FNVTaskElement* element);
struct FNVTaskAllocator {
    virtual void fn00();
    virtual void fn04();
    virtual void fn08();
    virtual void fn0c();
    virtual void Free(void* memory, unsigned int byteCount);
};
struct FNVTaskMemoryRouter {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    FNVTaskAllocator* allocator;
};
extern "C" FNVTaskMemoryRouter* __cdecl FUN_00c85750();

struct FNVTaskDynamicBuffer {
    void* entries;
    int elementCount;
    unsigned int capacityAndFlags;
    void __thiscall FUN_00ca1fb0();
};

void FNVTaskDynamicBuffer::FUN_00ca1fb0()
{
    FNVTaskAllocator* allocator = FUN_00c85750()->allocator;
    char* entry = (char*)entries;
    if (elementCount > 0) {
        int remaining = elementCount;
        do {
            FUN_00d1fa10((FNVTaskElement*)entry);
            entry += 48;
        } while (--remaining);
    }
    elementCount = 0;
    if ((capacityAndFlags & 0x80000000u) == 0)
        allocator->Free(entries, (capacityAndFlags & 0x3fffffffu) * 48);
    capacityAndFlags = 0x80000000u;
    entries = 0;
}