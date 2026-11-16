extern bool __cdecl SetSlotValueIfEmpty(int aiIndex, int aiValue);
extern "C" void __cdecl FUN_0080b4e0();
extern bool DAT_011dbd14;

// @fnv 0x00f97880
void __cdecl FUN_00f97880()
{
    DAT_011dbd14 = SetSlotValueIfEmpty(9, reinterpret_cast<int>(&FUN_0080b4e0));
}
