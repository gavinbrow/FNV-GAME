struct FnvCpu_FUN_00d645f0_CpuBlock;
struct FnvCpu_FUN_00d645f0_CpuAllocator {
    virtual void slot00();
    virtual void* Invoke(unsigned int size);
};
struct FnvCpu_FUN_00d645f0_CpuHolder {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    FnvCpu_FUN_00d645f0_CpuAllocator* allocator;
};
void* __cdecl FUN_00c85750();
struct FnvCpu_FUN_00d645f0_CpuBlock {
    unsigned int unk00;
    unsigned short size;
    FnvCpu_FUN_00d645f0_CpuBlock* FUN_00d64260(unsigned int value);
};
void* __cdecl FUN_00d645f0(unsigned int value)
{
    FnvCpu_FUN_00d645f0_CpuHolder* holder = static_cast<FnvCpu_FUN_00d645f0_CpuHolder*>(FUN_00c85750());
    FnvCpu_FUN_00d645f0_CpuBlock* block = static_cast<FnvCpu_FUN_00d645f0_CpuBlock*>(holder->allocator->Invoke(60));
    block->size = 60;
    block = block->FUN_00d64260(value);
    if (block) return reinterpret_cast<char*>(block) + 8;
    return 0;
}
