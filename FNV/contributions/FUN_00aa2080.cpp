typedef void (__cdecl *FUN_00aa2080_callback)();

extern int DAT_011f6108;
extern unsigned char DAT_011f610c;
extern FUN_00aa2080_callback DAT_011f60c8[];
extern int DAT_011f6088[];

void __cdecl FUN_00aa2080(FUN_00aa2080_callback callback, int value)
{
    DAT_011f60c8[DAT_011f6108] = callback;
    DAT_011f6088[DAT_011f6108] = value;
    ++DAT_011f6108;

    if (DAT_011f610c)
        return callback();
}