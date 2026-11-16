struct RgbaColor
{
    float r;
    float g;
    float b;
    float a;
};

extern const float DAT_010231a8;
extern float DAT_0101e2bc;
extern RgbaColor DAT_012030c8;
extern RgbaColor DAT_012030d8;
extern RgbaColor DAT_012030e8;
extern RgbaColor DAT_012030f8;

// @fnv 0x00fbbcb0
extern "C" void FUN_00fbbcb0()
{
    DAT_012030c8.r = DAT_010231a8;
    DAT_012030c8.g = DAT_010231a8;
    DAT_012030c8.b = DAT_010231a8;
    DAT_012030c8.a = DAT_0101e2bc;

    DAT_012030d8.r = 0.0f;
    DAT_012030d8.g = 0.8f;
    DAT_012030d8.b = 0.0f;
    DAT_012030d8.a = DAT_0101e2bc;

    DAT_012030e8.r = 0.0f;
    DAT_012030e8.g = 0.0f;
    DAT_012030e8.b = 0.7f;
    DAT_012030e8.a = DAT_0101e2bc;

    DAT_012030f8.r = 0.5f;
    DAT_012030f8.g = 0.0f;
    DAT_012030f8.b = 0.0f;
    DAT_012030f8.a = DAT_0101e2bc;
}
