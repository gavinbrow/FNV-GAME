struct HeapAllocator {
    virtual void* GetStats();
    virtual void* Allocate(unsigned int bytes);
};
struct MemorySystem {
    void* unknown00;
    void* unknown04;
    void* unknown08;
    void* unknown0c;
    HeapAllocator* heap;
};
struct AllocationRecord {
    unsigned int flags;
    unsigned short size;
    unsigned short reserved;
    AllocationRecord* FUN_00d62ef0(void* data, unsigned int enabled);
};
void* __cdecl FUN_00d62f60(void* data) {
    MemorySystem* memory = static_cast<MemorySystem*>(FUN_00c85750());
    AllocationRecord* record = static_cast<AllocationRecord*>(memory->heap->Allocate(44));
    record->size = 44;
    AllocationRecord* result = record->FUN_00d62ef0(data, 1);
    return result ? reinterpret_cast<char*>(result) + 8 : 0;
}