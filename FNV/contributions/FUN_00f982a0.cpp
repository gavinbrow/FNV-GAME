extern bool __cdecl SetSlotValueIfEmpty(int slot, int value);
extern "C" bool DAT_011dbf38;
extern "C" void FUN_0080c360();

// @fnv 0x00f982a0
void __cdecl FUN_00f982a0()
{
    DAT_011dbf38 = SetSlotValueIfEmpty(31, reinterpret_cast<int>(&FUN_0080c360));
}