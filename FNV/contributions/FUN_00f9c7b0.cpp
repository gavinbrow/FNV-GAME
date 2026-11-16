extern bool __cdecl SetSlotValueIfEmpty(int aiIndex, int aiValue);
extern "C" void __cdecl FUN_008280a0();
extern bool DAT_011dcc3c;

// @fnv 0x00f9c7b0
void __cdecl FUN_00f9c7b0()
{
    DAT_011dcc3c = SetSlotValueIfEmpty(5, reinterpret_cast<int>(&FUN_008280a0));
}
