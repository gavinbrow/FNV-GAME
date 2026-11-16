__declspec(thread) unsigned int currentAllocationContext = 0x3b;

struct ThreadContextGuard
{
    unsigned int oldValue;
    ThreadContextGuard()
        : oldValue(currentAllocationContext)
    {
        currentAllocationContext = 0x10;
    }
    ~ThreadContextGuard()
    {
        currentAllocationContext = oldValue;
    }
};

struct StandinClass
{
    void* unk00;
    void* unk04;
    void* unk08;
    void* m_pData;
    void* __thiscall FUN_00ccf680(bool* result);
};

struct MemoryManagerAllocHelper
{
    void* Allocate(unsigned int size);
};

extern float DAT_010c72bc;
extern MM g_memoryManager;

struct AllocatedBlock
{
    unsigned int unk00;
    float value04;
    unsigned int unk08;
    float value0c;
    float value10;
};

void* StandinClass::FUN_00ccf680(bool* result)
{
    ThreadContextGuard guard;
    *result = (m_pData == 0);
    if (*result)
    {
        MemoryManagerAllocHelper* allocator =
            reinterpret_cast<MemoryManagerAllocHelper*>(&g_memoryManager);
        AllocatedBlock* block =
            reinterpret_cast<AllocatedBlock*>(allocator->Allocate(0x14));
        if (block != 0)
        {
            block->unk00 = 0;
            block->value04 = DAT_010c72bc;
            block->unk08 = 0;
            block->value0c = 20.0f;
            block->value10 = 5.0f;
        }
        else
        {
            block = reinterpret_cast<AllocatedBlock*>(0);
        }
        m_pData = block;
    }
    return m_pData;
}