extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_012024f8 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_012024f8* DAT_012024f8;
extern "C" void __cdecl FUN_00fdd3b0(void)
{
    if (DAT_012024f8)
    {
        DAT_012024f8->DecRef();
    }
}
