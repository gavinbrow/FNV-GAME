extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011fa008 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011fa008* DAT_011fa008;
extern "C" void __cdecl FUN_00fdcca0(void)
{
    if (DAT_011fa008)
    {
        DAT_011fa008->DecRef();
    }
}
