struct Allocator {
    virtual void unused0();
    virtual void unused1();
    virtual void Free(void* block, unsigned int size);
};
struct AllocatorHolder {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    Allocator* allocator;
};
AllocatorHolder* __cdecl FUN_00c85750();
struct FUN_00ddabb0_shell {
    void* unk00;
    unsigned short size;
    void FUN_00d60590();
    FUN_00ddabb0_shell* FUN_00ddabb0(unsigned int flags);
};
FUN_00ddabb0_shell* FUN_00ddabb0_shell::FUN_00ddabb0(unsigned int flags)
{
    FUN_00d60590();
    if (flags & 1) {
        AllocatorHolder* holder = FUN_00c85750();
        holder->allocator->Free(this, size);
    }
    return this;
}
