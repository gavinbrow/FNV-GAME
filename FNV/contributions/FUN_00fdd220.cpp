extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_01201f58 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_01201f58* DAT_01201f58;
extern "C" void __cdecl FUN_00fdd220(void)
{
    if (DAT_01201f58)
    {
        DAT_01201f58->DecRef();
    }
}
