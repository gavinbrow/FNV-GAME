extern "C" double __cdecl sqrt(double);
extern const double DAT_01099680;
extern const double DAT_010996d0;
extern float DAT_011f3ff0;
// @fnv 0x00fb51c0
void FUN_00fb51c0()
{
    const float root = static_cast<float>(sqrt(DAT_01099680));
    DAT_011f3ff0 = static_cast<float>(DAT_010996d0 / root);
}