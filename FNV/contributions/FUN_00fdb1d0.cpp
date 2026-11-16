extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f5f3c { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f5f3c* DAT_011f5f3c;
extern "C" void __cdecl FUN_00fdb1d0(void)
{
    if (DAT_011f5f3c)
    {
        DAT_011f5f3c->DecRef();
    }
}
