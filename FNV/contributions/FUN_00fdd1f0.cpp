extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_01201f48 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_01201f48* DAT_01201f48;
extern "C" void __cdecl FUN_00fdd1f0(void)
{
    if (DAT_01201f48)
    {
        DAT_01201f48->DecRef();
    }
}
