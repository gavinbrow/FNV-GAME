struct Allocator {
    virtual void first();
    virtual void second();
    virtual void Free(void* memory, unsigned short bytes);
};
struct Manager { int unk00; int unk04; int unk08; int unk0c; Allocator* allocator; };
Manager* __cdecl FUN_00c85750();
struct Record {
    void* vtable00;
    unsigned short unk04;
    void FUN_00dcc160();
    Record* FUN_00dcca30(unsigned int flags);
};
Record* Record::FUN_00dcca30(unsigned int flags) {
    FUN_00dcc160();
    if (flags & 1) {
        Manager* manager = FUN_00c85750();
        Allocator* allocator = manager->allocator;
        unsigned short size = unk04;
        allocator->Free(this, size);
    }
    return this;
}
