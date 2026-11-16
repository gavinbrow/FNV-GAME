// @fnv 0x00fdb1a0
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
struct Obj {
    virtual void v0();
    virtual void v1();
    volatile long refcount;
    void Release() { if (!InterlockedDecrement(&refcount)) v1(); }
};
extern Obj* DAT_011f5ed4;
void FUN_00fdb1a0()
{
    if (DAT_011f5ed4) DAT_011f5ed4->Release();
}
