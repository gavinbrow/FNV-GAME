extern bool __cdecl SetSlotValueIfEmpty(int aiIndex, int aiValue);
extern "C" void __cdecl FUN_00828760();
extern bool DAT_011dcca4;

// @fnv 0x00f9ca30
void __cdecl FUN_00f9ca30()
{
    DAT_011dcca4 = SetSlotValueIfEmpty(19, reinterpret_cast<int>(&FUN_00828760));
}
