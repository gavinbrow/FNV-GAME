struct HavokHeap {
    virtual void reserve();
    virtual void allocate();
    virtual void release(void* memory, unsigned int size);
};
struct HavokRouter {
    int unk00, unk04, unk08, unk0c;
    HavokHeap* heap;
};
extern "C" HavokRouter* __cdecl FUN_00c85750();
struct EmbeddedRegistry {
    void FUN_00d877d0();
    ~EmbeddedRegistry() { FUN_00d877d0(); }
};
struct RegistryBase {
    virtual ~RegistryBase() {}
    unsigned short allocatedSize;
    unsigned short unk06;
    int unk08;
};
struct RegistryImpl : RegistryBase {
    EmbeddedRegistry embedded;
    RegistryImpl* FUN_00d47b30(unsigned int flags);
};
RegistryImpl* RegistryImpl::FUN_00d47b30(unsigned int flags) {
    embedded.~EmbeddedRegistry();
    RegistryBase::~RegistryBase();
    if (flags & 1) {
        HavokRouter* router = FUN_00c85750();
        router->heap->release(this, allocatedSize);
    }
    return this;
}