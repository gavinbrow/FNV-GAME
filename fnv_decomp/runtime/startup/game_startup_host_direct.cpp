// Experimental direct-source adapter; excluded from the reference recipe.
// Compile and link do not establish runtime or ABI readiness.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#if !defined(_M_IX86) || !defined(_MSC_VER) || _MSC_VER != 1500
#error This startup adapter requires the reviewed x86 VC9 compiler.
#endif

typedef char fnv_direct_pointer_width_must_be_32[(sizeof(void*) == 4) ? 1 : -1];
typedef char fnv_direct_uint_width_must_be_32[(sizeof(unsigned int) == 4) ? 1 : -1];
typedef char fnv_direct_int_width_must_be_32[(sizeof(int) == 4) ? 1 : -1];

// Match the original source's C++ linkage, four-dword stdcall declaration.
int __stdcall FUN_0086a850(unsigned int, unsigned int, unsigned int, unsigned int);

extern "C" int WINAPI WinMain(HINSTANCE instance, HINSTANCE previous_instance,
                             LPSTR command_tail, int show_state)
{
    return FUN_0086a850(
        reinterpret_cast<unsigned int>(instance),
        reinterpret_cast<unsigned int>(previous_instance),
        reinterpret_cast<unsigned int>(command_tail),
        static_cast<unsigned int>(show_state));
}
