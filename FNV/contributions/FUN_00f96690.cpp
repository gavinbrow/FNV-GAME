bool __cdecl SetSlotValueIfEmpty(int slot, int value);
void __cdecl FUN_00802ff0();
extern "C" bool DAT_011db9bc;

// @fnv 0x00f96690
void __cdecl FUN_00f96690()
{
    DAT_011db9bc = SetSlotValueIfEmpty(4, reinterpret_cast<int>(&FUN_00802ff0));
}
