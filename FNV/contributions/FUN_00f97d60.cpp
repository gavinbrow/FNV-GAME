extern bool __cdecl SetSlotValueIfEmpty(int aiIndex, int aiValue);
extern "C" void __cdecl FUN_0080bbf0();
extern bool DAT_011dbe10;

// @fnv 0x00f97d60
void __cdecl FUN_00f97d60()
{
    DAT_011dbe10 = SetSlotValueIfEmpty(10, reinterpret_cast<int>(&FUN_0080bbf0));
}
