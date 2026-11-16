extern volatile int DAT_01269cdc;
struct Target { void* volatile vptr; };
struct Thunk { void FUN_00ddc920(int, int, int, int, int); };
typedef void (__thiscall *VirtualTarget)(Target*, int, int, int, int, int);
void Thunk::FUN_00ddc920(int a, int b, int c, int d, int e) {
    Target* target = *(Target**)((char*)this - 8);
    void* volatile* table = (void* volatile*)target->vptr;
    volatile int& fifth = e;
    fifth = DAT_01269cdc;
    VirtualTarget call = (VirtualTarget)table[15];
    call(target, a, b, c, d, e);
}
