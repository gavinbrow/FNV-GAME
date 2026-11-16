struct FnvCpu_FUN_00d66770_CpuBlock;
struct FnvCpu_FUN_00d66770_CpuAllocator {
    virtual void slot00();
    virtual void* Invoke(unsigned int size);
};
struct FnvCpu_FUN_00d66770_CpuHolder {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    FnvCpu_FUN_00d66770_CpuAllocator* allocator;
};
void* __cdecl FUN_00c85750();
struct FnvCpu_FUN_00d66770_CpuBlock {
    unsigned int unk00;
    unsigned short size;
    FnvCpu_FUN_00d66770_CpuBlock* FUN_00d66430(unsigned int value);
};
void* __cdecl FUN_00d66770(unsigned int value)
{
    FnvCpu_FUN_00d66770_CpuHolder* holder = static_cast<FnvCpu_FUN_00d66770_CpuHolder*>(FUN_00c85750());
    FnvCpu_FUN_00d66770_CpuBlock* block = static_cast<FnvCpu_FUN_00d66770_CpuBlock*>(holder->allocator->Invoke(60));
    block->size = 60;
    block = block->FUN_00d66430(value);
    if (block) return reinterpret_cast<char*>(block) + 8;
    return 0;
}
