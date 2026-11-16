extern bool __cdecl SetSlotValueIfEmpty(int aiIndex, int aiValue);
extern "C" void __cdecl FUN_008085f0();
extern bool DAT_011dbbc8;

// @fnv 0x00f97100
void __cdecl FUN_00f97100()
{
    DAT_011dbbc8 = SetSlotValueIfEmpty(18, reinterpret_cast<int>(&FUN_008085f0));
}
