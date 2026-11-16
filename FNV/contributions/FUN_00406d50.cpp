extern "C" int __cdecl strcat_s(
    char* destination,
    unsigned int destinationSize,
    const char* source);

// @fnv 0x00406d50
void __cdecl FUN_00406d50(
    char* destination,
    unsigned int destinationSize,
    const char* source)
{
    strcat_s(destination, destinationSize, source);
}
