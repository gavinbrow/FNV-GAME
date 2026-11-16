struct SomeClass {
    void* vtbl;
    void** data;
    unsigned short capacity;
    unsigned short size;
    unsigned short firstFree;
    unsigned short grow;

    void* FUN_00a93c50(unsigned int uiIndex);
};

void* SomeClass::FUN_00a93c50(unsigned int uiIndex)
{
    if (uiIndex >= size)
        return 0;

    void* element = data[uiIndex];
    data[uiIndex] = 0;
    if (element)
        firstFree--;

    if (uiIndex == (unsigned short)(size - 1))
        size--;

    return element;
}
