struct NiMemObject {
    static void* __cdecl operator new(unsigned int size);
};
struct FUN_00e94ab0 : NiMemObject {
    void* objectVtable;
    unsigned int unk04;
    unsigned int unk08;
    void* mapVtable;
    unsigned int mapCount;
    void* mapData;
    unsigned int unk18;
    FUN_00e94ab0();
};
__declspec(noinline) FUN_00e94ab0::FUN_00e94ab0() {
    unk18 = 0;
}
FUN_00e94ab0* __cdecl FUN_00e94c00() {
    return new FUN_00e94ab0;
}
