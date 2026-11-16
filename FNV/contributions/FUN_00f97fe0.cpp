extern bool __cdecl SetSlotValueIfEmpty(int slot, int value);
extern "C" bool DAT_011dbe51;
extern "C" void FUN_0080bff0();

// @fnv 0x00f97fe0
void __cdecl FUN_00f97fe0()
{
    DAT_011dbe51 = SetSlotValueIfEmpty(33, reinterpret_cast<int>(&FUN_0080bff0));
}