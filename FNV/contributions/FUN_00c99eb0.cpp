struct FNV_Allocator {
    virtual void reserved();
    virtual void* allocate(unsigned int bytes);
};
struct FNV_AllocatorContext {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0C;
    FNV_Allocator* allocator;
};
FNV_AllocatorContext* __cdecl FUN_00c85750();
struct FNV_Subobject {
    void* FUN_00cf6da0(unsigned int value);
};
extern void* DAT_010c69cc;
struct FUN_00c99eb0 {
    void* m_vtable;
    unsigned short m_04;
    unsigned short m_flag06;
    unsigned int m_08;
    unsigned int m_0C;
    unsigned int m_10;
    void* m_14;
    FUN_00c99eb0();
};
FUN_00c99eb0::FUN_00c99eb0() {
    m_flag06 = 1;
    m_vtable = &DAT_010c69cc;
    m_08 = 0;
    m_0C = 0;
    m_10 = 0x80000000u;
    FNV_AllocatorContext* context = FUN_00c85750();
    void* memory = context->allocator->allocate(0x18);
    void* initialized = memory
        ? static_cast<FNV_Subobject*>(memory)->FUN_00cf6da0(1000)
        : 0;
    m_14 = initialized;
}