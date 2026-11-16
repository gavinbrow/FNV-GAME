struct FUN_006d0420_Base {
    virtual ~FUN_006d0420_Base();
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    FUN_006d0420_Base();
};
struct FUN_006cf570 : FUN_006d0420_Base {
    void* m_allocator;
    FUN_006cf570(unsigned int initialSize, unsigned int growth, void* allocator);
    virtual ~FUN_006cf570();
    void __thiscall FUN_0069b940(unsigned int initialSize, unsigned int growth);
};
FUN_006cf570::FUN_006cf570(unsigned int initialSize, unsigned int growth, void* allocator)
    : FUN_006d0420_Base()
{
    m_allocator = allocator ? allocator : FUN_00401020()->FUN_00aa42e0();
    FUN_0069b940(initialSize, growth);
}