#include <string.h>

// @fnv 0x00401460
void* __cdecl FUN_00401460(void* destination, const void* source, unsigned int byteCount)
{
    return memmove(destination, source, byteCount);
}
