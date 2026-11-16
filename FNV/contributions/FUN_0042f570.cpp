extern "C" char DAT_01015a08;

struct BSSimpleArray
{
    void* m_vtable;
    void __thiscall FUN_006b3eb0(unsigned int size, bool releaseMemory);
};

struct NavMeshArr : BSSimpleArray
{
    NavMeshArr* __thiscall FUN_0042f570();
};

// @fnv 0x0042f570
NavMeshArr* NavMeshArr::FUN_0042f570()
{
    m_vtable = &DAT_01015a08;
    FUN_006b3eb0(0, false);
    return this;
}
