#include <string.h>

int __cdecl FUN_00a86280(const char** a, const char** b)
{
    if (a == 0)
        return 1;

    if (b == 0)
        return -1;

    return strcmp(*a, *b);
}