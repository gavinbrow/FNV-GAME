// @fnv 0x00ee6d4a
// Indirect API thunk; exact imported signature remains unresolved.
typedef int (__stdcall *XNetApiThunk)();
extern "C" XNetApiThunk DAT_00fdf340;

extern "C" int __stdcall FUN_00ee6d4a()
{
    return DAT_00fdf340();
}
