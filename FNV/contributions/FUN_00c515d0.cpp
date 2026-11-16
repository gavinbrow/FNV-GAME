struct FNVHeap {
    void FUN_00aa4060(void* allocation);
};
extern FNVHeap DAT_011f6238;
extern "C" void __cdecl FUN_00c516d0();
extern "C" void __stdcall FUN_00ec5fce(void* objects, unsigned int objectSize, unsigned int count, void (__cdecl *destructor)());

struct DynamicObject {
    void FUN_00b00ec0();
    void* FUN_00c515d0(unsigned int flags);
};
void* DynamicObject::FUN_00c515d0(unsigned int flags)
{
    if (flags & 2) {
        FUN_00ec5fce(this, 0x20, *reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) - 4), &FUN_00c516d0);
        if (flags & 1) {
            DAT_011f6238.FUN_00aa4060(reinterpret_cast<char*>(this) - 4);
        }
        return reinterpret_cast<char*>(this) - 4;
    }
    FUN_00b00ec0();
    if (flags & 1) {
        DAT_011f6238.FUN_00aa4060(this);
    }
    return this;
}
