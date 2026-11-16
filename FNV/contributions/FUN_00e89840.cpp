extern "C" void __cdecl FUN_00aa10f0(void*);
extern int DAT_010ef73c;
extern int DAT_0101dce4;
extern volatile long DAT_011f4400;
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
struct ReleaseInterface {
    virtual void __stdcall GetType();
    virtual void __stdcall GetFlags();
    virtual void __stdcall Release();
};
struct FUN_00e89840_Class {
    void* m_vtable;
    int m_04;
    int m_08;
    void* m_0c;
    void* m_10;
    int m_14;
    void* m_18;
    int m_1c;
    ReleaseInterface* m_20;
    int m_24;
    int m_28;
    void FUN_00e89840();
};
void FUN_00e89840_Class::FUN_00e89840()
{
    m_vtable = &DAT_010ef73c;
    FUN_00aa10f0(m_0c);
    FUN_00aa10f0(m_10);
    FUN_00aa10f0(m_18);
    m_24 = 0;
    m_28 = 0;
    if (m_20 != 0) m_20->Release();
    m_20 = 0;
    m_vtable = &DAT_0101dce4;
    InterlockedDecrement(&DAT_011f4400);
}