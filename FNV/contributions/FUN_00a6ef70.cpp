
extern "C" void* __cdecl FUN_00aa13e0(unsigned int size);
extern "C" void* __cdecl FUN_00aa1070(unsigned int size);
extern "C" void* __cdecl FUN_00ec61c0(void* buffer, int value, unsigned int size);
extern "C" unsigned char DAT_01096284;
extern "C" unsigned char DAT_01096114;
extern "C" unsigned char DAT_0109618c;
struct PaletteBase {
    void* vtable;
    unsigned int unknown;
    void __thiscall FUN_00a5d3a0();
    __forceinline PaletteBase() throw() {
        FUN_00a5d3a0();
        vtable = &DAT_01096284;
    }
};
struct PaletteHash {
    void* vtable;
    unsigned int capacity;
    void* buckets;
    unsigned int count;
    __forceinline PaletteHash() throw() {
        vtable = &DAT_01096114;
        capacity = 37;
        count = 0;
        buckets = FUN_00aa1070(148);
        FUN_00ec61c0(buckets, 0, capacity * 4);
        vtable = &DAT_0109618c;
    }
};
struct PaletteObject : PaletteBase {
    PaletteHash hash;
    void* scene;
    static __forceinline void* operator new(unsigned int size) throw() { return FUN_00aa13e0(size); }
    __forceinline PaletteObject() throw() : PaletteBase(), hash(), scene(0) {}
};
struct PaletteOwner {
    void __thiscall FUN_00aa1000(PaletteObject* palette, void* argument);
    PaletteObject* __thiscall FUN_00a6ef70(void* argument);
};
PaletteObject* PaletteOwner::FUN_00a6ef70(void* argument)
{
    PaletteObject* palette = new PaletteObject;
    FUN_00aa1000(palette, argument);
    return palette;
}
