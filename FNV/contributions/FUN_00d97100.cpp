struct CpuAllocator {
    virtual void slot00();
    virtual void slot04();
    virtual void Invoke(void* block, unsigned int size);
};
struct CpuAllocatorHolder {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    CpuAllocator* allocator;
};
CpuAllocatorHolder* __cdecl FUN_00c85750();
struct CpuObject {
    unsigned int unk00;
    unsigned short size;
    void FUN_00d970c0();
    CpuObject* FUN_00d97100(unsigned int flags);
};
CpuObject* CpuObject::FUN_00d97100(unsigned int flags)
{
    FUN_00d970c0();
    if (flags & 1) {
        CpuAllocatorHolder* holder = FUN_00c85750();
        holder->allocator->Invoke(this, size);
    }
    return this;
}
