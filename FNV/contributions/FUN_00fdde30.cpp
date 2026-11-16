extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_01267be0 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_01267be0* DAT_01267be0;
extern "C" void __cdecl FUN_00fdde30(void)
{
    if (DAT_01267be0)
    {
        DAT_01267be0->DecRef();
    }
}
