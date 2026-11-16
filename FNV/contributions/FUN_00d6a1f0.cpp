struct Allocator { virtual void A(); virtual void B(); virtual void Free(void*, unsigned short); };
struct Manager { int unk00, unk04, unk08, unk0C; Allocator* unk10; };
extern Manager* __cdecl FUN_00c85750();
struct Owner {
    __declspec(noinline) virtual ~Owner();
    unsigned short unk04;
    unsigned short unk06;
    void* FUN_00d6a1f0(unsigned int flags);
};
Owner::~Owner() {}
void* Owner::FUN_00d6a1f0(unsigned int flags) {
    this->Owner::~Owner();
    if (flags & 1) {
        Manager* manager = FUN_00c85750();
        Allocator* allocator = manager->unk10;
        unsigned short size = unk04;
        allocator->Free(this, size);
    }
    return this;
}
Owner force_vtable;
