extern void* __cdecl FUN_00aa13e0(unsigned int size);
struct FUN_00ccd100 {
    void* vtable;
    unsigned int refCount;
    unsigned int flags;
    unsigned int dataA;
    unsigned int dataB;
    FUN_00ccd100();
    static void* __cdecl operator new(unsigned int bytes) {
        return FUN_00aa13e0(bytes);
    }
};
FUN_00ccd100* __cdecl FUN_00ccd250() {
    return new FUN_00ccd100;
}