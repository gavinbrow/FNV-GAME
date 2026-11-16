extern "C" __declspec(dllimport) unsigned long __stdcall GetCurrentThreadId();
void FUN_00cbb990();
struct ArenaReleaseAllocator : ArenaAllocator {
    virtual void Deallocate(void* p, unsigned int bytes);
};
struct ArenaRegistryRelease {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0C();
    virtual void Release(TemporaryArena* arena, ArenaRegistrationFlag flag);
};
struct ArenaManagedOwner {
    TemporaryArena* arena;
    void* buffer;
    unsigned long threadId;
};
void FUN_00c80240(ArenaManagedOwner* owner) {
    if (owner->arena) {
        ArenaEnterCriticalSection(&DAT_01267e48);
        TemporaryArena* arena = owner->arena;
        ArenaReleaseAllocator* allocator = static_cast<ArenaReleaseAllocator*>(arena->allocator);
        allocator->Deallocate(owner->buffer, 0x5000);
        owner->buffer = 0;
        if (GetCurrentThreadId() == owner->threadId)
            FUN_00cbb990();
        ArenaRegistryRelease* registry=(ArenaRegistryRelease*)FUN_00cbbfc0();
        registry->Release(arena,ArenaRegistrationFlag());
        arena->cursor = 0;
        arena->start = 0;
        arena->end = 0;
        owner->arena = 0;
        ArenaLeaveCriticalSection(&DAT_01267e48);
    }
}