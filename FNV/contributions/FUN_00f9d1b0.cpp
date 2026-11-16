extern bool __cdecl SetSlotValueIfEmpty(int slot, int value);
extern "C" bool DAT_011dce21;
extern "C" void FUN_0082b6d0();

// @fnv 0x00f9d1b0
void __cdecl FUN_00f9d1b0()
{
    DAT_011dce21 = SetSlotValueIfEmpty(27, reinterpret_cast<int>(&FUN_0082b6d0));
}