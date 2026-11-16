extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_01201fc4 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_01201fc4* DAT_01201fc4;
extern "C" void __cdecl FUN_00fdd250(void)
{
    if (DAT_01201fc4)
    {
        DAT_01201fc4->DecRef();
    }
}
