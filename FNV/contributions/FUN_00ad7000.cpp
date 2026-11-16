struct FUN_00aea0d0_Class { void Init(); };
extern unsigned int DAT_010a323c;
struct AudioInitializer
{
    unsigned int* vtable;
    unsigned int unknown_1;
    unsigned int unknown_2;
    unsigned int unknown_3;
    unsigned int unknown_4;
    FUN_00aea0d0_Class device;
    void FUN_00ad7000();
};
// @fnv 0x00ad7000
void AudioInitializer::FUN_00ad7000()
{
    vtable = &DAT_010a323c;
    device.Init();
}
