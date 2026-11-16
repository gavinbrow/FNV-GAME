extern bool __cdecl SetSlotValueIfEmpty(int slot, int value);
extern "C" bool DAT_011dcd80;
extern "C" void FUN_0082b110();

// @fnv 0x00f9cf30
void __cdecl FUN_00f9cf30()
{
    DAT_011dcd80 = SetSlotValueIfEmpty(21, reinterpret_cast<int>(&FUN_0082b110));
}