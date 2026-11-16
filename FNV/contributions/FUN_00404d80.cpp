#include <string.h>

// @fnv 0x00404d80
char* FUN_00404d80(char* destination, unsigned int destinationSize, const char* source)
{
    strcpy_s(destination, destinationSize, source);
    return destination;
}
