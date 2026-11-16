// @fnv 0x00fb40b0
extern "C" double __cdecl sqrt(double);
extern "C" float DAT_010956cc;
extern "C" double DAT_01011598;
extern "C" float DAT_010956d0;
extern "C" float DAT_011f3548;
void FUN_00fb40b0() {
    float tmp[3];
    tmp[2] = DAT_010956cc;
    tmp[0] = (float)sqrt((double)tmp[2]);
    tmp[1] = tmp[0];
    DAT_011f3548 = (DAT_01011598 / (DAT_010956cc * tmp[1])) * DAT_010956d0;
}