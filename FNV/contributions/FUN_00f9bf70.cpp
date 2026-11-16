extern bool __cdecl SetSlotValueIfEmpty(int aiIndex, int aiValue);
extern "C" void __cdecl FUN_00826260();
extern bool DAT_011dcac1;

// @fnv 0x00f9bf70
void __cdecl FUN_00f9bf70()
{
    DAT_011dcac1 = SetSlotValueIfEmpty(17, reinterpret_cast<int>(&FUN_00826260));
}
