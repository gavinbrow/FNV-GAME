extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f952c { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f952c* DAT_011f952c;
extern "C" void __cdecl FUN_00fdc930(void)
{
    if (DAT_011f952c)
    {
        DAT_011f952c->DecRef();
    }
}
