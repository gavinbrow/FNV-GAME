struct Allocator {
    virtual void first();
    virtual void second();
    virtual void deallocate(void* object, unsigned short size);
};
struct Global { int unk00; int unk04; int unk08; int unk0c; Allocator* allocator; };
extern "C" Global* __cdecl FUN_00c85750();
struct FUN_00dfe4b0_Class {
    int vtable; unsigned short size; int unk08; int unk0c; int unk10;
    void FUN_00e40fd0();
    void* FUN_00dfe4b0(unsigned char flags);
};
void* FUN_00dfe4b0_Class::FUN_00dfe4b0(unsigned char flags)
{
    FUN_00e40fd0();
    if (flags & 1) {
        Global* global = FUN_00c85750();
        global->allocator->deallocate(this, size);
    }
    return this;
}
