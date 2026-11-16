extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f9514 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f9514* DAT_011f9514;
extern "C" void __cdecl FUN_00fdc810(void)
{
    if (DAT_011f9514)
    {
        DAT_011f9514->DecRef();
    }
}
