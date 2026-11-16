struct Allocator {
    virtual void unused0();
    virtual void unused1();
    virtual void freeBlock(void*, unsigned int);
};
struct ThreadState {
    int unk00; int unk04; int unk08; int unk0c;
    Allocator* allocator;
};
ThreadState* __cdecl FUN_00c85750();
struct Object {
    void* vtable;
    unsigned short allocationSize;
    void FUN_00e00000();
    Object* FUN_00e00070(unsigned int flags);
};
Object* Object::FUN_00e00070(unsigned int flags) {
    FUN_00e00000();
    if (flags & 1) {
        ThreadState* state = FUN_00c85750();
        unsigned int size = allocationSize;
        state->allocator->freeBlock(this, size);
    }
    return this;
}


