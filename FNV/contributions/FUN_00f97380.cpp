extern bool __cdecl SetSlotValueIfEmpty(int slot, int value);
extern "C" bool DAT_011dbc34;
extern "C" void FUN_0080ac70();

// @fnv 0x00f97380
void __cdecl FUN_00f97380()
{
    DAT_011dbc34 = SetSlotValueIfEmpty(6, reinterpret_cast<int>(&FUN_0080ac70));
}