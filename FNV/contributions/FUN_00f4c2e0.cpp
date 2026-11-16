// @fnv 0x00f4c2e0
struct GameFloatSetting
{
    float* FUN_00403e20();
};
struct GlobalObject
{
    void FUN_0045d060(const char*, float);
};
extern GameFloatSetting DAT_011ca4cc;
extern GlobalObject DAT_011ca450;
extern const char DAT_01031218[];
extern "C" void FUN_00fcb040();
extern "C" int atexit(void (*)(void));

void FUN_00f4c2e0()
{
    DAT_011ca450.FUN_0045d060(DAT_01031218, *DAT_011ca4cc.FUN_00403e20());
    atexit(FUN_00fcb040);
}
