struct FnvCpu_FUN_00ddb710_CpuBlock;
struct FnvCpu_FUN_00ddb710_CpuAllocator {
    virtual void slot00();
    virtual void* Invoke(unsigned int size);
};
struct FnvCpu_FUN_00ddb710_CpuHolder {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    FnvCpu_FUN_00ddb710_CpuAllocator* allocator;
};
void* __cdecl FUN_00c85750();
struct FnvCpu_FUN_00ddb710_CpuBlock {
    unsigned int unk00;
    unsigned short size;
    FnvCpu_FUN_00ddb710_CpuBlock* FUN_00ddb600(unsigned int value);
};
void* __cdecl FUN_00ddb710(unsigned int value)
{
    FnvCpu_FUN_00ddb710_CpuHolder* holder = static_cast<FnvCpu_FUN_00ddb710_CpuHolder*>(FUN_00c85750());
    FnvCpu_FUN_00ddb710_CpuBlock* block = static_cast<FnvCpu_FUN_00ddb710_CpuBlock*>(holder->allocator->Invoke(48));
    block->size = 48;
    block = block->FUN_00ddb600(value);
    if (block) return reinterpret_cast<char*>(block) + 8;
    return 0;
}
