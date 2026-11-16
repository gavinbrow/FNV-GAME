extern bool __cdecl SetSlotValueIfEmpty(int aiIndex, int aiValue);
extern "C" void __cdecl FUN_008273c0();
extern bool DAT_011dcb88;

// @fnv 0x00f9c470
void __cdecl FUN_00f9c470()
{
    DAT_011dcb88 = SetSlotValueIfEmpty(25, reinterpret_cast<int>(&FUN_008273c0));
}
