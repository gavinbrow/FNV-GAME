extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
struct RefObj_011fedc4 { virtual void v00(); virtual void DeleteThis(); long m_uiRefCount;
    void DecRef() { if (!InterlockedDecrement(&m_uiRefCount)) DeleteThis(); } };
extern RefObj_011fedc4* DAT_011fedc4;
extern "C" void __cdecl FUN_00fdcda0(void)
{
    if (DAT_011fedc4)
    {
        DAT_011fedc4->DecRef();
    }
}
