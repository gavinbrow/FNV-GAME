extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011f9508 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011f9508* DAT_011f9508;
extern "C" void __cdecl FUN_00fdcb10(void)
{
    if (DAT_011f9508)
    {
        DAT_011f9508->DecRef();
    }
}
