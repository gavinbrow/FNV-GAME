struct FnvCpu_FUN_00c9d460_CpuAllocator {
    virtual void slot00();
    virtual void slot04();
    virtual void Invoke(void* block, unsigned int size);
};
struct FnvCpu_FUN_00c9d460_CpuAllocatorHolder {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    FnvCpu_FUN_00c9d460_CpuAllocator* allocator;
};
FnvCpu_FUN_00c9d460_CpuAllocatorHolder* __cdecl FUN_00c85750();
struct FnvCpu_FUN_00c9d460_CpuObject {
    unsigned int unk00;
    unsigned short size;
    void FUN_00c9d3b0();
    FnvCpu_FUN_00c9d460_CpuObject* FUN_00c9d460(unsigned int flags);
};
FnvCpu_FUN_00c9d460_CpuObject* FnvCpu_FUN_00c9d460_CpuObject::FUN_00c9d460(unsigned int flags)
{
    FUN_00c9d3b0();
    if (flags & 1) {
        FnvCpu_FUN_00c9d460_CpuAllocatorHolder* holder = FUN_00c85750();
        holder->allocator->Invoke(this, size);
    }
    return this;
}
