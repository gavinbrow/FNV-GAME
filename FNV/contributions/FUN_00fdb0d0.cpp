extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f5d28 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f5d28* DAT_011f5d28;
extern "C" void __cdecl FUN_00fdb0d0(void)
{
    if (DAT_011f5d28)
    {
        DAT_011f5d28->DecRef();
    }
}
