// @fnv 0x00fdae10
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
struct Obj {
    virtual void v0();
    virtual void v1();
    volatile long refcount;
    void Release() { if (!InterlockedDecrement(&refcount)) v1(); }
};
extern Obj* DAT_011f3f40;
void FUN_00fdae10()
{
    if (DAT_011f3f40) DAT_011f3f40->Release();
}
