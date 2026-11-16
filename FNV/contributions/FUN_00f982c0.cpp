extern bool __cdecl SetSlotValueIfEmpty(int slot, int value);
extern "C" bool DAT_011dbed9;
extern "C" void FUN_0080c3e0();

// @fnv 0x00f982c0
void __cdecl FUN_00f982c0()
{
    DAT_011dbed9 = SetSlotValueIfEmpty(32, reinterpret_cast<int>(&FUN_0080c3e0));
}