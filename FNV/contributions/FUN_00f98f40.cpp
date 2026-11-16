extern bool __cdecl SetSlotValueIfEmpty(int aiIndex, int aiValue);
extern "C" void __cdecl FUN_0080d880();
extern bool DAT_011dc144;

// @fnv 0x00f98f40
void __cdecl FUN_00f98f40()
{
    DAT_011dc144 = SetSlotValueIfEmpty(23, reinterpret_cast<int>(&FUN_0080d880));
}
