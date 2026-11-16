extern float DAT_011f940c;
extern double DAT_0104f2f0;
extern float DAT_0120005c;

struct FUN_00ba13b0_Class
{
    bool __thiscall FUN_00ba13b0(int unused);
};

bool FUN_00ba13b0_Class::FUN_00ba13b0(int unused)
{
    *(float*)((char*)this + 0xB0) =
        (DAT_011f940c / DAT_0104f2f0) * DAT_0120005c;
    return true;
}