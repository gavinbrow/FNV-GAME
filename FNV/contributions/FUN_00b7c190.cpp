extern unsigned char DAT_011ad80c;
extern int DAT_011f953c;
extern int DAT_011f9540;
extern unsigned char DAT_011f9425;
extern int DAT_011f9428;
void __stdcall FUN_00e7def0(int);
typedef void (__stdcall *FUN_00b7c190_VFn)(void*, int, int, int);

void __stdcall FUN_00b7c190(int index)
{
    SlotGlobal* global = (SlotGlobal*)DAT_0126f74c;
    SlotElem* element = global->m_24[index];
    int* source;

    if (DAT_011ad80c)
        source = &DAT_011f953c;
    else
        source = &DAT_011f9540;

    element->m_08 = *source;

    if (DAT_011f9425)
        FUN_00e7def0(7);

    void* object = *(void**)((char*)DAT_011f4748 + 0x288);
    void** vtable = *(void***)object;
    ((FUN_00b7c190_VFn)vtable[69])(object, index, 8, DAT_011f9428);
}