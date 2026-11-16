extern "C" void* DAT_010c9314;

struct OwnerManager {
    virtual void* Reserved0();
    virtual void* Reserved1();
    virtual void* Reserved2();
    virtual void* Reserved3();
    virtual void* CreateOwner(void* owner);
};

extern "C" OwnerManager* DAT_01268364;

struct FUN_00cc04d0_Class {
    void* m_pVtable;
    unsigned short m_iFlags;
    unsigned short m_iUnk;
    void* m_pOwner;

    FUN_00cc04d0_Class* __thiscall FUN_00cc04d0(void* owner);
};

FUN_00cc04d0_Class* __thiscall FUN_00cc04d0_Class::FUN_00cc04d0(void* owner)
{
    m_iUnk = 1;
    m_pVtable = &DAT_010c9314;
    m_pOwner = DAT_01268364->CreateOwner(owner);
    return this;
}
