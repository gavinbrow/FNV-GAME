extern bool __cdecl SetSlotValueIfEmpty(int aiIndex, int aiValue);
extern "C" void __cdecl FUN_0080c730();
extern bool DAT_011dbf7c;

// @fnv 0x00f98540
void __cdecl FUN_00f98540()
{
    DAT_011dbf7c = SetSlotValueIfEmpty(14, reinterpret_cast<int>(&FUN_0080c730));
}
