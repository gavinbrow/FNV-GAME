extern int DAT_010c925c;

struct FUN_00cbf6e0_cls
{
    void* m_vtable;
    FUN_00cbf6e0_cls* FUN_00cbf6e0(unsigned int flags);
};

FUN_00cbf6e0_cls* FUN_00cbf6e0_cls::FUN_00cbf6e0(unsigned int flags)
{
    m_vtable = &DAT_010c925c;
    if ((flags & 1) != 0)
        DAT_011f6238.Free(this);
    return this;
}
