// @fnv 0x00ee6d50
// Indirect API thunk; exact imported signature remains unresolved.
typedef int (__stdcall *XNetApiThunk)();
extern "C" XNetApiThunk DAT_00fdf344;

extern "C" int __stdcall FUN_00ee6d50()
{
    return DAT_00fdf344();
}
