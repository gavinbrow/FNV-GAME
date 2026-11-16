// @fnv 0x00f9b9f0
extern bool __cdecl SetSlotValueIfEmpty(int slot, int value);
extern "C" bool DAT_011dc998;
extern "C" void __cdecl FUN_008258a0();
void __cdecl FUN_00f9b9f0()
{
    DAT_011dc998 = SetSlotValueIfEmpty(15, reinterpret_cast<int>(&FUN_008258a0));
}
