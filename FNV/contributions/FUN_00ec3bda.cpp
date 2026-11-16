// @fnv 0x00ec3bda
unsigned short __cdecl FUN_00ec3bda(unsigned short v)
{
    unsigned short a = v << 8;
    unsigned short b = v >> 8;
    a += b;
    return a;
}
