extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f950c { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f950c* DAT_011f950c;
extern "C" void __cdecl FUN_00fdc7b0(void)
{
    if (DAT_011f950c)
    {
        DAT_011f950c->DecRef();
    }
}
