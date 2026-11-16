void* __cdecl FUN_00aa13e0(unsigned int size);
extern "C" void* DAT_0109cd44;
struct NiTriStripsObject {
    void* vtable;
    void FUN_00a89740();
    static void* operator new(unsigned int size, unsigned int extraBytes) {
        return FUN_00aa13e0(size + extraBytes);
    }
    NiTriStripsObject() {
        FUN_00a89740();
        vtable = &DAT_0109cd44;
    }
};
struct FUN_00a71db0_class {
    void FUN_00a9b140(NiTriStripsObject* strips, int value);
    NiTriStripsObject* FUN_00a71db0(int value);
};
NiTriStripsObject* FUN_00a71db0_class::FUN_00a71db0(int value)
{
    NiTriStripsObject* strips = new (0xc0) NiTriStripsObject;
    FUN_00a9b140(strips, value);
    return strips;
}