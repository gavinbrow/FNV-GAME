extern "C" double __cdecl sqrt(double);
extern float DAT_01094ef0;
extern float DAT_01094ef4;
extern float DAT_011f33b8;
extern const double DAT_01011598;

// @fnv 0x00fb3510
extern "C" void FUN_00fb3510()
{
    float values[3];
    values[2] = DAT_01094ef0;
    values[0] = static_cast<float>(sqrt(static_cast<double>(values[2])));
    values[1] = values[0];
    DAT_011f33b8 = static_cast<float>(
        DAT_01011598 / static_cast<double>(DAT_01094ef0 * values[1]) * DAT_01094ef4);
}
