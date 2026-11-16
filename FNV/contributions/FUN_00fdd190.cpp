extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_01201f40 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_01201f40* DAT_01201f40;
extern "C" void __cdecl FUN_00fdd190(void)
{
    if (DAT_01201f40)
    {
        DAT_01201f40->DecRef();
    }
}
