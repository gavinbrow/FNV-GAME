struct MemoryManager { void __thiscall Deallocate(void*); };
extern MemoryManager _g_memoryManager;
extern int DAT_0109bc84;
extern "C" void NiFreeAlias(void*);

struct NiTMapBaseStub {
    void RemoveAll();
};

struct NiTFixedStringMap_NiAVObject___ {
    void* m_baseData0;
    void* m_baseData1;
    void __thiscall RemoveAll();
};

struct FUN_00a639e0_Class {
    void* m_baseData0;
    void* m_baseData1;
    void* m_baseData2;
    FUN_00a639e0_Class* __thiscall FUN_00a639e0(char param_2);
};

FUN_00a639e0_Class* __thiscall FUN_00a639e0_Class::FUN_00a639e0(char param_2)
{
    m_baseData0 = &DAT_0109bc84;
    ((NiTMapBaseStub*)this)->RemoveAll();
    NiFreeAlias(m_baseData2);
    if (param_2 & 1)
        _g_memoryManager.Deallocate(this);
    return this;
}