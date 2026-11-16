struct ByteFlag { bool enabled; };
void __cdecl FUN_00ac3450(int* dest, unsigned int count, int* source) {
    int* pDest;
    ByteFlag current = {}; char tag3; bool remaining = current.enabled; char tag1 = tag3;
    int* value1 = dest; pDest = value1 + count;
    ByteFlag value3 = {}; bool uninitialized = value3.enabled;
    unsigned int tag2 = count; int* pEnd = value1;
    for (; tag2 > 0; --tag2, ++pEnd) { *pEnd = *source; }
}