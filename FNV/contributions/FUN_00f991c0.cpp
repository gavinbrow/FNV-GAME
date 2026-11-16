extern bool __cdecl SetSlotValueIfEmpty(int aiIndex, int aiValue);
extern "C" void __cdecl FUN_0080db30();
extern bool DAT_011dc1e8;

// @fnv 0x00f991c0
void __cdecl FUN_00f991c0()
{
    DAT_011dc1e8 = SetSlotValueIfEmpty(2, reinterpret_cast<int>(&FUN_0080db30));
}
