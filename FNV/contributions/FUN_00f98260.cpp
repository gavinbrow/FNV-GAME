extern bool __cdecl SetSlotValueIfEmpty(int slot, int value);
extern "C" bool DAT_011dbed8;
extern "C" void FUN_0080c260();

// @fnv 0x00f98260
void __cdecl FUN_00f98260()
{
    DAT_011dbed8 = SetSlotValueIfEmpty(3, reinterpret_cast<int>(&FUN_0080c260));
}