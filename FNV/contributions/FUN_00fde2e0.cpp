extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_00fde2e0 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_00fde2e0* DAT_0126f108[256];
void __cdecl FUN_00fde2e0(void)
{
    RefObj_00fde2e0** pp = &DAT_0126f108[256];
    for (int i = 255; i >= 0; --i)
    {
        RefObj_00fde2e0* p = *--pp;
        if (p)
        {
            p->DecRef();
        }
    }
}
