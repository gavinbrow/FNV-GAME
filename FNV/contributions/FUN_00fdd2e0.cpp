extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_012021e4 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_012021e4* DAT_012021e4;
extern "C" void __cdecl FUN_00fdd2e0(void)
{
    if (DAT_012021e4)
    {
        DAT_012021e4->DecRef();
    }
}
