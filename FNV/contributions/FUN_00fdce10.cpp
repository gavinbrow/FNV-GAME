extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011fffe0 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011fffe0* DAT_011fffe0;
extern "C" void __cdecl FUN_00fdce10(void)
{
    if (DAT_011fffe0)
    {
        DAT_011fffe0->DecRef();
    }
}
