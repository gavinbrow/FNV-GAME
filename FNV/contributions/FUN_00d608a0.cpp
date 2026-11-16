extern int DAT_010d14f8;
struct hkBoolD608 {
    unsigned char value;
    hkBoolD608(bool enabled = false) : value(enabled) {}
    hkBoolD608(const hkBoolD608& other) : value(other.value) {}
};
struct hkAllocatorD608 {
    virtual void vf00();
    virtual void* Allocate(int bytes);
};
struct hkRouterD608 {
    void* unk00; void* unk04; void* unk08; void* unk0c;
    hkAllocatorD608* allocator;
};
struct FUN_00d274c0 {
    void* unk00;
    unsigned short allocatedSize;
    FUN_00d274c0(int first, int second, hkBoolD608 enabled);
};
struct FUN_00d608a0 {
    void* vptr;
    unsigned short unk04;
    unsigned short count;
    FUN_00d274c0* child;
    unsigned char mode;
    FUN_00d608a0(int first, int second, unsigned char mode);
};
FUN_00d608a0::FUN_00d608a0(int first, int second, unsigned char mode) {
    count = 1;
    vptr = &DAT_010d14f8;
    this->mode = mode;
    hkRouterD608* router = static_cast<hkRouterD608*>(FUN_00c85750());
    FUN_00d274c0* next = static_cast<FUN_00d274c0*>(router->allocator->Allocate(28));
    next->allocatedSize = 28;
    child = new (next) FUN_00d274c0(first, second, hkBoolD608());
}