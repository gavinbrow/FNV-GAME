bool __cdecl SetSlotValueIfEmpty(int slot, int value);
void __cdecl FUN_0080b040();
extern "C" bool DAT_011dbc9c;

// @fnv 0x00f97600
void __cdecl FUN_00f97600()
{
    DAT_011dbc9c = SetSlotValueIfEmpty(12, reinterpret_cast<int>(&FUN_0080b040));
}
