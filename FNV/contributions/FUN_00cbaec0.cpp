extern int DAT_010c8d28;
struct FUN_00cbaec0_Obj {
    virtual void vf00();
    virtual void vf04();
    virtual void vf08(void* data);
    void* m_pData;
    unsigned int m_uiSize;
    unsigned int m_uiReservedSize;
    void __thiscall FUN_00cba0d0(void* data, unsigned int size);
    FUN_00cbaec0_Obj* __thiscall FUN_00cbaec0(unsigned char flags);
};
FUN_00cbaec0_Obj* __thiscall FUN_00cbaec0_Obj::FUN_00cbaec0(unsigned char flags) {
    void* oldData = m_pData;
    *reinterpret_cast<int**>(this) = &DAT_010c8d28;
    if (oldData) {
        FUN_00cba0d0(oldData, m_uiSize);
        vf08(m_pData);
        m_pData = 0;
        m_uiReservedSize = 0;
        m_uiSize = 0;
    }
    if (flags & 1)
        _g_memoryManager.Deallocate(this);
    return this;
}