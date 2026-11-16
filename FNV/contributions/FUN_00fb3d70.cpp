extern "C" double __cdecl sqrt(double);
extern float DAT_01095474;
extern float DAT_01095478;
extern float DAT_011f34dc;
extern const double DAT_01011598;

// @fnv 0x00fb3d70
extern "C" void FUN_00fb3d70()
{
    float values[3];
    values[2] = DAT_01095474;
    values[0] = static_cast<float>(sqrt(static_cast<double>(values[2])));
    values[1] = values[0];
    DAT_011f34dc = static_cast<float>(
        DAT_01011598 / static_cast<double>(DAT_01095474 * values[1]) * DAT_01095478);
}
