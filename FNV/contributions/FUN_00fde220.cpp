extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_012682f0 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_012682f0* DAT_012682f0;
extern "C" void __cdecl FUN_00fde220(void)
{
    if (DAT_012682f0)
    {
        DAT_012682f0->DecRef();
    }
}
