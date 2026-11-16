extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_01200840 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_01200840* DAT_01200840;
extern "C" void __cdecl FUN_00fdd0a0(void)
{
    if (DAT_01200840)
    {
        DAT_01200840->DecRef();
    }
}
