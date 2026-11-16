// @fnv 0x00fdafb0
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
struct Obj {
    virtual void v0();
    virtual void v1();
    volatile long refcount;
    void Release() { if (!InterlockedDecrement(&refcount)) v1(); }
};
extern Obj* DAT_011f49ac;
void FUN_00fdafb0()
{
    if (DAT_011f49ac) DAT_011f49ac->Release();
}
