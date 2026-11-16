// @fnv 0x00fb87c0
struct S00ac5490_Str
{
    void Init(int first, int second);
};

extern "C" S00ac5490_Str DAT_011f8b84;
extern "C" void FUN_00fdc4b0();
extern "C" int __cdecl atexit(void (__cdecl *function)());

// The initializer's local frame is 32 bytes. Only the marker and pointer
// assignment have independently recovered uses; other fields are unknown.
struct InitializationFrame
{
    unsigned int unknown00;
    unsigned int unknown04;
    unsigned int unknown08;
    unsigned int unknown0c;
    unsigned int unknown10;
    unsigned char unknown14;
    unsigned char unknown15;
    unsigned char unknown16;
    unsigned char marker;
    unsigned char* markerAddress;
    unsigned int unknown1c;
};

void FUN_00fb87c0()
{
    InitializationFrame frame;
    frame.markerAddress = &frame.marker;

    DAT_011f8b84.Init(0, 0);
    atexit(&FUN_00fdc4b0);
}
