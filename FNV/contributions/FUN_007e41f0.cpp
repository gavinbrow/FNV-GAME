extern int __cdecl FUN_004dc200();
extern int __cdecl FUN_004dc1f0();
extern void __cdecl FUN_00703080(float, float);

void __cdecl FUN_007e41f0(int arg0, int arg1)
{
    if (DAT_011dada4 != 0 && *((unsigned char*)DAT_011dada4 + 0x90) == 0) {
        FUN_00703080((float)((double)arg0 / (double)FUN_004dc1f0()),
                    (float)((double)arg1 / (double)FUN_004dc200()));
    }
}