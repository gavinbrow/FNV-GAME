extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f4438 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f4438* DAT_011f4438;
extern "C" void __cdecl FUN_00fdaea0(void)
{
    if (DAT_011f4438)
    {
        DAT_011f4438->DecRef();
    }
}
