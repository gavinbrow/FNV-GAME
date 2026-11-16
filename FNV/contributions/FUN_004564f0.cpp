int __cdecl _strnicmp(const char* first, const char* second, unsigned int count);

// @fnv 0x004564f0
int __cdecl FUN_004564f0(const char* first, const char* second, unsigned int count)
{
    return _strnicmp(first, second, count);
}
