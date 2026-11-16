extern __declspec(thread) int iCurrentMemContext;

struct MemoryContextGuard {
    int previous;
    MemoryContextGuard() {
        previous = iCurrentMemContext;
        iCurrentMemContext = 0x10;
    }
    ~MemoryContextGuard() {
        iCurrentMemContext = previous;
    }
};

struct FUN_00cb0780_Allocator {
    virtual void slot00();
    virtual void slot04();
    virtual void Free(void* memory, unsigned int size);
};
struct FUN_00cb0780_Manager {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00cb0780_Allocator* allocator;
};
void* __cdecl FUN_00c85750();

struct FUN_00cb0780_class {
    int unk00;
    int unk04;
    int unk08;
    void* memory;
    void FUN_00cb0780(bool release);
};
void FUN_00cb0780_class::FUN_00cb0780(bool release)
{
    void* allocation;
    MemoryContextGuard guard;
    if (release) {
        allocation = memory;
        if (allocation) {
            FUN_00cb0780_Manager* manager = (FUN_00cb0780_Manager*)FUN_00c85750();
            manager->allocator->Free(allocation, 0x30);
        }
        memory = 0;
    }
}
