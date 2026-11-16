struct AllocIfaceFree : AllocIface
{
    virtual void Free(void* block, unsigned int size);
};

extern void* DAT_012691fc;

void __cdecl FUN_00d88070()
{
    void* block = DAT_012691fc;
    if (block)
    {
        AllocHolder* holder = FUN_00c85750();
        AllocIfaceFree* allocator =
            static_cast<AllocIfaceFree*>(holder->m_pAllocator);
        allocator->Free(block, 60);
    }
    DAT_012691fc = 0;
}