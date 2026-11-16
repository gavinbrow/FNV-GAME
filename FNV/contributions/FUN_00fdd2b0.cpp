extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_012021e0 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_012021e0* DAT_012021e0;
extern "C" void __cdecl FUN_00fdd2b0(void)
{
    if (DAT_012021e0)
    {
        DAT_012021e0->DecRef();
    }
}
