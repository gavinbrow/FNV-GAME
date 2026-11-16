extern __declspec(thread) unsigned int g_ThreadMemoryContext;
struct MemoryContextGuard {
    unsigned int previous;
    __forceinline MemoryContextGuard() : previous(g_ThreadMemoryContext) { g_ThreadMemoryContext = 16; }
    __forceinline ~MemoryContextGuard() { g_ThreadMemoryContext = previous; }
};
struct AllocationManager { void* FUN_00aa3e40(unsigned int size); };
extern AllocationManager DAT_011f6238;
struct FUN_00c8f510 { unsigned int value; FUN_00c8f510(); ~FUN_00c8f510(); };
__forceinline void* __cdecl operator new(unsigned int size, AllocationManager& allocator) {
    unsigned char* storage = static_cast<unsigned char*>(allocator.FUN_00aa3e40(0xf0));
    unsigned char adjustment = static_cast<unsigned char>(16 - (reinterpret_cast<unsigned int>(storage) & 15));
    storage += adjustment;
    storage[-1] = adjustment;
    return storage;
}
void __cdecl operator delete(void* memory, AllocationManager& allocator);
struct FUN_00c8f5a0_Class {
    void* virtualFunctions;
    unsigned int referenceCount;
    void* havokObject;
    FUN_00c8f510* rigidBodyInfo;
    void FUN_00c8cfd0(FUN_00c8f510* info);
    FUN_00c8f510* FUN_00c8f5a0(unsigned char* wasCreated);
};
FUN_00c8f510* FUN_00c8f5a0_Class::FUN_00c8f5a0(unsigned char* wasCreated) {
    MemoryContextGuard context;
    const bool needsCreation = rigidBodyInfo == 0;
    *wasCreated = needsCreation;
    if (needsCreation) {
        rigidBodyInfo = new (DAT_011f6238) FUN_00c8f510();
        if (havokObject)
            FUN_00c8cfd0(rigidBodyInfo);
    }
    return rigidBodyInfo;
}