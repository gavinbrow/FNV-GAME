extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f5e7c { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f5e7c* DAT_011f5e7c;
extern "C" void __cdecl FUN_00fdb110(void)
{
    if (DAT_011f5e7c)
    {
        DAT_011f5e7c->DecRef();
    }
}
