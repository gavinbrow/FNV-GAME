// @fnv 0x00fcb280
extern "C" void __stdcall FUN_00ec5fce(void* array, unsigned int elementSize, int elementCount, void (__cdecl* destructor)());
extern "C" void FUN_0046ffb0();
extern "C" unsigned char DAT_011cb450;
void FUN_00fcb280()
{
    FUN_00ec5fce(&DAT_011cb450, 8, 14, FUN_0046ffb0);
}
