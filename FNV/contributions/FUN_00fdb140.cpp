extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f5e74 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f5e74* DAT_011f5e74;
extern "C" void __cdecl FUN_00fdb140(void)
{
    if (DAT_011f5e74)
    {
        DAT_011f5e74->DecRef();
    }
}
