extern double DAT_010996d0;
extern float DAT_011f4010;
extern "C" double __cdecl sqrt(double);

void __cdecl FUN_00fb5270(void)
{
    float s = (float)sqrt(0.9590659737586975);
    DAT_011f4010 = (float)(DAT_010996d0 / s);
}