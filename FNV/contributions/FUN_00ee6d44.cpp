// @fnv 0x00ee6d44
typedef int (__stdcall *XNetApiThunk)();
extern "C" XNetApiThunk DAT_00fdf33c;

extern "C" int __stdcall FUN_00ee6d44()
{
    return DAT_00fdf33c();
}
