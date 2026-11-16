extern "C" double __cdecl sqrt(double);
extern "C" float DAT_010956cc;
extern "C" float DAT_010956d0;
extern "C" float DAT_011f3544;

// @fnv 0x00fb4070
void FUN_00fb4070()
{
    float value = DAT_010956cc;
    float root = static_cast<float>(sqrt(static_cast<double>(value)));
    float scale = root;
    DAT_011f3544 = DAT_010956d0 / scale;
}
