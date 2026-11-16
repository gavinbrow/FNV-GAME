// @fnv 0x00f9c530
extern bool __cdecl SetSlotValueIfEmpty(int slot, int value);
extern "C" bool DAT_011dcbcc;
extern "C" void __cdecl FUN_00827a40();
void __cdecl FUN_00f9c530()
{
    DAT_011dcbcc = SetSlotValueIfEmpty(1, reinterpret_cast<int>(&FUN_00827a40));
}
