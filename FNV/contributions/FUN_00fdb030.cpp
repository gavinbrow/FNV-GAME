extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f4a64 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f4a64* DAT_011f4a64;
extern "C" void __cdecl FUN_00fdb030(void)
{
    if (DAT_011f4a64)
    {
        DAT_011f4a64->DecRef();
    }
}
