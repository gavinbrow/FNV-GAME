extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_01201f44 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_01201f44* DAT_01201f44;
extern "C" void __cdecl FUN_00fdd1c0(void)
{
    if (DAT_01201f44)
    {
        DAT_01201f44->DecRef();
    }
}
