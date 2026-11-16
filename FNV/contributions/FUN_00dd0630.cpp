struct FnvCpu_FUN_00dd0630_CpuAllocator {
    virtual void slot00();
    virtual void slot04();
    virtual void Invoke(void* block, unsigned int size);
};
struct FnvCpu_FUN_00dd0630_CpuAllocatorHolder {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    FnvCpu_FUN_00dd0630_CpuAllocator* allocator;
};
FnvCpu_FUN_00dd0630_CpuAllocatorHolder* __cdecl FUN_00c85750();
struct FnvCpu_FUN_00dd0630_CpuObject {
    unsigned int unk00;
    unsigned short size;
    void FUN_00dd05c0();
    FnvCpu_FUN_00dd0630_CpuObject* FUN_00dd0630(unsigned int flags);
};
FnvCpu_FUN_00dd0630_CpuObject* FnvCpu_FUN_00dd0630_CpuObject::FUN_00dd0630(unsigned int flags)
{
    FUN_00dd05c0();
    if (flags & 1) {
        FnvCpu_FUN_00dd0630_CpuAllocatorHolder* holder = FUN_00c85750();
        holder->allocator->Invoke(this, size);
    }
    return this;
}
