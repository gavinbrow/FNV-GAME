extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f95d8 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f95d8* DAT_011f95d8;
extern "C" void __cdecl FUN_00fdcb60(void)
{
    if (DAT_011f95d8)
    {
        DAT_011f95d8->DecRef();
    }
}
