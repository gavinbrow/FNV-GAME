extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_0120083c { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_0120083c* DAT_0120083c;
extern "C" void __cdecl FUN_00fdd070(void)
{
    if (DAT_0120083c)
    {
        DAT_0120083c->DecRef();
    }
}
