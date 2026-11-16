extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_0126f910 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_0126f910* DAT_0126f910;
extern "C" void __cdecl FUN_00fde390(void)
{
    if (DAT_0126f910)
    {
        DAT_0126f910->DecRef();
    }
}
