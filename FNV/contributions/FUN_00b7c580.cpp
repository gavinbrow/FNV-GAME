
struct FNVColorRGB {
    float red, green, blue;
};
struct FNVColorRGBA {
    float red, green, blue, alpha;
};
extern void* DAT_011f91e0;
extern float DAT_011fa0c0;

void FUN_00b7deb0_class::FUN_00b7c580()
{
    char* manager = static_cast<char*>(DAT_011f91e0);
    char* slot = *reinterpret_cast<char**>(manager + 0x0c);
    char* renderer = *reinterpret_cast<char**>(slot);
    char* state = *reinterpret_cast<char**>(renderer + 0xf8);
    FNVColorRGB rgb = *reinterpret_cast<FNVColorRGB*>(state + 0xc8);
    FNVColorRGBA color = { rgb.red, rgb.green, rgb.blue, 1.0f };
    *reinterpret_cast<FNVColorRGBA*>(&DAT_011fa0c0) = color;
}
