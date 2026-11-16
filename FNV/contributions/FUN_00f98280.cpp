extern bool __cdecl SetSlotValueIfEmpty(int, int);
extern "C" void FUN_0080c2e0();
extern "C" unsigned char DAT_011dbeda;
// @fnv 0x00f98280
void FUN_00f98280()
{
    DAT_011dbeda = SetSlotValueIfEmpty(30, reinterpret_cast<int>(&FUN_0080c2e0));
}
