void* __cdecl FUN_00aa13e0(unsigned int size);
inline void* __cdecl operator new(unsigned int, void* address) { return address; }
FUN_00a3fa30* __cdecl FUN_00a403f0()
{
    void* storage = FUN_00aa13e0(sizeof(FUN_00a3fa30));
    if (storage)
        return new (storage) FUN_00a3fa30(static_cast<NiTransformData*>(0));
    return 0;
}