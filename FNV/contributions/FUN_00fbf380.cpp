extern "C" int __cdecl FUN_00cabb00(int red, int green, int blue, int alpha);
extern int DAT_01268fe8;

// @fnv 0x00fbf380
void __cdecl FUN_00fbf380()
{
    DAT_01268fe8 = FUN_00cabb00(0x78, 0x78, 0x78, 0xff);
}
