extern bool __cdecl SetSlotValueIfEmpty(int aiIndex, int aiValue);
extern "C" void __cdecl FUN_0082a0d0();
extern bool DAT_011dcd00;

// @fnv 0x00f9ccb0
void __cdecl FUN_00f9ccb0()
{
    DAT_011dcd00 = SetSlotValueIfEmpty(28, reinterpret_cast<int>(&FUN_0082a0d0));
}
