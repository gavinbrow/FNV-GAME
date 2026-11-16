extern bool __cdecl SetSlotValueIfEmpty(int aiIndex, int aiValue);
extern "C" void __cdecl FUN_0082bc30();
extern bool DAT_011dcee4;

// @fnv 0x00f9d6b0
void __cdecl FUN_00f9d6b0()
{
    DAT_011dcee4 = SetSlotValueIfEmpty(0, reinterpret_cast<int>(&FUN_0082bc30));
}
