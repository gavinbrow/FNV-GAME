extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f4a7c { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f4a7c* DAT_011f4a7c;
extern "C" void __cdecl FUN_00fdb060(void)
{
    if (DAT_011f4a7c)
    {
        DAT_011f4a7c->DecRef();
    }
}
