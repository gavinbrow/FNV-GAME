extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_01201fd0 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_01201fd0* DAT_01201fd0;
extern "C" void __cdecl FUN_00fdd280(void)
{
    if (DAT_01201fd0)
    {
        DAT_01201fd0->DecRef();
    }
}
