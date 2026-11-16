extern "C" __declspec(dllimport) void __stdcall InitializeCriticalSection(void* section);
extern "C" __declspec(dllimport) void __stdcall DeleteCriticalSection(void* section);
struct CriticalSection {
    void* debugInfo;
    long lockCount;
    long recursionCount;
    void* ownerThread;
    void* semaphore;
    unsigned long spinCount;
    CriticalSection() { InitializeCriticalSection(this); }
    ~CriticalSection() { DeleteCriticalSection(this); }
};
struct LifoAllocator {
    void* current;
    void* end;
    void* firstNonLifoEnd;
    unsigned int slabSize;
    void* buffer;
    void* backingAllocator;
    int allocationCount;
};
struct HavokRouter {
    void* temporaryAllocator;
    void* heapAllocator;
    void* debugAllocator;
    LifoAllocator stackAllocator;
};
struct RouterSlot {
    int state;
    HavokRouter memory;
    RouterSlot();
    ~RouterSlot();
};
struct FUN_00c67fe0 {
    CriticalSection lock;
    RouterSlot routers[16];
    int state;
    FUN_00c67fe0();
};
FUN_00c67fe0::FUN_00c67fe0() : state(0) {}