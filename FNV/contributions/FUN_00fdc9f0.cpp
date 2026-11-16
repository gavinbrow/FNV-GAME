extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f953c { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f953c* DAT_011f953c;
extern "C" void __cdecl FUN_00fdc9f0(void)
{
    if (DAT_011f953c)
    {
        DAT_011f953c->DecRef();
    }
}
