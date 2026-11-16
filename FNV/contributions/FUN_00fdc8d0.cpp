extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f9524 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f9524* DAT_011f9524;
extern "C" void __cdecl FUN_00fdc8d0(void)
{
    if (DAT_011f9524)
    {
        DAT_011f9524->DecRef();
    }
}
