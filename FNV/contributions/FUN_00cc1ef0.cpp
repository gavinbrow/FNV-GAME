struct FUN_00cc1d80_object {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    void* unk10;
    void* unk14;
    void* unk18;
    void* unk1c;
    void* unk20;
    FUN_00cc1d80_object();
    static void* __cdecl operator new(unsigned int bytes);
    void __thiscall FUN_00a5b950(void* value);
};
extern "C" char DAT_011f49e0;
FUN_00cc1d80_object* __cdecl FUN_00cc1ef0()
{
    FUN_00cc1d80_object* value = new FUN_00cc1d80_object;
    value->FUN_00a5b950(&DAT_011f49e0);
    return value;
}