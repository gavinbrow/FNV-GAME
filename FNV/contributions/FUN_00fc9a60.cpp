extern "C" void __stdcall FUN_00ec5fce(
    void* elements,
    unsigned int elementSize,
    int elementCount,
    void (__cdecl *destroyElement)());

extern unsigned char DAT_011c7860[];
extern "C" void __cdecl FUN_0045cec0();

// @fnv 0x00fc9a60
void FUN_00fc9a60()
{
    FUN_00ec5fce(DAT_011c7860, 4, 3, FUN_0045cec0);
}
